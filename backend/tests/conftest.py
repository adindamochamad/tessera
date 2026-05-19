"""Test configuration"""

import pytest
import sys
from pathlib import Path

# Tambahkan app directory ke Python path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))
