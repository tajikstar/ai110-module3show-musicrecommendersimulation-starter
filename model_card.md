# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

---

## 2. Goal / Task, Intended Use and Non-Intended Use  

**Goal / task.** VibeMatch suggests the top 5 songs from a small catalog. It predicts which songs a listener will like. The listener is described by a taste profile: a favorite genre, a favorite mood, and target energy, valence (how positive a song sounds), and tempo. Each suggestion comes with a short explanation of why it scored well.

**Intended use.** This is a classroom project. It helps explore how recommenders turn data into suggestions. It assumes the user can name one favorite genre and one favorite mood. It also assumes those tastes stay the same all the time.

**Non-intended use.** It should not be used for a real music app or for real listeners. The catalog is far too small. It should not be used to judge artists or to decide which music gets promoted. It should not be treated as a fair picture of anyone's taste, because it uses invented songs and a single hand-picked set of weights.

---

## 3. How the Model Works  

Every song gets a score between 0 and 1 for how well it fits the listener, and the five highest scores are shown.

The score adds up five parts. A matching genre is worth the most (30%), a matching mood is worth 20%, and three "closeness" parts reward songs whose energy (25%), positivity (15%), and tempo (10%) are near what the listener wants. Closeness means a song only earns full points when it is right on target. Being much higher or much lower both lose points, so the system does not just favor the loudest or fastest song.

In plain terms: the program goes through the catalog one song at a time and acts like a judge with a scorecard. It awards points for each thing a song gets right, writes down every reason it gave points (for example "genre match (+0.30)"), adds them up, and then lines all the songs up from best to worst. The reasons are printed beside each recommendation so the listener can see exactly why a song was picked.

Compared with the starter code, which returned the first songs in the file, this version actually scores and ranks every song and writes out the reasons.

---

## 4. Data  

The catalog has 18 songs in `data/songs.csv`. The starter file had 10 songs, and I added 8 to cover genres and moods it lacked.

- **Genres:** pop, indie pop, lofi, rock, ambient, jazz, synthwave, hip-hop, classical, country, r&b, metal, edm, folk, reggae.
- **Moods:** happy, chill, intense, relaxed, moody, focused, confident, peaceful, nostalgic, romantic, angry, euphoric, sad.

The new songs were written by hand (with AI help) to fit each genre, so the numbers are plausible but invented. Missing from the data: lyrics, language, artist popularity, release year, and anything about how real people actually listen. Most genres have only one or two songs.

---

## 5. Strengths  

- It separates very different listeners. The Gym-goer and the Late-night studier received completely different top 5 lists.
- When a profile fits the catalog, the top result is convincing: "Storm Runner" scored 0.98 for the Gym-goer and "Midnight Coding" scored 0.99 for the Studier.
- Each result comes with reasons, so it is easy to see why a song ranked where it did.
- Closeness scoring behaved as intended: "Gym Hero" (energy 0.93) ranked second for a 0.90 energy target for good reasons, not just because its energy was high.

---

## 6. Limitations and Bias 

**Main weakness found: a few "high-energy, high-positivity" songs show up for almost everyone.** Across the seven test profiles, "Gym Hero" appeared in the top 5 of five of them and "Pulse Garden" in four, including for listeners who never asked for either song. Energy, valence, and tempo are scored by closeness on a 0-to-1 scale, so a loud, upbeat, fast song earns most of its points no matter what the listener's taste is, as long as the listener wants something energetic. Because genre and mood are all-or-nothing, a song that fails both still collects about 0.40 to 0.45 from the numbers alone. The effect is a mild filter bubble: energetic listeners keep seeing the same few songs, and the catalog's less typical songs rarely surface.

Other limitations:

- **Tiny, uneven catalog.** Only one rock song exists, so after the first result the Gym-goer's list is filled with songs that match on mood or numbers rather than genre. The Studier has three lofi songs, so they get a fuller list.
- **Exact-match labels.** "Indie pop" earns no genre credit for a "pop" fan, and "relaxed" earns nothing for a "chill" listener, even though they sound alike.
- **Labels can outvote sound.** Genre plus mood is 50% of the score. In the experiments, lowering the genre weight from 0.30 to 0.05 nearly erased the lead of the folk song for the conflicting "Sad gym rat" profile (0.67 vs 0.65 for a loud metal song).
- **One taste per user.** A listener who likes both rock and lofi cannot be described.
- **Unused features.** `danceability` and `acousticness` are ignored, and the `likes_acoustic` field in `UserProfile` has no effect.
- **Invented data.** The 8 added songs reflect my idea of each genre, which carries my own assumptions about what a genre "sounds like".

---

## 7. Evaluation  

**Profiles tested (seven).** Default pop/happy, Gym-goer, Late-night studier, and four edge cases: "Sad gym rat" (folk, sad, but wants loud and fast), "Loud lofi" (lofi and chill, but wants energy 0.95 and 150 BPM), "Genre not in catalog" (k-pop, which does not exist in the data), and "Middle of the road" (jazz, relaxed, everything medium). The full terminal output for each is in the README under "Sample Recommendation Output". I also checked that the two automated tests in `tests/test_recommender.py` pass.

**Does it feel right?** Mostly yes. Pop/happy returned "Sunrise City", which matches on everything. The Studier got the three lofi songs first, then the ambient and jazz songs that sound alike. Jazz/relaxed got "Coffee Shop Stories", a jazz song with a relaxed mood, at 0.93.

**What surprised me.**

