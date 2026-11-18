# UI Skills: Theory, Benefits, and Workflow

## 1. Theory & Concept
A **UI Skill** instructs the Meta Business Agent on when and how to respond using rich WhatsApp UI components instead of plain text. It links a specific behavioral trigger (the `instruction`) to a structured interactive element (the `component_type`), such as a Call-to-Action (CTA) button, image, interactive list, or WhatsApp Flow.

Instead of the LLM guessing how to format a URL or outputting raw text links, the AI Agent uses the UI Skill to securely map user intent to a native, high-converting WhatsApp message format. 

## 2. Supported Component Types
Based on the API schema, the agent supports:
- `cta_url`: A button containing an external URL.
- `flow`: A native WhatsApp Flow (requires a valid `flow_id`).
- `image`: A visual media response.
- `interactive_list`: A menu of selectable options.
- `location` / `location_request`: Sending or requesting map coordinates.
- `carousel_quick_reply` / `carousel_url`: Horizontal scrollable cards.

## 3. Benefits & Advantages
- **Eliminates Link Hallucinations:** Constrains the agent to use approved, hardcoded URLs or Flow IDs instead of inventing broken or unauthorized links.
- **Higher Conversion & Engagement:** Native CTA buttons, Carousels, and Flows provide a frictionless user experience compared to plain-text links.
- **Structured Data Collection:** Using `flow` components allows the business to collect structured form data (e.g., appointments, lead generation) natively within WhatsApp without asking the user to leave the chat.
- **Clear Separation of Concerns:** Separates the agent's conversational facts (Knowledge/FAQs) from its interactive transactional interfaces (UI Skills).

## 4. Operational Workflow
When tasked with adding or modifying an interactive UI component, follow this exact workflow:

### Step 1: Audit Existing UI Skills
Always run `python3 scripts/mba_ui_skills.py list` first. Check if a similar component already exists. Overlapping instructions (e.g., two different UI skills triggering on "when user asks to book") will confuse the agent's routing.

### Step 2: Draft the Payload
Copy `templates/uiskill.request.example.json` to a local working directory like `/tmp/uiskill.json`. Set the `title`, `component_type`, `status`, and most importantly, the `instruction`.
*Best Practice for `instruction`: Be explicit about the trigger intent and the UI element content.*
> "If a user asks to book a consultation or check schedules, send them a button with body text 'Click the link below to book', button label text 'Book Now', and URL https://example.com/book"

### Step 3: Validate Dependencies
If creating a `flow` component, ensure the `flow_id` is provided in the JSON and that the flow is officially published on Meta's side. A UI skill cannot be set to `enabled` if the underlying Flow is in a draft state or invalid.

### Step 4: Request Human Approval
Present the drafted JSON payload to the user, state the exact trigger condition, and wait for confirmation before mutating the agent's state.

### Step 5: Execute and Verify
Run `python3 scripts/mba_ui_skills.py create --body-file /tmp/uiskill.json`. 
Immediately follow up with `python3 scripts/mba_ui_skills.py list` or `get <id>` to confirm the UI Skill was successfully saved and its `status` is `enabled`.
