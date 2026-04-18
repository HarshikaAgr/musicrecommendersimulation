# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

This is a **content-based recommender system**—it matches songs to a user by comparing song characteristics to user preferences, rather than looking at what other users liked.

### Song Features (What We Know About Each Song)
Each song has these important characteristics:
- **genre**: Type of music (pop, rock, lofi, classical, etc.) — 15 genres total
- **mood**: Emotional vibe (happy, chill, peaceful, etc.) — 11 moods represented
- **energy**: 0.0 = calm to 1.0 = intense (numerical scale)
- **tempo_bpm**: Speed in beats per minute (continuous number)
- **valence**: 0.0 = sad/dark to 1.0 = happy/bright (numerical scale)
- **danceability**: 0.0 = not danceable to 1.0 = very danceable (numerical scale)
- **acousticness**: 0.0 = electronic to 1.0 = acoustic instruments (numerical scale)

### Dataset Size
**18 songs** total:
- Original 10 starter songs
- 8 new diverse songs added (reggae, country, house, hip-hop, metal, classical, r&b, folk)

### User Profile Information
A user profile stores their music preferences. Example: **Alex's Profile**
```python
user_profile = {
    "name": "Alex",
    "favorite_genre": "pop",           # Primary genre
    "favorite_mood": "happy",          # Emotional preference
    "preferred_energy": 0.80,          # How intense (0=calm, 1=intense)
    "preferred_valence": 0.75,         # How happy (0=sad, 1=happy)
    "preferred_danceability": 0.75,    # How danceable (0=no, 1=yes)
    "preferred_acousticness": 0.20     # Electronic=0, Acoustic=1
}
```

### The Scoring Algorithm Recipe 

For each song, the system calculates a **total score** by evaluating how well it matches the user's profile:

#### **Point Weights (What Matters Most)**

| Feature | Max Points | Match Logic |
|---------|-----------|-------------|
| **Genre** | +30 | Must match exactly. Pop genre song? +30. Rock? +0 |
| **Mood** | +20 | Must match exactly. Happy mood song? +20. Chill? +0 |
| **Energy** | +15 | Proximity scoring: closer to preference = more points |
| **Valence** | +10 | Proximity scoring: closer to preference = more points |
| **Danceability** | +10 | Proximity scoring: closer to preference = more points |
| **Acousticness** | +5 | Proximity scoring: closer to preference = more points |
| | **Maximum: 90 points** | Perfect match across all features |

#### **Proximity Scoring Formula (For Numerical Features)**
For energy, valence, danceability, and acousticness:
```
score = MAX_POINTS × (1 - |user_preference - song_value|)

Example:
- User prefers energy = 0.80
- Song has energy = 0.75
- Difference = |0.80 - 0.75| = 0.05
- Energy Score = 15 × (1 - 0.05) = 14.25 points
```

#### **Total Score Formula**
```
TOTAL_SCORE = genre_score(0 or 30) + mood_score(0 or 20) + 
              energy_score(0-15) + valence_score(0-10) + 
              danceability_score(0-10) + acousticness_score(0-5)
```

### How Recommendations Are Generated

**Data Flow:**
1. **INPUT** — Load user profile (e.g., Alex's preferences)
2. **LOAD** — Read all 18 songs from `data/songs.csv`
3. **SCORE LOOP** — For each song:
   - Calculate genre and mood match (0 or points)
   - Calculate proximity scores for energy, valence, danceability, acousticness
   - Sum all scores
4. **RANK** — Sort all songs by score (highest first)
5. **SELECT** — Return top K songs (e.g., top 5)
6. **OUTPUT** — Display recommendations with scores and explanations

### Expected Behavior & Potential Biases 

**What should work well:**
- Alex (who likes pop + happy) should get "Sunrise City," "Gym Hero," "Rooftop Lights"
- Should NOT match lofi songs or metal songs

**Potential biases I expect:**
1. **Genre over-prioritization** — The system might be too narrow, missing great "indie pop with rock energy" songs because the genre doesn't exactly match
2. **Exact mood matching** — Similarly, moods must match exactly, which might miss songs with slightly different but compatible moods
3. **No novelty** — System only finds songs similar to what the user already likes; won't discover new genres they might enjoy

### Why This Mirrors Real Recommendations
Spotify and YouTube use similar logic at massive scale—they find content whose features match your listening history. The difference is they use **collaborative filtering** (learning from millions of users) PLUS content-based filtering for much higher accuracy.

---

## System Architecture Diagram

Here's how data flows through the recommender:

```
INPUT: User Profile
   (Favorite Genre, Mood, Energy, etc.)
        ↓
LOAD: 18 Songs from CSV
        ↓
FOR EACH SONG:
   ├─ Calculate Genre Match (0 or 30 pts)
   ├─ Calculate Mood Match (0 or 20 pts)
   ├─ Calculate Energy Proximity (0-15 pts)
   ├─ Calculate Valence Proximity (0-10 pts)
   ├─ Calculate Danceability Proximity (0-10 pts)
   └─ Calculate Acousticness Proximity (0-5 pts)
        ↓
STORE: Song + Total Score (0-90)
        ↓
RANK: Sort Songs by Score
   (Highest Score First)
        ↓
SELECT: Top K Songs (e.g., Top 5)
        ↓
OUTPUT: Recommendations
   Song Name | Score | Why You'll Like It
```

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

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

