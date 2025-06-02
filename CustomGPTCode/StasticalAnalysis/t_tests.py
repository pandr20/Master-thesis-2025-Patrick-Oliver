import numpy as np
from scipy.stats import linregress, ttest_ind
import matplotlib.pyplot as plt

A = np.array([
    [48.54, 50.15, 51.18, 51.74],
    [51.98, 53.46, 54.40, np.nan],
    [53.47, 55.08,  np.nan, np.nan],
    [54.67, 56.46,  np.nan, np.nan]
])

m, n = A.shape

col_indices = np.arange(n)
row_slopes = []
for i in range(m):
    y = A[i, :]
    mask = ~np.isnan(y)
    if np.sum(mask) >= 2:  # at least 2 points needed
        slope, *_ = linregress(col_indices[mask], y[mask])
        row_slopes.append(slope)

# Get column slopes (over rows)
row_indices = np.arange(m)
col_slopes = []
for j in range(n):
    y = A[:, j]
    mask = ~np.isnan(y)
    if np.sum(mask) >= 2:
        slope, *_ = linregress(row_indices[mask], y[mask])
        col_slopes.append(slope)

row_slopes = np.array(row_slopes)
col_slopes = np.array(col_slopes)

t_stat, p_value = ttest_ind(col_slopes, row_slopes, alternative='greater')

print("Average row slope:", np.mean(row_slopes))
print("Average column slope:", np.mean(col_slopes))
print("T-statistic:", t_stat)
print("P-value (row > col):", p_value)
