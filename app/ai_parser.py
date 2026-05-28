from google import genai
from google.genai import types
from flask import current_app
import json
import time # <-- Make sure time is imported!

def analyze_resume_with_ai(resume_text, jd_text, max_retries=3):
    """
    Sends the resume and job description to Gemini and returns structured JSON.
    Includes an automatic retry mechanism to bypass API rate limits.
    """
    client = genai.Client(api_key=current_app.config['GEMINI_API_KEY'])
    
    prompt = f"""
    You are an expert technical recruiter and resume scanner. 
    Compare the provided Candidate Resume against the Job Description.
    
    You MUST return your response as a valid JSON object with the EXACT following keys:
    - "score": A number between 0 and 100 representing the overall match.
    - "matched_skills": A list of strings containing skills found in both the JD and resume.
    - "missing_skills": A list of strings containing important skills from the JD missing in the resume.
    - "ai_summary": A 2-sentence summary of the candidate's profile.
    - "experience_match": A short sentence assessing if their years/type of experience matches.
    - "education_match": A short sentence assessing their education vs requirements.
    - "certifications": A list of strings containing any certifications found.
    - "recommendation": A short string, either "Strong Hire", "Potential Hire", or "Do Not Hire".
    - "score_reason": A brief paragraph explaining why you gave the score you did.
    - "interview_questions": A list of 3 specific technical/behavioral questions to ask this candidate based on their resume gaps or strengths.

    Job Description:
    {jd_text}
    
    Candidate Resume:
    {resume_text}
    """
    
    # The Retry Loop
    for attempt in range(max_retries):
        try:
            print(f"      [AI] Calling Google Gemini API (Attempt {attempt + 1})...")
            response = client.models.generate_content(
                model='gemini-2.0-flash', # <-- Change this line to 2.0-flash!                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                )
            )
            print("      [AI] Response received from Google!")
            
            result_dict = json.loads(response.text)
            print("      [AI] JSON successfully parsed!")
            return result_dict
            
        except Exception as e:
            error_msg = str(e)
            print(f"      [AI ERROR]: {error_msg}")
            
            # If we hit a rate limit (429) and haven't run out of retries
            if "429" in error_msg and attempt < max_retries - 1:
                sleep_time = 15 # Wait 15 seconds to let the Google API cool down
                print(f"      [AI] API limit hit. Pausing for {sleep_time} seconds before retrying...")
                time.sleep(sleep_time)
                continue
                
            # If it's a different error (like a bad PDF) or we are out of retries, fail gracefully
            return None