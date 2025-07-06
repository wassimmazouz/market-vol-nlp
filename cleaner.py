import pandas as pd
import re

headlines = pd.read_csv('data/news_headlines/cnbc_headlines.csv')

print("Initial Data:")
print(headlines.head())
print("\nDataset Info:")
print(headlines.info())

def clean_text(text):
    text = str(text).lower()                          # Lowercase
    text = re.sub(r'[^a-zA-Z\s]', '', text)          # Remove non-letter characters
    text = re.sub(r'\s+', ' ', text)                 # Replace multiple spaces with single space
    return text.strip()

# Apply text cleaning
headlines['clean_headline'] = headlines['Headlines'].apply(clean_text)

# Parse date column
headlines['date'] = pd.to_datetime(headlines['Time'], errors='coerce')

# Check for missing or malformed dates
missing_dates = headlines['date'].isna().sum()
print(f"\nMissing dates after parsing: {missing_dates}")

# Drop rows with missing dates
headlines = headlines.dropna(subset=['date'])

# Check for duplicates
duplicates = headlines.duplicated(subset=['date', 'clean_headline']).sum()
print(f"Found {duplicates} duplicate rows. Removing them...")

# Drop duplicates
headlines = headlines.drop_duplicates(subset=['date', 'clean_headline'])

# Final check
print(f"\nCleaned dataset shape: {headlines.shape}")
print(headlines.head())
