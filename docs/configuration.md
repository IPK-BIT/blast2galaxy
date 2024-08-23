# Configuration

blast2galaxy provides two ways to configure servers and profiles to be used with blast2galaxy.

- **TOML file based configuration**<br />
  This type of configuration can be used when using the CLI or Python API of blast2galaxy.

- **Python API based configuration**<br />
  This type of configuration can only be used when using the Python API of blast2galaxy.

Both ways of configuration are described in the following sections of this page.

## TOML file based configuration

To connect to an API of an existing Galaxy server, the user of blast2galaxy has to provide API access credentials in the form of a Galaxy API key. Furthermore, it is possible to connect via the username and password of the user account on the specific Galaxy server. For security reasons, the latter variant should only be used if the use of an API key is not possible.



blast2galaxy uses the TOML file format for configuration of one or multiple Galaxy servers and one or multiple profiles.
The default filename of the config file id `.blast2galaxy.config.toml` and blast2galaxy looks for it in the current working directory.
If it can't find a configuration file in the current working directory it looks for one in the home-directory of the current user.
If it can't find any configuration file an error message will be displayed.

An individually named configuration file at a storage location of your choice can be set via the `--configfile=PATH` parameter of the CLI. 

Example: 
```
--configfile=/opt/myapps/config/app1.blast2galaxy.config.toml
```



<br />
### General Structure of the config TOML file

The configuration file has two types of sections:

 - `[servers.###]`
 - `[profiles.###]`

Where `###` has to be replaced with either `default` or a unique server-ID / profile-ID.


!!! note

    A config file must consist at least one `[servers.]` entry and one `[profiles.]` entry. 
    If you provide `[servers.default]` and `[profiles.default]` the `--server=` and `--profile=` parameter of the CLI commands can be omitted.








<br />
### Servers

The servers section holds one or multiple Galaxy server instances with their corresponding URLs and API-Keys.

Example:
```toml
[servers.default]
server_url = "https://usegalaxy.eu"
api_key = "65dcb*******************************"
```


!!! tip

    After configuration of at least one default server you can use the `list-tools` command of the CLI to get a table with all compatible NCBI BLAST+ tools and DIAMOND available on that Galaxy server. The table also contains the Tool-IDs for configuration of the profiles.

    List all available tools of the default server:
    ```bash
    blast2galaxy list-tools
    ```

    List all available tools of the server with ID `SERVER_ID`:
    ```bash
    blast2galaxy list-tools --server=SERVER_ID
    ```


<br />
### Profiles

The profiles section holds one or multiple profiles where each profile configures at least the Galaxy server and the Tool-ID to be used.

Mandatory fields for each profile are:

- `server` &nbsp; *An ID of an configured server in the servers section*
- `tool` &nbsp; *Tool-ID for the tool on the Galaxy server*

Optional fields for each profile are:

- `db` &nbsp; *The ID of the BLAST or DIAMOND database to be used when using this profile. The `--db` parameter of the CLI or the `db=` argument of the methods of the Python API can be then omitted.*


Example:
```toml
[profiles.default]
server = "default"
tool = "toolshed.g2.bx.psu.edu/repos/devteam/ncbi_blast_plus/ncbi_blastn_wrapper/2.14.1+galaxy2"
```

!!! tip

    After configuration of at least one default profile you can use the `list-dbs` command of the CLI to get a table with all available sequence databases for a specific tool.

    List all available databases of the tool with ID `TOOL_ID` on the default server:
    ```bash
    blast2galaxy list-tools --tool=TOOL_ID
    ```

    List all available databases of the tool with ID `TOOL_ID` on the server with ID `SERVER_ID`:
    ```bash
    blast2galaxy list-tools --server=SERVER_ID --tool=TOOL_ID
    ```



<br /><br />
<h4>Example of a complete configuration file with two servers and multiple profiles</h4>

```toml
[servers.default]
server_url = "https://usegalaxy.eu"
api_key = "65dcb*******************************"

[servers.my_institutes_server]
server_url = "https://galaxy.myinstitute.org"
api_key = "1k32z*******************************"

[profiles.default]
server = "default"
tool = "toolshed.g2.bx.psu.edu/repos/devteam/ncbi_blast_plus/ncbi_blastn_wrapper/2.14.1+galaxy2"

[profiles.blastp]
server = "default"
tool = "toolshed.g2.bx.psu.edu/repos/devteam/ncbi_blast_plus/ncbi_blastp_wrapper/2.14.1+galaxy2"

[profiles.blastp_plantae_genes]
server = "default"
tool = "toolshed.g2.bx.psu.edu/repos/devteam/ncbi_blast_plus/ncbi_blastp_wrapper/2.14.1+galaxy2"
database = "plant_proteins"

[profiles.diamond_blastp_plantae_genes]
server = "default"
tool = "toolshed.g2.bx.psu.edu/repos/bgruening/diamond/bg_diamond/2.0.15+galaxy0"
database = "plant_proteins"

[profiles.blastn_vertebrata]
server = "default"
tool = "toolshed.g2.bx.psu.edu/repos/devteam/ncbi_blast_plus/ncbi_blastn_wrapper/2.14.1+galaxy2"
database = "vertebrata_proteins"
```

## Python API based configuration

If you use the Python API of blast2galaxy it is also possible to provide the configuration programmatically without the need for an `.blast2galaxy.toml` file.

Example for API based configuration during runtime for setting a default server and a default profile:
```python
import blast2galaxy

blast2galaxy.config.add_default_server(
    server_url = 'https://usegalaxy.eu', 
    api_key = 'your_api_key'
)

blast2galaxy.config.add_default_profile(
    server = 'default', 
    tool = 'toolshed.g2.bx.psu.edu/repos/devteam/ncbi_blast_plus/ncbi_blastp_wrapper/2.14.1+galaxy2'
)

blast2galaxy.blastp(
    query = 'prot.fasta',
    db = 'database_id',
    out = 'result_blastp.txt',
    outfmt = '6'
)
```

If you want to add further servers and profiles beside the defaults you can use `blast2galaxy.config.add_server()` and `blast2galaxy.config.add_profile()`:
```python
import blast2galaxy

blast2galaxy.config.add_server(
    server = 'myserver',
    server_url = 'https://usegalaxy.eu', 
    api_key = 'your_api_key'
)

blast2galaxy.config.add_profile(
    profile = 'diamond',
    server = 'myserver',
    tool = 'toolshed.g2.bx.psu.edu/repos/bgruening/diamond/bg_diamond/2.0.15+galaxy0'
)

blast2galaxy.diamond(
    profile = 'diamond',
    query = 'prot.fasta',
    db = 'database_id',
    out = 'result_diamond_blastp.txt',
    outfmt = '6'
)
```