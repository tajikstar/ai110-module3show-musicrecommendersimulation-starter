# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This version is a **content-based** music recommender. It reads an 18-song catalog (`data/songs.csv`), compares each song to a user's taste profile (favorite genre and mood, plus target energy, valence, and tempo), and returns the top 5 songs with a plain-language explanation of why each one scored well. It was tested on three profiles: a gym-goer, a late-night studier, and a deliberately conflicting edge case.

---

## How The System Works

### How real-world recommenders work

Platforms like Spotify and YouTube predict what you will like next by combining two main approaches. **Collaborative filtering** uses the behavior of many users: if people who share your listening history loved a song you have not heard, it is probably a good guess for you. It relies on behavior data such as likes, skips, replays, and playlist adds. **Content-based filtering** looks at the attributes of the songs themselves (genre, mood, tempo, energy) and finds songs similar to what you already enjoy. Collaborative filtering struggles with the "cold start" problem, because a brand-new song has no behavior data yet, while content-based filtering can recommend it right away. At scale, real systems learn how much each signal matters from millions of listens.

### What this version prioritizes

This simulation is **content-based only**. There is no user behavior data, just a small catalog of songs (`data/songs.csv`) described by their attributes. It compares each song to a user's taste profile and prioritizes genre first, then mood, then how close the numeric "vibe" features (energy, valence, tempo) are to what the user wants.

### Features

**`Song`** stores: `id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`, plus five advanced features: `popularity` (0-100), `release_decade` (1970-2020), `mood_tags` (detailed tags like "nostalgic" or "aggressive"), `instrumentalness` (0-1), and `language`.

**`UserProfile`** stores the same kinds of attributes as the songs, so the two can be compared: a favorite `genre`, a favorite `mood`, and target values for `energy`, `valence`, and `tempo_bpm`. It can also set optional targets for the advanced features: `favorite_tags`, `target_popularity`, `target_decade`, `target_instrumentalness`, and `preferred_language`.

### Scoring rule (one song)

Each song gets a score between 0 and 1, which is a weighted sum:

| Feature | How it is scored | Weight |
|---|---|---|
| Genre | 1 if it matches the user's genre, otherwise 0 | 0.30 |
| Mood | 1 if it matches the user's mood, otherwise 0 | 0.20 |
| Energy | `1 - abs(song - target)` | 0.25 |
| Valence | `1 - abs(song - target)` | 0.15 |
| Tempo | `1 - abs(song - target) / 108` (108 = range of tempos in the catalog, 60 to 168 BPM, so tempo is normalized to 0-1) | 0.10 |
| Mood tags *(optional)* | share of the user's favorite tags that the song has | 0.10 |
| Popularity *(optional)* | `1 - abs(song - target) / 100` | 0.05 |
| Decade *(optional)* | `1 - abs(song - target) / 50` (1970 to 2020) | 0.05 |
| Instrumentalness *(optional)* | `1 - abs(song - target)` | 0.05 |
| Language *(optional)* | 1 if it matches the user's language, otherwise 0 | 0.05 |

The optional rows only count when the user sets the matching target. If a target is missing, that weight is left out and the score is rescaled, so profiles without advanced preferences score exactly as before.

Closeness scoring rewards songs that are *near* the user's target, not songs that simply have a higher or lower value. Genre is weighted highest because it is the broadest signal of taste, and mood is weighted lower because it is more situational.

### Ranking rule (list of songs)

The scoring rule only rates one song at a time. The ranking rule scores every song in the catalog, sorts them from highest to lowest score, and returns the top *k* as the recommendations. Ties are broken alphabetically by title.

### Data flow

```
INPUT: user profile (genre, mood, target energy / valence / tempo)
   |
PROCESS: loop over every song in data/songs.csv -> score_song() -> (score, reasons)
   |
OUTPUT: sort by score, highest first -> top k recommendations with explanations
```

### Test profiles

- **Gym-goer (main):** rock, intense, energy 0.90, valence 0.50, tempo 140
- **Late-night studier (contrast):** lofi, chill, energy 0.38, valence 0.58, tempo 78
- **Sad gym rat (edge case):** folk, sad, energy 0.95, valence 0.25, tempo 165. Genre and mood point to a quiet song while the numbers point to a loud one.

### Expected biases

