class CachingRetriever(object):
    def __init__(self, source_pipe):
        self.source_pipe = source_pipe
        self.cached_result = None

    def pull(self):
        if self.cached_result is None:
            self.cached_result = self.source_pipe.pull()
        return self.cached_result




