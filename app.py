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
def extract_domains_and_positions(jobs):
    domain_count = Counter()  # Count how many times each domain appears
    domain_positions = defaultdict(list)  # Track positions of each domain

    for job in jobs:
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
                    domain_positions[domain].append(idx)  # Store the position

    # Calculate average position for each domain
    domain_avg_position = {
        domain: round(sum(positions) / len(positions), 2)
        for domain, positions in domain_positions.items()
    }

    return domain_count, domain_avg_position

# Streamlit UI
st.title("Google for Jobs Rank Monitor")
job_query = st.text_input("Enter Job Title:", "Software Engineer")
location = st.text_input("Enter Location:", "United States")

if st.button("Fetch Job Listings"):
    jobs = get_google_jobs_results(job_query, location)
    domain_count, domain_avg_position = extract_domains_and_positions(jobs)

    if domain_count:
        # Convert data to a DataFrame
        domain_data = pd.DataFrame(
            {
                "Domain": domain_count.keys(),
                "Job Listings": domain_count.values(),
                "Avg. Position": [domain_avg_position[site] for site in domain_count.keys()]
            }
        )

        # ✅ Sort the DataFrame by "Job Listings" in descending order
        domain_data = domain_data.sort_values(by="Job Listings", ascending=False)

        st.write("### Website Share of Google Jobs Results (By Domain)")
        st.dataframe(domain_data)

        # Visualize sorted data
        st.bar_chart(domain_data.set_index("Domain")["Job Listings"])
    else:
        st.write("No job results found. Try a different query.")
