resource "aws_s3_bucket" "raw_data" {
  bucket = "ledgerra-raw-data-${data.aws_caller_identity.current.account_id}"
}