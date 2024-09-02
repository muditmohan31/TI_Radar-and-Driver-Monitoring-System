import pandas as pd

# Step 1: Read the CSV file
df = pd.read_csv('cleaned_file.csv')

# Print column names to verify the column you want to smooth
print(df.columns)

# Step 2: Apply Exponential Smoothing
def exponential_smoothing(df, column, alpha):
    df[column + '_smoothed'] = df[column].ewm(alpha=alpha).mean()
    return df

# Step 3: Apply the function to the DataFrame
# Replace 'your_column_name' with the actual column name you want to smooth
smoothed_df = exponential_smoothing(df, 'outBreathWfm', alpha=1.0)

# Step 4: Save the smoothed data to a new CSV file
smoothed_df.to_csv('smoothed_file.csv', index=False)
