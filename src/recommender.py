from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass
import csv

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

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file and converts numeric values to appropriate types.
    Handles both original fields and new advanced features.
    Returns a list of song dictionaries with numeric fields as floats/ints.
    """
    songs = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric columns and handle new features
                song = {
                    'id': int(row['id']),
                    'title': row['title'],
                    'artist': row['artist'],
                    'genre': row['genre'],
                    'mood': row['mood'],
                    'energy': float(row['energy']),
                    'tempo_bpm': int(row['tempo_bpm']),
                    'valence': float(row['valence']),
                    'danceability': float(row['danceability']),
                    'acousticness': float(row['acousticness']),
                    # New features
                    'popularity': float(row.get('popularity', 50)),
                    'release_decade': row.get('release_decade', '2020s'),
                    'artist_id': int(row.get('artist_id', 0)),
                    'mood_tags': row.get('mood_tags', '').split(';'),
                    'year': int(row.get('year', 2020))
                }
                songs.append(song)
    except FileNotFoundError:
        print(f"Error: Could not find file {csv_path}")
        return []
    except Exception as e:
        print(f"Error loading songs: {e}")
        return []
    
    return songs


def score_song(user_prefs: Dict, song: Dict, mode: str = "balanced") -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    
    Three scoring modes available:
    1. "balanced" - Original balanced scoring (default)
    2. "genre-first" - Prioritizes genre match heavily
    3. "mood-first" - Prioritizes mood and vibe
    4. "energy-focused" - Emphasizes energy and danceability
    
    Returns (total_score, list_of_reasons).
    """
    if mode == "genre-first":
        return score_song_genre_first(user_prefs, song)
    elif mode == "mood-first":
        return score_song_mood_first(user_prefs, song)
    elif mode == "energy-focused":
        return score_song_energy_focused(user_prefs, song)
    else:
        return score_song_balanced(user_prefs, song)


