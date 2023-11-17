from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict


def convert_datetime_to_gmt(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.strftime("%Y-%m-%d %H:%M:%S")


def convert_datetime_to_realworld(dt: datetime) -> str:
    return dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")


class CustomModel(BaseModel):
    model_config = ConfigDict(
        json_encoders={datetime: convert_datetime_to_gmt, ObjectId: str},
        populate_by_name=True,
        allow_population_by_field_name=True,
    )

    def serializable_dict(self, **kwargs):
        """Return a dict which contains only serializable fields."""
        default_dict = self.model_dump()

        return jsonable_encoder(default_dict)
