from pathlib import Path
import sys


TESTS_ROOT_PATH = Path(__file__).parent
BASE_PATH = TESTS_ROOT_PATH.parent


sys.path.append(BASE_PATH)
