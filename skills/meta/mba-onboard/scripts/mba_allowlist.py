import argparse
import sys
from mba_common import MetaConfig, add_yes_arg, print_json, request_json, require_yes, main_error

def main() -> int:
    parser = argparse.ArgumentParser(description="Manage allowlist")
    sub = parser.add_subparsers(dest="allowlist_cmd", required=True)
    sub.add_parser("list", help="List allowlist")
    
    add_parser = sub.add_parser("add", help="Add consumer phone")
    add_parser.add_argument("--entity", required=True, help="Consumer phone (E.164)")
    
    remove_parser = sub.add_parser("remove", help="Remove consumer phone")
    remove_parser.add_argument("entry_id", help="Entry ID")
    add_yes_arg(remove_parser)

    args = parser.parse_args()
    config = MetaConfig.from_env()

    if args.allowlist_cmd == "list":
        result = request_json(config, "GET", "agent_config/allowlist")
    elif args.allowlist_cmd == "add":
        result = request_json(config, "POST", "agent_config/allowlist", body={"consumer_phone_number": args.entity})
    elif args.allowlist_cmd == "remove":
        require_yes(args, f"remove allowlist entry {args.entry_id}")
        result = request_json(config, "DELETE", f"agent_config/allowlist/{args.entry_id}")

    print_json(result)
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        sys.exit(main_error(exc))