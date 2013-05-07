class MissingTokenException(Exception):
    def __init__(self, missing_token, *args, **kwargs):
        super(Exception, self).__init__(*args, **kwargs)
        self.missing_token = missing_token


class UnknownProviderException(Exception):
    pass
