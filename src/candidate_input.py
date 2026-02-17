from typing import Literal, Optional, Self

from pydantic import BaseModel, Field, HttpUrl, model_validator


class Candidate(BaseModel):
    currently_employed: bool = Field(
        ..., description="Whether the candidate is currently working"
    )
    current_company: Optional[str] = Field(
        description="The name of the candidate's current employer",
        examples=["Google", "Amazon"],
    )
    current_role: Optional[str] = Field(description="Current job title")
    current_job_tenure: Optional[float] = Field(
        ge=0, description="Number of years in the current position"
    )
    risk_tolerance: Literal[1, 2, 3, 4, 5] = Field(
        ..., description="Scale of 1 (low) to 5 (high) for risk appetite"
    )
    career_stage: Literal["early", "mid", "senior"] = Field(
        ..., description="The candidate's current professional seniority level"
    )
    career_priority: Literal["compensation", "stability"] = Field(
        ..., description="The primary driver for the candidate's next move"
    )

    @model_validator(mode="after")
    def check_employment_details(self) -> Self:
        if self.currently_employed and not all(
            [self.current_company, self.current_role, self.current_job_tenure]
        ):
            raise ValueError(
                "Encountered Error: Incomplete employment details, complete current_company, current_role and current_job_tenure"
            )
        if not self.currently_employed:
            self.current_company = None
            self.current_role = None
            self.current_job_tenure = None
        return self


class TargetCompany(BaseModel):
    company_name: str = Field(
        ..., min_length=1, description="The legal name of the target organization"
    )
    job_posting: HttpUrl = Field(
        ..., description="A valid URL to the specific job listing"
    )
