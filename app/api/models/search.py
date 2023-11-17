import ipaddress
from datetime import datetime
from typing import List, Union

from pydantic import Field, validator

from app.api.models.rwmodel import CustomModel


class SearchItem(CustomModel):
    ip: Union[ipaddress.IPv4Address, ipaddress.IPv6Address]


class SearchVisableResponse(SearchItem):
    first_seen: datetime
    last_seen: datetime
    raw_tags: List[str]

    @validator("first_seen", "last_seen", pre=True)
    def timestamp_to_datetime(cls, value):
        if isinstance(value, int):
            return datetime.fromtimestamp(value)
        return value


class IPExtrInfo(CustomModel):
    country: str
    countryCode: str
    region: str
    regionName: str
    city: str
    zip_field: str = Field(..., alias="zip")
    lat: float
    lon: float
    timezone: str
    isp: str
    org: str
    as_field: str = Field(..., alias="as")


class SearchHistoryResponse(SearchItem):
    source: str
    last_seen: datetime
    raw_tags: List[str]

    @validator("last_seen", pre=True)
    def timestamp_to_datetime(cls, value):
        if isinstance(value, int):
            return datetime.fromtimestamp(value)
        return value


class SearchResponse(CustomModel):
    visable: SearchVisableResponse
    history: List[SearchHistoryResponse] = []
    extro: IPExtrInfo = {}
