const OpenAPISnippet = require('openapi-snippet')


// https://github.com/ErikWittern/openapi-snippet/tree/main
//

function AddCodeExamples({languages}) {
  console.log("updating OperationIds ... ");
try {
  return {

    // For other types look up
    // https://redocly.com/docs/openapi-visual-reference/openapi-node-types/
    Root: {
      leave(target) {
        //console.log(target)
        const openApi = target
        const targets = ['shell_curl']
        
        // Shamelessly stolen from:
        // https://github.com/cdwv/oas3-api-snippet-enricher/blob/master/index.js
        try {
          for(var path in target.paths){
            for(var method in openApi.paths[path]){
              if ( !/get|put|post|delete|patch|options|head|trace/.test(method)) { continue; }
              var generatedCode = OpenAPISnippet.getEndpointSnippets(target, path, method, targets);
              target.paths[path][method]["x-codeSamples"] = [];
              for(var snippetIdx in generatedCode.snippets){
                var snippet = generatedCode.snippets[snippetIdx];
                target.paths[path][method]["x-codeSamples"][snippetIdx] = { "lang": snippet.title, "source": snippet.content };
              }        
            }
          }       

        } catch(e) {
          console.trace(e)
        }
        //console.log(results)
      }
    },

    Paths: {
      PathItem: {
        leave(terget, ctx, parents){
          // this will get us the path - it's working
          //console.log('boooboo', ctx.key)
        },

        Operation: {
          // Redoc's visitor pattern
          // https://redocly.com/docs/cli/custom-plugins/visitor/
          leave(target, ctx, parents) {
            // this gets us method - it's working
            //console.log('booboo',ctx.key)
            
            //console.log(ctx)

            //console.log()
            //target['x-codeSamples'] = [
            //  {
            //    lang: "Shell",
            //    source: `$ curl --booboo ${target.operationId}`
            //  }
            //]
            //console.log(target['x-codeSamplesMethod'])
            //console.log(target['x-codeSamplesPath'])
          }
        }
      },
    }
  }
} catch(e) {
  console.log("Exploded:")
  console.log(e)
}  
};

module.exports = AddCodeExamples;

