import ecs


class compA:
    def __init__(self):
        self.a = -1
        self.b = 1

class compB:
    def __init__(self):
        self.t = True
        self.f = False

class compC:
    def __init__(self):
        self.l = 'left'
        self.r = 'right'

class sysA(ecs.SystemTemplate):
    def __init__(self):
        super().__init__()

    def process(self):
        pass

class sysB(ecs.SystemTemplate)
    def __init__(self):
        super().__init__()

    def process(self):
        pass

class sysC(ecs.SystemTemplate)
    def __init__(self):
        super().__init__()

    def process(self):
        pass
