from pydantic import BaseModel

class CoverageRequest(BaseModel):
    frequency: int
    tx_power: int
    antenna_height: float
