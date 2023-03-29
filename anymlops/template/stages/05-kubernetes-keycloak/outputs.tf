output "keycloak_credentials" {
  description = "keycloak admin credentials"
  sensitive   = true
  value       = module.kubernetes-keycloak-helm.credentials
}

# At this point this might be redundant, see `anymlops-bot-password` in ./modules/kubernetes/keycloak-helm/variables.tf
output "keycloak_anymlops_bot_password" {
  description = "keycloak anymlops-bot credentials"
  sensitive   = true
  value       = random_password.keycloak-anymlops-bot-password.result
}
