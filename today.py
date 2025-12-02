# get today's date
from datetime import date
import os
today = date.today()
# run the corresponding script
script_name = f"{today.year}_{today.day:02}.py"
os.system(f"uv run {script_name}")