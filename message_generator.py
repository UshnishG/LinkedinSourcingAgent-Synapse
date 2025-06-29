import os
import google.generativeai as genai
import json



genai.configure(api_key="AIzaSyDiumfV9dSFOdkaNJjJRL-eHDXyTmd1x5Q")

def generate_messages(scored_candidates, job_description):
    messages = []
    model = genai.GenerativeModel("gemini-2.5-flash")

    for candidate in scored_candidates:
        prompt = f"""
You are a recruiter writing a personalized LinkedIn message. Analyze the candidate's profile and create a message that:

1. Highlights specific characteristics from their profile that match the job
2. Shows how their background aligns with the role requirements
3. Mentions specific skills, experience, or achievements that are relevant
4. Keeps the tone professional but warm
5. Ends with a clear call to action

Candidate Profile:
- Name: {candidate['name']}
- LinkedIn URL: {candidate['linkedin_url']}
- Score Breakdown: {json.dumps(candidate.get('breakdown', {}), indent=2)}

Job Description:
{job_description}

Write a concise, personalized message (max 200 words) that demonstrates you've reviewed their profile and shows why they'd be a great fit for this specific role.
Make sure that you don't put things to be filled in. Make it complete so we can copy and paste it to their profiles
"""

        try:
            response = model.generate_content(prompt)
            message = response.text.strip()
            
            # Create a structured message object
            message_data = {
                "candidate_name": candidate["name"],
                "linkedin_url": candidate["linkedin_url"],
                "fit_score": candidate.get("score", 0),
                "score_breakdown": candidate.get("breakdown", {}),
                "outreach_message": message,
                "key_matches": extract_key_matches(candidate, job_description)
            }
            
            messages.append(message_data)
            
        except Exception as e:
            print(f"Error generating message for {candidate['name']}: {e}")
            # Fallback message
            message_data = {
                "candidate_name": candidate["name"],
                "linkedin_url": candidate["linkedin_url"],
                "fit_score": candidate.get("score", 0),
                "score_breakdown": candidate.get("breakdown", {}),
                "outreach_message": f"Hi {candidate['name']}, I came across your profile and was impressed by your background. I think you'd be a great fit for our {job_description[:50]}... role. Would you be interested in learning more?",
                "key_matches": ["profile match", "relevant experience"]
            }
            messages.append(message_data)

    return messages

def extract_key_matches(candidate, job_description):
    """Extract key matching characteristics between candidate and job"""
    matches = []
    
    # Extract job requirements
    job_lower = job_description.lower()
    candidate_name = candidate['name'].lower()
    
    # Check for common matches
    if 'machine learning' in job_lower or 'ml' in job_lower:
        matches.append("ML/AI experience")
    if 'python' in job_lower:
        matches.append("Python skills")
    if 'aws' in job_lower or 'cloud' in job_lower:
        matches.append("Cloud experience")
    if 'senior' in job_lower:
        matches.append("Senior level experience")
    if 'mountain view' in job_lower or 'san francisco' in job_lower:
        matches.append("Bay Area location")
    if 'startup' in job_lower:
        matches.append("Startup experience")
    if 'fintech' in job_lower:
        matches.append("Fintech background")
    
    # Add score-based matches
    breakdown = candidate.get('breakdown', {})
    if breakdown.get('skills', 0) > 8:
        matches.append("Strong technical skills")
    if breakdown.get('company', 0) > 8:
        matches.append("Impressive company background")
    if breakdown.get('education', 0) > 8:
        matches.append("Strong educational background")
    
    return matches if matches else ["Profile match", "Relevant experience"]
