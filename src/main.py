"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

Run from the repo root with:  python -m src.main
"""

from src.recommender import load_songs, recommend_songs

PROFILES = {
    "Default (pop/happy)": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
        "target_valence": 0.80,
        "target_tempo_bpm": 120,
    },
    "Gym-goer (main)": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "target_valence": 0.50,
        "target_tempo_bpm": 140,
    },
    "Late-night studier (contrast)": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.38,
        "target_valence": 0.58,
        "target_tempo_bpm": 78,
    },
    "Sad gym rat (edge case)": {
        "favorite_genre": "folk",
        "favorite_mood": "sad",
        "target_energy": 0.95,
        "target_valence": 0.25,
        "target_tempo_bpm": 165,
    },
    "Loud lofi (edge case)": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.95,
        "target_valence": 0.60,
        "target_tempo_bpm": 150,
    },
    "Genre not in catalog (edge case)": {
        "favorite_genre": "k-pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
        "target_valence": 0.80,
        "target_tempo_bpm": 120,
    },
    "Middle of the road (edge case)": {
        "favorite_genre": "jazz",
        "favorite_mood": "relaxed",
        "target_energy": 0.50,
        "target_valence": 0.50,
        "target_tempo_bpm": 100,
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in PROFILES.items():
        print(f"\n=== {name} ===")
        print(
            f"Profile: genre={user_prefs['favorite_genre']}, "
            f"mood={user_prefs['favorite_mood']}, "
            f"energy={user_prefs['target_energy']}, "
            f"valence={user_prefs['target_valence']}, "
            f"tempo={user_prefs['target_tempo_bpm']}"
        )
        print("Top recommendations:\n")
        for i, (song, score, explanation) in enumerate(recommend_songs(user_prefs, songs, k=5), start=1):
            print(f"{i}. {song['title']} by {song['artist']} - Score: {score:.2f}")
            for reason in explanation.split("; "):
                print(f"     - {reason}")


if __name__ == "__main__":
    main()
