import google.generativeai as genai
import json
import os
   

# Configure Gemini API
genai.configure(api_key="AIzaSyDiumfV9dSFOdkaNJjJRL-eHDXyTmd1x5Q")
model = genai.GenerativeModel("gemini-2.0-flash")

def extract_job_info(job_description):
    """
    Extract job information from a string job description
    """
    if isinstance(job_description, dict):
        return job_description
    
    # Parse string job description to extract key information
    job_info = {
        "required_skills": [],
        "location": "",
        "industry": "",
        "title": ""
    }
    
    job_lower = job_description.lower()
    
    # Extract skills (common tech skills)
    tech_skills = [
        "python", "java", "javascript", "react", "node.js", "django", "flask", 
        "aws", "azure", "gcp", "docker", "kubernetes", "sql", "mongodb", 
        "redis", "kafka", "spark", "machine learning", "ai", "data science",
        "frontend", "backend", "full stack", "devops", "ci/cd", "git",
        "microservices", "api", "rest", "graphql", "typescript", "angular",
        "vue", "php", "ruby", "go", "rust", "scala", "c++", "c#", ".net"
    ]
    
    for skill in tech_skills:
        if skill in job_lower:
            job_info["required_skills"].append(skill)
    
    # Extract location
    location_indicators = ["location:", "based in", "in", "remote", "hybrid"]
    for indicator in location_indicators:
        if indicator in job_lower:
            # Simple extraction - could be improved with NLP
            start_idx = job_lower.find(indicator)
            if start_idx != -1:
                # Extract a reasonable amount of text after the indicator
                remaining_text = job_lower[start_idx + len(indicator):start_idx + len(indicator) + 50]
                # Clean up the extracted location
                location = remaining_text.split('.')[0].split(',')[0].strip()
                if location and len(location) > 2:
                    job_info["location"] = location
                    break
    
    # Extract industry
    industries = ["fintech", "healthcare", "ecommerce", "saas", "ai", "machine learning", "cybersecurity"]
    for industry in industries:
        if industry in job_lower:
            job_info["industry"] = industry
            break
    
    # Extract job title
    title_indicators = ["senior", "junior", "lead", "principal", "engineer", "developer", "architect"]
    for indicator in title_indicators:
        if indicator in job_lower:
            job_info["title"] = indicator
            break
    
    return job_info

def ai_score_candidate(candidate, job_description):
    """
    Use Gemini AI to score a candidate across all dimensions
    """
    prompt = f"""
You are an expert recruiter evaluating a candidate for a job position. Score the candidate from 1-10 on each dimension and provide a brief explanation.

Job Description: {job_description}

Candidate Information:
- Name: {candidate.get('name', 'N/A')}
- LinkedIn URL: {candidate.get('linkedin_url', 'N/A')}
- Headline: {candidate.get('headline', 'N/A')}
- Education: {candidate.get('education', [])}
- Experience: {candidate.get('experience', [])}
- Skills: {candidate.get('skills', [])}
- Location: {candidate.get('location', 'N/A')}

Scoring Rubric:
1. Education (20%): Elite schools (9-10), Strong schools (7-8), Standard universities (5-6)
2. Career Trajectory (20%): Steady growth (6-8), Limited progression (3-5)
3. Company Relevance (15%): Top tech companies (9-10), Relevant industry (7-8), Any experience (5-6)
4. Skills Match (25%): Perfect skill match (9-10), Strong overlap (7-8), Some relevant skills (5-6)
5. Location Match (10%): Exact city (10), Same metro (8), Remote-friendly (6)
6. Tenure (10%): 2-3 years average (9-10), 1-2 years (6-8), Job hopping (3-5)

Return ONLY a JSON object with this exact format:
{{
    "education": {{"score": 8.5, "explanation": "Graduated from Stanford with CS degree"}},
    "trajectory": {{"score": 7.0, "explanation": "Steady progression from junior to senior roles"}},
    "company": {{"score": 8.0, "explanation": "Experience at Google and relevant startups"}},
    "skills": {{"score": 9.0, "explanation": "Perfect match with Python, Django, AWS requirements"}},
    "location": {{"score": 8.0, "explanation": "Based in San Francisco, matches job location"}},
    "tenure": {{"score": 7.5, "explanation": "Average 2 years per role, good stability"}}
}}
"""

    try:
        response = model.generate_content(prompt)
        # Extract JSON from response
        response_text = response.text.strip()
        
        # Find JSON object in response
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        if start_idx != -1 and end_idx != 0:
            json_str = response_text[start_idx:end_idx]
            scores = json.loads(json_str)
            
            # Extract just the scores for the breakdown
            breakdown = {
                "education": scores["education"]["score"],
                "trajectory": scores["trajectory"]["score"],
                "company": scores["company"]["score"],
                "skills": scores["skills"]["score"],
                "location": scores["location"]["score"],
                "tenure": scores["tenure"]["score"]
            }
            
            return breakdown, scores
        else:
            raise ValueError("No JSON found in response")
            
    except Exception as e:
        print(f"AI scoring failed for {candidate.get('name', 'Unknown')}: {str(e)}")
        # Fallback to rule-based scoring
        return fallback_scoring(candidate, job_description)

def fallback_scoring(candidate, job_description):
    """
    Fallback rule-based scoring if AI fails
    """
    job_info = extract_job_info(job_description)
    
    # Simple rule-based scoring
    education_score = 6.0  # Default
    trajectory_score = 5.0
    company_score = 6.0
    skills_score = 7.0
    location_score = 6.0
    tenure_score = 5.0
    
    # Basic skills matching
    required_skills = job_info.get("required_skills", [])
    candidate_skills = candidate.get("skills", [])
    if required_skills and candidate_skills:
        matches = sum(1 for req in required_skills if any(req.lower() in skill.lower() for skill in candidate_skills))
        if matches > 0:
            skills_score = min(9.0, 6.0 + (matches / len(required_skills)) * 3)
    
    breakdown = {
        "education": education_score,
        "trajectory": trajectory_score,
        "company": company_score,
        "skills": skills_score,
        "location": location_score,
        "tenure": tenure_score,
    }
    
    return breakdown, None

def score_candidates(candidates, job_description):
    """
    Score candidates using AI-powered analysis with fallback
    """
    results = []
    
    for candidate in candidates:
        # Use AI for scoring
        breakdown, detailed_scores = ai_score_candidate(candidate, job_description)
        
        # Weights from rubric
        weights = {
            "education": 0.2,
            "trajectory": 0.2,
            "company": 0.15,
            "skills": 0.25,
            "location": 0.1,
            "tenure": 0.1
        }
        
        # Calculate weighted score
        score = sum(breakdown[k] * weights[k] for k in breakdown)
        
        result = {
            "name": candidate["name"],
            "linkedin_url": candidate["linkedin_url"],
            "score": round(score, 2),
            "breakdown": breakdown
        }
        
        # Add detailed explanations if available
        if detailed_scores:
            result["explanations"] = {
                k: v["explanation"] for k, v in detailed_scores.items()
            }
        
        results.append(result)
    
    # Sort by score in descending order
    results.sort(key=lambda x: x["score"], reverse=True)
    
    return results
