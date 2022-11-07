import datetime

from airflow.operators.python import PythonOperator
from airflow.utils.session import provide_session, NEW_SESSION
from airflow.api.common.experimental.mark_tasks import set_dag_run_state_to_success, set_dag_run_state_to_failed
from airflow.api.common.experimental import check_and_get_dag

from datamorphairflow import utils


class DMMarkDagSuccess(PythonOperator):
    """
    Operator to set DAG run state to Success.
    **
    Dag should be triggered with the following config:
    {
      "external_dag_id":"workflow1",
      "start_date":"2022-11-07 19:20:35.106944"
    }
    """

    def __init__(
            self,
            *args,
            **kwargs
    ):
        super().__init__(python_callable=mark_dag_success,
                         provide_context=True, *args, **kwargs)


def mark_dag_success(**context):
    external_dag_id = context["dag_run"].conf["external_dag_id"]
    start_date = context["dag_run"].conf["start_date"]
    set_dag_runs_state_to_success(dag_id=external_dag_id, start_date=start_date)


@provide_session
def set_dag_runs_state_to_success(
        dag_id: str,
        start_date: str,
        session=NEW_SESSION
) -> None:
    dag = check_and_get_dag(dag_id=dag_id)
    execution_date = utils.get_datetime(date_value=start_date)
    set_dag_run_state_to_success(dag, execution_date, commit=True)

class DMMarkDagFailed(PythonOperator):
    """
    Operator to set DAG run state to Failed.
    """

    def __init__(
            self,
            *args,
            **kwargs
    ):
        super().__init__(python_callable=mark_dag_failed,
                         provide_context=True, *args, **kwargs)


def mark_dag_failed(**context):
    external_dag_id = context["dag_run"].conf["external_dag_id"]
    start_date = context["dag_run"].conf["start_date"]
    set_dag_runs_state_to_failed(dag_id=external_dag_id, start_date=start_date)


@provide_session
def set_dag_runs_state_to_failed(
        dag_id: str,
        start_date: str,
        session=NEW_SESSION
) -> None:
    dag = check_and_get_dag(dag_id=dag_id)
    execution_date = utils.get_datetime(date_value=start_date)
    set_dag_run_state_to_failed(dag, execution_date, commit=True)
