"""Local stdlib server for the ANKoS static viewer."""

from __future__ import annotations

import http.server
import shutil
import socketserver
from pathlib import Path


def serve(bundle_path: str | Path | None = None, port: int = 0, host: str = "127.0.0.1") -> None:
    """Serve the static viewer directory on localhost until interrupted."""

    static_dir = Path(__file__).with_name("static")
    if not static_dir.is_dir():
        raise FileNotFoundError(f"static viewer directory not found: {static_dir}")

    resolved_bundle = None if bundle_path is None else Path(bundle_path).resolve()
    if resolved_bundle is not None and not resolved_bundle.is_file():
        raise FileNotFoundError(f"bundle not found: {resolved_bundle}")

    class ViewerHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args: object, **kwargs: object) -> None:
            super().__init__(*args, directory=str(static_dir), **kwargs)

        def do_GET(self) -> None:
            if self.path.split("?", 1)[0] == "/bundle.ankos" and resolved_bundle is not None:
                self.send_response(200)
                self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Content-Length", str(resolved_bundle.stat().st_size))
                self.end_headers()
                with resolved_bundle.open("rb") as source:
                    shutil.copyfileobj(source, self.wfile)
                return
            super().do_GET()

    with socketserver.TCPServer((host, int(port)), ViewerHandler) as httpd:
        selected_port = httpd.server_address[1]
        url = f"http://{host}:{selected_port}/"
        if resolved_bundle is not None:
            url = f"{url}?bundle=bundle.ankos"
            print(f"Serving ANKoS viewer for {resolved_bundle}")
        print(f"Open {url}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped ANKoS viewer server")


__all__ = ["serve"]
