variable "cluster_name" {}
variable "node_role_arn" {}
variable "subnet_ids" { type = list(string) }
variable "instance_type" {}
variable "desired" {}