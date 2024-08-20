# Usage

## Using the CLI

After installation of blast2galaxy you can use the `blast2galaxy` CLI to perform BLAST and DIAMOND searches against the Galaxy servers you have configured
in the `.blast2galaxy.config.toml` file

`blast2galaxy blastn --help`

You can find all possible subcommands and parameters in the [CLI reference](cli.md).





### List available tools and sequence database of a Galaxy server

After configuration of at least one default server you can use the `list-tools` command of the CLI to get a table with all NCBI BLAST+ tools and DIAMOND available on that Galaxy server. The table also contains the Tool-IDs for configuration of the blast2galaxy profiles and also all available sequences databases corresponding to the specific tool.

List all available tools of the default server: `blast2galaxy list-tools`

List all available tools of the server with ID <span style="font-family: monospace;">server_id</span>: `blast2galaxy list-tools --server=server_id`


### Perform search requests

```
blast2galaxy blastn --profile=blastn --query=test.fasta --db=vertebrata_cds --out=blastn_vertebrata.txt --outfmt=6
```

```
blast2galaxy diamond-blastx --profile=diamond_blastp --query=test.fasta --db=Hordeum_vulgare__BPGv2__all_BPGv2:pep --out=result_diamond_blastx_vrs1_cds.txt --outfmt=6
```





## Using the Python API

After installation with `pip install blast2galaxy` the Python API can be imported to your Python application via `import blast2galaxy`.

You can then perform BLAST or DIAMOND requests using the configured `default` profile like so:

```python
blast2galaxy.blastn(
    query = 'dna_sequence.fasta',
    db = 'database_id',
    out = 'result_blastn.txt',
    outfmt = '6'
)
```

A specific profile can be used like so:

```python
blast2galaxy.blastp(
    profile = 'blastp',
    query = 'protein_sequence.fasta',
    db = 'database_id',
    out = 'result_blastp.txt',
    outfmt = '6'
)
```

If the profile has configured a database you can omit the `db` parameter of the function call:

```python
blast2galaxy.diamond_blastp(
    profile = 'diamond_blastp_plantae_genes',
    query = 'protein_sequence.fasta',
    out = 'result_diamond.txt',
    outfmt = '6'
)
```

You can find all possible arguments and parameters in the [API reference](api.md).