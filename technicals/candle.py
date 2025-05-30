

def detect_strong_bullish(df, lookback=20, range_multiplier=1.5, wick_ratio_thresh=0.7, close_proximity_thresh=0.2):
    """
    Detects strong bullish candles using:
    1. Full candle range > avg of previous candle ranges * multiplier
    2. Wick-to-body ratio indicates a decisive candle
    3. Close is near the high (momentum)

    Adds a 'strong_bullish' column to df with boolean values.
    """

    # Calculate candle components
    df['body'] = df['mid_c'] - df['mid_o']
    df['total_range'] = df['mid_h'] - df['mid_l']
    df['upper_wick'] = df['mid_h'] - df[['mid_c', 'mid_o']].max(axis=1)
    df['lower_wick'] = df[['mid_c', 'mid_o']].min(axis=1) - df['mid_l']

    # Avoid divide-by-zero
    df['wick_ratio'] = df['body'] / df['total_range'].replace(0, 1e-9)
    df['avg_range'] = df['total_range'].rolling(window=lookback).mean()
    df['range_ok'] = df['total_range'] > df['avg_range'] * range_multiplier
    df['wick_ok'] = df['wick_ratio'] > wick_ratio_thresh
    df['close_near_high'] = (df['mid_h'] - df['mid_c']) / df['total_range'].replace(0, 1e-9) < close_proximity_thresh

    # All conditions must be met
    df['strong_bullish'] = df['range_ok'] & df['wick_ok'] & df['close_near_high']

    # Set 'setup_stage' to 'confirmation' if previous candle was 'reentry' and current is strong bullish
    # for i in range(1, len(df)):
    #     if df.at[df.index[i], 'strong_bullish'] and df.at[df.index[i - 1], 'setup_stage'] == 'reentry':
    #         df.at[df.index[i], 'setup_stage'] = 'confirmation'

def mark_confirmations(df, window=10):
    """
    Set 'setup_stage' to 'confirmation' for strong bullish candles
    occurring within `window` candles after a 'reentry'.
    """
    last_reentry_idx = None

    for i in range(len(df)):
        if df.at[df.index[i], 'setup_stage'] == 'reentry':
            last_reentry_idx = i

        if (
            last_reentry_idx is not None and
            i - last_reentry_idx <= window and
            df.at[df.index[i], 'strong_bullish']
        ):
            df.at[df.index[i], 'setup_stage'] = 'confirmation'
            last_reentry_idx = None
