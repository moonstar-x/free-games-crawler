import json
from dataclasses import dataclass
from pkg.interfaces.json_serializable import JsonSerializable


@dataclass
class Offer(JsonSerializable):
    storefront: str

    def to_json(self) -> str:
        return json.dumps(self.__dict__)
