import argparse
import sys
from mba_common import MetaConfig, print_json, request_json, main_error

def main() -> int:
    parser = argparse.ArgumentParser(description="Check if entity is eligible for MBA")
    args = parser.parse_args()
    config = MetaConfig.from_env()

    result = request_json(config, "GET", "agent_eligibility")
    print_json(result)
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        sys.exit(main_error(exc))