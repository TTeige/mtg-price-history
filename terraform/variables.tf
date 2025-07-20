variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "eu-north-1"
}

variable "ecr_repository_url" {
  description = "ECR repository URL for card-search Docker image"
  type        = string
  default     = "115780940165.dkr.ecr.eu-north-1.amazonaws.com/mtg-pricing-search:latest"
}

variable "container_name" {
  description = "Name of the container for ECS task"
  type        = string
  default     = "card-search"
}

variable "container_port" {
  description = "Port the card-search container exposes"
  type        = number
  default     = 8080
}

variable "domain_name" {
  description = "Domain name to use for the ECS service"
  type        = string
  default     = "mtg-trade.timteige.com"
}

variable "hosted_zone_id" {
  description = "Route53 hosted zone ID for the domain"
  type        = string
    default     = "Z027906936FX6S14YVXDE"
}