- **Genre and mood together are worth 0.50 of the score**, so the system may over-prioritize labels and bury songs from another genre that match the user's energy and tempo perfectly.
- **Exact-match labels are all-or-nothing.** "Indie pop" gets no credit for a "pop" fan, and "chill" gets none for a "relaxed" listener.
- **Tiny, uneven catalog (18 songs).** There is only one rock song, so after the top result the Gym-goer's list is filled by songs that merely match on mood or numbers.
- **One favorite genre and mood per user.** Real listeners like several.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
Loaded songs: 18

=== Default (pop/happy) ===
Profile: genre=pop, mood=happy, energy=0.8, valence=0.8, tempo=120
Top recommendations:

1. Sunrise City by Neon Echo - Score: 0.99
     - genre match (+0.30)
     - mood match (+0.20)
     - energy 0.82 vs target 0.80 (+0.25)
     - valence 0.84 vs target 0.80 (+0.14)
     - tempo 118 vs target 120 BPM (+0.10)
2. Gym Hero by Max Pulse - Score: 0.75
     - genre match (+0.30)
     - energy 0.93 vs target 0.80 (+0.22)
     - valence 0.77 vs target 0.80 (+0.15)
     - tempo 132 vs target 120 BPM (+0.09)
3. Rooftop Lights by Indigo Parade - Score: 0.68
     - mood match (+0.20)
     - energy 0.76 vs target 0.80 (+0.24)
     - valence 0.81 vs target 0.80 (+0.15)
     - tempo 124 vs target 120 BPM (+0.10)
4. Pulse Garden by Hexa Bloom - Score: 0.45
     - energy 0.94 vs target 0.80 (+0.22)
     - valence 0.88 vs target 0.80 (+0.14)
     - tempo 128 vs target 120 BPM (+0.09)
5. Concrete Crown by Verse Theory - Score: 0.44
     - energy 0.78 vs target 0.80 (+0.24)
     - valence 0.62 vs target 0.80 (+0.12)
     - tempo 92 vs target 120 BPM (+0.07)
```

This is the first of seven profiles in the full output. The other six are below, and `python -m src.main` prints all of them.

### Output for the other profiles

**Gym-goer (main)**

```
=== Gym-goer (main) ===
Profile: genre=rock, mood=intense, energy=0.9, valence=0.5, tempo=140
Top recommendations:

1. Storm Runner by Voltline - Score: 0.98
     - genre match (+0.30)
     - mood match (+0.20)
     - energy 0.91 vs target 0.90 (+0.25)
     - valence 0.48 vs target 0.50 (+0.15)
     - tempo 152 vs target 140 BPM (+0.09)
2. Gym Hero by Max Pulse - Score: 0.64
     - mood match (+0.20)
     - energy 0.93 vs target 0.90 (+0.24)
     - valence 0.77 vs target 0.50 (+0.11)
     - tempo 132 vs target 140 BPM (+0.09)
3. Night Drive Loop by Neon Echo - Score: 0.43
     - energy 0.75 vs target 0.90 (+0.21)
     - valence 0.49 vs target 0.50 (+0.15)
     - tempo 110 vs target 140 BPM (+0.07)
4. Iron Requiem by Black Furnace - Score: 0.43
     - energy 0.97 vs target 0.90 (+0.23)
     - valence 0.30 vs target 0.50 (+0.12)
     - tempo 168 vs target 140 BPM (+0.07)
5. Pulse Garden by Hexa Bloom - Score: 0.42
     - energy 0.94 vs target 0.90 (+0.24)
     - valence 0.88 vs target 0.50 (+0.09)
     - tempo 128 vs target 140 BPM (+0.09)
```

**Late-night studier (contrast)**

```
=== Late-night studier (contrast) ===
Profile: genre=lofi, mood=chill, energy=0.38, valence=0.58, tempo=78
Top recommendations:

1. Midnight Coding by LoRoom - Score: 0.99
     - genre match (+0.30)
     - mood match (+0.20)
     - energy 0.42 vs target 0.38 (+0.24)
     - valence 0.56 vs target 0.58 (+0.15)
     - tempo 78 vs target 78 BPM (+0.10)
2. Library Rain by Paper Lanterns - Score: 0.98
     - genre match (+0.30)
     - mood match (+0.20)
     - energy 0.35 vs target 0.38 (+0.24)
     - valence 0.60 vs target 0.58 (+0.15)
     - tempo 72 vs target 78 BPM (+0.09)
