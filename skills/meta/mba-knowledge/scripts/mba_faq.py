import argparse
import sys
from mba_common import MetaConfig, add_yes_arg, print_json, request_json, require_yes, load_json_file, main_error

def main() -> int:
    parser = argparse.ArgumentParser(description="FAQ operations")
    sub = parser.add_subparsers(dest="faq_cmd", required=True)
    sub.add_parser("list")
    sub.add_parser("get").add_argument("id")
    sub.add_parser("create").add_argument("--body-file", required=True)
    
    faq_upd = sub.add_parser("update")
    faq_upd.add_argument("id")
    faq_upd.add_argument("--body-file", required=True)
    
    faq_del = sub.add_parser("delete")
    faq_del.add_argument("id")
    add_yes_arg(faq_del)

    args = parser.parse_args()
    config = MetaConfig.from_env()

    if args.faq_cmd == "list":
        result = request_json(config, "GET", "agent_config/faq")
    elif args.faq_cmd == "get":
        result = request_json(config, "GET", f"agent_config/faq/{args.id}")
    elif args.faq_cmd == "create":
        result = request_json(config, "POST", "agent_config/faq", body=load_json_file(args.body_file))
    elif args.faq_cmd == "update":
        result = request_json(config, "PUT", f"agent_config/faq/{args.id}", body=load_json_file(args.body_file))
    elif args.faq_cmd == "delete":
        require_yes(args, f"delete FAQ {args.id}")
        result = request_json(config, "DELETE", f"agent_config/faq/{args.id}")
    
    print_json(result)
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        sys.exit(main_error(exc))