import pandas as pd
import numpy as np
# https://github.com/bukosabino/ta/blob/master/ta/utils.py


class IndicatorMixin:
    """Util mixin indicator class"""

    _fillna = False

    def _check_fillna(self, series: pd.Series, value: int = 0) -> pd.Series:
        """Check if fillna flag is True.
        Args:
            series(pandas.Series): dataset 'Close' column.
            value(int): value to fill gaps; if -1 fill values using 'backfill' mode.
        Returns:
            pandas.Series: New feature generated.
        """
        if self._fillna:
            series_output = series.copy(deep=False)
            series_output = series_output.replace([np.inf, -np.inf], np.nan)
            if isinstance(value, int) and value == -1:
                series = series_output.fillna(method="ffill").fillna(value=-1)
            else:
                series = series_output.fillna(method="ffill").fillna(value)
        return series

    @staticmethod
    def _true_range(
        high: pd.Series, low: pd.Series, prev_close: pd.Series
    ) -> pd.Series:
        tr1 = high - low
        tr2 = (high - prev_close).abs()
        tr3 = (low - prev_close).abs()
        true_range = pd.DataFrame(
            data={"tr1": tr1, "tr2": tr2, "tr3": tr3}).max(axis=1)
        return true_range
