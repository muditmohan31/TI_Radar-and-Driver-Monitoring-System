import os
import time
import shutil
import psutil
from datetime import datetime
import json
import initializer
import csv



def add_comments_ti(task, sensor, content, fps, toc, classes, road_condition, traffic_condition, electronic_disturbance,t_stamp):
    meta_file = 'metadata_v1.csv'
    meta_path = os.path.join(initializer.current_path, 'metadata')
    os.makedirs(meta_path, exist_ok=True)

    config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configs',
                                    'azure_ir_details_config.json')

    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as file:
            user_configuration = json.load(file)
    else:
        print("Configuration file not found.")
        return None

    if not os.path.exists(os.path.join(meta_path, meta_file)):
        with open(os.path.join(meta_path, meta_file), 'w', newline='') as meta_csv:
            csv_writer = csv.writer(meta_csv)
            csv_writer.writerow(['Task', 'Sensor', 'Date', 'Timestamp', 'Name', 'Contact_No',
                                 'Location', 'Gender', 'Age', 'Spectacles', 'Run', 'FPS', 'Time_to_capture', 'Classes', 'Road', 'Traffic', 'disturbance_TT', 'Comments', 'Trail_flag', 'Test_flag'])
            csv_writer.writerow([task,
                                 sensor,
                                 datetime.now().date(),
                                 t_stamp,
                                 user_configuration['name'],
                                 user_configuration['contact_number'],
                                 user_configuration['location'],
                                 user_configuration['gender'],
                                 user_configuration['age'],
                                 user_configuration['spectacles'],
                                 user_configuration['run'],
                                 fps,
                                 toc,
                                 classes,
                                 road_condition,
                                 traffic_condition,
                                 electronic_disturbance,
                                 content])

    else:
        with open(os.path.join(meta_path, meta_file), 'a', newline='') as meta_csv:
            csv_writer = csv.writer(meta_csv)
            csv_writer.writerow([task,
                                 sensor,
                                 datetime.now().date(),
                                 t_stamp,
                                 user_configuration['name'],
                                 user_configuration['contact_number'],
                                 user_configuration['location'],
                                 user_configuration['gender'],
                                 user_configuration['age'],
                                 user_configuration['spectacles'],
                                 user_configuration['run'],
                                 fps,
                                 toc,
                                 classes,
                                 road_condition,
                                 traffic_condition,
                                 electronic_disturbance,
                                 content])




def is_process_running(process_name):
    """Check if there is any running process with the given name."""
    for proc in psutil.process_iter(['pid', 'name']):
        if process_name.lower() in proc.info['name'].lower():
            return True
    return False

def get_process_start_time(process_name):
    """Get the start time of the running process with the given name."""
    for proc in psutil.process_iter(['pid', 'name', 'create_time']):
        if process_name.lower() in proc.info['name'].lower():
            return datetime.fromtimestamp(proc.info['create_time'])
    return None
def rename_file(file_path):
    """Rename the file based on configuration details."""

    # Load configuration data
    config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configs',
                                    'azure_ir_details_config.json')

    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as file:
            config_data = json.load(file)
    else:
        print("Configuration file not found.")
        return None

    # Extract configuration details
    name = str(config_data.get("name", "unknown"))[0:2]
    contact_number = config_data.get("contact_number", "0000000000")
    location = config_data.get("location", "unknown")
    gender = config_data.get("gender", "u")
    age = config_data.get("age", "00")
    spectacles = config_data.get("spectacles", "ng")
    lux = config_data.get("lux", "00000")
    traffic = config_data.get("traffic", "0000-0000")
    run_number = config_data.get("run_number", "01")
    frame_number = "0000000"
    extension = "bin"

    # Create new filename
    t = str(time.time())
    timestamp = t.replace('.', '-')

    new_filename = (f"{timestamp}_{name}_{contact_number[-4:]}_{location}_{gender}_{age}_{spectacles}_"
                    f"{lux}_{traffic}_{run_number}_{frame_number}.{extension}")

    # Construct the new path with the new filename
    new_path = os.path.join(os.path.dirname(file_path), new_filename)

    # Rename the file
    os.rename(file_path, new_path)
    print(f"File renamed to {new_filename}")

    return new_path, timestamp


def move_file(new_path, new_directory):
    """Move the renamed file to the new directory."""
    os.makedirs(new_directory, exist_ok=True)
    shutil.move(new_path, new_directory)
    print(f"File moved to {new_directory}")


def main():


    # Create specific directories
    data_folder = os.path.join(initializer.current_path, 'datafolder')
    driver_vitals_path = os.path.join(data_folder, 'driver_vitals', 'ti_radar', datetime.now().strftime('%Y-%m-%d'))

    os.makedirs(driver_vitals_path, exist_ok=True)

    # Path to monitor
    file_to_check = "C:\\Users\\MUDIT MOHAN\\Desktop\\mmwave_industrial_toolbox_4_9_0\\labs\\vital_signs\\68xx_vital_signs\\gui\\gui_exe\\dataOutputFromEVM.bin"
    process_start_time = None
    process_name = "VitalSignsRadar_Demo.exe"

    while True:
        if os.path.exists(file_to_check):
            if process_start_time is None and is_process_running("VitalSignsRadar_Demo.exe"):
                process_start_time = get_process_start_time("VitalSignsRadar_Demo.exe")

            if not is_process_running("VitalSignsRadar_Demo.exe") and process_start_time:
                process_end_time = datetime.now()
                execution_duration = process_end_time - process_start_time
                print(f"{process_name} executed for {execution_duration}")


                new_path, timestamp = rename_file(file_to_check)
                if new_path:
                    move_file(new_path, driver_vitals_path)
                    comment = input("Enter the comment:")
                    add_comments_ti('driver_vitals', 'ti_radar', comment, '0', execution_duration, 0, '0', '0','0',timestamp)
                break
            else:
                print(f"{process_name} is still running. Waiting...")
                time.sleep(10)  # Check every 10 seconds
        else:
            print(f"File {file_to_check} does not exist. Checking again...")
            time.sleep(10)  # Check every 10 seconds


if __name__ == "__main__":
    while True:
        main()
