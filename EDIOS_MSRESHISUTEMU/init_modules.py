import subprocess
import sys
import os
import logging

logger = logging.getLogger(__name__)

# Single source of truth: use requirements.txt so dependencies stay in sync with the project.
_REQUIREMENTS = "requirements.txt"

def _ensure_deps():
    if not os.path.isfile(_REQUIREMENTS):
        logger.warning("%s not found, skipping dependency install.", _REQUIREMENTS)
        return
    logger.info("Installing dependencies from requirements.txt...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", _REQUIREMENTS, "--no-cache-dir", "--timeout", "60"],
            check=True,
        )
        logger.info("Dependencies OK.")
    except subprocess.CalledProcessError as e:
        logger.exception("Error installing dependencies")
        raise
    except Exception as e:
        logger.exception("Unexpected error while installing dependencies")
        raise

if __name__ == "__main__":
    _ensure_deps()
    logger.info("run.py Starting...")
    try:
        subprocess.run([sys.executable, "run.py"], check=True)
    except subprocess.CalledProcessError as e:
        logger.error("run.py exited with code %s", e.returncode)
        sys.exit(e.returncode)
    logger.info("run.py Finished...")
