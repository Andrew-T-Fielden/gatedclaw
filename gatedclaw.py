import json
import os
import datetime
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def load_schema():
    with open("/home/andrew/demo/gatedclaw_schema.json", "r") as f:
        return json.load(f)

def fitd_check(proposed_action, schema):
    """
    Fit'd validation - checks proposed action against schema
    Returns alignment report
    """
    prompt = f"""
You are Fit'd - a governance validation system.

Your job is to check if a proposed AI action aligns with the defined schema.

SCHEMA:
{json.dumps(schema, indent=2)}

PROPOSED ACTION:
{proposed_action}

Analyse the proposed action against the schema and return a JSON response with:
{{
  "verdict": "APPROVED" or "BLOCKED" or "REVIEW",
  "alignment_score": 0.0 to 1.0,
  "fits": ["list of schema criteria this action satisfies"],
  "violations": ["list of schema criteria this action violates"],
  "review_flags": ["list of items requiring human review"],
  "summary": "one sentence explanation of verdict"
}}

Return only valid JSON, nothing else.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    return json.loads(response.choices[0].message.content)

def log_result(proposed_action, report):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if report["verdict"] == "APPROVED":
        path = f"/home/andrew/demo/outbox/approved_{timestamp}.json"
    elif report["verdict"] == "BLOCKED":
        path = f"/home/andrew/demo/rejected/blocked_{timestamp}.json"
    else:
        path = f"/home/andrew/demo/rejected/review_{timestamp}.json"
    
    output = {
        "timestamp": timestamp,
        "proposed_action": proposed_action,
        "fitd_report": report
    }
    
    with open(path, "w") as f:
        json.dump(output, f, indent=2)
    
    return path

def run_gatedclaw(proposed_action):
    print(f"\n{'='*60}")
    print("GATEDCLAW - Fit'd Validation Running")
    print(f"{'='*60}")
    print(f"Proposed action: {proposed_action[:100]}...")
    print("Checking against schema...")
    
    schema = load_schema()
    report = fitd_check(proposed_action, schema)
    log_path = log_result(proposed_action, report)
    
    print(f"\nVERDICT: {report['verdict']}")
    print(f"Alignment score: {report['alignment_score']}")
    print(f"\nFits:")
    for f in report.get("fits", []):
        print(f"  ✓ {f}")
    print(f"\nViolations:")
    for v in report.get("violations", []):
        print(f"  ✗ {v}")
    print(f"\nReview flags:")
    for r in report.get("review_flags", []):
        print(f"  ⚑ {r}")
    print(f"\nSummary: {report['summary']}")
    print(f"\nReport saved to: {log_path}")
    print(f"{'='*60}\n")
    
    return report

if __name__ == "__main__":
    # Test with OpenClaw's proposed actions from team_update.txt
    test_actions = [
        "Draft and send a request for compliance sign-off to the compliance team, emphasizing urgency",
        "Schedule a team review meeting for Friday and send calendar invites to all team members",
        "Respond to all team members and copy the board on project status",
        "Update the stakeholder report with current project status"
    ]
    
    for action in test_actions:
        report = run_gatedclaw(action)
        input("\nPress Enter for next action...")

