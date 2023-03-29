from typing import Dict

from anymlops.provider.terraform import (
    Data,
    Provider,
    TerraformBackend,
    tf_render_objects,
)
from anymlops.utils import deep_merge


def AnymlopsAWSProvider(anymlops_config: Dict):
    return Provider("aws", region=anymlops_config["amazon_web_services"]["region"])


def AnymlopsGCPProvider(anymlops_config: Dict):
    return Provider(
        "google",
        project=anymlops_config["google_cloud_platform"]["project"],
        region=anymlops_config["google_cloud_platform"]["region"],
    )


def AnymlopsAzureProvider(anymlops_config: Dict):
    return Provider("azurerm", features={})


def AnymlopsDigitalOceanProvider(anymlops_config: Dict):
    return Provider("digitalocean")


def AnymlopsKubernetesProvider(anymlops_config: Dict):
    if anymlops_config["provider"] == "aws":
        cluster_name = f"{anymlops_config['project_name']}-{anymlops_config['namespace']}"
        # The AWS provider needs to be added, as we are using aws related resources #1254
        return deep_merge(
            Data("aws_eks_cluster", "default", name=cluster_name),
            Data("aws_eks_cluster_auth", "default", name=cluster_name),
            Provider("aws", region=anymlops_config["amazon_web_services"]["region"]),
            Provider(
                "kubernetes",
                experiments={"manifest_resource": True},
                host="${data.aws_eks_cluster.default.endpoint}",
                cluster_ca_certificate="${base64decode(data.aws_eks_cluster.default.certificate_authority[0].data)}",
                token="${data.aws_eks_cluster_auth.default.token}",
            ),
        )
    return Provider(
        "kubernetes",
        experiments={"manifest_resource": True},
    )


def AnymlopsHelmProvider(anymlops_config: Dict):
    if anymlops_config["provider"] == "aws":
        cluster_name = f"{anymlops_config['project_name']}-{anymlops_config['namespace']}"

        return deep_merge(
            Data("aws_eks_cluster", "default", name=cluster_name),
            Data("aws_eks_cluster_auth", "default", name=cluster_name),
            Provider(
                "helm",
                kubernetes=dict(
                    host="${data.aws_eks_cluster.default.endpoint}",
                    cluster_ca_certificate="${base64decode(data.aws_eks_cluster.default.certificate_authority[0].data)}",
                    token="${data.aws_eks_cluster_auth.default.token}",
                ),
            ),
        )
    return Provider("helm")


def AnymlopsTerraformState(directory: str, anymlops_config: Dict):
    if anymlops_config["terraform_state"]["type"] == "local":
        return {}
    elif anymlops_config["terraform_state"]["type"] == "existing":
        return TerraformBackend(
            anymlops_config["terraform_state"]["backend"],
            **anymlops_config["terraform_state"]["config"],
        )
    elif anymlops_config["provider"] == "aws":
        return TerraformBackend(
            "s3",
            bucket=f"{anymlops_config['project_name']}-{anymlops_config['namespace']}-terraform-state",
            key=f"terraform/{anymlops_config['project_name']}-{anymlops_config['namespace']}/{directory}.tfstate",
            region=anymlops_config["amazon_web_services"]["region"],
            encrypt=True,
            dynamodb_table=f"{anymlops_config['project_name']}-{anymlops_config['namespace']}-terraform-state-lock",
        )
    elif anymlops_config["provider"] == "gcp":
        return TerraformBackend(
            "gcs",
            bucket=f"{anymlops_config['project_name']}-{anymlops_config['namespace']}-terraform-state",
            prefix=f"terraform/{anymlops_config['project_name']}/{directory}",
        )
    elif anymlops_config["provider"] == "do":
        return TerraformBackend(
            "s3",
            endpoint=f"{anymlops_config['digital_ocean']['region']}.digitaloceanspaces.com",
            region="us-west-1",  # fake aws region required by terraform
            bucket=f"{anymlops_config['project_name']}-{anymlops_config['namespace']}-terraform-state",
            key=f"terraform/{anymlops_config['project_name']}-{anymlops_config['namespace']}/{directory}.tfstate",
            skip_credentials_validation=True,
            skip_metadata_api_check=True,
        )
    elif anymlops_config["provider"] == "azure":
        return TerraformBackend(
            "azurerm",
            resource_group_name=f"{anymlops_config['project_name']}-{anymlops_config['namespace']}-state",
            # storage account must be globally unique
            storage_account_name=f"{anymlops_config['project_name']}{anymlops_config['namespace']}{anymlops_config['azure']['storage_account_postfix']}",
            container_name=f"{anymlops_config['project_name']}-{anymlops_config['namespace']}-state",
            key=f"terraform/{anymlops_config['project_name']}-{anymlops_config['namespace']}/{directory}",
        )
    elif anymlops_config["provider"] == "existing":
        optional_kwargs = {}
        if "kube_context" in anymlops_config["existing"]:
            optional_kwargs["confix_context"] = anymlops_config["existing"][
                "kube_context"
            ]
        return TerraformBackend(
            "kubernetes",
            secret_suffix=f"{anymlops_config['project_name']}-{anymlops_config['namespace']}-{directory}",
            load_config_file=True,
            **optional_kwargs,
        )
    elif anymlops_config["provider"] == "local":
        optional_kwargs = {}
        if "kube_context" in anymlops_config["local"]:
            optional_kwargs["confix_context"] = anymlops_config["local"]["kube_context"]
        return TerraformBackend(
            "kubernetes",
            secret_suffix=f"{anymlops_config['project_name']}-{anymlops_config['namespace']}-{directory}",
            load_config_file=True,
            **optional_kwargs,
        )
    else:
        raise NotImplementedError("state not implemented")


