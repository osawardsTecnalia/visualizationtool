import requests
import os
import pandas as pd
from bs4 import BeautifulSoup # type: ignore
from datetime import datetime

from modules.logging_config import logger


# Constants
OSOR_TOPICS = {
   "Digital government": [
       "Business and competition",
        "Collaboration",
        "Demography and population",
        "Digital-ready policymaking",
        "Digital government",
        "eDelivery and eInvoicing",
        "eIdentity and eSignature",
        "eInclusion",
        "eParticipation and eVoting",
        "eProcurement",
        "European Policies",
        "Interoperable Europe policy",
        "Legal",
        "Observatories",
        "Smart cities",
        "Social",
        "Tools"
    ],
    "Economics": [
        "Banking and financial services",
        "Industry and production",
        "Taxation",
        "Trade"
    ],
    "Education": [
        "Culture and education",
        "Languages and translation",
        "Science and technology"
    ],
    "Energy and environment": [
       "Energy and environment"
    ],
    "Health": [
       "eHealth"
    ],
    "ICT": [
        "Content and knowledge management",
        "ICT",
        "ICT",
        "Licensing",
        "Open Source Software",
        "Reusable Software Components",
        "Semantics",
        "Standardisation",
        "Statistics and information"
    ],
    "Innovation": [
        "Advanced data analytics",
        "AI Chatbot",
        "AI Machine translation",
        "AI Named entity recognition",
        "Artificial intelligence",
        "Blockchain",
        "Digital innovation",
        "Extended reality",
        "High performance computing",
        "Internet of Things",
        "Optical Character Recognition",
        "Robotic Process Automation"
    ],
    "Transport": [
        "Geospatial",
        "Land transport",
        "Maritime and inland waterway transport"
    ]
}



#####################################################
#################  MAIN FUNCTIONS  ##################
#####################################################


# Function: Retreive the OSH projects
def call_osh_api(token: str, limit: int, offset: int) -> pd.DataFrame:

    headers = {"Authorization": f"Bearer {token}"}
    url = os.getenv("GATEWAY_OSH_URL").replace("{1}", str(limit)).replace("{2}", str(offset))
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        items = data.get("items", [])
        if not items:
            return pd.DataFrame()
        
        # Build the dataframe with the result
        df = pd.DataFrame(items)

        # Filter the dataframe
        df = df[['oshwaUid', 'country', 'projectName', 'projectWebsite', 'primaryType', 'additionalType', 'hardwareLicense', 'softwareLicense']]
        df['additionalType'] = df['additionalType'].apply(lambda x: x if isinstance(x, list) else ["Other"])

        # Rename the columns
        df = df.rename(columns={'country': 'country_code', 'projectName': 'project_name', 'projectWebsite': 'website', 'primaryType': 'primary_type', 'additionalType': 'additional_type', 'hardwareLicense': 'hardware_license', 'softwareLicense': 'software_license'})

        # Add/modify/remove columns
        df = df.replace('"', 'ʺ', regex=True)
        df['country_code'] = df['oshwaUid'].str[:2]
        df['additional_type'] = df['additional_type'].apply(transform_list_to_string)
        df["status_flag"] = 0
        df.drop('oshwaUid', axis=1, inplace=True)
         
        # Recursive call
        if len(items) < limit:
            return df
        else:
            next_df = call_osh_api(token, limit, offset + limit)
            return pd.concat([df, next_df], ignore_index=True)
    else:
        logger.info(f"Error: {response.status_code}")
        return pd.DataFrame()


# Function: Retreive the CERN Open-Hardware projects
def call_cern_api() -> pd.DataFrame:

    response = requests.get(os.getenv("GATEWAY_CERN_URL"))
    
    if response.status_code == 200:
        data = response.json()
        if not data:
            return pd.DataFrame()
        
        # Build the dataframe with the result
        df = pd.json_normalize(data)

        # Filter the dataframe
        df = df.query("visibility == 'public'")
        df = df[['name', 'created_at', 'web_url']]

        # Rename the columns
        df = df.rename(columns={'name': 'project_name', 'created_at': 'year', 'web_url': 'website'})

        # Add/modify/remove columns
        df['year'] = pd.to_datetime(df['year'])
        df['year'] = df['year'].dt.year
        df["country_code"] = "EU"
        df["status_flag"] = 0

        # Re-order
        df = df[['country_code', 'year', 'project_name', 'website', 'status_flag']]
         
        return df
    else:
        logger.info(f"Error: {response.status_code}")
        return pd.DataFrame()


# Function: Retreive the EC Open-Source Observatory solutions
def call_eu_osor_solutions() -> pd.DataFrame:
    return pd.DataFrame()


#####################################################
###############  AUXILIARY FUNCTIONS  ###############
#####################################################


# Function: Transform a list to a string
def transform_list_to_string(val: str) -> str:

    if isinstance(val, list):
        return "|".join(map(str, val))
    return str(val)


# Function: Extract an OSOR parsed article name
def extract_osor_parsed_article_name(article):

    h3 = article.select_one("h3.tile__title")
    return h3.get_text(" ", strip=True) if h3 else ""


# Function: Extract an OSOR parsed article description
def extract_osor_parsed_article_description(article):

    abstract = article.select_one("div.solution__abstract")
    return abstract.get_text(" ", strip=True) if abstract else ""


# Function: Extract an OSOR parsed article year
def extract_osor_parsed_article_year(article):

    date = next(
        (
            span.get_text(" ", strip=True).replace("Last update:", "").strip()
            for span in article.select("span.tile__info-text")
            if span.get_text(" ", strip=True).startswith("Last update:")
        ),
        ""
    )
    return datetime.strptime(date, "%d/%m/%Y").year


# Function: Extract an OSOR parsed article topics
def extract_osor_parsed_article_topics(article):

    topics = "|".join(
        badge.get_text(" ", strip=True)
        for badge in article.select(".badge")
    )
    topics_list = topics.split("|")
    if topics_list and topics_list[-1].startswith('+'):
        topics_list.pop()
    topics_list = topics_list[:2]

    for i in range(len(topics_list)):
        topic = topics_list[i]
        found = False
        if topic in OSOR_TOPICS:
            found = True
        if not found:
            for osor_topic, osor_subtopics in OSOR_TOPICS.items():
                if topic in osor_subtopics:
                    topics_list[i] = osor_topic
                    found = True
                    break
    if len(topics_list) == 2 and topics_list[0] == topics_list[1]:
        topics_list.pop()

    return topics_list


# Function: Extract OSOR articles
def extract_osor_articles(country_code, page):

    result = []
    while True:
        articles = request_osor_articles(country_code, page)
        if not articles:
            break

        for article in articles:
            topics = extract_osor_parsed_article_topics(article)
            article_obj = {
                "country_code": "00",
                "year": extract_osor_parsed_article_year(article),
                "name": extract_osor_parsed_article_name(article),
                "description": extract_osor_parsed_article_description(article),
                "primary_topic": topics[0] if len(topics) > 0 else None,
                "secondary_topic": topics[1] if len(topics) > 1 else None
            }
            result.append(article_obj)
        page += 1
    return result


# Function: Request for OSOR articles
def request_osor_articles(country_code, page):

    params = {
        "f[0]": "type:solution",
        "page": page
    }
    if country_code:
        params["f[1]"] = f"organisation_country:{country_code}"
    response = requests.get(os.getenv("GATEWAY_EC_OSOR_URL"), params=params, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.select("article.tile")
    
