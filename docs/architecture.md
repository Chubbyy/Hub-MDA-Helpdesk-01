# System Architecture

## Overview
The MDA IT Helpdesk Assistant utilizes a serverless Retrieval-Augmented Generation (RAG) architecture built entirely on AWS. The system is designed to securely ingest, vectorize, and retrieve agency-specific IT documentation without exposing sensitive data to public LLM training sets.

## Component Pipeline
1. **Data Ingestion (Amazon S3):** Scrubbed IT manuals and runbooks are stored in a secure S3 bucket.
2. **Vectorization & Indexing (Amazon Bedrock Knowledge Bases):** The Bedrock KB automatically syncs with the S3 bucket, chunks the documents, and converts them into vector embeddings.
3. **Vector Storage (Amazon OpenSearch Serverless):** Embeddings are securely stored and queried using semantic search.
4. **Inference (Amazon Nova Lite via Bedrock):** When a user asks a question, Bedrock retrieves the most relevant semantic chunks from OpenSearch, packages them as context alongside the prompt, and passes them to the Nova Lite model for response generation.
5. **Frontend Application (Streamlit):** A custom Python web interface communicates directly with the Bedrock API via the `boto3` SDK, providing a seamless, high-quality chat experience.

## Escalation Protocol
If the inference engine cannot confidently answer a query based on the ingested context, it is programmed to decline safely and trigger a dynamic `mailto:` UI element, routing the user to human IT support.