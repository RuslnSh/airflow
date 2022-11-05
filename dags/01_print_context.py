from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

default_args = {
    "owner": "ShR",
    "custom_key_1": "custom_value_1",
    "custom_key_2": "custom_value_2"
}

# TODO print context attributes and pass them to operators in different ways
with DAG(
        dag_id="01_print_context",
        description="Print dag's context",
        start_date=days_ago(2),
        schedule_interval="@daily",
        # default_args=default_args,
        user_defined_macros=default_args,
) as dag:
    def _print_context(**context):
        print("Inside the '_print_context' function")
        print(context)

        print("custom_key_1" + " " + str(context['templates_dict']["custom_key_1"]))
        print("custom_key_2" + " " + str(context['templates_dict']["custom_key_2"]))


    print_context = PythonOperator(
        task_id="print_context",
        python_callable=_print_context,
        templates_dict=default_args,
        provide_context=True,
        dag=dag
    )

    templates_jinja_dict = {  # thanks to user_defined_macros parameter in DAG
        "custom_key_1": "{{ custom_key_1 }}",
        "custom_key_2": "{{ custom_key_2 }}"
    }

    print_context_jinja = PythonOperator(
        task_id="print_context_jinja",
        python_callable=_print_context,
        templates_dict=templates_jinja_dict,
        provide_context=True,
        dag=dag,
    )

    print_context
    print_context_jinja
