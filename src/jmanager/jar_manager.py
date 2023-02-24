
import os

from utils import config
from jmanager.handlers import DownloadHandler, JarDataHandler

class JarManager:
  def __init__(self):
    self.config = config.load_config()
    self.jar_data_handler = JarDataHandler()
  
  def upsert_jar(self, name, type='server', url=None):
    self.jar_data_handler.upsert_jar_data(name, type, url)
  
  def download_jar(self, jar_name):
    if jar_name not in jar_data.keys():
      print("Jar name not found!")
      return
    jar_data = self.jar_data[jar_name]
    url = jar_data['url']
    
    if url is None:
      print("Jar has no source URL!")
      return
    
    target = jar_data['target']
    
    dh = DownloadHandler()
    dh.download_from_url(url, target)