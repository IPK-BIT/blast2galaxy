import os
from pathlib import Path
import tomllib
import yaml
import json

from bioblend.galaxy import GalaxyInstance

def get_credentials():
    
    # Check for the environment variable
    server_url = os.getenv('GALAXY_SERVER_URL')
    api_key = os.getenv('GALAXY_API_KEY')
    
    if api_key:
        print("API key obtained from environment variable.")
        return api_key
    
    # If the environment variable is not set, check for the YAML file
    home_directory = os.path.expanduser('~')
    yaml_file_path = os.path.join(home_directory, 'blast2galaxy.config.yaml')
    
    if os.path.isfile(yaml_file_path):
        with open(yaml_file_path, 'r') as file:
            config = yaml.safe_load(file)
            if 'api_key' in config:
                print("API key obtained from YAML file.")
                return config['api_key']
            else:
                raise ValueError("API key not found in the YAML file.")
    else:
        raise FileNotFoundError("YAML configuration file not found.")
    
    # If neither is found, raise an exception
    raise EnvironmentError("API key not found in environment variable or YAML file.")


def get_user_home_dir():
    home_dir = str(Path.home())
    return home_dir


def get_config_toml_path():
    home_dir = get_user_home_dir()
    path_config = os.path.join(home_dir, '.blast2galaxy.toml')
    return path_config


def load_config_toml():
    path_config = get_config_toml_path()

    try:
        with open(path_config, 'rb') as f:
            config = tomllib.load(f)
            return config
    except FileNotFoundError as e:
        err_msg = 'Could not find the config file  .blast2galaxy.toml  in your home directory: ' + str(get_user_home_dir())
        raise Exception(err_msg) from e


def get_profile(server='default', profile=None):

    config = load_config_toml()
    #print(json.dumps(config, indent=4))
    #exit()

    if profile:

        if profile in config['profiles'].keys():
            config_profile = config['profiles'][profile]
        else: # use default profile
            config_profile = config['profiles']['default']

        if config_profile['server'] in config['servers'].keys():
            config_server = config['servers'][ config_profile['server'] ]
        else:
            exit(f'ERROR: The server `{server}` is not defined in the config TOML!')

        config_merged = config_server | config_profile

    else: # no profile given, just use server argument of get_profile()

        if server in config['servers'].keys():
            config_server = config['servers'][ server ]
            config_merged = config_server
        
        else:
            exit(f'ERROR: The server `{server}` is not defined in the config TOML!')

    # print('SERVER:')
    # print(config_server)
    # print('PROFILE:')
    # print(config_profile)
    # print('-'*150)
    # print('MERGED:')
    # print(json.dumps(config_merged, indent=2))

    return config_merged



def get_galaxy_instance(server = 'default', profile=None):

    config = get_profile(server=server, profile=profile)

    #print(config)
    #exit()

    try:
        if config['api_key']:
            gi = GalaxyInstance(
                url = str(config['server_url']),
                key = str(config['api_key'])
            )
        else:
            gi = GalaxyInstance(
                url = str(config['server_url']),
                email = str(config['email']),
                password = str(config['password'])
            )

    except:
        print('ERROR: Could not connect to Galaxy server: ', config['server_url'])
        exit()

    return gi



__all__ = ['load', 'get_profile', 'get_galaxy_instance']