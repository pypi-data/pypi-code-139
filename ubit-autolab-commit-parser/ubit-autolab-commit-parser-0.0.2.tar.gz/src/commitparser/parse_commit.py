"""
A function that reads a commit message, and returns info about the message
measage: "submit ~My assignment name~ file1.py file2.py ..."
"""


def parse_commit(commit):
    """A function parses a commit message"""
    if not commit.startswith('submit '):
        return False
    assignment = commit[commit.find('~')+1:commit.rfind('~')]
    files = [file for file in commit[commit.rfind('~')+1:].split(' ') if file]
    return assignment, files
