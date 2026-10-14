import logging
import os
import paramiko


# Function: Download all the files from a directory
def get_files_from_directory(remoteDirectory: str, localDirectory: str):
    """Function to retrieve all the files from a directory."""

    fileList = []
    try:
        # Retrieve the connection parameters
        conn = build_connection_parameters()

        # Create the SSH client
        client = build_ssh_client()

        # Open the SSH client
        client.connect(hostname = conn['hostname'],
                       port = conn['port'],
                       username = conn['username'],
                       password = conn['password'],
                       timeout = conn['timeout'])
        
        # Open the SFTP channel
        with client.open_sftp() as sftp:
            logging.info('Data Collector / SFTP /> Connection established!')
            for fileName in sftp.listdir(remoteDirectory):
                remotePath = f'{remoteDirectory}/{fileName}'
                localPath = os.path.join(localDirectory, fileName)
                logging.info(f'Data Collector / SFTP />  Downloading the file: {fileName} to {localPath}')
                sftp.get(remotePath, localPath)
                fileList.append(localPath)
    except Exception as error:
        raise
    finally:
    	# Close the client and return
        client.close()
        return fileList


# Function: Remove all the files in a directory
def remove_files_in_directory(remoteDirectory: str):
    """Function to remove all the files in a directory."""

    try:
        # Retrieve the connection parameters
        conn = build_connection_parameters()

        # Create the SSH client
        client = build_ssh_client()

        # Open the SSH client
        client.connect(hostname = conn['hostname'],
                       port = conn['port'],
                       username = conn['username'],
                       password = conn['password'],
                       timeout = conn['timeout'])
        
        # Open the SFTP channel
        with client.open_sftp() as sftp:
            logging.info('Data Collector / SFTP />  Connection established!')
            for nombre in sftp.listdir(remoteDirectory):
                path = os.path.join(remoteDirectory, nombre)
                sftp.remove(path)
    except Exception as error:
        raise
    finally:
    	# Close the client and return
        client.close()


#####################################################
###############  AUXILIARY FUNCTIONS  ###############
#####################################################


# Function: Build the connection parameters
def build_connection_parameters() -> dict:
    """Function to build the SFTP connection parameters."""

    return {
        'hostname': os.getenv('SFTP_HOST'),
        'port': int(os.getenv('SFTP_PORT')),
        'username': os.getenv('SFTP_USERNAME'),
        'password': os.getenv('SFTP_PASSWORD'),
        'timeout': int(os.getenv('SFTP_TIMEOUT'))
    }


# Function: Build the SSH client
def build_ssh_client() -> object:
    """Function to build the SSH client."""

    try:
        # Create the SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        return client
    except Exception as error:
        logging.error(str(error))
        raise
