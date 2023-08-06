class ProgressBar:
    text: str
    max_value: int

    def __init__(self, text: str, max_value: int):
        self.text = text
        self.max_value = max_value

    def progress(self, value: int):
        print(f"\r{self.text}: {value if value > 0 else 1}/{self.max_value}", end="")
