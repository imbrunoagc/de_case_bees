import os
import sys

import requests
import time

from typing import List, Dict, Optional

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
sys.path.append(parent_dir)

from utils.logger import logger
from config.settings import settings

class Breweries:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })

    def _is_valid_api_response(self, data):
        """Verifica se a resposta da API é válida (lista ou dicionário não vazio)"""
        if data is None:
            return False
        if isinstance(data, (list, dict)):
            return bool(data)  # Retorna False para listas/dicts vazios
        return False

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Método base para todas as requisições à API"""
        url = endpoint
        
        for attempt in range(settings.MAX_RETRIES):
            try:
                response = self.session.get(url, params=params)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                logger.error(f"Attempt {attempt + 1} failed for {url}: {str(e)}")
                if attempt == settings.MAX_RETRIES - 1:
                    raise
                time.sleep(settings.REQUEST_DELAY * (attempt + 1))

    def _fetch_paginated(self, endpoint: str,
                        per_page: int = settings.PER_PAGE,
                        params: Optional[Dict] = None
        ) -> List[Dict]:
        
        """Estratégia básica de paginação"""
        all_data = []
        page = 1
        
        while True:
            current_params = {
                'page': page,
                'per_page': per_page,
                **(params or {})
            }
                        
            data = self._make_request(endpoint, params=current_params) # get_data_base_line_zero
            
            if not self._is_valid_api_response(data):
                break
                
            all_data.extend(data)
                            
            if len(data) < per_page:
                break # finish loop of pagination
                
            logger.info(f"Page {page} collected - Total: {len(all_data)}")
            page += 1
            time.sleep(settings.REQUEST_DELAY)
        
        return all_data
    
if __name__ == "__main__":
    data = Breweries()._make_request(endpoint=settings.BASE_URL)
    print(data)