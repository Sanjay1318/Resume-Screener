import random
from datetime import datetime, timedelta, timezone
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from app import db, bcrypt, mail
from app.models import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    # If they are already logged in, send them to the dashboard
    if current_user.is_authenticated:
        return redirect(url_for('main.root'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if email is already taken
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Email already registered. Please log in.', 'danger')
            return redirect(url_for('auth.register'))

        # Hash the password and save the new user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(name=name, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('register.html')

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email").strip()
        password = request.form.get("password")
        
        user = User.query.filter_by(email=email).first()
        
        # Verify credentials using existing bcrypt hashing
        if user and bcrypt.check_password_hash(user.password_hash, password):
            # 1. Generate 6-digit random OTP
            otp = f"{random.randint(100000, 999999)}"
            
            # 2. Set expiry time to 5 minutes from now
            expiry = datetime.now(timezone.utc) + timedelta(minutes=5)
            
            # 3. Save OTP details securely to MySQL
            user.otp_code = otp
            user.otp_expiry = expiry
            db.session.commit()
            
            # 4. Send the OTP Email via Flask-Mail
            try:
                msg = Message(
                    subject="Your Res Scanner Verification Code",
                    recipients=[user.email]
                )
                # HTML formatting for a premium email presentation
                msg.html = f"""
                <div style="font-family: sans-serif; padding: 20px; background-color: #0f172a; color: #f8fafc; border-radius: 12px; max-width: 500px;">
                    <h2 style="color: #2dd4bf; margin-bottom: 10px;">Res Scanner ⚡</h2>
                    <p style="color: #94a3b8;">Use the security token below to finish signing into your recruiter workstation:</p>
                    <div style="background-color: #1e293b; padding: 15px; text-align: center; font-size: 28px; font-weight: bold; letter-spacing: 4px; color: #14f1d9; border-radius: 8px; margin: 20px 0;">
                        {otp}
                    </div>
                    <p style="font-size: 12px; color: #64748b;">This request was generated on your behalf. Token expires in 5 minutes.</p>
                </div>
                """
                mail.send(msg)
                
                # 5. Save user id to temporary session and redirect
                session['otp_user_id'] = user.id
                flash("A security code has been dispatched to your email address.", "success")
                return redirect(url_for("auth.verify_otp"))
                
            except Exception as e:
                print(f"SMTP Delivery Failure: {e}")
                flash("Failed to send OTP email. Please ensure mail server configuration is correct.", "danger")
                return redirect(url_for("auth.login"))
        
        flash("Invalid identification email or account credentials.", "danger")
        
    return render_template("login.html")


@auth.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():
    # Enforce sequence: Ensure user has passed standard step-1 validation first
    user_id = session.get('otp_user_id')
    if not user_id:
        flash("Authorization session expired. Please sign in again.", "danger")
        return redirect(url_for("auth.login"))
        
    user = User.query.get(user_id)
    
    if request.method == "POST":
        input_code = request.form.get("otp_code", "").strip()
        current_time = datetime.now(timezone.utc)
        
        # Security Guardrails: Verify token validity and strict expiration windows
        if user.otp_code and user.otp_code == input_code:
            # Check if current time has passed the database expiry timestamp
            # Ensuring timezone alignment during comparison
            otp_expiry_utc = user.otp_expiry.replace(tzinfo=timezone.utc) if user.otp_expiry.tzinfo is None else user.otp_expiry
            
            if current_time < otp_expiry_utc:
                # Clear security fields in database upon entry success
                user.otp_code = None
                user.otp_expiry = None
                db.session.commit()
                
                # Formally establish Flask-Login session cookies
                login_user(user)
                session.pop('otp_user_id', None) # Clear validation token
                
                flash(f"Access granted. Welcome back, {user.name}.", "success")
                return redirect(url_for("main.root"))
            else:
                flash("The security key has expired. Please initiate sign in again.", "danger")
                return redirect(url_for("auth.login"))
        else:
            flash("Invalid security authorization code. Access denied.", "danger")
            
    return render_template("verify_otp.html")

@auth.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email").strip()
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Reuse our 2FA logic!
            otp = f"{random.randint(100000, 999999)}"
            user.otp_code = otp
            user.otp_expiry = datetime.now(timezone.utc) + timedelta(minutes=10)
            db.session.commit()
            
            try:
                msg = Message(subject="Password Reset Request", recipients=[user.email])
                msg.html = f"""
                <div style="font-family: sans-serif; padding: 20px; background-color: #0f172a; color: #f8fafc; border-radius: 12px; max-width: 500px;">
                    <h2 style="color: #2dd4bf; margin-bottom: 10px;">Password Reset</h2>
                    <p style="color: #94a3b8;">Use this 6-digit code to reset your password:</p>
                    <div style="background-color: #1e293b; padding: 15px; text-align: center; font-size: 28px; font-weight: bold; letter-spacing: 4px; color: #14f1d9; border-radius: 8px; margin: 20px 0;">
                        {otp}
                    </div>
                    <p style="font-size: 12px; color: #64748b;">Code expires in 10 minutes.</p>
                </div>
                """
                mail.send(msg)
                session['reset_email'] = user.email
                flash("A reset code has been sent to your email.", "info")
                return redirect(url_for("auth.reset_password"))
            except Exception as e:
                flash("Error sending email.", "danger")
        else:
            # Security best practice: Don't reveal if an email exists
            flash("If an account exists with that email, a reset code was sent.", "info")
            
    return render_template("forgot_password.html")

@auth.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    email = session.get('reset_email')
    if not email:
        return redirect(url_for("auth.forgot_password"))
        
    if request.method == "POST":
        input_code = request.form.get("otp_code").strip()
        new_password = request.form.get("new_password")
        
        user = User.query.filter_by(email=email).first()
        current_time = datetime.now(timezone.utc)
        otp_expiry_utc = user.otp_expiry.replace(tzinfo=timezone.utc) if user.otp_expiry and user.otp_expiry.tzinfo is None else user.otp_expiry
        
        if user and user.otp_code == input_code and current_time < otp_expiry_utc:
            # Hash new password and clear OTP
            user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
            user.otp_code = None
            user.otp_expiry = None
            db.session.commit()
            
            session.pop('reset_email', None)
            flash("Your password has been successfully reset. Please log in.", "success")
            return redirect(url_for("auth.login"))
        else:
            flash("Invalid or expired reset code.", "danger")
            
    return render_template("reset_password.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.root"))