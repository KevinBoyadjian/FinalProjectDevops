terraform {
    required_version = ">=1.0"

    required_providers {
        aws = {
            source  = "hashicorp/aws"
            version = "~> 5.0" # Always pin versions!
        }
        kubernetes  = {
            source  = "hashicorp/kubernetes"
            version = "~> 2.25" # Manages resources inside K8s
        }
        tls = {
            source  = "hashicorp/tls"
            version = "~> 4.0" # Used for EKS OIDC provider
        }
    }
}

provider "aws" {
    region = var.aws_region
}

# The Kubernetes provider configuration will be dynamic,
# as it needs to connect to the EKS cluster created by AWS provider.
# We'll configure this later, using the EKS cluster's output.
provider "kubernetes" {
    host                    = module.eks.cluster_endpoint
    cluster_ca_certificate  = base64decode(module.eks.cluster_certificate_authority_data)
    token                   = data.aws_eks_cluster_auth.main.token
}

# Data source for EKS cluster authentication
data "aws_eks_cluster_auth" "main" {
    name = module.eks.cluster_name.cluster_name
}