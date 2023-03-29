from pathlib import Path
from typing import Optional
from zipfile import ZipFile

import typer
from click import Context
from kubernetes import client
from kubernetes import config as kube_config
from rich import print
from ruamel import yaml
from typer.core import TyperGroup

from anymlops.cli.dev import app_dev
from anymlops.cli.init import (
    check_auth_provider_creds,
    check_cloud_provider_creds,
    check_project_name,
    check_ssl_cert_email,
    enum_to_list,
    guided_init_wizard,
    handle_init,
)
from anymlops.cli.keycloak import app_keycloak
from anymlops.cost import infracost_report
from anymlops.deploy import deploy_configuration
from anymlops.destroy import destroy_configuration
from anymlops.render import render_template
from anymlops.schema import (
    AuthenticationEnum,
    CiEnum,
    GitRepoEnum,
    InitInputs,
    ProviderEnum,
    TerraformStateEnum,
    verify,
)
from anymlops.upgrade import do_upgrade
from anymlops.utils import load_yaml
from anymlops.version import __version__

SECOND_COMMAND_GROUP_NAME = "Debugging Commands"
GUIDED_INIT_MSG = (
    "[bold green]START HERE[/bold green] - this will guide you step-by-step "
    "to generate your [purple]anymlops-config.yaml[/purple]. "
    "It is an [i]alternative[/i] to passing the options listed below."
)
KEYCLOAK_COMMAND_MSG = (
    "Interact with the Anymlops Keycloak identity and access management tool."
)
DEV_COMMAND_MSG = "Development tools and advanced features."


class OrderCommands(TyperGroup):
    def list_commands(self, ctx: Context):
        """Return list of commands in the order appear."""
        return list(self.commands)


app = typer.Typer(
    cls=OrderCommands,
    help="🐻‍❄️  Anymlops CLI ",
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode="rich",
    context_settings={"help_option_names": ["-h", "--help"]},
)
app.add_typer(
    app_keycloak,
    name="keycloak",
    help=KEYCLOAK_COMMAND_MSG,
    rich_help_panel=SECOND_COMMAND_GROUP_NAME,
)


@app.callback(invoke_without_command=True)
def version(
    version: Optional[bool] = typer.Option(
        None,
        "-v",
        "--version",
        help="Anymlops version number",
        is_eager=True,
    ),
):
    if version:
        print(__version__)
        raise typer.Exit()


@app.command()
def init(
    cloud_provider: str = typer.Argument(
        "local",
        help=f"options: {enum_to_list(ProviderEnum)}",
        callback=check_cloud_provider_creds,
        is_eager=True,
    ),
    guided_init: bool = typer.Option(
        False,
        help=GUIDED_INIT_MSG,
        callback=guided_init_wizard,
        is_eager=True,
    ),
    project_name: str = typer.Option(
        ...,
        "--project-name",
        "--project",
        "-p",
        callback=check_project_name,
    ),
    domain_name: str = typer.Option(
        ...,
        "--domain-name",
        "--domain",
        "-d",
    ),
    namespace: str = typer.Option(
        "dev",
    ),
    auth_provider: str = typer.Option(
        "password",
        help=f"options: {enum_to_list(AuthenticationEnum)}",
        callback=check_auth_provider_creds,
    ),
    auth_auto_provision: bool = typer.Option(
        False,
    ),
    repository: str = typer.Option(
        None,
        help=f"options: {enum_to_list(GitRepoEnum)}",
    ),
    repository_auto_provision: bool = typer.Option(
        False,
    ),
    ci_provider: str = typer.Option(
        None,
        help=f"options: {enum_to_list(CiEnum)}",
    ),
    terraform_state: str = typer.Option(
        "remote", help=f"options: {enum_to_list(TerraformStateEnum)}"
    ),
    kubernetes_version: str = typer.Option(
        "latest",
    ),
    ssl_cert_email: str = typer.Option(
        None,
        callback=check_ssl_cert_email,
    ),
    disable_prompt: bool = typer.Option(
        False,
        is_eager=True,
    ),
):
    """
    Create and initialize your [purple]anymlops-config.yaml[/purple] file.

    This command will create and initialize your [purple]anymlops-config.yaml[/purple] :sparkles:

    This file contains all your Anymlops cluster configuration details and,
    is used as input to later commands such as [green]anymlops render[/green], [green]anymlops deploy[/green], etc.

    If you're new to Anymlops, we recommend you use the Guided Init wizard.
    To get started simply run:

            [green]anymlops init --guided-init[/green]

    """
    inputs = InitInputs()

    inputs.cloud_provider = cloud_provider
    inputs.project_name = project_name
    inputs.domain_name = domain_name
    inputs.namespace = namespace
    inputs.auth_provider = auth_provider
    inputs.auth_auto_provision = auth_auto_provision
    inputs.repository = repository
    inputs.repository_auto_provision = repository_auto_provision
    inputs.ci_provider = ci_provider
    inputs.terraform_state = terraform_state
    inputs.kubernetes_version = kubernetes_version
    inputs.ssl_cert_email = ssl_cert_email
    inputs.disable_prompt = disable_prompt

    handle_init(inputs)


