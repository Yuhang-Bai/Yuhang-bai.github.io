import os
import subprocess
import sys
import threading
import time
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HOST = "127.0.0.1"
PORT = 4000
POLL_INTERVAL = 1.0
WATCH_FILES = ("publications.bib", "build_site.py")


def file_mtime(path):
    try:
        return os.path.getmtime(path)
    except FileNotFoundError:
        return None


def run_build(script_dir):
    result = subprocess.run(
        [sys.executable, "build_site.py"],
        cwd=script_dir,
        check=False,
    )
    if result.returncode != 0:
        print("Build failed. Waiting for the next file change.")


def watch_and_build(script_dir):
    watched_paths = {name: os.path.join(script_dir, name) for name in WATCH_FILES}
    mtimes = {name: file_mtime(path) for name, path in watched_paths.items()}

    while True:
        time.sleep(POLL_INTERVAL)
        changed = False
        for name, path in watched_paths.items():
            current = file_mtime(path)
            if current != mtimes[name]:
                mtimes[name] = current
                changed = True

        if changed:
            print("\nDetected changes. Rebuilding site...\n")
            run_build(script_dir)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    run_build(script_dir)

    handler = partial(SimpleHTTPRequestHandler, directory=script_dir)
    server = ThreadingHTTPServer((HOST, PORT), handler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    print(f"\nPreview server running at http://{HOST}:{PORT}")
    print("Changes to publications.bib or build_site.py will rebuild the site automatically.")
    print("Press Ctrl+C to stop.\n")

    try:
        watch_and_build(script_dir)
    except KeyboardInterrupt:
        print("\nStopping preview server...")
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
