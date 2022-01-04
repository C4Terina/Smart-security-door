from pydantic import BaseModel
from datetime import datetime

class Data(BaseModel):
    entry_id: int
    camera_id: int
    person_id: int
    person_name: str
    time_recognised: datetime

    class Config:
        orm_mode = True
