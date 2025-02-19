import streamlit as st
import requests
import pandas as pd
from collections import defaultdict, Counter
import tldextract  # Extracts domain and subdomain

# Display Logo
st.image("logo.png", width=200)  # Adjust width as needed

# Your SerpApi Key
SERP_API_KEY = st.secrets["SERP_API_KEY"]

# Function to fetch job listings from Google Jobs API
def get_google_jobs_results(query, location="Chicago, IL"):
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

# Function to extract job sources & company names
def extract_data(jobs):
    domain_count = Counter()  # Count how many times each domain appears
    domain_positions = defaultdict(list)  # Track positions of each domain
    company_count = Counter()  # Count how many times each company appears

    for job in jobs:
        # Track company names
        if "company_name" in job:
            company_name = job["company_name"]
            company_count[company_name] += 1

        # Track domains from "apply_options"
        if "apply_options" in job:
            for idx, option in enumerate(job["apply_options"], start=1):
                if "link" in option:
                    url = option["link"]
                    extracted = tldextract.extract(url)
                    
                    # Extract domain with subdomain (if any)
                    if extracted.subdomain:
                        domain = f"{extracted.subdomain}.{extracted.domain}.{extracted.suffix}"
                    else:
                        domain = f"{extracted.domain}.{extracted.suffix}"

                    # Store the count and position
                    domain_count[domain] += 1
                    domain_positions[domain].append(idx)

    # Calculate average position for each domain
    domain_avg_position = {
        domain: round(sum(positions) / len(positions), 2)
        for domain, positions in domain_positions.items()
    }

    return domain_count, domain_avg_position, company_count

# Streamlit UI
st.title("Google for Jobs Tracker")
job_query = st.text_input("Enter Job Title:", "Software Engineer")
location = st.text_input("Enter Location:", "United States")

if st.button("Fetch Job Listings"):
    jobs = get_google_jobs_results(job_query, location)
    domain_count, domain_avg_position, company_count = extract_data(jobs)

    if domain_count:
        # Convert data to a DataFrame for domain stats
        domain_data = pd.DataFrame(
            {
                "Domain": domain_count.keys(),
                "Job Listings": domain_count.values(),
                "Avg. Position": [domain_avg_position[site] for site in domain_count.keys()]
            }
        ).sort_values(by="Job Listings", ascending=False)  # Sort by job count

        st.write("### Website Share of Google Jobs Results (By Domain)")
        st.dataframe(domain_data.set_index("Domain"))  # ✅ Fix: Remove auto-index

    if company_count:
        # Convert data to a DataFrame for company stats
        company_data = pd.DataFrame(
            {
                "Company Name": company_count.keys(),
                "Job Listings": company_count.values()
            }
        ).sort_values(by="Job Listings", ascending=False)  # Sort by job count

        st.write("### Job Listings Count by Company")
        st.dataframe(company_data.set_index("Company Name"))  # ✅ Fix: Remove auto-index


    if not domain_count and not company_count:
        st.write("No job results found. Try a different query.")
