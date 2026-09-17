output "chat_endpoint" {
  description = "POST to this URL to chat"
  value       = "${aws_apigatewayv2_api.chat_api.api_endpoint}/chat"
}
