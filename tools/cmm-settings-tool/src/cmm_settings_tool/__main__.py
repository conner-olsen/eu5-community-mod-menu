import argparse
import webbrowser
from .server import run_server


def main():
    parser = argparse.ArgumentParser(description="CMM Settings Tool")
    parser.add_argument(
        "--port", type=int, default=5005, help="Port to run the server on"
    )
    parser.add_argument(
        "--no-open", action="store_true", help="Do not auto-open browser"
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    args = parser.parse_args()

    url = f"http://{args.host}:{args.port}"
    print(f"CMM Settings Tool running at {url}")
    print("Press Ctrl+C to stop.")

    if not args.no_open:
        webbrowser.open(url)

    run_server(args.host, args.port)


if __name__ == "__main__":
    main()
