import sys
import pandas as pd

print("arguments", sys.argv)

Month = int(sys.argv[1])
print(f"Running pipeline,month={Month}")

df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
df['month'] = Month
print(df.head())

df.to_parquet(f"output_{Month}.parquet", index=False)