3. Focus Flow by LoRoom - Score: 0.79
     - genre match (+0.30)
     - energy 0.40 vs target 0.38 (+0.24)
     - valence 0.59 vs target 0.58 (+0.15)
     - tempo 80 vs target 78 BPM (+0.10)
4. Spacewalk Thoughts by Orbit Bloom - Score: 0.65
     - mood match (+0.20)
     - energy 0.28 vs target 0.38 (+0.23)
     - valence 0.65 vs target 0.58 (+0.14)
     - tempo 60 vs target 78 BPM (+0.08)
5. Coffee Shop Stories by Slow Stereo - Score: 0.47
     - energy 0.37 vs target 0.38 (+0.25)
     - valence 0.71 vs target 0.58 (+0.13)
     - tempo 90 vs target 78 BPM (+0.09)
```

**Sad gym rat (edge case)**

```
=== Sad gym rat (edge case) ===
Profile: genre=folk, mood=sad, energy=0.95, valence=0.25, tempo=165
Top recommendations:

1. Porch Light Lullaby by Willow & Pine - Score: 0.75
     - genre match (+0.30)
     - mood match (+0.20)
     - energy 0.30 vs target 0.95 (+0.09)
     - valence 0.28 vs target 0.25 (+0.15)
     - tempo 76 vs target 165 BPM (+0.02)
2. Iron Requiem by Black Furnace - Score: 0.48
     - energy 0.97 vs target 0.95 (+0.24)
     - valence 0.30 vs target 0.25 (+0.14)
     - tempo 168 vs target 165 BPM (+0.10)
3. Storm Runner by Voltline - Score: 0.44
     - energy 0.91 vs target 0.95 (+0.24)
     - valence 0.48 vs target 0.25 (+0.12)
     - tempo 152 vs target 165 BPM (+0.09)
4. Gym Hero by Max Pulse - Score: 0.39
     - energy 0.93 vs target 0.95 (+0.25)
     - valence 0.77 vs target 0.25 (+0.07)
     - tempo 132 vs target 165 BPM (+0.07)
5. Pulse Garden by Hexa Bloom - Score: 0.37
     - energy 0.94 vs target 0.95 (+0.25)
     - valence 0.88 vs target 0.25 (+0.06)
     - tempo 128 vs target 165 BPM (+0.07)
```

**Loud lofi (edge case)**

```
=== Loud lofi (edge case) ===
Profile: genre=lofi, mood=chill, energy=0.95, valence=0.6, tempo=150
Top recommendations:

1. Midnight Coding by LoRoom - Score: 0.79
     - genre match (+0.30)
     - mood match (+0.20)
     - energy 0.42 vs target 0.95 (+0.12)
     - valence 0.56 vs target 0.60 (+0.14)
     - tempo 78 vs target 150 BPM (+0.03)
2. Library Rain by Paper Lanterns - Score: 0.78
     - genre match (+0.30)
     - mood match (+0.20)
     - energy 0.35 vs target 0.95 (+0.10)
     - valence 0.60 vs target 0.60 (+0.15)
     - tempo 72 vs target 150 BPM (+0.03)
3. Focus Flow by LoRoom - Score: 0.60
     - genre match (+0.30)
     - energy 0.40 vs target 0.95 (+0.11)
     - valence 0.59 vs target 0.60 (+0.15)
     - tempo 80 vs target 150 BPM (+0.04)
4. Storm Runner by Voltline - Score: 0.47
     - energy 0.91 vs target 0.95 (+0.24)
     - valence 0.48 vs target 0.60 (+0.13)
     - tempo 152 vs target 150 BPM (+0.10)
5. Gym Hero by Max Pulse - Score: 0.45
     - energy 0.93 vs target 0.95 (+0.25)
     - valence 0.77 vs target 0.60 (+0.12)
     - tempo 132 vs target 150 BPM (+0.08)
```

**Genre not in catalog (edge case)**

```
=== Genre not in catalog (edge case) ===
Profile: genre=k-pop, mood=happy, energy=0.8, valence=0.8, tempo=120
Top recommendations:

1. Sunrise City by Neon Echo - Score: 0.69
     - mood match (+0.20)
     - energy 0.82 vs target 0.80 (+0.25)
     - valence 0.84 vs target 0.80 (+0.14)
     - tempo 118 vs target 120 BPM (+0.10)
