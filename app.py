from flask import Flask, render_template, request, jsonify, session
import json
import os
from datetime import datetime
from job_input import get_job_description  # assuming this is used elsewhere
from search_engine import search_candidates
from scoring_engine import score_candidates
from message_generator import generate_messages

app = Flask(__name__)
app.secret_key = " "  # Use env var for security

@app.route('/')
def index():
    """Main page with job description input"""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """Handle job search and candidate sourcing"""
    try:
        # Get job description from form
        job_description = request.form.get('job_description', '').strip()

        # Default description if not provided
        if not job_description:
            job_description = (
                "Software Engineer ML Research at Windsurf (Codeium) - Forbes AI 50 company "
                "building AI-powered developer tools. Train LLMs for code generation, "
                "$140-300k + equity, Mountain View. Machine learning, neural networks, "
                "large language models, code generation, developer tools."
            )

        # Store description in session
        session['job_description'] = job_description

        # Step 1: Search for candidates
        print("=== Starting Candidate Search ===")
        candidates = search_candidates(job_description)

        # Step 2: Score candidates
        print("=== Scoring Candidates ===")
        scored_candidates = score_candidates(candidates, job_description)

        # Step 3: Generate outreach messages for top 10
        print("=== Generating Outreach Messages ===")
        messages = generate_messages(scored_candidates[:10], job_description)

        # Final output structure
        output_data = {
            "job_id": f"job-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "job_description": job_description,
            "candidates_found": len(candidates),
            "top_candidates": []
        }

        # Add detailed info for each candidate
        for msg in messages:
            candidate_info = {
                "name": msg.get("candidate_name"),
                "linkedin_url": msg.get("linkedin_url"),
                "fit_score": msg.get("fit_score"),
                "score_breakdown": msg.get("score_breakdown"),
                "key_matches": msg.get("key_matches"),
                "outreach_message": msg.get("outreach_message")
            }
            output_data["top_candidates"].append(candidate_info)

        # Save to JSON
        output_file = "candidates_output.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        return jsonify({
            "success": True,
            "data": output_data,
            "message": f"Found {len(candidates)} candidates and generated {len(messages)} outreach messages"
        })

    except Exception as e:
        print(f"Error in /search: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/results')
def results():
    """Display results page"""
    return render_template('results.html')

@app.route('/api/results')
def api_results():
    """API endpoint to get the latest search results"""
    try:
        file_path = 'candidates_output.json'
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return jsonify({"success": True, "data": data})
        else:
            return jsonify({"success": False, "message": "No results found"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3030)
