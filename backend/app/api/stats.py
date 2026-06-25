from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.models import Job, CV, Application

router = APIRouter()


@router.get("/stats", tags=["stats"])
def get_stats(db: Session = Depends(deps.get_db)):
    """Return simple aggregate statistics for the dashboard."""
    return {
        "total_jobs": db.query(Job).count(),
        "total_saved_cvs": db.query(CV).count(),
        "total_applications": db.query(Application).count(),
    }


@router.get("/insights/dashboard", tags=["stats"])
def get_dashboard_insights(
    current_user: "User" = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    applications = db.query(Application).filter(
        Application.user_id == current_user.id
    ).all()

    total = len(applications)
    applied = sum(1 for a in applications if a.status == "applied")
    avg_score = sum(a.match_score or 0 for a in applications) / max(total, 1)

    buckets = {"0-40": 0, "41-60": 0, "61-80": 0, "81-100": 0}
    for a in applications:
        s = a.match_score or 0
        if s <= 40:
            buckets["0-40"] += 1
        elif s <= 60:
            buckets["41-60"] += 1
        elif s <= 80:
            buckets["61-80"] += 1
        else:
            buckets["81-100"] += 1

    top_matched = [
        {"title": a.job.title, "company": a.job.company, "score": a.match_score}
        for a in sorted(applications, key=lambda x: x.match_score or 0, reverse=True)[:5]
    ]

    return {
        "total_jobs_scraped": db.query(Job).count(),
        "total_applications": total,
        "applications_sent": applied,
        "avg_match_score": round(avg_score, 1),
        "score_distribution": buckets,
        "top_matched_jobs": top_matched,
    }
