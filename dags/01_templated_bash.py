from datetime import timedelta
from textwrap import dedent

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

with DAG(
        dag_id='01_templated_bash',
        description='Figuring out with bash operator',
        start_date=days_ago(0, minute=10),
        schedule_interval=timedelta(minutes=1)
) as dag:

    templated_command = dedent(
        """
            {% for i in range(5) %}
                echo "{{ ds }}"
                echo "{{ macros.ds_add(ds, 7)}}"
                echo "{{ params.my_param }}"
            {% endfor %}
        """
    )

    t4 = BashOperator(
        task_id='templated',
        depends_on_past=False,
        bash_command=templated_command,
        params={'my_param': 'Parameter I passed in'},
    )

    dag.doc_md = __doc__

    t1.doc_md = dedent(
        """
            #### Task Documentation
            You can document your task using the attributes `doc_md` (markdown),
            `doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
            rendered in the UI's Task Instance Details page.

            ![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)
        """
    )

    t1 >> t2
    t1 >> t3 >> t4
