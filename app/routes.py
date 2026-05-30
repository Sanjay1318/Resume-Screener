import os
import time
import csv
from io import StringIO
from flask import Response
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import pdfplumber

# FIXED: Removed the stray bcrypt import and added 'User' to the models import!
from app import bcrypt
from app.models import db, Scan, Resume, User
from app.ai_parser import analyze_resume_with_ai
from app.utils import extract_text_from_pdf, extract_text_from_txt

main = Blueprint('main', __name__)

# Helper function to read JD files safely
def read_jd_file(file):
    filename = secure_filename(file.filename)
    lower = filename.lower()
    
    if lower.endswith('.txt'):
        return file.read().decode('utf-8', errors='ignore')
    elif lower.endswith('.pdf'):
        text_parts = []
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text_parts.append(page.extract_text() or "")
        return "\n".join(text_parts)
    return ""

@main.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        new_name = request.form.get("name").strip()
        new_email = request.form.get("email").strip()
        
        # New password fields
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        
        updates_made = False

        # 1. Update Name
        if new_name and new_name != current_user.name:
            current_user.name = new_name
            updates_made = True
            
        # 2. Update Email
        if new_email and new_email != current_user.email:
            existing_user = User.query.filter_by(email=new_email).first()
            if existing_user:
                flash("That email address is already in use.", "danger")
            else:
                current_user.email = new_email
                updates_made = True
                
        # 3. Secure Password Update Logic
        if new_password:
            if not current_password:
                flash("You must enter your current password to set a new one.", "danger")
                return redirect(url_for("main.profile"))
                
            # Verify the current password is correct
            if not bcrypt.check_password_hash(current_user.password_hash, current_password):
                flash("Incorrect current password.", "danger")
                return redirect(url_for("main.profile"))
                
            # If it matches, hash and save the new password
            current_user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
            updates_made = True
            
        if updates_made:
            db.session.commit()
            flash("Account settings updated successfully!", "success")
            
        return redirect(url_for("main.profile"))
        
    return render_template("profile.html")

@main.route("/")
@main.route("/welcome")
def root():
    return render_template("welcome.html")

@main.route("/history")
@login_required
def history():
    # Fetch all past scans
    scans = Scan.query.filter_by(user_id=current_user.id).order_by(Scan.created_at.desc()).all()
    
    # Calculate Global Analytics
    analytics = {
        "total_scans": len(scans),
        "total_resumes": sum(s.total_resumes for s in scans),
        "total_priority": sum(s.priority_count for s in scans),
        "total_shortlisted": sum(s.shortlisted_count for s in scans),
        "total_rejected": sum(s.rejected_count for s in scans)
    }
    
    return render_template("history.html", scans=scans, analytics=analytics)

@main.route("/delete_scan/<int:scan_id>", methods=["POST"])
@login_required
def delete_scan(scan_id):
    # Find the scan in the database
    scan = Scan.query.get_or_404(scan_id)
    
    # Security check: Ensure the logged-in user actually owns this scan
    if scan.user_id != current_user.id:
        flash("Unauthorized access. You cannot delete this scan.", "danger")
        return redirect(url_for('main.history'))
        
    # Delete the scan (MySQL ON DELETE CASCADE will automatically remove the attached resumes)
    db.session.delete(scan)
    db.session.commit()
    
    flash(f"Scan '{scan.job_title}' was successfully deleted.", "success")
    return redirect(url_for('main.history'))

