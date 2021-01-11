from libgen_api import LibgenSearch

def search(text,f):
    result00 = LibgenSearch().search_title_filtered(text,f)
    return result00