output "chat_endpoint" {
  description = "POST to this URL to chat"
  value       = "${aws_apigatewayv2_api.chat_api.api_endpoint}/chat"
}

output "frontend_url" {
  description = "Open this URL in a browser to use the chat UI"
  value       = aws_s3_bucket_website_configuration.frontend.website_endpoint
}
