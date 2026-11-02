import argparse
import os
import sys

DEFAULT_QUERY = "Show top 3 US trending videos with metadata and thumbnails"


def main():
    parser = argparse.ArgumentParser(description="YouTube tool calling agent")
    parser.add_argument("query", nargs="?", default=DEFAULT_QUERY)
    parser.add_argument(
        "--mode",
        choices=["recursive", "fixed"],
        default="recursive",
        help="recursive: any number of tool rounds (default) | fixed: exactly 2 tool rounds",
    )
    args = parser.parse_args()

    from chains import fixed_chain, universal_chain

    if args.mode == "fixed":
        answer = fixed_chain.invoke({"query": args.query})
    else:
        messages = universal_chain.invoke({"query": args.query})
        # the full history is returned; the last message is the final answer
        print(f"({len(messages)} messages exchanged)\n")
        answer = messages[-1].content

    print(answer)

"""Usage:
    python main.py "Summarize https://www.youtube.com/watch?v=T-D1OfcDW1M"
    python main.py --mode fixed  "Summarize https://www.youtube.com/watch?v=T-D1OfcDW1M"
"""

if __name__ == "__main__":
    main()
