class MissingTokenException(Exception):
    def __init__(self, missing_token, provider, *args, **kwargs):
        super(Exception, self).__init__(*args, **kwargs)
        self.missing_token = missing_token
        self.provider = provider
