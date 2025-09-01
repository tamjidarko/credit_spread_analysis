# Credit Spread Analysis

A comprehensive analysis of corporate credit spreads using real-world Treasury yield data and market stress indicators, demonstrating the relationship between credit risk premiums and systematic market risk.

## Project Overview

This project analyzes credit spread dynamics in the U.S. corporate bond market, focusing on:
- **Investment Grade (IG)** corporate bonds (LQD ETF proxy)
- **High Yield (HY)** corporate bonds (HYG ETF proxy)
- **Market stress indicators** (VIX)
- **Risk-free benchmarks** (10-Year Treasury yields from FRED)

### Key Research Question
*How do credit spreads respond to systematic market risk, and what does this relationship reveal about credit market dynamics?*

## Key Findings

### Market Stress Correlations
- **Investment Grade vs VIX**: 0.512*** (statistically significant)
- **High Yield vs VIX**: 0.632*** (statistically significant)

### Risk Premium During Stress Periods (VIX > 30)
| Credit Quality | Normal Periods | Stress Periods | Risk Premium |
|---------------|----------------|----------------|--------------|
| Investment Grade | 78 bps | 315 bps | +237 bps |
| High Yield | 236 bps | 620 bps | +384 bps |

### Economic Insights
1. **Flight-to-Quality**: Credit spreads widen significantly during market stress
2. **Risk Hierarchy**: High yield spreads are more sensitive to systematic risk
3. **Systematic Risk Component**: Strong positive correlation with VIX confirms credit spreads contain systematic risk premiums
4. **Investment Timing**: Spread widening during stress creates potential buying opportunities

## Technical Implementation

### Data Sources
- **Corporate Bond ETFs**: Yahoo Finance (LQD, HYG)
- **Treasury Yields**: Federal Reserve Economic Data (FRED API)
- **Volatility Index**: CBOE VIX via Yahoo Finance
- **Analysis Period**: 2020-2025 (1,393 observations)

### Methodology
1. **Credit Spread Calculation**: Corporate Yield - Treasury Yield
2. **Statistical Analysis**: Pearson correlation coefficients
3. **Regime Analysis**: Market stress periods identification (VIX > 30)
4. **Visualization**: Time series and scatter plot analysis

### Dependencies
```bash
pip install pandas numpy matplotlib scipy yfinance fredapi
```

## Results & Visualizations

### Four-Panel Analysis
1. **Credit Spreads Over Time**: Historical spread evolution
2. **Treasury Yield Environment**: Risk-free rate context
3. **IG Spread vs VIX**: Systematic risk relationship
4. **HY Spread vs VIX**: Enhanced sensitivity demonstration

### Key Statistical Results
```
DATA PERIOD: 2020-01-31 to 2025-08-28
OBSERVATIONS: 1,393 trading days

CURRENT LEVELS:
• Treasury Yield: 4.22%
• IG Spread: -128 bps (avg: 103 bps)
• HY Spread: 49 bps (avg: 276 bps)

STRESS PERIODS: 146 days (10.5% of sample)
```

## Usage

### Setup
1. Obtain a free FRED API key from https://fred.stlouisfed.org/docs/api/api_key.html
2. Replace `FRED_API_KEY` in the script with your actual key

### Running the Analysis
```python
# Clone repository
git clone [your-repo-url]
cd credit-spread-analysis

# Install dependencies
pip install -r requirements.txt

# Run analysis
python credit_spread_analysis.py
```

### Expected Output
- Market data fetch confirmation
- Statistical correlation analysis
- Professional visualizations
- Comprehensive summary report

## Economic Theory Background

### Credit Risk Premium Theory
Credit spreads represent the additional yield investors demand for bearing:
- **Default Risk**: Probability of issuer bankruptcy
- **Recovery Risk**: Expected loss given default
- **Liquidity Risk**: Difficulty in trading corporate bonds
- **Systematic Risk**: Economy-wide factors affecting creditworthiness

### Mathematical Foundation
```
Credit Spread = Corporate Bond Yield - Risk-Free Treasury Yield
```

Where the spread compensates for:
```
Spread = Default Probability × (1 - Recovery Rate) + Liquidity Premium + Systematic Risk Premium
```

## Advanced Applications

### For Investment Management
- **Tactical Asset Allocation**: Identify attractive entry points during spread widening
- **Risk Management**: Monitor systematic risk exposure in credit portfolios
- **Relative Value**: Compare current spreads to historical percentiles

### For Economic Research
- **Business Cycle Analysis**: Credit spreads as leading economic indicators
- **Monetary Policy Impact**: Relationship between rates and credit risk premiums
- **Market Microstructure**: Liquidity effects during stress periods

## Sample Output

### Correlation Analysis
```
Investment Grade vs VIX: 0.512 ***
High Yield vs VIX: 0.632 ***
```

### Stress Period Analysis
```
STRESS PERIODS (VIX > 30): 146 days (10.5%)
IG: 78 bps (normal) vs 315 bps (stress)
HY: 236 bps (normal) vs 620 bps (stress)
```

## Educational Value

### Demonstrates Understanding Of:
- **Fixed Income Markets**: Credit risk pricing mechanisms
- **Quantitative Finance**: Statistical analysis of financial time series
- **Risk Management**: Systematic vs idiosyncratic risk components
- **Data Science**: API integration, data processing, and visualization
- **Economic Theory**: Flight-to-quality, risk premiums, market efficiency

### Professional Skills Showcased:
- Real-world data integration (FRED API)
- Statistical analysis and interpretation
- Professional-quality visualization
- Economic intuition and market understanding
- Clean, documented code structure

## Future Enhancements

### Potential Extensions:
1. **Sector Analysis**: Break down spreads by industry sectors
2. **Term Structure**: Analyze spreads across different maturities
3. **International Comparison**: Compare US vs European credit markets
4. **Predictive Modeling**: Develop spread forecasting models
5. **Options-Adjusted Spreads**: Account for embedded options in corporate bonds

### Advanced Features:
- Real-time data streaming
- Interactive dashboard development
- Machine learning applications
- Portfolio optimization integration

---
