# linkedin_sourcing_agent/main.py
import json
from job_input import get_job_description
from search_engine import search_candidates
from scoring_engine import score_candidates
from message_generator import generate_messages


def main():
    """Main function to run the LinkedIn sourcing agent"""
    job_description = get_job_description()
    candidates = search_candidates(job_description)
    scored = score_candidates(candidates, job_description)
    messages = generate_messages(scored[:10], job_description)

    # Create the final output structure
    output_data = {
        "job_id": "backend-fintech-sf",
        "job_description": job_description,
        "candidates_found": len(candidates),
        "top_candidates": []
    }

    # Add each candidate with their detailed information
    for message_data in messages:
        candidate_info = {
            "name": message_data["candidate_name"],
            "linkedin_url": message_data["linkedin_url"],
            "fit_score": message_data["fit_score"],
            "score_breakdown": message_data["score_breakdown"],
            "key_matches": message_data["key_matches"],
            "outreach_message": message_data["outreach_message"]
        }
        output_data["top_candidates"].append(candidate_info)

    # Save to JSON file with proper formatting
    with open("candidates_output.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print("Output saved to candidates_output.json")
    print(json.dumps(output_data, indent=2, ensure_ascii=False))
    
    return output_data

if __name__ == "__main__":
    main()

