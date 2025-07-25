import os
import sys

from loguru import logger

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
data_dir = os.path.abspath(os.path.join(current_dir, "..", "..", "..", "..","data"))
sys.path.append(parent_dir)

from api.breweries_api import Breweries
from api.config.settings import settings
from utils.functions import write_json

def run_bronze():

    try:
        #data = Breweries()._make_request(endpoint=settings.BASE_URL) # -- Consulta da primeira pagina 
        data = Breweries()._fetch_paginated(endpoint=settings.BASE_URL)
        logger.success("Coleta finalizada!")
    except Exception as e:
        logger.error("Falha na coleta de dados: ", e)

    write_json(
        data=data,
        path=os.path.join(data_dir, 'bronze'),
        name='breweries')

if __name__ == "__main__":
    run_bronze()