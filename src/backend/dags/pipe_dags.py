import os
import sys
from datetime import datetime, timedelta
from airflow.decorators import dag, task

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
sys.path.append(parent_dir)

from pipeline.layer1_bronze.bronze import run_bronze
from pipeline.layer2_silver.silver import run_silver
from pipeline.layer3_gold.gold import run_gold

#ajustado 10
@dag(
    dag_id="pipe_brewery",
    description="pipeline of data (architecture medallion [bronze --> silver --> gold])",
    schedule=None,
    start_date=datetime.now() - timedelta(days=1),
    catchup=False,
    tags=["modular", "bronze-silver-gold"]
)

def pipeline():
    
    @task
    def brewery_to_bronze():
        run_bronze()

    @task
    def transform_in_silver():
        run_silver()

    @task
    def silver_to_gold():
        run_gold()

    brewery_to_bronze() >> transform_in_silver() >> silver_to_gold()

pipeline()