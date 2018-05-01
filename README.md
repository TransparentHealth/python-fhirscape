python-fhirscape - A set of command line tools for inspecting FHIR resources. 
============================================================================

Please see https://hl7.og/fhir for more information on FHIR.


The command line tool `fhir_validate.py` expects a FHIR bundle as input.  It outputs a summary as JSON to stdout and writes
CSV to disk.  Here is the example usage:



    >python fhhir_validate.py pde.json

Produces the output:


    {
        "number_of_entries": 1,
        "number_entries_processed": 1,
        "number_of_errors": 1,
        "result_filename": "fhirscape/pde.json.csv"
    }    

Lets print the CSV output:


     >cat pde.json.csv
     severity,code,diagnostics,location
     error,processing,"Profile http://hl7.org/fhir/StructureDefinition/ExplanationOfBenefit, Element 'ExplanationOfBenefit.item.detail.sequence': minimum required = 1, but only found 0",ExplanationOfBenefit.item.detail


Another tool `fhir_eob_stats.py` is designed to provide  information about the complexity and quality of `ExplanationOfBenefit`
 `Bundle` resources.  Here is an example of its use.
 
 
     >python fhir_eob_stats.py pde.json

Ant the output is:




    {
        "total_number_or_resources": 1,
        "unique_systems": 22,
        "unique_eob_types": [
            "PDE"
        ],
        "coding_count": 30,
        "code_count": 41,
        "no_display_count": 29,
        "percent_missing_display": 0.7073170731707317,
        "coding_count_wo_display": 3,
        "displayless_codings": [
            "https://bluebutton.cms.gov/resources/variables/ptnt_rsdnc_cd",
            "http://hl7.org/fhir/sid/ndc",
            "https://bluebutton.cms.gov/resources/codesystem/eob-type"
        ],
        "displayless_valuecodings": []
    }

