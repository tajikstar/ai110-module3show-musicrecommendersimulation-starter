import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

# Algorithm Recipe: weights sum to 1.0, so a perfect match scores 1.0.
WEIGHTS = {
    "genre": 0.30,
    "mood": 0.20,
    "energy": 0.25,
    "valence": 0.15,
    "tempo": 0.10,
}

# Tempo range of the catalog (BPM), used to normalize tempo closeness to 0-1.
TEMPO_MIN = 60
TEMPO_MAX = 168
TEMPO_RANGE = TEMPO_MAX - TEMPO_MIN


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_valence: Optional[float] = None
    target_tempo_bpm: Optional[float] = None

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the k songs that score highest for this user, best first."""
        user_prefs = asdict(user)
        ranked = sorted(
            self.songs,
            key=lambda song: (-score_song(user_prefs, asdict(song))[0], song.title),
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain in one line why this song scored the way it did."""
        score, reasons = score_song(asdict(user), asdict(song))
        return f"Score {score:.2f}: " + "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs.csv into a list of dicts, converting numeric columns to int/float."""
    int_fields = ("id",)
    float_fields = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song from 0 to 1 against the user's prefs, returning (score, reasons)."""
    # Valence and tempo targets are optional. If one is missing its weight is
    # left out and the score is rescaled, so a perfect match is still 1.0.
    earned = 0.0
    possible = 0.0
    reasons = []

    possible += WEIGHTS["genre"]
    if song["genre"] == user_prefs["favorite_genre"]:
        earned += WEIGHTS["genre"]
        reasons.append(f"genre match (+{WEIGHTS['genre']:.2f})")

    possible += WEIGHTS["mood"]
    if song["mood"] == user_prefs["favorite_mood"]:
        earned += WEIGHTS["mood"]
        reasons.append(f"mood match (+{WEIGHTS['mood']:.2f})")

    energy_closeness = 1 - abs(song["energy"] - user_prefs["target_energy"])
    possible += WEIGHTS["energy"]
    earned += WEIGHTS["energy"] * energy_closeness
    reasons.append(
        f"energy {song['energy']:.2f} vs target {user_prefs['target_energy']:.2f} "
        f"(+{WEIGHTS['energy'] * energy_closeness:.2f})"
    )

    target_valence = user_prefs.get("target_valence")
    if target_valence is not None:
        valence_closeness = 1 - abs(song["valence"] - target_valence)
        possible += WEIGHTS["valence"]
        earned += WEIGHTS["valence"] * valence_closeness
        reasons.append(
            f"valence {song['valence']:.2f} vs target {target_valence:.2f} "
            f"(+{WEIGHTS['valence'] * valence_closeness:.2f})"
        )

    target_tempo = user_prefs.get("target_tempo_bpm")
    if target_tempo is not None:
        tempo_closeness = max(0.0, 1 - abs(song["tempo_bpm"] - target_tempo) / TEMPO_RANGE)
        possible += WEIGHTS["tempo"]
        earned += WEIGHTS["tempo"] * tempo_closeness
        reasons.append(
            f"tempo {song['tempo_bpm']:.0f} vs target {target_tempo:.0f} BPM "
            f"(+{WEIGHTS['tempo'] * tempo_closeness:.2f})"
        )

    return earned / possible, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, then return the top k as (song, score, explanation), best first."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))

    # Highest score first; ties are broken alphabetically by title.
    scored.sort(key=lambda item: (-item[1], item[0]["title"]))
    return scored[:k]
