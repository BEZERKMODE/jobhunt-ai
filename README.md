# Job Hunt AI 🚀

Job Hunt AI is a modern, full-stack automated job search and application platform. It uses intelligent background workers to scrape job listings (e.g., from Indeed), perform semantic/keyword resume matching, allow users to manage their profiles, and automatically apply to relevant positions.

---

## 🌟 Key Features

* **AI Resume Matching & Scoring**: Upload your CV/Resume to calculate keyword match scores against scraped job descriptions using background processors.
* **Indeed Job Scraper**: Integrated headless browser scraper powered by **Playwright** that crawls and saves jobs based on custom queries.
* **Auto-Apply Engine**: Queue automated job applications in the background using **Celery** tasks.
* **Real-time Stats & Dashboard**: A premium, responsive interface to track application status, view system stats, and configure preferences.
* **Secure Auth Flow**: Complete cookie-based authentication system with route protection.

---

## 🛠️ Tech Stack

### Frontend
* **React 19** with **TypeScript** & **Vite**
* **TailwindCSS** for responsive, modern UI styling
* **Zustand** for lightweight and reactive state management
* **Axios** for API requests (configured with automatic cookie/credential handling)
* **Lucide React** for icons

### Backend
* **FastAPI** (Python 3.12) high-performance REST API
* **PostgreSQL** for reliable relational data storage
* **Redis** as a Celery message broker and caching layer
* **Celery** for distributed asynchronous task queues
* **Playwright** for headless browser automation/web scraping
* **SQLAlchemy** (ORM) & **Alembic** (Database Migrations)

### DevOps & Infrastructure
* **Docker & Docker Compose** for multi-container orchestration
* **GitHub Actions** CI/CD pipeline (configured for automated testing and deployment)

---

## 🚀 Getting Started

### Prerequisites
Make sure you have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running on your system.

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/BEZERKMODE/jobhunt-ai.git
   cd jobhunt-ai
   ```

2. **Configure Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   POSTGRES_SERVER=db
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=123456
   POSTGRES_DB=jobhunt
   SECRET_KEY=supersecretkeyhere
   ```

3. **Start the Application**:
   Run the following command to build and launch all services:
   ```bash
   docker compose up --build -d
   ```

4. **Run Database Migrations**:
   Set up the database tables by executing the migrations:
   ```bash
   docker compose exec backend alembic upgrade head
   ```

5. **Seed Job Data (Optional)**:
   Seed the database with sample job listings:
   ```bash
   docker compose exec backend python seed_data.py
   ```

6. **Access the Services**:
   * **Frontend Application**: [http://localhost:3000](http://localhost:3000)
   * **Backend REST API API Docs (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📂 Project Structure

```
jobhunt-ai/
├── .github/workflows/   # CI/CD pipelines
├── backend/
│   ├── app/
│   │   ├── api/         # API Route Handlers (Auth, Jobs, Profile)
│   │   ├── core/        # App Configuration & Security
│   │   ├── db/          # DB Connection & Sessions
│   │   ├── models/      # SQLAlchemy Models (User, CV, Job, Application)
│   │   ├── schemas/     # Pydantic v2 validation models
│   │   ├── services/    # Business logic (Playwright Scraper, Scorer)
│   │   ├── tasks/       # Celery background tasks
│   │   └── worker.py    # Celery app instantiation
│   ├── Dockerfile
│   ├── entrypoint.sh
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/         # API clients (Axios configurations)
│   │   ├── components/  # Layout, Protected Routes
│   │   ├── pages/       # Dashboard, Jobs, Applications, Profile, Login
│   │   ├── store/       # Zustand State Stores
│   │   └── App.tsx      # Routing definitions
│   ├── Dockerfile
│   ├── package.json
│   └── tailwind.config.js
└── docker-compose.yml
```

---

## 🔒 License
This project is licensed under the MIT License.