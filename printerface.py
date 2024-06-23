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

    def gohome(self):
        pass
