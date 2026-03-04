from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import logging
import os

from backend.models import (
    UserProfileRequest,
    FeedbackRequest,
    NutritionTipRequest,
    PlanResponse,
    NutritionTipResponse,
    ErrorResponse
)
from backend.database import (
    initialize_database,
    insert_user,
    get_user,
    insert_plan,
    get_plan_by_user,
    update_plan
)
from backend.gemini_service import (
    generate_workout_plan,
    refine_workout_plan,
    generate_nutrition_tip
)

# ─────────────────────────────────────────────
# LOGGING SETUP
# ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# APP INITIALIZATION
# ─────────────────────────────────────────────
app = FastAPI(
    title="FitBuddy API",
    description="AI-powered personalized fitness plan generator using Gemini",
    version="1.0.0"
)

# ─────────────────────────────────────────────
# CORS MIDDLEWARE
# ─────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# SERVE FRONTEND
# ─────────────────────────────────────────────
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/", response_class=FileResponse)
def serve_frontend():
    return "frontend/index.html"

# ─────────────────────────────────────────────
# STARTUP EVENT — Initialize DB
# ─────────────────────────────────────────────
@app.on_event("startup")
def startup_event():
    os.makedirs("database", exist_ok=True)
    initialize_database()
    logger.info("🚀 FitBuddy API started successfully!")


# ─────────────────────────────────────────────
# HEALTH CHECK
# ─────────────────────────────────────────────
@app.get("/health")
def health_check():
    return {"status": "✅ FitBuddy API is running!", "version": "1.0.0"}


# ─────────────────────────────────────────────
# ENDPOINT 1: Generate Workout Plan (Scenario 1)
# ─────────────────────────────────────────────
@app.post("/generate-plan", response_model=PlanResponse)
def generate_plan(user: UserProfileRequest):
    """
    Takes user profile details and generates a personalized 7-day workout plan.
    Stores the user and plan in the database.
    """
    try:
        logger.info(f"📥 Received plan generation request for: {user.name}")

        # Step 1: Save user to DB
        user_id = insert_user(
            name=user.name,
            age=user.age,
            weight=user.weight,
            goal=user.goal,
            intensity=user.intensity
        )

        # Step 2: Generate plan via Gemini
        workout_plan = generate_workout_plan(
            name=user.name,
            age=user.age,
            weight=user.weight,
            goal=user.goal,
            intensity=user.intensity
        )

        # Step 3: Generate nutrition tip alongside
        nutrition_tip = generate_nutrition_tip(goal=user.goal)

        # Step 4: Save plan to DB
        plan_id = insert_plan(
            user_id=user_id,
            workout_plan=workout_plan,
            nutrition_tip=nutrition_tip
        )

        logger.info(f"✅ Plan generated and stored. User ID: {user_id}, Plan ID: {plan_id}")

        return PlanResponse(
            success=True,
            user_id=user_id,
            plan_id=plan_id,
            workout_plan=workout_plan,
            nutrition_tip=nutrition_tip,
            message="Your personalized 7-day workout plan has been generated successfully!"
        )

    except Exception as e:
        logger.error(f"❌ Error in /generate-plan: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────
# ENDPOINT 2: Refine Plan via Feedback (Scenario 2)
# ─────────────────────────────────────────────
@app.post("/feedback", response_model=PlanResponse)
def submit_feedback(feedback_request: FeedbackRequest):
    """
    Accepts user feedback and regenerates an improved workout plan.
    Updates the existing plan in the database.
    """
    try:
        logger.info(f"📥 Received feedback for plan ID: {feedback_request.plan_id}")

        # Step 1: Get user details from DB
        user = get_user(feedback_request.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found!")

        # Step 2: Get existing plan from DB
        existing_plan_data = get_plan_by_user(feedback_request.user_id)
        if not existing_plan_data:
            raise HTTPException(status_code=404, detail="No existing plan found for this user!")

        # Step 3: Refine plan via Gemini
        refined_plan = refine_workout_plan(
            existing_plan=existing_plan_data["workout_plan"],
            feedback=feedback_request.feedback,
            goal=user["goal"],
            intensity=user["intensity"]
        )

        # Step 4: Update plan in DB
        update_plan(
            plan_id=feedback_request.plan_id,
            new_plan=refined_plan,
            feedback=feedback_request.feedback
        )

        logger.info(f"✅ Plan refined and updated for plan ID: {feedback_request.plan_id}")

        return PlanResponse(
            success=True,
            user_id=feedback_request.user_id,
            plan_id=feedback_request.plan_id,
            workout_plan=refined_plan,
            message="Your workout plan has been updated based on your feedback!"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error in /feedback: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────
# ENDPOINT 3: Get Nutrition Tip (Scenario 3)
# ─────────────────────────────────────────────
@app.get("/nutrition-tip", response_model=NutritionTipResponse)
def get_nutrition_tip(goal: str):
    """
    Returns a personalized nutrition or recovery tip based on the fitness goal.
    """
    try:
        allowed_goals = ["weight_loss", "muscle_gain", "general_wellness"]
        if goal.lower() not in allowed_goals:
            raise HTTPException(
                status_code=400,
                detail=f"Goal must be one of: {', '.join(allowed_goals)}"
            )

        logger.info(f"📥 Nutrition tip requested for goal: {goal}")
        tip = generate_nutrition_tip(goal=goal)

        return NutritionTipResponse(
            success=True,
            goal=goal,
            tip=tip
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error in /nutrition-tip: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────
# ENDPOINT 4: Get Plan by User ID
# ─────────────────────────────────────────────
@app.get("/plan/{user_id}", response_model=PlanResponse)
def get_plan(user_id: int):
    """
    Retrieves the latest stored workout plan for a specific user.
    """
    try:
        logger.info(f"📥 Plan retrieval requested for user ID: {user_id}")

        user = get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found!")

        plan = get_plan_by_user(user_id)
        if not plan:
            raise HTTPException(status_code=404, detail="No plan found for this user!")

        return PlanResponse(
            success=True,
            user_id=user_id,
            plan_id=plan["id"],
            workout_plan=plan["workout_plan"],
            nutrition_tip=plan.get("nutrition_tip"),
            message="Plan retrieved successfully!"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error in /plan/{user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))