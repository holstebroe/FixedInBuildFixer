import re


class ChangeCommentParser:
    def __init__(self, comment):
        self.comment = comment
        self.merge_reference = None
        self.fixed_references = None
        self.parse_youtrack_reference(comment)

    def parse_youtrack_reference(self, comment):
        # Parse GitHub merge reference comment
        m = re.search('Merge pull request #\d+ from \w+/(\w+-\d+)', comment, re.MULTILINE)
        if m is not None:
            self.merge_reference = m.group(1)

        # Parse youtrack fixed reference
        m = re.search('#?(\w+-\d+)\s+#?fixed', comment, re.MULTILINE)
        if m is not None:
            self.fixed_references = m.groups()
