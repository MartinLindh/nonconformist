#!/usr/bin/env python

"""
Example: inductive conformal regression using DecisionTreeRegressor
"""

# Authors: Henrik Linusson

import numpy as np
import pandas as pd

from sklearn.tree import DecisionTreeRegressor
from sklearn.datasets import load_boston

from nonconformist.icp import IcpRegressor
from nonconformist.nc import RegressorNc, abs_error, abs_error_inv

# -----------------------------------------------------------------------------
# Setup training, calibration and test indices
# -----------------------------------------------------------------------------
data = load_boston()

idx = np.random.permutation(data.target.size)
train = idx[:int(idx.size / 3)]
calibrate = idx[int(idx.size / 3):int(2 * idx.size / 3)]
test = idx[int(2 * idx.size / 3):]

# -----------------------------------------------------------------------------
# Train and calibrate
# -----------------------------------------------------------------------------
icp = IcpRegressor(RegressorNc(DecisionTreeRegressor(), abs_error, abs_error_inv))
icp.fit(data.data[train, :], data.target[train])
icp.calibrate(data.data[calibrate, :], data.target[calibrate])

# -----------------------------------------------------------------------------
# Predict
# -----------------------------------------------------------------------------
prediction = icp.predict(data.data[test, :], significance=0.1)
header = np.array(['min','max','Truth'])
table = np.vstack([prediction.T, data.target[test]]).T
df = pd.DataFrame(np.vstack([header, table]))
print(df)