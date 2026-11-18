import argparse
import sys
from mba_common import MetaConfig, add_yes_arg, print_json, request_json, require_yes, load_json_file, main_error

def main() -> int:
    parser = argparse.ArgumentParser(description="Agent UI Skills operations")
    sub = parser.add_subparsers(dest="cmd", required=True)
    
    sub.add_parser("list")
    
    sub.add_parser("get").add_argument("id")
    
    sub.add_parser("create").add_argument("--body-file", required=True)
    
    upd = sub.add_parser("update")
    upd.add_argument("id")
    upd.add_argument("--body-file", required=True)
    
    del_cmd = sub.add_parser("delete")
    del_cmd.add_argument("id")
    add_yes_arg(del_cmd)

    args = parser.parse_args()
    config = MetaConfig.from_env()

    if args.cmd == "list":
        result = request_json(config, "GET", "agent-ui-skills")
    elif args.cmd == "get":
        result = request_json(config, "GET", f"agent-ui-skills/{args.id}")
    elif args.cmd == "create":
        result = request_json(config, "POST", "agent-ui-skills", body=load_json_file(args.body_file))
    elif args.cmd == "update":
        result = request_json(config, "PUT", f"agent-ui-skills/{args.id}", body=load_json_file(args.body_file))
    elif args.cmd == "delete":
        require_yes(args, f"delete UI skill {args.id}")
        result = request_json(config, "DELETE", f"agent-ui-skills/{args.id}")
    
    else:
        result = {}

    print_json(result)
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        sys.exit(main_error(exc))
