#!/usr/bin/env python3
"""
VSG Pinecone — Semantic memory for the Viable System Generator.

Vector database for persistent knowledge retrieval across sessions.
Uses Pinecone serverless (free tier) with llama-text-embed-v2 embeddings.

CLI subcommands:
    test        Verify API access and show index stats
    search      Semantic search across knowledge base
    upsert      Add records to the knowledge base
    stats       Show detailed index statistics
    embed-file  Embed content from a file (wins.md, pains.md, etc.)

Architecture:
    - REST API only (no SDK dependency)
    - Single index: vsg-memory (1024-dim, cosine, serverless us-east-1)
    - Pinecone inference API for embeddings (llama-text-embed-v2)
    - Namespaces: knowledge (lessons/decisions/tensions), episodes, cycles

v1.0 — Z337 (2026-02-21)
"""

import sys
import os
import json
import urllib.request
import urllib.error
import re

# --- Configuration ---

INDEX_NAME = "vsg-memory"
EMBED_MODEL = "llama-text-embed-v2"
EMBED_DIM = 1024
CONTROL_URL = "https://api.pinecone.io"
API_VERSION = "2025-04"


def load_api_key():
    """Load Pinecone API key from .env file."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(env_path):
        print("ERROR: .env file not found")
        sys.exit(1)
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                if k.strip() == "PINECONE_API_KEY":
                    return v.strip()
    print("ERROR: PINECONE_API_KEY not found in .env")
    sys.exit(1)


def get_headers(api_key):
    return {
        "Api-Key": api_key,
        "Content-Type": "application/json",
        "X-Pinecone-API-Version": API_VERSION,
    }


def api_call(method, url, headers, data=None):
    """Make an API call. Returns (status_code, response_dict)."""
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read()
            return resp.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            return e.code, json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            return e.code, {"raw": raw[:500]}
    except urllib.error.URLError as e:
        return 0, {"error": str(e)}


def get_index_host(api_key, headers):
    """Get the data plane host for the index."""
    status, info = api_call("GET", f"{CONTROL_URL}/indexes/{INDEX_NAME}", headers)
    if status == 200:
        return info.get("host", "")
    elif status == 404:
        print(f"Index '{INDEX_NAME}' not found. Run 'vsg_pinecone.py test' first.")
        sys.exit(1)
    else:
        print(f"ERROR getting index: HTTP {status}")
        print(json.dumps(info, indent=2)[:300])
        sys.exit(1)


def embed_texts(api_key, headers, texts, input_type="passage"):
    """Generate embeddings via Pinecone inference API."""
    status, result = api_call(
        "POST",
        f"{CONTROL_URL}/embed",
        headers,
        {
            "model": EMBED_MODEL,
            "inputs": [{"text": t} for t in texts],
            "parameters": {"input_type": input_type, "truncate": "END"},
        },
    )
    if status != 200:
        print(f"ERROR embedding: HTTP {status}")
        print(json.dumps(result, indent=2)[:300])
        sys.exit(1)
    return [d["values"] for d in result["data"]], result.get("usage", {})


# --- CLI Commands ---


def cmd_test(api_key, headers):
    """Test API access and show index status."""
    print("=== Pinecone API Test ===\n")

    # List indexes
    status, result = api_call("GET", f"{CONTROL_URL}/indexes", headers)
    if status != 200:
        print(f"FAILED: HTTP {status}")
        print(json.dumps(result, indent=2)[:300])
        return

    indexes = result.get("indexes", [])
    print(f"API access: OK (HTTP {status})")
    print(f"Indexes: {len(indexes)}")

    for idx in indexes:
        name = idx.get("name", "?")
        state = idx.get("status", {}).get("state", "?")
        dim = idx.get("dimension", "?")
        metric = idx.get("metric", "?")
        print(f"  - {name}: {dim}d, {metric}, state={state}")

    # Test embedding
    print("\nEmbedding test:")
    vecs, usage = embed_texts(api_key, headers, ["test"], input_type="query")
    print(f"  Model: {EMBED_MODEL}")
    print(f"  Dimension: {len(vecs[0])}")
    print(f"  Usage: {usage}")

    # Index stats if exists
    if any(idx.get("name") == INDEX_NAME for idx in indexes):
        host = get_index_host(api_key, headers)
        status, stats = api_call("GET", f"https://{host}/describe_index_stats", headers)
        if status == 200:
            print(f"\nIndex '{INDEX_NAME}' stats:")
            for ns, info in stats.get("namespaces", {}).items():
                print(f"  namespace '{ns}': {info.get('vectorCount', 0)} vectors")
            print(f"  total: {stats.get('totalVectorCount', 0)} vectors")

    print("\nAll checks passed.")


def cmd_search(api_key, headers, args):
    """Semantic search across knowledge base."""
    if not args:
        print("Usage: vsg_pinecone.py search <query> [--namespace NS] [--category CAT] [--top N]")
        return

    # Parse args
    query_parts = []
    namespace = "knowledge"
    category = None
    top_k = 5
    i = 0
    while i < len(args):
        if args[i] == "--namespace" and i + 1 < len(args):
            namespace = args[i + 1]
            i += 2
        elif args[i] == "--category" and i + 1 < len(args):
            category = args[i + 1]
            i += 2
        elif args[i] == "--top" and i + 1 < len(args):
            top_k = int(args[i + 1])
            i += 2
        else:
            query_parts.append(args[i])
            i += 1

    query = " ".join(query_parts)
    if not query:
        print("ERROR: No query provided")
        return

    host = get_index_host(api_key, headers)

    # Embed query
    vecs, usage = embed_texts(api_key, headers, [query], input_type="query")

    # Build query body
    body = {
        "vector": vecs[0],
        "topK": top_k,
        "includeMetadata": True,
        "namespace": namespace,
    }
    if category:
        body["filter"] = {"category": {"$eq": category}}

    status, result = api_call("POST", f"https://{host}/query", headers, body)
    if status != 200:
        print(f"ERROR: HTTP {status}")
        print(json.dumps(result, indent=2)[:300])
        return

    matches = result.get("matches", [])
    print(f"Query: {query}")
    print(f"Namespace: {namespace}" + (f", category={category}" if category else ""))
    print(f"Results: {len(matches)}\n")

    for m in matches:
        meta = m.get("metadata", {})
        score = m.get("score", 0)
        content = meta.get("content", "")
        cat = meta.get("category", "?")
        cycle = meta.get("cycle", "?")
        print(f"  [{score:.3f}] {m['id']} ({cycle}, {cat})")
        # Word-wrap content at 100 chars
        words = content.split()
        line = "         "
        for w in words:
            if len(line) + len(w) + 1 > 100:
                print(line)
                line = "         " + w
            else:
                line += (" " if line.strip() else "") + w
        if line.strip():
            print(line)
        print()


def cmd_upsert(api_key, headers, args):
    """Add records to the knowledge base.

    Usage:
        vsg_pinecone.py upsert --id ID --content "text" --category CAT --cycle Z123 [--namespace NS]
        vsg_pinecone.py upsert --json '{"id": "...", "content": "...", "category": "...", "cycle": "..."}'
    """
    if not args:
        print("Usage: vsg_pinecone.py upsert --id ID --content TEXT --category CAT --cycle Z123 [--namespace NS]")
        print("   or: vsg_pinecone.py upsert --json '{...}'")
        return

    namespace = "knowledge"
    record = {}

    if args[0] == "--json":
        record = json.loads(" ".join(args[1:]))
        namespace = record.pop("namespace", namespace)
    else:
        i = 0
        while i < len(args):
            if args[i] == "--id" and i + 1 < len(args):
                record["id"] = args[i + 1]
                i += 2
            elif args[i] == "--content" and i + 1 < len(args):
                record["content"] = args[i + 1]
                i += 2
            elif args[i] == "--category" and i + 1 < len(args):
                record["category"] = args[i + 1]
                i += 2
            elif args[i] == "--cycle" and i + 1 < len(args):
                record["cycle"] = args[i + 1]
                i += 2
            elif args[i] == "--namespace" and i + 1 < len(args):
                namespace = args[i + 1]
                i += 2
            else:
                i += 1

    required = ["id", "content", "category", "cycle"]
    missing = [k for k in required if k not in record]
    if missing:
        print(f"ERROR: Missing required fields: {', '.join(missing)}")
        return

    host = get_index_host(api_key, headers)

    # Embed
    vecs, usage = embed_texts(api_key, headers, [record["content"]])
    print(f"Embedded ({usage.get('total_tokens', '?')} tokens)")

    # Upsert
    status, result = api_call(
        "POST",
        f"https://{host}/vectors/upsert",
        headers,
        {
            "vectors": [
                {
                    "id": record["id"],
                    "values": vecs[0],
                    "metadata": {
                        "content": record["content"],
                        "category": record["category"],
                        "cycle": record["cycle"],
                    },
                }
            ],
            "namespace": namespace,
        },
    )

    if status == 200:
        print(f"Upserted: {record['id']} → namespace={namespace}")
    else:
        print(f"ERROR: HTTP {status}")
        print(json.dumps(result, indent=2)[:300])


def cmd_stats(api_key, headers):
    """Show detailed index statistics."""
    host = get_index_host(api_key, headers)
    status, stats = api_call("GET", f"https://{host}/describe_index_stats", headers)
    if status != 200:
        print(f"ERROR: HTTP {status}")
        return

    print(f"Index: {INDEX_NAME}")
    print(f"Dimension: {stats.get('dimension', '?')}")
    print(f"Metric: {stats.get('metric', '?')}")
    print(f"Vector type: {stats.get('vectorType', '?')}")
    print(f"Total vectors: {stats.get('totalVectorCount', 0)}")
    print(f"Fullness: {stats.get('indexFullness', 0)}")
    print("\nNamespaces:")
    for ns, info in stats.get("namespaces", {}).items():
        print(f"  '{ns}': {info.get('vectorCount', 0)} vectors")


def cmd_embed_file(api_key, headers, args):
    """Embed content from a structured file into the knowledge base.

    Usage: vsg_pinecone.py embed-file <filepath> [--namespace NS] [--category CAT] [--dry-run]

    Parses markdown files with ### headers as record boundaries.
    Each section becomes a record with id derived from the header.
    """
    if not args:
        print("Usage: vsg_pinecone.py embed-file <filepath> [--namespace NS] [--category CAT] [--dry-run]")
        return

    filepath = args[0]
    namespace = "knowledge"
    category = "unknown"
    dry_run = False

    i = 1
    while i < len(args):
        if args[i] == "--namespace" and i + 1 < len(args):
            namespace = args[i + 1]
            i += 2
        elif args[i] == "--category" and i + 1 < len(args):
            category = args[i + 1]
            i += 2
        elif args[i] == "--dry-run":
            dry_run = True
            i += 1
        else:
            i += 1

    if not os.path.exists(filepath):
        print(f"ERROR: File not found: {filepath}")
        return

    with open(filepath) as f:
        content = f.read()

    # Parse sections by ### headers
    sections = re.split(r"\n### ", content)
    records = []
    for section in sections[1:]:  # skip preamble
        lines = section.strip().split("\n")
        header = lines[0].strip()
        body = "\n".join(lines[1:]).strip()

        if not body or len(body) < 20:
            continue

        # Extract cycle reference (Z123 pattern)
        cycle_match = re.search(r"Z(\d+)", header)
        cycle = f"Z{cycle_match.group(1)}" if cycle_match else "unknown"

        # Generate id from header
        record_id = re.sub(r"[^a-z0-9]+", "-", header.lower())[:60].strip("-")

        # Truncate body for embedding (max ~2000 chars)
        embed_text = body[:2000]

        records.append({
            "id": record_id,
            "content": embed_text,
            "category": category,
            "cycle": cycle,
        })

    print(f"File: {filepath}")
    print(f"Sections found: {len(records)}")
    print(f"Namespace: {namespace}, category: {category}")

    if dry_run:
        for r in records:
            print(f"  [{r['cycle']}] {r['id']}: {r['content'][:80]}...")
        print("\n(dry run — no changes made)")
        return

    if not records:
        print("No sections to embed.")
        return

    host = get_index_host(api_key, headers)

    # Batch embed (up to 96 at a time per Pinecone limits)
    batch_size = 50
    total_tokens = 0
    total_upserted = 0

    for start in range(0, len(records), batch_size):
        batch = records[start : start + batch_size]
        texts = [r["content"] for r in batch]

        vecs, usage = embed_texts(api_key, headers, texts)
        total_tokens += usage.get("total_tokens", 0)

        vectors = []
        for j, rec in enumerate(batch):
            vectors.append({
                "id": rec["id"],
                "values": vecs[j],
                "metadata": {
                    "content": rec["content"],
                    "category": rec["category"],
                    "cycle": rec["cycle"],
                },
            })

        status, result = api_call(
            "POST",
            f"https://{host}/vectors/upsert",
            headers,
            {"vectors": vectors, "namespace": namespace},
        )

        if status == 200:
            count = result.get("upsertedCount", len(batch))
            total_upserted += count
            print(f"  Batch {start // batch_size + 1}: {count} records upserted")
        else:
            print(f"  ERROR batch {start // batch_size + 1}: HTTP {status}")
            print(json.dumps(result, indent=2)[:300])

    print(f"\nDone. {total_upserted} records upserted, {total_tokens} tokens used.")


# --- Main ---

def main():
    if len(sys.argv) < 2:
        print("VSG Pinecone — Semantic memory for the Viable System Generator")
        print()
        print("Usage: vsg_pinecone.py <command> [args]")
        print()
        print("Commands:")
        print("  test         Verify API access and show index stats")
        print("  search       Semantic search: search <query> [--namespace NS] [--category CAT] [--top N]")
        print("  upsert       Add record: upsert --id ID --content TEXT --category CAT --cycle Z123")
        print("  stats        Show index statistics")
        print("  embed-file   Embed file sections: embed-file <path> [--namespace NS] [--category CAT]")
        print()
        print(f"Index: {INDEX_NAME} | Model: {EMBED_MODEL} | Dim: {EMBED_DIM}")
        return

    api_key = load_api_key()
    headers = get_headers(api_key)
    cmd = sys.argv[1]

    if cmd == "test":
        cmd_test(api_key, headers)
    elif cmd == "search":
        cmd_search(api_key, headers, sys.argv[2:])
    elif cmd == "upsert":
        cmd_upsert(api_key, headers, sys.argv[2:])
    elif cmd == "stats":
        cmd_stats(api_key, headers)
    elif cmd == "embed-file":
        cmd_embed_file(api_key, headers, sys.argv[2:])
    else:
        print(f"Unknown command: {cmd}")
        print("Run without arguments for usage.")


if __name__ == "__main__":
    main()
