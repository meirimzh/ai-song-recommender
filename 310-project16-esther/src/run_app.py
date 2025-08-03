# run_app.py

import subprocess
import sys
python_exec = sys.executable

subprocess.run([python_exec, "src/data_processing.py"], check=True)

subprocess.run([python_exec, "src/logic.py"], check=True)

subprocess.run([python_exec, "src/app.py"], check=True)
