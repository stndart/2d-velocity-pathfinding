import os

from PIL import Image

import config

class Assets(object):
    def __init__(self):
        self.assets_path = config.assets_path
        self.storage = dict()
    
    def load_asset(self, asset_name: str):
        if asset_name in self.storage:
            return
        
        if hasattr(self, asset_name):
            raise RuntimeError(f"Can't load asset {asset_name}")
        
        asset_fn = os.path.join(self.assets_path, asset_name + '.png')
        if not os.path.exists(asset_fn) or not os.path.isfile(asset_fn):
            raise RuntimeError(f"Not found asset {asset_name}")
        
        self.storage[asset_name] = Image.open(asset_fn)
    
    def __getattribute__(self, attr):
        storage = object.__getattribute__(self, 'storage')
        if attr in storage:
            return storage[attr]
        else:
            return object.__getattribute__(self, attr)

assets = Assets()