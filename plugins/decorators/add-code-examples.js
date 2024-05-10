module.exports = AddCodeExamples;

function AddCodeExamples({languages}) {
  console.log("updating OperationIds ... ");
  return {

    // For other types look up
    // https://redocly.com/docs/openapi-visual-reference/openapi-node-types/
    PathItem: {
    
      // Redoc's visitor pattern
      // https://redocly.com/docs/cli/custom-plugins/visitor/
      leave(target) {
        console.log(target)
        if(target.description) {
          target['x-codeSamples'] = [
            {
              lang: "Shell",
              source: `$ curl --booboo ${target.operationId}`
            }
          ]  
        }
      }
    },
  }
};
