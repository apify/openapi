import os
import yaml
import csv
import json

# Path to the root openapi.yaml file
openapi_file_path = '../openapi/openapi.yaml'

# Open and parse mapping csv
with open('./mapping.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    mapping = list(csv_reader)
    print(mapping)

with open('./js-methods.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    js_methods = list(csv_reader)

with open('./py-methods.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    js_methods = list(csv_reader)

    # Load JSON from file and parse
with open('./permalinks-to-old-doc.json', 'r') as json_file:
    all_legacy_link = json.load(json_file)

# Get all paths from root openapi.yaml file and create operationId for each path.
with open(openapi_file_path, 'r') as file:
    openapi_yaml = yaml.safe_load(file)

notfound = []

# Update each path with custom logic
for path, ref in openapi_yaml.get('paths').items():
    print(f'Working with path: {path}')

    # Get the yaml file for the path and parse it
    path_path = '../openapi/' + ref.get('$ref')
    with open(path_path, 'r') as file:
        path_yaml = yaml.safe_load(file)

    # For each method in path do the following
    for method, operation in path_yaml.items():
        print(f'Method: {method}')

        # Operation ID for method
        operationId = operation.get('operationId')
        # Some update logic
        summary = operation.get('summary')

        summary_kabab_case = '-'.join(summary.lower().split(' '))
        # Find in mapping list by API reference URL which is equal to summary
        found_refferece = None
        for legacy_item in all_legacy_link:
            if summary in legacy_item.get('text'):
                print(f"Found matching item: {legacy_item.get('text')} for {summary}")
                found_refferece = legacy_item
                operation['x-legacy-doc-url'] = legacy_item.get('url')

                break
        if not found_refferece:
            notfound.append(summary)
            print(f"Could not find matching item for {summary}")
            continue

    with open(path_path, 'w') as file:
        yaml.safe_dump(path_yaml, file, default_style=None, sort_keys=False)

