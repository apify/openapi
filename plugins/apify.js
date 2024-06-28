const LegacyDocUrlDecorator = require("./decorators/legacy-doc-url-decorator");

module.exports = {
  id: 'apify',
  decorators: {
    oas3: {
      'legacy-doc-url-decorator': LegacyDocUrlDecorator
    }
  }
}
