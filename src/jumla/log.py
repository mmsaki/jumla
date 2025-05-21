import time
from colorama import Fore, Style


class Logger:
    def __init__(self):
        self.start_time = time.time()

    def info(self, msg: str):
        print(f"{Fore.BLUE}{msg}{Style.RESET_ALL}")

    def success(self, msg: str):
        print(f"{Fore.GREEN}{msg}{Style.BRIGHT}")

    def warn(self, msg: str):
        print(f"⚠️  {Fore.YELLOW}{msg}{Style.RESET_ALL}")

    def error(self, msg: str):
        print(f"{Fore.RED}{msg}{Style.RESET_ALL}")

    def bullet(self, msg: str):
        print(f"  • {msg}")

    def step(self, msg: str):
        print(f"→  {msg}")

    def finish(self, msg="Done"):
        elapsed = time.time() - self.start_time
        print(f"{Fore.GREEN}{msg} in {elapsed:.2f}s")


logger = Logger()
