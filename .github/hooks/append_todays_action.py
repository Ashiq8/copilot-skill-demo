import json
import sys

if __name__ == "__main__":
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        print(json.dumps({"decision": "continue"}))
        sys.exit(0)

    prompt = data.get("prompt", "") if isinstance(data, dict) else ""
    if not isinstance(prompt, str):
        print(json.dumps({"decision": "continue"}))
        sys.exit(0)

    trigger_phrases = [
        "roadmap",
        "study plan",
        "project recommendation",
        "project recommendations",
        "interview preparation",
        "interview prep",
        "career guidance",
        "learning plan",
        "study plan",
        "job preparation",
        "resume review"
    ]

    prompt_lower = prompt.lower()
    should_append = any(phrase in prompt_lower for phrase in trigger_phrases)

    if should_append:
        print(json.dumps({
            "decision": "continue",
            "systemMessage": "Append the following section to the response if you are generating a learning roadmap, study plan, project recommendation, or interview preparation advice:\n\n📌 Today's Action\n- One thing to do today\n- One thing to practice\n- One next milestone\n\nKeep it short and actionable.",
            "continue": true
        }))
    else:
        print(json.dumps({"decision": "continue"}))
