from datetime import datetime, timezone
from typing import Any
from zoneinfo import ZoneInfo
from bson import ObjectId

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict, model_validator


def convert_datetime_to_gmt(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


def convert_datetime_to_realworld(dt: datetime) -> str:
    return dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")


class CustomModel(BaseModel):
    model_config = ConfigDict(
        json_encoders={datetime: convert_datetime_to_gmt, ObjectId: str},
        populate_by_name=True,
        # alias_generator=convert_datetime_to_realworld
    )

    @model_validator(mode="before")
    @classmethod
    def set_null_microseconds(cls, data: dict[str, Any]) -> dict[str, Any]:
        datetime_fields = {
            k: v.replace(microsecond=0)
            for k, v in data.items()
            if isinstance(k, datetime)
        }

        return {**data, **datetime_fields}

    def serializable_dict(self, **kwargs):
        """Return a dict which contains only serializable fields."""
        default_dict = self.model_dump()

        return jsonable_encoder(default_dict)