def stage_01_terraform_state(config):
    if config["provider"] == "gcp":
        return {
            "stages/01-terraform-state/gcp/_anymlops.tf.json": tf_render_objects(
                [
                    AnymlopsGCPProvider(config),
                ]
            )
        }
    elif config["provider"] == "aws":
        return {
            "stages/01-terraform-state/aws/_anymlops.tf.json": tf_render_objects(
                [
                    AnymlopsAWSProvider(config),
                ]
            )
        }
    else:
        return {}


def stage_02_infrastructure(config):
    if config["provider"] == "gcp":
        return {
            "stages/02-infrastructure/gcp/_anymlops.tf.json": tf_render_objects(
                [
                    AnymlopsGCPProvider(config),
                    AnymlopsTerraformState("02-infrastructure", config),
                ]
            )
        }
    elif config["provider"] == "do":
        return {
            "stages/02-infrastructure/do/_anymlops.tf.json": tf_render_objects(
                [
                    AnymlopsTerraformState("02-infrastructure", config),
                ]
            )
        }
    elif config["provider"] == "azure":
        return {
            "stages/02-infrastructure/azure/_anymlops.tf.json": tf_render_objects(
                [
                    AnymlopsTerraformState("02-infrastructure", config),
                ]
            ),
        }
    elif config["provider"] == "aws":
        return {
            "stages/02-infrastructure/aws/_anymlops.tf.json": tf_render_objects(
                [
                    AnymlopsAWSProvider(config),
                    AnymlopsTerraformState("02-infrastructure", config),
                ]
            )
        }
    else:
        return {}


def stage_03_kubernetes_initialize(config):
    return {
        "stages/03-kubernetes-initialize/_anymlops.tf.json": tf_render_objects(
            [
                AnymlopsTerraformState("03-kubernetes-initialize", config),
                AnymlopsKubernetesProvider(config),
                AnymlopsHelmProvider(config),
            ]
        ),
    }


def stage_04_kubernetes_ingress(config):
    return {
        "stages/04-kubernetes-ingress/_anymlops.tf.json": tf_render_objects(
            [
                AnymlopsTerraformState("04-kubernetes-ingress", config),
                AnymlopsKubernetesProvider(config),
                AnymlopsHelmProvider(config),
            ]
        ),
    }


def stage_05_kubernetes_keycloak(config):
    return {
        "stages/05-kubernetes-keycloak/_anymlops.tf.json": tf_render_objects(
            [
                AnymlopsTerraformState("05-kubernetes-keycloak", config),
                AnymlopsKubernetesProvider(config),
                AnymlopsHelmProvider(config),
            ]
        ),
    }


def stage_06_kubernetes_keycloak_configuration(config):
    return {
        "stages/06-kubernetes-keycloak-configuration/_anymlops.tf.json": tf_render_objects(
            [
                AnymlopsTerraformState("06-kubernetes-keycloak-configuration", config),
            ]
        ),
    }


def stage_07_kubernetes_services(config):
    return {
        "stages/07-kubernetes-services/_anymlops.tf.json": tf_render_objects(
            [
                AnymlopsTerraformState("07-kubernetes-services", config),
                AnymlopsKubernetesProvider(config),
                AnymlopsHelmProvider(config),
            ]
        ),
    }


def stage_08_anymlops_tf_extensions(config):
    return {
        "stages/08-anymlops-tf-extensions/_anymlops.tf.json": tf_render_objects(
            [
                AnymlopsTerraformState("08-anymlops-tf-extensions", config),
                AnymlopsKubernetesProvider(config),
                AnymlopsHelmProvider(config),
            ]
        ),
    }
