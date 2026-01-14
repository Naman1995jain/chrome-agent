
log_file = "agent_execution.log"
try:
    with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if any(k in line for k in ["Agent says", "Error", "Step", "Clicked", "Typed", "Navigated"]):
                print(line.strip())
except Exception as e:
    print(e)
