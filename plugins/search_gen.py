from libgen_api import LibgenSearch

def search(text):
    result00 = LibgenSearch().search_title_filtered(text)
    return result00
