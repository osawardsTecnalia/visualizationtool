# General imports
import base64
import configparser
import csv
import docker # type: ignore
import io
import json
import os
import uuid
import uvicorn # type: ignore
import pandas as pd

from datetime import datetime
from http.client import HTTPException

# Model imports
from model.api_response_model import ApiResponse
from model.metric_model import Metric
from model.report_model import Report
from model.user_story_model import UserStory
from model.invalid_api_key_exception_model import InvalidApiKeyException

# Modules imports
import modules.external as external
import modules.rest as rest
import modules.sftp as sftp
import modules.security as security
from modules.logging_config import logger

# FastAPI imports
from fastapi import FastAPI, Depends, Form, File, Header, Request, UploadFile # type: ignore
from fastapi.responses import JSONResponse, StreamingResponse # type: ignore
from fastapi.security import APIKeyHeader # type: ignore


# Create the config objects and read .ini and .properties files
config = configparser.ConfigParser()
config.read('config/config.ini')
properties = configparser.ConfigParser()
properties.read('properties/gateway.properties')


# Init API
app = FastAPI(
    title = properties['API-MESSAGES']['api.message.title'],
    version = config['API']['api.version'],
    description = properties['API-MESSAGES']['api.message.description'],
    root_path = config['API']['api.root.path'],
    docs_url = config['API']['api.docs.url'],
    openapi_url = config['API']['api.openapi.url']
)


# Register the custom exception handler
@app.exception_handler(InvalidApiKeyException)
async def invalid_api_key_exception_handler(_request: Request,
                                            _exc: InvalidApiKeyException) -> JSONResponse:
    """Custom exception handler to manage unauthorized accesses."""

    return rest.build_response_401(properties)


# API Function: Verify if the REST API is online
@app.get('/hello',
         summary='Check REST API online',
         tags=['Security and connectivity'],
         response_model=ApiResponse,
         status_code=200)
async def hello() -> JSONResponse:
    """API function to check if the REST API is online."""

    ###############################################################################
    #####        This function is used to check the health of the API         #####
    #####  No information logs are generated to avoid overloading the output  #####
    ###############################################################################
    
    # Create and return the OK response for welcome
    welcome_message = properties['API-MESSAGES']['api.message.welcome'].replace('{1}', config['API']['api.version'])
    return rest.build_response_200(True, welcome_message)


# API Function: Verify if the input SFTP Server is online
@app.get('/hello-server',
         summary='Check SFTP Server online',
         tags=['Security and connectivity'],
         response_model=ApiResponse,
         status_code=200)
async def hello_sftp_server(api_key: bool = Depends(security.verify_api_key)) -> JSONResponse:
    """API function to check if the input SFTP Server is online."""
    
    # Show info logs
    logger.info('')
    logger.info('****************************************************************')
    logger.info('****  OSAwards Gateway API  :: Version ' + config['API']['api.version'])
    logger.info('****  FUNCTION :: hello_sftp_server()')
    logger.info('****************************************************************')
    
    # Connect to the input SFTP Server
    message = properties['API-MESSAGES']['api.message.server.online']
    try:
        logger.info('  GATEWAY/> Connecting to the SFTP Server...')
        result = sftp.hello()
        if not result:
            message = properties['API-MESSAGES']['api.message.server.connection.problem']
        logger.info(f'  GATEWAY/> {message}')

        # Create the OK response
        response = rest.build_response_200(result, message)
    except Exception as cre:
        # Create an Unauthorized response
        response = rest.build_response_401(properties)

    # Return the response
    logger.info('')
    logger.info('****************************************************************')
    logger.info('')
    return response


#####################################################
###################  DATA FILES  ###################
#####################################################


# API Function: Retrieve all the stored indicators and data files
@app.get('/retrieve-stored-data-files',
          summary='Retrieve all the stored data files',
          tags=['Operations on Data Files'],
          response_model=ApiResponse,
          status_code=200)
