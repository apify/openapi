import schemathesis

@schemathesis.hook
def map_headers(context, headers):
    if headers:
        headers.pop("Authorization", None)  
    return headers
