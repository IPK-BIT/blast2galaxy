# Installation

## Prerequisites

- Python version has to be >= 3.10

!!! note
    It is highly recommended to install blast2galaxy in an isolated environment created with an environment management tool like conda/mamba, pixi, virtualenv or similar.

## Installation with pip

You can install blast2galaxy from PyPI.org using pip:

```
pip install blast2galaxy
```

After installation you can check if the blast2galaxy CLI was installed correctly by executing the following command on your shell:

```
blast2galaxy --help
```

##  Installation with mamba or conda

!!! note
    Please make sure you have added the channels `bioconda` and `conda-forge` to your mamba/conda settings.
    You can do this by executing the following commands:

    ```bash
    conda config --add channels bioconda
    conda config --add channels conda-forge
    conda config --set channel_priority strict
    ```

    This will modify your ~/.condarc file.


You can install blast2galaxy the from BioConda channel:

```
mamba install blast2galaxy
```

or

```
conda install blast2galaxy
```


After installation you can check if the blast2galaxy CLI was installed correctly by executing the following command on your shell:

```
blast2galaxy --help
```