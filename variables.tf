variable "aws_region" {
  description = "AWS region to deploy into. Must be a region where your Bedrock model is available."
  type        = string
  default     = "eu-north-1"
}

variable "project_name" {
  description = "Name prefix used for all resources"
  type        = string
  default     = "simple-bedrock-chatbot"
}

variable "bedrock_model_id" {
  description = "Bedrock model ID to invoke. Must have model access enabled in the Bedrock console for your account/region. Nova Micro is Amazon's cheapest text model ($0.035 per 1M input tokens, $0.14 per 1M output tokens)."
  type        = string
  default     = "amazon.nova-micro-v1:0"
}
