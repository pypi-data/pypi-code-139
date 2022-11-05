from typing import Any, Dict, List, Type, TypeVar

from pydantic import BaseModel, Field

from ..models.record_day_boolean_or_undefined import RecordDayBooleanOrUndefined
from ..types import UNSET

T = TypeVar("T", bound="VisualCronScheduleExpressionsItem")


class VisualCronScheduleExpressionsItem(BaseModel):
    """
    Attributes:
        days (RecordDayBooleanOrUndefined): Construct a type with a set of properties K of type T
        time (str):
    """

    days: RecordDayBooleanOrUndefined = None
    time: str = None
    additional_properties: Dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        days = self.days.to_dict()

        time = self.time

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "days": days,
                "time": time,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        if src_dict is None or src_dict is UNSET:
            return {}
        d = {k: v if v is not None else UNSET for k, v in src_dict.items()}
        days = RecordDayBooleanOrUndefined.from_dict(d.pop("days"))

        time = d.pop("time")

        visual_cron_schedule_expressions_item = cls(
            days=days,
            time=time,
        )

        visual_cron_schedule_expressions_item.additional_properties = d
        return visual_cron_schedule_expressions_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
