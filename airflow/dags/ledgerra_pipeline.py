from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator

PROJECT = "/opt/airflow/project"

with DAG(
    dag_id="ledgerra_pipeline",
    description="Pull Africa Data Bank series, archive to S3, load to SQLite, run the analysis",
    start_date=datetime(2026, 10, 1),
    schedule=None,
    catchup=False,
    default_args={"retries": 0},
    tags=["ledgerra"],
) as dag:
    pull = BashOperator(task_id="pull", bash_command="python pull_multi.py", cwd=PROJECT)
    load = BashOperator(task_id="load", bash_command="python load_all_to_sqlite.py", cwd=PROJECT)
    phase1 = BashOperator(task_id="phase1_analysis", bash_command="python phase1_analysis.py", cwd=PROJECT)
    phase2 = BashOperator(task_id="phase2_analysis", bash_command="python phase2_analysis.py", cwd=PROJECT)

    pull >> load >> phase1 >> phase2
