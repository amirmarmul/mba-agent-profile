import argparse
import sys
from mba_common import MetaConfig, add_yes_arg, print_json, request_json, require_yes, load_json_file, main_error

def main() -> int:
    parser = argparse.ArgumentParser(description="Connector operations")
    sub = parser.add_subparsers(dest="action", required=True)

    sub.add_parser("list")
    sub.add_parser("get").add_argument("id")
    sub.add_parser("create").add_argument("--body-file", required=True)
    upd = sub.add_parser("update")
    upd.add_argument("id")
    upd.add_argument("--body-file", required=True)
    del_parser = sub.add_parser("delete")
    del_parser.add_argument("id")
    add_yes_arg(del_parser)

    auth = sub.add_parser("auth", help="Upsert API key for connector")
    auth.add_argument("id")
    auth.add_argument("--body-file", required=True)

    logs = sub.add_parser("logs", help="Get connector logs")
    logs.add_argument("id")
    logs.add_argument("--start-time", type=int)
    logs.add_argument("--end-time", type=int)
    logs.add_argument("--limit", type=int)
    logs.add_argument("--tool-id")
    logs.add_argument("--include-stats", action="store_true")
    logs.add_argument("--summary-only", action="store_true")
    logs.add_argument("--top-n", type=int)

    args = parser.parse_args()
    config = MetaConfig.from_env()

    if args.action == "list":
        result = request_json(config, "GET", "agent_connectors")
    elif args.action == "get":
        result = request_json(config, "GET", f"agent_connectors/{args.id}")
    elif args.action == "create":
        result = request_json(config, "POST", "agent_connectors/", body=load_json_file(args.body_file))
    elif args.action == "update":
        result = request_json(config, "PUT", f"agent_connectors/{args.id}", body=load_json_file(args.body_file))
    elif args.action == "delete":
        require_yes(args, f"delete connector {args.id}")
        result = request_json(config, "DELETE", f"agent_connectors/{args.id}")
    elif args.action == "auth":
        result = request_json(config, "POST", f"agent_connectors/{args.id}/upsertApiKey", body=load_json_file(args.body_file))
    elif args.action == "logs":
        query = {
            "start_time": args.start_time,
            "end_time": args.end_time,
            "limit": args.limit,
            "tool_id": args.tool_id,
            "include_stats": "true" if args.include_stats else None,
            "summary_only": "true" if args.summary_only else None,
            "top_n": args.top_n,
        }
        result = request_json(config, "GET", f"agent_connectors/{args.id}/logs", query=query)

    print_json(result)
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        sys.exit(main_error(exc))