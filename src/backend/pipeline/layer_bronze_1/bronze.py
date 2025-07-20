import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
data_dir = os.path.abspath(os.path.join(current_dir, "..", "..", "..", "..","data"))
sys.path.append(parent_dir)

from api.breweries_api import Breweries
from api.config.settings import settings
from mini_io.s3_manager import PandasBucket

def run_bronze():
    data = Breweries()._fetch_paginated(endpoint=settings.BASE_URL)
    PandasBucket(name='bronze').write_json(data=data, name='breweries')