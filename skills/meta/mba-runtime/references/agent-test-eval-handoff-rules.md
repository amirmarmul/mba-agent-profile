# Agent Test and Evaluation Rules

## 1. Agent Test (`mba_test.py`)
- Purpose: Execute a dry-run prompt against the agent's current configured "brain" without needing a live WhatsApp client.
- Payload: `user_msg` (string, the human message), `conversation_id` (string, optional session key).
- Context: Passing the same `conversation_id` across multiple `mba_test.py` calls enables multi-turn memory tests.

## 2. Agent Evaluation (`mba_eval.py`)
- Purpose: Run a batch of predefined edge-cases (`eval_case_ids`) against the agent to measure baseline accuracy and regression.
- Flow: `run` -> returns a job ID -> poll `status` -> fetch `summary` or `details`.
- Results: Categorized into `passed`, `failed`, `skipped`. 
- Rule: Do not deploy an agent from `ALLOWLISTED_ONLY` to `EVERYONE` if evaluation results contain critical `failed` cases regarding business policy.

## 3. Thread Control Handoff (`mba_runtime.py`)
- API Route: `https://api.facebook.com/business/whatsapp/phone_numbers/{entity_id}/thread_control`
- Payload: `messaging_product: "whatsapp"`, `action` (`pass` or `release`), `to` (the E.164 phone number of the customer).
- Purpose: Temporarily suspends the Meta AI agent from responding to a specific user so a live human agent (or third-party bot) can take over.