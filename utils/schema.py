from pydantic import BaseModel, Field
from typing import Annotated

# schema for prediction data validation
class InputData(BaseModel):
    brand: Annotated[str, Field(...,description='Enter the brand name of car')]
    weight: Annotated[str, Field(..., description='Enter the range of weight of the car')]
    displacement: Annotated[float, Field(..., description='Displacement of the engine', lt=461, gt=59)]
    horsepower: Annotated[float, Field(..., description='Horsepower of engine',gt=39,lt=241)]
    cylinders: Annotated[int, Field(..., description='Number of cylinders in the car', gt=2,lt=9)]
    acceleration: Annotated[float, Field(..., description='Amount of acceleration car produces',gt=5,lt=7)]
    year: Annotated[int, Field(..., description='What is the manufacturing year of the car')]
    origin: Annotated[int, Field(..., description='Which of the car is')]

# Pydantic schema for incoming validation requests
class TokenVerificationRequest(BaseModel):
    token: str