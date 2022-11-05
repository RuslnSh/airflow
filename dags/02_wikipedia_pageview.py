import os

import airflow.utils.dates
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from include.dag_02_wikipedia_pageview_lib import _download_pages_python, _fetch_pageviews

cwd = os.getcwd()

with DAG(
    dag_id="02_wikipedia_pageview",
    description="download data from wiki and calc statistics",
    start_date=airflow.utils.dates.days_ago(1),
    schedule_interval="@daily",
    template_searchpath=[f"{cwd}/tmp/"],  # to search sql scripts for PostgresOperator by Jinja
) as dag:
    # download_pages_bash = BashOperator(
    #     task_id="download_pages_bash",
    #     bash_command=f"curl -o {cwd}/tmp/wikipageviews.gz "
    #                  "https://dumps.wikimedia.org/other/pageviews/"
    #                  "{{ execution_date.year }}/"
    #                  "{{ execution_date.year }}-"
    #                  "{{ '{:02}'.format(execution_date.month) }}/"
    #                  "pageviews-{{ execution_date.year }}"
    #                  "{{ '{:02}'.format(execution_date.month) }}"
    #                  "{{ '{:02}'.format(execution_date.day) }}-"
    #                  "{{ '{:02}'.format(execution_date.hour-1) }}0000.gz"
    #     ,
    #     dag=dag
    # )

    download_pages_python = PythonOperator(
        task_id="download_pages_python",
        python_callable=_download_pages_python,
        op_kwargs={
            "output_path": f"{cwd}/tmp",
            "output_file": "wikipageviews.gz"
        },
        dag=dag
    )

    extract_gz = BashOperator(
        task_id="extract_gz",
        bash_command=f"gunzip --force {cwd}/tmp/wikipageviews.gz",
        dag=dag,
    )

    fetch_pageviews = PythonOperator(
        task_id="fetch_pageviews",
        python_callable=_fetch_pageviews,
        op_kwargs={
            "pagenames": {
                "Google",
                "Amazon",
                "Apple",
                "Microsoft",
                "Facebook",
            }
        },
        dag=dag,
    )

    write_to_postgres = PostgresOperator(
        task_id="write_to_postgres",
        postgres_conn_id="postgres_db",
        sql="postgres_insert_stat.sql",
        dag=dag,
    )

download_pages_python >> extract_gz >> fetch_pageviews >> write_to_postgres
