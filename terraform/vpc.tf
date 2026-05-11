module "vpc" {
    source  = "terraform-aws-modules/vpc/aws"
    version = "~> 5.0"

    name = "${var.project_name}-vpc-${var.environment}"
    cidr = var.vpc_cidr

    azs             = ["${var.aws_region}a", "${var.aws_region}b"] # Using two AZs for High availability
    private_subnets = var.private_subnet_cidrs
    public_subnets  = var.public_subnet_cidrs

    enable_nat_gateway   = true
    single_nat_gateway   = true # Cost-effective for dev/test
    enable_dns_hostnames = true
    enable_dns_support   = true

    tags = var.common_tags
} 