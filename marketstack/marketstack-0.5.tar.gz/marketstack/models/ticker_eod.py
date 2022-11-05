from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.eod_price import EodPrice
from ..models.exchange import Exchange
from ..models.timezone import Timezone
from ..types import UNSET, Unset

T = TypeVar("T", bound="TickerEod")


@attr.s(auto_attribs=True)
class TickerEod:
    """
    Attributes:
        name (str):
        symbol (str):
        has_intraday (bool):
        has_eod (bool):
        eod (List[EodPrice]):
        stock_exchange (Union[Unset, Exchange]):
        timezone (Union[Unset, Timezone]):
    """

    name: str
    symbol: str
    has_intraday: bool
    has_eod: bool
    eod: List[EodPrice]
    stock_exchange: Union[Unset, Exchange] = UNSET
    timezone: Union[Unset, Timezone] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        symbol = self.symbol
        has_intraday = self.has_intraday
        has_eod = self.has_eod
        eod = []
        for eod_item_data in self.eod:
            eod_item = eod_item_data.to_dict()

            eod.append(eod_item)

        stock_exchange: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.stock_exchange, Unset):
            stock_exchange = self.stock_exchange.to_dict()

        timezone: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.timezone, Unset):
            timezone = self.timezone.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "symbol": symbol,
                "has_intraday": has_intraday,
                "has_eod": has_eod,
                "eod": eod,
            }
        )
        if stock_exchange is not UNSET:
            field_dict["stock_exchange"] = stock_exchange
        if timezone is not UNSET:
            field_dict["timezone"] = timezone

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        symbol = d.pop("symbol")

        has_intraday = d.pop("has_intraday")

        has_eod = d.pop("has_eod")

        eod = []
        _eod = d.pop("eod")
        for eod_item_data in _eod:
            eod_item = EodPrice.from_dict(eod_item_data)

            eod.append(eod_item)

        _stock_exchange = d.pop("stock_exchange", UNSET)
        stock_exchange: Union[Unset, Exchange]
        if isinstance(_stock_exchange, Unset):
            stock_exchange = UNSET
        else:
            stock_exchange = Exchange.from_dict(_stock_exchange)

        _timezone = d.pop("timezone", UNSET)
        timezone: Union[Unset, Timezone]
        if isinstance(_timezone, Unset):
            timezone = UNSET
        else:
            timezone = Timezone.from_dict(_timezone)

        ticker_eod = cls(
            name=name,
            symbol=symbol,
            has_intraday=has_intraday,
            has_eod=has_eod,
            eod=eod,
            stock_exchange=stock_exchange,
            timezone=timezone,
        )

        ticker_eod.additional_properties = d
        return ticker_eod

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
