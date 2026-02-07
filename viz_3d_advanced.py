"""
Advanced 3D Visualizations - Multi-dimensional pattern revelation
Each chart reveals unique insights impossible to see in 2D
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

# Editorial palette
PALETTE = {
    'earned': '#2A9D8F',
    'uncertain': '#E76F51',
    'false_epic': '#F4A261',
    'verified': '#264653',
    'bg': '#F8F9FA',
    'text': '#1A1A1A',
    'accent': '#E63946'
}

def trust_time_stability_3d(df: pd.DataFrame, sample_size: int = 6000) -> go.Figure:
    """
    3D #1: Trust-Time-Stability Landscape
    Reveals the void where trustworthy long games should be
    """
    sample = df.sample(min(sample_size, len(df)), random_state=42).copy()
    sample['stability_index'] = sample['confidence_score'] / (sample['adjusted_time_cost'] + 1)
    
    fig = go.Figure()
    
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
                    opacity=0.7,
                    line=dict(width=0.5, color='white')
                ),
                text=zone_data['name'],
                customdata=zone_data[['main_story_polled', 'primary_genre']],
                hovertemplate='<b>%{text}</b><br>Hours: %{x:.1f}<br>Confidence: %{y:.2f}<br>Stability: %{z:.2f}<br>Polls: %{customdata[0]}<br>Genre: %{customdata[1]}<extra></extra>'
            ))
    
    # Annotation: The Void
    fig.add_trace(go.Scatter3d(
        x=[80], y=[5], z=[3],
        mode='text',
        text=['THE VOID<br>(Trustworthy epics<br>barely exist)'],
        textfont=dict(size=12, color=PALETTE['accent'], family="Inter"),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    camera = dict(eye=dict(x=1.5, y=1.5, z=1.3))
    
    fig.update_layout(
        title=dict(
            text="<b>Trust-Time-Stability Landscape</b><br><sub>The void reveals truth: trustworthy long games are exceptional</sub>",
            font=dict(size=24, color=PALETTE['text'], family="Inter")
        ),
        scene=dict(
            xaxis=dict(title='<b>Hours</b>', backgroundcolor=PALETTE['bg'], gridcolor='rgba(0,0,0,0.1)'),
            yaxis=dict(title='<b>Confidence</b>', backgroundcolor=PALETTE['bg'], gridcolor='rgba(0,0,0,0.1)'),
            zaxis=dict(title='<b>Stability</b>', backgroundcolor=PALETTE['bg'], gridcolor='rgba(0,0,0,0.1)'),
            camera=camera
        ),
        height=800,
        font=dict(size=12, family="Inter"),
        showlegend=True,
        legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.9)", bordercolor=PALETTE['text'], borderwidth=1)
    )
    
    return fig

def genre_honesty_orbit_3d(df: pd.DataFrame) -> go.Figure:
    """
    3D #2: Genre Honesty Orbit
    Reveals which genres are honest vs misleading
    """
    # Calculate genre stats with std dev
    genre_stats = df.groupby('primary_genre').agg({
        'time_cost': ['median', 'std', 'count'],
        'confidence_score': 'median',
        'main_story_polled': 'sum'
    }).reset_index()
    
    genre_stats.columns = ['genre', 'median_time', 'time_std', 'count', 'median_conf', 'total_polls']
    genre_stats = genre_stats[genre_stats['count'] >= 30].copy()
    
    # Honesty score (inverse of std/median ratio)
    genre_stats['honesty'] = 1 / (1 + genre_stats['time_std'] / (genre_stats['median_time'] + 1))
    
    # Color by honesty
    colors = genre_stats['honesty'].values
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter3d(
        x=genre_stats['median_time'],
        y=genre_stats['median_conf'],
        z=genre_stats['time_std'],
        mode='markers+text',
        marker=dict(
            size=np.sqrt(genre_stats['count']) * 2,
            color=colors,
            colorscale='RdYlGn',
            showscale=True,
            colorbar=dict(title="Honesty", thickness=15, len=0.7),
            line=dict(width=1, color='white')
        ),
        text=genre_stats['genre'],
        textposition='top center',
        textfont=dict(size=8, family="Inter"),
        customdata=genre_stats[['count', 'honesty', 'total_polls']],
        hovertemplate='<b>%{text}</b><br>Median Time: %{x:.1f}h<br>Confidence: %{y:.2f}<br>Std Dev: %{z:.1f}<br>Games: %{customdata[0]}<br>Honesty: %{customdata[1]:.2f}<extra></extra>'
    ))
    
    # Annotate most honest
    most_honest = genre_stats.nlargest(1, 'honesty').iloc[0]
    fig.add_trace(go.Scatter3d(
        x=[most_honest['median_time']],
        y=[most_honest['median_conf']],
        z=[most_honest['time_std']],
        mode='markers',
        marker=dict(size=20, color='gold', symbol='diamond', line=dict(width=3, color='black')),
        name='Most Honest',
        hoverinfo='skip'
    ))
    
    # Annotate most misleading
    most_misleading = genre_stats.nsmallest(1, 'honesty').iloc[0]
    fig.add_trace(go.Scatter3d(
        x=[most_misleading['median_time']],
        y=[most_misleading['median_conf']],
        z=[most_misleading['time_std']],
        mode='markers',
        marker=dict(size=20, color=PALETTE['accent'], symbol='x', line=dict(width=3, color='black')),
        name='Most Misleading',
        hoverinfo='skip'
    ))
    
    camera = dict(eye=dict(x=1.3, y=1.3, z=1.5))
    
    fig.update_layout(
        title=dict(
            text="<b>Genre Honesty Orbit</b><br><sub>Z-axis shows variability — higher = less consistent</sub>",
            font=dict(size=24, color=PALETTE['text'], family="Inter")
        ),
        scene=dict(
            xaxis=dict(title='<b>Median Hours</b>', backgroundcolor=PALETTE['bg'], gridcolor='rgba(0,0,0,0.1)'),
            yaxis=dict(title='<b>Confidence</b>', backgroundcolor=PALETTE['bg'], gridcolor='rgba(0,0,0,0.1)'),
            zaxis=dict(title='<b>Std Deviation</b>', backgroundcolor=PALETTE['bg'], gridcolor='rgba(0,0,0,0.1)'),
            camera=camera
        ),
        height=800,
        font=dict(size=12, family="Inter"),
        showlegend=True,
        legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.9)", bordercolor=PALETTE['text'], borderwidth=1)
    )
    
    return fig

def platform_reliability_cube_3d(df: pd.DataFrame) -> go.Figure:
    """
    3D #3: Platform Reliability Cube
    Reveals platform-specific patterns
    """
    # Get primary platform
    df_platform = df.copy()
    df_platform['primary_platform'] = df_platform['platform'].fillna('Unknown').str.split(',').str[0].str.strip()
    
    # Platform stats
    platform_stats = df_platform.groupby('primary_platform').agg({
        'time_cost': 'median',
        'confidence_score': 'median',
        'main_story_polled': ['sum', 'count']
    }).reset_index()
    
    platform_stats.columns = ['platform', 'median_time', 'median_conf', 'total_polls', 'count']
    platform_stats = platform_stats[platform_stats['count'] >= 50].copy()
    platform_stats = platform_stats.sort_values('median_time')
    
    # Encode platform as numeric
    platform_stats['platform_num'] = range(len(platform_stats))
    
    # Color by confidence
    colors = platform_stats['median_conf'].values
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter3d(
        x=platform_stats['platform_num'],
        y=platform_stats['median_time'],
        z=platform_stats['median_conf'],
        mode='markers+text',
        marker=dict(
            size=np.sqrt(platform_stats['count']) * 1.5,
            color=colors,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Confidence", thickness=15, len=0.7),
            line=dict(width=1, color='white')
        ),
        text=platform_stats['platform'],
        textposition='top center',
        textfont=dict(size=8, family="Inter"),
        customdata=platform_stats[['count', 'total_polls']],
        hovertemplate='<b>%{text}</b><br>Median Time: %{y:.1f}h<br>Confidence: %{z:.2f}<br>Games: %{customdata[0]}<br>Total Polls: %{customdata[1]}<extra></extra>'
    ))
    
    camera = dict(eye=dict(x=1.8, y=1.2, z=1.2))
    
    fig.update_layout(
        title=dict(
            text="<b>Platform Reliability Cube</b><br><sub>Each platform occupies unique trust-time space</sub>",
            font=dict(size=24, color=PALETTE['text'], family="Inter")
        ),
        scene=dict(
            xaxis=dict(title='<b>Platform</b>', backgroundcolor=PALETTE['bg'], gridcolor='rgba(0,0,0,0.1)', showticklabels=False),
            yaxis=dict(title='<b>Median Hours</b>', backgroundcolor=PALETTE['bg'], gridcolor='rgba(0,0,0,0.1)'),
            zaxis=dict(title='<b>Confidence</b>', backgroundcolor=PALETTE['bg'], gridcolor='rgba(0,0,0,0.1)'),
            camera=camera
        ),
        height=800,
        font=dict(size=12, family="Inter"),
        showlegend=False
    )
    
    return fig

def misrepresentation_risk_helix_3d(df: pd.DataFrame, sample_size: int = 5000) -> go.Figure:
    """
    3D #4: Misrepresentation Risk Helix
    Reveals games that look long but are unreliable
    """
    sample = df.sample(min(sample_size, len(df)), random_state=42).copy()
    
    # High risk games (top 20%)
    risk_threshold = sample['misrep_risk'].quantile(0.8)
    sample['risk_category'] = sample['misrep_risk'].apply(
        lambda x: 'High Risk' if x >= risk_threshold else 'Moderate Risk' if x >= sample['misrep_risk'].median() else 'Low Risk'
    )
    
    fig = go.Figure()
    
    for risk_cat, color in [('Low Risk', PALETTE['earned']), 
                             ('Moderate Risk', PALETTE['false_epic']), 
                             ('High Risk', PALETTE['accent'])]:
        cat_data = sample[sample['risk_category'] == risk_cat]
        if len(cat_data) > 0:
            fig.add_trace(go.Scatter3d(
                x=cat_data['adjusted_time_cost'],
                y=cat_data['confidence_score'],
                z=cat_data['misrep_risk'],
                mode='markers',
                name=risk_cat,
                marker=dict(
                    size=np.sqrt(cat_data['main_story_polled']) * 0.6,
                    color=color,
                    opacity=0.7,
                    line=dict(width=0.5, color='white')
                ),
                text=cat_data['name'],
                customdata=cat_data[['main_story_polled', 'time_cost']],
                hovertemplate='<b>%{text}</b><br>Adj Time: %{x:.1f}h<br>Confidence: %{y:.2f}<br>Risk: %{z:.2%}<br>Polls: %{customdata[0]}<extra></extra>'
            ))
    
    # Annotate danger zone
    danger_zone = sample[(sample['adjusted_time_cost'] > 50) & (sample['misrep_risk'] > 0.5)]
    if len(danger_zone) > 0:
        fig.add_trace(go.Scatter3d(
            x=[danger_zone['adjusted_time_cost'].mean()],
            y=[danger_zone['confidence_score'].mean()],
            z=[danger_zone['misrep_risk'].mean()],
            mode='text',
            text=['DANGER ZONE<br>(Long + Unreliable)'],
            textfont=dict(size=12, color=PALETTE['accent'], family="Inter"),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    camera = dict(eye=dict(x=1.4, y=1.4, z=1.4))
    
    fig.update_layout(
        title=dict(
            text="<b>Misrepresentation Risk Helix</b><br><sub>High Z-axis = unreliable estimates — avoid the danger zone</sub>",
            font=dict(size=24, color=PALETTE['text'], family="Inter")
        ),
        scene=dict(
            xaxis=dict(title='<b>Adjusted Hours</b>', backgroundcolor=PALETTE['bg'], gridcolor='rgba(0,0,0,0.1)'),
            yaxis=dict(title='<b>Confidence</b>', backgroundcolor=PALETTE['bg'], gridcolor='rgba(0,0,0,0.1)'),
            zaxis=dict(title='<b>Risk Score</b>', backgroundcolor=PALETTE['bg'], gridcolor='rgba(0,0,0,0.1)'),
            camera=camera
        ),
        height=800,
        font=dict(size=12, family="Inter"),
        showlegend=True,
        legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.9)", bordercolor=PALETTE['text'], borderwidth=1)
    )
    
    return fig

def hidden_gems_cluster_3d(df: pd.DataFrame, sample_size: int = 4000) -> go.Figure:
    """
    3D #5: Hidden Gems Cluster Explorer
    Reveals underrated (high confidence, low time) vs overhyped (low confidence, high time)
    """
    sample = df.sample(min(sample_size, len(df)), random_state=42).copy()
    
    # Classify games
    high_conf = sample['confidence_score'] > sample['confidence_score'].quantile(0.7)
    low_time = sample['adjusted_time_cost'] < sample['adjusted_time_cost'].quantile(0.3)
    high_time = sample['adjusted_time_cost'] > sample['adjusted_time_cost'].quantile(0.7)
    low_conf = sample['confidence_score'] < sample['confidence_score'].quantile(0.3)
    
    sample['cluster'] = 'Standard'
    sample.loc[high_conf & low_time, 'cluster'] = 'Hidden Gems'
    sample.loc[low_conf & high_time, 'cluster'] = 'Overhyped'
    sample.loc[high_conf & high_time, 'cluster'] = 'Verified Epics'
    
    fig = go.Figure()
    
    for cluster, color in [('Hidden Gems', PALETTE['earned']), 
                            ('Verified Epics', PALETTE['verified']),
                            ('Overhyped', PALETTE['accent']),
                            ('Standard', 'lightgray')]:
        cluster_data = sample[sample['cluster'] == cluster]
        if len(cluster_data) > 0:
            fig.add_trace(go.Scatter3d(
                x=cluster_data['adjusted_time_cost'],
                y=cluster_data['confidence_score'],
                z=cluster_data['main_story_polled'],
                mode='markers',
                name=cluster,
                marker=dict(
                    size=5 if cluster == 'Standard' else 8,
                    color=color,
                    opacity=0.5 if cluster == 'Standard' else 0.8,
                    line=dict(width=0.5, color='white')
                ),
                text=cluster_data['name'],
                customdata=cluster_data[['time_cost', 'primary_genre']],
                hovertemplate='<b>%{text}</b><br>Adj Time: %{x:.1f}h<br>Confidence: %{y:.2f}<br>Polls: %{z}<br>Raw Time: %{customdata[0]:.1f}h<br>Genre: %{customdata[1]}<extra></extra>'
            ))
    
    # Annotate clusters
    gems = sample[sample['cluster'] == 'Hidden Gems']
    if len(gems) > 0:
        fig.add_trace(go.Scatter3d(
            x=[gems['adjusted_time_cost'].mean()],
            y=[gems['confidence_score'].mean()],
            z=[gems['main_story_polled'].mean()],
            mode='text',
            text=['HIDDEN GEMS<br>(Trustworthy + Short)'],
            textfont=dict(size=11, color=PALETTE['earned'], family="Inter"),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    overhyped = sample[sample['cluster'] == 'Overhyped']
    if len(overhyped) > 0:
        fig.add_trace(go.Scatter3d(
            x=[overhyped['adjusted_time_cost'].mean()],
            y=[overhyped['confidence_score'].mean()],
            z=[overhyped['main_story_polled'].mean()],
            mode='text',
            text=['OVERHYPED<br>(Long + Uncertain)'],
            textfont=dict(size=11, color=PALETTE['accent'], family="Inter"),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    camera = dict(eye=dict(x=1.6, y=1.3, z=1.4))
    
    fig.update_layout(
        title=dict(
            text="<b>Hidden Gems Cluster Explorer</b><br><sub>Z-axis shows poll volume — discover trustworthy short games</sub>",
            font=dict(size=24, color=PALETTE['text'], family="Inter")
        ),
        scene=dict(
            xaxis=dict(title='<b>Adjusted Hours</b>', backgroundcolor=PALETTE['bg'], gridcolor='rgba(0,0,0,0.1)'),
            yaxis=dict(title='<b>Confidence</b>', backgroundcolor=PALETTE['bg'], gridcolor='rgba(0,0,0,0.1)'),
            zaxis=dict(title='<b>Poll Count</b>', backgroundcolor=PALETTE['bg'], gridcolor='rgba(0,0,0,0.1)', type='log'),
            camera=camera
        ),
        height=800,
        font=dict(size=12, family="Inter"),
        showlegend=True,
        legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.9)", bordercolor=PALETTE['text'], borderwidth=1)
    )
    
    return fig
