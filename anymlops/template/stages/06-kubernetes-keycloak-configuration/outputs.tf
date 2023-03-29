output "realm_id" {
  description = "Realm id used for anymlops resources"
  value       = keycloak_realm.main.id
}
