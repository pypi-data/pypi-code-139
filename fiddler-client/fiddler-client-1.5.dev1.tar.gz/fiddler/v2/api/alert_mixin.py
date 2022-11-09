from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from pydantic import parse_obj_as

from fiddler.libs.http_client import RequestClient
from fiddler.utils import logging
from fiddler.v2.constants import BINSIZE_2_SECONDS, COMPARE_PERIOD_2_SECONDS
from fiddler.v2.schema.alert import AlertRule, AlertRulePayload, TriggeredAlerts
from fiddler.v2.utils.exceptions import handle_api_error_response
from fiddler.v2.utils.response_handler import (
    APIResponseHandler,
    PaginatedResponseHandler,
)

logger = logging.getLogger(__name__)


class AlertMixin:
    client: RequestClient
    organization_name: str

    @handle_api_error_response
    def add_alert_rule(
        self,
        name: str,
        project_name: str,
        model_name: str,
        alert_type: str,
        metric: str,
        compare_to: str,
        priority: str,
        critical_threshold: float,
        condition: str,
        bin_size: str = '1 day',
        compare_period: Optional[str] = None,
        column: Optional[str] = None,
        warning_threshold: Optional[float] = None,
        notifications_config: Optional[Dict[str, Dict[str, Any]]] = None,
    ) -> AlertRule:
        """
        To add an alert rule
        :param project_name: Unique project name for which the alert rule is created
        :param model_name: Unique model name for which the alert rule is created
        :param name: Name of the Alert rule
        :param alert_type: Selects one of the four metric types:
                1) performance
                2) data_drift
                3) data_integrity
                4) service_metrics


        :param metric: "metric":
                For service_metrics:
                1) Traffic

                For performance:
                1)  For binary_classfication:
                        a) accuracy b) tpr c) fpr d) precision e) recall
                        f) f1_score g) expected_callibration_error h) auc
                2)  For Regression:
                        a) r2 b) mse c) mae d) mape e) wmape
                3)  For Multi-class:
                        a) accuracy b) log_loss
                4) For Ranking:
                        a) map b) mean_ndcg

                For drift:
                    1) psi
                    2) jsd

                For data_integrity:
                    1) range_violation
                    2) missing_values
                    3) type_violation
        :param bin_size: bin_size
                Possible Values:
                    1) 5 minutes(not for drift)
                    2) 1 hour,
                    3) 1 day,
                    4) 7 days
        :param compare_to: Select from the two:
                1) raw_value
                2) time_period
        :param compare_period: Comparing with a previous time time period. Possible values:
                1) 1 day
                2) 7 days
                3) 30 days
                4) 90 days
        :param priority: To set the priority for the alert rule. Select from:
                1) LOW
                2) MEDIUM
                3) HIGH
        :param warning_threshold: Threshold value to crossing which a warning level severity alert will be triggered
        :param critical_threshold: Threshold value to crossing which a critical level severity alert will be triggered
        :param condition: Select from:
                1) lesser
                2) greater
        :param column: column name on which alert rule is to be created. It can take '__ANY__' to check for all columns
        :param notifications_config: notifications config object created using helper method build_notifications_config()
        :return: created alert rule object
        """

        if not notifications_config:
            notifications_config = self.build_notifications_config()
        bin_size_possible_values = list(BINSIZE_2_SECONDS.keys())
        if bin_size not in bin_size_possible_values:
            raise ValueError(f'bin_size should be one of: {bin_size_possible_values}')
        elif bin_size == '5 minutes' and alert_type == 'drift':
            bin_size_possible_values.remove('5 minutes')
            raise ValueError(
                f'5 minutes bin_size not allowed for drift. Choose from: {bin_size_possible_values}'
            )
        compare_period_possible_values = list(COMPARE_PERIOD_2_SECONDS.keys())
        if compare_period and compare_period not in compare_period_possible_values:
            raise ValueError(
                f'compare_period should be one of{compare_period_possible_values}'
            )

        request_body = AlertRulePayload(
            organization_name=self.organization_name,
            project_name=project_name,
            model_name=model_name,
            name=name,
            alert_type=alert_type,
            metric=metric,
            compare_to=compare_to,
            compare_period=COMPARE_PERIOD_2_SECONDS[compare_period]
            if compare_period
            else 0,
            priority=priority.upper(),
            warning_threshold=warning_threshold,
            critical_threshold=critical_threshold,
            condition=condition,
            feature_name=column,
            time_bucket=BINSIZE_2_SECONDS[bin_size],
            notifications=notifications_config,
        ).dict()
        response = self.client.post(
            url='alert-configs',
            data=request_body,
        )
        response_data = APIResponseHandler(response)
        alert_rule_id = response_data.get_data().get('uuid')

        logger.info(f'alert config created with alert_rule_id: {alert_rule_id}')

        return AlertRule.deserialize(response_data)

    @handle_api_error_response
    def delete_alert_rule(self, alert_rule_uuid: str) -> None:
        """
        Delete an alert rule
        :param alert_rule_id: unique id for the alert rule to be deleted
        :return: the response for the delete operation
        """
        self.client.delete(url=f'alert-configs/{alert_rule_uuid}')

        logger.info(
            f'alert config with alert_rule_id: {alert_rule_uuid} deleted successfully.'
        )

    @handle_api_error_response
    def get_alert_rules(
        self,
        project_name: Optional[str] = None,
        model_name: Optional[str] = None,
        alert_type: Optional[str] = None,
        metric: Optional[str] = None,
        column: Optional[str] = None,
        ordering: Optional[List[str]] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> List[AlertRule]:

        """
        Get a list of alert rules with respect to the filtering parameters
        :param project_name: unique project name
        :param model_name: unique model name
        :param alert_type: Selects one of the four metric types:
                1) performance
                2) data_drift
                3) data_integrity
                4) service_metrics


        :param metric: "metric":
                For service_metrics:
                1) Traffic

                For performance:
                1)  For binary_classfication:
                        a) accuracy b) tpr c) fpr d) precision e) recall
                        f) f1_score g) expected_callibration_error h) auc
                2)  For Regression:
                        a) r2 b) mse c) mae d) mape e) wmape
                3)  For Multi-class:
                        a) accuracy b) log_loss
                4) For Ranking:
                        a) map b) mean_ndcg

                For drift:
                    1) psi
                    2) jsd

                For data_integrity:
                    1) range_violation
                    2) missing_values
                    3) type_violation
        :param column: Filter based on the column
        :param limit: Number of records to be retrieved per page, also referred as page_size
        :param offset: Pointer to the starting of the page index. offset of the first page is 0
                        and it increments by limit for each page, for e.g., 5th pages offset when
                        limit=100 will be (5 - 1) * 100 = 400. This means 5th page will contain
                        records from index 400 to 499.
        :return: paginated list of alert rules for the set filters
        """
        response = self.client.get(
            url='alert-configs',
            params={
                'organization_name': self.organization_name,
                'project_name': project_name,
                'model_name': model_name,
                'alert_type': alert_type,
                'metric': metric,
                'feature_name': column,
                'offset': offset,
                'limit': limit,
                'ordering': ordering,
            },
        )
        _, items = PaginatedResponseHandler(response).get_pagination_details_and_items()
        return parse_obj_as(List[AlertRule], items)

    @handle_api_error_response
    def get_triggered_alerts(
        self,
        alert_rule_uuid: str,
        start_time: datetime = datetime.now() - timedelta(days=7),
        end_time: datetime = datetime.now(),
        ordering: Optional[List[str]] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> List[TriggeredAlerts]:
        """
        To get a list of triggered alerts  for a given alert rule
        :param alert_rule_id: Unique id for the alert rule
        :param start_time: Start time to filter trigger alerts :default: 7 days ago
        :param end_time: End time to filter trigger alerts :default: time now
        :param limit: Number of records to be retrieved per page, also referred as page_size
        :param offset: Pointer to the starting of the page index. offset of the first page is 0
                        and it increments by limit for each page, for e.g., 5th pages offset when
                        limit=100 will be (5 - 1) * 100 = 400. This means 5th page will contain
                        records from index 400 to 499.
        :return: paginated list of triggered_alerts for the given alert rule
        """
        response = self.client.get(
            url=f'alert-configs/{alert_rule_uuid}/records',
            params={
                'organization_name': self.organization_name,
                'start_time': start_time,
                'end_time': end_time,
                'offset': offset,
                'limit': limit,
                'ordering': ordering,
            },
        )
        _, items = PaginatedResponseHandler(response).get_pagination_details_and_items()
        return parse_obj_as(List[TriggeredAlerts], items)

    def build_notifications_config(
        self,
        emails: str = '',
        pagerduty_services: str = '',
        pagerduty_severity: str = '',
    ) -> Dict[str, Dict[str, Any]]:
        """
        To get the notifications value to be set for alert rule
        :param emails: Comma separated emails list
        :param pagerduty_services: Comma separated pagerduty services list
        :param pagerduty severity: Severity for the alerts triggered by pagerduty
        :return: dict with emails and pagerduty dict. If left unused, will store empty string for these values
        """
        return {
            'emails': {
                'email': emails,
            },
            'pagerduty': {
                'service': pagerduty_services,
                'severity': pagerduty_severity,
            },
        }
