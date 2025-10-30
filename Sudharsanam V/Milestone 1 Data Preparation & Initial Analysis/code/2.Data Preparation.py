# -----------------------------------------------------------
# Milestone 1: Data Preparation & Initial Analysis
# Dataset: GlobalWeather.csv
# -----------------------------------------------------------

import pandas as pd
import numpy as np

# 1️⃣ Load dataset
df = pd.read_csv("weather_clean_story.csv`")

# 2️⃣ Inspect structure and data types
print("Initial Dataset Info:")
print(df.info())
print("\nSample Data:")
print(df.head())

# 3️⃣ Handle missing values
# Replace empty strings and fill missing numerics with column mean
df.replace(["", "NA", "N/A", "null"], np.nan, inplace=True)

numeric_cols = [
    "temperature_celsius", "feels_like_celsius", "humidity", "precip_mm",
    "cloud", "wind_kph", "uv_index",
    "air_quality_PM2.5", "air_quality_PM10", "air_quality_us-epa-index"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df[col] = df[col].fillna(df[col].mean())

# Fill missing categorical data (like condition_text, wind_direction) with mode
for col in ["condition_text", "wind_direction", "timezone"]:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].mode()[0])

# 4️⃣ Handle anomalies (e.g., humidity > 100, negative precipitation)
df.loc[df["humidity"] > 100, "humidity"] = 100
df.loc[df["humidity"] < 0, "humidity"] = np.nan
df["humidity"] = df["humidity"].fillna(df["humidity"].mean())

df.loc[df["precip_mm"] < 0, "precip_mm"] = 0
df.loc[df["temperature_celsius"] < -90, "temperature_celsius"] = np.nan
df["temperature_celsius"] = df["temperature_celsius"].fillna(df["temperature_celsius"].mean())

# 5️⃣ Convert & normalize units
df["wind_kph_norm"] = (df["wind_kph"] - df["wind_kph"].min()) / (df["wind_kph"].max() - df["wind_kph"].min())
df["humidity_norm"] = df["humidity"] / 100

# 6️⃣ Convert last_updated to datetime
df["last_updated"] = pd.to_datetime(df["last_updated"], errors="coerce")

# 7️⃣ Create Month column & aggregate monthly averages
df["month"] = df["last_updated"].dt.to_period("M")

monthly_df = (
    df.groupby(["country", "location_name", "month"], as_index=False)
      .agg({
          "temperature_celsius": "mean",
          "feels_like_celsius": "mean",
          "humidity": "mean",
          "precip_mm": "mean",
          "wind_kph": "mean",
          "uv_index": "mean",
          "air_quality_PM2.5": "mean",
          "air_quality_PM10": "mean",
          "air_quality_us-epa-index": "mean"
      })
)

# 8️⃣ Save cleaned and aggregated datasets
df.to_csv("Cleaned_GlobalWeather.csv", index=False)
monthly_df.to_csv("Monthly_GlobalWeather.csv", index=False)

# 9️⃣ Generate summary report
summary = {
    "Total Rows (Raw)": len(df),
    "Columns": list(df.columns),
    "Missing Values (after cleaning)": df.isnull().sum().to_dict(),
    "Numeric Columns Summary": df.describe().to_dict()
}

summary_df = pd.DataFrame({"Attribute": summary.keys(), "Details": summary.values()})
summary_df.to_csv("Data_Summary_Report.csv", index=False)

# 🔟 Display completion message
print("\n✅ Milestone 1 Complete!")
print("Files generated:")
print(" - Cleaned_GlobalWeather.csv")
print(" - Monthly_GlobalWeather.csv")
print(" - Data_Summary_Report.csv")
