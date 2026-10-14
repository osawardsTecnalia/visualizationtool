from configparser import ConfigParser
from fastapi import status # type: ignore
from fastapi.responses import JSONResponse # type: ignore


# Function: Build a 200-OK response
def build_response_200(result: bool,
                       message: str) -> JSONResponse:
    """Function to build an OK response.

    Args:
        result (bool):The result to set as part of the output.
        message (str):The message to set as part of the output.

    Returns:
        JSONResponse

    """

    # Build the body
    body = {
        'code': status.HTTP_200_OK,
        'error': False,
        'result': result,
        'message': message
    }
    
    # Build and return the response
    return JSONResponse(
        content=body,
        status_code=status.HTTP_200_OK,
        headers={'Content-Type': 'application/json'}
    )


# Function: Build a 400-Bad request response
def build_response_400(message: str) -> JSONResponse:
    """Function to build a Bad Request response.

    Args:
        message (str): The error message to set as part of the output.

    Returns:
        JSONResponse

    """

    # Build the body
    body = {
        'code': status.HTTP_400_BAD_REQUEST,
        'error': True,
        'result': None,
        'message': message
    }
    
    # Build and return the response
    return JSONResponse(
        content=body,
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={'Content-Type': 'application/json'}
    )


# Function: Build a 401-Unauthorized request response
def build_response_401(properties: ConfigParser) -> JSONResponse:
    """Function to build an Unauthorized Request response.

    Args:
    	properties (ConfigParser): The content of the properties file.

    Returns:
        JSONResponse

    """

    # Build the body
    body = {
        'code': status.HTTP_401_UNAUTHORIZED,
        'error': False,
        'result': None,
        'message': properties['API-EXCEPTIONS']['api.exception.unauthorized']
    }
    
    # Build and return the response
    return JSONResponse(
        content=body,
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={'Content-Type': 'application/json'}
    )
