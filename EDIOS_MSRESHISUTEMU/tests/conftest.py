# conftest.py - pytest fixtures for Flask app (generated)
"""Pytest configuration and fixtures. Provides app and client for tests."""
import os
import sys

import pytest

# Ensure project root is on path when running tests
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

os.environ.setdefault("FLASK_ENV", "testing")


@pytest.fixture
def app():
    """Create application for testing."""
    from run import app as flask_app
    flask_app.config["TESTING"] = True
    return flask_app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()
