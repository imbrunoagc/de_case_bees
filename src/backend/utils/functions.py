import json
from typing import List, Dict

def read_json(file_path: str, name_file: str) -> List[Dict]:
    """Leitura de arquivo no formato/extensao .json"""
    with open(f'{file_path}/{name_file}.json') as f:
        return json.load(f)

def write_json(data: List[Dict], path: str, name: str):
    """Escrita do conteudo em JSON na indentação 4"""
    with open(f"{path}/{name}" + '.json', 'w') as f:
        json.dump(data, f, indent=4)
        print(f'Successfully saved file -> {path}/{name}.json')