import schemathesis

# Create a custom config
custom_config = (
        schemathesis.sanitization.Config(replacement="[Filtered]")
    .with_keys_to_sanitize("token")
    .with_sensitive_markers("token")
)

# Configure Schemathesis to use your custom sanitization configuration
schemathesis.sanitization.configure(custom_config)

@schemathesis.hook
def map_headers(context, headers):
    if headers:
        headers.pop("Authorization", None)  
    return headers
