from pydantic import BaseModel


class MarketQueryInput(BaseModel):
    text: str


class MarketQueryOutput(BaseModel):
    output: str
    intermediate_steps: list[str]