async def retrieve_data_files(api_key: bool = Depends(security.verify_api_key)) -> JSONResponse:
    """API function to retrieve all the stored data files on the SFTP Server."""
    
    # Show info logs
    logger.info('')
    logger.info('****************************************************************')
    logger.info('****  OSAwards Gateway API  :: Version ' + config['API']['api.version'])
    logger.info('****  FUNCTION :: retrieve_data_files()')
    logger.info('****************************************************************')
    
    try:
        # Check the health of the SFTP Server
        logger.info('  GATEWAY/> Checking the health of the SFTP Server...')
        result = sftp.hello()
        if not result:
            raise Exception(properties['API-EXCEPTIONS']['api.exception.server.connection.health'])
        
        # Connect and upload the file
        result = sftp.retrieve_files_in_directory(os.getenv('SFTP_DIR_METRICS'))
        message = properties['API-MESSAGES']['api.message.server.retrieve.metric.files'] \
            if result is not None else \
                properties['API-MESSAGES']['api.message.server.retrieve.metric.files.problem']

        # Create the OK response
        response = rest.build_response_200(result, message)
    except Exception as error:
        # Create a Bad Request response
        response = rest.build_response_400(str(error))

    # Return the response
    logger.info('')
    logger.info('****************************************************************')
    logger.info('')
    return response


# API Function: Upload a data file to the SFTP Server
@app.post('/upload-data-file',
          summary='Upload a data file',
          tags=['Operations on Data Files'],
          response_model=ApiResponse,
          status_code=200)
async def upload_data_file(file: UploadFile = File(..., description='Data file to be uploaded to the SFTP Server.'),
                           data_file: Metric = Form(..., description="Selected data file"),
                           _: bool = Depends(security.verify_api_key)) -> JSONResponse:
    """API function to upload a data file to the SFTP Server."""
    
    # Show info logs
    logger.info('')
    logger.info('****************************************************************')
    logger.info('****  OSAwards Gateway API  :: Version ' + config['API']['api.version'])
    logger.info('****  FUNCTION :: upload_data_file()')
    logger.info('****************************************************************')
    
    try:
        # Check the file
        if not file or not file.filename:
            raise HTTPException(status_code=400, detail="No valid file uploaded")
        
        # Check the health of the SFTP Server
        logger.info('  GATEWAY/> Checking the health of the SFTP Server...')
        result = sftp.hello()
        if not result:
            raise Exception(properties['API-EXCEPTIONS']['api.exception.server.connection.health'])
        
        # Connect and upload the file
        content = await file.read()
        result = sftp.upload_file(os.getenv('SFTP_DIR_METRICS'), data_file.filename, content)
        if not result[0]:
            message = properties['API-MESSAGES']['api.message.server.directory.not.exists']
        else:
            message = properties['API-MESSAGES']['api.message.server.file.upload'] \
                if result[1] is not None else \
                    properties['API-MESSAGES']['api.message.server.file.upload.problem']

        # Create the OK response
        response = rest.build_response_200(result[1], message)
    except Exception as error:
        # Create a Bad Request response
        response = rest.build_response_400(str(error))

    # Return the response
    logger.info('')
    logger.info('****************************************************************')
    logger.info('')
    return response


# API Function: Remove a remote data file
@app.delete('/remove-data-file',
            summary='Remove a remote data file',
            tags=['Operations on Data Files'],
            response_model=ApiResponse,
            status_code=200)
async def remove_remote_data_file(data_file: Metric = Form(..., description="Data file to be removed"),
                                  _: bool = Depends(security.verify_api_key)) -> JSONResponse:
    """API function to remove a remote data file."""
    
    # Show info logs
    logger.info('')
    logger.info('****************************************************************')
    logger.info('****  OSAwards Gateway API  :: Version ' + config['API']['api.version'])
    logger.info('****  FUNCTION :: remove_remote_data_file()')
    logger.info('****************************************************************')
    
    try:
        # Check the health of the SFTP Server
        logger.info('  GATEWAY/> Checking the health of the SFTP Server...')
        result = sftp.hello()
        if not result:
            raise Exception(properties['API-EXCEPTIONS']['api.exception.server.connection.health'])
        
        # Connect and remove the file
        result = sftp.remove_file(os.getenv('SFTP_DIR_METRICS'),
                                  data_file.filename)
        message = properties['API-MESSAGES']['api.message.server.file.remove'] \
            if result else \
                properties['API-MESSAGES']['api.message.server.file.remove.problem']

        # Create the OK response
        response = rest.build_response_200(result, message)
    except Exception as error:
        # Create a Bad Request response
        response = rest.build_response_400(str(error))

    # Return the response
    logger.info('')
    logger.info('****************************************************************')
    logger.info('')
    return response