2. Rooftop Lights by Indigo Parade - Score: 0.68
     - mood match (+0.20)
     - energy 0.76 vs target 0.80 (+0.24)
     - valence 0.81 vs target 0.80 (+0.15)
     - tempo 124 vs target 120 BPM (+0.10)
3. Gym Hero by Max Pulse - Score: 0.45
     - energy 0.93 vs target 0.80 (+0.22)
     - valence 0.77 vs target 0.80 (+0.15)
     - tempo 132 vs target 120 BPM (+0.09)
4. Pulse Garden by Hexa Bloom - Score: 0.45
     - energy 0.94 vs target 0.80 (+0.22)
     - valence 0.88 vs target 0.80 (+0.14)
     - tempo 128 vs target 120 BPM (+0.09)
5. Concrete Crown by Verse Theory - Score: 0.44
     - energy 0.78 vs target 0.80 (+0.24)
     - valence 0.62 vs target 0.80 (+0.12)
     - tempo 92 vs target 120 BPM (+0.07)
```

**Nostalgic throwback (advanced features)**. This profile also sets mood tags, popularity, decade, instrumentalness, and language.

```
=== Nostalgic throwback (advanced features) ===
Profile: genre=country, mood=nostalgic, energy=0.5, valence=0.6, tempo=95
Top recommendations:

1. Dust Road Home by Hollis Creek - Score: 0.98
     - genre match (+0.30)
     - mood match (+0.20)
     - energy 0.55 vs target 0.50 (+0.24)
     - valence 0.68 vs target 0.60 (+0.14)
     - tempo 98 vs target 95 BPM (+0.10)
     - mood tags shared: nostalgic, warm (+0.10)
     - popularity 63 vs target 60 (+0.05)
     - decade 1990s vs target 1990s (+0.05)
     - instrumentalness 0.06 vs target 0.10 (+0.05)
     - language match: English (+0.05)
2. Coffee Shop Stories by Slow Stereo - Score: 0.54
     - energy 0.37 vs target 0.50 (+0.22)
     - valence 0.71 vs target 0.60 (+0.13)
     - tempo 90 vs target 95 BPM (+0.10)
     - mood tags shared: nostalgic, warm (+0.10)
     - popularity 49 vs target 60 (+0.04)
     - decade 2000s vs target 1990s (+0.04)
     - instrumentalness 0.55 vs target 0.10 (+0.03)
     - language match: English (+0.05)
3. Velvet Hours by Amara Lux - Score: 0.53
     - energy 0.52 vs target 0.50 (+0.24)
     - valence 0.72 vs target 0.60 (+0.13)
     - tempo 86 vs target 95 BPM (+0.09)
     - mood tags shared: warm (+0.05)
     - popularity 77 vs target 60 (+0.04)
     - decade 2010s vs target 1990s (+0.03)
     - instrumentalness 0.04 vs target 0.10 (+0.05)
     - language match: English (+0.05)
4. Island Drift by Sun Lantern - Score: 0.49
     - energy 0.48 vs target 0.50 (+0.24)
     - valence 0.80 vs target 0.60 (+0.12)
     - tempo 82 vs target 95 BPM (+0.09)
     - mood tags shared: warm (+0.05)
     - popularity 68 vs target 60 (+0.05)
     - decade 2000s vs target 1990s (+0.04)
     - instrumentalness 0.10 vs target 0.10 (+0.05)
5. Night Drive Loop by Neon Echo - Score: 0.48
     - energy 0.75 vs target 0.50 (+0.19)
     - valence 0.49 vs target 0.60 (+0.13)
     - tempo 110 vs target 95 BPM (+0.09)
     - mood tags shared: nostalgic (+0.05)
     - popularity 66 vs target 60 (+0.05)
     - decade 2010s vs target 1990s (+0.03)
     - instrumentalness 0.40 vs target 0.10 (+0.03)
     - language match: English (+0.05)
```

**Middle of the road (edge case)**

```
=== Middle of the road (edge case) ===
Profile: genre=jazz, mood=relaxed, energy=0.5, valence=0.5, tempo=100
Top recommendations:

1. Coffee Shop Stories by Slow Stereo - Score: 0.93
     - genre match (+0.30)
     - mood match (+0.20)
     - energy 0.37 vs target 0.50 (+0.22)
     - valence 0.71 vs target 0.50 (+0.12)
     - tempo 90 vs target 100 BPM (+0.09)