@main.route("/analyze", methods=["POST"])
@login_required
def analyze():
    job_title = request.form.get("job_title", "").strip()
    jd_text = request.form.get("jd_text", "").strip()
    jd_file = request.files.get("jd_file")
    
    if jd_file and jd_file.filename:
        jd_text = read_jd_file(jd_file) 
        
    if not jd_text:
        flash("Please provide a Job Description either by pasting text or uploading a file.", "danger")
        return redirect(url_for("main.root"))

    files = request.files.getlist("resumes")
    files = [f for f in files if f and f.filename.strip()]
    
    if not files:
        flash("Please upload at least one resume.", "danger")
        return redirect(url_for("main.root"))
        
    MAX_RESUMES = 30
    if len(files) > MAX_RESUMES:
        flash(f"Limit exceeded! You can only process up to {MAX_RESUMES} resumes per scan.", "danger")
        return redirect(url_for("main.root"))

    new_scan = Scan(
        user_id=current_user.id,
        job_title=job_title,
        skills_text=jd_text, 
        total_resumes=len(files)
    )
    db.session.add(new_scan)
    db.session.commit() 
    
    os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    success_count = 0 

    for index, file in enumerate(files, 1):
        filename = secure_filename(file.filename)
        print(f"\n[{index}/{len(files)}] Processing File: {filename}")
        
        temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(temp_path)
        
        # 1. Extract Text
        print(" -> Extracting text...")
        if filename.lower().endswith('.pdf'):
            resume_text = extract_text_from_pdf(temp_path)
        else:
            resume_text = extract_text_from_txt(temp_path)
            
        print(f" -> Text extracted successfully! ({len(resume_text)} characters)")
            
        if not resume_text or not resume_text.strip():
            print(" -> FAILED: No readable text found.")
            flash(f"Skipped {filename}: No readable text found.", "warning")
            continue 
            
        # 2. Call the AI Engine
        print(" -> Sending to Gemini AI...")
        ai_data = analyze_resume_with_ai(resume_text, jd_text)
        
        if ai_data:
            print(" -> SUCCESS: AI returned JSON data!")
            score = ai_data.get('score', 0)
            ats_score = ai_data.get('ats_score', 0)  # <-- Pull the new ATS Score
            
            if score > 85:
                bucket = "Priority"
                new_scan.priority_count += 1
            elif score >= 65:
                bucket = "Shortlisted"
                new_scan.shortlisted_count += 1
            else:
                bucket = "Rejected"
                new_scan.rejected_count += 1
                
            matched_skills = ai_data.get('matched_skills', [])
            
            new_resume = Resume(
                scan_id=new_scan.id,
                user_id=current_user.id,
                candidate_name=filename.split('.')[0], 
                original_filename=filename,
                stored_filename=filename,
                stored_path=temp_path,
                bucket=bucket,
                score=score,
                ats_score=ats_score,  # <-- Save it to the database!
                matched_count=len(matched_skills),
                total_count=len(matched_skills) + len(ai_data.get('missing_skills', [])),
                matched_skills=matched_skills,
                ai_summary=ai_data.get('ai_summary'),
                missing_skills=ai_data.get('missing_skills'),
                experience_match=ai_data.get('experience_match'),
                education_match=ai_data.get('education_match'),
                certifications=ai_data.get('certifications'),
                recommendation=ai_data.get('recommendation'),
                score_reason=ai_data.get('score_reason'),
                interview_questions=ai_data.get('interview_questions')
            )
            db.session.add(new_resume)
            success_count += 1
        else:
            print(" -> FAILED: AI did not return data.")
            flash(f"Failed to analyze {filename} with AI.", "danger")
            
        # print(" -> Pausing for 5 seconds to respect API limits...")
        # time.sleep(15) 
    
    db.session.commit()
    
    if success_count > 0:
        flash(f"Scan complete! {success_count} resumes processed successfully.", "success")
    else:
        flash("Scan finished, but no resumes were successfully processed.", "warning")
        
    return redirect(url_for('main.view_scan', scan_id=new_scan.id))

@main.route("/scan/<int:scan_id>")
@login_required
def view_scan(scan_id):
    # Fetch the scan and ensure it belongs to the logged-in user
    scan = Scan.query.get_or_404(scan_id)
    if scan.user_id != current_user.id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('main.root'))
        
    # Fetch all resumes for this scan
    resumes = Resume.query.filter_by(scan_id=scan.id).all()
    
    # Group them by bucket
    results = {"Priority": [], "Shortlisted": [], "Rejected": []}
    for r in resumes:
        if r.bucket in results:
            results[r.bucket].append(r)
            
    # Sort candidates in each bucket by their AI score (highest first)
    for bucket in results:
        results[bucket].sort(key=lambda x: x.score, reverse=True)
        
    return render_template("analyze.html", scan=scan, results=results)

@main.route("/export_csv/<int:scan_id>")
@login_required
def export_csv(scan_id):
    # Fetch the scan
    scan = Scan.query.get_or_404(scan_id)
    
    # Security check: Ensure the user owns this data
    if scan.user_id != current_user.id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('main.history'))
        
    # Fetch all resumes attached to this scan
    resumes = Resume.query.filter_by(scan_id=scan.id).all()
    
    # Create an in-memory string buffer for the CSV data
    si = StringIO()
    cw = csv.writer(si)
    
    # 1. Write the Header Row
    cw.writerow([
        'Candidate Name', 'Original Filename', 'AI Score', 'Bucket', 
        'Recommendation', 'Matched Skills Count', 'Missing Skills Count', 
        'AI Summary', 'Experience Match', 'Education Match'
    ])
    
    # 2. Write the Candidate Data Rows
    for r in resumes:
        # Safely count missing skills if the JSON exists
        missing_count = len(r.missing_skills) if r.missing_skills else 0
        
        cw.writerow([
            r.candidate_name,
            r.original_filename,
            f"{r.score}%",
            r.bucket,
            r.recommendation,
            r.matched_count,
            missing_count,
            r.ai_summary,
            r.experience_match,
            r.education_match
        ])
        
    # 3. Package it as a downloadable file
    output = si.getvalue()
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename=ScanResults_{scan.job_title.replace(' ', '')}.csv"}
    )