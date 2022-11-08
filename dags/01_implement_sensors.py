import os
from pathlib import Path

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.sensors.python import PythonSensor
import airflow.utils.dates as air_date


def _wait_for_data(directory: str, filemask: str):
    searching_path = Path(directory)
    Path.mkdir(searching_path, parents=True, exist_ok=True)
    data_files = searching_path.glob(filemask)
    success_file = searching_path / "_SUCCESS"
    return data_files and success_file.exists()


with DAG(
        dag_id="01_implement_sensors",
        description="Implementing Sensor functionality",
        start_date=air_date.days_ago(1),
        schedule_interval="0 16 * * *",
) as dag:
    cwd = os.getcwd()

    for store_number in range(1, 5):
        wait_for_data = PythonSensor(
            task_id=f"wait_for_data_{store_number}",
            python_callable=_wait_for_data,
            op_kwargs={
                "directory": f"{cwd}/tmp/01_implement_sensors/supermarket_{store_number}/",
                "filemask": "data_*.csv"
            },
            timeout=600,
            mode="reschedule",
        )

        copy = DummyOperator(task_id=f"copy_to_raw_supermarket_{store_number}")
        process = DummyOperator(task_id=f"process_supermarket_{store_number}")
        create_metrics = DummyOperator(task_id=f"create_metrics_{store_number}")
        wait_for_data >> copy >> process >> create_metrics
