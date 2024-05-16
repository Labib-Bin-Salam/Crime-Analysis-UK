import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Define the base URL
base_url = "https://data.police.uk/api/"

# Define the location (latitude and longitude)
location = "51.5074,-0.1278"  # This is the latitude and longitude for London
 
# Define the date range
start_date = datetime(2021, 3, 1)
end_date = datetime.now() - relativedelta(months=3)

#Fetch crime data for the location
crimes = []
for year in range(start_date.year, end_date.year + 1):
    # Start from January if it's not the start year, else start from the start_date month
    start_month = 1 if year > start_date.year else start_date.month
    for month in range(start_month, 13):
        if year == end_date.year and month > end_date.month:
            break
        date_str = f"{year}-{month:02d}"
        response = requests.get(base_url + f"crimes-street/all-crime?lat={location.split(',')[0]}&lng={location.split(',')[1]}&date={date_str}")
        crimes_month = response.json()
        crimes.extend(crimes_month)



import pandas as pd
import json

# Create a DataFrame from the crimes data
df = pd.DataFrame(crimes)

# Remove rows where 'month' is null
df = df.dropna(subset=['month'])

# Convert 'month' from 'YYYY-MM' to datetime
df['month'] = pd.to_datetime(df['month'])

# Rename the 'category' column to 'Crime type'
df = df.rename(columns={'category': 'Crime type'})

# Extract latitude, longitude, name, street, category, and date from the location and outcome_status columns
df['latitude'] = df['location'].apply(lambda x: x['latitude'])
df['longitude'] = df['location'].apply(lambda x: x['longitude'])
df['name'] = df['location'].apply(lambda x: x['street']['name'])
df['street'] = df['location'].apply(lambda x: x['street']['id'])
df['category'] = df['outcome_status'].apply(lambda x: x['category'] if x else None)
df['date'] = df['outcome_status'].apply(lambda x: x['date'] if x else None)

# Rename the 'category' column to 'Last Outcome'
df = df.rename(columns={'category': 'Last Outcome'})

# Drop the original location and outcome_status columns
df = df.drop(columns=['location', 'outcome_status'])


from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns

# Convert 'Crime type' and 'Last Outcome' to numerical form
le = LabelEncoder()
df['Crime type'] = le.fit_transform(df['Crime type'])
df['Last Outcome'] = le.fit_transform(df['Last Outcome'])

# find 3 clusters in the dataframe df
kmeans = KMeans(n_clusters=3, n_init=10)

# Fit the model to the data
kmeans.fit(df[['Crime type', 'Last Outcome']])

# Get the cluster assignments for each data point
df['cluster'] = kmeans.labels_

sns.scatterplot(x='Crime type', y='Last Outcome', hue='cluster', palette='viridis', data=df)
plt.legend(loc='upper right')
plt.show()




from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# predict 'Crime type' based on 'Last Outcome', 'latitude', and 'longitude'
X = df[['Last Outcome', 'latitude', 'longitude']]
y = df['Crime type']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Fit the model to the training data
model.fit(X_train, y_train)

# Use the model to make predictions on the test data
predictions = model.predict(X_test)

# Print a classification report
print(classification_report(y_test, predictions))




from sqlalchemy import create_engine

# connection string
conn_str = (
    r'mysql+mysqlconnector://root:4321@localhost:3306/london_crime_data'
)

# Create a SQLAlchemy engine
engine = create_engine(conn_str)

# Save the DataFrame to a new table in your MySQL database
df.to_sql('city_of_london_street_crime_data', engine, if_exists='replace', index=False)