#!/usr/bin/env python
__author__ = 'Alan Viars @aviars'
import requests
import sys
import json
from collections import OrderedDict
import requests
import time
import csv
from six import iteritems

__author__  = "Alan Viars"

default_fhir_url = "https://hapi.fhir.org/baseDstu3/"


 
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
 
        
        
def fhir_get_validate_errors(resource, fhir_url=default_fhir_url):
    l = []
    # Validate each record      
    val_url = "%s%s/$validate" % (fhir_url, resource['resourceType'])
    r = requests.post(val_url, json=resource)
    response = r.json(object_pairs_hook=OrderedDict)
    for issue in response['issue']:
        if issue['severity'] == 'error':
            l.append(issue)
    return l
        
    

                    
def verify_fhir(resource, fhir_url):
    response = OrderedDict()
    unique_systems = []
    unique_codes = [] 
    unique_eob_types = []
    resource_d = json.loads(resource)
    validation_errors = []
    unique_diagnostics = []
    unique_validation_errors = []
    

    #print(len(resource_d['entry']),  "Entries found.")
    response['number_of_entries'] = len(resource_d['entry'])
    index = 0
    
    for e in resource_d['entry']:
        # print(index)
        #print(e['resource']['resourceType'])
        index += 1
        #for i in e['resource']['type']['coding']:
           
         #   if i['system'] == "https://bluebutton.cms.gov/resources/codesystem/eob-type":
          #       if i['code'] not in unique_eob_types:
           #          unique_eob_types.append(i['code'])
                     #print(i['code'])
        #l = nested_lookup('system', e)
        
        
        # for c in e['resource']['type']['coding']:
        #     if c['system'] not in unique_systems:
        #         unique_systems.append(c['system'])
        #         unique_code = OrderedDict()
        #         unique_code['name'] = c['system']
        #         unique_code['codes'] = [c['code'], ]
        #         unique_code['displays'] = [c.get('display', ""),]
        #         unique_codes.append(unique_code)    
        #     else:
        #         for u in unique_codes:
        #             if u['name'] == c['system']:
        #                 if c['code'] not in u['codes']:
        #                     u['codes'].append(c['code'])
        #                     u['displays'].append(c.get('display', ""))
        #                 
        # for s in l:
        #     if s not in unique_systems:
        #         unique_systems.append(s)
                
        validation_errors += fhir_get_validate_errors(e['resource'])
        # Validate each record      
        #val_url = "%s%s/$validate" % (fhir_url, e['resource']['resourceType'])
        #print(val_url)
        #print("E",e)
        
        
        # 
        # r = requests.post(val_url, json=e['resource'])
        # response = r.json()
        # for issue in response['issue']:
        #     if issue['severity'] == 'error':
        #         # print(issue)
        #         # print(json.dumps(e['resource']['type'], indent = 4))
        #         validation_errors.append(issue)
        #         if issue['diagnostics'] not in unique_diagnostics:
        #             unique_diagnostics.append(issue['diagnostics'] ) 
        #             unique_validation_errors.append(issue)
        
        #if index == 2:
         #   break
    #print("Unique Systems", len(unique_systems))
    #for s in unique_systems:
    #    print(s)
        
    #for u in unique_codes:
     #   line = "System %s" % (u['name'])
        #print(line)
        #print(u['codes'])
        #print(u['displays'])
    #print(unique_eob_types)
    response['number_entries_processed'] = index
    response['number_of_errors'] = len(validation_errors)
    response['validation_errors'] = validation_errors
    #response['uniaue_validation_errors'] = unique_validation_errors
    return response




#command line app.
if __name__ == "__main__":
    


    if len(sys.argv) not in (2,3):
        print("Usage:")
        print("verify_fhir.py [JSON_FHIR_RESOURCE_FILE] <FHIR_BASE_URL>")
        print("Example: fhir_validate.py myresource.json https://hapi.fhir.org/baseDstu3/")
        sys.exit(1)
    
    json_resource_path = sys.argv[1]    
    if len(sys.argv) == 3:
        fhir_url = sys.argv[2]
    else:
        fhir_url = default_fhir_url
        
    
    resource_fh = open(json_resource_path)
    resource = resource_fh.read()
    result = verify_fhir(resource, fhir_url)
    result_filename = json_resource_path + ".csv"
    result['result_filename'] = result_filename
    # MAke the CSV
    with open(result_filename,'w') as fou:
        dw = csv.DictWriter(fou, delimiter=',', fieldnames=result['validation_errors'][0])
        dw.writeheader()
        for row in result['validation_errors']:
            row['location'] = row['location'][0] 
            dw.writerow(row)
    del result['validation_errors']
    print(json.dumps(result, indent = 4))
    #print("Done.")
    resource_fh.close()








