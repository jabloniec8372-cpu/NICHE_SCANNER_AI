from connectors.connector_manager import search_all_sources


def scan_keyword(keyword, selected_platforms=None):
    return search_all_sources(keyword, selected_platforms=selected_platforms)
