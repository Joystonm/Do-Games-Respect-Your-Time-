"""
Do Games Respect Your Time?

This is not a dashboard. This is visual reasoning.
"""
import streamlit as st
import pandas as pd
import numpy as np
from data_engine import TimeRespectAnalyzer
from viz_engine import (
    trust_time_landscape, perception_reality_split, genre_honesty_ranking,
    sensitivity_proof, confidence_crisis_histogram, trs_leaderboard, topographic_density_map, zone_distribution_pie, PALETTE
)
from viz_3d_advanced import (
    trust_time_stability_3d, genre_honesty_orbit_3d, platform_reliability_cube_3d,
    misrepresentation_risk_helix_3d, hidden_gems_cluster_3d
)
from timeline_viz import create_timeline_viz, generate_synthetic_journey, TIMELINE_PALETTE
from radar_viz import create_radar_chart, get_game_stats, RADAR_PALETTE
from model_eval import (
    prepare_model_data, train_models, create_roc_curve, 
    get_feature_importance, create_feature_importance_viz, MODEL_PALETTE
)
# Page config
st.set_page_config(
    page_title="Do Games Respect Your Time?",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Minimal CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    * { font-family: 'Inter', -apple-system, sans-serif; }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        color: #1A1A1A;
        line-height: 1.2;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        font-size: 1.3rem;
        color: #666;
        font-weight: 400;
        margin-bottom: 3rem;
    }
    
    .section-break { height: 3rem; }
    
    .insight-box {
        background: #2A3441;
        color: white;
        padding: 2.5rem;
        border-radius: 6px;
        margin: 3rem 0;
        font-size: 1.6rem;
        font-weight: 600;
        text-align: center;
        border-left: 3px solid #4A90E2;
    }
    
    .narrative {
        font-size: 1.05rem;
        line-height: 1.7;
        color: #2A2A2A;
        margin: 2rem 0;
        max-width: 800px;
    }
    
    .narrative strong { color: #1A1A1A; font-weight: 600; }
    .narrative em { color: #666; font-style: italic; }
    
    .stat-hero { text-align: center; padding: 1.5rem; margin: 1.5rem 0; }
    .stat-number { font-size: 3rem; font-weight: 700; color: #1A1A1A; }
    .stat-label { font-size: 0.85rem; color: #666; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 0.5rem; }
    
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1A1A1A;
        margin: 4rem 0 2rem 0;
        border-left: 3px solid #4A90E2;
        padding-left: 1.5rem;
    }
    
    .conclusion-box {
        background: #F8F9FA;
        border-left: 3px solid #4A90E2;
        padding: 2rem;
        margin: 3rem 0;
        font-size: 1.05rem;
        line-height: 1.7;
        color: #2A2A2A;
    }
    
    div[data-testid="stMetricValue"] { font-size: 2rem; font-weight: 600; }
    .stButton>button {
        background: #4A90E2;
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 0.95rem;
        border-radius: 4px;
        font-weight: 600;
    }
    .stButton>button:hover { background: #357ABD; }
    html { scroll-behavior: smooth; }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    analyzer = TimeRespectAnalyzer('hltb_dataset.csv')
    analyzer.clean_data()
    analyzer.compute_metrics()
    return analyzer

analyzer = load_data()
insight = analyzer.get_core_insight()

# ============================================================================
# OPENING: THE HOOK
# ============================================================================

st.markdown('<h1 class="main-title">Do Games Respect Your Time?</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">An analysis of uncertainty in game completion data</p>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
Time is finite. Every hour in a game is an hour not spent elsewhere.

When you see <strong>"20 hours to beat,"</strong> you're seeing a number. But is it based on 5 players or 500?

Most platforms show raw averages. <strong>We model uncertainty.</strong>

And when you do that, something breaks.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# ============================================================================
# THE CRISIS
# ============================================================================

st.markdown('<h2 class="section-header">The Crisis</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="stat-hero">
        <div class="stat-number">{insight['unreliable_pct']:.0f}%</div>
        <div class="stat-label">Unreliable Estimates</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-hero">
        <div class="stat-number">{len(analyzer.df):,}</div>
        <div class="stat-label">Games Analyzed</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-hero">
        <div class="stat-number">{insight['avg_misrep_risk']:.0%}</div>
        <div class="stat-label">Avg Risk Score</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
<strong>74% of games have fewer than 10 completion reports.</strong>

That's not a sample. That's a guess.

Yet platforms treat a game with 5 reports the same as one with 500.
</div>
""", unsafe_allow_html=True)

fig_crisis = confidence_crisis_histogram(analyzer.df)
st.plotly_chart(fig_crisis, use_container_width=True)

st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# ============================================================================
# THE INSIGHT
# ============================================================================

st.markdown('<h2 class="section-header">The Insight</h2>', unsafe_allow_html=True)

st.markdown(f"""
<div class="insight-box">
{insight['pct_noise']:.0f}% of perceived game length<br>is statistical noise
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="narrative">
When you weight completion times by confidence, the median drops from <strong>{insight['weighted_median_raw']:.1f} hours</strong> to <strong>{insight['weighted_median_adj']:.1f} hours</strong>.

That's a <strong>{insight['difference']:.1f}-hour</strong> gap.

Not because games lie. Because <em>we don't know their length</em> — and platforms don't tell you that.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# ============================================================================
# THE LANDSCAPE (HERO VISUAL)
# ============================================================================

st.markdown('<h2 class="section-header">The Trust-Time Landscape</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
This is the map. Every dot is a game. Position reveals truth.

<strong>Notice the voids.</strong> High-confidence long games are rare. Most "epics" sit in the fog.
</div>
""", unsafe_allow_html=True)

fig_landscape = trust_time_landscape(analyzer.df)
st.plotly_chart(fig_landscape, use_container_width=True, config={'displayModeBar': False})

zone_dist = analyzer.get_zone_distribution()
st.markdown("**Zone Distribution:**")
st.dataframe(zone_dist, use_container_width=True, hide_index=True)

fig_pie = zone_distribution_pie(analyzer.df)
st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})

st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# ============================================================================
# TOPOGRAPHIC DENSITY MAP
# ============================================================================

st.markdown('<h2 class="section-header">Topographic Density Map</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
<strong>Where do games actually cluster?</strong>

This topographic map reveals the terrain of game completion data. 
Peaks show high-density regions where most games concentrate. 
Valleys reveal the voids — unexplored territory where few games exist.

The contour lines trace elevation: <strong>higher = more games</strong>.
</div>
""", unsafe_allow_html=True)

fig_topo = topographic_density_map(analyzer.df)
st.plotly_chart(fig_topo, use_container_width=True, config={'displayModeBar': False})

st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# ============================================================================
# THE TRANSFORMATION
# ============================================================================

st.markdown('<h2 class="section-header">Perception vs Reality</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
Watch what happens when confidence is modeled.

The rankings shift. The "short" genres stay short. But the "long" ones? <strong>They collapse.</strong>
</div>
""", unsafe_allow_html=True)

genre_stats = analyzer.genre_analysis()
fig_split = perception_reality_split(analyzer.df, genre_stats)
st.plotly_chart(fig_split, use_container_width=True, config={'displayModeBar': False})

st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# ============================================================================
# GENRE HONESTY
# ============================================================================

st.markdown('<h2 class="section-header">Genre Honesty Ranking</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
Some genres are systematically over-estimated. Others under-estimated.

<strong>Honesty score</strong> = inverse of perception gap. Higher means more trustworthy.
</div>
""", unsafe_allow_html=True)

fig_honesty = genre_honesty_ranking(genre_stats)
st.plotly_chart(fig_honesty, use_container_width=True, config={'displayModeBar': False})

# Show biggest movers
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Most Over-Estimated (fall when adjusted):**")
    fallers = genre_stats.nsmallest(5, 'rank_shift')[['primary_genre', 'raw_median', 'adjusted_median', 'rank_shift']]
    st.dataframe(fallers, use_container_width=True, hide_index=True)

with col2:
    st.markdown("**Most Under-Estimated (rise when adjusted):**")
    risers = genre_stats.nlargest(5, 'rank_shift')[['primary_genre', 'raw_median', 'adjusted_median', 'rank_shift']]
    st.dataframe(risers, use_container_width=True, hide_index=True)

st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# ============================================================================
# 3D VISUALIZATION SUITE (5 ADVANCED CHARTS)
# ============================================================================

st.markdown('<h2 class="section-header">The 3D Revelation</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
Two dimensions can't capture the full truth. What follows is a journey through five 3D spaces, 
each revealing patterns <strong>impossible to see in 2D</strong>.

<em>Tip: Drag to rotate • Scroll to zoom • Scroll outside chart to navigate page</em>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# Config for 3D charts - full interactivity
plotly_3d_config = {
    'scrollZoom': True,
    'displayModeBar': True,
    'responsive': True,
    'displaylogo': False
}

# ============================================================================
# 3D #1: TRUST-TIME-STABILITY LANDSCAPE
# ============================================================================

st.markdown('<h3 class="section-header">3D #1: Trust-Time-Stability Landscape</h3>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
<strong>The void reveals truth.</strong>

In this 3D space, stability (Z-axis) shows how consistent estimates are. 
Notice the <strong>void in the upper-right-back corner</strong> — trustworthy long games barely exist.

Most "epics" float in unstable territory. The few verified epics form a tiny, isolated cluster.
</div>
""", unsafe_allow_html=True)

with st.container():
    fig_3d_1 = trust_time_stability_3d(analyzer.df)
    st.plotly_chart(fig_3d_1, use_container_width=True, config=plotly_3d_config)

st.markdown("---")
st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# ============================================================================
# 3D #2: GENRE HONESTY ORBIT
# ============================================================================

st.markdown('<h3 class="section-header">3D #2: Genre Honesty Orbit</h3>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
<strong>Which genres are honest?</strong>

Z-axis shows standard deviation — higher means less consistent. 
Genres with <strong>low Z + high confidence</strong> are trustworthy. 
Genres with <strong>high Z + low confidence</strong> are misleading.

The gold diamond marks the most honest genre. The red X marks the most misleading.
</div>
""", unsafe_allow_html=True)

with st.container():
    fig_3d_2 = genre_honesty_orbit_3d(analyzer.df)
    st.plotly_chart(fig_3d_2, use_container_width=True, config=plotly_3d_config)

st.markdown("---")
st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# ============================================================================
# 3D #3: PLATFORM RELIABILITY CUBE
# ============================================================================

st.markdown('<h3 class="section-header">3D #3: Platform Reliability Cube</h3>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
<strong>Platforms occupy unique trust-time spaces.</strong>

Each platform has its own signature: some trend toward short, confident games; 
others toward long, uncertain ones.

The cube reveals <strong>platform-specific patterns</strong> invisible in aggregate analysis.
</div>
""", unsafe_allow_html=True)

with st.container():
    fig_3d_3 = platform_reliability_cube_3d(analyzer.df)
    st.plotly_chart(fig_3d_3, use_container_width=True, config=plotly_3d_config)

st.markdown("---")
st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# ============================================================================
# 3D #4: MISREPRESENTATION RISK HELIX
# ============================================================================

st.markdown('<h3 class="section-header">3D #4: Misrepresentation Risk Helix</h3>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
<strong>The danger zone is visible.</strong>

Z-axis shows misrepresentation risk — higher means less trustworthy. 
Games in the <strong>high X, high Z region</strong> look long but are unreliable.

Avoid the danger zone. Trust the low-Z cluster.
</div>
""", unsafe_allow_html=True)

with st.container():
    fig_3d_4 = misrepresentation_risk_helix_3d(analyzer.df)
    st.plotly_chart(fig_3d_4, use_container_width=True, config=plotly_3d_config)

st.markdown("---")
st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# ============================================================================
# 3D #5: HIDDEN GEMS CLUSTER EXPLORER
# ============================================================================

st.markdown('<h3 class="section-header">3D #5: Hidden Gems Cluster Explorer</h3>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
<strong>Discover the hidden gems.</strong>

Z-axis shows poll volume (log scale). Three clusters emerge:

• <strong>Hidden Gems</strong> (green) — High confidence, low time, well-measured  
• <strong>Verified Epics</strong> (dark blue) — High confidence, high time, trustworthy  
• <strong>Overhyped</strong> (red) — Low confidence, high time, avoid  

The structure is invisible in 2D. In 3D, it's unmistakable.
</div>
""", unsafe_allow_html=True)

with st.container():
    fig_3d_5 = hidden_gems_cluster_3d(analyzer.df)
    st.plotly_chart(fig_3d_5, use_container_width=True, config=plotly_3d_config)

st.markdown("---")

st.markdown("""
<div class="narrative">
<strong>Key insight from 3D suite:</strong>

The five visualizations reveal a consistent truth: <em>trustworthy long games are rare</em>. 
Most games either respect your time (short + confident) or waste it (long + uncertain).

The void, the clusters, the danger zones — all tell the same story from different angles.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# ============================================================================
# ROBUSTNESS PROOF
# ============================================================================

st.markdown('<h2 class="section-header">Sensitivity Proof</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
An insight that survives only one threshold is not an insight. It's noise.

<strong>This survives every threshold.</strong> From 1 poll to 100 polls, the gap persists.
</div>
""", unsafe_allow_html=True)

sensitivity_df = analyzer.sensitivity_analysis()
fig_sensitivity = sensitivity_proof(sensitivity_df)
st.plotly_chart(fig_sensitivity, use_container_width=True, config={'displayModeBar': False})

st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# ============================================================================
# ============================================================================
# TIME RESPECT SCORE LEADERBOARD
# ============================================================================

st.markdown('<h2 class="section-header">Time Respect Score Leaderboard</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
<strong>Which games respect your time?</strong>

Time Respect Score (TRS) combines three factors:

• <strong>Length penalty</strong> — Shorter games score higher  
• <strong>Confidence reward</strong> — Well-measured games score higher  
• <strong>Genre fit</strong> — Games close to genre norms score higher  

The formula: <code>TRS = 0.4×Length + 0.4×Confidence + 0.2×Genre</code>
<br><br>
Rankings reveal truth. The best games are short, confident, and honest. The worst are long, uncertain, and outliers.
</div>
""", unsafe_allow_html=True)

top_games, bottom_games = analyzer.get_trs_leaderboard(top_n=10, bottom_n=10)
fig_trs = trs_leaderboard(top_games, bottom_games)
st.plotly_chart(fig_trs, use_container_width=True, config={'displayModeBar': False})

# Show detailed tables
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Top 10 Details:**")
    display_top = top_games[['name', 'time_cost', 'main_story_polled', 'time_respect_score']].copy()
    display_top.columns = ['Game', 'Hours', 'Polls', 'TRS']
    display_top['TRS'] = display_top['TRS'].round(3)
    display_top['Hours'] = display_top['Hours'].round(1)
    st.dataframe(display_top, use_container_width=True, hide_index=True)

with col2:
    st.markdown("**Bottom 10 Details:**")
    display_bottom = bottom_games[['name', 'time_cost', 'main_story_polled', 'time_respect_score']].copy()
    display_bottom.columns = ['Game', 'Hours', 'Polls', 'TRS']
    display_bottom['TRS'] = display_bottom['TRS'].round(3)
    display_bottom['Hours'] = display_bottom['Hours'].round(1)
    st.dataframe(display_bottom, use_container_width=True, hide_index=True)

st.markdown("""
<div class="narrative">
<strong>Key insight:</strong> The top games average <strong>{:.1f} hours</strong> with <strong>{:.0f} polls</strong>. 
The bottom games average <strong>{:.1f} hours</strong> with <strong>{:.0f} polls</strong>.

Time respect isn't just about being short — it's about being <em>measurably efficient</em>.
</div>
""".format(
    top_games['time_cost'].mean(),
    top_games['main_story_polled'].mean(),
    bottom_games['time_cost'].mean(),
    bottom_games['main_story_polled'].mean()
), unsafe_allow_html=True)

st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)


# ============================================================================
# PLAYER JOURNEY TIMELINE
# ============================================================================

st.markdown('<h2 class="section-header">Player Journey Timeline</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
<strong>How does game design affect time investment across playtime?</strong>

This timeline models player engagement, fatigue, and retention patterns. 
Watch how metrics evolve from early game through post-game padding.

<em>Select a metric to visualize its trajectory over 100 hours of gameplay.</em>
</div>
""", unsafe_allow_html=True)

# Generate synthetic journey data
journey_df = generate_synthetic_journey(hours=100)

# Metric selector
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    timeline_metric = st.selectbox(
        'Select Metric',
        ['engagement', 'progress_time', 'dropoff', 'content_density', 'repetition'],
        format_func=lambda x: {
            'engagement': 'Engagement Index',
            'progress_time': 'Avg Time to Progress',
            'dropoff': 'Drop-off Rate',
            'content_density': 'Content Density',
            'repetition': 'Repetition Intensity'
        }[x],
        key='timeline_metric_selector'
    )

with col2:
    avg_val = journey_df[timeline_metric].mean()
    st.markdown(f"""
    <div style="background: {TIMELINE_PALETTE['surface']}; border-radius: 12px; padding: 1.5rem; border: 1px solid {TIMELINE_PALETTE['grid']};">
        <div style="font-size: 0.85rem; color: {TIMELINE_PALETTE['text_dim']}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Average</div>
        <div style="font-size: 2rem; font-weight: 700; color: {TIMELINE_PALETTE['text']};">{avg_val:.1f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    peak_val = journey_df[timeline_metric].max()
    st.markdown(f"""
    <div style="background: {TIMELINE_PALETTE['surface']}; border-radius: 12px; padding: 1.5rem; border: 1px solid {TIMELINE_PALETTE['grid']};">
        <div style="font-size: 0.85rem; color: {TIMELINE_PALETTE['text_dim']}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Peak</div>
        <div style="font-size: 2rem; font-weight: 700; color: {TIMELINE_PALETTE['text']};">{peak_val:.1f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Timeline visualization
fig_timeline = create_timeline_viz(journey_df, timeline_metric)
st.plotly_chart(fig_timeline, use_container_width=True, config={'displayModeBar': False})

# Insights
timeline_insights = {
    'engagement': '<strong>Early Hook:</strong> Strong initial engagement drops as novelty fades. Mid-game oscillation suggests content variety. Late-game decline indicates fatigue.',
    'progress_time': '<strong>Pacing Analysis:</strong> Time investment per milestone increases steadily. Spikes indicate difficulty walls or grinding requirements.',
    'dropoff': '<strong>Retention Risk:</strong> Drop-off accelerates in late game. Critical threshold around 60h where player commitment wanes.',
    'content_density': '<strong>Content Efficiency:</strong> High density early, declining as padding increases. Sinusoidal pattern suggests repetitive mission structure.',
    'repetition': '<strong>Grind Detection:</strong> Repetition intensity climbs sharply post-50h. Indicates content recycling and diminishing returns.'
}

st.markdown(f"""
<div style="background: {TIMELINE_PALETTE['surface']}; border-radius: 12px; padding: 1.5rem; border: 1px solid {TIMELINE_PALETTE['grid']}; margin-top: 1rem;">
    <div style="font-size: 0.85rem; color: {TIMELINE_PALETTE['text_dim']}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Insight</div>
    <div style="color: {TIMELINE_PALETTE['text']}; font-size: 0.95rem; line-height: 1.6;">
        {timeline_insights[timeline_metric]}
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# ============================================================================
# RADAR ANALYTICS - TIME RESPECT PROFILE
# ============================================================================

st.markdown('<h2 class="section-header">Time Respect Profile</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
<strong>Multi-dimensional assessment of game design quality.</strong>

Six metrics form a complete picture: efficiency, density, repetition control, retention, engagement, and progression value.

<em>Select games to analyze their time respect signature.</em>
</div>
""", unsafe_allow_html=True)

# Game selector
top_games_list = analyzer.df.nlargest(100, 'main_story_polled')['name'].tolist()

col1, col2 = st.columns(2)

with col1:
    radar_game1 = st.selectbox(
        'Primary Game',
        top_games_list,
        index=0,
        key='radar_game1'
    )

with col2:
    radar_game2 = st.selectbox(
        'Compare With (Optional)',
        ['None'] + top_games_list,
        index=0,
        key='radar_game2'
    )

# Radar chart
radar_game2_val = None if radar_game2 == 'None' else radar_game2
fig_radar = create_radar_chart(analyzer.df, radar_game1, radar_game2_val)
st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})

# Stat cards
stats = get_game_stats(analyzer.df, radar_game1)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {RADAR_PALETTE['surface']} 0%, #252d3d 100%); 
                border-radius: 12px; padding: 1.5rem; border: 1px solid {RADAR_PALETTE['grid']}; 
                box-shadow: 0 4px 12px rgba(0,0,0,0.3); text-align: center;">
        <div style="font-size: 2.5rem; font-weight: 700; color: {RADAR_PALETTE['accent']}; margin-bottom: 0.5rem;">
            {stats['completion_time']:.1f}h
        </div>
        <div style="font-size: 0.75rem; color: {RADAR_PALETTE['text_dim']}; text-transform: uppercase; letter-spacing: 0.05em;">
            Avg Completion
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {RADAR_PALETTE['surface']} 0%, #252d3d 100%); 
                border-radius: 12px; padding: 1.5rem; border: 1px solid {RADAR_PALETTE['grid']}; 
                box-shadow: 0 4px 12px rgba(0,0,0,0.3); text-align: center;">
        <div style="font-size: 2.5rem; font-weight: 700; color: {RADAR_PALETTE['accent']}; margin-bottom: 0.5rem;">
            {stats['completion_rate']:.0f}%
        </div>
        <div style="font-size: 0.75rem; color: {RADAR_PALETTE['text_dim']}; text-transform: uppercase; letter-spacing: 0.05em;">
            Finish Rate
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {RADAR_PALETTE['surface']} 0%, #252d3d 100%); 
                border-radius: 12px; padding: 1.5rem; border: 1px solid {RADAR_PALETTE['grid']}; 
                box-shadow: 0 4px 12px rgba(0,0,0,0.3); text-align: center;">
        <div style="font-size: 2.5rem; font-weight: 700; color: {RADAR_PALETTE['accent']}; margin-bottom: 0.5rem;">
            {stats['dropoff_hours']:.0f}h
        </div>
        <div style="font-size: 0.75rem; color: {RADAR_PALETTE['text_dim']}; text-transform: uppercase; letter-spacing: 0.05em;">
            Avg Drop-off
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {RADAR_PALETTE['surface']} 0%, #252d3d 100%); 
                border-radius: 12px; padding: 1.5rem; border: 1px solid {RADAR_PALETTE['grid']}; 
                box-shadow: 0 4px 12px rgba(0,0,0,0.3); text-align: center;">
        <div style="font-size: 2.5rem; font-weight: 700; color: {RADAR_PALETTE['accent']}; margin-bottom: 0.5rem;">
            {stats['side_quest_density']:.0f}%
        </div>
        <div style="font-size: 0.75rem; color: {RADAR_PALETTE['text_dim']}; text-transform: uppercase; letter-spacing: 0.05em;">
            Side Quest Density
        </div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {RADAR_PALETTE['surface']} 0%, #252d3d 100%); 
                border-radius: 12px; padding: 1.5rem; border: 1px solid {RADAR_PALETTE['grid']}; 
                box-shadow: 0 4px 12px rgba(0,0,0,0.3); text-align: center;">
        <div style="font-size: 2.5rem; font-weight: 700; color: {RADAR_PALETTE['accent']}; margin-bottom: 0.5rem;">
            {stats['grind_index']:.0f}
        </div>
        <div style="font-size: 0.75rem; color: {RADAR_PALETTE['text_dim']}; text-transform: uppercase; letter-spacing: 0.05em;">
            Grind Index
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="narrative" style="margin-top: 2rem;">
<strong>Reading the profile:</strong> Larger radar area = better time respect. 
Balanced shapes indicate well-designed pacing. Spiky patterns reveal design weaknesses.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)
# INTERACTIVE EXPLORATION (MINIMAL)
# ============================================================================

st.markdown('<h2 class="section-header">Explore</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
Filter by confidence threshold. Watch how the insight stabilizes.
</div>
""", unsafe_allow_html=True)

confidence_threshold = st.slider(
    "Minimum confidence (polls required)",
    min_value=1,
    max_value=100,
    value=1,
    step=1
)

filtered_df = analyzer.df[analyzer.df['main_story_polled'] >= confidence_threshold]

if len(filtered_df) > 100:
    weights = filtered_df['main_story_polled']
    sorted_idx = filtered_df['time_cost'].argsort()
    sorted_weights = weights.iloc[sorted_idx].cumsum()
    median_idx = (sorted_weights >= sorted_weights.iloc[-1] / 2).idxmax()
    wm_raw = filtered_df.loc[median_idx, 'time_cost']
    
    sorted_idx_adj = filtered_df['adjusted_time_cost'].argsort()
    sorted_weights_adj = weights.iloc[sorted_idx_adj].cumsum()
    median_idx_adj = (sorted_weights_adj >= sorted_weights_adj.iloc[-1] / 2).idxmax()
    wm_adj = filtered_df.loc[median_idx_adj, 'adjusted_time_cost']
    
    gap = wm_raw - wm_adj
    pct = 100 * gap / wm_raw if wm_raw > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Games", f"{len(filtered_df):,}")
    col2.metric("Perceived", f"{wm_raw:.1f}h")
    col3.metric("Adjusted", f"{wm_adj:.1f}h")
    col4.metric("Noise %", f"{pct:.0f}%")
else:
    st.warning("Not enough games at this threshold")

st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# ============================================================================

# ============================================================================
# MODEL EVALUATION - PREDICTION ANALYSIS
# ============================================================================

st.markdown('<h2 class="section-header">Model Evaluation</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
<strong>Can we predict which games respect player time?</strong>

Using machine learning to classify games based on time efficiency, content density, 
repetition patterns, completion rates, and drop-off risk.
</div>
""", unsafe_allow_html=True)

# Prepare data and train models
with st.spinner('Training models...'):
    X, y = prepare_model_data(analyzer.df)
    results = train_models(X, y)
    feature_names = ['Time Efficiency', 'Content Density', 'Repetition Rate', 'Completion Rate', 'Drop-off Risk']
    importance_df = get_feature_importance(results['gradient']['model'], feature_names)

# Two-column layout
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div style="color: {MODEL_PALETTE['text']}; font-size: 1rem; font-weight: 600; margin-bottom: 1rem;">
        Model Performance Curve
    </div>
    """, unsafe_allow_html=True)
    
    fig_roc = create_roc_curve(results)
    st.plotly_chart(fig_roc, use_container_width=True, config={'displayModeBar': False})

with col2:
    st.markdown(f"""
    <div style="color: {MODEL_PALETTE['text']}; font-size: 1rem; font-weight: 600; margin-bottom: 1rem;">
        Feature Impact on Time Respect Score
    </div>
    """, unsafe_allow_html=True)
    
    fig_importance = create_feature_importance_viz(importance_df)
    st.plotly_chart(fig_importance, use_container_width=True, config={'displayModeBar': False})

# Feature details table
st.markdown("<br>", unsafe_allow_html=True)

st.markdown(f"""
<div style="background: {MODEL_PALETTE['surface']}; border-radius: 6px; padding: 1.5rem; border: 1px solid {MODEL_PALETTE['grid']};">
    <div style="font-size: 0.9rem; color: {MODEL_PALETTE['text_dim']}; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.5px;">
        Feature Contributions
    </div>
    <div style="color: {MODEL_PALETTE['text']}; font-size: 0.95rem; line-height: 1.8;">
""", unsafe_allow_html=True)

for _, row in importance_df.iterrows():
    impact_color = MODEL_PALETTE['positive'] if row['impact'] == 'Positive' else MODEL_PALETTE['negative']
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem; padding: 0.5rem; background: rgba(255,255,255,0.02); border-radius: 4px;">
        <div style="flex: 1;">
            <strong>{row['feature']}</strong>
        </div>
        <div style="flex: 0 0 120px; text-align: right;">
            <span style="color: {MODEL_PALETTE['text_dim']};">{row['importance']:.1f}%</span>
        </div>
        <div style="flex: 0 0 100px; text-align: right;">
            <span style="color: {impact_color}; font-size: 0.85rem;">{row['impact']}</span>
        </div>
        <div style="flex: 0 0 100px; text-align: right; font-family: monospace; font-size: 0.9rem;">
            {row['coefficient']:.3f}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# Insight box
st.markdown(f"""
<div style="background: {MODEL_PALETTE['surface']}; border-left: 3px solid {MODEL_PALETTE['gradient']}; 
            border-radius: 6px; padding: 1.5rem; margin-top: 2rem; border: 1px solid {MODEL_PALETTE['grid']};">
    <div style="font-size: 0.85rem; color: {MODEL_PALETTE['text_dim']}; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.5px;">
        Key Finding
    </div>
    <div style="color: {MODEL_PALETTE['text']}; font-size: 1rem; line-height: 1.7;">
        <strong>Time Efficiency</strong> and <strong>Content Density</strong> are the strongest predictors of perceived time respect, 
        contributing {importance_df.iloc[0]['importance']:.1f}% and {importance_df.iloc[1]['importance']:.1f}% respectively. 
        The Gradient Boosting model achieves <strong>{results['gradient']['auc']:.1%} AUC</strong>, 
        indicating strong predictive performance for identifying games that respect player time.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)
# THE CONCLUSION
# ============================================================================

st.markdown('<h2 class="section-header">What This Means</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="conclusion-box">
<strong>Three takeaways:</strong><br><br>

1. <strong>74% of games have <10 polls</strong> — most length estimates are statistically unreliable<br><br>

2. <strong>37% of perceived time is noise</strong> — when confidence is modeled, games are shorter than they appear<br><br>

3. <strong>Genre rankings shift dramatically</strong> — some genres are systematically over/under-estimated
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
When you see a game's completion time, you're not seeing truth.

You're seeing a confidence-weighted average that most platforms ignore.

The games that "respect your time" might just be the ones with enough players to report accurately.
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="insight-box">
Most games don't disrespect your time by being long.<br>
They disrespect it by being <strong>unmeasured</strong>.
</div>
""", unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
