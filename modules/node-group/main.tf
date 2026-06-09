resource "aws_eks_node_group" "nodes" {
  cluster_name    = var.cluster_name
  node_group_name = "worker-nodes"
  node_role_arn   = var.node_role_arn
  subnet_ids      = var.subnet_ids

  scaling_config {
    desired_size = var.desired
    max_size     = 3
    min_size     = 1
  }

  instance_types = [var.instance_type]
}