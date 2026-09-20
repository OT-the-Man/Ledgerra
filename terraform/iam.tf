resource "aws_iam_user" "pipeline" {
  name = "ledgerra-pipeline"
}

resource "aws_iam_policy" "pipeline_s3_access" {
  name        = "ledgerra-pipeline-s3-access"
  description = "Least-privilege: read/write only to the Ledgerra raw data bucket"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:PutObject", "s3:ListBucket"]
        Resource = [
          aws_s3_bucket.raw_data.arn,
          "${aws_s3_bucket.raw_data.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_user_policy_attachment" "pipeline_attach" {
  user       = aws_iam_user.pipeline.name
  policy_arn = aws_iam_policy.pipeline_s3_access.arn
}

resource "aws_iam_access_key" "pipeline_key" {
  user = aws_iam_user.pipeline.name
}