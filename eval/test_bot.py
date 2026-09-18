"""
Lightweight evaluation harness for the CloudCart agent.

Not a unit test suite - it hits the real deployed endpoint and checks that
responses contain expected keywords. This is the kind of smoke-test harness
used to catch regressions when you change the system prompt, swap models, or
add tools: run it after every deploy and see if the agent still behaves.

Usage:
    python eval/test_bot.py https://YOUR-ENDPOINT/chat
"""

import sys
import json
import urllib.request

TEST_CASES = [
    {
        "name": "Order status lookup (tool use)",
        "message": "What's the status of order ORD-1001?",
        "expect_any": ["shipped", "Shipped"]
    },
    {
        "name": "Unknown order (tool use, graceful failure)",
        "message": "What's the status of order ORD-9999?",
        "expect_any": ["no order", "not found", "couldn't find", "doesn't exist"]
    },
    {
        "name": "Knowledge base lookup (RAG)",
        "message": "What is CloudCart's return policy?",
        "expect_any": ["30 days", "return"]
    },
    {
        "name": "Knowledge base lookup - warranty",
        "message": "Does CloudCart offer a warranty on electronics?",
        "expect_any": ["warranty", "1-year", "1 year"]
    },
    {
        "name": "Plain conversation (no tool needed)",
        "message": "Hi, who are you?",
        "expect_any": ["CloudCart", "assistant", "help"]
    },
]


def call_bot(endpoint, session_id, message):
    req = urllib.request.Request(
        endpoint,
        data=json.dumps({"session_id": session_id, "message": message}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def main():
    if len(sys.argv) < 2:
        print("Usage: python eval/test_bot.py https://YOUR-ENDPOINT/chat")
        sys.exit(1)

    endpoint = sys.argv[1]
    passed = 0
    failed = 0

    for i, case in enumerate(TEST_CASES):
        session_id = f"eval-{i}"
        try:
            result = call_bot(endpoint, session_id, case["message"])
            reply = result.get("reply", "")
            ok = any(kw.lower() in reply.lower() for kw in case["expect_any"])

            status = "PASS" if ok else "FAIL"
            if ok:
                passed += 1
            else:
                failed += 1

            print(f"[{status}] {case['name']}")
            print(f"       Q: {case['message']}")
            print(f"       A: {reply[:150]}")
            print()

        except Exception as e:
            failed += 1
            print(f"[ERROR] {case['name']}: {e}\n")

    print(f"Results: {passed} passed, {failed} failed out of {len(TEST_CASES)}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
