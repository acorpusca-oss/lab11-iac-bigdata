resource "aws_s3_bucket" "data_lake" {
  bucket = var.data_lake_bucket

  tags = {
    Project     = "UCV Big Data"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
