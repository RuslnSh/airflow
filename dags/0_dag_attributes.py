from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.python import PythonSensor

default_args = {
    "owner": "ShR",
    "depends_on_past": False,  # scheduled DUG_RUN start even if previous DAG_RUN failed
    "retries": 1,
    "retry_delay": 5
    # "email": ["rush2331@gmail.com"],
    # "email_on_failure": True,
    # "email_on_retry": True,
    # "end_date": datetime(2024, 1, 1),
    # "execution_timeout": timedelta(seconds=300),
    # "sla": timedelta(hours=2),
    # "execution_timeout": timedelta(seconds=300),
    # "on_failure_callback": _function,
    # "on_success_callback": _another_function,
    # "on_retry_callback": _another_function,
    # "sla_miss_callback": _another_function,
    # "trigger_rule": "all_success"
    # "queue": "bash_queue",
    # "pool": "backfill",
    # "priority_weight": 10,
    # "end_date": datetime(2016, 1, 1),
    # "wait_for_downstream": False,
}


dag = DAG(
    default_args=default_args,
    user_defined_macros=default_args,  # Each value in the dictionary is evaluated as a Jinja template
    max_active_runs=1,
    catchup=False,  # Allow to execute previous scheduled tasks
    concurrency=10  # Allowing number if concurrently running DAGs
)


task_1 = PythonOperator(
    task_id='task_1',
    python_callable=lambda x: x*x,
    params=1,
    dag=dag
)

task_2 = PythonSensor(
    task_id="task_2",
    python_callable=lambda filename: filename.is_exists(),
    op_kwargs={"filename": "data.json"},
    timeout=600,  #
    mode="reschedule",  # With this mode sensor release slot after poking, allowing other tasks to run
    dag=dag,
)
