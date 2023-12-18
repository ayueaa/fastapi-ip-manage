import ipaddress
import re
from typing import Any, Dict, Optional

import requests

from app.api.models.search import VtSearchResponse

virustotal_api_key = "b78bfd6ad30746179616bca7690fee2e6ef230d9e297ff202457a0a34b7534ca"

ip = "216.73.161.242"


class VtClient:
    BASE_URL = "https://www.virustotal.com/api/v3/"

    def __init__(self, api_key: str):
        self.api_key: str = api_key
        self.headers: Dict[str, str] = {"x-apikey": self.api_key}

    def _make_request(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> VtSearchResponse:
        """执行请求的通用方法"""
        url: str = f"{self.BASE_URL}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        data = response.json().get("data") or {}
        return {
            "ioc": data.get("id"),
            "ioc_type": data.get("type"),
            "attributes": data.get("attributes"),
        }

    def get_ip_report(self, ip: str) -> VtSearchResponse:
        """查询指定 IP 的报告"""
        endpoint: str = f"ip_addresses/{ip}"
        return self._make_request(endpoint)

    def get_domain_report(self, domain: str) -> VtSearchResponse:
        """查询指定域名的报告"""
        endpoint: str = f"domains/{domain}"
        return self._make_request(endpoint)

    def auto_search(self, ioc: str) -> VtSearchResponse:
        ioc = ioc.strip()
        pattern = re.compile(
            r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$"
        )
        if pattern.match(ioc):
            return self.get_domain_report(ioc)

        try:
            ipaddress.ip_address(ioc)
        except ValueError:
            raise ValueError("input must be ip or domain")
        else:
            return self.get_ip_report(ioc)


if __name__ == "__main__":
    client = VtClient(api_key=virustotal_api_key)
    res = client.auto_search("www.baidu.com")
    print(res)
