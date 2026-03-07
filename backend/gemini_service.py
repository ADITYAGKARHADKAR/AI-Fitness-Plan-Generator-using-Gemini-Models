# import google.generativeai as genai
# from dotenv import load_dotenv
# import os
# import logging

# # Setup logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Load environment variables
# load_dotenv()


# def configure_gemini():
#     """Configure Gemini API with key from .env"""
#     api_key = os.getenv("GEMINI_API_KEY")
#     if not api_key:
#         raise ValueError("❌ GEMINI_API_KEY not found in .env file!")
#     genai.configure(api_key=api_key)
#     return genai.GenerativeModel("gemini-1.5-flash")


# # ─────────────────────────────────────────────
# # SCENARIO 1: Generate 7-Day Workout Plan
# # ─────────────────────────────────────────────

# def generate_workout_plan(name: str, age: int, weight: float, goal: str, intensity: str) -> str:
#     """Generate a personalized 7-day workout plan using Gemini."""
#     try:
#         model = configure_gemini()

#         prompt = f"""
#         You are a professional fitness coach. Create a detailed personalized 7-day workout plan.

#         User Profile:
#         - Name: {name}
#         - Age: {age} years
#         - Weight: {weight} kg
#         - Fitness Goal: {goal.replace('_', ' ').title()}
#         - Workout Intensity: {intensity.title()}

#         Requirements:
#         - Provide a day-by-day plan from Day 1 to Day 7
#         - Each day should include: workout name, sets, reps, duration
#         - Tailor exercises specifically to the goal: {goal}
#         - Match the difficulty to {intensity} intensity
#         - Include rest days where appropriate
#         - Keep each day's plan clear and structured

#         Format each day exactly like this:
#         Day 1 - [Focus Area]
#         • Exercise 1: [name] - [sets x reps or duration]
#         • Exercise 2: [name] - [sets x reps or duration]
#         ...

#         Day 2 - [Focus Area]
#         ...and so on until Day 7.
#         """

#         logger.info(f"🔄 Generating workout plan for user: {name}")
#         response = model.generate_content(prompt)
#         logger.info("✅ Workout plan generated successfully!")
#         return response.text

#     except Exception as e:
#         logger.error(f"❌ Error generating workout plan: {str(e)}")
#         raise Exception(f"Failed to generate workout plan: {str(e)}")


# # ─────────────────────────────────────────────
# # SCENARIO 2: Refine Plan Based on Feedback
# # ─────────────────────────────────────────────

# def refine_workout_plan(existing_plan: str, feedback: str, goal: str, intensity: str) -> str:
#     """Regenerate a workout plan based on user feedback using Gemini."""
#     try:
#         model = configure_gemini()

#         prompt = f"""
#         You are a professional fitness coach. A user has provided feedback on their existing 
#         workout plan and wants an improved version.

#         Existing Workout Plan:
#         {existing_plan}

#         User Feedback:
#         "{feedback}"

#         User Details:
#         - Fitness Goal: {goal.replace('_', ' ').title()}
#         - Workout Intensity: {intensity.title()}

#         Requirements:
#         - Address the user's feedback directly
#         - Keep what was working well in the original plan
#         - Improve or replace what the user requested
#         - Maintain a full 7-day structure
#         - Keep the same clear formatting as the original

#         Format each day exactly like this:
#         Day 1 - [Focus Area]
#         • Exercise 1: [name] - [sets x reps or duration]
#         • Exercise 2: [name] - [sets x reps or duration]
#         ...and so on until Day 7.
#         """

#         logger.info("🔄 Refining workout plan based on feedback...")
#         response = model.generate_content(prompt)
#         logger.info("✅ Refined workout plan generated successfully!")
#         return response.text

#     except Exception as e:
#         logger.error(f"❌ Error refining workout plan: {str(e)}")
#         raise Exception(f"Failed to refine workout plan: {str(e)}")


# # ─────────────────────────────────────────────
# # SCENARIO 3: Generate Nutrition / Recovery Tip
# # ─────────────────────────────────────────────

# def generate_nutrition_tip(goal: str) -> str:
#     """Generate a nutrition or recovery tip based on fitness goal using Gemini."""
#     try:
#         model = configure_gemini()

#         prompt = f"""
#         You are a professional nutritionist and fitness recovery expert.
        
#         Provide ONE concise, practical, and actionable nutrition or recovery tip 
#         for someone whose fitness goal is: {goal.replace('_', ' ').title()}

#         Requirements:
#         - Keep it to 2-3 sentences maximum
#         - Make it specific to the goal: {goal}
#         - Be practical and easy to follow
#         - Do not include bullet points, just plain helpful advice
#         """

