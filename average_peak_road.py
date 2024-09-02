import pandas as pd

# Load the dataset
file_path = '1721297156-887109_sa_1955_cc_f_45_wg_00000_0001-0000_10_0000000.csv'
data = pd.read_csv(file_path)

# Extract positive peak values for each of the gyr columns
positive_gyrx_peaks = data['gyrx'][data['gyrx'] > 10].max()
positive_gyry_peaks = data['gyry'][data['gyry'] > 10].max()
positive_gyrz_peaks = data['gyrz'][data['gyrz'] > 0].max()

# Calculate the average of these peak values
average_peak_value = (positive_gyrx_peaks + positive_gyry_peaks + positive_gyrz_peaks) / 3

# Print the results
print(f"Positive peak value for gyrx: {positive_gyrx_peaks}")
print(f"Positive peak value for gyry: {positive_gyry_peaks}")
print(f"Positive peak value for gyrz: {positive_gyrz_peaks}")
print(f"Average of positive peak values: {average_peak_value}")
