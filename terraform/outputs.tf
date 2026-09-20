output "bucket_name" {
  value = aws_s3_bucket.raw_data.bucket
}

output "pipeline_access_key_id" {
  value = aws_iam_access_key.pipeline_key.id
}

output "pipeline_secret_access_key" {
  value     = aws_iam_access_key.pipeline_key.secret
  sensitive = true
}