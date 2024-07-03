import ruamel.yaml
import csv
import json


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

# Open and parse mapping csv
with open('./lost-mapping.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    lost_mapping = list(csv_reader)
    print(lost_mapping)

not_found = []

# Get all paths from root openapi.yaml file and create operationId for each path.
with open(openapi_file_path, 'r') as file:
    openapi_yaml = yaml.load(file)


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

        # Operation ID for method
        operationId = operation.get('operationId')
        # Some update logic
        summary = operation.get('summary')
        print(f"Summary: {summary}")
        tag = operation.get('tags')[0]
        print(f"Tag: {tag}")
    
        # Find in mapping list by API reference URL which is equal to summary
        new_tag = None
        for row in lost_mapping:
            if summary in row['Action Name'] and tag in row['Resource Group']:
                new_tag = f"{row['Resource Group']}/{row['Resource']}"
                print(f"Found new tag: {new_tag}")
                operation['tags'][0] = new_tag

                break
        if not new_tag:
            not_found.append(summary)
            print(f"Could not find matching item for {summary}")
            continue


    with open(path_path, 'w') as file:
        yaml.dump(path_yaml, file)

print(not_found)

