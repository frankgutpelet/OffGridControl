class LoggerStub:
    error = ""

    def Debug(self, msg):
        pass

    def Error(self, msg):
        self.error = msg