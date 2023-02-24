import requests
from utils import config


class DownloadHandler:
  def __init__(self):
    self.config = config.load_config()
    
  def download_from_url(self, url, directory_path):
    r = requests.get(url, allow_redirects=True)
    file_path = directory_path + r.headers.get('Content-Disposition').split('=')[1]
    open(file_path, 'w').write(r.content)