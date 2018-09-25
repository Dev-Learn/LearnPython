class English:
    def greeting(self):
        print("Hello")


class French:
    def greeting(self):
        print("Bonjour")


def intro(language):
    language.greeting()


flora = English()
aalase = French()

intro(flora)
intro(aalase)