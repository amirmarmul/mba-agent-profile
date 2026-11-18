# Agent Skill Authoring Rules

When defining AI Agent Skills (behavioral guidelines, tone of voice, response patterns) via `python3 scripts/mba_skills.py`, you must adhere to strict API and logical constraints.

## 1. Schema Constraints
Every skill payload (`templates/skill.request.example.json`) requires three fields:

- **`title`**: 
  - Max length: 64 characters.
  - Allowed characters: Lowercase letters, numbers, and hyphens (`-`) only.
  - Restrictions: Cannot start or end with a hyphen.
  - Example: `greeting-skill`, `product-return-policy`. Avoid `skill-1`.

- **`description`**: 
  - Max length: 1,024 characters.
  - Purpose: Tells the AI *when* to apply this skill. Be specific about the trigger.
  - Example: "Apply when the customer first messages the agent to set the greeting tone."

- **`skill`**: 
  - Max length: 20,000 characters.
  - Purpose: The concrete instructions the agent must follow.

## 2. Behavioral Rules (No Conflicting Priorities)
The Meta Business Agent follows skills exactly as written.
- **Do not write conflicting skills**. If two different skills both claim priority for the exact same situation (e.g., two skills starting with "When the customer first messages... do this first"), the agent cannot resolve the conflict and will hallucinate or duplicate responses.
- **Consolidation**: If multiple actions must happen on the same trigger, consolidate them into a single skill with a numbered, sequential list.

**Bad Example (Conflicting)**:
- Skill A: "When user says hi, ask for their email."
- Skill B: "When user says hi, send the product catalog."

**Good Example (Consolidated)**:
- Skill A: "When user says hi: 1) Ask for their email. 2) If they provide it, send the product catalog."