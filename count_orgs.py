"""
Builds url like (initially):
`https://repository.library.brown.edu/api/search/?q=-rel_is_part_of_ssim:*+rel_is_member_of_collection_ssim:%22bdr:wum3gm43%22&fl=pid,identifier,primary_title&rows=100&start=0`
...which returns all org-items (100 at a time) given collection, as the `start` param is continually incremented.
"""

import json, pprint, sys
import requests


def prep_org_count():
    """ Prepares count of all orgs in collection.
        Called by dundermain. """
    ( base_url, q_param, fl_param, rows_param, start_param, all_docs ) = initialize_vars()
    static_url_part = f'{base_url}?q={q_param}&fl={fl_param}&rows={rows_param}'
    while True:
        ## build url ----------------------------------------------------
        built_url = f'{static_url_part}&start={start_param}'  # it's the start param that'll be updated in the while-loop
        ## retrieve data ------------------------------------------------
        rsp: requests.models.Response = requests.get( built_url )
        data: dict = rsp.json()
        ## add retrieved docs to all_docs -------------------------------
        docs: list = data['response']['docs']
        all_docs.extend( docs )  
        ## check if all docs have been retrieved ------------------------
        num_found = data['response']['numFound']
        start_param += rows_param
        if start_param >= num_found:
            break
    ## prep output --------------------------------------------------
    output: dict = { 'num_orgs': len(all_docs) }
    jsn = json.dumps( output )
    print( jsn )

def initialize_vars():
    base_url = 'https://repository.library.brown.edu/api/search/'
    q_param = '-rel_is_part_of_ssim:*+rel_is_member_of_collection_ssim:"bdr:wum3gm43"'
    fl_param = 'pid,identifier,primary_title'
    rows_param = 100
    start_param = 0  # this is the param that'll be updated in the while-loop
    all_docs = []
    return (base_url, q_param, fl_param, rows_param, start_param, all_docs)

## call function from dundermain ------------------------------------
if __name__ == '__main__':
    prep_org_count()
