# #!/usr/bin/env python3
# import subprocess
# from pathlib import Path
# import sys

# root = Path(__file__).resolve().parent.parent
# services_dir = root / "services"
# exit_code = 0

# subprocess.run(["uv", "sync", "--frozen"], cwd=root, check=True)

# for service in services_dir.iterdir():
#     if (service / "pyproject.toml").exists():
#         print(f"\n🧪 Testing {service.name}...")
#         result = subprocess.run(["uv", "run", "pytest", "-v"], cwd=service)

#         exit_code = exit_code or result.returncode

# sys.exit(exit_code)
