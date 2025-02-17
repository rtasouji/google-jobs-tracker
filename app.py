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

    return data.get("jobs_results", [])

# Function to extract job sources
def extract_job_sources(jobs):
    return [job["detected_extensions"]["source"] for job in jobs if "detected_extensions" in job and "source" in job["detected_extensions"]]

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
