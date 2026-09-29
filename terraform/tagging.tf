# Flag resources that are missing the required cost-allocation tags.
resource "aws_config_config_rule" "required_tags" {
  name = "required-cost-allocation-tags"
  source {
    owner             = "AWS"
    source_identifier = "REQUIRED_TAGS"
  }
  input_parameters = jsonencode({
    tag1Key = var.required_tags[0]
    tag2Key = var.required_tags[1]
    tag3Key = var.required_tags[2]
    tag4Key = var.required_tags[3]
  })
}
