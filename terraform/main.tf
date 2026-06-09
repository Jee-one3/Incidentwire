module "vpc" {
  source = "../modules/vpc"

  vpc_cidr     = "10.0.0.0/16"
  subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24"]
  azs          = ["us-east-1a", "us-east-1b"]
}

module "iam" {
  source = "../modules/iam"
}

module "eks" {
  source = "../modules/eks"

  cluster_name     = var.cluster_name
  cluster_role_arn = module.iam.cluster_role_arn
  subnet_ids       = module.vpc.subnet_ids
}

module "nodes" {
  source = "../modules/node-group"

  cluster_name  = module.eks.cluster_name
  node_role_arn = module.iam.node_role_arn
  subnet_ids    = module.vpc.subnet_ids

  instance_type = var.node_instance_type
  desired       = var.desired_capacity
}

