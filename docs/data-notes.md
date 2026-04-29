# Data Management & Ingestion Notes

## Document Preparation & Sanitization
Prior to ingestion into the AWS environment, all raw IT documentation underwent a rigorous manual scrubbing process to ensure compliance and security:
* **PII & Credential Removal:** All placeholder passwords, live IP addresses, and sensitive employee data were stripped from the source files and replaced with fake and generic alternatives.
* **Typesetting for LLMs:** Documents were converted into clean Markdown (`.md`) format to optimize semantic chunking within the Amazon Bedrock Knowledge Base.

## Knowledge Base Syncing
The vector database is treated as read-only by the application. To update the AI's knowledge:
1. Upload new/updated `.md` IT manuals to the designated S3 bucket.
2. Trigger a manual sync via the AWS Bedrock Console to re-index the OpenSearch Serverless database.