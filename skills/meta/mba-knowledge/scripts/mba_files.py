import argparse
import sys
from pathlib import Path
from mba_common import MetaConfig, add_yes_arg, print_json, request_json, request_multipart, require_yes, main_error

def main() -> int:
    parser = argparse.ArgumentParser(description="File knowledge operations")
    sub = parser.add_subparsers(dest="file_cmd", required=True)
    sub.add_parser("list")
    sub.add_parser("get").add_argument("id")
    
    file_upd = sub.add_parser("upload")
    file_upd.add_argument("file_path")
    file_upd.add_argument("--name")
    
    file_del = sub.add_parser("delete")
    file_del.add_argument("id")
    add_yes_arg(file_del)

    args = parser.parse_args()
    config = MetaConfig.from_env()

    if args.file_cmd == "list":
        result = request_json(config, "GET", "agent_config/files")
    elif args.file_cmd == "get":
        result = request_json(config, "GET", f"agent_config/files/{args.id}")
    elif args.file_cmd == "upload":
        p = Path(args.file_path)
        content = p.read_bytes()
        filename = args.name or p.name
        result = request_multipart(
            config,
            "POST",
            "agent_config/files",
            fields={"file_name": filename},
            file_fields={"file": (filename, content)}
        )
    elif args.file_cmd == "delete":
        require_yes(args, f"delete file {args.id}")
        result = request_json(config, "DELETE", f"agent_config/files/{args.id}")
    
    print_json(result)
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        sys.exit(main_error(exc))