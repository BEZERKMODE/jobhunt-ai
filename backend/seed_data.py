from app.db.session import SessionLocal
from app.models.job import JobListing
from datetime import datetime
import json

db = SessionLocal()

jobs = [
    {
        "title": "Senior Frontend Developer",
        "company": "TechNova",
        "location": "Remote",
        "type": "Full-time",
        "source": "Internal",
        "description": "We are looking for an experienced Frontend Developer with deep knowledge of React and TailwindCSS. You will lead our UI architecture and mentor junior developers.",
        "posted_at": datetime.utcnow()
    },
    {
        "title": "Machine Learning Engineer",
        "company": "AI Innovations",
        "location": "New York, NY",
        "type": "Full-time",
        "source": "LinkedIn",
        "description": "Join our AI research team to build cutting edge models for NLP and computer vision. Strong Python and PyTorch skills required.",
        "posted_at": datetime.utcnow()
    },
    {
        "title": "Product Designer",
        "company": "Creative Solutions",
        "location": "San Francisco, CA",
        "type": "Contract",
        "source": "Indeed",
        "description": "Looking for a talented product designer to craft beautiful user experiences. Figma expertise is a must.",
        "posted_at": datetime.utcnow()
    }
]

for job_data in jobs:
    job = JobListing(**job_data)
    db.add(job)

db.commit()
print("Seeded database with fake jobs!")
db.close()
