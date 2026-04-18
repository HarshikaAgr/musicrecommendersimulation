# Music Recommender Simulation - Model Card

## 1. What is This? (Model Name)

**VibeMatcher 1.0** - A simple music recommender system that tries to match songs to what you like.

Not a real app you'd use on Spotify, but a learning project to understand how recommendation algorithms actually work.

---

## 2. What's It For? (Intended Use)

This system is built for **learning and understanding**, not real users. It shows how a basic recommendation algorithm scores songs based on your preferences.

**What it actually does:**
- You tell it your music taste (favorite genre, mood, energy level)
- It scores all the songs in its collection
- It gives you the top 5 best matches with explanations of why

**Who would use this:**
- Students wanting to learn about recommender systems
- Developers curious about how Spotify-like systems work
- Anyone who wants to see algorithm bias in action

---

## 3. How Does It Actually Work?

Imagine you're looking through 18 songs and want to find your new favorite. The algorithm is like a friend checking each one:

"Does this match your genre? Genre gets points."
"Is the mood right? Mood gets points."
"Is the energy level close? Energy gets points."

Then it adds up all the points and ranks all the songs.

**The Scoring Breakdown** (out of 90 points max):

| Feature | Points | How It Works |
|---------|--------|------------|
| Genre match (pop vs pop) | +30 | Gotta match exactly or get nothing |
| Mood match (happy vs happy) | +20 | Same deal - exact match only |
| Energy closeness | +15 | If you like 0.8 and song is 0.75, you get close to 15 |
| Valence (happy/sad feeling) | +10 | Proximity based - closer = more points |
| Danceability | +10 | How danceable - proximity based |
| Acousticness | +5 | Real instruments vs electronic - proximity based |

**Real Example:**
- You like: pop + happy + high energy (0.8)
- "Sunrise City" is pop, happy, 0.82 energy → Gets almost all points (88.3/90) ✓
- "Gym Hero" is pop, intense (wrong mood), 0.93 energy → Gets 65.8/90 (loses mood points)
- "Piano Dreams" is classical, peaceful, 0.32 energy → Gets almost nothing

---

## 4. What Data Does It Use?

**The Song Collection:**
- 18 total songs
- Started with 10, I added 8 more to get variety
- Genres: pop, rock, lofi, jazz, ambient, synthwave, indie pop, reggae, country, house, hip-hop, metal, classical, r&b, folk
- Moods: happy, chill, intense, focused, relaxed, moody, uplifting, energetic, aggressive, peaceful, smooth
- Each song has 7 features (genre, mood, energy, tempo, valence, danceability, acousticness)

**Real talk about the data:**
- It's super small (18 songs vs millions on Spotify)
- All the songs are kind of generic examples
- Missing a lot of mood types (no sad, romantic, angry specifically)
- This is just for learning, not realistic

---

## 5. What Does It Do Well?

**The wins:**

1. **It actually separates different music tastes** - If I run it for a pop fan vs lofi fan vs rock fan, they get COMPLETELY different recommendations. That's good.

2. **It explains itself** - Every recommendation shows you the math: "Genre match +30, Mood match +20, Energy +14.7" etc. You're not a black box.

3. **The top matches usually feel right** - "Sunrise City" for the pop fan, "Focus Flow" for the lofi coder, "Storm Runner" for the rock fan. These make sense intuitively.

4. **It's actually fast** - Scores all 18 songs instantly. No waiting around.

---

## 6. What's Broken? (The Big Problems)

**The Real Issues:**

