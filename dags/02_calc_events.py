import pathlib
import os

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import airflow.utils.dates as air_dates

from include.dag_02_calc_events_lib import _calculate_stats, _send_email

with DAG(
        dag_id="02_calc_events",
        start_date=air_dates.days_ago(1),
        schedule_interval="@daily"
) as dag:
    '''
    For dag start need to send event to https://localhost:5000/events
    You may found service in docker/events-api directory
    '''

    cwd = os.getcwd()
    events_wd = f"{cwd}/tmp/02_calc_events/events"
    # pathlib.Path(events_wd).mkdir(parents=True, exist_ok=True)
    stats_wd = f"{cwd}/tmp/02_calc_events/stats"
    pathlib.Path(stats_wd).mkdir(parents=True, exist_ok=True)

    download_events = BashOperator(
        task_id="download_events",
        bash_command=(
            f"mkdir -p {events_wd} && "
            f"curl -o {events_wd}/"
            "{{ds}}.json "
            "http://172.28.0.1:5000/events?"  # TODO localhost don'w work, find out why so
            # "http://localhost:5000/events?"
            # "start_date={{execution_date.strftime('%Y-%m-%d')}}&"
            # "end_date={{next_execution_date.strftime('%Y-%m-%d')}}"
            "start_date={{ds}}&"
            "end_date={{next_ds}}"
        ),
        dag=dag
    )

    calculate_stats = PythonOperator(
        task_id="calculate_stats",
        python_callable=_calculate_stats,
        op_kwargs={
            "input_path": f"{events_wd}/" + "{{ds}}.json",
            "output_path": f"{stats_wd}/" + "{{ds}}.csv"
        },
        dag=dag
    )

    send_stats = PythonOperator(
        task_id="send_stats",
        python_callable=_send_email,
        op_kwargs={"address_to": "rush2331@gmail.com"},
        templates_dict={"stats_path": f"{stats_wd}/" + "{{ds}}.csv"},
        dag=dag
    )

download_events >> calculate_stats >> send_stats
