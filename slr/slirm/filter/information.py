import logging


class CountEntries(object):

    def __init__(self, source_pipe, message="Found [%d] entries."):
        self.source_pipe = source_pipe
        self.message = message

    def pull(self):
        database = self.source_pipe.pull()
        logging.info(self.message, len(database.get_entry_list()))
        return database
