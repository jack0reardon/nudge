import pandas as pd
from dfply import * 

df = pd.read_csv('./data/202210-baywheels-tripdata.csv')

print(df.head())

# asdf1 = df.groupby(['start_lat', 'start_lng']).size().sort_values(ascending = False).reset_index()
# print(asdf1)
# asdf = asdf1[asdf1.size >= 100]
# print(asdf)


print(df >>
 group_by(X.start_lat, X.start_lng) >>
 summarize(count = n(X.start_lat)))
