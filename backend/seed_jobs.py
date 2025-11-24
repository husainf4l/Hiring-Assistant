"""
Seed script to add 10 sample jobs to the database
"""

from datetime import datetime
from database import SessionLocal
from db_models import JobPost

# Sample jobs data
SAMPLE_JOBS = [
    {
        "title": "Senior Frontend Engineer",
        "company": "TechCorp Innovation Labs",
        "location": "San Francisco, CA",
        "workplace_type": "Remote",
        "job_type": "Full-Time",
        "summary": "Join our elite frontend team building next-gen web applications. We're looking for a senior engineer to lead our React initiative.",
        "responsibilities": [
            "Lead frontend architecture and design decisions",
            "Build scalable React applications with TypeScript",
            "Mentor junior developers",
            "Optimize performance and user experience",
            "Collaborate with product and design teams"
        ],
        "requirements": [
            "5+ years of experience",
            "Expert-level React and TypeScript",
            "Web performance optimization",
            "Testing frameworks",
            "Leadership skills"
        ],
        "skills": ["react", "typescript", "javascript", "performance", "leadership"],
        "keywords": ["react", "typescript", "frontend", "senior"],
        "culture_and_team": "We value innovation, collaboration, and continuous learning."
    },
    {
        "title": "Full-Stack Engineer",
        "company": "CloudScale Systems",
        "location": "Seattle, WA",
        "workplace_type": "Hybrid",
        "job_type": "Full-Time",
        "summary": "We're building cloud infrastructure for the future. Looking for talented full-stack engineers to join our growing team.",
        "responsibilities": [
            "Design and implement full-stack solutions",
            "Work with Python and JavaScript/TypeScript",
            "Build RESTful APIs and microservices",
            "Implement database solutions",
            "Write clean, maintainable code"
        ],
        "requirements": [
            "3+ years of full-stack development",
            "Proficiency in Python or Node.js",
            "Experience with React or Vue.js",
            "Database design knowledge",
            "Git and version control expertise"
        ],
        "skills": ["Python", "JavaScript", "React", "PostgreSQL", "API Design"],
        "keywords": ["fullstack", "python", "javascript", "cloud"],
        "culture_and_team": "Fast-paced startup environment with opportunities to grow."
    },
    {
        "title": "Product Manager",
        "company": "InnovateTech Solutions",
        "location": "New York, NY",
        "workplace_type": "On-Site",
        "job_type": "Full-Time",
        "summary": "Lead our product vision and strategy. We need a PM who can bridge the gap between user needs and technical capabilities.",
        "responsibilities": [
            "Define product roadmap and strategy",
            "Gather and analyze user requirements",
            "Work with engineering and design teams",
            "Present to stakeholders and investors",
            "Drive product adoption and growth"
        ],
        "requirements": [
            "4+ years of product management experience",
            "Strong analytical and communication skills",
            "Experience with SaaS products",
            "Data-driven decision making",
            "Agile methodology experience"
        ],
        "skills": ["Product Strategy", "Analytics", "Communication", "Agile", "User Research"],
        "keywords": ["product", "pm", "saas", "strategy"],
        "culture_and_team": "Collaborative team focused on user success and impact."
    },
    {
        "title": "DevOps Engineer",
        "company": "CloudOps Pro",
        "location": "Austin, TX",
        "workplace_type": "Remote",
        "job_type": "Full-Time",
        "summary": "Build and maintain our cloud infrastructure. We're looking for an experienced DevOps engineer to optimize our deployment pipeline.",
        "responsibilities": [
            "Manage AWS and Kubernetes infrastructure",
            "Implement CI/CD pipelines",
            "Monitor system performance and uptime",
            "Automate deployment processes",
            "Ensure security and compliance"
        ],
        "requirements": [
            "3+ years of DevOps experience",
            "AWS or GCP expertise",
            "Docker and Kubernetes proficiency",
            "Infrastructure as Code experience",
            "Linux system administration"
        ],
        "skills": ["AWS", "Kubernetes", "Docker", "CI/CD", "Terraform"],
        "keywords": ["devops", "aws", "kubernetes", "infrastructure"],
        "culture_and_team": "Innovation and reliability are core to our mission."
    },
    {
        "title": "Data Scientist",
        "company": "AI Insights Corp",
        "location": "Boston, MA",
        "workplace_type": "Hybrid",
        "job_type": "Full-Time",
        "summary": "Join our data science team working on cutting-edge machine learning projects. Help us extract insights from big data.",
        "responsibilities": [
            "Build machine learning models",
            "Analyze large datasets",
            "Create data visualizations",
            "Deploy models to production",
            "Collaborate with product teams"
        ],
        "requirements": [
            "3+ years of data science experience",
            "Python and SQL expertise",
            "Machine learning frameworks (TensorFlow, PyTorch)",
            "Statistical analysis skills",
            "Experience with big data tools"
        ],
        "skills": ["Python", "Machine Learning", "SQL", "TensorFlow", "Statistics"],
        "keywords": ["data science", "ml", "python", "ai"],
        "culture_and_team": "Cutting-edge research with real-world applications."
    },
    {
        "title": "UX/UI Designer",
        "company": "DesignStudio Creative",
        "location": "Los Angeles, CA",
        "workplace_type": "Remote",
        "job_type": "Full-Time",
        "summary": "Create beautiful and intuitive user interfaces. We're looking for a talented designer to lead our design team.",
        "responsibilities": [
            "Design user interfaces and experiences",
            "Create wireframes and prototypes",
            "Conduct user research and testing",
            "Maintain design systems",
            "Collaborate with developers and product"
        ],
        "requirements": [
            "4+ years of UX/UI design experience",
            "Proficiency in Figma or Sketch",
            "Portfolio with 3+ shipped products",
            "Understanding of design principles",
            "User research experience"
        ],
        "skills": ["Figma", "UI Design", "UX Research", "Prototyping", "Design Systems"],
        "keywords": ["design", "ux", "ui", "figma"],
        "culture_and_team": "Design-driven company where creativity thrives."
    },
    {
        "title": "Backend Engineer (Python)",
        "company": "DataFlow Systems",
        "location": "Chicago, IL",
        "workplace_type": "Hybrid",
        "job_type": "Full-Time",
        "summary": "Build robust backend systems processing millions of transactions daily. We need experienced Python engineers.",
        "responsibilities": [
            "Design and build Python microservices",
            "Create efficient database schemas",
            "Implement API endpoints",
            "Optimize system performance",
            "Write comprehensive tests"
        ],
        "requirements": [
            "4+ years of backend development",
            "Advanced Python skills",
            "PostgreSQL or MySQL expertise",
            "REST API design experience",
            "Testing framework knowledge"
        ],
        "skills": ["Python", "FastAPI", "PostgreSQL", "Microservices", "API Design"],
        "keywords": ["backend", "python", "fastapi", "database"],
        "culture_and_team": "High-performance systems and quality engineering."
    },
    {
        "title": "Mobile App Developer (React Native)",
        "company": "MobileFirst Apps",
        "location": "Denver, CO",
        "workplace_type": "Remote",
        "job_type": "Full-Time",
        "summary": "Build cross-platform mobile applications. Looking for React Native expert to scale our mobile team.",
        "responsibilities": [
            "Develop iOS and Android apps with React Native",
            "Implement mobile UI components",
            "Optimize app performance",
            "Integrate with backend APIs",
            "Debug and troubleshoot issues"
        ],
        "requirements": [
            "3+ years of mobile development",
            "React Native expertise",
            "JavaScript/TypeScript proficiency",
            "iOS/Android platform knowledge",
            "Git version control"
        ],
        "skills": ["React Native", "JavaScript", "TypeScript", "iOS", "Android"],
        "keywords": ["mobile", "react native", "ios", "android"],
        "culture_and_team": "Building apps that millions use every day."
    },
    {
        "title": "QA Engineer (Automation)",
        "company": "TestSuite Automation",
        "location": "Portland, OR",
        "workplace_type": "On-Site",
        "job_type": "Full-Time",
        "summary": "Ensure product quality at scale. We're looking for QA engineers to build automated testing frameworks.",
        "responsibilities": [
            "Write automated test scripts",
            "Build testing frameworks",
            "Execute regression testing",
            "Report and track bugs",
            "Collaborate with developers"
        ],
        "requirements": [
            "3+ years of QA automation experience",
            "Selenium or Cypress expertise",
            "JavaScript or Python scripting",
            "Testing methodologies knowledge",
            "Bug tracking tools experience"
        ],
        "skills": ["Selenium", "Cypress", "Python", "Test Automation", "JIRA"],
        "keywords": ["qa", "automation", "testing", "selenium"],
        "culture_and_team": "Quality-first culture with attention to detail."
    },
    {
        "title": "Tech Lead / Engineering Manager",
        "company": "FutureTech Ventures",
        "location": "San Francisco, CA",
        "workplace_type": "Hybrid",
        "job_type": "Full-Time",
        "summary": "Lead our engineering team. We're looking for an experienced tech lead to scale our engineering efforts.",
        "responsibilities": [
            "Lead and mentor engineering team",
            "Define technical architecture",
            "Code review and quality standards",
            "Hiring and team building",
            "Communicate with leadership"
        ],
        "requirements": [
            "7+ years of software engineering",
            "3+ years of team leadership",
            "Strong technical foundation",
            "Excellent communication skills",
            "System design expertise"
        ],
        "skills": ["Leadership", "System Design", "Mentoring", "Architecture", "Communication"],
        "keywords": ["tech lead", "manager", "leadership", "engineering"],
        "culture_and_team": "Building great teams that ship excellent products."
    }
]

def seed_jobs():
    """Seed the database with sample jobs"""
    db = SessionLocal()
    
    try:
        # Check if jobs already exist
        existing_count = db.query(JobPost).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} jobs. Skipping seed.")
            return
        
        # Add jobs
        for i, job_data in enumerate(SAMPLE_JOBS, 1):
            job = JobPost(
                user_id=1,
                title=job_data["title"],
                company=job_data["company"],
                location=job_data.get("location", ""),
                workplace_type=job_data.get("workplace_type", ""),
                job_type=job_data.get("job_type", ""),
                summary=job_data["summary"],
                responsibilities=job_data["responsibilities"],
                requirements=job_data["requirements"],
                skills=job_data.get("skills", []),
                keywords=job_data.get("keywords", []),
                culture_and_team=job_data.get("culture_and_team", ""),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            db.add(job)
            print(f"✅ Added: {i}. {job_data['title']} @ {job_data['company']}")
        
        db.commit()
        print(f"\n✅ Successfully seeded {len(SAMPLE_JOBS)} jobs to database!")
        
    except Exception as e:
        print(f"❌ Error seeding jobs: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_jobs()
