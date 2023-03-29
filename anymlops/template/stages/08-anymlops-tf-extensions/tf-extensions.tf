module "extension" {
  for_each = { for extension in var.tf_extensions : extension.name => extension }

  source = "./modules/anymlopsextension"

  name             = "anymlops-ext-${each.key}"
  namespace        = var.environment
  image            = each.value.image
  urlslug          = each.value.urlslug
  private          = lookup(each.value, "private", false)
  oauth2client     = lookup(each.value, "oauth2client", false)
  keycloakadmin    = lookup(each.value, "keycloakadmin", false)
  jwt              = lookup(each.value, "jwt", false)
  anymlopsconfigyaml = lookup(each.value, "anymlopsconfigyaml", false)
  external-url     = var.endpoint
  anymlops-realm-id  = var.realm_id

  keycloak_anymlops_bot_password = each.value.keycloakadmin ? var.keycloak_anymlops_bot_password : ""

  envs = lookup(each.value, "envs", [])
}
