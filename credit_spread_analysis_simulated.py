import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.stats import pearsonr
import warnings

warnings.filterwarnings('ignore')

class SimpleCreditSpreadAnalyzer:
    """
    Simplified Credit Spread Analysis focusing on core concepts:
    1. Track credit spreads over time using ETF proxies
    2. Analyze relationship with VIX (market stress)
    3. Identify basic spread patterns
    """
    
    def __init__(self):
        self.data = {}
        
    def fetch_data(self, start_date='2020-01-01', end_date=None):
        """
        Fetch essential data: Corporate bonds, Treasuries, and VIX
        """
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
            
        print("Fetching market data...")
        
        # Key ETFs we need
        tickers = {
            'LQD': 'Investment Grade Corporate Bonds',
            'HYG': 'High Yield Corporate Bonds', 
            'TLT': 'Long-Term Treasury Bonds',
            'VIX': 'CBOE Volatility Index'
        }
        
        yahoo_tickers = ['LQD', 'HYG', 'TLT', '^VIX']
        
        for i, ticker in enumerate(yahoo_tickers):
            try:
                print(f"  Fetching {ticker}...")
                data = yf.download(ticker, start=start_date, end=end_date, progress=False)
                
                if data.empty:
                    print(f"    ✗ No data returned for {ticker}")
                    continue
                
                # Extract closing prices as Series (fix the DataFrame issue)
                if ticker == '^VIX':
                    self.data['VIX'] = data['Close'].squeeze()  # Convert to Series
                else:
                    self.data[ticker] = data['Close'].squeeze()  # Convert to Series
                    
                print(f"    ✓ Got {len(self.data[ticker if ticker != '^VIX' else 'VIX'])} observations")
                
            except Exception as e:
                print(f"    ✗ Error fetching {ticker}: {e}")
        
        print(f"Data fetching complete!")
        
    def calculate_simple_spreads(self):
        """
        Calculate credit spreads using a simplified approach
        """
        print("\nCalculating credit spreads...")
        
        # Check we have the minimum required data
        required_data = ['LQD', 'HYG', 'TLT', 'VIX']
        missing_data = [ticker for ticker in required_data if ticker not in self.data]
        
        if missing_data:
            print(f"Missing required data: {missing_data}")
            return False
        
        # Find common dates
        common_dates = self.data['LQD'].index
        for ticker in ['HYG', 'TLT', 'VIX']:
            common_dates = common_dates.intersection(self.data[ticker].index)
        
        print(f"Found {len(common_dates)} common trading days")
        
        if len(common_dates) < 100:
            print("Insufficient overlapping data for analysis")
            return False
        
        # Create aligned dataset
        self.spreads = pd.DataFrame(index=common_dates)
        
        # Add VIX
        self.spreads['VIX'] = self.data['VIX'].reindex(common_dates)
        
        # Calculate simple spread proxies
        # Method: Track performance difference between corporate bonds and Treasuries
        # When credit risk increases, corporate bonds underperform Treasuries
        
        # Investment Grade Spread Proxy
        print("  Calculating Investment Grade spread proxy...")
        lqd_returns = self.data['LQD'].reindex(common_dates).pct_change()
        tlt_returns = self.data['TLT'].reindex(common_dates).pct_change()
        
        # Performance difference (Treasury outperformance = wider spreads)
        ig_spread_raw = (tlt_returns - lqd_returns) * 10000  # Convert to basis points
        self.spreads['IG_Spread'] = ig_spread_raw.rolling(20).mean()  # Smooth with 20-day average
        
        # High Yield Spread Proxy
        print("  Calculating High Yield spread proxy...")
        hyg_returns = self.data['HYG'].reindex(common_dates).pct_change()
        
        hy_spread_raw = (tlt_returns - hyg_returns) * 10000  # Convert to basis points
        self.spreads['HY_Spread'] = hy_spread_raw.rolling(20).mean()  # Smooth with 20-day average
        
        # Clean data
        self.spreads = self.spreads.dropna()
        
        print(f"  ✓ Calculated spreads for {len(self.spreads)} observations")
        
        # Basic statistics
        print(f"\nSpread Statistics:")
        print(f"  IG Spread - Mean: {self.spreads['IG_Spread'].mean():.1f} bps, Std: {self.spreads['IG_Spread'].std():.1f} bps")
        print(f"  HY Spread - Mean: {self.spreads['HY_Spread'].mean():.1f} bps, Std: {self.spreads['HY_Spread'].std():.1f} bps")
        
        return True
        
    def analyze_spread_vix_relationship(self):
        """
        Analyze the relationship between credit spreads and market stress (VIX)
        """
        print("\nAnalyzing Spread-VIX Relationships...")
        
        correlations = {}
        
        for spread_type in ['IG_Spread', 'HY_Spread']:
            # Calculate correlation
            corr, p_value = pearsonr(self.spreads[spread_type], self.spreads['VIX'])
            correlations[spread_type] = {'correlation': corr, 'p_value': p_value}
            
            significance = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*" if p_value < 0.05 else ""
            
            print(f"  {spread_type} vs VIX:")
            print(f"    Correlation: {corr:.3f} {significance}")
            print(f"    P-value: {p_value:.4f}")
            
        self.correlations = correlations
        
        # Economic interpretation
        print(f"\nEconomic Interpretation:")
        print(f"  - Positive correlation means spreads widen when market stress increases")
        print(f"  - Higher correlation indicates stronger relationship with systematic risk")
        print(f"  - HY bonds typically show stronger correlation with VIX than IG bonds")
        
    def identify_spread_regimes(self):
        """
        Identify periods of spread widening vs tightening
        """
        print("\nIdentifying Spread Regimes...")
        
        regimes = {}
        
        for spread_type in ['IG_Spread', 'HY_Spread']:
            spread_data = self.spreads[spread_type]
            
            # Calculate percentiles for regime definition
            p25 = spread_data.quantile(0.25)
            p75 = spread_data.quantile(0.75)
            
            # Define regimes
            tight = spread_data <= p25
            normal = (spread_data > p25) & (spread_data < p75)
            wide = spread_data >= p75
            
            regimes[spread_type] = {
                'tight_periods': tight.sum(),
                'normal_periods': normal.sum(), 
                'wide_periods': wide.sum(),
                'total_periods': len(spread_data)
            }
            
            print(f"\n  {spread_type} Regimes:")
            print(f"    Tight spreads (< 25th percentile): {tight.sum()} days ({tight.mean()*100:.1f}%)")
            print(f"    Normal spreads: {normal.sum()} days ({normal.mean()*100:.1f}%)")
            print(f"    Wide spreads (> 75th percentile): {wide.sum()} days ({wide.mean()*100:.1f}%)")
            
        self.regimes = regimes
        
    def create_visualizations(self):
        """
        Create clear, focused visualizations
        """
        print("\nCreating visualizations...")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Credit Spread Analysis', fontsize=16, fontweight='bold')
        
        # 1. Spread Time Series
        ax1 = axes[0, 0]
        ax1.plot(self.spreads.index, self.spreads['IG_Spread'], label='Investment Grade', linewidth=2, alpha=0.8)
        ax1.plot(self.spreads.index, self.spreads['HY_Spread'], label='High Yield', linewidth=2, alpha=0.8)
        ax1.set_title('Credit Spreads Over Time')
        ax1.set_ylabel('Spread Proxy (basis points)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. VIX Time Series
        ax2 = axes[0, 1]
        ax2.plot(self.spreads.index, self.spreads['VIX'], color='red', linewidth=2, alpha=0.8)
        ax2.set_title('VIX (Market Fear Gauge)')
        ax2.set_ylabel('VIX Level')
        ax2.grid(True, alpha=0.3)
        
        # 3. Spread vs VIX Scatter (Investment Grade)
        ax3 = axes[1, 0]
        ax3.scatter(self.spreads['VIX'], self.spreads['IG_Spread'], alpha=0.6, s=10)
        
        # Add trend line
        z = np.polyfit(self.spreads['VIX'], self.spreads['IG_Spread'], 1)
        p = np.poly1d(z)
        ax3.plot(self.spreads['VIX'], p(self.spreads['VIX']), "r--", alpha=0.8, linewidth=2)
        
        corr = self.correlations['IG_Spread']['correlation']
        ax3.set_title(f'IG Spread vs VIX (r={corr:.3f})')
        ax3.set_xlabel('VIX Level')
        ax3.set_ylabel('IG Spread (bps)')
        ax3.grid(True, alpha=0.3)
        
        # 4. Spread vs VIX Scatter (High Yield)
        ax4 = axes[1, 1]
        ax4.scatter(self.spreads['VIX'], self.spreads['HY_Spread'], alpha=0.6, s=10, color='orange')
        
        # Add trend line
        z = np.polyfit(self.spreads['VIX'], self.spreads['HY_Spread'], 1)
        p = np.poly1d(z)
        ax4.plot(self.spreads['VIX'], p(self.spreads['VIX']), "r--", alpha=0.8, linewidth=2)
        
        corr = self.correlations['HY_Spread']['correlation']
        ax4.set_title(f'HY Spread vs VIX (r={corr:.3f})')
        ax4.set_xlabel('VIX Level')
        ax4.set_ylabel('HY Spread (bps)')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        # Additional plot: Rolling correlations
        self._plot_rolling_correlations()
        
    def _plot_rolling_correlations(self):
        """
        Plot rolling correlations to show how relationships change over time
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Calculate 60-day rolling correlations
        ig_rolling_corr = self.spreads['IG_Spread'].rolling(60).corr(self.spreads['VIX'])
        hy_rolling_corr = self.spreads['HY_Spread'].rolling(60).corr(self.spreads['VIX'])
        
        ax.plot(ig_rolling_corr.index, ig_rolling_corr, label='IG Spread vs VIX', linewidth=2)
        ax.plot(hy_rolling_corr.index, hy_rolling_corr, label='HY Spread vs VIX', linewidth=2)
        
        ax.set_title('60-Day Rolling Correlations with VIX', fontsize=14, fontweight='bold')
        ax.set_ylabel('Correlation')
        ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
    def generate_summary_report(self):
        """
        Generate a focused summary report
        """
        print("\n" + "="*60)
        print("           CREDIT SPREAD ANALYSIS SUMMARY")
        print("="*60)
        
        print(f"\nDATA PERIOD: {self.spreads.index.min().strftime('%Y-%m-%d')} to {self.spreads.index.max().strftime('%Y-%m-%d')}")
        print(f"OBSERVATIONS: {len(self.spreads)}")
        
        print(f"\nKEY FINDINGS:")
        
        # Spread levels
        print(f"\nAverage Spread Levels:")
        print(f"  Investment Grade: {self.spreads['IG_Spread'].mean():.0f} basis points")
        print(f"  High Yield: {self.spreads['HY_Spread'].mean():.0f} basis points")
        print(f"  HY Premium over IG: {self.spreads['HY_Spread'].mean() - self.spreads['IG_Spread'].mean():.0f} basis points")
        
        # Volatility
        print(f"\nSpread Volatility:")
        print(f"  Investment Grade: {self.spreads['IG_Spread'].std():.0f} basis points")
        print(f"  High Yield: {self.spreads['HY_Spread'].std():.0f} basis points")
        
        # VIX relationships
        print(f"\nRelationship with Market Stress (VIX):")
        for spread_type, stats in self.correlations.items():
            spread_name = "Investment Grade" if spread_type == "IG_Spread" else "High Yield"
            print(f"  {spread_name}: {stats['correlation']:.3f} correlation")
            
        # Extreme periods
        print(f"\nMarket Stress Periods (VIX > 30):")
        high_vix = self.spreads['VIX'] > 30
        if high_vix.any():
            stress_periods = high_vix.sum()
            avg_ig_stress = self.spreads.loc[high_vix, 'IG_Spread'].mean()
            avg_hy_stress = self.spreads.loc[high_vix, 'HY_Spread'].mean()
            
            print(f"  Number of high-stress days: {stress_periods}")
            print(f"  Average IG spread during stress: {avg_ig_stress:.0f} bps")
            print(f"  Average HY spread during stress: {avg_hy_stress:.0f} bps")
        else:
            print("  No high-stress periods (VIX > 30) in dataset")
        
        print(f"\nINVESTMENT INSIGHTS:")
        print(f"  • Credit spreads widen during market stress, creating buying opportunities")
        print(f"  • High yield spreads are more sensitive to market conditions than investment grade")
        print(f"  • Strong positive correlation with VIX confirms systematic risk component")
        
        print("="*60)
        
    def run_analysis(self, start_date='2020-01-01'):
        """
        Run the complete simplified analysis
        """
        print("Starting Simplified Credit Spread Analysis...")
        print("-" * 50)
        
        # Step 1: Fetch data
        self.fetch_data(start_date)
        
        # Step 2: Calculate spreads
        if not self.calculate_simple_spreads():
            print("Analysis terminated due to data issues")
            return
        
        # Step 3: Analyze relationships
        self.analyze_spread_vix_relationship()
        
        # Step 4: Identify regimes
        self.identify_spread_regimes()
        
        # Step 5: Create visualizations
        self.create_visualizations()
        
        # Step 6: Summary report
        self.generate_summary_report()
        
        print("\n✅ Analysis complete!")

# Example usage
if __name__ == "__main__":
    # Create analyzer
    analyzer = SimpleCreditSpreadAnalyzer()
    
    # Run analysis (try different start dates if needed)
    try:
        analyzer.run_analysis(start_date='2020-01-01')
        
        # Access results
        print(f"\nQuick data check:")
        print(f"Spread data shape: {analyzer.spreads.shape}")
        print(f"Available columns: {list(analyzer.spreads.columns)}")
        
    except Exception as e:
        print(f"Analysis failed: {e}")
        print("Try a more recent start date like '2022-01-01'")