import argparse
import sys
from mba_common import MetaConfig, add_yes_arg, print_json, request_json, require_yes, load_json_file, main_error

def main() -> int:
    parser = argparse.ArgumentParser(description="Website operations")
    sub = parser.add_subparsers(dest="web_cmd", required=True)
    sub.add_parser("list")
    sub.add_parser("get").add_argument("id")
    sub.add_parser("create").add_argument("--body-file", required=True)
    
    web_upd = sub.add_parser("update")
    web_upd.add_argument("id")
    web_upd.add_argument("--body-file", required=True)
    
    web_del = sub.add_parser("delete")
    web_del.add_argument("id")
    add_yes_arg(web_del)

    args = parser.parse_args()
    config = MetaConfig.from_env()

    if args.web_cmd == "list":
        result = request_json(config, "GET", "agent_config/websites")
    elif args.web_cmd == "get":
        result = request_json(config, "GET", f"agent_config/websites/{args.id}")
    elif args.web_cmd == "create":
        result = request_json(config, "POST", "agent_config/websites", body=load_json_file(args.body_file))
    elif args.web_cmd == "update":
        result = request_json(config, "PUT", f"agent_config/websites/{args.id}", body=load_json_file(args.body_file))
    elif args.web_cmd == "delete":
        require_yes(args, f"delete website {args.id}")
        result = request_json(config, "DELETE", f"agent_config/websites/{args.id}")
    
    print_json(result)
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        sys.exit(main_error(exc))