2. Island Drift by Sun Lantern - Score: 0.63
     - mood match (+0.20)
     - energy 0.48 vs target 0.50 (+0.24)
     - valence 0.80 vs target 0.50 (+0.10)
     - tempo 82 vs target 100 BPM (+0.08)
3. Dust Road Home by Hollis Creek - Score: 0.46
     - energy 0.55 vs target 0.50 (+0.24)
     - valence 0.68 vs target 0.50 (+0.12)
     - tempo 98 vs target 100 BPM (+0.10)
4. Midnight Coding by LoRoom - Score: 0.45
     - energy 0.42 vs target 0.50 (+0.23)
     - valence 0.56 vs target 0.50 (+0.14)
     - tempo 78 vs target 100 BPM (+0.08)
5. Velvet Hours by Amara Lux - Score: 0.45
     - energy 0.52 vs target 0.50 (+0.24)
     - valence 0.72 vs target 0.50 (+0.12)
     - tempo 86 vs target 100 BPM (+0.09)
```

For the default pop/happy profile, the top result is "Sunrise City", the only song that matches on genre, mood, and every number. "Gym Hero" is second because it is pop but intense, not happy.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

All experiments changed one weight at a time and re-ran the Gym-goer and the Sad gym rat.

| Experiment | Gym-goer top 3 | Sad gym rat top 3 |
|---|---|---|
| Baseline (genre 0.30) | Storm Runner 0.98, Gym Hero 0.64, Night Drive Loop 0.43 | Porch Light Lullaby 0.75, Iron Requiem 0.48, Storm Runner 0.44 |
| Genre weight 0.05 | Storm Runner 0.98, Gym Hero 0.86, Night Drive Loop 0.58 | Porch Light Lullaby 0.67, Iron Requiem 0.65, Storm Runner 0.59 |
| Genre weight 0.60 | Storm Runner 0.99, Gym Hero 0.50, Night Drive Loop 0.33 | Porch Light Lullaby 0.81, Iron Requiem 0.37, Storm Runner 0.34 |
| Valence and tempo removed | Storm Runner 1.00, Gym Hero 0.59, Pulse Garden 0.32 | Porch Light Lullaby 0.78, Pulse Garden 0.33, Gym Hero 0.33 |

What I noticed:

- **Genre weight controls the edge case.** With genre at 0.05, the Sad gym rat's folk song barely beats the loud metal song (0.67 vs 0.65). At 0.60 it wins easily. The labels outvote the numbers whenever genre and mood carry enough weight.
- **Storm Runner is first for the Gym-goer in every experiment**, because it matches on every feature. Only the lower ranks move.
- **Removing valence and tempo changed the lower ranks.** "Night Drive Loop" dropped out of the Gym-goer's top 3 and EDM "Pulse Garden" appeared, since valence and tempo are what separate a dark song from a bright one at the same energy.
- **Different users get different lists.** The Gym-goer's and the Studier's top 5 share no songs.

---

## Limitations and Risks

- It only works on a tiny catalog (18 songs), and some genres have a single song, so a genre match can surface only one result.
- It matches genre and mood by exact text, so "indie pop" earns nothing for a "pop" fan and "relaxed" earns nothing for a "chill" listener.
- It uses one favorite genre and one favorite mood per user, so it cannot represent a listener with several tastes.
- It does not use lyrics, artist, or any listening behavior, and it ignores `danceability` and `acousticness`. The advanced features (tags, popularity, decade, instrumentalness, language) only count for profiles that set them.
- Genre and mood together carry 0.50 of the score, so it can over-favor labels over how a song actually sounds.

See [model_card.md](model_card.md) for more detail.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

A recommender turns data into predictions by describing songs and users in the same terms and then measuring how close they are. Most of the work is not the math but the choices behind it: which features count, how close a number must be to earn points, and how much each feature is worth. Changing a single weight (genre from 0.30 to 0.05) was enough to change which song a conflicting profile received, which showed me that the weights are really opinions about what matters.

Bias can come in through the catalog and through the labels. With one rock song and a handful of lofi songs, some users get a full list of good matches while others get a list padded with loose matches. Exact-match labels also treat near-identical tastes ("pop" and "indie pop") as completely different. Real systems face the same problems at a far larger scale, with the added risk that popular songs and groups with more data get recommended more.



