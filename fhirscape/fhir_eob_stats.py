#!/usr/bin/env python
__author__ = 'Alan Viars @aviars'
import requests
import sys
import json
from collections import OrderedDict
import requests
import time

from six import iteritems

        

def nested_lookup(key, document, wild=False):
    """Lookup a key in a nested document, return a list of values"""
    return list(_nested_lookup(key, document, wild=wild))

def _nested_lookup(key, document, wild=False):
    """Lookup a key in a nested document, yield a value"""
    if isinstance(document, list):
        for d in document:
            for result in _nested_lookup(key, d, wild=wild):
                yield result

    if isinstance(document, dict):
        for k, v in iteritems(document):
            if key == k or (wild and key.lower() in k.lower()):
                yield v
            elif isinstance(v, dict):
                for result in _nested_lookup(key, v, wild=wild):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in _nested_lookup(key, d, wild=wild):
                        yield result


          
def fhir_eob_stats(resource):
    """Expects a Bundle resource"""    
    unique_systems = []
    unique_codes = [] 
    unique_eob_types = []
    displayless_codings = []
    displayless_valuecodings = []
    missing_displays = 0
    valuecoding_count = 0
    code_count = 0
    coding_count = 0
    coding_count_wo_display = 0
    valuecoding_count_wo_display = 0
    resource_d = json.loads(resource)
    number_entries = len(resource_d['entry'])
    index = 1
    response = OrderedDict()
    codes_without_displays = 0
    no_display_count = 0

    
    for e in resource_d['entry']:
        
        if e['resource'].get('type'):
                
            for i in e['resource']['type']['coding']:
                if i['system'] == "https://bluebutton.cms.gov/resources/codesystem/eob-type":
                     if i['code'] not in unique_eob_types:
                         unique_eob_types.append(i['code'])
                     
        l = nested_lookup('system', e)
        
        code_lookup = nested_lookup('code', e)
        code_count += len(code_lookup)
        
        coding_lookup = nested_lookup('coding', e)
        coding_count += len(coding_lookup)
        for i in coding_lookup:
            for j in i:
                if not j.get('display'):
                    coding_count_wo_display += 1
                    displayless_codings.append(j.get('system'))
                    
        valuecoding_lookup = nested_lookup('valueCoding', e)
        valuecoding_count += len(valuecoding_lookup)
        for i in valuecoding_lookup:
            if not i.get('display'):
                valuecoding_count_wo_display += 1
                displayless_valuecodings.append(j.get('system'))
        
        
        no_display_lookup = nested_lookup('display', e)
        no_display_count += len(no_display_lookup)
        coding_count_wo_display 
        if e['resource'].get('type'):
            for c in e['resource']['type']['coding']:
                if c['system'] not in unique_systems:
                    unique_systems.append(c['system'])
                    unique_code = OrderedDict()
                    unique_code['name'] = c['system']
                    unique_code['codes'] = [c['code'], ]
                    unique_code['displays'] = [c.get('display', ""),]
                    unique_codes.append(unique_code)
                else:
                    for u in unique_codes:
                        if u['name'] == c['system']:
                            
                            
                            if c['code'] not in u['codes']:
                                u['codes'].append(c['code'])
                                u['displays'].append(c.get('display', ""))

        #Get all the unique systems                        
        for s in l:
            if s not in unique_systems:
                unique_systems.append(s)
                

        index += 1
    #print("Unique Systems", len(unique_systems))
    #for s in unique_systems:
    #    print(s)
        
    for u in unique_codes:
        # line = "System %s" % (u['name'])
        # print(line)
        # print(u['codes'])
        # print(u['displays'])
        if not (u['displays']):
            codes_without_displays += 1
        
    response['total_number_or_resources'] = number_entries
    response['unique_systems'] = len(unique_systems)
    response['unique_eob_types'] = unique_eob_types
    #response['unique_systems'] = unique_systems
    response['coding_count'] =  coding_count
    response['code_count'] = code_count
    response['no_display_count'] =  no_display_count
    response['percent_missing_display'] =   float(no_display_count) /  float(code_count)
    response['coding_count_wo_display'] = coding_count_wo_display
    response['displayless_codings'] =  list(set(displayless_codings))
    response['displayless_valuecodings'] =  list(set(displayless_valuecodings))
    
    return json.dumps(response, indent = 4)




#command line app.
if __name__ == "__main__":
    


    if len(sys.argv) not in (2,):
        print("Usage:")
        print("fhir_stats.py [JSON_FHIR_RESOURCE_FILE]")
        print("Example: fhir_stats.py myresource.json")
        sys.exit(1)
    
    json_resource_path = sys.argv[1]    
    resource_fh = open(json_resource_path)
    resource = resource_fh.read()
    result = fhir_eob_stats(resource)
    print(result)
    resource_fh.close()








