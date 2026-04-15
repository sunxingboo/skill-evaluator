#!/usr/bin/env python3
"""Qianfan API chat client for skill-evaluator.

Calls Baidu Qianfan LLM platform (OpenAI-compatible v2 API).
Supports single-model, batch-parallel, and per-model-prompt modes. Zero external dependencies.

Usage:
  # Single model (stdout = plain text)
  python qianfan_chat.py --model ernie-5.0 --prompt "Hello"
  python qianfan_chat.py --model ernie-5.0 --prompt-file /tmp/prompt.txt

  # Batch parallel, shared prompt (stdout = JSON)
  python qianfan_chat.py --models ernie-5.0,deepseek-v3.2 --prompt "Hello"
  python qianfan_chat.py --models ernie-5.0,deepseek-v3.2 --prompt-file /tmp/prompt.txt

  # Batch parallel, per-model prompts (stdout = JSON)
  python qianfan_chat.py --prompt-files ernie-5.0:/tmp/p1.txt,deepseek-v3.2:/tmp/p2.txt

Environment:
  QIANFAN_BEARER_TOKEN  Bearer token for authentication (bce-v3/... format)
"""

import argparse
import json
import os
import sys
import threading
import urllib.error
import urllib.request

DEFAULT_ENDPOINT = "https://qianfan.baidubce.com/v2/chat/completions"
DEFAULT_TIMEOUT = 120


def call_model(endpoint, token, model, prompt, timeout):
    """Call a single model via Qianfan API. Returns (content, None) or (None, error_msg)."""
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")

    req = urllib.request.Request(
        endpoint,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        content = data["choices"][0]["message"]["content"]
        return content, None
    except urllib.error.HTTPError as e:
        err_body = ""
        try:
            err_body = e.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        return None, f"HTTP {e.code}: {err_body[:500]}"
    except urllib.error.URLError as e:
        return None, f"URL error: {e.reason}"
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        return None, f"Response parse error: {e}"
    except TimeoutError:
        return None, f"Timeout after {timeout}s"
    except Exception as e:
        return None, str(e)


def call_model_with_retry(endpoint, token, model, prompt, timeout, retries):
    """Call a single model with optional retries."""
    content, error = call_model(endpoint, token, model, prompt, timeout)
    if error and retries > 0:
        content, error = call_model(endpoint, token, model, prompt, timeout)
    return content, error


def batch_call(endpoint, token, model_prompts, timeout, retries):
    """Call multiple models in parallel. model_prompts is dict[model] -> prompt.
    Returns dict[model] -> {status, content/error}."""
    results = {}
    lock = threading.Lock()

    def worker(model, prompt):
        content, error = call_model_with_retry(endpoint, token, model, prompt, timeout, retries)
        with lock:
            if error:
                results[model] = {"status": "error", "error": error}
            else:
                results[model] = {"status": "ok", "content": content}

    threads = [
        threading.Thread(target=worker, args=(m, p), daemon=True)
        for m, p in model_prompts.items()
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=timeout + 10)

    for model in model_prompts:
        if model not in results:
            results[model] = {"status": "error", "error": "Thread did not complete"}

    return results


def parse_prompt_files(value):
    """Parse --prompt-files value like 'model1:/path1,model2:/path2'.
    Returns dict[model] -> prompt_text."""
    model_prompts = {}
    for entry in value.split(","):
        entry = entry.strip()
        if not entry:
            continue
        colon_idx = entry.find(":")
        if colon_idx <= 0:
            print(f"Error: Invalid --prompt-files entry (expected model:/path): {entry}", file=sys.stderr)
            sys.exit(1)
        model = entry[:colon_idx].strip()
        path = entry[colon_idx + 1:].strip()
        try:
            with open(path, "r", encoding="utf-8") as f:
                model_prompts[model] = f.read()
        except FileNotFoundError:
            print(f"Error: Prompt file not found for model {model}: {path}", file=sys.stderr)
            sys.exit(1)
    if not model_prompts:
        print("Error: No valid entries in --prompt-files.", file=sys.stderr)
        sys.exit(1)
    return model_prompts


def main():
    parser = argparse.ArgumentParser(description="Qianfan API chat client")

    model_group = parser.add_mutually_exclusive_group(required=True)
    model_group.add_argument("--model", help="Single model ID")
    model_group.add_argument("--models", help="Comma-separated model IDs for batch parallel (shared prompt)")
    model_group.add_argument("--prompt-files",
                             help="Per-model prompt files: model1:/path1,model2:/path2 (batch parallel, each model uses its own prompt)")

    prompt_group = parser.add_mutually_exclusive_group()
    prompt_group.add_argument("--prompt", help="Prompt text")
    prompt_group.add_argument("--prompt-file", help="Path to file containing prompt")

    parser.add_argument("--token", help="Bearer token (default: QIANFAN_BEARER_TOKEN env)")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT, help="API endpoint URL")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Request timeout in seconds")
    parser.add_argument("--retry", type=int, default=0, help="Number of retries for failed requests (default: 0)")

    args = parser.parse_args()

    token = args.token or os.environ.get("QIANFAN_BEARER_TOKEN")
    if not token:
        print("Error: No token provided. Set QIANFAN_BEARER_TOKEN or use --token.", file=sys.stderr)
        sys.exit(1)

    # --prompt-files mode: each model has its own prompt file
    if args.prompt_files:
        if args.prompt or args.prompt_file:
            print("Error: --prompt-files cannot be used with --prompt or --prompt-file.", file=sys.stderr)
            sys.exit(1)
        model_prompts = parse_prompt_files(args.prompt_files)
        results = batch_call(args.endpoint, token, model_prompts, args.timeout, args.retry)
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    # --model / --models mode: require a shared prompt
    if not args.prompt and not args.prompt_file:
        print("Error: --prompt or --prompt-file is required when using --model or --models.", file=sys.stderr)
        sys.exit(1)

    if args.prompt_file:
        try:
            with open(args.prompt_file, "r", encoding="utf-8") as f:
                prompt = f.read()
        except FileNotFoundError:
            print(f"Error: Prompt file not found: {args.prompt_file}", file=sys.stderr)
            sys.exit(1)
    else:
        prompt = args.prompt

    if not prompt.strip():
        print("Error: Prompt is empty.", file=sys.stderr)
        sys.exit(1)

    if args.model:
        content, error = call_model_with_retry(args.endpoint, token, args.model, prompt, args.timeout, args.retry)
        if error:
            print(f"Error [{args.model}]: {error}", file=sys.stderr)
            sys.exit(1)
        print(content)
    else:
        models = [m.strip() for m in args.models.split(",") if m.strip()]
        if not models:
            print("Error: No models specified.", file=sys.stderr)
            sys.exit(1)
        model_prompts = {m: prompt for m in models}
        results = batch_call(args.endpoint, token, model_prompts, args.timeout, args.retry)
        print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
