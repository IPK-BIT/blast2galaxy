After installation of blast2galaxy you can use the `blast2galaxy` CLI to perform BLAST and DIAMOND searches against the Galaxy servers you have configured
in the `.blast2galaxy.toml` file

<!--`blast2galaxy blastn --help`-->

You can find all possible subcommands and parameters in the [CLI reference](cli.md).





### List available and compatible BLAST+ and DIAMOND tools of a Galaxy server

After configuration of at least one default server you can use the `list-tools` command of the CLI to get a table with all NCBI BLAST+ tools and DIAMOND available on that Galaxy server. The table also contains the Tool-IDs for configuration of the blast2galaxy profiles.

List all available tools of the default server: 
```shell
blast2galaxy list-tools
```

List all available tools of the server with the ID `SERVER_ID`:
```
blast2galaxy list-tools --server=SERVER_ID
```


### List available tools and sequence databases of a Galaxy server

After configuration of at least one default profile you can use the `list-dbs` command of the CLI to get a table with all available sequence databases for a specific tool.

List all available databases of the tool with ID `TOOL_ID` on the default server:
```bash
blast2galaxy list-tools --tool=TOOL_ID
```

If you have configured multiple servers in the config file `.blast2galaxy.toml`, you can also obtain the available databases for a tool on a specific server other than the default server.

List all available databases of the tool with ID `TOOL_ID` on the server with ID `SERVER_ID`:
```bash
blast2galaxy list-tools --server=SERVER_ID --tool=TOOL_ID
```


### Perform search requests

```
blast2galaxy blastn --profile=blastn --query=dna.fasta --db=vertebrata_cds --out=blastn_vertebrata.txt --outfmt=6
```

```
blast2galaxy diamond-blastp --profile=diamond_blastp --query=protein.fasta --db=uniprot_swissprot_2023_03 --out=result_diamond_blastp.txt --outfmt=6
```

### Output result to `stdout`

If the `--out` parameter of the CLI is omitted, the result of the search request is forwarded to `stdout`.