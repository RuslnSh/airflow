from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago, timedelta

default_args = {
    "owner": "ShR",
    "custom_key_1": "custom_value_1",
    "custom_key_2": "custom_value_2"
}

with DAG(
        dag_id="01_pass_params",
        description="Pass parameters to python callable",
        start_date=days_ago(1),
        schedule_interval="@daily",
        # default_args=default_args,
        user_defined_macros=default_args,  # Allow using dictionary keys in jinja templates inside the dag
) as dag:
    def _print_kwargs_1(**kwargs):
        print("Inside the '_print_kwargs_1' function")
        for key in kwargs.keys():
            print(str(key) + " " + str(kwargs[key]))

    print_kwargs_1 = PythonOperator(
        task_id="print_kwargs_1",
        python_callable=_print_kwargs_1,
        params={
            "param_1": "value_1",
            "param_2": "value_2"
        },
        dag=dag
    )

    print_kwargs_2 = PythonOperator(
        task_id="print_kwargs_2",
        python_callable=lambda param_1, param_2: print(param_1, param_2),
        op_args=["value_1", "value_2"],
        dag=dag
    )

    def _print_kwargs_3(param_1, **context):
        print("Inside the '_print_kwargs_3' function")
        print("param_1: " + str(param_1))
        for key in context.keys():
            print(context[key])

    print_kwargs_3 = PythonOperator(
        task_id="print_kwargs_3",
        python_callable=_print_kwargs_3,
        op_kwargs={
            "param_1": "value_1",
            "param_2": "value_2",
        },
        dag=dag
    )

    bash_command_1 = """
        echo "access via DAG's user_defined_macros = {{ custom_key_1 }}"
        echo "access via Operator's params = {{ params.custom_key_2 }}"
    """

    print_bash_1 = BashOperator(
        task_id='print_bash_1',
        bash_command=bash_command_1,
        params=default_args,
        dag=dag,
    )

    print_kwargs_1  # pass with param attribute
    print_kwargs_2  # pass with op_args attribute
    print_kwargs_3  # pass with op_kwargs attribute
    print_bash_1  # pass with param attribute and jinja template
