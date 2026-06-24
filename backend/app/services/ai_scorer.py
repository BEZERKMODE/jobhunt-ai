"""
AI Scorer — calls Claude Haiku to semantically score a resume against a job description.
Returns structured analysis: score, skills gap, cover letter draft, ATS keywords.
"""

import httpx
import json
import re
import structlog
from app.core.config import settings

log = structlog.get_logger()

SYSTEM_PROMPT = """You are a world-class ATS system and senior technical recruiter with 15+ years of experience.
Your job is to analyze how well a candidate's resume matches a job description.
You always respond with ONLY a valid JSON object — no preamble, no markdown, no explanation."""

SCORE_PROMPT = """Analyze this resume against the job description and return ONLY a JSON object with these exact fields:

{{
  "match_score": <integer 0-100>,
  "matched_skills": [<list of skills/keywords present in both>],
  "missing_skills": [<list of skills in the job but missing from resume>],
  "experience_fit": "<junior|mid|senior|overqualified>",
  "recommendation": "<apply|stretch|skip>",
  "recommendation_reason": "<1-2 sentence explanation>",
  "cover_letter_draft": "<3 paragraph professional cover letter tailored to this specific role>",
  "ats_keywords": [<list of exact keywords from the job to add to resume>],
  "strengths": [<top 3 candidate strengths for this role>],
  "score_breakdown": {{
    "skills_match": <0-40>,
    "experience_level": <0-30>,
    "domain_fit": <0-20>,
    "education": <0-10>
  }}
}}

RESUME:
{resume}

JOB DESCRIPTION:
{job_description}"""


async def llm_score_resume_against_job(
    resume_text: str,
    job_description: str,
    job_title: str = "",
    company: str = "",
) -> dict:
    """
    Score resume against job using Claude Haiku (fast, cheap for batch ops).
    Falls back to keyword scoring if API key missing or call fails.
    """
    if not settings.ANTHROPIC_API_KEY:
        log.warning("anthropic_api_key_missing", fallback="keyword_scorer")
        return _keyword_fallback_score(resume_text, job_description)

    prompt = SCORE_PROMPT.format(
        resume=resume_text[:4000],
        job_description=job_description[:2500],
    )

    try:
        async with httpx.AsyncClient(timeout=45.0) as client:
            resp = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": settings.ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": "claude-haiku-4-5-20251001",
                    "max_tokens": 1500,
                    "system": SYSTEM_PROMPT,
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
        resp.raise_for_status()
        data = resp.json()
        raw_text = data["content"][0]["text"]

        # Strip markdown fences if model adds them despite instructions
        raw_text = re.sub(r"```json|```", "", raw_text).strip()
        result = json.loads(raw_text)

        log.info(
            "ai_score_complete",
            score=result.get("match_score"),
            recommendation=result.get("recommendation"),
            company=company,
        )
        return result

    except (httpx.HTTPError, json.JSONDecodeError, KeyError) as e:
        log.error("ai_scorer_failed", error=str(e), fallback="keyword_scorer")
        return _keyword_fallback_score(resume_text, job_description)


async def generate_cover_letter(
    resume_text: str,
    job_description: str,
    job_title: str,
    company: str,
    tone: str = "professional",
) -> str:
    """Generate a standalone cover letter (called from frontend on demand)."""
    if not settings.ANTHROPIC_API_KEY:
        return "API key not configured. Please add ANTHROPIC_API_KEY to your .env file."

    prompt = f"""Write a {tone} cover letter for this candidate applying to {job_title} at {company}.

RESUME:
{resume_text[:3000]}

JOB DESCRIPTION:
{job_description[:2000]}

Write 3 focused paragraphs:
1. Why this role, why this company (specific, not generic)
2. Top 2-3 relevant achievements with numbers where possible
3. Forward-looking close

Do not include date, address headers, or "Dear Hiring Manager" — just the 3 paragraphs."""

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": settings.ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-haiku-4-5-20251001",
                "max_tokens": 800,
                "messages": [{"role": "user", "content": prompt}],
            },
        )
    resp.raise_for_status()
    return resp.json()["content"][0]["text"]


def _keyword_fallback_score(resume_text: str, job_description: str) -> dict:
    """Simple TF-IDF-style keyword overlap as fallback when LLM unavailable."""
    import re

    def tokenize(text: str) -> set:
        words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
        stopwords = {"the", "and", "for", "with", "this", "that", "have", "will", "are", "you"}
        return {w for w in words if w not in stopwords}

    resume_tokens = tokenize(resume_text)
    job_tokens = tokenize(job_description)

    if not job_tokens:
        return {"match_score": 0, "matched_skills": [], "missing_skills": [], "recommendation": "skip"}

    matched = resume_tokens & job_tokens
    score = min(100, int((len(matched) / len(job_tokens)) * 100))

    return {
        "match_score": score,
        "matched_skills": list(matched)[:15],
        "missing_skills": list(job_tokens - resume_tokens)[:15],
        "experience_fit": "mid",
        "recommendation": "apply" if score >= 60 else "stretch" if score >= 40 else "skip",
        "recommendation_reason": f"Keyword overlap: {score}% match (fallback scoring — configure ANTHROPIC_API_KEY for full AI analysis)",
        "cover_letter_draft": "Configure ANTHROPIC_API_KEY to generate tailored cover letters.",
        "ats_keywords": list(job_tokens - resume_tokens)[:10],
        "strengths": [],
        "score_breakdown": {
            "skills_match": min(40, int(score * 0.4)),
            "experience_level": min(30, int(score * 0.3)),
            "domain_fit": min(20, int(score * 0.2)),
            "education": min(10, int(score * 0.1)),
        },
    }
