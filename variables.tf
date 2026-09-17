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
  description = "Bedrock model/inference-profile ID to invoke. Nova Micro can only be invoked via its EU cross-region inference profile from eu-north-1, not its bare model ID."
  type        = string
  default     = "eu.amazon.nova-micro-v1:0"
}
