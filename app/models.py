from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(180), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    otp_code = db.Column(db.String(6), nullable=True)
    otp_expiry = db.Column(db.DateTime, nullable=True)

    # Relationships: If a user is deleted, their scans and resumes go with them
    scans = db.relationship('Scan', backref='user', lazy=True, cascade="all, delete-orphan")
    resumes = db.relationship('Resume', backref='user', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email}>"


class Scan(db.Model):
    __tablename__ = 'scans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    job_title = db.Column(db.String(180), nullable=True)
    company_name = db.Column(db.String(180), nullable=True)
    skills_text = db.Column(db.Text, nullable=False)
    
    # Tracking the batch results
    total_resumes = db.Column(db.Integer, default=0, nullable=False)
    priority_count = db.Column(db.Integer, default=0, nullable=False)
    shortlisted_count = db.Column(db.Integer, default=0, nullable=False)
    rejected_count = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    resumes = db.relationship('Resume', backref='scan', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Scan {self.id} - {self.job_title}>"


class Resume(db.Model):
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    scan_id = db.Column(db.Integer, db.ForeignKey('scans.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    # Core Resume Data
    candidate_name = db.Column(db.String(180), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    stored_filename = db.Column(db.String(255), nullable=False)
    stored_path = db.Column(db.String(500), nullable=False)
    bucket = db.Column(db.String(40), nullable=False) # Priority, Shortlisted, Rejected
    
    # Scoring Data
    score = db.Column(db.Numeric(5, 2), nullable=False)
    matched_count = db.Column(db.Integer, nullable=False)
    total_count = db.Column(db.Integer, nullable=False)
    
    # --- Advanced AI Features (JSON & Text Fields) ---
    matched_skills = db.Column(db.JSON, nullable=True)
    ai_summary = db.Column(db.Text, nullable=True)
    missing_skills = db.Column(db.JSON, nullable=True)
    experience_match = db.Column(db.Text, nullable=True)
    education_match = db.Column(db.Text, nullable=True)
    certifications = db.Column(db.JSON, nullable=True)
    recommendation = db.Column(db.String(80), nullable=True)
    score_reason = db.Column(db.Text, nullable=True)
    interview_questions = db.Column(db.JSON, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Resume {self.candidate_name} - {self.score}%>"