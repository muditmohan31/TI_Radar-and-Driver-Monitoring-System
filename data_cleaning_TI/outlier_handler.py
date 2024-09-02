import pandas as pd


# Step 1: Read the CSV file
df = pd.read_csv('sameer_radar.csv')

# Step 2: Define a function to remove outliers
def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

# Step 3: Apply the function to the DataFrame
cleaned_df = remove_outliers(df, ['outBreathWfm','outHeartWfm'])  # Replace 'column_name' with the actual column name

# Step 4: Save the cleaned data to a new CSV file
cleaned_df.to_csv('cleaned_file.csv', index=False)
