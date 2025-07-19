import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
data_dir = os.path.abspath(os.path.join(current_dir, "..", "..", "..", "data"))
sys.path.append(parent_dir)

from api.breweries_api import Breweries
from api.config.settings import settings
from utils.functions import write_json

def run_bronze() -> None:
    data = Breweries()._make_request(endpoint=settings.BASE_URL)
    write_json(data,os.path.join(data_dir, "bronze"),'breweries')

if __name__ == "__main__":
    run_bronze()