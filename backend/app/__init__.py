# FastAPI app package
import sys
from pathlib import Path

# Make sure required directories exist
routes_dir = Path(__file__).parent / "routes"
routes_dir.mkdir(exist_ok=True)

# Create empty __init__.py files in the routes directory if they don't exist
init_file = routes_dir / "__init__.py"
if not init_file.exists():
    with open(init_file, "w") as f:
        f.write("# Routes package\n")

# Make sure the routes directory is in the Python path
sys.path.append(str(Path(__file__).parent.parent))