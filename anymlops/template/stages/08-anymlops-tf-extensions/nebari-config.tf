resource "kubernetes_secret" "anymlops_yaml_secret" {
  metadata {
    name      = "anymlops-config-yaml"
    namespace = var.environment
  }

  data = {
    "anymlops-config.yaml" = yamlencode(var.anymlops_config_yaml)
  }
}