#         logger.info(f"🔄 Generating nutrition tip for goal: {goal}")
#         response = model.generate_content(prompt)
#         logger.info("✅ Nutrition tip generated successfully!")
#         return response.text.strip()

#     except Exception as e:
#         logger.error(f"❌ Error generating nutrition tip: {str(e)}")
#         raise Exception(f"Failed to generate nutrition tip: {str(e)}")


from google import genai
from dotenv import load_dotenv
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def get_client():
    """Configure and return a Gemini client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("❌ GEMINI_API_KEY not found in .env file!")
    return genai.Client(api_key=api_key)


# ─────────────────────────────────────────────
# SCENARIO 1: Generate 7-Day Workout Plan
# ─────────────────────────────────────────────

def generate_workout_plan(name: str, age: int, weight: float, goal: str, intensity: str) -> str:
    """Generate a personalized 7-day workout plan using Gemini."""
    try:
        client = get_client()

        prompt = f"""
        You are a professional fitness coach. Create a detailed personalized 7-day workout plan.

        User Profile:
        - Name: {name}
        - Age: {age} years
        - Weight: {weight} kg
        - Fitness Goal: {goal.replace('_', ' ').title()}
        - Workout Intensity: {intensity.title()}

        Requirements:
        - Provide a day-by-day plan from Day 1 to Day 7
        - Each day should include: workout name, sets, reps, duration
        - Tailor exercises specifically to the goal: {goal}
        - Match the difficulty to {intensity} intensity
        - Include rest days where appropriate
        - Keep each day's plan clear and structured

        Format each day exactly like this:
        Day 1 - [Focus Area]
        • Exercise 1: [name] - [sets x reps or duration]
        • Exercise 2: [name] - [sets x reps or duration]

        Day 2 - [Focus Area]
        ...and so on until Day 7.
        """

        logger.info(f"🔄 Generating workout plan for user: {name}")
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        logger.info("✅ Workout plan generated successfully!")
        return response.text

    except Exception as e:
        logger.error(f"❌ Error generating workout plan: {str(e)}")
        raise Exception(f"Failed to generate workout plan: {str(e)}")


# ─────────────────────────────────────────────
# SCENARIO 2: Refine Plan Based on Feedback
# ─────────────────────────────────────────────

def refine_workout_plan(existing_plan: str, feedback: str, goal: str, intensity: str) -> str:
    """Regenerate a workout plan based on user feedback using Gemini."""
    try:
        client = get_client()

        prompt = f"""
        You are a professional fitness coach. A user has provided feedback on their existing 
        workout plan and wants an improved version.

        Existing Workout Plan:
        {existing_plan}

        User Feedback:
        "{feedback}"

        User Details:
        - Fitness Goal: {goal.replace('_', ' ').title()}
        - Workout Intensity: {intensity.title()}

        Requirements:
        - Address the user's feedback directly
        - Keep what was working well in the original plan
        - Improve or replace what the user requested
        - Maintain a full 7-day structure
        - Keep the same clear formatting as the original

        Format each day exactly like this:
        Day 1 - [Focus Area]
        • Exercise 1: [name] - [sets x reps or duration]
        • Exercise 2: [name] - [sets x reps or duration]
        ...and so on until Day 7.
        """

        logger.info("🔄 Refining workout plan based on feedback...")
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        logger.info("✅ Refined workout plan generated successfully!")
        return response.text

    except Exception as e:
        logger.error(f"❌ Error refining workout plan: {str(e)}")
        raise Exception(f"Failed to refine workout plan: {str(e)}")


# ─────────────────────────────────────────────
# SCENARIO 3: Generate Nutrition / Recovery Tip
# ─────────────────────────────────────────────

def generate_nutrition_tip(goal: str) -> str:
    """Generate a nutrition or recovery tip based on fitness goal using Gemini."""
    try:
        client = get_client()

        prompt = f"""
        You are a professional nutritionist and fitness recovery expert.
        
        Provide ONE concise, practical, and actionable nutrition or recovery tip 
        for someone whose fitness goal is: {goal.replace('_', ' ').title()}

        Requirements:
        - Keep it to 2-3 sentences maximum
        - Make it specific to the goal: {goal}
        - Be practical and easy to follow
        - Do not include bullet points, just plain helpful advice
        """

        logger.info(f"🔄 Generating nutrition tip for goal: {goal}")
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        logger.info("✅ Nutrition tip generated successfully!")
        return response.text.strip()

    except Exception as e:
        logger.error(f"❌ Error generating nutrition tip: {str(e)}")
        raise Exception(f"Failed to generate nutrition tip: {str(e)}")