import streamlit as st
import requests
import pandas as pd
from collections import Counter

# Your SerpApi Key (Replace with your actual API key)
SERP_API_KEY = "46930cc44519939193e43455f1cb55a09588e2f533ba48db87257f5c725d7057"

# Function to fetch job results from Google Jobs API
def get_google_jobs_results(query, location="United States"):
    url = "https://serpapi.com/search"
    
    params = {
        "engine": "google_jobs",
        "q": query,
        "location": location,
        "hl": "en",
        "api_key": SERP_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    # 🛠️ Debug: Print Full API Response
    print("Full API Response:", data)

    return data.get("jobs_results", [])  # Ensure it correctly fetches job listings

# Function to extract job sources (websites)
from urllib.parse import urlparse


def extract_job_sources(jobs):
    sources = []

<<<<<<< HEAD
    for job in jobs:
        # 🛠️ Debug: Print job entry to check its structure
        print("🔍 Job Entry:", job)

        # 1️⃣ Extract domains from the 'apply_options' field
        if "apply_options" in job and isinstance(job["apply_options"], list):
            for source in job["apply_options"]:
                if "link" in source:
                    domain = urlparse(source["link"]).netloc  # Extract domain from URL
                    sources.append(domain)
        else:
            print("⚠️ Warning: 'apply_options' field missing in this job entry")

    # 🛠️ Debug: Print extracted job sources
    print("✅ Extracted Job Sources:", sources)
    return sources





# Streamlit UI
st.title("Google Jobs Tracker")
st.write("Track which websites rank in Google for Jobs for a specific role and location.")

# User inputs
job_query = st.text_input("Enter Job Title:", "Software Engineer")
location = st.text_input("Enter Location:", "United States")

if st.button("Fetch Job Listings"):
    jobs = get_google_jobs_results(job_query, location)
    
    # Extract job sources (websites)
    job_sources = extract_job_sources(jobs)

    if job_sources:
        # Count occurrences of each website
        website_counts = pd.DataFrame(pd.Series(job_sources).value_counts()).reset_index()
        website_counts.columns = ["Website", "Occurrences"]

        # Display results
        st.write(f"### Website Occurrences for '{job_query}' in {location}")
        st.dataframe(website_counts)

        # Show a bar chart for visualization
        st.bar_chart(website_counts.set_index("Website"))
    else:
        st.error("⚠️ No job listings found, or no sources detected. Try a different query.")
=======
# Function to calculate website share
def calculate_website_share(sources):
    source_counts = Counter(sources)
    total_jobs = sum(source_counts.values())
    
    share_data = [{"Website": website, "Job Listings": count, "Share (%)": round((count / total_jobs) * 100, 2)} for website, count in source_counts.items()]
    
    return pd.DataFrame(share_data)

# Streamlit UI
st.title("Google Jobs Tracker")
job_query = st.text_input("Enter Job Title:", "Software Engineer")
location = st.text_input("Enter Location:", "United States")

if st.button("Fetch Job Listings"):
    jobs = get_google_jobs_results(job_query, location)
    job_sources = extract_job_sources(jobs)
    
    if job_sources:
        website_share_df = calculate_website_share(job_sources)
        st.write("### Website Share of Google Jobs Results")
        st.dataframe(website_share_df)
        
        # Visualize data
        st.bar_chart(website_share_df.set_index("Website")["Share (%)"])
    else:
        st.write("No job results found. Try a different query.")
>>>>>>> 625d4d667a024f903da96fa0c44a38d466691dfb
