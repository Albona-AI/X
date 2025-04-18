
import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scheduler import start_scheduler


def main():
    load_dotenv(dotenv_path="./config/.env")
    start_scheduler()


if __name__ == "__main__":
    main()
