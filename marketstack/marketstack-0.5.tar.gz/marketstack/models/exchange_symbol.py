from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="ExchangeSymbol")


@attr.s(auto_attribs=True)
class ExchangeSymbol:
    """
    Attributes:
        name (str):
        symbol (str):
        has_intraday (bool):
        has_eod (bool):
    """

    name: str
    symbol: str
    has_intraday: bool
    has_eod: bool
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        symbol = self.symbol
        has_intraday = self.has_intraday
        has_eod = self.has_eod

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "symbol": symbol,
                "has_intraday": has_intraday,
                "has_eod": has_eod,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        symbol = d.pop("symbol")

        has_intraday = d.pop("has_intraday")

        has_eod = d.pop("has_eod")

        exchange_symbol = cls(
            name=name,
            symbol=symbol,
            has_intraday=has_intraday,
            has_eod=has_eod,
        )

        exchange_symbol.additional_properties = d
        return exchange_symbol

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
