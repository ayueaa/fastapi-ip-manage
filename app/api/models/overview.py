from app.api.models.rwmodel import CustomModel


class OverviewResponse(CustomModel):
    total: int
    increase_today: int
    increase_7day: int
