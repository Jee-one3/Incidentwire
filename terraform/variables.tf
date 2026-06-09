variable "region" {
default = "us-east-1"
}

variable "cluster_name" {
default = "monitoring-cluster"
}

variable "node_instance_type" {
  default = "t3.small"
}

variable "desired_capacity" {
  default = 3
}