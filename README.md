### To start this project execute "docker_compose up" in the root directory.


### "01_" dags show basic concepts of airflow

1. "01_set_chain" is an example of chaining tasks inside the dag.
Also this dag shows how to use XCom values for purpose of communication between tasks.

2. "01_print_context" shows how airflow context works and how we can extend it.

3. "01_pass_params" shows how to pass parameters to task.

4. "01_implement_sensors" shows a use case of airflow sensor.

5. Two DAGs "01_dag_triggering" and "01_dag_trig_dependant"
Dag "01_dag_triggering is main, it calls "01_dag_trig_dependant".
Dag "01_dag_trig_dependant" depend on DAG "01_dag_triggering".

Don't forget to create "fs_conn_id" connection at Admin panel for "FileSensor".

6. "01_external_task_sensor" show operator "ExternalTeskSensor" for communication between DAGs.
The ExternalTaskSensor checks for a successful state of a task with the exact same execution date as itself. 
So, if an ExternalTaskSensor runs with an execution date of 2022-11-05T18:00:00, it would query the Airflow metastore for the given task, also with an execution date of 2022-11-05T18:00:00. 
Now let’s say both DAGs have a different schedule interval; then these would not align and thus the ExternalTaskSensor would never find the corresponding task!
The offset is controlled by the "execution_delta argument" on the "ExternalTaskSensor".


### "02_" task more difficult and contain "real" work examples, which you can meet at job.

1. "02_rocket_launches"

2. "02_wikipedia_pageview"

3. "02_calc_events"
Don't forget to create "postgres_db" connection to postgesql at Admin panel.

4. 


### Triggering DAGs is possible from outside Airflow with the REST API and/or CLI
### Connect to db through CLI: psql -U postgres postgres or psql -U airflow -W airflow