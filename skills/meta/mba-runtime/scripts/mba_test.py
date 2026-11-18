import argparse
import sys
from mba_common import MetaConfig, print_json, request_json, write_run_output, main_error

def main() -> int:
    parser = argparse.ArgumentParser(description="Test agent with a message")
    parser.add_argument("user_msg", help="Message text")
    parser.add_argument("--conversation-id", help="Optional conversation ID for multi-turn")
    parser.add_argument("--save", action="store_true", help="Save response to mba/<ENTITY_ID>/tests/")

    args = parser.parse_args()
    config = MetaConfig.from_env()

    payload = {"user_msg": args.user_msg}
    if args.conversation_id:
        payload["conversation_id"] = args.conversation_id

    result = request_json(config, "POST", "agent_test", body=payload)
    print_json(result)
    if args.save:
        saved = write_run_output("tests", result, prefix="agent-test")
        print(f"\nSaved to {saved}", file=sys.stderr)
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        sys.exit(main_error(exc))