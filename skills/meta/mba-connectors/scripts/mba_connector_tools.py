import argparse
import sys
from mba_common import MetaConfig, add_yes_arg, print_json, request_json, require_yes, load_json_file, main_error

def main() -> int:
    parser = argparse.ArgumentParser(description="Connector Tools operations")
    sub = parser.add_subparsers(dest="tools_cmd", required=True)

    sub.add_parser("list").add_argument("connector_id")

    t_get = sub.add_parser("get")
    t_get.add_argument("connector_id")
    t_get.add_argument("tool_id")

    t_create = sub.add_parser("create")
    t_create.add_argument("connector_id")
    t_create.add_argument("--body-file", required=True)

    t_update = sub.add_parser("update")
    t_update.add_argument("connector_id")
    t_update.add_argument("tool_id")
    t_update.add_argument("--body-file", required=True)

    t_del = sub.add_parser("delete")
    t_del.add_argument("connector_id")
    t_del.add_argument("tool_id")
    add_yes_arg(t_del)

    t_run = sub.add_parser("run")
    t_run.add_argument("connector_id")
    t_run.add_argument("tool_id")
    t_run.add_argument("--body-file", required=True)

    args = parser.parse_args()
    config = MetaConfig.from_env()

    base_path = f"agent_connectors/{args.connector_id}/tools"
    if args.tools_cmd == "list":
        result = request_json(config, "GET", base_path)
    elif args.tools_cmd == "get":
        result = request_json(config, "GET", f"{base_path}/{args.tool_id}")
    elif args.tools_cmd == "create":
        result = request_json(config, "POST", f"{base_path}/", body=load_json_file(args.body_file))
    elif args.tools_cmd == "update":
        result = request_json(config, "PUT", f"{base_path}/{args.tool_id}", body=load_json_file(args.body_file))
    elif args.tools_cmd == "delete":
        require_yes(args, f"delete tool {args.tool_id} from connector {args.connector_id}")
        result = request_json(config, "DELETE", f"{base_path}/{args.tool_id}")
    elif args.tools_cmd == "run":
        result = request_json(config, "POST", f"{base_path}/{args.tool_id}/run", body=load_json_file(args.body_file))

    print_json(result)
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        sys.exit(main_error(exc))