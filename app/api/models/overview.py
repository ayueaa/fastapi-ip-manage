from pydantic import Field
from app.api.models.rwmodel import CustomModel


class OverviewResponse(CustomModel):
    total: int
    increase_today: int
    increase_7day: int


class CountGroupResponse(CustomModel):
    date: str = Field(..., example="20231107")
    count: int = Field(..., example=123)