def score_song_balanced(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Original balanced scoring from Phase 1:
    - Genre match: +30 points (exact match only)
    - Mood match: +20 points (exact match only)
    - Energy: +15 points (proximity-based)
    - Valence: +10 points (proximity-based)
    - Danceability: +10 points (proximity-based)
    - Acousticness: +5 points (proximity-based)
    """
    total_score = 0.0
    reasons = []
    
    # 1. GENRE MATCH: +30 points (exact match only)
    if user_prefs.get('genre', '').lower() == song['genre'].lower():
        total_score += 30.0
        reasons.append(f"Genre match (+30.0)")
    else:
        reasons.append(f"Genre mismatch (+0)")
    
    # 2. MOOD MATCH: +20 points (exact match only)
    if user_prefs.get('mood', '').lower() == song['mood'].lower():
        total_score += 20.0
        reasons.append(f"Mood match (+20.0)")
    else:
        reasons.append(f"Mood variant (+0)")
    
    # 3. ENERGY: +15 points (proximity-based)
    if 'energy' in user_prefs and isinstance(user_prefs['energy'], (int, float)):
        energy_diff = abs(user_prefs['energy'] - song['energy'])
        energy_score = 15.0 * (1 - energy_diff)
        total_score += energy_score
        reasons.append(f"Energy (+{energy_score:.1f})")
    
    # 4. VALENCE: +10 points (proximity-based)
    if 'valence' in user_prefs and isinstance(user_prefs['valence'], (int, float)):
        valence_diff = abs(user_prefs['valence'] - song['valence'])
        valence_score = 10.0 * (1 - valence_diff)
        total_score += valence_score
        reasons.append(f"Valence (+{valence_score:.1f})")
    
    # 5. DANCEABILITY: +10 points (proximity-based)
    if 'danceability' in user_prefs and isinstance(user_prefs['danceability'], (int, float)):
        dance_diff = abs(user_prefs['danceability'] - song['danceability'])
        dance_score = 10.0 * (1 - dance_diff)
        total_score += dance_score
        reasons.append(f"Danceability (+{dance_score:.1f})")
    
    # 6. ACOUSTICNESS: +5 points (proximity-based)
    if 'acousticness' in user_prefs and isinstance(user_prefs['acousticness'], (int, float)):
        acoustic_diff = abs(user_prefs['acousticness'] - song['acousticness'])
        acoustic_score = 5.0 * (1 - acoustic_diff)
        total_score += acoustic_score
        reasons.append(f"Acousticness (+{acoustic_score:.1f})")
    
    # Bonus: Popularity boosts recent popular songs slightly
    if 'popularity' in song and song.get('popularity', 50) > 75:
        pop_bonus = 2.0
        total_score += pop_bonus
        reasons.append(f"Popularity bonus (+{pop_bonus:.1f})")
    
    return (total_score, reasons)


def score_song_genre_first(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Genre-First mode: Prioritizes genre heavily. If genre matches perfectly, 
    it gets a major score boost.
    """
    total_score = 0.0
    reasons = []
    
    # 1. GENRE MATCH: +45 points (heavily weighted)
    if user_prefs.get('genre', '').lower() == song['genre'].lower():
        total_score += 45.0
        reasons.append(f"Genre match (+45.0)")
    else:
        reasons.append(f"Genre mismatch (+0)")
    
    # 2. MOOD MATCH: +15 points
    if user_prefs.get('mood', '').lower() == song['mood'].lower():
        total_score += 15.0
        reasons.append(f"Mood match (+15.0)")
    else:
        reasons.append(f"Mood variant (+0)")
    
    # 3. ENERGY: +12 points
    if 'energy' in user_prefs and isinstance(user_prefs['energy'], (int, float)):
        energy_diff = abs(user_prefs['energy'] - song['energy'])
        energy_score = 12.0 * (1 - energy_diff)
        total_score += energy_score
        reasons.append(f"Energy (+{energy_score:.1f})")
    
    # 4. Other features: less weight
    if 'valence' in user_prefs and isinstance(user_prefs['valence'], (int, float)):
        valence_diff = abs(user_prefs['valence'] - song['valence'])
        valence_score = 6.0 * (1 - valence_diff)
        total_score += valence_score
        reasons.append(f"Valence (+{valence_score:.1f})")
    
    if 'danceability' in user_prefs and isinstance(user_prefs['danceability'], (int, float)):
        dance_diff = abs(user_prefs['danceability'] - song['danceability'])
        dance_score = 6.0 * (1 - dance_diff)
        total_score += dance_score
        reasons.append(f"Danceability (+{dance_score:.1f})")
    
    if 'acousticness' in user_prefs and isinstance(user_prefs['acousticness'], (int, float)):
        acoustic_diff = abs(user_prefs['acousticness'] - song['acousticness'])
        acoustic_score = 3.0 * (1 - acoustic_diff)
        total_score += acoustic_score
        reasons.append(f"Acousticness (+{acoustic_score:.1f})")
    
    return (total_score, reasons)


def score_song_mood_first(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Mood-First mode: Focuses on matching the user's mood and vibe. 
    Also checks mood tags for deeper mood matching.
    """
    total_score = 0.0
    reasons = []
    
    # 1. MOOD MATCH: +40 points (heavily weighted)
    if user_prefs.get('mood', '').lower() == song['mood'].lower():
        total_score += 40.0
        reasons.append(f"Mood match (+40.0)")
    else:
        reasons.append(f"Mood variant (+0)")
    
    # 2. Check mood tags for additional points
    mood_tags = song.get('mood_tags', [])
    if 'mood_tags' in user_prefs:
        user_tags = user_prefs['mood_tags']  # list like ['peaceful', 'calm']
        matching_tags = len(set(user_tags) & set(mood_tags))
        if matching_tags > 0:
            tag_bonus = matching_tags * 8.0
            total_score += tag_bonus
            reasons.append(f"Mood tags match (+{tag_bonus:.1f})")
    
    # 3. VALENCE: +12 points (affects mood)
    if 'valence' in user_prefs and isinstance(user_prefs['valence'], (int, float)):
        valence_diff = abs(user_prefs['valence'] - song['valence'])
        valence_score = 12.0 * (1 - valence_diff)
        total_score += valence_score
        reasons.append(f"Valence (+{valence_score:.1f})")
    
    # 4. GENRE: +15 points (secondary)
    if user_prefs.get('genre', '').lower() == song['genre'].lower():
        total_score += 15.0
        reasons.append(f"Genre match (+15.0)")
    else:
        reasons.append(f"Genre mismatch (+0)")
    
    # 5. ENERGY: +8 points
    if 'energy' in user_prefs and isinstance(user_prefs['energy'], (int, float)):
        energy_diff = abs(user_prefs['energy'] - song['energy'])
        energy_score = 8.0 * (1 - energy_diff)
        total_score += energy_score
        reasons.append(f"Energy (+{energy_score:.1f})")
    
    # 6. DANCEABILITY: +7 points
    if 'danceability' in user_prefs and isinstance(user_prefs['danceability'], (int, float)):
        dance_diff = abs(user_prefs['danceability'] - song['danceability'])
        dance_score = 7.0 * (1 - dance_diff)
        total_score += dance_score
        reasons.append(f"Danceability (+{dance_score:.1f})")
    
    if 'acousticness' in user_prefs and isinstance(user_prefs['acousticness'], (int, float)):
        acoustic_diff = abs(user_prefs['acousticness'] - song['acousticness'])
        acoustic_score = 3.0 * (1 - acoustic_diff)
        total_score += acoustic_score
        reasons.append(f"Acousticness (+{acoustic_score:.1f})")
    
    return (total_score, reasons)


def score_song_energy_focused(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Energy-Focused mode: Prioritizes high-energy, danceable tracks. Great for 
    workout playlists or parties.
    """
    total_score = 0.0
    reasons = []
    
    # 1. ENERGY: +30 points (heavily weighted)
    if 'energy' in user_prefs and isinstance(user_prefs['energy'], (int, float)):
        energy_diff = abs(user_prefs['energy'] - song['energy'])
        energy_score = 30.0 * (1 - energy_diff)
        total_score += energy_score
        reasons.append(f"Energy match (+{energy_score:.1f})")
    
    # 2. DANCEABILITY: +25 points (heavily weighted)
    if 'danceability' in user_prefs and isinstance(user_prefs['danceability'], (int, float)):
        dance_diff = abs(user_prefs['danceability'] - song['danceability'])
        dance_score = 25.0 * (1 - dance_diff)
        total_score += dance_score
        reasons.append(f"Danceability (+{dance_score:.1f})")
    
    # 3. TEMPO: +8 points (higher is generally more energetic)
    user_target_tempo = user_prefs.get('tempo_bpm', 120)
    if isinstance(user_target_tempo, (int, float)):
        tempo_diff = abs(user_target_tempo - song['tempo_bpm'])
        tempo_score = 8.0 * (1 - min(tempo_diff / 100, 1.0))
        total_score += tempo_score
        reasons.append(f"Tempo match (+{tempo_score:.1f})")
    
    # 4. VALENCE: +10 points (uplifting songs)
    if 'valence' in user_prefs and isinstance(user_prefs['valence'], (int, float)):
        valence_diff = abs(user_prefs['valence'] - song['valence'])
        valence_score = 10.0 * (1 - valence_diff)
        total_score += valence_score
        reasons.append(f"Valence (+{valence_score:.1f})")
    
    # 5. GENRE: +8 points
    if user_prefs.get('genre', '').lower() == song['genre'].lower():
        total_score += 8.0
        reasons.append(f"Genre match (+8.0)")
    else:
        reasons.append(f"Genre mismatch (+0)")
    
    # 6. MOOD: +6 points
    if user_prefs.get('mood', '').lower() == song['mood'].lower():
        total_score += 6.0
        reasons.append(f"Mood match (+6.0)")
    else:
        reasons.append(f"Mood variant (+0)")
    
    # 7. ACOUSTICNESS: Low acoustic = higher energy bonus
    if 'acousticness' in song:
        acoustic_bonus = (1 - song['acousticness']) * 5.0
        total_score += acoustic_bonus
        reasons.append(f"Electronic feel (+{acoustic_bonus:.1f})")
    
    # 8. Popularity bonus
    if song.get('popularity', 50) > 75:
        pop_bonus = 2.0
        total_score += pop_bonus
        reasons.append(f"Popular track (+{pop_bonus:.1f})")
    
    return (total_score, reasons)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, 
                   mode: str = "balanced", apply_diversity: bool = True) -> List[Tuple[Dict, float, str]]:
    """
    Finds the top k songs that match user preferences.
    
    Args:
        user_prefs: User preference dictionary
        songs: List of song dictionaries
        k: Number of recommendations to return
        mode: Scoring mode - "balanced", "genre-first", "mood-first", "energy-focused"
        apply_diversity: If True, applies diversity penalty to reduce similar artist/genre clustering
    
    Returns:
        List of (song_dict, final_score, explanation) tuples, sorted by score (highest first).
    """
    # Step 1: Score every single song
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, mode=mode)
        explanation = " | ".join(reasons)
        scored_songs.append((song, score, explanation))
    
    # Step 2: Apply diversity penalty if enabled
    if apply_diversity:
        scored_songs = apply_diversity_penalty(scored_songs, k)
    
    # Step 3: Sort by score (highest first)
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    
    # Step 4: Return top k results
    return scored_songs[:k]