# API Function: Remove all the remote data files
@app.delete('/remove-all-data-files',
            summary='Remove all the remote data files',
            tags=['Operations on Data Files'],
            response_model=ApiResponse,
            status_code=200)
async def remove_remote_all_data_files(_: bool = Depends(security.verify_api_key)) -> JSONResponse:
    """API function to remove all the remote data files."""
    
    # Show info logs
    logger.info('')
    logger.info('****************************************************************')
    logger.info('****  OSAwards Gateway API  :: Version ' + config['API']['api.version'])
    logger.info('****  FUNCTION :: remove_remote_all_data_files()')
    logger.info('****************************************************************')
    
    try:
        # Check the health of the SFTP Server
        logger.info('  GATEWAY/> Checking the health of the SFTP Server...')
        result = sftp.hello()
        if not result:
            raise Exception(properties['API-EXCEPTIONS']['api.exception.server.connection.health'])
        
        # Connect and remove the file
        result = sftp.clear_directory(os.getenv('SFTP_DIR_METRICS'))
        message = properties['API-MESSAGES']['api.message.server.directory.clear'] \
            if result else \
                properties['API-MESSAGES']['api.message.server.directory.clear.problem']

        # Create the OK response
        response = rest.build_response_200(result, message)
    except Exception as error:
        # Create a Bad Request response
        response = rest.build_response_400(str(error))

    # Return the response
    logger.info('')
    logger.info('****************************************************************')
    logger.info('')
    return response


# API Function: Collect data
@app.get('/execute-data-collection',
         summary='Execute the data collection process',
         tags=['Operations on Data Files'],
         response_model=ApiResponse,
         status_code=200)
async def execute_data_collection(_: bool = Depends(security.verify_api_key)) -> JSONResponse:
    """API function to execute the data collection process."""
    
    # Show info logs
    logger.info('')
    logger.info('****************************************************************')
    logger.info('****  OSAwards Gateway API  :: Version ' + config['API']['api.version'])
    logger.info('****  FUNCTION :: execute_data_collection()')
    logger.info('****************************************************************')
    
    try:
        # Restart the DataCollector container to execute the process
        client = docker.from_env()
        container = client.containers.get(os.getenv("CONTAINER_DATA_COLLECTOR"))
        container.restart()

        # Wait until the end of the execution, and build the response message
        result = container.wait()
        message = properties['API-MESSAGES']['api.message.server.collect.data.ok']
        if not result or result['StatusCode'] != 0:
            raise Exception(properties['API-MESSAGES']['api.message.server.collect.data.problem'])

        # Create the OK response
        response = rest.build_response_200(True, message)
    except Exception as error:
        # Create a Bad Request response
        response = rest.build_response_400(str(error))

    # Return the response
    logger.info('')
    logger.info('****************************************************************')
    logger.info('')
    return response


#####################################################
################  EXTERNAL SOURCES  #################
#####################################################


# API Function: Retrieve Open-Source Hardware projects
@app.get('/retrieve-osh-projects',
         summary='Retrieve all the Open-Source Hardware projects',
         tags=['Operations on External Sources'],
         response_model=ApiResponse,
         status_code=200)
