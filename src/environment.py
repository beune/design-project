class Environment(object):
    @staticmethod
    def get_NLP() -> NLP:
        return NotImplemented

    @staticmethod
    def get_structure() -> structure:
        return NotImplemented

    @staticmethod
    def get_hinter() -> hinter:
        return NotImplemented


    # Optie 1
    @staticmethod
    def process():
        return NotImplemented

    # MammoEnvironment
    @staticmethod
    def process(self, text):
        shreyasi_wrapper.process(text)

    # Optie 2
    # environment.nlp.process
    # mammo = Environment(shreyasi, ...)
    # tumor = Environment(nlp, ...)
    # tumor.process(text)

    def process(self, text):
        return self.nlp.process(text)

    # Hinter
    #     method 1
    #     method 2
