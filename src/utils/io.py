import os
import json
from sys import platform

def read_json_file(path):
    obj = {}
    with open(path, 'r') as file:
        obj = json.load(file)
        
    return obj

def write_json_file(path, obj):
    with open(path, 'w') as file:
        json.dump(obj, file)

def save_data_file(filename, content):
  # Get the user's home directory
  home_dir = os.path.expanduser("~")
    # Determine the appropriate directory for data files based on the operating system
  if platform == "linux" or platform == "linux2" or platform == "darwin":  # Linux or macOS
      data_dir = os.path.join(home_dir, ".local", "share")
  elif platform == "win32":  # Windows
      data_dir = os.path.join(os.getenv("APPDATA"))
  else:
      print("Unknown operating system")
      return
    
  data_dir = os.path.join(data_dir, 'spsm')
  
  # Create the data directory if it does not exist
  if not os.path.exists(data_dir):
      os.makedirs(data_dir)

  # Create a new file in the data directory
  full_filename = os.path.join(data_dir, filename)
  with open(full_filename, "w") as f:
      f.write(content)