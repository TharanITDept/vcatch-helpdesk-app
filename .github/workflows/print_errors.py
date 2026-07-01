import sys
import re

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

error_found = False
for idx, line in enumerate(lines):
    # Match typical compiler errors
    if "error:" in line.lower() or "failed" in line.lower() or "error" in line.lower():
        print(f"--- Line {idx+1}: {line}")
        # Print 8 lines of context
        for j in range(1, 9):
            if idx + j < len(lines):
                print(f"    {lines[idx+j]}")
        error_found = True
        print("-" * 60)

if not error_found:
    print("No lines containing 'error', 'failed' found.")
    print("=== FIRST 100 LINES OF LOG ===")
    for line in lines[:100]:
        print(line)
    print("=== LAST 100 LINES OF LOG ===")
    for line in lines[-100:]:
        print(line)
