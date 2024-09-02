import os
import shutil
import pandas as pd
from datetime import datetime


# Function to rename and move the .bin file
def rename_and_move_bin_file(bin_filepath, csv_filename):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_filename)

    # Get the filename from the file path
    bin_filename = os.path.basename(bin_filepath)

    # Search for the row corresponding to the bin file
    row = df[df['filename'] == bin_filename]

    if row.empty:
        print(f"No entry found for {bin_filename} in {csv_filename}")
        return

    # Extract data from the row
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    name = row['name'].values[0]
    phone_number = row['phone_number'].values[0]
    location = row['location'].values[0]
    gender = row['gender'].values[0]
    age = row['age'].values[0]
    spectacles = row['spectacles'].values[0]
    lux = row['lux'].values[0]
    traffic = row['traffic'].values[0]
    run_number = row['run_number'].values[0]
    frame_number = row['frame_number'].values[0]

    # Construct the new filename
    new_filename = f"{timestamp}_{name}_{phone_number}_{location}_{gender}_{age}_{spectacles}_{lux}_{traffic}_{run_number}_{frame_number}.bin"

    # Create the folder structure
    base_folder = os.path.join('driver_vitals', 'ti_radar', timestamp.split('_')[0])
    os.makedirs(base_folder, exist_ok=True)

    # Move and rename the .bin file
    new_file_path = os.path.join(base_folder, new_filename)
    shutil.move(bin_filepath, new_file_path)
    print(f"File {bin_filename} renamed and moved to {new_file_path}")


# Function to process all .bin files in a folder
def process_bin_files_in_folder(bin_folder, csv_filename):
    for filename in os.listdir(bin_folder):
        if filename.endswith('.bin'):
            bin_filepath = os.path.join(bin_folder, filename)
            rename_and_move_bin_file(bin_filepath, csv_filename)


# Example usage
bin_folder = 'path_to_bin_folder'  # Replace with the path to your folder containing .bin files
csv_filename = 'data.csv'  # Replace with the path to your CSV file

process_bin_files_in_folder(bin_folder, csv_filename)
