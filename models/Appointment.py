from pydantic import BaseModel

class Appointment(BaseModel):
    doc_id: int
    symptom_id: int