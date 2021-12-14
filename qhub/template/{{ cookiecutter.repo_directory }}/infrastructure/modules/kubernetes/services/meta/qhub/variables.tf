variable "name" {
  description = "Name for QHub Deployment"
  type        = string
}

variable "namespace" {
  description = "Namespace for QHub Deployment"
  type        = string
}

variable "home-pvc" {
  description = "Name for persistent volume claim to use for home directory uses /home/{username}"
  type        = string
}

variable "conda-store-pvc" {
  description = "Name for persistent volume claim to use for conda-store directory"
  type        = string
}

variable "external-url" {
  description = "External url that jupyterhub cluster is accessible"
  type        = string
}

variable "jupyterhub-image" {
  description = "Docker image to use for jupyterhub hub"
  type = object({
    name = string
    tag  = string
  })
}

variable "jupyterlab-image" {
  description = "Docker image to use for jupyterlab users"
  type = object({
    name = string
    tag  = string
  })
}

variable "dask-worker-image" {
  description = "Docker image to use for dask worker image"
  type = object({
    name = string
    tag  = string
  })
}

variable "dask-gateway-image" {
  description = "Docker image to use for dask gateway image"
  type = object({
    name = string
    tag  = string
  })
  default = {
    name = "daskgateway/dask-gateway-server"
    tag  = "0.9.0"
  }
}

variable "general-node-group" {
  description = "Node key value pair for bound general resources"
  type = object({
    key   = string
    value = string
  })
}

variable "user-node-group" {
  description = "Node group key value pair for bound user resources"
  type = object({
    key   = string
    value = string
  })
}

variable "worker-node-group" {
  description = "Node group key value pair for bound worker resources"
  type = object({
    key   = string
    value = string
  })
}

variable "jupyterhub-overrides" {
  description = "Jupyterhub helm overrides"
  type        = list(string)
}

variable "jupyterhub-hub-extraEnv" {
  description = "Extracted overrides to merge with jupyterhub.hub.extraEnv"
  type        = list(map(any))
  default     = []
}

variable "dask_gateway_extra_config" {
  description = "dask gateway extra configuration"
  type        = string
  default     = ""
}

variable "certificate-secret-name" {
  description = "tls certificate secret name to use"
  type        = string
  default     = ""
}

variable "forwardauth-callback-url-path" {
  description = "Callback URL Path for ForwardAuth"
  type        = string
  default     = ""
}

variable "OAUTH_CLIENT_ID" {
  description = "ID for JupyterHub client in Keycloak"
  type        = string
}

variable "OAUTH_CLIENT_SECRET" {
  description = "Secret for JupyterHub client in Keycloak"
  type        = string
}

variable "OAUTH_CALLBACK_URL" {
  description = "Callback URL for JupyterHub client in Keycloak"
  type        = string
}

variable "OAUTH2_TLS_VERIFY" {
  description = "Whether OAuthenticator should check HTTPS certs (true/false as string)"
  type        = string
}

variable "keycloak_authorize_url" {
  description = "Keycloak OAuth start URL"
  type        = string
}

variable "keycloak_token_url" {
  description = "Keycloak OAuth start URL"
  type        = string
}

variable "keycloak_userdata_url" {
  description = "Keycloak OAuth start URL"
  type        = string
}

variable "keycloak_logout_url" {
  description = "Keycloak logout URL"
  type        = string
}

variable "keycloak_server_url" {
  description = "URL of Keycloak service"
  type        = string
}

variable "keycloak_username" {
  description = "Keycloak username"
  type        = string
}

variable "keycloak_password" {
  description = "Keycloak password"
  type        = string
}
