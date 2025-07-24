import os
import sys

import pandas as pd

current_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
data_dir = os.path.abspath(os.path.join(current_dir, "..", "..", "..", "..", "data"))
sys.path.append(parent_dir)

from mini_io.s3_manager import PandasBucket

def run_gold() -> None:
        
        bucket_silver = PandasBucket(name="silver")
        df = bucket_silver.read_parquet_partitioned(prefix='breweries', filters=["country", "state"])
        
        print(df.columns)

        df_aggregate = (
            df
            .groupby(["brewery_type", "country", "state"], observed=True)["id"] # Apenas as combinações que ocorreram '>0'
            .count()
            .reset_index(name="quantidade")
        )\
        .sort_values(['quantidade'], ascending=False)

        bucket_gold = PandasBucket(name="gold")
        bucket_gold.write_parquet_partitioned(
            df=df_aggregate,
            prefix="quantity_of_breweries_per_type_and_location.parquet"
        )
        
if __name__ == "__main__":
    run_gold()