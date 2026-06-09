variable "vpc_cidr" {}
variable "subnet_cidrs" { type = list(string) }
variable "azs" { type = list(string) }