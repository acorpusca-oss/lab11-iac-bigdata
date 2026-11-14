
resource "aws_glue_catalog_database" "domains" {
  for_each = toset(var.domains)

  catalog_id  = var.catalog_id
  name        = "${each.value}_domain"
  description = "Data Catalog for ${each.value} domain"

  tags = {
    Domain      = each.value
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
