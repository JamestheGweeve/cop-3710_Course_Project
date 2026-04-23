import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm

print(df[['price', 'area']].describe())

plt.figure(figsize=(10,5))
sns.histplot(df['price'], kde=True)
plt.title('Histogram of Home Sales Price (USD)')
plt.xlabel('Price (USD)')
plt.ylabel('Frequency')
plt.savefig('price_histogram.png')
plt.close()

plt.figure(figsize=(10,5))
sns.boxplot(x=df['price'])
plt.title('Box Plot of Home Sales Price (USD)')
plt.xlabel('Price (USD)')
plt.savefig('price_boxplot.png')
plt.close()

# Repeat similarly for area histogram & boxplot
# Scatter with regression line
sns.regplot(x='area', y='price', data=df, line_kws={'color': 'red'})
plt.title('Scatter Plot: Price vs Square Footage with Regression Line')
plt.xlabel('Area (sq. ft.)')
plt.ylabel('Price (USD)')
plt.savefig('scatter_regression.png')
plt.close()

# 4 - Regression & Correlation
X = sm.add_constant(df['area'])
model = sm.OLS(df['price'], X).fit()
print(model.summary())  # Gives slope, intercept, R, R², etc.

slope = model.params[1]
intercept = model.params[0]
r = df['price'].corr(df['area'])
r2 = r**2
print(f"Slope: {slope:.2f}, Intercept: {intercept:.2f}, R: {r:.3f}, R2: {r2:.3f}")

# 5 - 95% CI for slope
ci = model.conf_int().iloc[1]
print(f"95% CI for slope: {ci.values}")

# 6 - Hypothesis test (already in model.summary() - look at t-stat and p-value for 'area')
print(f"p-value: {model.pvalues[1]}")
