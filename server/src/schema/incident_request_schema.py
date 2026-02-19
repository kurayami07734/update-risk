from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class IncidentFetchRequest(BaseModel):
    package_name: List[str] = Field(..., min_items=1)
    from_date: Optional[datetime] = None
