## Architect SDK Codegen

The client SDK is primarily generated through introspecting our public APIs.

### Run Codegen

Run either of the following commands
* `npm run codegen`
* `node_modules/.bin/graphql-codgen`

### Validate Codegen

Currently codegen validation is mostly a manual process, with some basic tests
and demos and some type-tests.
* Ensure the `demo/run.mjs` file still completes
* Ensure `tsc --noEmit` still typechecks
* Open editor and spot check input and output types from the API
* Link to an example repo to ensure consumer usage works as expected
