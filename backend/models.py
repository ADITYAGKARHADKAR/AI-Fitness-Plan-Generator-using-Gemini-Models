# from pydantic import BaseModel, Field, validator
# from typing import Optional


# # ─────────────────────────────────────────────
# # REQUEST MODELS
# # ─────────────────────────────────────────────

# class UserProfileRequest(BaseModel):
#     """Model for user profile input to generate a workout plan."""
#     name: str = Field(..., min_length=1, max_length=100, description="User's full name")
#     age: int = Field(..., ge=10, le=100, description="User's age (10-100)")
#     weight: float = Field(..., gt=0, le=500, description="User's weight in kg")
#     goal: str = Field(..., description="Fitness goal: weight_loss, muscle_gain, general_wellness")
#     intensity: str = Field(..., description="Workout intensity: low, medium, high")

#     @validator("goal")
#     def validate_goal(cls, v):
#         allowed = ["weight_loss", "muscle_gain", "general_wellness"]
#         if v.lower() not in allowed:
#             raise ValueError(f"Goal must be one of: {', '.join(allowed)}")
#         return v.lower()

#     @validator("intensity")
#     def validate_intensity(cls, v):
#         allowed = ["low", "medium", "high"]
#         if v.lower() not in allowed:
#             raise ValueError(f"Intensity must be one of: {', '.join(allowed)}")
#         return v.lower()


# class FeedbackRequest(BaseModel):
#     """Model for submitting feedback to refine an existing plan."""
#     user_id: int = Field(..., gt=0, description="ID of the user")
#     plan_id: int = Field(..., gt=0, description="ID of the plan to update")
#     feedback: str = Field(..., min_length=5, max_length=500, description="User feedback text")


# class NutritionTipRequest(BaseModel):
#     """Model for requesting a nutrition or recovery tip."""
#     goal: str = Field(..., description="Fitness goal: weight_loss, muscle_gain, general_wellness")

#     @validator("goal")
#     def validate_goal(cls, v):
#         allowed = ["weight_loss", "muscle_gain", "general_wellness"]
#         if v.lower() not in allowed:
#             raise ValueError(f"Goal must be one of: {', '.join(allowed)}")
#         return v.lower()


# # ─────────────────────────────────────────────
# # RESPONSE MODELS
# # ─────────────────────────────────────────────

# class PlanResponse(BaseModel):
#     """Response model for a generated or updated workout plan."""
#     success: bool
#     user_id: int
#     plan_id: int
#     workout_plan: str
#     nutrition_tip: Optional[str] = None
#     message: str


# class NutritionTipResponse(BaseModel):
#     """Response model for a nutrition or recovery tip."""
#     success: bool
#     goal: str
#     tip: str


# class ErrorResponse(BaseModel):
#     """Generic error response model."""
#     success: bool = False
#     error: str
#     detail: Optional[str] = None

from pydantic import BaseModel, Field, validator
from typing import Optional


# ─────────────────────────────────────────────
# REQUEST MODELS
# ─────────────────────────────────────────────

class UserProfileRequest(BaseModel):
    """Model for user profile input to generate a workout plan."""
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    age: int = Field(..., ge=10, le=100, description="User's age (10-100)")
    weight: float = Field(..., gt=0, le=500, description="User's weight in kg")
    goal: str = Field(..., description="Fitness goal: weight_loss, muscle_gain, general_wellness")
    intensity: str = Field(..., description="Workout intensity: low, medium, high")

    @validator("goal")
    def validate_goal(cls, v):
        allowed = ["weight_loss", "muscle_gain", "general_wellness"]
        if v.lower() not in allowed:
            raise ValueError(f"Goal must be one of: {', '.join(allowed)}")
        return v.lower()

    @validator("intensity")
    def validate_intensity(cls, v):
        allowed = ["low", "medium", "high"]
        if v.lower() not in allowed:
            raise ValueError(f"Intensity must be one of: {', '.join(allowed)}")
        return v.lower()


class FeedbackRequest(BaseModel):
    """Model for submitting feedback to refine an existing plan."""
    user_id: int = Field(..., gt=0, description="ID of the user")
    plan_id: int = Field(..., gt=0, description="ID of the plan to update")
    feedback: str = Field(..., min_length=5, max_length=500, description="User feedback text")


class NutritionTipRequest(BaseModel):
    """Model for requesting a nutrition or recovery tip."""
    goal: str = Field(..., description="Fitness goal: weight_loss, muscle_gain, general_wellness")

    @validator("goal")
    def validate_goal(cls, v):
        allowed = ["weight_loss", "muscle_gain", "general_wellness"]
        if v.lower() not in allowed:
            raise ValueError(f"Goal must be one of: {', '.join(allowed)}")
        return v.lower()


# ─────────────────────────────────────────────
# RESPONSE MODELS
# ─────────────────────────────────────────────

class PlanResponse(BaseModel):
    """Response model for a generated or updated workout plan."""
    success: bool
    user_id: int
    plan_id: int
    workout_plan: str
    nutrition_tip: Optional[str] = None
    message: str


class NutritionTipResponse(BaseModel):
    """Response model for a nutrition or recovery tip."""
    success: bool
    goal: str
    tip: str


class ErrorResponse(BaseModel):
    """Generic error response model."""
    success: bool = False
    error: str
    detail: Optional[str] = None