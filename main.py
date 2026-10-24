#!/usr/bin/env python3
import sys
import argparse
from http.server import HTTPServer
from core.api import DetectiveHandler

def main():
    parser = argparse.ArgumentParser(description="Solana Syndicate Detective — Movie Crime Board Console")
    parser.add_argument("--port", type=int, default=8920, help="Port to bind (default: 8920)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host interface (default: 0.0.0.0)")
    args = parser.parse_args()

    server_address = (args.host, args.port)
    httpd = HTTPServer(server_address, DetectiveHandler)
    
    print("=" * 70)
    print("  🕵️ SOLANA SYNDICATE DETECTIVE — CRIME BOARD CONSOLE")
    print("=" * 70)
    print(f"[*] Port: {args.port}")
    print(f"[*] Local UI: http://localhost:{args.port}")
    print(f"[*] Cloud Integrations: GitHub + Supabase + Vercel")
    print(f"[*] Active Crime Syndicates: Frankfurt Ghosts, Cluster Alpha (Ben), Vilnius")
    print("=" * 70)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Closing investigation console...")
        httpd.server_close()
        sys.exit(0)

if __name__ == "__main__":
    main()
