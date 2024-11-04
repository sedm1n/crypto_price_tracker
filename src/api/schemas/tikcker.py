from pydantic import BaseModel, constr, field_validator

class TickerSchema(BaseModel):
    name: str = constr(min_length=1, strip_whitespace=True)

    @field_validator('name')
    def validate_name(cls, value):
        if not value.strip():  
            raise ValueError('Ticker name must not be empty or whitespace')
        return value