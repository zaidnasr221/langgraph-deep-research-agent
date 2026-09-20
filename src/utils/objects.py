from pydantic import BaseModel , Field
from typing import List

class Analyst(BaseModel):
    affiliation: str = Field(..., description="Primary affiliation of the analyst.")
    name: str = Field(..., description="Name of the analyst.")
    role: str = Field(..., description="Role of the analyst in the context of the research topic.")
    description: str = Field(..., description="Description of the analyst's focus, concerns, and motives.")
    
    @property
    def persona(self) -> str:
        """
        Returns a persona string that combines the analyst's name, role, and affiliation.
        """
        return f"{self.name}\n{self.role}\n{self.affiliation}\n{self.description}"

class Perspectives(BaseModel):
    analysts: List[Analyst] = Field(..., description="Comprehensive list of analysts with their roles and affiliations.")
    
    