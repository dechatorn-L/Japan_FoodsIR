import sys
import json
import urllib.parse
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import argparse

from ..engine import get_engine

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
WEB_DIR = PROJECT_ROOT / "web"


class JapaneseFoodIRHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query_params = urllib.parse.parse_qs(parsed_url.query)

        if path == "/api/search":
            self.handle_search_api(query_params)
        elif path == "/api/clusters":
            self.handle_clusters_api()
        elif path == "/api/inverted_index":
            self.handle_inverted_index_api(query_params)
        elif path == "/api/pipeline/status":
            self.handle_pipeline_status_api()
        elif path == "/" or path == "":
            self.path = "/index.html"
            super().do_GET()
        else:
            super().do_GET()

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        
        content_length = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else "{}"
        
        try:
            body_json = json.loads(post_body)
        except Exception:
            body_json = {}

        if path == "/api/pantry":
            self.handle_pantry_api(body_json)
        elif path == "/api/evaluate":
            self.handle_evaluate_api(body_json)
        elif path == "/api/pipeline/reindex":
            self.handle_pipeline_reindex_api()
        elif path == "/api/pipeline/scrape":
            self.handle_pipeline_scrape_api(body_json)
        else:
            self.send_error(404, "Endpoint not found")

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def send_json_response(self, data, status_code=200):
        response_bytes = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(response_bytes)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response_bytes)

    def handle_search_api(self, query_params):
        query = query_params.get('q', [''])[0]
        top_k = int(query_params.get('top_k', [15])[0])
        cluster_filter = query_params.get('cluster', [None])[0]
        if cluster_filter is not None and cluster_filter != 'all':
            cluster_filter = int(cluster_filter)
        else:
            cluster_filter = None

        engine = get_engine()
        results = engine.search(query, top_k=top_k, cluster_filter=cluster_filter)
        self.send_json_response(results)

    def handle_clusters_api(self):
        engine = get_engine()
        clusters_summary = engine.get_clusters_summary()
        self.send_json_response(clusters_summary)

    def handle_inverted_index_api(self, query_params):
        term = query_params.get('term', [''])[0]
        engine = get_engine()
        result = engine.inspect_inverted_index(term)
        self.send_json_response(result)

    def handle_pantry_api(self, body_json):
        ingredients = body_json.get('ingredients', [])
        top_k = int(body_json.get('top_k', 15))
        engine = get_engine()
        results = engine.pantry_search(ingredients, top_k=top_k)
        self.send_json_response(results)

    def handle_evaluate_api(self, body_json):
        query = body_json.get('query', '')
        k = int(body_json.get('k', 10))
        engine = get_engine()
        
        search_res = engine.search(query, top_k=50)
        retrieved_ids = [r['id'] for r in search_res['results']]
        
        metrics = engine.compute_evaluation_metrics(retrieved_ids, query, k=k)
        self.send_json_response(metrics)

    def handle_pipeline_status_api(self):
        engine = get_engine()
        status = engine.get_status()
        self.send_json_response(status)

    def handle_pipeline_reindex_api(self):
        engine = get_engine()
        status = engine.reindex_existing_data()
        self.send_json_response({'success': True, 'message': 'Dataset cleaned and VSM models reindexed successfully.', 'status': status})

    def handle_pipeline_scrape_api(self, body_json):
        amount = int(body_json.get('amount', 20))
        engine = get_engine()
        res = engine.run_scraping_pipeline(target_count=amount)
        self.send_json_response(res)


def run_server(host: str = "0.0.0.0", port: int = 8000):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

    print("Initializing Japanese Foods IR Engine...")
    engine = get_engine()
    print(f"Loaded {len(engine.df)} Japanese recipes and built Inverted Index.")

    # Port Fallback Loop (handles occupied ports smoothly)
    candidate_ports = [port, 8000, 8080, 8081, 8090, 8001, 8002, 8888]
    if port not in candidate_ports:
        candidate_ports.insert(0, port)

    httpd = None
    active_port = port

    for p in candidate_ports:
        try:
            server_address = (host, p)
            httpd = HTTPServer(server_address, JapaneseFoodIRHandler)
            active_port = p
            break
        except OSError as e:
            if "10048" in str(e) or "already in use" in str(e).lower():
                continue
            raise e

    if httpd is None:
        # Fallback to ephemeral random OS port
        server_address = (host, 0)
        httpd = HTTPServer(server_address, JapaneseFoodIRHandler)
        active_port = httpd.server_port
    
    print("\n" + "="*55)
    print(f" [Japanese Foods IR] Web Server is running!")
    print(f" Local URL:    http://localhost:{active_port}")
    print(f" Network URL:  http://127.0.0.1:{active_port}")
    print("="*55 + "\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Japanese Foods IR Server...")
        httpd.server_close()
        sys.exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Japanese Foods IR Server")
    parser.add_argument("--port", type=int, default=8000, help="Port (default: 8000)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host (default: 0.0.0.0)")
    args = parser.parse_args()
    run_server(host=args.host, port=args.port)
