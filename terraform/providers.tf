terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.40.0"
    }
  }
}

terraform {
  backend "s3" {
    bucket         = "capstone-bucket-26"
    key            = "capstone-backend/terraform.tfstate"
    region         = "us-east-1"
    use_lockfile = true
  }
}