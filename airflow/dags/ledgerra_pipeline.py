from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator

PROJECT = "/opt/airflow/project"

with DAG(
    dag_id="ledgerra_pipeline",
    description="Pull Africa Data Bank series, archive to S3, load to SQLite, run the analysis",
    start_date=datetime(2026, 10, 1),
    schedule="0 6 * * *",  # daily at 06:00 UTC
    max_active_runs=1,
    catchup=False,
    default_args={"retries": 0},
    tags=["ledgerra"],
) as dag:
    # pull_multi.py exits 99 when nothing was fetched only because of the API quota:
    # show that as Skipped (so load/analysis don't run on stale data), not as a green Success.
    pull = BashOperator(task_id="pull", bash_command="python pull_multi.py", cwd=PROJECT, skip_on_exit_code=99)
    load = BashOperator(task_id="load", bash_command="python load_all_to_sqlite.py", cwd=PROJECT)
    phase1 = BashOperator(task_id="phase1_analysis", bash_command="python phase1_analysis.py", cwd=PROJECT)
    phase2 = BashOperator(task_id="phase2_analysis", bash_command="python phase2_analysis.py", cwd=PROJECT)

    pull >> load >> phase1 >> phase2
