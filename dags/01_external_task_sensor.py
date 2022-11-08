from datetime import timedelta
import airflow.utils.dates as air_dates
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.sensors.external_task import ExternalTaskSensor

dag_1 = DAG(
    dag_id="01_external_task_sensored",
    description="Example of external task sensor",
    start_date=air_dates.days_ago(2),
    schedule_interval="0 16 * * *",
)

dag_2 = DAG(
    dag_id="01_external_task_sensor",
    description="Example of dependant DAG",
    start_date=air_dates.days_ago(2),
    schedule_interval="0 18 * * *",
)

DummyOperator(task_id="copy_to_raw", dag=dag_1) >> DummyOperator(task_id="process_supermarket", dag=dag_1)

wait = ExternalTaskSensor(
    task_id="wait_for_process_supermarket",
    external_dag_id="01_external_task_sensored",
    external_task_id="process_supermarket",
    execution_delta=timedelta(hours=6),
    dag=dag_2,
)
wait >> DummyOperator(task_id="report", dag=dag_2)