- **"Gym Hero" keeps showing up.** For a listener who just wants happy pop, "Gym Hero" ranks second. It is a pop song, so it gets the genre points, and it is very energetic and upbeat, so it earns almost full points for energy and positivity too. It is intense, not happy, so it loses the mood points, but that only costs 0.20. In plain terms, the system sees "pop, high energy, bright" and does not notice that the vibe is a workout, not a sunny afternoon. It also appears for the Gym-goer, the Sad gym rat, and the Loud lofi listener, so it behaves like a safe default for anyone who wants energy.
- **An unknown genre does not break it.** For "k-pop", nobody gets genre points, so the ranking falls back on mood and the numbers. The result (Sunrise City, Rooftop Lights) is sensible, but top scores fall to 0.69 from 0.99, since 0.30 of the score is out of reach.
- **Conflicting tastes: labels win.** The Sad gym rat gets a quiet folk song first (0.75) even though the listener wants energy 0.95 and 165 BPM, because genre and mood together are worth 0.50. The Loud lofi listener gets the three quiet, slow lofi songs ahead of loud songs for the same reason.

**Comparing pairs of profiles.**

- **Gym-goer vs. Late-night studier:** the top 5 lists share no songs. The Gym-goer's list is loud and fast (energy 0.75 to 0.97, tempo 110 to 168 BPM), while the Studier's list is quiet and slow (energy 0.28 to 0.42, tempo 60 to 90 BPM). That is the right outcome, since the two profiles are opposites.
- **Pop/happy vs. Genre not in catalog (k-pop):** the same numbers and mood, but the k-pop listener's top two are "Sunrise City" and "Rooftop Lights", and "Gym Hero" falls to third. Without a pop genre match, "Gym Hero" loses its 0.30 head start and the happy songs overtake it, which makes sense.
- **Late-night studier vs. Loud lofi:** the same genre and mood, so the same top three songs, but their scores drop from 0.99 to 0.79. The system is honest that they are weaker matches, but it never leaves lofi, so it cannot find the loud songs the listener really asked for until position four.
- **Gym-goer vs. Sad gym rat:** both want very energetic songs, but the Gym-goer wants rock and intense, so "Storm Runner" wins at 0.98. The Sad gym rat's genre and mood point to a quiet folk song, which wins at 0.75, and the loud songs it wanted follow behind. The comparison shows that the label matches decide who wins when taste conflicts.
- **Middle of the road vs. everyone else:** the medium-energy profile has the most diverse top 5 (jazz, reggae, country, lofi, r&b), because mid-range numbers are close to many songs. High-energy profiles share more songs, since fewer songs live at the top of the scale.

**Experiment: double energy, halve genre** (energy weight 0.25 to 0.50, genre weight 0.30 to 0.15; scores stay valid between 0 and 1, because the total is divided by the sum of the weights used).

| Profile | Before (top 3) | After (top 3) |
|---|---|---|
| Default pop/happy | Sunrise City, Gym Hero, Rooftop Lights | Sunrise City, **Rooftop Lights**, Gym Hero |
| Gym-goer | Storm Runner, Gym Hero, Night Drive Loop | Storm Runner, Gym Hero, **Pulse Garden** |
| Sad gym rat | Porch Light Lullaby, Iron Requiem, Storm Runner | **Iron Requiem**, Porch Light Lullaby, Storm Runner |
| Loud lofi | Midnight Coding, Library Rain, Focus Flow | Midnight Coding, Library Rain, **Storm Runner** |

The change made the results **more accurate for conflicting profiles, but not clearly better for everyone**. The Sad gym rat now gets the loud, fast, dark metal song first, which is closer to what they asked for, and "Rooftop Lights" (happy) climbs above "Gym Hero" for pop/happy, which feels right. But "Gym Hero" and "Pulse Garden" gained ground for the Gym-goer, so the repeat-song problem got slightly worse. Earlier single-weight tests (genre 0.05 and 0.60, and removing valence and tempo) are in the README's "Experiments" section.

---

## 8. Future Work  

- Allow several favorite genres and moods, and give partial credit to similar ones (pop and indie pop).
- Use `danceability` and `acousticness`, and make `likes_acoustic` do something.
- Add diversity so the top 5 are not near-duplicates.
- Expand the catalog, especially genres that have only one song.
- Add collaborative signals such as skips and likes, which would also fix the cold-start gap in the other direction.

---

## 9. Personal Reflection  

**Biggest learning moment.** A recommender is mostly a set of choices written as numbers. Someone decides which features count, what "close" means, and how much each feature is worth. Changing one weight was enough to change the answer for a listener with conflicting tastes. That showed me the weights are opinions, not facts.

**How AI helped, and when I double-checked it.** AI helped me plan the algorithm, write the code, invent 8 extra songs, and draft the documentation. It saved a lot of time. But I had to check its work. After adding songs, the tempo range changed from 92 to 108 BPM, so the formula had to be updated. The assignment's example said a bias might come from "60% of the dataset being pop", but only 2 of my 18 songs are pop, so I wrote about the problem I actually found. I also ran the code and the tests myself instead of trusting that it worked.

**What surprised me.** A simple point system can still feel like a real recommendation. When "Sunrise City" came out on top for a happy pop fan, it felt right. The "Because:" lines made it feel even more convincing. But it is only adding up points. It does not understand music, and it keeps suggesting "Gym Hero" to people who only want happy pop.

**What I would try next.** I would let users have several favorite genres, give partial credit to similar genres, and add more songs. I would also try a diversity rule so the top 5 are not all alike. After that, I would try adding a "skips" signal to get a taste of collaborative filtering.
