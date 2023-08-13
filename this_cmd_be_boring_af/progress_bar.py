import abc


class BaseProgressBar(abc.ABC):
    text: str
    max_value: int

    def __init__(self, text: str, max_value: int):
        self.text = text
        self.max_value = max_value

    @abc.abstractmethod
    def progress(self, value: int):
        pass


class DivideProgressBar(BaseProgressBar):
    def progress(self, value: int):
        print(f"\r{self.text}: {value if value > 0 else 1}/{self.max_value}", end="")


class BlockProgressBar(BaseProgressBar):
    def progress(self, value: int):
        progress = int(50 * (value / self.max_value))
        status = '█' * progress + '-' * (50 - progress)
        percentage = int(100 * (value / self.max_value))
        print(f"\r{self.text}: |{status}| {percentage}%", end="")
