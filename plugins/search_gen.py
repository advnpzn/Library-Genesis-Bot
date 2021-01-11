from libgen_api import LibgenSearch

def search(text):
    result00 = LibgenSearch().search_title(text)
    return result00
