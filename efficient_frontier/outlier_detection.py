import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.covariance import EllipticEnvelope
from sklearn.cluster import DBSCAN
from matplotlib import cm
from sklearn.preprocessing import MinMaxScaler

data = pd.read_csv("result_frame_test.csv", index_col = 0)

min_vol = pd.read_csv("min_vol_port.csv", index_col = 0)
max_sharpe = pd.read_csv("max_sharpe_port.csv", index_col = 0)

data_subset = data.sample(n = int(len(data) * 0.01))

data_subset = data_subset.append(pd.Series(name = "max_sharpe"))
data_subset = data_subset.append(pd.Series(name = "min_vol"))
    
data_subset.at["max_sharpe", "ret"] = float(max_sharpe.loc[['ret']].values)
data_subset.at["max_sharpe", "stdev"] = float(max_sharpe.loc[['stdev']].values)
data_subset.at["max_sharpe", "sharpe"] = float(max_sharpe.loc[['sharpe']].values)

data_subset.at["min_vol", "ret"] = float(min_vol.loc[['ret']].values)
data_subset.at["min_vol", "stdev"] = float(min_vol.loc[['stdev']].values)
data_subset.at["min_vol", "sharpe"] = float(min_vol.loc[['sharpe']].values)

scan_data = data_subset[['ret', 'stdev']].values

plt.scatter(data_subset['stdev'], data_subset['ret'])
plt.xlabel("standard deviation")
plt.ylabel("returns")

'''
#plt.title(len(data_subset), "samples")
plt.xlabel("expected standard deviation")
plt.ylabel("expected return")
'''