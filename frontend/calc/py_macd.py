import pandas as pd
import numpy as np
from .py_Indicatormixin import IndicatorMixin

# https://github.com/bukosabino/ta/blob/master/ta/trend.py    
class MACD(IndicatorMixin):
    """Moving Average Convergence Divergence (MACD)
    Is a trend-following momentum indicator that shows the relationship between
    two moving averages of prices.
    https://school.stockcharts.com/doku.php?id=technical_indicators:moving_average_convergence_divergence_macd
    Args:
        close(pandas.Series): dataset 'Close' column.
        window_fast(int): n period short-term.
        window_slow(int): n period long-term.
        window_sign(int): n period to signal.
        fillna(bool): if True, fill nan values.
    """

    def __init__(
        self,
        close: pd.Series,
        window_slow: int = 26,
        window_fast: int = 12,
        window_sign: int = 9,
        fillna: bool = False,
    ):
        self._close = close
        self._window_slow = window_slow
        self._window_fast = window_fast
        self._window_sign = window_sign
        self._fillna = fillna
        self._run()

    def _ema(self,series, periods, fillna=False):
        min_periods = 0 if fillna else periods
        return series.ewm(span=periods, min_periods=min_periods, adjust=False).mean()


    def _run(self):
        self._emafast = self._ema(self._close, self._window_fast, self._fillna)
        self._emaslow = self._ema(self._close, self._window_slow, self._fillna)
        self._macd = self._emafast - self._emaslow
        self._macd_signal = self._ema(self._macd, self._window_sign, self._fillna)
        self._macd_diff = self._macd - self._macd_signal

    def macd(self) -> pd.Series:
        """MACD Line
        Returns:
            pandas.Series: New feature generated.
        """
        macd_series = self._check_fillna(self._macd, value=0)
        return pd.Series(
            macd_series, name=f"MACD_{self._window_fast}_{self._window_slow}"
        )

    def macd_signal(self) -> pd.Series:
        """Signal Line
        Returns:
            pandas.Series: New feature generated.
        """

        macd_signal_series = self._check_fillna(self._macd_signal, value=0)
        return pd.Series(
            macd_signal_series,
            name=f"MACD_sign_{self._window_fast}_{self._window_slow}",
        )

    def macd_diff(self) -> pd.Series:
        """MACD Histogram
        Returns:
            pandas.Series: New feature generated.
        """
        macd_diff_series = self._check_fillna(self._macd_diff, value=0)
        return pd.Series(
            macd_diff_series, name=f"MACD_diff_{self._window_fast}_{self._window_slow}"
        )
    