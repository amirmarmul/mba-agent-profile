# Agent Skill Mutation Workflow

Use when creating or updating Meta Business Agent behavior skills through `python3 scripts/mba_skills.py`.

## Sequence

1. Inspect existing agent skills with `python3 scripts/mba_skills.py list` before drafting, so new behavior does not duplicate or conflict with existing skills.
2. Draft payload from `templates/skill.request.example.json` shape:
   - `title`: stable kebab-case behavior name.
   - `description`: when this behavior applies.
   - `skill`: concrete rules the WhatsApp agent must follow.
3. Save draft payload before mutation:
   - Preferred path: `workspace/<META_ENTITY_ID>/changelog/payloads/YYYY-MM-DD_<topic>-skill.json`.
   - If entity ID cannot be read, use `workspace/unknown/changelog/payloads/` rather than blocking payload prep.
4. Ask user approval before `python3 scripts/mba_skills.py create`, `update`, or `delete`.
   - Provide exact script path, e.g. `python3 scripts/mba_skills.py create --body-file /path/to/payload`
   - Wait for "yes", "proceed", or "approve".
5. After approval, execute mutation.
6. Log executed mutation to `workspace/<ENTITY_ID-or-unknown>/changelog/history.md` with:
   - Date/Time
   - Action
   - Payload path
   - Reason/Context
   - Outcome including returned skill ID or error

## Behavior-rule drafting pattern

For connector-backed behavior skills, make rules deterministic:

- Name connector tool to use, e.g. `list_coupons`.
- Define output routing by result count or clear condition.
- Add exception rules for explicit user requests.
- Prohibit inventing data not returned by connector tool.

Example rule class: promo/voucher UI routing.

- Ask for active promo/voucher: use `list_coupons` when live voucher data is needed.
- 1-3 results: WhatsApp reply buttons.
- 4-10 results: WhatsApp list.
- More than 10 results: summarize or ask user to narrow preference.
- If user asks for randomized text/copy variations/shuffled wording: plain text only, no interactive UI.
