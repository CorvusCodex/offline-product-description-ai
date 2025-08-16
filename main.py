#!/usr/bin/env python3
"""
Product Description Optimizer (offline)
Usage:
  python main.py --file product.txt
  python main.py --input "Short product text..."
"""
import argparse, requests, os, sys, textwrap

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL = "llama3.2:4b"
TIMEOUT = 180

def run_llama(prompt):
    r = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "stream": False}, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json().get("response","").strip()

def build_prompt(orig):
    return (
        "You are an e-commerce copywriter.\n"
        "Rewrite the product description to be more persuasive and SEO-friendly.\n"
        "Output format:\n- Headline (short)\n- 3 benefit bullets\n- 2-sentence description\n- 120-160 char meta description\n\n"
        f"Original:\n{orig}"
    )

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", "-i")
    p.add_argument("--file", "-f")
    args = p.parse_args()
    content = args.input or ""
    if args.f:
        try:
            with open(args.f, "r", encoding="utf-8") as fh:
                content += ("\n" if content else "") + fh.read()
        except Exception as e:
            print("Error:", e, file=sys.stderr); sys.exit(1)
    if not content.strip():
        print("Provide --input or --file", file=sys.stderr); sys.exit(1)
    print(run_llama(build_prompt(content)))

if __name__ == "__main__":
    main()
