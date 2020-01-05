import json

class fuzzConf:
    name = "default"
    input = ".\\input"
    retry = 1
    binaries = []
    executable = None
    regsToDelete = []
    filesToDelete = []
    windowToInteract = None
    windowToInteractKey = None
    logNullCrashes = False
    restartWhenException = False
    restartWhenLoop = False
    maxWait = 90
    logging = [
        {
            "type": "filesystem",
            "dir": ".\\Crashes"
        }
    ]
    mutators = [
        {
            "type": "bitflip",
            "rate": 40000
        },
        {
            "type": "special",
            "rate": 60000
        }
    ]


    def __init__(self, confFile):
        data = json.load(open(confFile, "rb"))
        self.initializeValues(data)

    def checkConfFields(self, data):
        if "executable" not in data:
            raise Exception("No 'executable' field")

    def initializeValues(self, data):
        self.checkConfFields(data)
        for field in ["name", "input", "retry", "executable", "binaries", "logNullCrashes", "regsToDelete", "filesToDelete", "logging", "mutators", "restartWhenException", "restartWhenLoop", "windowToInteract", "windowToInteractKey", "maxWait"]:
            if field in data:
                setattr(self, field, data[field])
        self.fixConfFields()

    def fixConfFields(self):
        if len(self.logging) == 0:
            raise Exception("No logging configured")

        while self.input[-1] in ["\\", "/"]:
            self.input = self.input[0:-1]