async def retrieve_osh_projects(osh_api_token: str) -> JSONResponse:
    """API function to retrieve all the Open-Source Hardware projects."""

    # Show info logs
    logger.info('')
    logger.info('****************************************************************')
    logger.info('****  OSAwards Gateway API  :: Version ' + config['API']['api.version'])
    logger.info('****  FUNCTION :: retrieve_osh_projects()')
    logger.info('****************************************************************')

    try:
        # Call to OSH API
        df = external.call_osh_api(
            osh_api_token.strip(),
            int(config['API']['api.osh.limit']),
            int(config['API']['api.osh.offset']))

        if df is None:
            # Create the OK response
            response = rest.build_response_200(False, properties['API-MESSAGES']['api.message.osh.no.data'])
        else:
            logger.info(f"Total number of records retrieved -> {len(df)}")
            
            # Create a buufer to store the CSV
            stream = io.StringIO()
            df.to_csv(stream, index=False, quoting=csv.QUOTE_ALL)
            
            # Create the OK response
            response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
            response.headers["Content-Disposition"] = "attachment; filename=osh_projects.csv"
    except Exception as error:
        # Create a Bad Request response
        response = rest.build_response_400(str(error))

    # Return the response
    logger.info('')
    logger.info('****************************************************************')
    logger.info('')
    return response


# API Function: Retrieve CERN Open-Hardware Repository
@app.get('/retrieve-cern-projects',
         summary='Retrieve all the CERN Open-Hardware projects',
         tags=['Operations on External Sources'],
         response_model=ApiResponse,
         status_code=200)
async def retrieve_cern_projects() -> JSONResponse:
    """API function to retrieve all the CERN Open-Hardware projects."""

    # Show info logs
    logger.info('')
    logger.info('****************************************************************')
    logger.info('****  OSAwards Gateway API  :: Version ' + config['API']['api.version'])
    logger.info('****  FUNCTION :: retrieve_cern_projects()')
    logger.info('****************************************************************')

    try:
        # Call to CERN API
        df = external.call_cern_api()

        if df is None:
            # Create the OK response
            response = rest.build_response_200(False, properties['API-MESSAGES']['api.message.cern.no.data'])
        else:
            logger.info(f"Total number of records retrieved -> {len(df)}")
            
            # Create a buufer to store the CSV
            stream = io.StringIO()
            df.to_csv(stream, index=False, quoting=csv.QUOTE_ALL)
            
            # Create the OK response
            response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
            response.headers["Content-Disposition"] = "attachment; filename=cern_projects.csv"
    except Exception as error:
        # Create a Bad Request response
        response = rest.build_response_400(str(error))

    # Return the response
    logger.info('')
    logger.info('****************************************************************')
    logger.info('')
    return response


# API Function: Retrieve EC Open-Source Observatory solutions
@app.get('/retrieve-ec-osor-solutions',
         summary='Retrieve all the EC Open-Source Observatory solutions',
         tags=['Operations on External Sources'],
         response_model=ApiResponse,
         status_code=200)
async def retrieve_ec_osor_solutions() -> JSONResponse:
    """API function to retrieve all the EC Open-Source Observatory solutions."""

    # Show info logs
    logger.info('')
    logger.info('****************************************************************')
    logger.info('****  OSAwards Gateway API  :: Version ' + config['API']['api.version'])
    logger.info('****  FUNCTION :: retrieve_ec_osor_solutions()')
    logger.info('****************************************************************')

    try:
        # Retrieve the solutions
        solutions = external.extract_osor_articles(None, 0)

        if not solutions:
            # Create the OK response
            response = rest.build_response_200(False, properties['API-MESSAGES']['api.message.osor.no.data'])
        else:
            logger.info(f"Total number of records retrieved -> {len(solutions)}")
            countries = json.loads(os.getenv("GATEWAY_EC_OSOR_COUNTRIES"))
            for key, value in countries.items():
                articles_by_country = external.extract_osor_articles(value, 0)
                if articles_by_country:
                    for article_by_country in articles_by_country:
                        for article in solutions:
                            if article_by_country["name"] == article["name"]:
                                article["country_code"] = key
                                break
            
            # Create the resulting Dataframe
            df = pd.DataFrame(solutions)

            # Adjust the Dataframe
            df = df.replace('"', 'ʺ', regex=True)
            df["status_flag"] = 0
            
            # Create a buufer to store the CSV
            stream = io.StringIO()
            df.to_csv(stream, index=False, quoting=csv.QUOTE_ALL)
            
            # Create the OK response
            response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
            response.headers["Content-Disposition"] = "attachment; filename=ec_osor_solutions.csv"
    except Exception as error:
        # Create a Bad Request response
        response = rest.build_response_400(str(error))

    # Return the response
    logger.info('')
    logger.info('****************************************************************')
    logger.info('')
    return response


