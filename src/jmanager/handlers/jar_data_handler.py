import os
import json

from utils.config import load_config
from utils import io

class JarDataHandler():
  def __init__(self):
    self.config = load_config()
    self.jar_data = self.load_jar_data()
    
  def touches_jar_data(func):
    def touch_and_save(self, *args, **kwargs):
      func(args, kwargs)
      self.save_jar_data()
    return touch_and_save
  
  @touches_jar_data()
  def upsert_jar_data(self, name, type, url):
    if type != 'server' and type != 'plugin':
      print("Jar must be either of type 'server' or 'plugin'")
      return
    
    jar_data = {}
    
    jar_data['url'] = url
    target = f'./jars/plugins/{name}/'
    if type == 'server':
      target = './jars/server/'
      
    jar_data['target'] = target
    
    self.jar_data[name] = jar_data
    
  def load_jar_data(self):
    path = self.config['jar_data_path'] if 'jar_files_path' in self.config.keys() else 'jardata.json'
    if not os.path.exists(path):
      io.write_json_file(path, {})
    
    return io.read_json_file(path)
    
  def save_jar_data(self):
    path = self.config['jar_data_path'] if 'jar_files_path' in self.config.keys() else 'jardata.json'
    io.write_json_file(path, self.jar_data)
      
  
  