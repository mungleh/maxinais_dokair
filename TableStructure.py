from typing import Optional
from pydantic import BaseModel

#struture table inputs
class bddinputs(BaseModel):
    input: Optional[str]
    prediction : Optional[str]
    probabilité : Optional[float]