#####################################################
##################  USER STORIES  ###################
#####################################################


# API Function: Retrieve all the User Stories
@app.get('/retrieve-user-stories',
         summary='Retrieve all the User Stories',
         tags=['Operations on User Stories'],
         response_model=ApiResponse,
         status_code=200)
async def retrieve_user_stories() -> JSONResponse:
    """API function to retrieve all the User Stories."""

    # Show info logs
    logger.info('')
    logger.info('****************************************************************')
    logger.info('****  OSAwards Gateway API  :: Version ' + config['API']['api.version'])
    logger.info('****  FUNCTION :: retrieve_user_stories()')
    logger.info('****************************************************************')

    try:
        # Check the health of the SFTP Server
        logger.info('  GATEWAY/> Checking the health of the SFTP Server...')
        result = sftp.hello()
        if not result:
            raise Exception(properties['API-EXCEPTIONS']['api.exception.server.connection.health'])
        
        # Download the User Stories file
        result = sftp.download_file(os.getenv('SFTP_FILE_USER_STORIES'))
        if not result or not result[0] or not result[1] or not result[2] or len(result[2]) == 0:
            raise Exception(properties['API-MESSAGES']['api.message.server.user.stories.problem'])
        
        # Convert the file content into a JSON object
        result = json.loads(base64.b64decode(result[2]).decode("utf-8").strip())

        # Create the OK response
        response = rest.build_response_200(result, properties['API-MESSAGES']['api.message.server.user.stories.ok'])
    except Exception as error:
        # Create a Bad Request response
        response = rest.build_response_400(str(error))

    # Return the response
    logger.info('')
    logger.info('****************************************************************')
    logger.info('')
    return response


# API Function: Add a new User Story
@app.post('/add-user-story',
          summary='Add a new User Story',
          tags=['Operations on User Stories'],
          response_model=ApiResponse,
          status_code=200)
async def add_user_story(user_story: UserStory = Form(..., description="User Story information"),
                         api_key: bool = Depends(security.verify_api_key)) -> JSONResponse:
    """API function to add a new User Story."""

    # Show info logs
    logger.info('')
    logger.info('****************************************************************')
    logger.info('****  OSAwards Gateway API  :: Version ' + config['API']['api.version'])
    logger.info('****  FUNCTION :: add_user_story()')
    logger.info('****************************************************************')

    try:
        # Check the health of the SFTP Server
        logger.info('  GATEWAY/> Checking the health of the SFTP Server...')
        result = sftp.hello()
        if not result:
            raise Exception(properties['API-EXCEPTIONS']['api.exception.server.connection.health'])
        
        # Build the dictionary for the new User Story
        date = datetime.now()
        formatted_date = date.strftime('%Y-%m-%d')
        new_user_story = {
            "id": str(uuid.uuid4()),
            "date": formatted_date,
            "description": user_story.description.strip(),
            "link": user_story.link.strip()
        }
        
        # Download the User Stories file
        result = sftp.download_file(os.getenv('SFTP_FILE_USER_STORIES'))
        if not result or not result[0] or not result[1] or not result[2] or len(result[2]) == 0:
            raise Exception(properties['API-MESSAGES']['api.message.server.user.stories.new.problem'])
        
        # Append the new User Story to the list
        result = json.loads(base64.b64decode(result[2]).decode("utf-8").strip())
        if not result:
            result = []
        result.append(new_user_story)

        # Sort the result
        sorted_result = sorted(result, key=lambda x: x['date'], reverse=True)

        # Upload the list of User Stories
        logger.info('  GATEWAY/> Uploading the file to the SFTP Server...')
        result = sftp.upload_file(os.getenv('SFTP_DIR_USER_STORIES'), os.getenv('SFTP_FILE_USER_STORIES'), json.dumps(sorted_result).encode('utf-8'))

        # Create the OK response
        response = rest.build_response_200(sorted_result, properties['API-MESSAGES']['api.message.server.user.stories.new.ok'])
    except Exception as error:
        # Create a Bad Request response
        response = rest.build_response_400(str(error))

    # Return the response
    logger.info('')
    logger.info('****************************************************************')
    logger.info('')
    return response


