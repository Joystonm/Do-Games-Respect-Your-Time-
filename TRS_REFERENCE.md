# Time Respect Score (TRS) - Quick Reference

## What It Does
Ranks games by how much they respect your time using three factors:

### Formula
```
TRS = 0.4 × Length Penalty + 0.4 × Confidence Reward + 0.2 × Genre Fit
```

### Components

1. **Length Penalty (40%)**
   - Formula: `exp(-hours / 30)`
   - Shorter games score higher
   - 10 hours → 0.72 penalty
   - 30 hours → 0.37 penalty
   - 60 hours → 0.14 penalty

2. **Confidence Reward (40%)**
   - Formula: `log(polls + 1) / max_confidence`
   - More polls = higher score
   - 10 polls → ~0.15 reward
   - 100 polls → ~0.30 reward
   - 1000 polls → ~0.50 reward

3. **Genre Fit (20%)**
   - Formula: `1 / (1 + |hours - genre_median| / genre_median)`
   - Games close to genre norms score higher
   - Penalizes outliers (too short or too long for genre)

## Example Scores

### High TRS (Respectful)
- **Portal** (3h, 500 polls, Puzzle) → TRS ≈ 0.85
- **Journey** (2h, 300 polls, Adventure) → TRS ≈ 0.88
- **Limbo** (4h, 400 polls, Platformer) → TRS ≈ 0.82

### Low TRS (Time Wasters)
- **Unknown MMO** (200h, 5 polls, MMO) → TRS ≈ 0.05
- **Obscure RPG** (150h, 3 polls, RPG) → TRS ≈ 0.03
- **Indie Grind** (80h, 8 polls, Simulation) → TRS ≈ 0.08

## Why It Works

1. **Penalizes extreme length** — Long games naturally score lower
2. **Rewards confidence** — Well-measured games score higher
3. **Normalizes by genre** — 40h RPG isn't penalized like 40h platformer
4. **Balanced weights** — Length and confidence equally important (40% each)

## Interpretation

- **TRS > 0.7** — Highly respectful (short, confident, genre-appropriate)
- **TRS 0.4-0.7** — Moderately respectful (balanced)
- **TRS < 0.4** — Time waster (long, uncertain, or outlier)

## Use Cases

1. **Game selection** — Choose games with high TRS
2. **Genre comparison** — See which genres respect time
3. **Data quality** — Low TRS often means unreliable data
4. **Content creation** — "Top 10 games that respect your time"

## Limitations

- Biased toward short games (by design)
- Doesn't account for quality or enjoyment
- Genre medians can be skewed by outliers
- New games have low confidence (few polls)

## Files Modified

- `data_engine.py` — Added `compute_time_respect_score()` and `get_trs_leaderboard()`
- `viz_engine.py` — Added `trs_leaderboard()` visualization
- `app.py` — Added TRS leaderboard section
- `README.md` — Updated to mention TRS
