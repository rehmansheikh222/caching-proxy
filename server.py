from flask import Flask, request, Response
import requests
from cachetools import TTLCache

cache = TTLCache(maxsize=100, ttl=300)


def start_server(port, origin):
    app = Flask(__name__)

    @app.route('/', defaults={'path': ''}, methods=['GET'])
    @app.route('/<path:path>', methods=['GET'])
    def proxy(path):
        cache_key = request.full_path

        # Check cache
        if cache_key in cache:
            cached_response = cache[cache_key]
            response = Response(
                cached_response['data'], cached_response['status'], cached_response['headers'])
            response.headers['X-Cache'] = 'HIT'
        else:
            # Fetch from origin server
            url = f"{origin}/{path}"
            upstream_response = requests.get(url, params=request.args)

            # Store minimal response data in the cache
            cache[cache_key] = {
                'data': upstream_response.content,
                'status': upstream_response.status_code,
                'headers': {'Content-Type': upstream_response.headers.get('Content-Type', 'text/plain')}
            }

            # Build response
            response = Response(upstream_response.content,
                                upstream_response.status_code)
            response.headers['Content-Type'] = upstream_response.headers.get(
                'Content-Type', 'text/plain')
            response.headers['X-Cache'] = 'MISS'

        return response

    print(f"Starting caching proxy on port {port}, forwarding to {origin}")
    app.run(port=port)


def clear_cache():
    cache.clear()
    print("Cache cleared.")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Simple Caching Proxy Server")
    parser.add_argument('--port', type=int, help="Port to run the server on")
    parser.add_argument('--origin', type=str, help="Origin server URL")
    parser.add_argument('--clear-cache', action='store_true',
                        help="Clear the cache")

    args = parser.parse_args()

    if args.clear_cache:
        clear_cache()
    elif args.port and args.origin:
        start_server(args.port, args.origin)
    else:
        print("Error: Both --port and --origin are required to start the server.")
