import json
import sys

if __name__ == "__main__":
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        print(json.dumps({"decision": "continue"}))
        sys.exit(0)

    # Extract tool information from hook data
    tool_name = data.get("toolName", "").lower() if isinstance(data, dict) else ""
    prompt = data.get("prompt", "") if isinstance(data, dict) else ""
    
    if not isinstance(prompt, str):
        prompt = ""
    
    prompt_lower = prompt.lower()

    # Analysis tools that indicate code review or repository analysis is happening
    analysis_tools = [
        "semantic_search",
        "grep_search",
        "read_file",
        "file_search",
        "vscode_listCodeUsages",
        "get_errors",
        "list_dir",
        "vscode_renameSymbol"
    ]

    # Context keywords that indicate this is a review/analysis request
    trigger_phrases = [
        "repository",
        "repo",
        "code review",
        "project review",
        "architecture",
        "assessment",
        "improvement",
        "refactor",
        "optimization",
        "analysis",
        "codebase",
        "project structure",
        "technical debt",
        "design",
        "best practice"
    ]

    # Check if we're in a repository analysis context
    is_analysis_tool = tool_name in analysis_tools
    has_context_keyword = any(phrase in prompt_lower for phrase in trigger_phrases)

    if is_analysis_tool and has_context_keyword:
        print(json.dumps({
            "decision": "continue",
            "systemMessage": """After providing your main analysis, response, or review, append the following sections to offer actionable next steps:

📌 Suggested GitHub Issues
- Generate 3 practical GitHub issues based on the project analysis
- Format: "Issue Title - Brief description (Priority: High/Medium/Low)"
- Make each issue specific and actionable (not generic)

📌 Priority Improvements
- Identify the single most important improvement to tackle first
- Explain why this should be prioritized
- Be specific to this project's context

📌 Next Development Milestone
- Suggest the next logical feature or enhancement
- Explain how it fits into the project roadmap
- Keep recommendations concrete and project-specific

IMPORTANT:
- Keep the summary concise (under 200 words total)
- Avoid repeating information from your main response
- Base recommendations on actual project context, not generic advice
- Use bullet points for clarity""",
            "continue": True
        }))
    else:
        print(json.dumps({"decision": "continue"}))
