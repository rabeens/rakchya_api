from pydantic import BaseModel

class Invoice(BaseModel):
    doc: str 
    category: str
    token: str = ""