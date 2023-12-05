import ipaddress
from datetime import datetime
import re
from typing import Dict, List, Union

from pydantic import BaseModel, Field, validator

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


class VtIPParams(BaseModel):
    ioc: str

    @validator("ioc")
    def valid_ip(cls, ioc):
        ioc = ioc.strip()
        domain_pattern = re.compile(
            r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$'
        )
        if domain_pattern.match(ioc) or cls.is_valid_ip(ioc):
            return ioc
        raise ValueError("input must be a valid IP address or domain")

    @classmethod
    def is_valid_ip(cls, value):
        try:
            ipaddress.ip_address(value)
            return True
        except ValueError:
            return False


class VtIPAnalysis(CustomModel):
    category: str
    result: str
    method: str
    engine_name: str


class VtSearchIPAttributes(CustomModel):
    network: str
    tags: List[str]
    whois: str
    whois_date: int
    last_analysis_date: int
    asn: int
    as_owner: str
    last_analysis_stats: Dict[str, int]
    last_analysis_results: Dict[str, VtIPAnalysis]


class VtSearchResponse(CustomModel):
    ioc: str
    ioc_type: str
    attributes: VtSearchIPAttributes
