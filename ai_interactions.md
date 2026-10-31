# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Challenge 1: add five or more advanced song attributes to `data/songs.csv` and make the scoring in `src/recommender.py` account for them.

**Prompts used:**

- "Introduce 5 or more complex attributes to your dataset that are not currently present in the baseline data, such as Song Popularity (0-100), Release Decade, or Detailed Mood Tags. Update both data/songs.csv and the scoring logic in src/recommender.py so scoring accounts for the new attributes."
- The user chose this challenge by answering "1" when asked which optional challenges to do.

**What did the agent generate or change?**

- Added five columns to all 18 songs in `data/songs.csv`: `popularity`, `release_decade`, `mood_tags` (separated by `|`), `instrumentalness`, and `language`.
- `src/recommender.py`: extended `Song` and `UserProfile` with optional fields, made `load_songs` convert the new columns (ints, floats, and a list of tags), added five optional weights, and added scoring and "reasons" for each new feature.
- `src/main.py`: added a "Nostalgic throwback (advanced features)" profile that sets every new target.
- `README.md`: documented the new features, weights, and sample output.

**What did you verify or fix manually?**

- The new features are optional, so the existing profiles should be unchanged. I re-ran all of them and confirmed every score matched the earlier output.
- The two tests in `tests/test_recommender.py` still pass, since the new `Song` fields have defaults.
- The first attempt to rewrite `songs.csv` was refused because the file had changed since it was read, so the file was read again before it was rewritten.
- The new profile's top result ("Dust Road Home", 0.98) matches expectations: it is the only song that is country, nostalgic, from the 1990s, and has both of the requested tags.
- The song data for the new columns is invented. It is plausible but is not real data.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

<!-- e.g., Strategy, Factory, Observer, etc. -->

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->
