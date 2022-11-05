import uuid

import airflow.utils.dates as air_dates
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.latest_only import LatestOnlyOperator
from airflow.decorators import task

# Trigger rules:
# all_success
# all_failed
# all_done (task starts when downstrean tasks executed regardless successfully or not)
# one_failed
# one_success
# none_failed
# none_skipped
# dummy (for tests)

# XCom limitation:
# SQLite — Stored as BLOB type, 2GB limit
# PostgreSQL — Stored as BYTEA type, 1 GB limit
# MySQL — Stored as BLOB type, 64 KB limit
# Or create your own XCom backend inherited from BaseXCom

ERP_SWITCH_DATE = air_dates.days_ago(2)


def _pick_erp(**context):
    if context["execution_date"] > ERP_SWITCH_DATE:
        return "new_fetch_sales"
    else:
        return "old_fetch_sales"


with DAG(
        dag_id="01_set_chain",
        description="Set chain of operators",
        start_date=air_dates.datetime(2022, 11, 1),  # Best practice is to use a static start_date
        end_date=air_dates.datetime.now(),
        schedule_interval="@daily"
)as dag:
    start_task = DummyOperator(task_id="start_task")

    pick_erp = BranchPythonOperator(
        task_id="pick_erp",
        python_callable=_pick_erp
    )

    new_fetch_sales = DummyOperator(task_id="new_fetch_sales")
    old_fetch_sales = DummyOperator(task_id="old_fetch_sales")

    new_clean_sales = DummyOperator(task_id="new_clean_sales")
    old_clean_sales = DummyOperator(task_id="old_clean_sales")

    fetch_weather = DummyOperator(task_id="fetch_weather")
    clean_weather = DummyOperator(task_id="clean_weather")

    join_erp = DummyOperator(task_id="join_erp", trigger_rule="none_failed")
    join_datasets = DummyOperator(task_id="join_datasets")


    # def _train_model(**context):
    #     model_id = str(uuid.uuid4())
    #     context["task_instance"].xcom_push(key="model_id", value=model_id)
    #
    #
    # train_model = PythonOperator(task_id="train_model", python_callable=_train_model)
    #
    #
    # def _deploy_model(**context):
    #     model_id = context["task_instance"].xcom_pull(task_ids="train_model", key="model_id")
    #     print(f"Deploying model {model_id}")
    #
    #
    # deploy_model = PythonOperator(task_id="deploy_model", python_callable=_deploy_model)

    @task
    def train_model():
        model_id = str(uuid.uuid4())
        return model_id


    @task
    def deploy_model(model_id: str):
        print(f"Deploying model {model_id}")


    pick_latest = LatestOnlyOperator(task_id="pick_latest")

    start_task >> [fetch_weather, pick_erp]
    fetch_weather >> clean_weather
    pick_erp >> [old_fetch_sales, new_fetch_sales]
    old_fetch_sales >> old_clean_sales
    new_fetch_sales >> new_clean_sales
    [old_clean_sales, new_clean_sales] >> join_erp
    [clean_weather, join_erp] >> join_datasets

    model_id = train_model()
    deploy_model = deploy_model(model_id)

    join_datasets >> model_id
    pick_latest >> deploy_model
