# Configuration

To connect to an API of an existing Galaxy server, the user of blast2galaxy has to provide API access credentials in the form of a Galaxy API key. Furthermore, it is possible to connect via the username and password of the user account on the specific Galaxy server. For security reasons, the latter variant should only be used if the use of an API key is not possible.



blast2galaxy uses the TOML file format for configuration of one or multiple Galaxy servers and one or multiple profiles.
The default filename of the config file id `.blast2galaxy.config.toml` and blast2galaxy looks for it in the current working directory.
If it can't find a configuration file in the current working directory it looks for one in the home-directory of the current user.
If it can't find any configuration file an error message will be displayed.

An individually named configuration file at a storage location of your choice can be set via the `--configfile=PATH` parameter of the CLI. 
Example: `--configfile=/opt/myapps/config/app1.blast2galaxy.config.toml`



<br />
<h3>General Structure of the config TOML</h3>

The configuration file has two types of sections:

 - `[servers.###]`
 - `[profiles.###]`

Where `###` has to be replaced with either `default` or a unique server-ID / profile-ID.


!!! note

    A config file must consist at least one `[servers.]` entry and one `[profiles.]` entry. 
    If you provide `[servers.default]` and `[profiles.default]` the `--profile` parameter of the CLI can be omitted.








<br />
<h3>Servers</h3>

The servers section holds one or multiple Galaxy server instances with their corresponding URLs and API-Keys.

Example:
```toml
[servers.default]
server_url = "https://usegalaxy.eu"
api_key = "65dcb*******************************"
```


!!! tip

    After configuration of at least one default server you can use the `list-tools` command of the CLI to get a table with all NCBI BLAST+ tools and DIAMOND available on that Galaxy server. The table also contains the Tool-IDs for configuration of the profiles and also all available sequences databases corresponding to the specific tool.

    List all available tools of the default server:
    ```bash
    blast2galaxy list-tools
    ```

    List all available tools of the server with ID <span style="font-family: monospace;">server_id</span>:
    ```bash
    blast2galaxy list-tools --server=server_id
    ```


<br />
<h3>Profiles</h3>

The profiles section holds one or multiple profiles where each profile configures at least the Galaxy server and the Tool-ID to be used.

Mandatory fields for each profile are:

- `server` &nbsp; *An ID of an configured server in the servers section*
- `tool_id` &nbsp; *Tool-ID for the tool on the Galaxy server*

Optional fields for each profile are:

- `db` &nbsp; *The ID of the BLAST or DIAMOND database to be used when using this profile. The `--db` parameter of the CLI or the `db=` argument of the methods of the Python API can be then omitted.*


Example:
```toml
[profiles.default]
server = "default"
tool_id = "toolshed.g2.bx.psu.edu/repos/devteam/ncbi_blast_plus/ncbi_blastn_wrapper/2.14.1+galaxy2"
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
tool_id = "toolshed.g2.bx.psu.edu/repos/devteam/ncbi_blast_plus/ncbi_blastn_wrapper/2.14.1+galaxy2"

[profiles.blastp]
server = "default"
tool_id = "toolshed.g2.bx.psu.edu/repos/devteam/ncbi_blast_plus/ncbi_blastp_wrapper/2.14.1+galaxy2"

[profiles.blastp_plantae_genes]
server = "default"
tool_id = "toolshed.g2.bx.psu.edu/repos/devteam/ncbi_blast_plus/ncbi_blastp_wrapper/2.14.1+galaxy2"
database = "plant_proteins"

[profiles.diamond_blastp_plantae_genes]
server = "default"
tool_id = "toolshed.g2.bx.psu.edu/repos/bgruening/diamond/bg_diamond/2.0.15+galaxy0"
database = "plant_proteins"

[profiles.blastn_vertebrata]
server = "default"
tool_id = "toolshed.g2.bx.psu.edu/repos/devteam/ncbi_blast_plus/ncbi_blastn_wrapper/2.14.1+galaxy2"
database = "vertebrata_proteins"
```