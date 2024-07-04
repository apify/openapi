import ruamel.yaml
import csv
import json
from slugify import slugify

yaml = ruamel.yaml.YAML(typ='rt')
yaml.indent(mapping=2, sequence=4, offset=2)

# https://stackoverflow.com/questions/78075152/preserve-line-wrapping-in-ruamel-yaml
# needed to convert flow sclars (>-) to literal blocks (|)
yaml.width = 10000

# https://stackoverflow.com/questions/42094599/preserving-quotes-in-ruamel-yaml
yaml.preserve_quotes = True

# non empty null
# https://stackoverflow.com/questions/57172997/yaml-dumper-outputs-blank-instead-of-null-from-none-value-how-to-make-it-output
def my_represent_none(self, data):
    return self.represent_scalar(u'tag:yaml.org,2002:null', u'null')

yaml.representer.add_representer(type(None), my_represent_none)

# Path to the root openapi.yaml file
openapi_file_path = '../openapi/openapi.yaml'

# Get all paths from root openapi.yaml file and create operationId for each path.
with open(openapi_file_path, 'r') as file:
    openapi_yaml = yaml.load(file)

tags_file_path = '../openapi/components/tags.yaml'
with open(tags_file_path, 'r') as file:
    tags = yaml.load(file)

# Open and parse mapping csv
with open('./mapping.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    mappings = list(csv_reader)

with open('./js-methods.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    js_methods = list(csv_reader)

with open('./py-methods.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    py_methods = list(csv_reader)

js_not_found = []
py_not_found = []
# Update each path with custom logic
for path, ref in openapi_yaml.get('paths').items():
    print(f'Working with path: {path}')

    # Get the yaml file for the path and parse it
    path_path = '../openapi/' + ref.get('$ref')
    with open(path_path, 'r') as file:
        path_yaml = yaml.load(file)

    # For each method in path do the following
    for method, operation in path_yaml.items():
        print(f'Method: {method}')
        legacy_doc_url = operation.get('x-legacy-doc-urls')

        if not legacy_doc_url: raise Exception(f"No legacy link for {path} / {operation.get('summary')}") 
    
        # find js
        found = None
        for mapping in js_methods:
            if legacy_doc_url[0] in mapping.get('parsedAPIReferenceUrl'):
              found = True
              operation['x-js-parent'] = mapping.get('parent')
              operation['x-js-name'] = mapping.get('name')
              operation['x-js-doc-url'] = mapping.get('jsReferenceUrl')
              
              
              
        if not found :
            #raise Exception(f"Can't find mapping for {legacy_doc_url}")
            print(f"Can't find mapping for {legacy_doc_url}")
            js_not_found.append(legacy_doc_url)

        # find py
        found = None
        for mapping in py_methods:
            if legacy_doc_url[0] in mapping.get('parsedAPIReferenceUrl'):
              found = True
              operation['x-py-parent'] = mapping.get('parentName')
              operation['x-py-name'] = mapping.get('methodName')
              operation['x-py-doc-url'] = mapping.get('pythonReferenceUrl')
              
        if not found :
            #raise Exception(f"Can't find mapping for {legacy_doc_url}")
            print(f"Can't find mapping for {legacy_doc_url}")
            py_not_found.append(legacy_doc_url)

        

    with open(path_path, 'w') as file:
        yaml.dump(path_yaml, file)


print(f"js not found {len(js_not_found)}")
print(js_not_found)
print(f"js not found {len(py_not_found)}")
print(py_not_found)


"""
  x-client-js-doc-url: <url>
  x-client-js-class:
  x-client-js-method:
  x-client-py-doc-url: <url>
  x-client-py-class:
  x-client-py-method:
"""


