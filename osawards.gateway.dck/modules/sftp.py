import base64
import os
import paramiko # type: ignore
import stat

from modules.logging_config import logger
from pathlib import Path


#####################################################
#################  MAIN FUNCTIONS  ##################
#####################################################


# Function: Check if the SFTP Server is online
def hello() -> bool:
    """Function to check if the SFTP Server is online.

    Args:
    	None

    Returns:
        bool

    """

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
        client.open_sftp()
        
        # Close the SSH client and return
        client.close()
        return True
    except Exception as error:
        logger.error(str(error))
        return False


# Function: Rename a file
def rename_file(remote_source_file: str,
                remote_target_file: str) -> bool:
    """Function to check if a remote file exists.

    Args:
    	remote_source_file (str): The remote file to be renamed.
        remote_target_file (str): The new name for the remote source file.

    Returns:
        bool

    """

    try:
        if remote_source_file and remote_target_file:
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
            sftp = client.open_sftp()

            # Check if the source file exists
            result = True
            try:
                sftp.stat(remote_source_file)
            except FileNotFoundError:
                result = False
            except IOError:
                result = False
            
            # Check if the target file already exists
            if result:
                try:
                    sftp.stat(remote_target_file)
                except FileNotFoundError:
                    result = False
                except IOError:
                    result = False
            
                # Rename the file
                if not result:
                    try:
                        sftp.rename(remote_source_file,
                                    remote_target_file)
                        result = True
                    except Exception as e:
                        logger.error(e)
                        result = False
        
            # Close the SSH client and return
            client.close()
            return result
        return False
    except Exception as error:
        logger.error(str(error))
        raise


# Function: Retrieve all the files in a directory
def retrieve_files_in_directory(remote_directory: str) -> list:
    """Function to retrieve all the files in a directory.

    Args:
        remote_directory (str): The remote directory.
        remote_file (str): The remote file to be removed

    Returns:
        list

    """

    try:
        if remote_directory:
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
            sftp = client.open_sftp()
            
            # Retrieve the files the file
            result = False
            path = Path(remote_directory)
            try:
                result = sftp.listdir(str(path))
            except Exception as e:
                logger.error(e)
                result = None
        
            # Close the SSH client and return
            client.close()
            return result
        return False
    except Exception as error:
        logger.error(str(error))
        raise


# Function: Upload a file as a byte array
def upload_file(remote_directory: str,
                remote_file_name: str,
                remote_file_content: bytes) -> list:
    """Function to upload a file as a byte array.

    Args:
        remote_directory (str): The remote directory where the file has to be uploaded.
        remote_file_name (str): The name for the file to be uploaded.
        remote_file_content (bytes): The content of the file to be uploaded.

    Returns:
        list

    """

    try:
        if remote_directory and remote_file_name and remote_file_content:
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
            sftp = client.open_sftp()

            # Check if the directory exists using the "chdir()" trick
            # result[0] -> directory exists
            # result[1] -> file uploaded
            result = [True, False]
            try:
                sftp.chdir(remote_directory)
                sftp.chdir('..')
            except IOError:
                result[0] = False
            
            # Check if the file already exists
            if result[0]:
                # Upload the file and change the permissions
                remote_file_path = os.path.join(remote_directory,
                                                remote_file_name)
                with sftp.file(remote_file_path, 'wb') as f:
                    f.write(remote_file_content)
                sftp.chmod(remote_file_path, 0o755)
                result[1] = True

            # Close the SSH client and return
            client.close()
            return result
        return [False, False]
    except Exception as error:
        logger.error(str(error))
        raise


# Function: Remove a file
def remove_file(remote_directory: str,
                remote_file: str) -> bool:
    """Function to remove a file.

    Args:
        remote_directory (str): The remote directory where the file is allocated.
        remote_file (str): The remote file to be removed.

    Returns:
        bool

    """

    try:
        if remote_directory and remote_file:
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
            sftp = client.open_sftp()
            
            # Remove the file
            result = False
            path = Path(remote_directory) / remote_file
            try:
                sftp.remove(str(path))
                result = True
            except FileNotFoundError:
                result = False
            except PermissionError:
                result = False
        
            # Close the SSH client and return
            client.close()
            return result
        return False
    except Exception as error:
        logger.error(str(error))
        raise


# Function: Clear a directory
def clear_directory(remote_directory: str) -> bool:
    """Function to remove all the files in a directory.

    Args:
        remote_directory (str): The remote directory to be cleared.

    Returns:
        bool

    """

    try:
        if remote_directory:
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
            sftp = client.open_sftp()
            
            # Remove all the files
            result = False
            try:
                for entry in sftp.listdir_attr(str(remote_directory)):
                    path = Path(remote_directory) / entry.filename
                    if stat.S_ISREG(entry.st_mode):
                        sftp.remove(str(path))
                result = True
            except FileNotFoundError:
                result = False
            except PermissionError:
                result = False
        
            # Close the SSH client and return
            client.close()
            return result
        return False
    except Exception as error:
        logger.error(str(error))
        raise


# Function: Download a file
def download_file(remote_path: str):
    """Function to download a file."""

    try:
        if remote_path:
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
            sftp = client.open_sftp()

            # Divide the file path
            full_path = Path(remote_path)
            directory = str(full_path.parent)
            file_name = str(full_path.name)

            # Check if the directory exists using the "chdir()" trick
            # [0]: directory exists
            # [1]: file exists
            # [2]: file content
            result = [True, None, None]
            try:
                sftp.chdir(directory)
                sftp.chdir('..')
            except IOError:
                result[0] = False
            
            # Check if the file exists
            if result[0]:
                file_list = sftp.listdir(directory)
                result[1] = file_name in file_list
                if result[1]:
                    # Download the file
                    with sftp.file(str(full_path), 'rb') as remote_file:
                        result[2] = base64.b64encode(remote_file.read()).decode('utf-8')                        
            
            # Close the SSH client and return
            client.close()
            return result
        return [False, None, None]
    except Exception as error:
        raise


#####################################################
###############  AUXILIARY FUNCTIONS  ###############
#####################################################


# Function: Build the connection parameters
def build_connection_parameters() -> dict:
    """Function to build the SFTP connection parameters.

    Args:
    	None

    Returns:
        dict

    """

    return {
        'hostname': os.getenv('SFTP_HOST'),
        'port': int(os.getenv('SFTP_PORT')),
        'username': os.getenv('SFTP_USERNAME'),
        'password': os.getenv('SFTP_PASSWORD'),
        'timeout': int(os.getenv('SFTP_TIMEOUT'))
        }


# Function: Build the SSH client
def build_ssh_client() -> object:
    """Function to build the SSH client.

    Args:
    	None

    Returns:
        object

    """

    try:
        # Create the SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        return client
    except Exception as error:
        logger.error(str(error))
        raise
