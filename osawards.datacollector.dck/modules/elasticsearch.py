import json
import logging
import os
import requests
import warnings

import pandas as pd

import modules.constants as constants
from elasticsearch import Elasticsearch, ElasticsearchWarning
from elasticsearch.helpers import bulk

# Supress the security warning
warnings.filterwarnings("ignore", category = ElasticsearchWarning)


# Function: Create indices
def create_index(file_element: str, expected_colums: list, filters: dict, country_limit: int) -> tuple:
    """Function to create the indices in Elasticsearch."""
    
    field_list = []
    try:
        # Connect to Elasticsearch
        logging.info('Data Collector / Elastic />  Connecting to Elasticsearch...')
        elastic = Elasticsearch(os.getenv('ELASTICSEARCH_URL'))
        logging.info('Data Collector / Elastic />  Connection established!')

        # Split the path to build the index name
        base = os.path.basename(file_element)
        name = os.path.splitext(base)[0]
        _, extension = os.path.splitext(base)
                    
        # Load the file in a DataFrame
        df = pd.read_csv(file_element, sep=',', keep_default_na=False)

        # Validate the columns are the expected
        for col in df.columns.tolist():
            if col not in expected_colums:
                raise Exception(f'The data file contains invalid columns -> {col}')

        # Apply filters if needed
        if filters is not None:
            logging.info('Data Collector / Elastic />  Applying filters...')

            # Filter the DataFrame by countries (if needed)
            if filters["countries"] and os.getenv('DC_COUNTRIES'):
                df = filter_dataframe_by_countries(df, os.getenv('DC_COUNTRIES').split(','))

            # Normalize the data
            df = normalize_data(df)

            # Filter the DataFrame by limits
            if filters["lower_year_limit"] and filters["lower_year_limit"] > 0 and filters["upper_year_limit"] and filters["upper_year_limit"] > 0:
                df = filter_dataframe_by_limits(df,
                                                filters["lower_year_limit"],
                                                filters["upper_year_limit"],
                                                country_limit)

        # Build a new column "country" with the mapped "country_code" value
        df = add_complementary_columns(df, "country", "country_code")

        # Upload the data to Elasticsearch
        if df is not None:
            # Define the index where the data will be stored
            index_name = name + '_index'
            field_list = df.columns
                
            # Convert the DataFrame to JSON
            df_json = df.to_dict(orient='records')

            # Remove the previous index (if exists)
            elastic.indices.delete(index=index_name, ignore_unavailable=True)

            # (Re)Create the index
            for record in df_json:
                elastic.index(index=index_name, body=record)
            logging.info(f'Data Collector / Elastic />  Index -> {index_name} (created)')
        return index_name, field_list
    except Exception as error:
        raise


# Function: Create an index pattern
def create_index_pattern(index_name: str, definition: dict):
    """Function to create and index pattern."""

    try:
        logging.info(f'Data Collector / Elastic />  Creating the index pattern for "{index_name}"...')
        url = os.getenv('ELASTICSEARCH_URL') + '/.kibana/_doc/index-pattern:' + index_name
        response = requests.post(url, headers = {'Content-Type': 'application/json'}, data = json.dumps(definition))
        if not response.status_code in (200, 201):
            raise ValueError('Data Collector / Elastic />   An error occurred creating the index pattern!')

        logging.info(f'Data Collector / Elastic />  The index pattern for "{index_name}" was created successfully!')
        return index_name
    except Exception as error:
       raise


# Function: Create a Kibiter Visual Object (Visualization / Dashboard)
def create_kibiter_visual_object(template: dict, is_visualization: bool):
    """Function to create a Kibiter Visual Object (Visualization / Dashboard)."""

    try:
        # Define the the logText and the final URL
        log_text = constants.DASHBOARD if not is_visualization else constants.VISUALIZATION
        url = os.getenv('ELASTICSEARCH_URL') + '/.kibana/_doc/' + log_text + ':' + template[log_text]['title']
        
        # Create the object
        logging.info(f'Data Collector / Elastic />  Creating the {log_text}...')
        if template:
            headers = {'Content-Type': 'application/json'}
            response = requests.put(url, headers=headers, data=json.dumps(template))
            if not response.status_code in (200, 201):
                raise ValueError(f'Data Collector / Elastic />  An error occurred creating the {log_text}!')
            logging.info(f'Data Collector / Elastic />  The {log_text} was created successfully!')
    except Exception as error:
       raise


