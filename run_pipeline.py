import subprocess
import sys

steps = [
    "pull_multi.py",
    "load_all_to_sqlite.py",
    "phase1_analysis.py",
    "phase2_analysis.py",
]

for step in steps:
    print(f"\n{'='*50}\nRunning {step}\n{'='*50}")
    result = subprocess.run([sys.executable, step])
    if result.returncode != 0:
        print(f"FAILED at {step}, stopping pipeline.")
        sys.exit(1)

print("\nPipeline complete — fresh pull through full analysis, zero manual steps.")