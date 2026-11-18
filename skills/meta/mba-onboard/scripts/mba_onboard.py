import argparse
from mba_common import MetaConfig, add_yes_arg, print_json, request_json, require_yes, load_json_file

def main():
    parser = argparse.ArgumentParser(description="Onboard, settings, and allowlist operations")
    sub = parser.add_subparsers(dest="action", required=True)

    sub.add_parser("check-eligibility", help="Check if entity is eligible for MBA")

    settings_parser = sub.add_parser("settings", help="Manage agent settings")
    settings_sub = settings_parser.add_subparsers(dest="settings_cmd", required=True)
    settings_sub.add_parser("get", help="Get settings")
    update_settings = settings_sub.add_parser("update", help="Update settings")
    update_settings.add_argument("--body-file", required=True, help="JSON body file")

    allowlist_parser = sub.add_parser("allowlist", help="Manage allowlist")
    allowlist_sub = allowlist_parser.add_subparsers(dest="allowlist_cmd", required=True)
    allowlist_sub.add_parser("list", help="List allowlist")
    add_allowlist = allowlist_sub.add_parser("add", help="Add consumer phone")
    add_allowlist.add_argument("--phone", required=True, help="Consumer phone (E.164)")
    remove_allowlist = allowlist_sub.add_parser("remove", help="Remove consumer phone")
    remove_allowlist.add_argument("entry_id", help="Entry ID")
    add_yes_arg(remove_allowlist)

    args = parser.parse_args()
    config = MetaConfig.from_env()

    if args.action == "check-eligibility":
        result = request_json(config, "GET", "agent_eligibility")
        print_json(result)

    elif args.action == "settings":
        if args.settings_cmd == "get":
            result = request_json(config, "GET", "agent_config/settings")
        elif args.settings_cmd == "update":
            result = request_json(config, "PUT", "agent_config/settings", body=load_json_file(args.body_file))
        else:
            raise ValueError(f"Unknown settings command: {args.settings_cmd}")
        print_json(result)

    elif args.action == "allowlist":
        if args.allowlist_cmd == "list":
            result = request_json(config, "GET", "agent_config/allowlist")
        elif args.allowlist_cmd == "add":
            result = request_json(config, "POST", "agent_config/allowlist", body={"consumer_phone_number": args.phone})
        elif args.allowlist_cmd == "remove":
            require_yes(args, f"remove allowlist entry {args.entry_id}")
            result = request_json(config, "DELETE", f"agent_config/allowlist/{args.entry_id}")
        else:
            raise ValueError(f"Unknown allowlist command: {args.allowlist_cmd}")
        print_json(result)

if __name__ == "__main__":
    main()
