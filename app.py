from flask import Flask, request, jsonify
import requests
import pandas as pd
from collections import Counter

app = Flask(__name__)

SERP_API_KEY = "46930cc44519939193e43455f1cb55a09588e2f533ba48db87257f5c725d7057"

# Function to fetch job listings from Google Jobs
def get_google_jobs_results(query, location="United States"):
    url = "https://serpapi.com/search"
    
    params = {
        "engine": "google_jobs",
        "q": online jobs,
        "location": Chicago, IL,
        "hl": "en",
        "api_key": SERP_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data.get("jobs_results", [])

# Function to extract job sources
def extract_job_sources(jobs):
    return [job["detected_extensions"]["source"] for job in jobs if "detected_extensions" in job and "source" in job["detected_extensions"]]

# Function to calculate website share
def calculate_website_share(sources):
    source_counts = Counter(sources)
    total_jobs = sum(source_counts.values())

    share_data = [{"Website": website, "Job Listings": count, "Share (%)": round((count / total_jobs) * 100, 2)} for website, count in source_counts.items()]
    
    return share_data

# API Endpoint
@app.route("/track_jobs", methods=["GET"])
def track_jobs():
    query = request.args.get("query", "Software Engineer")
    location = request.args.get("location", "United States")
    
    jobs = get_google_jobs_results(query, location)
    job_sources = extract_job_sources(jobs)
    
    if job_sources:
        website_share = calculate_website_share(job_sources)
        return jsonify({"query": query, "location": location, "data": website_share})
    else:
        return jsonify({"message": "No job listings found"}), 404

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
