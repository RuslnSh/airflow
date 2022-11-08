import os
from pathlib import Path

import airflow.utils.dates as air_dates
from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.operators.dummy import DummyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

# The value of the run_id starts with one of the following:
#  scheduled__ to indicate the DAG run started because of its schedule
#  backfill__ to indicate the DAG run started by a backfill job
#  manual__ to indicate the DAG run started by a manual action (e.g., pressing the Trigger Dag button, or triggered by a TriggerDagRunOperator)


dag_1 = DAG(
    dag_id="01_dag_triggering",
    description="Example if triggering DAG from another DAG",
    start_date=air_dates.days_ago(1),
    schedule_interval="@daily",
    default_args={"depends_on_past": True},
)

dag_2 = DAG(
    dag_id="01_dag_trig_dependant",
    description="Example if dependant DAG",
    start_date=air_dates.days_ago(1),
    schedule_interval=None,
)

cwd = os.getcwd()
for store_number in range(1, 5):
    directory = f"{cwd}/tmp/01_implement_sensors/supermarket_{store_number}/"
    file_name = directory + "data_1.csv"
    print("file_name" + file_name)

    Path(directory).mkdir(parents=True, exist_ok=True)

    wait_for_data = FileSensor(
        task_id=f"wait_for_data_{store_number}",
        filepath=file_name,
        # fs_conn_id="fs_default",  # You have to create this in airflow Admin panel in Connections menu
        dag=dag_1
    )

    copy = DummyOperator(task_id=f"copy_to_raw_supermarket_{store_number}", dag=dag_1)
    process = DummyOperator(task_id=f"process_supermarket_{store_number}", dag=dag_1)
    trigger_create_metrics_dag = TriggerDagRunOperator(
        task_id=f"trigger_create_metrics_dag_supermarket_{store_number}",
        trigger_dag_id="01_dag_trig_dependant",
        dag=dag_1,
    )
    wait_for_data >> copy >> process >> trigger_create_metrics_dag

compute_differences = DummyOperator(task_id="compute_differences", dag=dag_2)
update_dashboard = DummyOperator(task_id="update_dashboard", dag=dag_2)
notify_new_data = DummyOperator(task_id="notify_new_data", dag=dag_2)
compute_differences >> update_dashboard
