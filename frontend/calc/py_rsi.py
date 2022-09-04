import pandas as pd
import numpy as np
from .py_Indicatormixin import IndicatorMixin

# https://github.com/bukosabino/ta/blob/master/ta/momentum.py


class RSIIndicator(IndicatorMixin):
    """Relative Strength Index (RSI)
    Compares the magnitude of recent gains and losses over a specified time
    period to measure speed and change of price movements of a security. It is
    primarily used to attempt to identify overbought or oversold conditions in
    the trading of an asset.
    https://www.investopedia.com/terms/r/rsi.asp
    Args:
        close(pandas.Series): dataset 'Close' column.
        window(int): n period.
        fillna(bool): if True, fill nan values.
    """

    def __init__(self, close: pd.Series, window: int = 14, fillna: bool = False):
        self._close = close
        self._window = window
        self._fillna = fillna
        self._run()

    def _run(self):
        diff = self._close.diff(1)
        up_direction = diff.where(diff > 0, 0.0)
        down_direction = -diff.where(diff < 0, 0.0)
        min_periods = 0 if self._fillna else self._window
        emaup = up_direction.ewm(
            alpha=1 / self._window, min_periods=min_periods, adjust=False
        ).mean()
        emadn = down_direction.ewm(
            alpha=1 / self._window, min_periods=min_periods, adjust=False
        ).mean()
        relative_strength = emaup / emadn
        self._rsi = pd.Series(
            np.where(emadn == 0, 100, 100 - (100 / (1 + relative_strength))),
            index=self._close.index,
        )

    def rsi(self) -> pd.Series:
        """Relative Strength Index (RSI)
        Returns:
            pandas.Series: New feature generated.
        """
        rsi_series = self._check_fillna(self._rsi, value=50)
        return pd.Series(rsi_series, name="rsi")
