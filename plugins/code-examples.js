const AddCodeExamples = require('./decorators/add-code-examples.js');

module.exports = {
  id: 'code-examples',
  decorators: {
    oas3: {
      'add': AddCodeExamples
    }
  }  
}
