from pydantic import BaseModel, field_validator, model_validator
from typing import Literal

# Pydantic Schema with Custom Validators
class UserInput(BaseModel):
    # Categorical
    country: str
    job_role: str
    ai_specialization: str
    industry: str
    work_mode: Literal["Remote", "Hybrid", "On-site"]
    education_required: str
 
    # Ordinal
    experience_level: Literal["Entry", "Mid", "Senior", "Lead"]
    company_size: Literal["Startup", "Small", "Medium", "Large", "Enterprise"]
 
    # Numerical 
    weekly_hours: float
    hiring_difficulty_score: float
    ai_adoption_score: float
    economic_index: float
    offer_acceptance_rate: float
    tax_rate_percent: float
    skill_demand_score: float
    automation_risk: float
    job_security_score: float
    career_growth_score: float
    work_life_balance_score: float
    promotion_speed: float
    salary_percentile: float
    employee_satisfaction: float
    bonus_usd: float
    
    # String validators
    @field_validator("country", "job_role", "ai_specialization", "industry", "education_required")
    @classmethod
    def not_empty_string(cls, value: str, info) -> str:
        value = value.strip()
        if not value:
            raise ValueError(f"{info.field_name} must not be empty or whitespace.")
        if len(value) < 2:
            raise ValueError(f"{info.field_name} must be at least 2 characters.")
        if len(value) > 100:
            raise ValueError(f"{info.field_name} must be at most 100 characters.")
        return value
    
    # Weekly hours
    @field_validator("weekly_hours")
    @classmethod
    def validate_weekly_hours(cls, value: float) -> float:
        if not (1 <= value <= 168):
            raise ValueError("weekly_hours must be between 1 and 168.")
        return round(value, 2)
    
    # Score Fields 
    @field_validator("hiring_difficulty_score", "ai_adoption_score", "offer_acceptance_rate", "tax_rate_percent", "skill_demand_score", "automation_risk", "job_security_score", "career_growth_score", "work_life_balance_score", "promotion_speed", "salary_percentile", "employee_satisfaction")
    @classmethod
    def validate_zero_to_hundred(cls, value: float, info) -> float:
        if not (0.0 <= value <= 100.0):
            raise ValueError(f"{info.field_name} must be between 0 and 100.")
        return round(value, 4)
    
    # Economic index
    @field_validator("economic_index")
    @classmethod
    def validate_economic_index(cls, value: float) -> float:
        if not (-100.0 <= value <= 100.0):
            raise ValueError("economic_index must be between -100 and 100.")
        return round(value, 4)
    
    # Bonus
    @field_validator("bonus_usd")
    @classmethod
    def validate_bonus(cls, value: float) -> float:
        if value < 0:
            raise ValueError("bonus_usd must be non-negative.")
        if value > 10000000:
            raise ValueError("bonus_usd seems unrealistically high (> $10,000,000).")
        return round(value, 2)
    
    # Cross field
    @model_validator(mode="after")
    def cross_field_sanity(self):
        if self.experience_level in ("Senior", "Lead") and self.offer_acceptance_rate == 0:
            raise ValueError(
                "offer_acceptance_rate of 0 is implausible for Senior/Lead roles."
            )
        return self