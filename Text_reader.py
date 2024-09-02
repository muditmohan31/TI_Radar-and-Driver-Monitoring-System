import os
from tqdm import tqdm
def process_files(directory):
  """
  Processes text files in the specified directory, printing file name and content
  if the first element is 0, 1, or 2.

  Args:
    directory: The directory path to search for text files.
  """

  for filename in tqdm(os.listdir(directory)):
    if filename.endswith(".txt"):
      file_path = os.path.join(directory, filename)
      with open(file_path, 'r') as file:
        first_line = file.readline()
        try:
          first_element = int(first_line.split(" ")[0])
          if first_element not in [0, 1, 2]:
            print(f"File: {filename}")
            print(first_line)
            print()
        except (ValueError, IndexError):
          print(filename,first_line)
          # Handle cases where the first line is empty or cannot be converted to int
          continue

# Replace 'your_directory_path' with the actual path to your files
directory_path = r"C:\Users\MUDIT MOHAN\Desktop\VT DMS\annotations\2024-07-22"
process_files(directory_path)
