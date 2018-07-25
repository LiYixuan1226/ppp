from bibtexparser.bibdatabase import BibDatabase

import msvcrt


class InteractiveFilter(object):
    """
    A simple interactive user interface for reviewing and deciding on retrieved papers.
    When using on a Windows Command Prompt, type the commands

    > chcp 65001
    > set PYTHONIOENCODING=utf-8

    before executing your protocol script to avoid encoding problems when printing output.

    """

    def __init__(self, source_pipe, user_interface, included_keys_file, excluded_keys_file):
        self.source_pipe = source_pipe
        self.user_interface = user_interface

        self.included_keys_file = included_keys_file
        self.excluded_keys_file = excluded_keys_file

    def pull(self):
        database = self.source_pipe.pull()
        result = BibDatabase()

        for entry in database.get_entry_list():
            if 'ID' in entry:
                entry_key = entry['ID']

                user_response = str(self.user_interface.prompt_user(entry), 'utf-8')
                if user_response == 'i':
                    self.included_keys_file.write(entry_key + "\n")
                    result.get_entry_list().append(entry)
                elif user_response == 'e':
                    self.excluded_keys_file.write(entry_key + "\n")
                elif user_response == 'q':
                    break
                else:
                    result.get_entry_list().append(entry)

        return result


class CIUserInterface(object):

    def __init__(self):
        pass

    def prompt_user(self, entry):
        message = \
            """
Should the following entry be included in the systematic literature review Include(i)/Exclude(e)/Defer(d)/Quit(q)?

  {author}, {year}, {title}.
  {publication}

  Abstract: {abstract}

  URL: {url}

  Keywords: {keywords}

Response:"""

        values = {
            'author': entry.get('author', ""),
            'title': entry.get('title', ""),
            'year': entry.get('year', ""),
            'publication': entry.get('journal', entry.get('booktitle', "")),
            'abstract': entry.get('abstract', ""),
            'url': entry.get('url', ""),
            'keywords': entry.get('keywords', ""),
        }

        print(message.format(**values), end='')
        ch = msvcrt.getche()
        print()
        return ch


