output "bucket_name" {
  value = aws_s3_bucket.site.id
}

output "bucket_arn" {
  value = aws_s3_bucket.site.arn
}

output "cloudfront_domain" {
  value = aws_cloudfront_distribution.site.domain_name
}

output "api_url" {
  value = "${aws_apigatewayv2_api.api.api_endpoint}/count"
}

output "github_actions_role_arn" {
  value = aws_iam_role.github_actions.arn
}