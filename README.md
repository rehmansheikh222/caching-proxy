# Simple Caching Proxy Server

This project implements a simple caching proxy server that forwards HTTP GET requests to an origin server, caches the responses for a specified time (TTL), and serves cached responses to improve performance.

This is a solution for the [Caching Server Project](https://roadmap.sh/projects/caching-server) on roadmap.sh.

---

## Features

- **Caching of HTTP Responses**  
  - Utilizes a TTL-based in-memory cache to store previously fetched responses.
  - Returns `X-Cache: MISS` when fetching from the origin server and caching the response.
  - Returns `X-Cache: HIT` when serving from the cache.

- **Clearing Cache**  
  - Allows you to clear the entire cache via a command-line argument.

---

## Requirements

- **Python 3.8+**
- Dependencies are listed in `requirements.txt`.

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/rehmansheikh222/caching-proxy.git
   cd https://github.com/rehmansheikh222/caching-proxy.git
2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt

---

## Usage

1. **Start the Proxy Server**:
        python server.py --port <port-number> --origin <origin-url>
    --port: The port on which the proxy server will run.
    --origin: The origin server URL to forward requests to.

    Example:

        python server.py --port 3000 --origin http://dummyjson.com
    This will start the server at http://localhost:3000, forwarding requests to http://dummyjson.com.

2. **Making Requests**:
    Send HTTP GET requests to the proxy server:

    Example:

        curl -i http://localhost:3000/products
    On First Request: The response is fetched from the origin and cached (X-Cache: MISS).
    On Subsequent Requests: The cached response is returned (X-Cache: HIT).

3. **Clearing the cache**
    To clear the cache, run:

    ```bash
    python server.py --clear-cache
