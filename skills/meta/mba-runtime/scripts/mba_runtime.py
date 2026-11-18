import argparse
import sys
from mba_common import MetaConfig, print_json, request_json, load_json_file, main_error

def main() -> int:
    parser = argparse.ArgumentParser(description="Thread Control and Agent Events")
    sub = parser.add_subparsers(dest="runtime_cmd", required=True)
    
    # Thread Control
    tc = sub.add_parser("thread-control", help="Pass or release thread")
    tc.add_argument("tc_action", choices=["pass", "release"])
    tc.add_argument("consumer_id")

    # Events
    ev = sub.add_parser("event", help="Trigger agent event")
    ev.add_argument("consumer_id")
    ev.add_argument("--body-file", required=True)

    ev_stat = sub.add_parser("event-status", help="Check event status")
    ev_stat.add_argument("event_id")

    args = parser.parse_args()
    config = MetaConfig.from_env()

    if args.runtime_cmd == "thread-control":
        payload = {
            "messaging_product": "whatsapp",
            "action": args.tc_action,
            "to": args.consumer_id
        }
        result = request_json(config, "POST", "thread_control", body=payload)
    elif args.runtime_cmd == "event":
        payload = {
            "to": args.consumer_id,
            "event": load_json_file(args.body_file)
        }
        result = request_json(config, "POST", "agent_event", body=payload)
    elif args.runtime_cmd == "event-status":
        result = request_json(config, "GET", f"agent_event/{args.event_id}")

    print_json(result)
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        sys.exit(main_error(exc))