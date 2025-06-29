import requests
import os
import re



SERPAPI_KEY = "005f7be521005ec0bad704ee2c79703aec69885090b71a3468cbbe1063189666"

def extract_key_terms(job_description):
    """Extract key search terms from job description"""
    # Common ML/AI terms that appear in LinkedIn profiles
    ml_terms = [
        "machine learning", "ML", "AI", "artificial intelligence", 
        "neural networks", "deep learning", "LLM", "large language models",
        "code generation", "developer tools", "software engineer",
        "Mountain View", "San Francisco", "Bay Area",
        # Additional ML/AI terms
        "data science", "data scientist", "ML engineer", "AI engineer",
        "machine learning engineer", "deep learning engineer", "NLP", "natural language processing",
        "computer vision", "CV", "reinforcement learning", "RL", "transformers",
        "BERT", "GPT", "OpenAI", "PyTorch", "TensorFlow", "scikit-learn",
        "pandas", "numpy", "matplotlib", "seaborn", "Jupyter", "notebooks",
        "model training", "model deployment", "MLOps", "ML Ops", "model serving",
        "feature engineering", "hyperparameter tuning", "cross-validation",
        "gradient boosting", "XGBoost", "LightGBM", "random forest", "SVM",
        "clustering", "classification", "regression", "supervised learning",
        "unsupervised learning", "semi-supervised learning", "transfer learning",
        "ensemble methods", "neural network", "CNN", "RNN", "LSTM", "GRU",
        "attention mechanism", "self-attention", "multi-head attention",
        "generative AI", "GAN", "VAE", "diffusion models", "stable diffusion",
        "prompt engineering", "fine-tuning", "pre-trained models",
        "distributed training", "GPU", "TPU", "cloud computing", "AWS", "GCP", "Azure",
        "Kubernetes", "Docker", "microservices", "API development",
        "software architecture", "system design", "scalability", "performance optimization"
    ]
    
    # Extract company names
    companies = [
        # AI/ML Companies
        "Windsurf", "Codeium", "Cursor", "Copilot", "ChatGPT", "OpenAI", "Anthropic", "Claude",
        "Google", "DeepMind", "Microsoft", "Azure", "Amazon", "AWS", "Meta", "Facebook",
        "Apple", "Tesla", "NVIDIA", "Intel", "AMD", "IBM", "Watson", "Palantir",
        "Databricks", "Snowflake", "MongoDB", "Elastic", "Splunk", "Tableau", "PowerBI",
        "Hugging Face", "Stability AI", "Midjourney", "DALL-E", "Jasper", "Copy.ai",
        "Scale AI", "Labelbox", "Weights & Biases", "MLflow", "Kubeflow", "Ray",
        "Cohere", "AI21", "Aleph Alpha", "Character.ai", "Replika", "Synthesia",
        "Runway", "Descript", "ElevenLabs", "Whisper", "AssemblyAI", "Speechmatics",
        "Cresta", "Gong", "Chorus", "Salesforce", "Einstein", "Oracle", "SAP",
        "Adobe", "Creative Suite", "Figma", "Notion", "Airtable", "Zapier",
        "Stripe", "Square", "PayPal", "Venmo", "Robinhood", "Coinbase", "Binance",
        "Uber", "Lyft", "DoorDash", "Instacart", "Airbnb", "Booking.com", "Expedia",
        "Netflix", "Spotify", "TikTok", "Snapchat", "Discord", "Slack", "Zoom",
        "Twilio", "SendGrid", "Mailchimp", "HubSpot", "Marketo", "Pardot",
        "Shopify", "WooCommerce", "Magento", "BigCommerce", "Squarespace", "Wix",
        "GitHub", "GitLab", "Bitbucket", "Atlassian", "Jira", "Confluence", "Trello",
        "Linear", "Notion", "Airtable", "Figma", "Canva", "Miro", "Loom",
        "Dropbox", "Box", "OneDrive", "Google Drive", "iCloud", "Evernote",
        "Asana", "Monday.com", "ClickUp", "Basecamp", "Smartsheet", "Airtable",
        "Zendesk", "Intercom", "Drift", "Crisp", "Freshdesk", "Help Scout",
        "PagerDuty", "Datadog", "New Relic", "Sentry", "LogRocket", "Amplitude",
        "Mixpanel", "Google Analytics", "Hotjar", "FullStory", "Lucky Orange",
        "Calendly", "Acuity", "Cal.com", "When2meet", "Doodle", "SurveyMonkey",
        "Typeform", "Google Forms", "Qualtrics", "Hotjar", "UserTesting",
        "Optimizely", "VWO", "Google Optimize", "AB Tasty", "Convert",
        "Segment", "RudderStack", "Amplitude", "Mixpanel", "PostHog", "Heap",
        "Klaviyo", "Mailchimp", "ConvertKit", "ActiveCampaign", "Drip",
        "Kajabi", "Teachable", "Thinkific", "Podia", "Gumroad", "Patreon",
        "Substack", "Medium", "Dev.to", "Hashnode", "Ghost", "WordPress",
        "Webflow", "Bubble", "Glide", "Adalo", "Retool", "Zapier", "Make",
        "n8n", "Integromat", "IFTTT", "Pipedream", "Tray.io", "Workato"
    ]
    
    # Create a focused search query
    key_terms = []
    job_lower = job_description.lower()
    
    for term in ml_terms:
        if term.lower() in job_lower:
            key_terms.append(term)
    
    for company in companies:
        if company.lower() in job_lower:
            key_terms.append(company)
    
    # If no specific terms found, use basic terms
    if not key_terms:
        key_terms = ["backend", "python", "consultant", "developer"]
    
    return key_terms[:3]  # Limit to top 3 terms

