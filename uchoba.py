class Dog:
    def __init__(self, name: str) -> None:
        self.name = name

    def bark(self):
        self.name = "ИЗМЕНЕНО"
        return self.name


c = Dog("Barsik")
print(c.bark())
print(c.name)