# API Function: Remove an existing User Story
@app.delete('/remove-user-story',
            summary='Remove an existing User Story',
            tags=['Operations on User Stories'],
            response_model=ApiResponse,
            status_code=200)
async def remove_user_story(id: str,
                            api_key: bool = Depends(security.verify_api_key)) -> JSONResponse:
    """API function to remove an existing User Story."""

    # Show info logs
    logger.info('')
    logger.info('****************************************************************')
    logger.info('****  OSAwards Gateway API  :: Version ' + config['API']['api.version'])
    logger.info('****  FUNCTION :: remove_user_story()')
    logger.info('****************************************************************')

    try:
        # Check the health of the SFTP Server
        logger.info('  GATEWAY/> Checking the health of the SFTP Server...')
        result = sftp.hello()
        if not result:
            raise Exception(properties['API-EXCEPTIONS']['api.exception.server.connection.health'])
        
        # Download the User Stories file
        result = sftp.download_file(os.getenv('SFTP_FILE_USER_STORIES'))
        if not result or not result[0] or not result[1] or not result[2] or len(result[2]) == 0:
            raise Exception(properties['API-MESSAGES']['api.message.server.user.stories.problem'])
        
        # Retrieve the list of User Stories
        user_stories = json.loads(base64.b64decode(result[2]).decode("utf-8").strip())

        # Find the User Story to remove, iterating through a copy of the list
        result = False
        if user_stories:
            for user_story in user_stories[:]:
                if user_story['id'] == str(id).strip():
                    user_stories.remove(user_story)
                    result = True
                    break
            
            # Upload the file with the updated information
            logger.info('  GATEWAY/> Uploading the file to the SFTP Server...')
            sftp.upload_file(os.getenv('SFTP_DIR_USER_STORIES'), os.getenv('SFTP_FILE_USER_STORIES'), json.dumps(user_stories).encode('utf-8'))

        # Create the OK response
        response = rest.build_response_200(result, 'OK')
    except Exception as error:
        # Create a Bad Request response
        response = rest.build_response_400(str(error))

    # Return the response
    logger.info('')
    logger.info('****************************************************************')
    logger.info('')
    return response



#####################################################
#####################  REPORTS  #####################
#####################################################


# API Function: Retrieve all the Reports
@app.get('/retrieve-reports',
         summary='Retrieve all the Reports',
         tags=['Operations on Reports'],
         response_model=ApiResponse,
         status_code=200)
async def retrieve_reports() -> JSONResponse:
    """API function to retrieve all the Reports."""

    try:
        # Check the health of the SFTP Server
        logger.info('  GATEWAY/> Checking the health of the SFTP Server...')
        result = sftp.hello()
        if not result:
            raise Exception(properties['API-EXCEPTIONS']['api.exception.server.connection.health'])

        # Download the Reports file
        result = sftp.download_file(os.getenv('SFTP_FILE_REPORTS'))
        if not result or not result[0] or not result[1] or not result[2] or len(result[2]) == 0:
            raise Exception(properties['API-MESSAGES']['api.message.server.reports.problem'])
        
        # Convert the file content into a JSON object
        result = json.loads(base64.b64decode(result[2]).decode("utf-8").strip())

        # Create the OK response
        response = rest.build_response_200(result, properties['API-MESSAGES']['api.message.server.reports.ok'])
    except Exception as error:
        # Create a Bad Request response
        response = rest.build_response_400(str(error))

    # Return the response
    logger.info('')
    logger.info('****************************************************************')
    logger.info('')
    return response


# API Function: Add a new Report
@app.post('/add-report',
          summary='Add a new Report',
          tags=['Operations on Reports'],
          response_model=ApiResponse,
          status_code=200)
