import airflow.utils.dates as air_dates
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import os

from include.dag_02_rocket_launches_lib import _get_pictures_by_json


with DAG(
        dag_id="02_rocket_launches",
        description="download and save pictures of launched rockets",
        start_date=air_dates.days_ago(1),
        schedule_interval="@daily"
) as dag:
    cwd = os.getcwd()
    src_url = 'https://ll.thespacedevs.com/2.0.0/launch/upcoming'
    json_file = f"{cwd}/tmp/launches.json"
    dst_images = f"{cwd}/tmp/images/"

    download_launches = BashOperator(
        task_id="download_launches",
        bash_command=f"curl -o {json_file} -L {src_url}",
            # o - write to file instead of stdout
            # L - If the server reports that the requested page has moved to a different location, this option will make curl redo the request on the new place
        dag=dag
    )

    get_pictures = PythonOperator(
        task_id="get_pictures",
        python_callable=_get_pictures_by_json,
        op_kwargs={
            "p_jsn": f"{json_file}",
            "p_dst": f"{dst_images}"
        },
        dag=dag
    )

    notify = BashOperator(
        task_id="notify",
        bash_command=f'echo "There are now $(ls {dst_images} | wc -l) images."',
        dag=dag,
    )

download_launches >> get_pictures >> notify
