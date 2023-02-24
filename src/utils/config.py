import os
import shutil

def load_config():
  if not os.path.exists('./config.ini'):
    default_path = os.path.join(os.path.dirname(__file__), 'data', 'default_config.ini')
    shutil.copy(default_path, './config.ini')
  config = {}
  with open('./config.ini', 'r') as f:
    for line in f:
      key, value = line.strip().split('=')
      config[key] = value
  return config