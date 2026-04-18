"""
Command line runner for the Music Recommender Simulation with Advanced Features.

This script tests:
- Multiple scoring modes (balanced, genre-first, mood-first, energy-focused)
- Diversity penalty to prevent artist/genre clustering
- New song features (popularity, release decade, mood tags)
- Pretty table output for easy reading
"""

from .recommender import load_songs, recommend_songs


def print_table_header(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)


def print_song_table(recommendations, max_width: int = 100):
    """Print recommendations as a formatted ASCII table"""
    
    # Column widths
    col_rank = 4
    col_title = 30
    col_artist = 18
    col_score = 8
    col_match = 8
    
    # Header
    header = f"{'#':<{col_rank}} | {'Title':<{col_title}} | {'Artist':<{col_artist}} | {'Score':<{col_score}} | {'Match':<{col_match}}"
    print("\n" + header)
    print("-" * 50)
    
    # Rows
    for rank, (song, score, explanation) in enumerate(recommendations, 1):
        match_pct = f"{(score/100)*100:.0f}%"  # Approximate max based on mode
        
        title = song['title'][:col_title].ljust(col_title)
        artist = song['artist'][:col_artist].ljust(col_artist)
        score_str = f"{score:.1f}".rjust(col_score)
        match_str = match_pct.rjust(col_match)
        
        row = f"{rank:<{col_rank}} | {title} | {artist} | {score_str} | {match_str}"
        print(row)
        
        # Print explanation below
        reasons = explanation.split(" | ")
        reasons_text = " + ".join([r.strip() for r in reasons[:3]])  # Show first 3 reasons
        if len(reasons) > 3:
            reasons_text += f" + {len(reasons) - 3} more"
        print(f"     Why: {reasons_text}\n")


def print_recommendations_by_mode(songs, user_prefs, profile_name, modes: list = None):
    """Show recommendations using different scoring modes"""
    
    if modes is None:
        modes = ["balanced", "genre-first", "mood-first", "energy-focused"]
    
    print_table_header(f"Profile: {profile_name}")
    print(f"\nPreferences: Genre={user_prefs.get('genre')}, Mood={user_prefs.get('mood')}, "
          f"Energy={user_prefs.get('energy')}, Danceability={user_prefs.get('danceability')}")
    
    # Test each mode
    for mode in modes:
        print(f"\n--- Scoring Mode: {mode.upper()} ---")
        recommendations = recommend_songs(user_prefs, songs, k=5, mode=mode, apply_diversity=True)
        print_song_table(recommendations)


def print_diversity_comparison(songs, user_prefs, profile_name):
    """Show how diversity penalty affects recommendations"""
    
    print_table_header(f"Diversity Logic Demo: {profile_name}")
    
    # Without diversity
    print("\nWithout Diversity Penalty (same artist/genre can repeat):")
    recs_no_diversity = recommend_songs(user_prefs, songs, k=5, mode="balanced", apply_diversity=False)
    print_song_table(recs_no_diversity)
    
    # Check artist/genre clustering
    artists = [song['artist'] for song, _, _ in recs_no_diversity]
    genres = [song['genre'] for song, _, _ in recs_no_diversity]
    print(f"Artists in top 5: {', '.join(artists)}")
    print(f"Genres in top 5: {', '.join(genres)}")
    
    # With diversity
    print("\n\nWith Diversity Penalty (diverse artist/genre picks):")
    recs_with_diversity = recommend_songs(user_prefs, songs, k=5, mode="balanced", apply_diversity=True)
    print_song_table(recs_with_diversity)
    
    # Check artist/genre clustering
    artists = [song['artist'] for song, _, _ in recs_with_diversity]
    genres = [song['genre'] for song, _, _ in recs_with_diversity]
    print(f"Artists in top 5: {', '.join(artists)}")
    print(f"Genres in top 5: {', '.join(genres)}")
    print("\nNotice: Diversity mode spreads recommendations across different artists and genres!")


def main() -> None:
    # Load all songs from CSV (now with 5 new features)
    songs = load_songs("data/songs.csv")
    print(f"\nLoaded {len(songs)} songs from data/songs.csv")
    print("New features added: popularity, release_decade, artist_id, mood_tags, year")
    
    # Define user profiles with different needs
    profiles = [
        {
            "name": "Alex - High Energy Pop",
            "prefs": {
                "genre": "pop",
                "mood": "happy",
                "energy": 0.80,
                "valence": 0.75,
                "danceability": 0.75,
                "acousticness": 0.20,
                "tempo_bpm": 120
            }
        },
        {
            "name": "Blake - Chill Coding",
            "prefs": {
                "genre": "lofi",
                "mood": "focused",
                "energy": 0.35,
                "valence": 0.55,
                "danceability": 0.50,
                "acousticness": 0.75,
                "tempo_bpm": 80,
                "mood_tags": ["peaceful", "concentration", "zen"]
            }
        },
        {
            "name": "Jordan - Intense Rock",
            "prefs": {
                "genre": "rock",
                "mood": "intense",
                "energy": 0.90,
                "valence": 0.35,
                "danceability": 0.65,
                "acousticness": 0.10,
                "tempo_bpm": 140
            }
        }
    ]
    
    print_table_header("CHALLENGE 1: Advanced Song Features & Multiple Scoring Modes")
    print("\nDemonstrating all 4 scoring modes: balanced, genre-first, mood-first, energy-focused")
    
    # Show each profile with all modes
    for profile in profiles:
        print_recommendations_by_mode(
            songs, 
            profile["prefs"], 
            profile["name"],
            modes=["balanced", "genre-first", "mood-first", "energy-focused"]
        )
    
    print_table_header("CHALLENGE 3: Diversity & Fairness Logic")
    print("\nComparing recommendations with and without artist/genre diversity penalties")
    
    # Show diversity impact for one profile
    print_diversity_comparison(songs, profiles[0]["prefs"], profiles[0]["name"])
    
    # Summary
    print("\n\n" + "=" * 50)
    print("  PHASE COMPLETE! Summary of new features:")
    print("=" * 50)
    print("""
  Challenge 1 (Advanced Features):
  - Added 5 new song attributes: popularity, release_decade, artist_id, mood_tags, year
  - Extended songs.csv with real data for each song
  - Updated scoring logic to use new features
  
  Challenge 2 (Multiple Scoring Modes):
  - Balanced Mode: Evenly weights all features
  - Genre-First Mode: Prioritizes genre match (45 pts) over others
  - Mood-First Mode: Focuses on mood + mood tags for vibe matching
  - Energy-Focused Mode: Prioritizes energy and danceability for workouts/parties
  
  Challenge 3 (Diversity Logic):
  - Implemented diversity penalty: same artist -5, same genre -3
  - Prevents top 5 from being all from one artist or all one genre
  - Results in more varied recommendations
  
  Challenge 4 (Table Output):
  - Created readable ASCII tables showing rank, song, artist, score
  - Included reason explanations for each recommendation
  - Better readability than line-by-line output
    """)
    print("=" * 50)


if __name__ == "__main__":
    main()