# Function: Remove Kibiter Visual Objects (Index pattern / Visualization / Dashboard)
def remove_kibiter_visual_objects(definition: list):
    """Function to remove Kibiter Visual Objects (Index pattern / Visualization / Dashboard)."""

    try:
        # Remove the dashboard object
        dashboard = definition[3]['dashboard']['title']
        logging.info(f'Data Collector / Elastic />  Removing the dashboard object -> {dashboard}...')
        url = os.getenv('KIBITER_URL') + f'/api/saved_objects/dashboard/{dashboard}'
        response = requests.delete(url, headers={"kbn-xsrf": "true"})
        if response.status_code == 200:
            # Remove the visualization object
            visualization = definition[2]['visualization']['title']
            logging.info(f'Data Collector / Elastic />  Removing the visualization object -> {visualization}...')
            url = os.getenv('KIBITER_URL') + f'/api/saved_objects/visualization/{visualization}'
            response = requests.delete(url, headers={"kbn-xsrf": "true"})
            if response.status_code == 200:
                # Remove the index pattern object
                index_pattern = definition[1]['index-pattern']['title']
                logging.info(f'Data Collector / Elastic />  Removing the index pattern object -> {index_pattern}...')
                url = os.getenv('KIBITER_URL') + f'/api/saved_objects/index-pattern/{index_pattern}'
                response = requests.delete(url, headers={"kbn-xsrf": "true"})
    except Exception as error:
       raise


# Function: Normalize the data
def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
    """Function to normalize the data."""

    # Normalize the "country_code" column
    logging.info(f'Data Collector / Elastic /> Normalizing data -> "country_code" column...')
    df = df[df["country_code"].notna() & (df["country_code"].astype(str).str.strip() != "") & (df["country_code"] != "\\N")]

    # Normalize the last column
    logging.info(f'Data Collector / Elastic /> Normalizing data -> last column...')
    last_column_name = df.columns[-1]
    df = df[df[last_column_name].notna() & (df[last_column_name].astype(str).str.strip() != "") & (df[last_column_name] != "\\N")]
    df[last_column_name] = df[last_column_name].astype(float)
    
    # Return the normalized DataFrame
    return df


# Function: Filter a DataFrame by countries
def filter_dataframe_by_countries(df: pd.DataFrame, countries: list) -> pd.DataFrame:
    """Function to filter a DataFrame by countries."""

    # Remove the rows with empty "country_code"
    logging.info(f'Data Collector / Elastic /> Filtering the DataFrame by countries...')
    df_filtered = df[df["country_code"] == ""]
    df_filtered = df[df['country_code'].isin(countries)]
    
    # Return the filtered DataFrame
    return df_filtered


# Function: Filter a DataFrame by limits
def filter_dataframe_by_limits(df: pd.DataFrame, inf_limit: int, top_limit: int, num_countries: int) -> pd.DataFrame:
    """Function to filter a DataFrame by limits."""

    # Remove the rows with empty "country_code"
    logging.info(f'Data Collector / Elastic /> Filtering the DataFrame by limits...')
    df_filtered = df[df["country_code"] != ""]

    # Filter by years
    df_filtered = df_filtered[(df_filtered["year"] >= inf_limit) & (df_filtered["year"] <= top_limit)]

    # Obtain the name of the last column
    last_column_name = df_filtered.columns[-1]

    # Obtain the top countries and obtain the final DataFrame
    sum_last_column = df_filtered.groupby("country_code")[last_column_name].sum()
    top_countries = sum_last_column.nlargest(num_countries).index.tolist()
    df_filtered = df_filtered[df_filtered["country_code"].isin(top_countries)]
    
    # Return the filtered DataFrame
    return df_filtered


# Function: Add complementary columns to a DataFrame
def add_complementary_columns(df: pd.DataFrame, new_column_name: str, left_column_name: str) -> pd.DataFrame:
    """Function to add some complementary columns to a DataFrame."""

    # Add the columns
    logging.info(f'Data Collector / Elastic /> Adding complementary columns...')
    new_column_index = df.columns.get_loc(left_column_name) + 1
    df[new_column_name] = df[left_column_name].map(constants.COUNTRIES)
    country_column = df.pop(new_column_name)
    df.insert(new_column_index, new_column_name, country_column)

    # Return the DataFrame
    return df
