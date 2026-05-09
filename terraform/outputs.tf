output "cluster_name" {
    description = "The name of the EKS cluster"
    value       = module.eks_cluster.cluster_name
}

output "cluster_endpoint" {
    description = "The endpoint for the EKS cluster"
    value       = module.eks_cluster.cluster_endpoint
}

output "cluster_certificate_authority_data" {
    description = "The base64 encoded certificate authority data for the EKS cluster"
    value       = module.eks_cluster.cluster_certificate_authority_data
}

output "vpc_id" {
    description = "The ID of the VPC"
    value       = module.vpc.vpc_id
}

output "private_subnet_ids" {
    description = "List of IDs of private subnets"
    value       = module.vpc.private_subnets
}

output "public_subnet_ids" {
    description = "List of IDs of public subnets"
    value       = module.vpc.public_subnets
}

output "kubeconfig_command" {
    description = "Command to update your local kubeconfig"
    value       = "aws eks update-kubeconfig --region ${var.aws_region} -- name ${module.eks_cluster.cluster_name}"
}