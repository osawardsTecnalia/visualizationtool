import configparser
import json
import logging
import os

from modules import elasticsearch
from modules import sftp


# Create the config object and read .ini file
config = configparser.ConfigParser()
config.read('config/config.ini')

# Configure the logging level
logging.basicConfig(level = logging.INFO)
logging.getLogger("elastic_transport.transport").setLevel(logging.WARNING)


# Function: Retrieve files from the SFTP Server
def retrieve_from_SFTP_server(remote_directory: str, local_directory: str):
    """Function to retrieve files from the SFTP Server."""

    try:
        # Remove all the files from the local directory
        for file_name in os.listdir(local_directory):
            local_path = os.path.join(local_directory, file_name)
            if os.path.isfile(local_path):
                os.remove(local_path)

        # Download the files from the SFTP Server
        return sftp.get_files_from_directory(remote_directory, local_directory)
    except Exception as error:
        raise


# Function: Execute the process to collect the metrics
def execute_metrics_collection():
    """Function to execute the process to collect the metrics."""
    
    try:
        # Retrieve the template files from the SFTP Server
        logging.info('Data Collector / Main />  Process started!')
        logging.info('Data Collector / Main />  Retrieving the Template files...')
        template_list = retrieve_from_SFTP_server(os.getenv('SFTP_TEMPLATES_DIRECTORY'),
                                                  os.getenv('LOCAL_TEMPLATES_DIRECTORY'))
        logging.info(f'Data Collector / Main />  Downloaded  < {str(len(template_list))} >  Templates')
                    
        # Retrieve the data files from the SFTP Server
        logging.info('Data Collector />  Retrieving the Data Files...')
        file_list = retrieve_from_SFTP_server(os.getenv('SFTP_METRICS_DIRECTORY'),
                                              os.getenv('LOCAL_METRICS_DIRECTORY'))
        logging.info(f'Data Collector / Main />  Downloaded  <  {str(len(file_list))}  >  Data Files')
        
        # Load the files to Elasticsearch, and create the index and all the visual objects
        if file_list and len(file_list) > 0:
            for file_element in file_list:
                # Load the appropriate template
                file_name = os.path.splitext(file_element)[0]
                for template_element in template_list: 
                    template_name = os.path.splitext(os.path.basename(template_element))[0]
                    if template_name in file_name:
                        with open(template_element, 'r') as f:
                            definition = json.load(f)
                        break
                if definition and definition is not None:
                    # (Re)Create the index (if exists)
                    index, fieldList = elasticsearch.create_index(file_element, definition[0]['expected_fields'], definition[0]['filters'], definition[0]['country_limit'])
                    if index and not fieldList.empty:
                        elasticsearch.remove_kibiter_visual_objects(definition)
                        indexPattern = elasticsearch.create_index_pattern(index, definition[1])
                        if indexPattern:
                            # Create a visualization for each index pattern
                            elasticsearch.create_kibiter_visual_object(definition[2], True)
                              
                            # Create the dashboard
                            elasticsearch.create_kibiter_visual_object(definition[3], False)
                
            # Remove all the files in the directory
            sftp.remove_files_in_directory(os.getenv('SFTP_METRICS_DIRECTORY'))
            logging.info('Data Collector / Main />  Process completed!')
    except Exception as error:
        logging.error(str(error))


##### Main program #####
if __name__ == "__main__":
    # Welcome message
    logging.info('***************************************************************************')
    logging.info('*********************  OSAwards: Data Collector  **************************')
    logging.info('***************************************************************************')

    # Execute the process
    execute_metrics_collection()
