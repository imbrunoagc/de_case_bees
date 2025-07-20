from typing import List, Type, TypeVar
from pydantic import BaseModel, parse_obj_as, ValidationError
import pandas as pd

T = TypeVar("T", bound=BaseModel) # Só vai herdar se a classe de modelo for do tipo BaseModel

def validate_and_convert_to_df(data: List[dict], model: Type[T]) -> pd.DataFrame:
    """
    Valida uma lista de dicionários com um modelo Pydantic e converte em DataFrame.
    """
    try:
        validated_data = parse_obj_as(List[model], data)
        return pd.DataFrame([item.dict() for item in validated_data])
    except ValidationError as e:
        print("Erro de validação nos dados:")
        print(e.json())
        raise