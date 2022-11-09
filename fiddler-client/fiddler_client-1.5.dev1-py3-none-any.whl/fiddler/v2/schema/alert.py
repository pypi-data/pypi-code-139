from typing import Any, Dict, Optional

from pydantic import Field

from fiddler.v2.schema.base import BaseDataSchema


class AlertRulePayload(BaseDataSchema):
    organization_name: str
    project_name: str
    model_name: str
    name: str
    alert_type: str
    metric: str
    feature_name: Optional[str]
    priority: str
    compare_to: str
    compare_period: Optional[int]
    warning_threshold: Optional[float]
    critical_threshold: float
    condition: str
    time_bucket: int
    notifications: Optional[Dict[str, Dict[str, Any]]]


class AlertRule(BaseDataSchema):
    alert_rule_uuid: str = Field(alias='uuid')
    organization_name: str
    project_id: str = Field(alias='project_name')
    model_id: str = Field(alias='model_name')
    name: Optional[str]
    alert_type: str
    metric: str
    column: str = Field(alias='feature_name')
    priority: str
    compare_to: str
    compare_period: Optional[int]
    compare_threshold: Optional[int]
    raw_threshold: Optional[int]
    warning_threshold: Optional[float]
    critical_threshold: float
    condition: str
    bin_size: int = Field(alias='time_bucket')


class TriggeredAlerts(BaseDataSchema):
    id: int
    triggered_alert_id: str = Field(alias='uuid')
    alert_rule_uuid: str = Field(alias='alert_config_uuid')
    alert_run_start_time: int
    alert_time_bucket: int
    alert_value: float
    baseline_time_bucket: Optional[int]
    baseline_value: Optional[float]
    is_alert: bool
    severity: Optional[str]
    failure_reason: str
    message: str
