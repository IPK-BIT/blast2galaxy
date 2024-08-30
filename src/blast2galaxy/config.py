from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib

from bioblend.galaxy import GalaxyInstance

from . import errors


class ConfigHolder:
    def __init__(self):
        self.config = {}


conf = ConfigHolder()

def get_conf():
    return conf.config

def set_config(config):
    global conf
    conf.config = config
    print('Set conf to: ', conf.config)


def add_server(server, server_url, api_key):
    if 'servers' not in conf.config:
        conf.config['servers'] = {}

    conf.config['servers'][server] = {
        'server_url': server_url,
        'api_key': api_key
    }

def add_profile(profile, server, tool):
    if 'profiles' not in conf.config:
        conf.config['profiles'] = {}

    conf.config['profiles'][profile] = {
        'server': server,
        'tool': tool
    }

def add_default_server(server_url, api_key):
    add_server('default', server_url, api_key)

def add_default_profile(server_id, tool):
    add_profile('default', server_id, tool)


def load_config_toml():

    if conf.config:
        return conf.config, False

    config_path_cwd = Path.cwd().joinpath('.blast2galaxy.toml')
    config_path_home_dir = Path.home().joinpath('.blast2galaxy.toml')

    try:
        with open(config_path_cwd, 'rb') as f:
            config = tomllib.load(f)
            return config, config_path_cwd
    except FileNotFoundError as e:
        try:
            with open(config_path_home_dir, 'rb') as f:
                config = tomllib.load(f)
                return config, config_path_home_dir
        except FileNotFoundError as e:
            err_msg = f'Could not find the config file  `.blast2galaxy.toml`  in the current working directory or in your home directory: {str(Path.home())}'
            raise errors.Blast2galaxyConfigFileError(err_msg)


def get_profile(server='default', profile=None):

    config, _ = load_config_toml()

    if profile:

        try:
            if profile in config['profiles'].keys():
                config_profile = config['profiles'][profile]
            else: # use default profile
                config_profile = config['profiles']['default']

            if config_profile['server'] in config['servers'].keys():
                config_server = config['servers'][ config_profile['server'] ]
            else:
                raise errors.Blast2galaxyConfigFileError(f'ERROR: The server `{server}` is not defined in the config TOML!')

            config_merged = config_server | config_profile

        except KeyError as e:
            err_msg = f'The profile `{profile}` could not be found in the configuration.'
            raise errors.Blast2galaxyConfigFileError(err_msg)

    else: # no profile given, just use server argument of get_profile()

        if server in config['servers'].keys():
            config_server = config['servers'][ server ]
            config_merged = config_server
        
        else:
            raise errors.Blast2galaxyConfigFileError(f'The server `{server}` is not defined in the config TOML file!')

    return config_merged



def get_galaxy_instance(server = 'default', profile=None):

    config = get_profile(server=server, profile=profile)

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