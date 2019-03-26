class UpdaterException(Exception):
    def __init__(self, error_word):
        self.error_word = error_word