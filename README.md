<p align="center">
<picture>
  <source media="(prefers-color-scheme: light)" srcset="https://beartell.com/img/Any_png.png">
  <source media="(prefers-color-scheme: dark)" srcset="https://beartell.com/img/Any_png.png">
  <img alt="Anymlops logo mark - text will be black in light color mode and white in dark color mode." src="https://beartell.com/img/Any_png.png" width="50%"/>
</picture>
</p>

<h1 align="center"> A data science operating platform that literally works ;) </h1>
<h1 align="center"> For everyone, from startups to the largest companies. </h1>

---

| Information | Links |
| :---------- | :-----|
|   Project   | [![License](https://img.shields.io/badge/License-BSD%203--Clause-gray.svg?colorA=2D2A56&colorB=5936D9&style=flat.svg)](https://opensource.org/licenses/BSD-3-Clause) |

## Table of contents

- [Table of contents](#table-of-contents)
- [Anymlops](#anymlops)
  - [Cloud Providers ☁️](#cloud-providers-️)
- [Installation 💻](#installation-)
  - [Pre-requisites](#pre-requisites)
  - [Install Anymlops](#install-anymlops)
- [Usage 🚀](#usage-)
- [Code of Conduct 📖](#code-of-conduct-)
- [License](#license)

Automated data science platform. From [JupyterHub](https://jupyter.org/hub "Multi-user version of the Notebook") to Cloud environments with
[Dask Gateway](https://docs.dask.org/ "Python horizontal computation").

Anymlops is an open source data science platform that enables enterprises to build and maintain cost-effective and scalable compute platforms
on [Kubernetes](#anymlops) at day 0.

## Anymlops

The Kubernetes version of Anymlops uses [Terraform](https://www.terraform.io/), [Helm](https://helm.sh/), and
[GitHub Actions](https://docs.github.com/en/free-pro-team@latest/actions).

- Terraform handles the build, change, and versioning of the infrastructure.
- Helm helps to define, install, and manage [Kubernetes](https://kubernetes.io/ "Automated container deployment, scaling, and management") resources.
- GitHub Actions is used to automatically create commits when the configuration file (`anymlops-config.yaml`) is rendered,
  as well as to kick off the deployment action.

At Anymlops, we're all about making things easy for you! That's why you don't need to worry about understanding any of the technical jargon we've mentioned. Our goal is to ensure your project is deployed smoothly and successfully, without any fuss on your end.

### Cloud Providers ☁️

Anymlops offers out-of-the-box support for the major public cloud providers: [Digital Ocean](https://www.digitalocean.com/),
Amazon [AWS](https://aws.amazon.com/), [GCP](https://cloud.google.com/ "Google Cloud Provider"), and Microsoft [Azure](https://azure.microsoft.com/en-us/).
![High-level illustration of Anymlops architecture](https://raw.githubusercontent.com/nebari-dev/nebari-docs/main/docs/static/img/welcome/nebari_overview_sequence.png)

## Installation 💻

### Pre-requisites

- Operating System: Currently, Anymlops supports development on Linux and Macos operating systems. Windows is NOT supported.
- You need Python >= 3.7 on your local machine or virtual environment to work on Anymlops.
- Adopting virtual environments ([`conda`](https://docs.conda.io/en/latest/), [`pipenv`](https://github.com/pypa/pipenv) or
  [`venv`](https://docs.python.org/3/library/venv.html)) is also encouraged.

### Install Anymlops

To install Anymlops type the following commands in your command line:

- Install using `conda`:

  ```bash
  conda install -c conda-forge anymlops

  # if you prefer using mamba
  mamba install -c conda-forge anymlops
  ```

- Install using `pip`:

  ```bash
  pip install anymlops
  ```

Once finished, you can check Anymlops's version (and additional CLI arguments) by typing:

```bash
anymlops --help
```

If successful, the CLI output will be similar to the following:

```bash
usage: anymlops [-h] [-v] {deploy,destroy,render,init,validate} ...

Anymlops command line

positional arguments:
  {deploy,destroy,render,init,validate}
                        Anymlops

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Anymlops version
```

## Usage 🚀

To ensure a seamless and fully automated deployment with Anymlops, you must configure multiple environment variables. Obtain the required variables by consulting the [Anymlops Get started documentation][docs-get-started].

After collecting the necessary credentials, establish them as UNIX environment variables. With this step complete, you'll be able to deploy Anymlops in mere minutes.

For detailed step-by-step instructions on how to deploy Anymlops, check the [Anymlops documentation][docs-deploy].

## Code of Conduct 📖

To guarantee a welcoming and friendly community, we require all community members to follow our [Code of Conduct](https://github.com/beartell/anymlops/CODE_OF_CONDUCT.md).

## License

[Anymlops is BSD3 licensed](LICENSE).
