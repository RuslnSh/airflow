from airflow import DAG
from airflow.providers.amazon.aws.operators.s3 import S3CopyObjectOperator
import airflow.utils.dates as air_dates


with DAG(
    dag_id="02_calc_airbnb_stats",
    description="description",
    start_date=air_dates.days_ago(1),
    schedule_interval=None,
) as dag:
    S3CopyObjectOperator(
        task_id="...",
        source_bucket_name="databucket",
        source_bucket_key="/data/{{ ds }}.json",
        dest_bucket_name="backupbucket",
        dest_bucket_key="/data/{{ ds }}-backup.json",
    )