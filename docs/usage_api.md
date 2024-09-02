## Using the Python API

After installation of blast2galaxy the Python API can be imported into your Python application via `import blast2galaxy`.

!!! note
    If using the API the BLAST+ or DIAMOND results are not written to a file but instead are returned from the called API function.

You can then perform BLAST or DIAMOND requests using the configured `default` profile like so:

```python
result = blast2galaxy.blastn(
    query = 'dna_sequence.fasta',
    db = 'database_id',
    outfmt = '6'
)
```

A specific profile can be used like so:

```python
result = blast2galaxy.blastp(
    profile = 'blastp',
    query = 'protein_sequence.fasta',
    db = 'database_id',
    outfmt = '6'
)
```

<!-- currently not implemented!
If the profile has configured a database you can omit the `db` parameter of the function call:

```python
blast2galaxy.diamond_blastp(
    profile = 'diamond_blastp_plantae_genes',
    query = 'protein_sequence.fasta',
    out = 'result_diamond.txt',
    outfmt = '6'
)
```
-->

Instead of a filename it is also possible to provide the query as a Python string. This is helpful in the situation of an integration with other tools / databases where writing intermediate files for query sequences is not desired.

```python

protein_seq = """
>sp|P62805|H4_HUMAN Histone H4 OS=Homo sapiens OX=9606 GN=H4C1 PE=1 SV=2
MSGRGKGGKGLGKGGAKRHRKVLRDNIQGITKPAIRRLARRGGVKRISGLIYEETRGVLK
VFLENVIRDAVTYTEHAKRKTVTAMDVVYALKRQGRTLYGFGG
"""

result = blast2galaxy.blastp(
    profile = 'blastp',
    query_str = protein_seq,
    db = 'database_id',
    outfmt = '6'
)
```



!!! tip
    You can find all possible arguments and parameters in the [API reference](api.md).



### Exceptions

blast2galaxy throws the following exceptions when used in API mode:

<small>
::: blast2galaxy.errors
    handler: python
    options:
      show_source: false
      annotations_path: brief
      show_signature: true
      separate_signature: true
      show_signature_annotations: false
      show_root_heading: false
      show_root_toc_entry: false
      parameter_headings: false
      heading_level: 4
      show_object_full_path: true
</small>