def search_candidates(job_description):
    if not SERPAPI_KEY:
        print("Error: SERPAPI_KEY environment variable not set")
        return []
    
    # Extract key terms for a more targeted search
    key_terms = extract_key_terms(job_description)
    search_terms = " ".join(key_terms)
    
    all_results = []
    
    # Primary search with specific terms
    query = f'site:linkedin.com/in "{search_terms}"'
    print(f"Primary search with query: {query}")
    
    results = perform_search(query, 50)
    all_results.extend(results)
    
    # If we don't have enough results, try broader searches
    if len(all_results) < 10:
        print(f"Only found {len(all_results)} candidates, trying broader searches...")
        
        # Try with just ML terms
        ml_query = f'site:linkedin.com/in "machine learning" "AI" "data scientist"'
        print(f"Broad ML search: {ml_query}")
        additional_results = perform_search(ml_query, 30)
        all_results.extend(additional_results)
        
        # Try with location-based search
        if len(all_results) < 10:
            location_query = f'site:linkedin.com/in "San Francisco" "Mountain View" "Bay Area" "software engineer"'
            print(f"Location-based search: {location_query}")
            additional_results = perform_search(location_query, 30)
            all_results.extend(additional_results)
    
    # Remove duplicates based on LinkedIn URL
    unique_results = []
    seen_urls = set()
    for result in all_results:
        if result["linkedin_url"] not in seen_urls:
            unique_results.append(result)
            seen_urls.add(result["linkedin_url"])
    
    print(f"Found {len(unique_results)} unique LinkedIn profiles")
    return unique_results[:15]  # Return up to 15 candidates

def perform_search(query, num_results):
    """Helper function to perform a single search"""
    url = "https://serpapi.com/search.json"
    params = {
        "q": query,
        "engine": "google",
        "api_key": SERPAPI_KEY,
        "num": num_results
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if "error" in data:
            print(f"SerpAPI Error: {data['error']}")
            return []
            
        results = []
        for res in data.get("organic_results", []):
            link = res.get("link", "")
            title = res.get("title", "")
            if "linkedin.com/in" in link:
                results.append({
                    "name": title.split("|")[0].strip(),
                    "linkedin_url": link,
                    "headline": title.strip()
                })
        
        return results
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []