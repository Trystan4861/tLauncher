class Sizes:
    class Message:
        HEIGHT = 27

    class CommandInput:
        HEIGHT = 80

    class Window:
        WIDTH = 800
        HEIGHT = 80
        
        @classmethod
        def HEIGHT_WITH_MESSAGE(cls):
            return cls.HEIGHT + Sizes.Message.HEIGHT
