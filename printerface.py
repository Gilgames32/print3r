"""
two little interfaces used for the dependency injection
"""

class IHub:
    def busy(self):
        pass

    def waiting(self):
        pass

    def wait_no_presses(self):
        pass

    def choice(self):
        pass

    def title(self, text):
        pass

    def text(self, text, x, y, clear_screen):
        pass


class IPen:
    def activecolor(self, hexa):
        pass

    def up(self):
        pass

    def down(self):
        pass

    def initialize(self):
        pass

    def dotcoord(self, x, y):
        pass

    def line(self, x1, y1, x2, y2):
        pass

    def gohome(self):
        pass

    def empty(self):
        pass

    def adjust(self):
        pass
