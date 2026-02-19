"""
Premium Radar Analytics - Game Time Respect Profile
Research-grade multi-dimensional assessment
"""
import plotly.graph_objects as go
import numpy as np
import pandas as pd

RADAR_PALETTE = {
    'bg': '#0f1419',
    'surface': '#1a1f2e',
    'grid': '#2a3441',
    'text': '#e8eaed',
    'text_dim': '#9aa0a6',
    'accent': '#6366f1',
    'accent_glow': 'rgba(99, 102, 241, 0.4)',
    'compare': '#ec4899',
    'compare_glow': 'rgba(236, 72, 153, 0.4)'
}

def calculate_game_profile(df, game_name):
    """Calculate 6-dimensional time respect profile"""
    game = df[df['name'] == game_name].iloc[0]
    
    # Normalize metrics to 0-100 scale
    time_efficiency = 100 - min(100, (game['main_story'] / df['main_story'].quantile(0.95)) * 100)
    content_density = min(100, (game['confidence_score'] / df['confidence_score'].quantile(0.95)) * 100)
    repetition_level = 100 - min(100, (game.get('main_extras', game['main_story']) / game['main_story'] - 1) * 50)
    dropoff_risk = 100 - min(100, (game['main_story'] / 50) * 100)
    engagement_depth = min(100, (game['main_story_polled'] / df['main_story_polled'].quantile(0.75)) * 100)
    progression = min(100, game['time_respect_score'] * 100) if 'time_respect_score' in game else 50
    
    return {
        'Time Efficiency': max(0, min(100, time_efficiency)),
        'Content Density': max(0, min(100, content_density)),
        'Repetition Control': max(0, min(100, repetition_level)),
        'Retention Quality': max(0, min(100, dropoff_risk)),
        'Engagement Depth': max(0, min(100, engagement_depth)),
        'Progression Value': max(0, min(100, progression))
    }

def create_radar_chart(df, game1_name, game2_name=None):
    """Premium radar visualization with optional comparison"""
    profile1 = calculate_game_profile(df, game1_name)
    categories = list(profile1.keys())
    values1 = list(profile1.values())
    
    fig = go.Figure()
    
    # Primary game
    fig.add_trace(go.Scatterpolar(
        r=values1 + [values1[0]],
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor=RADAR_PALETTE['accent_glow'],
        line=dict(color=RADAR_PALETTE['accent'], width=3),
        name=game1_name,
        hovertemplate='<b>%{theta}</b><br>Score: %{r:.1f}/100<extra></extra>'
    ))
    
    # Comparison game
    if game2_name:
        profile2 = calculate_game_profile(df, game2_name)
        values2 = list(profile2.values())
        fig.add_trace(go.Scatterpolar(
            r=values2 + [values2[0]],
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor=RADAR_PALETTE['compare_glow'],
            line=dict(color=RADAR_PALETTE['compare'], width=3),
            name=game2_name,
            hovertemplate='<b>%{theta}</b><br>Score: %{r:.1f}/100<extra></extra>'
        ))
    
    fig.update_layout(
        polar=dict(
            bgcolor=RADAR_PALETTE['bg'],
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor=RADAR_PALETTE['grid'],
                gridwidth=1,
                tickfont=dict(size=10, color=RADAR_PALETTE['text_dim']),
                tickmode='linear',
                tick0=0,
                dtick=25
            ),
            angularaxis=dict(
                gridcolor=RADAR_PALETTE['grid'],
                gridwidth=1,
                linecolor=RADAR_PALETTE['grid'],
                tickfont=dict(size=12, color=RADAR_PALETTE['text'], family='Inter, sans-serif')
            )
        ),
        paper_bgcolor=RADAR_PALETTE['bg'],
        plot_bgcolor=RADAR_PALETTE['bg'],
        font=dict(family='Inter, sans-serif', color=RADAR_PALETTE['text']),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.2,
            xanchor='center',
            x=0.5,
            font=dict(size=12),
            bgcolor='rgba(0,0,0,0)'
        ),
        margin=dict(l=80, r=80, t=40, b=80),
        height=500
    )
    
    return fig

def get_game_stats(df, game_name):
    """Extract key stats for stat cards"""
    game = df[df['name'] == game_name].iloc[0]
    
    # Calculate derived metrics
    completion_rate = min(100, (game['main_story_polled'] / df['main_story_polled'].quantile(0.5)) * 50)
    dropoff_hours = game['main_story'] * 0.7  # Estimate
    side_quest_density = ((game.get('main_extras', game['main_story']) / game['main_story']) - 1) * 100 if game.get('main_extras', 0) > 0 else 0
    grind_index = max(0, min(100, (game['main_story'] / 30) * 100 - 50))
    
    return {
        'completion_time': game['main_story'],
        'completion_rate': max(0, min(100, completion_rate)),
        'dropoff_hours': dropoff_hours,
        'side_quest_density': max(0, side_quest_density),
        'grind_index': grind_index
    }
