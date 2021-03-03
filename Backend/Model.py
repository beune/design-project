from Backend.DBConnector import DBConnector


class Model:

    def __init__(self):
        self.text = ""
        self.environment = []
        self.envs = {}
        self.DBConnector = DBConnector()

    def switch_env(self, new_env):
        if self.envs[new_env] is not None:
            self.environment = self.envs[new_env]
        else:
            pass
            # TODO THROW ERROR
