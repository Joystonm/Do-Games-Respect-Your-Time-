"""
Data Engine for Time Respect Analysis
Research-grade confidence modeling and uncertainty quantification
"""
import pandas as pd
import numpy as np
from typing import Tuple, Dict, List
from scipy import stats

class TimeRespectAnalyzer:
    def __init__(self, filepath: str):
        self.df_raw = pd.read_csv(filepath)
        self.df = None
        self.stats = {}
        
    def clean_data(self) -> pd.DataFrame:
        """Transparent, documented cleaning pipeline"""
        df = self.df_raw.copy()
        
        # Filter: games only
        df = df[df['type'] == 'game'].copy()
        
        # Filter: must have main story data
        df = df[df['main_story_polled'].notna() & (df['main_story_polled'] > 0)]
        df = df[df['main_story'].notna() & (df['main_story'] > 0)]
        
        # Remove extreme outliers (>99th percentile)
        time_99 = df['main_story'].quantile(0.99)
        df = df[df['main_story'] <= time_99].copy()
        
        self.df = df
        return df
    
    def compute_metrics(self):
        """Research-grade confidence-aware metrics"""
        df = self.df
        
        # Confidence score (log-scaled, bounded)
        df['confidence_score'] = np.log1p(df['main_story_polled'])
        
        # Raw time
        df['time_cost'] = df['main_story']
        
        # Adjusted time (uncertainty penalty)
        df['adjusted_time_cost'] = df['time_cost'] / df['confidence_score']
        
        # Reliability gradient (0-1 scale)
        max_conf = df['confidence_score'].max()
        df['reliability'] = df['confidence_score'] / max_conf
        
        # Misrepresentation risk (exponential decay)
        df['misrep_risk'] = np.exp(-df['main_story_polled'] / 50)
        
        # Perception gap (absolute difference)
        df['perception_gap'] = df['adjusted_time_cost'] - df['time_cost']
        
        # Statistical weight (for weighted statistics)
        df['stat_weight'] = df['main_story_polled'] / df['main_story_polled'].sum()
        
        # Confidence tiers
        df['confidence_tier'] = pd.cut(
            df['main_story_polled'], 
            bins=[0, 10, 50, 200, np.inf],
            labels=['Unreliable', 'Weak', 'Moderate', 'Strong']
        )
        
        # Zone classification (for Trust-Time Landscape)
        df['zone'] = 'Unknown'
        df.loc[(df['confidence_score'] > 3.5) & (df['time_cost'] < 15), 'zone'] = 'Earned Time'
        df.loc[(df['confidence_score'] < 2.5) & (df['time_cost'] > 30), 'zone'] = 'Uncertain Grind'
        df.loc[(df['confidence_score'] < 2.0) & (df['time_cost'] > 50), 'zone'] = 'False Epic'
        df.loc[(df['confidence_score'] > 3.0) & (df['time_cost'] > 40), 'zone'] = 'Verified Epic'
        
        # Genre normalization
        df['primary_genre'] = df['genres'].fillna('Unknown').str.split(',').str[0].str.strip()
        
        self.df = df
    
    def get_core_insight(self) -> Dict:
        """The unforgettable insight with robust statistics"""
        # Weighted medians (not raw medians)
        weights = self.df['main_story_polled']
        
        # Sort by time for weighted median calculation
        sorted_idx = self.df['time_cost'].argsort()
        sorted_weights = weights.iloc[sorted_idx].cumsum()
        median_idx = (sorted_weights >= sorted_weights.iloc[-1] / 2).idxmax()
        weighted_median_raw = self.df.loc[median_idx, 'time_cost']
        
        # Adjusted weighted median
        sorted_idx_adj = self.df['adjusted_time_cost'].argsort()
        sorted_weights_adj = weights.iloc[sorted_idx_adj].cumsum()
        median_idx_adj = (sorted_weights_adj >= sorted_weights_adj.iloc[-1] / 2).idxmax()
        weighted_median_adj = self.df.loc[median_idx_adj, 'adjusted_time_cost']
        
        diff = weighted_median_raw - weighted_median_adj
        pct = 100 * diff / weighted_median_raw
        
        # Unreliable fraction
        unreliable_pct = 100 * len(self.df[self.df['main_story_polled'] < 10]) / len(self.df)
        
        # Average misrepresentation risk
        avg_risk = self.df['misrep_risk'].mean()
        
        return {
            'weighted_median_raw': weighted_median_raw,
            'weighted_median_adj': weighted_median_adj,
            'difference': diff,
            'pct_noise': pct,
            'unreliable_pct': unreliable_pct,
            'avg_misrep_risk': avg_risk
        }
    
    def genre_analysis(self, min_games: int = 30) -> pd.DataFrame:
        """Genre-level weighted analysis with honesty scoring"""
        def weighted_median(values, weights):
            if len(values) == 0:
                return 0
            sorted_idx = np.argsort(values.values)
            sorted_vals = values.values[sorted_idx]
            sorted_weights = weights.values[sorted_idx]
            cumsum = np.cumsum(sorted_weights)
            cutoff = cumsum[-1] / 2.0
            median_idx = np.searchsorted(cumsum, cutoff)
            return sorted_vals[min(median_idx, len(sorted_vals) - 1)]
        
        genre_stats = self.df.groupby('primary_genre').apply(
            lambda g: pd.Series({
                'raw_median': weighted_median(g['time_cost'], g['main_story_polled']),
                'adjusted_median': weighted_median(g['adjusted_time_cost'], g['main_story_polled']),
                'count': len(g),
                'total_polls': g['main_story_polled'].sum(),
                'avg_reliability': g['reliability'].mean(),
                'avg_risk': g['misrep_risk'].mean()
            })
        ).reset_index()
        
        genre_stats = genre_stats[genre_stats['count'] >= min_games].copy()
        
        # Honesty score (inverse of perception gap)
        genre_stats['perception_gap'] = genre_stats['adjusted_median'] - genre_stats['raw_median']
        genre_stats['honesty_score'] = 1 / (1 + np.abs(genre_stats['perception_gap']))
        
        # Rank shifts
        genre_stats['raw_rank'] = genre_stats['raw_median'].rank()
        genre_stats['adjusted_rank'] = genre_stats['adjusted_median'].rank()
        genre_stats['rank_shift'] = (genre_stats['raw_rank'] - genre_stats['adjusted_rank']).astype(int)
        
        return genre_stats.sort_values('adjusted_median')
    
    def sensitivity_analysis(self, thresholds: List[int] = [1, 5, 10, 20, 50, 100]) -> pd.DataFrame:
        """Robust sensitivity analysis across confidence thresholds"""
        def weighted_median(values, weights):
            if len(values) == 0:
                return 0
            sorted_idx = np.argsort(values.values)
            sorted_vals = values.values[sorted_idx]
            sorted_weights = weights.values[sorted_idx]
            cumsum = np.cumsum(sorted_weights)
            cutoff = cumsum[-1] / 2.0
            median_idx = np.searchsorted(cumsum, cutoff)
            return sorted_vals[min(median_idx, len(sorted_vals) - 1)]
        
        results = []
        for thresh in thresholds:
            subset = self.df[self.df['main_story_polled'] >= thresh]
            if len(subset) > 100:
                weights = subset['main_story_polled']
                wm_raw = weighted_median(subset['time_cost'], weights)
                wm_adj = weighted_median(subset['adjusted_time_cost'], weights)
                
                results.append({
                    'threshold': thresh,
                    'n_games': len(subset),
                    'weighted_median_raw': wm_raw,
                    'weighted_median_adj': wm_adj,
                    'gap': wm_raw - wm_adj,
                    'pct_retained': 100 * len(subset) / len(self.df)
                })
        return pd.DataFrame(results)
    
    def get_zone_distribution(self) -> pd.DataFrame:
        """Distribution across Trust-Time zones"""
        return self.df['zone'].value_counts().reset_index()
    
    def get_illusion_games(self, top_n: int = 20) -> pd.DataFrame:
        """Games with largest perception gaps (False Epics)"""
        illusion = self.df[self.df['main_story_polled'] < 20].copy()
        illusion = illusion.nlargest(top_n, 'perception_gap')
        return illusion[['name', 'time_cost', 'adjusted_time_cost', 'main_story_polled', 
                        'perception_gap', 'primary_genre', 'zone']]
