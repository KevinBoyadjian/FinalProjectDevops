# ---------------------------------------------------------------------------------------------------------------------
# AWS LOAD BALANCER CONTROLLER - IAM INFRASTRUCTURE (IRSA)
# ---------------------------------------------------------------------------------------------------------------------

# 1. Define the Trust Policy
# This allows the EKS OIDC provider to assume this specific IAM role
data "aws_iam_policy_document" "lb_controller_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"

    condition {
      test     = "StringEquals"
      # This strips the 'https://' from the OIDC URL to match the required AWS format
      variable = "${replace(module.eks_cluster.cluster_oidc_issuer_url, "https://", "")}:sub"
      values   = ["system:serviceaccount:kube-system:aws-load-balancer-controller"]
    }

    condition {
      test     = "StringEquals"
      variable = "${replace(module.eks_cluster.cluster_oidc_issuer_url, "https://", "")}:aud"
      values   = ["sts.amazonaws.com"]
    }

    principals {
      identifiers = [module.eks_cluster.oidc_provider_arn]
      type        = "Federated"
    }
  }
}

# 2. Create the IAM Role for the Controller
resource "aws_iam_role" "lb_controller" {
  name               = "${var.project_name}-lb-controller-role"
  assume_role_policy = data.aws_iam_policy_document.lb_controller_assume_role_policy.json
  
  tags = var.common_tags
}

# 3. Create and Attach the Policy
# This gives the controller permission to create ALBs, SGs, and Listeners
resource "aws_iam_role_policy" "lb_controller" {
  name   = "${var.project_name}-lb-controller-policy"
  role   = aws_iam_role.lb_controller.id
  
  # We use 'file' to keep the long AWS policy json clean and separate
  # You can download the official policy here: 
  # https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/install/iam_policy.json
  policy = file("${path.module}/iam_policy_alb.json")
}

# ---------------------------------------------------------------------------------------------------------------------
# AWS LOAD BALANCER CONTROLLER - HELM INSTALLATION
# ---------------------------------------------------------------------------------------------------------------------

resource "helm_release" "lb_controller" {
  name       = "aws-load-balancer-controller"
  repository = "https://aws.github.io/eks-charts"
  chart      = "aws-load-balancer-controller"
  namespace  = "kube-system"
  version    = "1.6.2"

  # CHANGE: Use the 'set' argument with a list of objects
  set = [
    {
      name  = "clusterName"
      value = module.eks_cluster.cluster_name
    },
    {
      name  = "serviceAccount.create"
      value = "true"
    },
    {
      name  = "serviceAccount.name"
      value = "aws-load-balancer-controller"
    },
    {
      name  = "serviceAccount.annotations.eks\\.amazonaws\\.com/role-arn"
      value = aws_iam_role.lb_controller.arn
    },
    {
      name  = "region"
      value = var.aws_region
    },
    {
      name  = "vpcId"
      value = module.vpc.vpc_id
    }
  ]
}
