# Quality Assurance & Testing

## QA Testing Details
During the Proof of Concept development process, the model was subjected to a rigorous testing matrix designed to evaluate both retrieval accuracy and system guardrails. 

* **Target Accuracy:** >85%
* **Achieved Accuracy:** ~98%\*

\* This accuracy was yielded by our in- and post-development QA testing procedures, totaling over 300 inquiries to the AI Assistant. Failures detected during QA testing were subsequently handled via tweaking the textPromptTemplate.

## Test Categories
1. **Typical, Relevant Queries (In-Scope):** Evaluated the model's ability to pull highly specific instructions (e.g., MAGIC portal resets) from the vector database and format them cleanly.
2. **Adversarial Queries (Out-of-Scope):** Tested the model's prompt adherence by asking non-IT or highly sensitive questions. The model successfully refused to hallucinate and adhered to its system prompt.
3. **Semantic Boundary Queries:** Responses to inquiries with keywords similar to those found in the ingested data files were evaluated to ensure that the model would successfully refuse to answer these types of inquiries despite being semantically relevant (i.e., a inquiry of a *personal* printer's ink being low would originally trigger the retrieval of printer ink-related details from ingested data).
4. **Escalation Triggering:** Verified that the UI correctly captured "unanswerable" states and spawned the `mailto:` fallback button for human handoff.

## Resolved Issues
* **Prompt Bleed / Parsing Errors:** During early sandbox testing, the model occasionally output raw prompt templates. System instructions were refined, and the parsing error was fully resolved prior to the Streamlit integration.
* **Retrieval of Data for Semantic Boundary Inquiries:** As mentioned above, inquiries that included keywords found in the ingested data would originally yield a response with such data instead of refusal (see example in 3. of the "Test Categories" section above). With textPromptTemplate tweaks, this issue was successfully alleviated.