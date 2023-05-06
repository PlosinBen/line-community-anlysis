import sys
import pandas as pd
import yfinance as yf
import numpy as np
from scipy.optimize import minimize


class Asset:
    def __init__(self, symbol):
        self.symbol: str = symbol

    def get_close(self, start_date: str, end_date: str, interval: str = '1d'):
        df = yf.download(
            self.symbol,
            start=start_date,
            end=end_date,
            interval=interval
        )

        return df['Close']


# 定義風險平衡目標函數
def risk_parity_objective(weights, cov_matrix):
    risk_contrib = weights * (cov_matrix @ weights)
    risk_contrib /= risk_contrib.sum()
    return np.sum((risk_contrib - risk_contrib.mean()) ** 2)


def calculate(start_date: str, end_date: str, assets: list[Asset], period: int):
    df = pd.DataFrame()

    for asset in assets:
        df[asset.symbol] = asset.get_close(start_date, end_date)

    df = df.pct_change().dropna()

    print(df, file=sys.stdout)

    # 計算資產的波動性
    volatility = df.rolling(window=int(period)).std() * np.sqrt(252)

    print(volatility, file=sys.stdout)

    # 計算資產間的相關性
    correlation_matrix = df.rolling(window=int(period)).corr()

    # 設定優化約束
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = [(0, 1) for _ in range(df.shape[1])]

    # 計算風險平衡權重
    risk_parity_weights = pd.DataFrame(index=df.index, columns=df.columns)

    asset_count = len(assets)

    for t in range(len(df)):
        if t >= 120:
            np.outer(volatility.iloc[t].values, volatility.iloc[t].values)
            a = correlation_matrix.iloc[t * asset_count: (t + 1) * asset_count]

            cov_matrix = a * np.outer(volatility.iloc[t].values, volatility.iloc[t].values)

            initial_weights = np.ones(df.shape[1]) / df.shape[1]
            result = minimize(
                risk_parity_objective,
                initial_weights,
                args=(cov_matrix),
                bounds=bounds,
                constraints=constraints
            )
            risk_parity_weights.iloc[t] = result.x

    return {asset: risk_parity_weights[asset][-1] for asset in risk_parity_weights}
