const X_LEGACY_DOC_URL_PROPERTY = "x-legacy-doc-url";

/**
 * Prepends an HTML anchor to the description of each node with an HTML fragment from the legacy documentation.
 * This achieves link backward compatibility.
 *
 * For example, if the old URL is https://docs.apify.com/api/v2#/reference/logs/log/get-log, then we prepend:
 *   <div id="/reference/logs/log/get-log"></div>
 *
 * The legacy URL is stored on a custom property `x-legacy-doc-url` in the operation object.
 */
function prependLegacyUrlAnchor(target) {
    if (target[X_LEGACY_DOC_URL_PROPERTY]) {
        const [_, id] = target[X_LEGACY_DOC_URL_PROPERTY].split("#");

        if (!id) {
            console.warn(`Invalid legacy doc URL on ${target.operationId}: ${target[X_LEGACY_DOC_URL_PROPERTY]}`);
            return;
        }

        target.description = `<div id="${id}"></div>${target.description || ""}`;
    }
}

module.exports = () => ({
    Tag: {
        leave: prependLegacyUrlAnchor
    },
    Operation: {
        leave: prependLegacyUrlAnchor
    },
});

