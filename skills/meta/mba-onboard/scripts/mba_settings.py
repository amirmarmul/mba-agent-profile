import argparse
import sys
from mba_common import MetaConfig, print_json, request_json, load_json_file, main_error

def main() -> int:
    parser = argparse.ArgumentParser(description="Manage agent settings")
    sub = parser.add_subparsers(dest="settings_cmd", required=True)
    sub.add_parser("get", help="Get settings")
    
    update_parser = sub.add_parser("update", help="Update settings")
    update_parser.add_argument("--body-file", required=True, help="JSON body file")

    args = parser.parse_args()
    config = MetaConfig.from_env()

    if args.settings_cmd == "get":
        result = request_json(config, "GET", "agent_config/settings")
    elif args.settings_cmd == "update":
        result = request_json(config, "PUT", "agent_config/settings", body=load_json_file(args.body_file))
    
    print_json(result)
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        sys.exit(main_error(exc))