import os
import zipfile
import glob
import datetime

from server.enums.log_levels import LogLevels

class LogHandler:
  def __init__(self, config, wrapper):
    self.config = config
    self.wrapper = wrapper
    self.log = []
    self.output_handler = None
    self.error_handler = None
  
  def connect_output(self, output_handler):
    self.output_handler = output_handler
  
  def connect_error_handling(self, error_handler):
    self.error_handler = error_handler
  
  def append(self, message, source="spsm", severity=LogLevels.INFO):
    """
    Add a log entry with the current timestamp, message, and severity level to the log list.

    Args:
        message (str): The log message to add.
        severity (int, optional): The severity level of the log message. 0 is INFO, 1 is WARNING, 
        2 is ERROR, 3 is ALERT, 4 is CRITICAL, and 5 is FATAL. Defaults to 0.
    """
    time = datetime.datetime.now()
    formatted_time = time.strftime("%H:%M:%S")
    log_val = [formatted_time, message, severity, source]
    self.log.append(log_val)
    self.output_handler.queue_output(self.log_to_string(log_val), color=severity.value)

  def set_output_handler(self, output_handler):
    self.output_handler = output_handler

  def log_to_string(self, log):
    return f"[{log[0]} {log[2].name}] [{log[3]}]: {log[1]}\n"

  def get_log_as_strings(self):
    log = []
    for line in self.log:
      log.append({'content': self.log_to_string(line), 'color': line[2].value})
      
    return log
  
  def dump_log(self):
    logs_dir = 'spsm/logs'
    
    if not os.path.exists(logs_dir):
      os.makedirs(logs_dir)

    time = datetime.datetime.now()
    formatted_time = time.strftime("[%Y-%m-%d]")

    file_name = f'{formatted_time}.log'
    latest_file_name = 'latest.log'

    base_file_path = os.path.join(logs_dir, file_name)
    latest_file_path = os.path.join(logs_dir, latest_file_name)

    try:
      if len(os.listdir(logs_dir)) > int(self.config['max_stored_logs']):
        self.zip_logs()
    except Exception as e:
      self.append(f"{e}")

    if os.path.exists(latest_file_path):
      i = 1
      while True:
        file_path = f"{base_file_path[:-4]}-{i}{base_file_path[-4:]}"
        if os.path.exists(file_path):
          i += 1
        else:
          os.rename(latest_file_path, file_path)
          break
      
    with open(latest_file_path, 'w') as f:
      f.write('\n---------- START LOGS\n\n')
      
      for log in self.log:
        f.write(self.log_to_string(log))
      
      f.write('\n\n---------- END LOGS\n')
  def zip_logs(self):
    self.append("Archiving logs...", source='spsm/LogHandler')
    cwd = os.getcwd()
    os.chdir('spsm/logs')
    file_paths = glob.glob('*.log')
    file_paths.remove('latest.log')
    
    time = datetime.datetime.now()
    formatted_time = time.strftime("[%Y-%m-%d]")

    archive_dir = 'archive'
    file_name = f'{formatted_time}.zip'
    
    file_path = os.path.join(archive_dir, file_name)
    
    i = 1
    while True:
      file_path = f"{file_path.split('.')[0]}-{i}.zip"
      self.append(f"{file_path}")
      if os.path.exists(file_path):
        i += 1
      else:      
        with zipfile.ZipFile(file_path, 'w') as file:
          for path in file_paths:
            file.write(path)
            os.remove(path)
        break
    
    os.chdir(cwd)
      