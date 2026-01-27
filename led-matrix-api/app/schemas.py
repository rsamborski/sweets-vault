from pydantic import BaseModel, Field

class SectionSchema(BaseModel):
    char: str = Field(..., min_length=1, max_length=1, description="Single character to display")
    locked: bool = Field(..., description="Locked status (True=Red Lock, False=Green Unlock)")
