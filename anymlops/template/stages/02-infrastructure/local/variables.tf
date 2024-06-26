variable "kubeconfig_filename" {
  description = "Kubernetes kubeconfig written to filesystem"
  type        = string
  default     = null
}

variable "kube_context" {
  description = "Optional kubernetes context to use to connect to kubernetes cluster"
  type        = string
}
