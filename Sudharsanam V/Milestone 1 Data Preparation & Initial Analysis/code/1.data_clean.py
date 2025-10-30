import pandas as pd

# Load the CSV file
file_path = "GlobalWeather.csv"
df = pd.read_csv(file_path)

# Define the required columns
keep_cols = [
    'country', 'location_name', 'latitude', 'longitude', 'timezone', 'last_updated',
    'temperature_celsius', 'feels_like_celsius', 'humidity', 'precip_mm',
    'condition_text', 'cloud', 'wind_kph', 'wind_direction', 'uv_index',
    'air_quality_PM2.5', 'air_quality_PM10', 'air_quality_us-epa-index',
    'sunrise', 'sunset'
]

# Filter only existing columns
existing_keep_cols = [col for col in keep_cols if col in df.columns]

# Create cleaned DataFrame
df_clean = df[existing_keep_cols].copy()

# Drop duplicates and handle missing values
df_clean = df_clean.drop_duplicates(subset=['country', 'location_name', 'last_updated'])
df_clean = df_clean.dropna(subset=['temperature_celsius', 'humidity'])

# Save cleaned dataset
df_clean.to_csv("weather_clean_story.csv", index=False)

# Save excluded columns
excluded_cols = [col for col in df.columns if col not in existing_keep_cols]
df_excluded = df[excluded_cols].copy()
df_excluded.to_csv("weather_excluded_columns.csv", index=False)

print("✅ Cleaned data saved to 'weather_clean_story.csv'")
print("📁 Excluded columns saved to 'weather_excluded_columns.csv'")
