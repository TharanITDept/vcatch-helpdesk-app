import sys
import re
import os

if len(sys.argv) < 2:
    print("Usage: python3 print_errors.py <log_file>")
    sys.exit(1)

log_file = sys.argv[1]
try:
    with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
except Exception as e:
    print(f"Error reading log file {log_file}: {e}")
    sys.exit(1)

# Strip ANSI escape codes
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
clean_content = ansi_escape.sub('', content)

lines = clean_content.splitlines()
print(f"=== TOTAL LOG LINES: {len(lines)} ===")

# Collect errors for step summary
summary_lines = []
error_found = False

for idx, line in enumerate(lines):
    # Match typical compiler errors
    if "error:" in line.lower() or "failed" in line.lower() or "error" in line.lower():
        error_msg = f"--- Line {idx+1}: {line}"
        print(error_msg)
        summary_lines.append(f"**Line {idx+1}**: `{line}`")
        
        # Print and capture context
        context = []
        for j in range(1, 9):
            if idx + j < len(lines):
                print(f"    {lines[idx+j]}")
                context.append(f"&nbsp;&nbsp;&nbsp;&nbsp;{lines[idx+j]}")
        error_found = True
        print("-" * 60)
        
        summary_lines.append("```\n" + "\n".join([lines[idx+j] for j in range(1, 9) if idx + j < len(lines)]) + "\n```\n")

summary_file = os.environ.get('GITHUB_STEP_SUMMARY')
if summary_file:
    try:
        with open(summary_file, 'a', encoding='utf-8') as sf:
            sf.write(f"## ❌ build-ios Compiler Error Output for `{os.path.basename(log_file)}`\n")
            if error_found:
                sf.write("\n".join(summary_lines))
            else:
                sf.write("No compiler errors detected directly. See log tail below:\n")
                sf.write("### First 50 lines:\n```\n" + "\n".join(lines[:50]) + "\n```\n")
                sf.write("### Last 50 lines:\n```\n" + "\n".join(lines[-50:]) + "\n```\n")
    except Exception as e:
        print(f"Error writing to GITHUB_STEP_SUMMARY: {e}")

if not error_found:
    print("No lines containing 'error', 'failed' found.")
    print("=== FIRST 100 LINES OF LOG ===")
    for line in lines[:100]:
        print(line)
    print("=== LAST 100 LINES OF LOG ===")
    for line in lines[-100:]:
        print(line)
