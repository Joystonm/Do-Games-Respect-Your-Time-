#!/usr/bin/env python3
"""
Quick test to verify TRS implementation works
"""
from data_engine import TimeRespectAnalyzer

print("Testing TRS implementation...")

# Load and process data
analyzer = TimeRespectAnalyzer('hltb_dataset.csv')
print("✓ Data loaded")

analyzer.clean_data()
print(f"✓ Data cleaned: {len(analyzer.df)} games")

analyzer.compute_metrics()
print("✓ Metrics computed")

analyzer.compute_time_respect_score()
print("✓ TRS computed")

# Test leaderboard
top, bottom = analyzer.get_trs_leaderboard(top_n=10, bottom_n=10)
print(f"✓ Leaderboard generated: {len(top)} top, {len(bottom)} bottom")

# Show sample results
print("\n🏆 Top 3 Most Respectful Games:")
for i, row in top.head(3).iterrows():
    print(f"  {row['name']}: TRS={row['time_respect_score']:.3f}, {row['time_cost']:.1f}h, {row['main_story_polled']} polls")

print("\n⚠️ Bottom 3 Time Wasters:")
for i, row in bottom.head(3).iterrows():
    print(f"  {row['name']}: TRS={row['time_respect_score']:.3f}, {row['time_cost']:.1f}h, {row['main_story_polled']} polls")

print("\n✅ All tests passed!")