@app.command()
def deploy(
    config: str = typer.Option(
        ...,
        "--config",
        "-c",
        help="anymlops configuration yaml file path",
    ),
    output: str = typer.Option(
        "./",
        "-o",
        "--output",
        help="output directory",
    ),
    dns_provider: str = typer.Option(
        False,
        "--dns-provider",
        help="dns provider to use for registering domain name mapping",
    ),
    dns_auto_provision: bool = typer.Option(
        False,
        "--dns-auto-provision",
        help="Attempt to automatically provision DNS, currently only available for `cloudflare`",
    ),
    disable_prompt: bool = typer.Option(
        False,
        "--disable-prompt",
        help="Disable human intervention",
    ),
    disable_render: bool = typer.Option(
        False,
        "--disable-render",
        help="Disable auto-rendering in deploy stage",
    ),
    disable_checks: bool = typer.Option(
        False,
        "--disable-checks",
        help="Disable the checks performed after each stage",
    ),
    skip_remote_state_provision: bool = typer.Option(
        False,
        "--skip-remote-state-provision",
        help="Skip terraform state deployment which is often required in CI once the terraform remote state bootstrapping phase is complete",
    ),
):
    """
    Deploy the Anymlops cluster from your [purple]anymlops-config.yaml[/purple] file.
    """
    config_filename = Path(config)

    if not config_filename.is_file():
        raise ValueError(
            f"passed in configuration filename={config_filename} must exist"
        )

    config_yaml = load_yaml(config_filename)

    verify(config_yaml)

    if not disable_render:
        render_template(output, config, force=True)

    deploy_configuration(
        config_yaml,
        dns_provider=dns_provider,
        dns_auto_provision=dns_auto_provision,
        disable_prompt=disable_prompt,
        disable_checks=disable_checks,
        skip_remote_state_provision=skip_remote_state_provision,
    )


@app.command()
def destroy(
    config: str = typer.Option(
        ..., "-c", "--config", help="anymlops configuration file path"
    ),
    output: str = typer.Option(
        "./",
        "-o",
        "--output",
        help="output directory",
    ),
    disable_render: bool = typer.Option(
        False,
        "--disable-render",
        help="Disable auto-rendering before destroy",
    ),
    disable_prompt: bool = typer.Option(
        False,
        "--disable-prompt",
        help="Destroy entire Anymlops cluster without confirmation request. Suggested for CI use.",
    ),
):
    """
    Destroy the Anymlops cluster from your [purple]anymlops-config.yaml[/purple] file.
    """

    def _run_destroy(config=config, disable_render=disable_render):
        config_filename = Path(config)
        if not config_filename.is_file():
            raise ValueError(
                f"passed in configuration filename={config_filename} must exist"
            )

        config_yaml = load_yaml(config_filename)

        verify(config_yaml)

        if not disable_render:
            render_template(output, config, force=True)

        destroy_configuration(config_yaml)

    if disable_prompt:
        _run_destroy()
    elif typer.confirm("Are you sure you want to destroy your Anymlops cluster?"):
        _run_destroy()
    else:
        raise typer.Abort()

def get_config_namespace(config):
    config_filename = Path(config)
    if not config_filename.is_file():
        raise ValueError(
            f"passed in configuration filename={config_filename} must exist"
        )

    with config_filename.open() as f:
        config = yaml.safe_load(f.read())

    return config["namespace"]


if __name__ == "__main__":
    app()