def apply_diversity_penalty(scored_songs: List[Tuple[Dict, float, str]], k: int) -> List[Tuple[Dict, float, str]]:
    """
    Applies a diversity penalty to prevent too many songs from the same artist or genre 
    in the top k recommendations.
    
    How it works:
    - We select songs one by one, starting with the highest-scored
    - If an artist or genre already appears in our selection, we reduce its score slightly
    - This encourages variety while still respecting the initial ranking
    """
    if not scored_songs or k <= 1:
        return scored_songs
    
    # Build selection progressively
    selected = []
    used_artists: Dict[str, int] = {}  # artist -> count
    used_genres: Dict[str, int] = {}   # genre -> count
    remaining = list(scored_songs)
    
    # Keep selecting until we have enough songs or run out
    while len(selected) < k and remaining:
        # Sort remaining by score (descending)
        remaining.sort(key=lambda x: x[1], reverse=True)
        
        best_song = remaining[0]
        song_dict, original_score, explanation = best_song
        
        artist = song_dict.get('artist', '')
        genre = song_dict.get('genre', '')
        
        # Calculate penalty based on duplicates already selected
        penalty = 0.0
        penalty_reasons = []
        
        # Artist penalty: -5 points per duplicate artist (max -15)
        artist_count = used_artists.get(artist, 0)
        if artist_count > 0:
            penalty_amount = min(artist_count * 5.0, 15.0)
            penalty += penalty_amount
            penalty_reasons.append(f"Artist diversity penalty (-{penalty_amount:.1f})")
        
        # Genre penalty: -3 points per duplicate genre (max -9)
        genre_count = used_genres.get(genre, 0)
        if genre_count > 0:
            penalty_amount = min(genre_count * 3.0, 9.0)
            penalty += penalty_amount
            penalty_reasons.append(f"Genre diversity penalty (-{penalty_amount:.1f})")
        
        # Apply penalty to score
        final_score = max(0, original_score - penalty)
        
        # Update explanation
        if penalty_reasons:
            explanation = explanation + " | " + " | ".join(penalty_reasons)
        
        # Add to selection
        selected.append((song_dict, final_score, explanation))
        
        # Update usage counts
        used_artists[artist] = used_artists.get(artist, 0) + 1
        used_genres[genre] = used_genres.get(genre, 0) + 1
        
        # Remove from remaining
        remaining.pop(0)
    
    return selected
