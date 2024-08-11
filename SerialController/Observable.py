class Observable:
    def __init__(self):
        self.Observers = []

    def Subscribe(self, observer):
        self.Observers.append(observer)

    def NotifyObservers(self):
        for observer in self.Observers:
            observer()
