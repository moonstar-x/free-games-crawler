import json
from typing import Literal, Union, Optional
from dataclasses import dataclass
from pkg.interfaces.json_serializable import JsonSerializable


OfferType = Union[Literal['game'], Literal['dlc'], Literal['bundle'], Literal['other']]


@dataclass
class Offer(JsonSerializable):
    storefront: str
    url: str

    title: str
    description: str
    type: OfferType

    publisher: Optional[str]
    original_price: Optional[float]
    original_price_fmt: Optional[str]

    thumbnail: Optional[str]

    def to_json(self) -> str:
        return json.dumps(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
