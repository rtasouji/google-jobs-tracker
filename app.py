import streamlit as st
import requests
import pandas as pd
from collections import defaultdict, Counter

# Your SerpApi Key
SERP_API_KEY = st.secrets["SERP_API_KEY"]

# Function to fetch job listings from Google Jobs API
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

# Function to extract job sources & calculate average positions
def extract_job_sources_and_positions(jobs):
    sources_count = Counter()  # Track count of each website
    sources_positions = defaultdict(list)  # Track positions of each website

    for job in jobs:
        if "apply_options" in job:
            for idx, option in enumerate(job["apply_options"], start=1):
                website = option["title"]
                sources_count[website] += 1
                sources_positions[website].append(idx)  # Store the position

    # Calculate average position for each website
    sources_avg_position = {
        website: round(sum(positions) / len(positions), 2)
        for website, positions in sources_positions.items()
    }

    return sources_count, sources_avg_position

# Streamlit UI
st.title("Google Jobs Tracker")
job_query = st.text_input("Enter Job Title:", "Software Engineer")
location = st.text_input("Enter Location:", "United States")

if st.button("Fetch Job Listings"):
    jobs = get_google_jobs_results(job_query, location)
    sources_count, sources_avg_position = extract_job_sources_and_positions(jobs)

    if sources_count:
        # Convert data to a DataFrame
        website_data = pd.DataFrame(
            {
                "Website": sources_count.keys(),
                "Job Listings": sources_count.values(),
                "Avg. Position": [sources_avg_position[site] for site in sources_count.keys()]
            }
        )

        st.write("### Website Share of Google Jobs Results")
        st.dataframe(website_data)

        # Visualize data
        st.bar_chart(website_data.set_index("Website")["Job Listings"])
    else:
        st.write("No job results found. Try a different query.")
