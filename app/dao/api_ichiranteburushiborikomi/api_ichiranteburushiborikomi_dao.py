class ApiIchiranteburushiborikomiDao:
    def api_ichiranteburushiborikomi(self, dtoObj=None):
        return []
    def __getattr__(self, name):
        def _missing(*args, **kwargs):
            return []
        return _missing
