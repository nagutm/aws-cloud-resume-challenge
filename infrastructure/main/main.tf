resource "aws_s3_bucket" "site" {
  bucket = var.bucket_name
}

resource "aws_s3_object" "index" {
  bucket = aws_s3_bucket.site.id
  key    = "index.html"
  source = "${path.module}/../../frontend/index.html"
  etag = filemd5("${path.module}/../../frontend/index.html")
  content_type = "text/html"
}