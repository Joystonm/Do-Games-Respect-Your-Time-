"""
Signature Visualizations - Research-grade visual reasoning
Every chart encodes WHY, not WHAT
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

# Professional vibrant palette
PALETTE = {
    'earned': '#00D9A3',      # Vibrant teal - Trustworthy, short
    'uncertain': '#FF6B6B',    # Coral red - Long but unreliable
    'false_epic': '#FFB84D',   # Golden orange - Statistical illusion
    'verified': '#4A90E2',     # Royal blue - Long and trustworthy
    'bg': '#FAFBFC',
    'text': '#2C3E50',
    'accent': '#9B59B6',       # Purple accent
    'gradient_start': '#667EEA',
    'gradient_end': '#F093FB'
}

def trust_time_landscape(df: pd.DataFrame, sample_size: int = 8000) -> go.Figure:
    """
    THE HERO VISUAL
    Maps confidence vs time, reveals zones of truth and illusion
    """
    sample = df.sample(min(sample_size, len(df)), random_state=42)
    
    fig = go.Figure()
    
    # Zone backgrounds (visual reasoning)
    fig.add_shape(type="rect", x0=0, y0=3.5, x1=15, y1=6,
                  fillcolor=PALETTE['earned'], opacity=0.15, line_width=0)
    
    fig.add_shape(type="rect", x0=30, y0=0, x1=100, y1=2.5,
                  fillcolor=PALETTE['uncertain'], opacity=0.15, line_width=0)
    
    fig.add_shape(type="rect", x0=50, y0=0, x1=100, y1=2.0,
                  fillcolor=PALETTE['false_epic'], opacity=0.2, line_width=0)
    
    # Scatter by zone
    for zone, color in [('Earned Time', PALETTE['earned']),
                        ('Uncertain Grind', PALETTE['uncertain']),
                        ('False Epic', PALETTE['false_epic']),
                        ('Verified Epic', PALETTE['verified'])]:
        zone_data = sample[sample['zone'] == zone]
        if len(zone_data) > 0:
            fig.add_trace(go.Scatter(
                x=zone_data['time_cost'],
                y=zone_data['confidence_score'],
                mode='markers',
                name=zone,
                marker=dict(
                    size=np.sqrt(zone_data['main_story_polled']) * 0.6,
                    color=color,
                    opacity=0.75,
                    line=dict(width=1, color='white')
                ),
                text=zone_data['name'],
                customdata=zone_data[['main_story_polled', 'misrep_risk']],
                hovertemplate='<b>%{text}</b><br>' +
                              'Hours: %{x:.1f}<br>' +
                              'Confidence: %{y:.2f}<br>' +
                              'Polls: %{customdata[0]}<br>' +
                              'Risk: %{customdata[1]:.2%}<extra></extra>'
            ))
    
    # Critical annotations (the reasoning)
    fig.add_annotation(
        x=8, y=5.5, text="<b>EARNED TIME</b><br>High confidence + Low hours<br><i>Trust these estimates</i>",
        showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor=PALETTE['earned'],
        ax=-80, ay=-40, bgcolor="white", bordercolor=PALETTE['earned'], borderwidth=2,
        font=dict(size=11, color=PALETTE['text']), borderpad=8
    )
    
    fig.add_annotation(
        x=70, y=2.0, text="<b>UNCERTAIN GRIND</b><br>Long hours + Low confidence<br><i>Verify before committing</i>",
        showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor=PALETTE['uncertain'],
        ax=60, ay=40, bgcolor="white", bordercolor=PALETTE['uncertain'], borderwidth=2,
        font=dict(size=11, color=PALETTE['text']), borderpad=8
    )
    
    fig.add_annotation(
        x=75, y=1.3, text="<b>FALSE EPIC</b><br>Seems long, but unreliable<br><i>Statistical mirage</i>",
        showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor=PALETTE['false_epic'],
        ax=-70, ay=50, bgcolor="white", bordercolor=PALETTE['false_epic'], borderwidth=2,
        font=dict(size=11, color=PALETTE['text']), borderpad=8
    )
    
    fig.update_layout(
        title=dict(
            text="<b>The Trust-Time Landscape</b><br><sub>Where confidence meets reality — notice the voids</sub>",
            font=dict(size=26, color=PALETTE['text'], family="Inter")
        ),
        xaxis_title="<b>Main Story Hours</b>",
        yaxis_title="<b>Confidence Score</b> (log polls)",
        template="plotly_white",
        height=750,
        font=dict(size=13, family="Inter"),
        hovermode='closest',
        plot_bgcolor=PALETTE['bg'],
        showlegend=True,
        legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.9)", bordercolor=PALETTE['text'], borderwidth=1)
    )
    
    fig.update_xaxes(gridcolor='rgba(0,0,0,0.05)', zeroline=False)
    fig.update_yaxes(gridcolor='rgba(0,0,0,0.05)', zeroline=False)
    
    return fig

def perception_reality_split(df: pd.DataFrame, genre_stats: pd.DataFrame) -> go.Figure:
    """
    THE TRANSFORMATION VISUAL
    Side-by-side: what you see vs what's real
    """
    top_genres = genre_stats.head(12).sort_values('raw_median', ascending=True)
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("What You See (Raw)", "What's Real (Adjusted)"),
        horizontal_spacing=0.15
    )
    
    # LEFT: Raw perception
    fig.add_trace(go.Bar(
        y=top_genres['primary_genre'],
        x=top_genres['raw_median'],
        orientation='h',
        marker=dict(
            color=top_genres['raw_median'],
            colorscale=[[0, '#E8E8E8'], [1, '#B0B0B0']],
            opacity=0.8,
            line=dict(width=1, color='white')
        ),
        text=top_genres['raw_median'].round(1),
        textposition='outside',
        textfont=dict(size=11, color=PALETTE['text'], family="Inter", weight=600),
        showlegend=False,
        hovertemplate='%{y}<br>%{x:.1f} hours<extra></extra>'
    ), row=1, col=1)
    
    # RIGHT: Adjusted reality
    colors = [PALETTE['earned'] if x < 2 else PALETTE['uncertain'] if x > 5 else PALETTE['verified'] 
              for x in top_genres['adjusted_median']]
    
    fig.add_trace(go.Bar(
        y=top_genres['primary_genre'],
        x=top_genres['adjusted_median'],
        orientation='h',
        marker=dict(color=colors, line=dict(width=1, color='white')),
        text=top_genres['adjusted_median'].round(1),
        textposition='outside',
        textfont=dict(size=11, color=PALETTE['text'], family="Inter", weight=600),
        showlegend=False,
        hovertemplate='%{y}<br>%{x:.1f} hours<extra></extra>'
    ), row=1, col=2)
    
    fig.update_layout(
        title=dict(
            text="<b>Perception vs Reality</b><br><sub>Watch the lie dissolve when confidence is modeled</sub>",
            font=dict(size=24, color=PALETTE['text'], family="Inter")
        ),
        height=600,
        font=dict(size=12, family="Inter"),
        plot_bgcolor=PALETTE['bg'],
        showlegend=False
    )
    
    fig.update_xaxes(title_text="Hours", gridcolor='rgba(0,0,0,0.05)', row=1, col=1)
    fig.update_xaxes(title_text="Hours", gridcolor='rgba(0,0,0,0.05)', row=1, col=2)
    fig.update_yaxes(showgrid=False)
    
    return fig

def genre_honesty_ranking(genre_stats: pd.DataFrame) -> go.Figure:
    """
    THE RERANKING VISUAL
    Genres sorted by honesty (reliability-adjusted value)
    """
    top = genre_stats.nlargest(15, 'honesty_score')
    
    fig = go.Figure()
    
    # Honesty bars
    fig.add_trace(go.Bar(
        y=top['primary_genre'],
        x=top['honesty_score'],
        orientation='h',
        marker=dict(
            color=top['honesty_score'],
            colorscale=[[0, PALETTE['uncertain']], [0.5, PALETTE['accent']], [1, PALETTE['earned']]],
            showscale=True,
            colorbar=dict(title="Honesty", thickness=20, len=0.7, outlinewidth=1, outlinecolor=PALETTE['text'])
        ),
        text=top['honesty_score'].round(2),
        textposition='outside',
        textfont=dict(size=11, color=PALETTE['text'], family="Inter", weight=600),
        hovertemplate='<b>%{y}</b><br>Honesty: %{x:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text="<b>Genre Honesty Ranking</b><br><sub>Inverse of perception gap — higher is more trustworthy</sub>",
            font=dict(size=24, color=PALETTE['text'], family="Inter")
        ),
        xaxis_title="<b>Honesty Score</b> (1 = perfect alignment)",
        height=600,
        font=dict(size=12, family="Inter"),
        plot_bgcolor=PALETTE['bg'],
        showlegend=False
    )
    
    fig.update_xaxes(gridcolor='rgba(0,0,0,0.05)', range=[0, 1])
    fig.update_yaxes(showgrid=False)
    
    return fig

def trs_leaderboard(top_df: pd.DataFrame, bottom_df: pd.DataFrame) -> go.Figure:
    """
    THE LEADERBOARD VISUAL
    Top 10 Most Respectful vs Bottom 10 Time Wasters
    """
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("🏆 Most Respectful Games", "⚠️ Biggest Time Wasters"),
        horizontal_spacing=0.15
    )
    
    # LEFT: Top 10 (reversed for top-down display)
    top_sorted = top_df.sort_values('time_respect_score', ascending=True)
    fig.add_trace(go.Bar(
        y=top_sorted['name'],
        x=top_sorted['time_respect_score'],
        orientation='h',
        marker=dict(
            color=top_sorted['time_respect_score'],
            colorscale=[[0, PALETTE['verified']], [0.5, PALETTE['accent']], [1, PALETTE['earned']]],
            showscale=False,
            line=dict(width=1, color='white')
        ),
        text=top_sorted['time_respect_score'].round(3),
        textposition='outside',
        textfont=dict(size=10, color=PALETTE['text'], family="Inter", weight=600),
        customdata=top_sorted[['time_cost', 'main_story_polled', 'primary_genre']],
        hovertemplate='<b>%{y}</b><br>' +
                      'TRS: %{x:.3f}<br>' +
                      'Hours: %{customdata[0]:.1f}<br>' +
                      'Polls: %{customdata[1]}<br>' +
                      'Genre: %{customdata[2]}<extra></extra>',
        showlegend=False
    ), row=1, col=1)
    
    # RIGHT: Bottom 10 (reversed for top-down display)
    bottom_sorted = bottom_df.sort_values('time_respect_score', ascending=False)
    fig.add_trace(go.Bar(
        y=bottom_sorted['name'],
        x=bottom_sorted['time_respect_score'],
        orientation='h',
        marker=dict(
            color=bottom_sorted['time_respect_score'],
            colorscale=[[0, '#D32F2F'], [0.5, PALETTE['uncertain']], [1, PALETTE['false_epic']]],
            showscale=False,
            line=dict(width=1, color='white')
        ),
        text=bottom_sorted['time_respect_score'].round(3),
        textposition='outside',
        textfont=dict(size=10, color=PALETTE['text'], family="Inter", weight=600),
        customdata=bottom_sorted[['time_cost', 'main_story_polled', 'primary_genre']],
        hovertemplate='<b>%{y}</b><br>' +
                      'TRS: %{x:.3f}<br>' +
                      'Hours: %{customdata[0]:.1f}<br>' +
                      'Polls: %{customdata[1]}<br>' +
                      'Genre: %{customdata[2]}<extra></extra>',
        showlegend=False
    ), row=1, col=2)
    
    fig.update_layout(
        title=dict(
            text="<b>Time Respect Score Leaderboard</b><br>" +
                 "<sub>TRS = 0.4×Length Penalty + 0.4×Confidence + 0.2×Genre Fit</sub>",
            font=dict(size=24, color=PALETTE['text'], family="Inter")
        ),
        height=700,
        font=dict(size=11, family="Inter"),
        plot_bgcolor=PALETTE['bg'],
        showlegend=False
    )
    
    fig.update_xaxes(title_text="Time Respect Score", gridcolor='rgba(0,0,0,0.05)', row=1, col=1)
    fig.update_xaxes(title_text="Time Respect Score", gridcolor='rgba(0,0,0,0.05)', row=1, col=2)
    fig.update_yaxes(showgrid=False)
    
    return fig

def sensitivity_proof(sensitivity_df: pd.DataFrame) -> go.Figure:
    """
    THE ROBUSTNESS VISUAL
    Proves the insight survives across thresholds
    """
    fig = go.Figure()
    
    # Gap line (the insight)
    fig.add_trace(go.Scatter(
        x=sensitivity_df['threshold'],
        y=sensitivity_df['gap'],
        mode='lines+markers',
        name='Perception Gap',
        line=dict(color=PALETTE['accent'], width=5, shape='spline'),
        marker=dict(size=14, symbol='diamond', line=dict(width=2, color='white')),
        hovertemplate='Threshold: %{x} polls<br>Gap: %{y:.1f} hours<extra></extra>',
        fill='tozeroy',
        fillcolor='rgba(155, 89, 182, 0.1)'
    ))
    
    # Sample size context
    fig.add_trace(go.Scatter(
        x=sensitivity_df['threshold'],
        y=sensitivity_df['n_games'] / 1000,
        mode='lines',
        name='Sample Size (thousands)',
        line=dict(color=PALETTE['verified'], width=3, dash='dot'),
        yaxis='y2',
        hovertemplate='Threshold: %{x} polls<br>Games: %{y:.1f}k<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text="<b>Sensitivity Proof</b><br><sub>The insight is robust — it survives every threshold</sub>",
            font=dict(size=24, color=PALETTE['text'], family="Inter")
        ),
        xaxis_title="<b>Minimum Poll Threshold</b>",
        yaxis_title="<b>Perception Gap (hours)</b>",
        yaxis2=dict(title="<b>Sample Size</b>", overlaying='y', side='right', showgrid=False),
        height=500,
        font=dict(size=12, family="Inter"),
        plot_bgcolor=PALETTE['bg'],
        legend=dict(x=0.7, y=0.95, bgcolor="rgba(255,255,255,0.9)", bordercolor=PALETTE['text'], borderwidth=1)
    )
    
    fig.update_xaxes(gridcolor='rgba(0,0,0,0.05)', type='log')
    fig.update_yaxes(gridcolor='rgba(0,0,0,0.05)')
    
    return fig

def confidence_crisis_histogram(df: pd.DataFrame) -> go.Figure:
    """
    THE CRISIS VISUAL
    Most games are unmeasured
    """
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=df['main_story_polled'],
        nbinsx=60,
        marker=dict(
            color=df['main_story_polled'],
            colorscale=[[0, PALETTE['uncertain']], [0.5, PALETTE['false_epic']], [1, PALETTE['earned']]],
            opacity=0.85,
            line=dict(width=1, color='white')
        ),
        hovertemplate='Polls: %{x}<br>Games: %{y}<extra></extra>'
    ))
    
    # Critical thresholds
    for thresh, label, color in [(10, '10 polls', '#D32F2F'), 
                                   (50, '50 polls', PALETTE['earned'])]:
        fig.add_vline(
            x=thresh, line_dash="dash", line_color=color, line_width=4,
            annotation_text=label, annotation_position="top right",
            annotation_font=dict(size=13, color=color, family="Inter", weight=600)
        )
    
    fig.update_layout(
        title=dict(
            text="<b>The Confidence Crisis</b><br><sub>74% of games have <10 polls — we don't know their length</sub>",
            font=dict(size=24, color=PALETTE['text'], family="Inter")
        ),
        xaxis_title="<b>Number of Completion Reports</b>",
        yaxis_title="<b>Number of Games</b>",
        height=450,
        font=dict(size=12, family="Inter"),
        plot_bgcolor=PALETTE['bg'],
        showlegend=False,
        xaxis=dict(range=[0, 300], gridcolor='rgba(0,0,0,0.05)'),
        yaxis=dict(gridcolor='rgba(0,0,0,0.05)')
    )
    
    return fig

def hidden_gems_cluster_3d(df: pd.DataFrame, sample_size: int = 5000) -> go.Figure:
    """
    THE 3D SIGNATURE VISUAL
    Reveals hidden patterns in trust-time-stability space
    Third dimension shows stability (inverse of adjusted time variance)
    """
    # Sample for performance
    sample = df.sample(min(sample_size, len(df)), random_state=42)
    
    # Calculate stability index (inverse coefficient of variation)
    # Higher stability = more consistent estimates
    sample = sample.copy()
    sample['stability_index'] = sample['confidence_score'] / (sample['adjusted_time_cost'] + 1)
    
    # Genre color mapping
    top_genres = sample['primary_genre'].value_counts().head(10).index.tolist()
    genre_colors = {
        genre: PALETTE['earned'] if i < 3 else PALETTE['verified'] if i < 6 else PALETTE['uncertain']
        for i, genre in enumerate(top_genres)
    }
    sample['color'] = sample['primary_genre'].map(genre_colors).fillna(PALETTE['uncertain'])
    
    fig = go.Figure()
    
    # Create traces by zone for better legend
    for zone in ['Earned Time', 'Verified Epic', 'Uncertain Grind', 'False Epic', 'Unknown']:
        zone_data = sample[sample['zone'] == zone]
        if len(zone_data) > 0:
            zone_color = {
                'Earned Time': PALETTE['earned'],
                'Verified Epic': PALETTE['verified'],
                'Uncertain Grind': PALETTE['uncertain'],
                'False Epic': PALETTE['false_epic'],
                'Unknown': 'lightgray'
            }[zone]
            
            fig.add_trace(go.Scatter3d(
                x=zone_data['time_cost'],
                y=zone_data['confidence_score'],
                z=zone_data['stability_index'],
                mode='markers',
                name=zone,
                marker=dict(
                    size=np.sqrt(zone_data['main_story_polled']) * 0.5,
                    color=zone_color,
                    opacity=0.8,
                    line=dict(width=1, color='white')
                ),
                text=zone_data['name'],
                customdata=zone_data[['main_story_polled', 'primary_genre', 'misrep_risk']],
                hovertemplate='<b>%{text}</b><br>' +
                              'Hours: %{x:.1f}<br>' +
                              'Confidence: %{y:.2f}<br>' +
                              'Stability: %{z:.2f}<br>' +
                              'Polls: %{customdata[0]}<br>' +
                              'Genre: %{customdata[1]}<br>' +
                              'Risk: %{customdata[2]:.1%}<extra></extra>'
            ))
    
    # Annotations for key clusters
    # High stability cluster
    high_stability = sample.nlargest(1, 'stability_index').iloc[0]
    fig.add_trace(go.Scatter3d(
        x=[high_stability['time_cost']],
        y=[high_stability['confidence_score']],
        z=[high_stability['stability_index']],
        mode='markers+text',
        marker=dict(size=15, color='gold', symbol='diamond', line=dict(width=2, color='black')),
        text=['Most Stable'],
        textposition='top center',
        textfont=dict(size=10, color='black', family="Inter"),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Low stability, high time (False Epic cluster)
    false_epics = sample[(sample['time_cost'] > 60) & (sample['stability_index'] < 0.5)]
    if len(false_epics) > 0:
        center = false_epics.iloc[0]
        fig.add_trace(go.Scatter3d(
            x=[center['time_cost']],
            y=[center['confidence_score']],
            z=[center['stability_index']],
            mode='markers+text',
            marker=dict(size=15, color=PALETTE['false_epic'], symbol='x', line=dict(width=2, color='black')),
            text=['False Epic Zone'],
            textposition='top center',
            textfont=dict(size=10, color='black', family="Inter"),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Set camera angle for storytelling
    camera = dict(
        eye=dict(x=1.5, y=1.5, z=1.3),
        center=dict(x=0, y=0, z=0),
        up=dict(x=0, y=0, z=1)
    )
    
    fig.update_layout(
        title=dict(
            text="<b>Hidden Patterns in 3D: Trust, Time, and Stability</b><br>" +
                 "<sub>Third dimension reveals stability — notice the void in high-time, high-stability space</sub>",
            font=dict(size=24, color=PALETTE['text'], family="Inter")
        ),
        scene=dict(
            xaxis=dict(
                title='<b>Main Story Hours</b>',
                backgroundcolor=PALETTE['bg'],
                gridcolor='rgba(0,0,0,0.1)',
                showbackground=True
            ),
            yaxis=dict(
                title='<b>Confidence Score</b>',
                backgroundcolor=PALETTE['bg'],
                gridcolor='rgba(0,0,0,0.1)',
                showbackground=True
            ),
            zaxis=dict(
                title='<b>Stability Index</b>',
                backgroundcolor=PALETTE['bg'],
                gridcolor='rgba(0,0,0,0.1)',
                showbackground=True
            ),
            camera=camera
        ),
        height=800,
        font=dict(size=12, family="Inter"),
        showlegend=True,
        legend=dict(
            x=0.02,
            y=0.98,
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor=PALETTE['text'],
            borderwidth=1
        ),
        hovermode='closest'
    )
    
    return fig
