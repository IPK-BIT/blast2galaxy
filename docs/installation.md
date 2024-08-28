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

blast2galaxy is available as a [Bioconda package](https://bioconda.github.io/recipes/blast2galaxy/README.html){:target="_blank"}.

!!! note
    Please make sure you have added the channels `bioconda` and `conda-forge` to your mamba/conda settings.
    You can do this by executing the following commands:

    ```bash
    conda config --add channels bioconda
    conda config --add channels conda-forge
    conda config --set channel_priority strict
    ```

    This will modify your ~/.condarc file.


You can install blast2galaxy the from the `bioconda` channel:

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

## Using Biocontainers image with Docker or Podman

blast2galaxy is available as a [Biocontainers](https://biocontainers.pro/){:target="_blank"} image.

Please replace `<tag>` in the commands listed below with an available version tag. All available version tags are listed here: [https://quay.io/repository/biocontainers/blast2galaxy?tab=tags](https://quay.io/repository/biocontainers/blast2galaxy?tab=tags){:target="_blank"}

<h3>Pull the image</h3>

Using Podman:

```bash
podman pull quay.io/biocontainers/blast2galaxy:<tag>
```

Using Docker:

```bash
docker pull quay.io/biocontainers/blast2galaxy:<tag>
```

<h3>Start a container</h3>

Using Podman:

```bash
$ podman run --name blast2galaxy -it quay.io/biocontainers/blast2galaxy:<tag>
```

Using Docker:

```bash
$ docker run --name blast2galaxy -it quay.io/biocontainers/blast2galaxy:<tag>
```

When the container is running you can check if everything works fine by executing the following command on the shell of the running container:

```
blast2galaxy --help
```