import os
import sys
from datetime import timedelta, datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
sys.path.append(parent_dir)

from pipeline.layer_bronze_1.bronze import run_bronze
#from pipeline.layer_silver_2.

from airflow.decorators import dag, task

@dag(
    dag_id="pipe_brewery",
    description="pipeline",
    schedule=None,
    start_date=datetime(2024, 12, 5),
    catchup=False
)
def pipeline():
    
    @task
    def brewery_to_bronze():
        run_bronze()

    # @task
    # def transform_in_silver():
    #     pass

    # @task
    # def silver_to_gold():
    #     pass

    brewery_to_bronze() ##>> transform_data_from_bronze_to_silver() >> silver_to_gold()

pipeline()