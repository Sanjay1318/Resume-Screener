import json
import time
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables just in case
load_dotenv()

def analyze_resume_with_ai(resume_text, jd_text, max_retries=3):
    """
    Sends the resume and job description to Groq (LLaMA 3) for lightning-fast analysis.
    Returns structured JSON in 1-2 seconds.
    """
    # Initialize the Groq client pulling directly from your .env file
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    prompt = f"""
    You are an expert technical recruiter and Applicant Tracking System (ATS). 
    Compare the provided Candidate Resume against the Job Description.
    
    You MUST return your response as a valid, raw JSON object with the EXACT following structure. 

    {{
        "score": <int 0-100 based on overall quality and impact>,
        "ats_score": <int 0-100 based strictly on keyword matching, formatting, and parseability>,
        "matched_skills": ["skill1", "skill2"],
        "missing_skills": ["skill3"],
        "ai_summary": "<string 2-sentence summary>",
        "experience_match": "<string short sentence>",
        "education_match": "<string short sentence>",
        "certifications": ["cert1"],
        "recommendation": "<string Strong Hire, Potential Hire, or Do Not Hire>",
        "score_reason": "<string brief paragraph>",
        "interview_questions": ["q1", "q2", "q3"]
    }}

    Job Description:
    {jd_text}
    
    Candidate Resume:
    {resume_text}
    """

    for attempt in range(max_retries):
        try:
            # The Groq Chat Completion API
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a precise JSON-generating AI. Always output perfectly formatted JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.3-70b-versatile", # Groq's flagship fast model
                response_format={"type": "json_object"}, # Forces guaranteed JSON output!
                temperature=0.2, # Keeps the AI highly focused and analytical
            )
            
            raw_text = chat_completion.choices[0].message.content.strip()
            
            # Parse the text into a Python Dictionary
            parsed_data = json.loads(raw_text)
            return parsed_data
            
        except Exception as e:
            print(f"API Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print("Retrying in 2 seconds...")
                time.sleep(2)
            else:
                print("Max retries reached. AI Analysis failed.")
                return None