import logging
from google import genai
from google.genai import types
from app.core.config import settings

logger = logging.getLogger(__name__)

def evaluate_match(cv_text: str, job_description: str) -> dict:
    """
    Evaluates the match between a CV and a job description using Gemini.
    Returns a dict with 'score' (0-100), 'verdict', and 'missing_skills'.
    """
    if not settings.GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY is not set. Returning mock score.")
        return {
            "score": 75.0,
            "verdict": "Mock: Good match but missing some key skills.",
            "missing_skills": ["Mock Skill 1", "Mock Skill 2"]
        }

    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
        prompt = f"""
        You are an expert ATS (Applicant Tracking System).
        Evaluate how well the following CV matches the Job Description.
        
        Job Description:
        {job_description}
        
        CV Text:
        {cv_text}
        
        Provide the output strictly in the following JSON format:
        {{
            "score": <a float from 0 to 100>,
            "verdict": "<a short sentence explaining the score>",
            "missing_skills": ["<skill1>", "<skill2>"]
        }}
        """

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )
        
        import json
        result = json.loads(response.text)
        return result
    except Exception as e:
        logger.error(f"Error evaluating match with Gemini: {e}")
        return {
            "score": 0.0,
            "verdict": f"Error: {str(e)}",
            "missing_skills": []
        }
