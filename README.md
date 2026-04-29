# MDA IT Helpdesk AI (Phase 1 PoC)

## Overview
A serverless, RAG-enabled helpdesk assistant utilizing AWS S3, OpenSearch Vector Database, and Bedrock Knowledge Base through the Amazon Nova Lite model and Streamlit designed to support the Mississippi Development Authority answer general and redundant inquiries sent to the IT Helpdesk.

## Agency Problem
MDA employees need a fast, accurate approach to assist with generic and often repetitive IT troubleshooting inquiries, allowing IT staff to focus their efforts on more complex, high-level support tickets.

## PoC Scope and Demonstrated Capabilities
This PoC demonstrates the feasibility of using a localized AWS Bedrock Knowledge Base to retrieve and synthesize IT documentation into a conversational interface that can reliably answer relevant inquiries.

## Architecture Overview
**Frontend**: Streamlit
**Backend**: `boto3` Bedrock Agent Runtime
**LLM**: Amazon Nova Lite

## Repository Structure
* `/assets` - UI branded images
* `/docs` - Additional sectioned documentation
* `app.py` - Core application logic

## Setup
1. Clone the repository.
2. Run `pip install -r requirements.txt`.
3. Create an `.env` file based on `.env.example` and add your `KNOWLEDGE_BASE_ID`.

## Usage
Use `aws sso login` to refresh account token and allow the application to run until the token expires.
Run the application using `streamlit run app.py`.

## Data Notes
This repository does not include real agency data. Sensitive information has been replaced with safe sample placeholders.

## Limitations
This PoC was developed within a limited timeline and controlled environment. It may contain mock integrations, limited testing coverage, and simple user interfaces.

## Disclaimer
This repository contains code and supporting materials developed as part of a Mississippi Artificial Intelligence Innovation Hub Proof of Concept project. The contents are provided for prototype demonstration purposes. They are not production ready by default and may include simplified workflows, incomplete security guardrails, placeholder integrations, or reduced controls appropriate only for a Proof-of-Concept environment.

## License
MIT License