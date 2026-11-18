import argparse
from pathlib import Path
from mba_common import MetaConfig, add_yes_arg, print_json, request_json, request_multipart, require_yes, load_json_file

def main():
    parser = argparse.ArgumentParser(description="FAQ, Websites, Files and Skills knowledge")
    sub = parser.add_subparsers(dest="action", required=True)

    faq_parser = sub.add_parser("faq", help="FAQ operations")
    faq_sub = faq_parser.add_subparsers(dest="faq_cmd", required=True)
    faq_sub.add_parser("list")
    faq_sub.add_parser("get").add_argument("id")
    faq_sub.add_parser("create").add_argument("--body-file", required=True)
    faq_upd = faq_sub.add_parser("update")
    faq_upd.add_argument("id")
    faq_upd.add_argument("--body-file", required=True)
    faq_del = faq_sub.add_parser("delete")
    faq_del.add_argument("id")
    add_yes_arg(faq_del)

    web_parser = sub.add_parser("web", help="Website operations")
    web_sub = web_parser.add_subparsers(dest="web_cmd", required=True)
    web_sub.add_parser("list")
    web_sub.add_parser("get").add_argument("id")
    web_sub.add_parser("create").add_argument("--body-file", required=True)
    web_upd = web_sub.add_parser("update")
    web_upd.add_argument("id")
    web_upd.add_argument("--body-file", required=True)
    web_del = web_sub.add_parser("delete")
    web_del.add_argument("id")
    add_yes_arg(web_del)

    file_parser = sub.add_parser("file", help="File knowledge operations")
    file_sub = file_parser.add_subparsers(dest="file_cmd", required=True)
    file_sub.add_parser("list")
    file_sub.add_parser("get").add_argument("id")
    file_upd = file_sub.add_parser("upload")
    file_upd.add_argument("file_path")
    file_upd.add_argument("--name")
    file_del = file_sub.add_parser("delete")
    file_del.add_argument("id")
    add_yes_arg(file_del)
    
    skills_parser = sub.add_parser("skills", help="Agent Skills (Instructions) operations")
    skills_sub = skills_parser.add_subparsers(dest="skills_cmd", required=True)
    skills_sub.add_parser("list")
    skills_sub.add_parser("get").add_argument("id")
    skills_sub.add_parser("create").add_argument("--body-file", required=True)
    skills_upd = skills_sub.add_parser("update")
    skills_upd.add_argument("id")
    skills_upd.add_argument("--body-file", required=True)
    skills_del = skills_sub.add_parser("delete")
    skills_del.add_argument("id")
    add_yes_arg(skills_del)

    args = parser.parse_args()
    config = MetaConfig.from_env()

    if args.action == "faq":
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

    elif args.action == "web":
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

    elif args.action == "file":
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
        
    elif args.action == "skills":
        if args.skills_cmd == "list":
            result = request_json(config, "GET", "agent_config/skills")
        elif args.skills_cmd == "get":
            result = request_json(config, "GET", f"agent_config/skills/{args.id}")
        elif args.skills_cmd == "create":
            result = request_json(config, "POST", "agent_config/skills", body=load_json_file(args.body_file))
        elif args.skills_cmd == "update":
            result = request_json(config, "PUT", f"agent_config/skills/{args.id}", body=load_json_file(args.body_file))
        elif args.skills_cmd == "delete":
            require_yes(args, f"delete agent skill {args.id}")
            result = request_json(config, "DELETE", f"agent_config/skills/{args.id}")
        print_json(result)

if __name__ == "__main__":
    main()