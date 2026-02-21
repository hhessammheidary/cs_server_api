from pydantic import BaseModel
from typing import Optional

class ServerInstanceOut(BaseModel):
    server_name: Optional[str] = None
    ip: str
    port: int
    mod: str
    players_current: Optional[int] = None
    players_max: Optional[int] = None
    online: bool
