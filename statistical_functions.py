import logging
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.tsa.stattools import coint, adfuller
import statsmodels.api as sm


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ForexStats:
    def __init__(self, arr1: np.ndarray, arr2: np.ndarray) -> None:
        """
        Initialize ForexStats with two time-series data.

        :param arr1: A 1-D numpy array representing the first time-series data (e.g. close prices of a forex symbol).
        :param arr2: A 1-D numpy array representing the second time-series data (e.g. close prices of another forex symbol).
        """
        self.arr1 = arr1
        self.arr2 = arr2
        self.model = sm.OLS(self.arr1, self.arr2).fit()
        self.hedge_ratio = self.calculate_hedge_ratio()
        self.spread = self.calculate_spread()

    def calculate_correlation(self) -> float:
        """
        Calculate the correlation between the two input time-series.

        :return: A float representing the correlation coefficient ranging from -1 to 1. 
        """
        try:
            correlation = np.corrcoef(self.arr1, self.arr2)[0, 1]
            logger.info(f"Calculated correlation: {correlation}")
            return correlation
        except Exception as e:
            logger.error(f"Error calculating correlation: {str(e)}")
            return 0.0

    def check_cointegration(self, threshold: float = 0.05) -> bool:
        """
        Check if the two time-series are cointegrated using the Engle-Granger two-step method.

        :param threshold: A float representing the p-value cut-off for deciding cointegration. Default is 0.05.
        :return: A boolean value. True if p-value is less than threshold (indicating cointegration), False otherwise.
        """
        try:
            _, pvalue, _ = coint(self.arr1, self.arr2)
            cointegrated = pvalue < threshold
            logger.info(f"Cointegration test p-value: {pvalue}, cointegrated: {cointegrated}")
            return cointegrated
        except Exception as e:
            logger.error(f"Error checking cointegration: {str(e)}")
            return False

    def check_stationarity(self, threshold: float = 0.05) -> bool:
        """
        Check if the spread of the two time-series is stationary using the Augmented Dickey-Fuller test.

        :param threshold: A float representing the p-value cut-off for deciding stationarity. Default is 0.05.
        :return: A boolean value. True if p-value is less than threshold (indicating stationarity), False otherwise.
        """
        try:
            adf_result = adfuller(self.spread)
            stationary = adf_result[1] < threshold
            logger.info(f"ADF test p-value: {adf_result[1]}, stationary: {stationary}")
            return stationary
        except Exception as e:
            logger.error(f"Error checking stationarity: {str(e)}")
            return False

    def calculate_hedge_ratio(self) -> float:
        """
        Calculate the hedge ratio between the two time-series. The hedge ratio is the slope coefficient from 
        regressing arr1 on arr2, which can be used to form a stationary pair for pair trading.

        :return: A float representing the hedge ratio.
        """
        try:
            hedge_ratio = self.model.params[0]
            logger.info(f"Calculated hedge ratio: {hedge_ratio}")
            return hedge_ratio
        except Exception as e:
            logger.error(f"Error calculating hedge ratio: {str(e)}")
            return 0.0

    def calculate_spread(self) -> np.ndarray:
        """
        Calculate the spread between the two time-series by regressing arr1 on arr2 and then subtracting 
        arr2 times the regression coefficient from arr1.

        :return: A 1-D numpy array representing the spread of the two time-series.
        """
        try:
            spread = self.arr1 - self.hedge_ratio * self.arr2
            logger.info("Calculated spread")
            return spread
        except Exception as e:
            logger.error(f"Error calculating spread: {str(e)}")
            return np.array([])

    def calculate_half_life(self) -> float:
        """
        Calculate the half-life of the spread. Half-life is the time it takes for the spread to revert to 
        half of its initial value, assuming a mean-reverting process.

        :return: A float representing the half-life of the spread.
        """
        try:
            if np.any(pd.isnull(self.spread)):
                logging.warning(
                    'NaN values found. Replacing with backward fill method.')
                spread_lag = pd.Series(self.spread).shift(
                    1).fillna(method='bfill').values
            else:
                spread_lag = np.roll(self.spread, 1)  # equivalent to shift
            spread_ret = self.spread - spread_lag
            spread_lag2 = sm.add_constant(spread_lag)
            model = sm.OLS(spread_ret, spread_lag2)
            res = model.fit()
            half_life = -np.log(2) / res.params[1]
            logger.info(f"Calculated half-life: {half_life}")
            return half_life
        except Exception as e:
            logger.error(f"Error calculating half-life: {str(e)}")
            return 0.0

    def calculate_zscore(self) -> np.ndarray:
        """
        Calculate the z-score of the spread. The z-score indicates how many standard deviations an element is 
        from the mean.

        :return: A 1-D numpy array representing the z-score of the spread.
        """
        try:
            zscore = stats.zscore(self.spread)
            logger.info("Calculated z-score")
            return zscore
        except Exception as e:
            logger.error(f"Error calculating z-score: {str(e)}")
            return np.array([])

    def calculate_zscore_rolling(self, window: int = 21) -> np.ndarray:
        """
        Calculate the rolling z-score of the spread. The z-score indicates how many standard deviations an element is 
        from the mean.

        :param window: An integer representing the window size for the rolling z-score calculation. Default is 21.
        :return: A 1-D numpy array representing the rolling z-score of the spread.
        """
        try:
            spread_series = pd.Series(self.spread)
            mean = spread_series.rolling(window=window).mean()
            std = spread_series.rolling(window=window).std()
            zscore_rolling = (spread_series - mean) / std
            logger.info("Calculated rolling z-score")
            return zscore_rolling.values  # Convert the result back to np.ndarray
        except Exception as e:
            logger.error(f"Error calculating rolling z-score: {str(e)}")
            return np.array([])
