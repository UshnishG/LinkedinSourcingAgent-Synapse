# LinkedIn Sourcing Agent

An AI-powered LinkedIn candidate sourcing and outreach automation tool that finds, scores, and generates personalized messages for potential candidates.

## Features

- **Smart Candidate Search**: Uses SerpAPI to find relevant LinkedIn profiles
- **AI-Powered Scoring**: Leverages Google Gemini AI to score candidates across multiple dimensions
- **Personalized Outreach**: Generates customized LinkedIn messages for each candidate
- **Beautiful Web Interface**: Modern Flask web application with responsive design
- **Comprehensive Analysis**: Detailed score breakdowns and key matches

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Synapse
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up API keys (optional - the app includes default keys):
   - SerpAPI key for LinkedIn search
   - Google Gemini API key for AI scoring and message generation

## Usage

### Web Application (Recommended)

1. Start the Flask web server:
```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:5000`

3. Enter a job description or use the default one

4. Click "Start Sourcing" to begin the automated process

5. View results with detailed candidate analysis and outreach messages

### Command Line Interface

Run the original command-line version:
```bash
python main.py
```

## Web Interface Features

- **Modern UI**: Beautiful gradient design with smooth animations
- **Real-time Progress**: Visual progress indicators during processing
- **Detailed Results**: Complete candidate analysis with:
  - Fit scores (1-10 scale)
  - Score breakdowns (Education, Skills, Experience, etc.)
  - Key matches and qualifications
  - Personalized outreach messages
  - Direct LinkedIn profile links
- **Responsive Design**: Works on desktop and mobile devices

## API Endpoints

- `GET /` - Main search page
- `POST /search` - Submit job description and start sourcing
- `GET /results` - View results page
- `GET /api/results` - Get results as JSON

## Output Format

The application generates a comprehensive JSON output with:

```json
{
  "job_id": "job-20241230-143022",
  "job_description": "...",
  "candidates_found": 15,
  "top_candidates": [
    {
      "name": "John Doe",
      "linkedin_url": "https://linkedin.com/in/johndoe",
      "fit_score": 8.5,
      "score_breakdown": {
        "education": 8.0,
        "skills": 9.0,
        "experience": 7.5,
        "location": 8.0,
        "company": 8.5,
        "tenure": 7.0
      },
      "key_matches": ["ML/AI experience", "Python skills", "Bay Area location"],
      "outreach_message": "Personalized LinkedIn message..."
    }
  ]
}
```

## Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **AI**: Google Gemini AI
- **Search**: SerpAPI
- **Styling**: Custom CSS with gradients and animations

## Screenshots

The web interface includes:
- Beautiful gradient backgrounds
- Card-based candidate displays
- Interactive score breakdowns
- Professional outreach messages
- Direct LinkedIn integration

## License

This project is for educational and demonstration purposes. 