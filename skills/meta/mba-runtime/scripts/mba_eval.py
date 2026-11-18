import argparse
import sys
from mba_common import MetaConfig, print_json, request_json, load_json_file, write_run_output, main_error

def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluation operations")
    sub = parser.add_subparsers(dest="eval_cmd", required=True)
    
    ec = sub.add_parser("cases")
    ec.add_argument("--save", action="store_true")
    
    er = sub.add_parser("run")
    er.add_argument("--eval-case-ids", required=True, help="Comma-separated pfbid list")
    er.add_argument("--body-file", required=True, help="JSON body file")
    er.add_argument("--no-save", action="store_true", help="Disable saving to workspace/")
    
    es = sub.add_parser("status")
    es.add_argument("job_id")
    es.add_argument("--no-save", action="store_true")
    
    esu = sub.add_parser("summary")
    esu.add_argument("--summary-ids", required=True, help="Comma-separated summary IDs")
    esu.add_argument("--no-save", action="store_true")
    
    ed = sub.add_parser("details")
    ed.add_argument("--eval-ids", required=True, help="Comma-separated eval IDs")
    ed.add_argument("--no-save", action="store_true")

    args = parser.parse_args()
    config = MetaConfig.from_env()

    if args.eval_cmd == "cases":
        result = request_json(config, "GET", "agent-eval/cases")
        print_json(result)
        if getattr(args, "save", False):
            saved = write_run_output("eval", result, prefix="cases")
            print(f"\nSaved to {saved}", file=sys.stderr)

    elif args.eval_cmd == "run":
        query = {"eval_case_ids": args.eval_case_ids}
        result = request_json(config, "POST", "agent-eval/run", query=query, body=load_json_file(args.body_file))
        print_json(result)
        if not getattr(args, "no_save", False):
            saved = write_run_output("eval", result, prefix="run")
            print(f"\nSaved to {saved}", file=sys.stderr)

    elif args.eval_cmd == "status":
        result = request_json(config, "GET", f"agent-eval/run/{args.job_id}")
        print_json(result)
        if not getattr(args, "no_save", False):
            saved = write_run_output("eval", result, prefix=f"status-{args.job_id}")
            print(f"\nSaved to {saved}", file=sys.stderr)

    elif args.eval_cmd == "summary":
        query = {"summary_ids": args.summary_ids}
        result = request_json(config, "GET", "agent-eval/summary", query=query)
        print_json(result)
        if not getattr(args, "no_save", False):
            saved = write_run_output("eval", result, prefix="summary")
            print(f"\nSaved to {saved}", file=sys.stderr)

    elif args.eval_cmd == "details":
        query = {"eval_ids": args.eval_ids}
        result = request_json(config, "GET", "agent-eval/details", query=query)
        print_json(result)
        if not getattr(args, "no_save", False):
            saved = write_run_output("eval", result, prefix="details")
            print(f"\nSaved to {saved}", file=sys.stderr)

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        sys.exit(main_error(exc))