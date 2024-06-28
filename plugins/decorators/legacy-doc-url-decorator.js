const X_LEGACY_DOC_URL_PROPERTY = "x-legacy-doc-url";

/**
 * Prepends an HTML anchor to the description of each operation with an HTML fragment from the legacy documentation.
 * This achieves link backward compatibility.
 *
 * For example, if the old URL is https://docs.apify.com/api/v2#/reference/logs/log/get-log, then we prepend:
 *   <div id="/reference/logs/log/get-log"></div>
 *
 * The legacy URL is stored on a custom property `x-legacy-doc-url` in the operation object.
 */
function LegacyDocUrlDecorator() {
  return {
    Operation: {
      leave(operation) {
        if (operation[X_LEGACY_DOC_URL_PROPERTY]) {
          const [_, id] = operation[X_LEGACY_DOC_URL_PROPERTY].split("#");

          if (!id) {
            console.warn(`Invalid legacy doc URL on ${operation.operationId}: ${operation[X_LEGACY_DOC_URL_PROPERTY]}`);
            return;
          }

          operation.description = `<div id="${id}"></div>${operation.description || ""}`;
        }
      }
    },
  }
}

module.exports = LegacyDocUrlDecorator;

