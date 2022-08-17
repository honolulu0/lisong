import re


def find_middle_all(text, begin, end):
    return re.findall(fr'{begin}(.+?){end}', text)


class StringUtil:
    pass
