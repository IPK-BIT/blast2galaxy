from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib

from bioblend.galaxy import GalaxyInstance


class ConfigHolder:
    def __init__(self):
        self.config = None


conf = ConfigHolder()

def get_conf():
    return conf.config

def set_config(config):
    global conf
    conf.config = config
    print('Set conf to: ', conf.config)


def load_config_toml():
    config_path_cwd = Path.cwd().joinpath('.blast2galaxy.toml')
    config_path_home_dir = Path.home().joinpath('.blast2galaxy.toml')

    try:
        with open(config_path_cwd, 'rb') as f:
            config = tomllib.load(f)
            return config
    except FileNotFoundError as e:
        try:
            with open(config_path_home_dir, 'rb') as f:
                config = tomllib.load(f)
                return config
        except FileNotFoundError as e:
            err_msg = 'Could not find the config file  `.blast2galaxy.toml`  in the current working directory or in your home directory: ' + str(Path.home())
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