1. **Genre weight is TOO HIGH**
   - Genre = 30 out of 90 points (that's 33%!)
   - This means you basically can't get recommendations outside your exact genre
   - Example: "Rooftop Lights" is indie pop with PERFECT mood match but gets pushed down by "Gym Hero" which is just "pop" with the wrong mood
   - If you say "I like pop," you'll NEVER see a great indie pop song, even if it matches everything else perfectly
   - This is the biggest bias in the system

2. **Mood has to match exactly**
   - "happy" ≠ "uplifting"
   - "chill" ≠ "relaxed"
   - So a song that's basically the same vibe but labeled differently gets 0 mood points
   - This is dumb and too rigid

3. **The dataset is tiny**
   - Only 18 songs - real Spotify has millions
   - Only 11 mood types - people have way more emotional responses than that
   - Missing a ton of cultural music diversity

4. **No learning or adaptation**
   - Your preferences are frozen forever
   - If you're tired of pop today, too bad - the algorithm still thinks you want pop
   - Real apps learn what you actually skip/like

5. **Can't discover anything new**
   - If you want exactly what you already like, great
   - If you want to explore or find something slightly different, the algorithm will never help

---

## 7. How Did I Test This?

**Test 1: Three Different People**
- ALEX (loves pop, happy, high energy) → Got pop songs ✓
- BLAKE (loves lofi, focused, low energy) → Got lofi songs ✓  
- JORDAN (loves rock, intense, high energy) → Got rock songs ✓
- Result: It actually works - each person got totally different recommendations

**Test 2: What if I change the math?**
- I modified the algorithm weights
- Original: Genre=30, Energy=15
- Modified: Genre=15, Energy=30 (energy now matters more)
- For Alex: Top songs changed from [pop, pop, indie pop] to [pop, indie pop, pop]
- Indie pop jumped to #2 just because I reduced genre importance
- This shows genre weight IS a huge deal - changing it changes everything

**Test 3: Do the explanations make sense?**
- I looked at why each song got its score
- The math all checked out
- But the genre bias showed up clearly - genre was always the decider

---

## 8. What Would I Fix?

If I had more time, here's what I'd do:

1. **Lower genre weight to 20** instead of 30 - let songs from similar genres compete fairly
2. **Make genre matching smarter** - indie pop should be more similar to pop than metal is. Right now it's all-or-nothing.
3. **Add "exploration mode"** - Give users some recommendations that match their taste (70%) and some wild cards (30% random genre)
4. **Stop exact mood matching** - Use a spectrum instead (sad←→happy) so similar moods count
5. **Add diversity to results** - Don't let one artist dominate the top 5

---

## 9. What I Actually Learned

Building this was weirdly eye-opening. Here's what stuck with me:

**The Biggest Realization:**
Every algorithm has hidden assumptions baked in. By setting genre=30 points, I was making a choice that said "genre is the most important thing about music taste." But that's not always true for everyone. Some people care more about energy or mood than genre.

When I tested changing the weights, I realized: **A tiny math change (halving one number) completely changed what got recommended.** That showed me that these "simple" algorithms actually have a lot of hidden power to shape what people see.

**What Surprised Me:**
I thought the genre strictness would be a small issue. Turns out it was THE BIGGEST problem. When I reduced genre weight in the experiment, recommendation results actually got more interesting. This makes me think real Spotify was probably super deliberate about their genre choices - they probably tested a million different weights.

**When AI Tools Helped vs Hurt:**
- AI was great for: Writing the scoring math initially, explaining bias concepts
- I had to fix: Sometimes the explanations were too polished/non-human. I had to re-read recommendations to make sure they actually made sense

**What I'd Do Next:**
If I extended this, I'd be curious about:
- What if users could say "I'm in a pop mood TODAY but try something new"
- What if the system learned from what I actually skip vs listen to
- What if it had 1000 songs - would the bias show up differently

---

## 10. Technical Note (If You Care)

**How to Run It:**
```
cd musicrecommendersimulation
python -m src.main
```

**The Code Structure:**
- `recommender.py` - Does all the scoring/ranking
- `main.py` - Tests with 3 different profiles
- `experiment.py` - Tests weight sensitivity
- `data/songs.csv` - The 18 songs

**The Algorithm in Words:**
1. Load songs from CSV
2. For each song: calculate 6 scores (genre, mood, energy, valence, danceability, acousticness)
3. Add them up
4. Sort songs by total score
5. Return top 5

---

**Made by:** @harsh  
**Date:** April 2026  
**For:** CodePath AI110 Learning Project