async def add_report(report: Report = Form(..., description="Report information"),
                     api_key: bool = Depends(security.verify_api_key)) -> JSONResponse:
    """API function to add a new Report."""

    # Show info logs
    logger.info('')
    logger.info('****************************************************************')
    logger.info('****  OSAwards Gateway API  :: Version ' + config['API']['api.version'])
    logger.info('****  FUNCTION :: add_report()')
    logger.info('****************************************************************')

    try:
        # Check the health of the SFTP Server
        logger.info('  GATEWAY/> Checking the health of the SFTP Server...')
        result = sftp.hello()
        if not result:
            raise Exception(properties['API-EXCEPTIONS']['api.exception.server.connection.health'])
        
        # Build the dictionary for the new Report
        date = datetime.now()
        formatted_date = date.strftime('%Y-%m-%d')
        new_report = {
            "id": str(uuid.uuid4()),
            "date": formatted_date,
            "title": report.title.strip(),
            "description": report.description.strip(),
            "link": report.link.strip()
        }
        
        # Download the Reports file
        result = sftp.download_file(os.getenv('SFTP_FILE_REPORTS'))
        if not result or not result[0] or not result[1] or not result[2] or len(result[2]) == 0:
            raise Exception(properties['API-MESSAGES']['api.message.server.reports.new.problem'])
        
        # Append the new Report to the list
        result = json.loads(base64.b64decode(result[2]).decode("utf-8").strip())
        if not result:
            result = []
        result.append(new_report)

        # Sort the result
        sorted_result = sorted(result, key=lambda x: x['date'], reverse=True)

        # Upload the list of Reports
        logger.info('  GATEWAY/> Uploading the file to the SFTP Server...')
        sftp.upload_file(os.getenv('SFTP_DIR_REPORTS'), os.getenv('SFTP_FILE_REPORTS'), json.dumps(sorted_result).encode('utf-8'))

        # Create the OK response
        response = rest.build_response_200(sorted_result, properties['API-MESSAGES']['api.message.server.reports.new.ok'])
    except Exception as error:
        # Create a Bad Request response
        response = rest.build_response_400(str(error))

    # Return the response
    logger.info('')
    logger.info('****************************************************************')
    logger.info('')
    return response


# API Function: Remove an existing Report
@app.delete('/remove-report',
            summary='Remove an existing Report',
            tags=['Operations on Reports'],
            response_model=ApiResponse,
            status_code=200)
async def remove_report(id: str,
                        api_key: bool = Depends(security.verify_api_key)) -> JSONResponse:
    """API function to remove an existing Report."""

    # Show info logs
    logger.info('')
    logger.info('****************************************************************')
    logger.info('****  OSAwards Gateway API  :: Version ' + config['API']['api.version'])
    logger.info('****  FUNCTION :: remove_report()')
    logger.info('****************************************************************')

    try:
        # Check the health of the SFTP Server
        logger.info('  GATEWAY/> Checking the health of the SFTP Server...')
        result = sftp.hello()
        if not result:
            raise Exception(properties['API-EXCEPTIONS']['api.exception.server.connection.health'])
        
        # Download the Reports file
        result = sftp.download_file(os.getenv('SFTP_FILE_REPORTS'))
        if not result or not result[0] or not result[1] or not result[2] or len(result[2]) == 0:
            raise Exception(properties['API-MESSAGES']['api.message.server.reports.problem'])
        
        # Retrieve the list of Reports
        reports = json.loads(base64.b64decode(result[2]).decode("utf-8").strip())

        # Find the Report to remove, iterating through a copy of the list
        result = False
        if reports:
            for report in reports[:]:
                if report['id'] == str(id).strip():
                    reports.remove(report)
                    result = True
                    break
            
            # Upload the file with the updated information
            logger.info('  GATEWAY/> Uploading the file to the SFTP Server...')
            sftp.upload_file(os.getenv('SFTP_DIR_REPORTS'), os.getenv('SFTP_FILE_REPORTS'), json.dumps(reports).encode('utf-8'))

        # Create the OK response
        response = rest.build_response_200(result, 'OK')
    except Exception as error:
        # Create a Bad Request response
        response = rest.build_response_400(str(error))

    # Return the response
    logger.info('')
    logger.info('****************************************************************')
    logger.info('')
    return response


# Run app
if __name__ == '__main__':  # pragma: no cover
     uvicorn.run(app, host="0.0.0.0", port=5010)
