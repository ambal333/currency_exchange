import re
def search_currencies(expression):
    pattern = r"^[/]{1}[currencies]+[/]{1}[A-Z]+"
    res = re.search(pattern, expression)
    if res is None:
        return res
    else:
        return res.group()
def extract_code(expression):
    pattern = r"[A-Z]+"
    res = re.search(pattern, expression)
    if res is None:
        return res
    else:
        return res.group()