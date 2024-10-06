const { oldVisit, PluginFunction, Types } = require('@graphql-codegen/plugin-helpers');
const { transformSchemaAST } = require('@graphql-codegen/schema-ast');
/*
const PREFIX = `/**
 * Copyright (c) Architect Financial Technologies, Inc. and affiliates.
 *
 * This source code is licensed under the Apache 2.0 license found in the
 *
 * LICENSE file in the root directory of this source tree.
 *`;
*/

const PREFIX = `/**
 * Temp file for iteratively building the JS SDK codegen
 */`;

module.exports = {
  /***
   * @param {import('graphql').GraphQLSchema} schema
   * @param {import('graphql').DocumentNode} documents
   * @param {unknown} config
   * @param {unknown} info
   */
  plugin(schema, documents, config) {
    const result = oldVisit(
      schema.astNode, {
      leave: {
        FieldDefinition(node) {
          console.log('OperationDefinition', node);
        },
        OperationDefinition(node) {
          console.log('OperationDefinition', node);
        },
      },
    });

    /*
    return documents
      .map(doc => {
        const docsNames = doc.document.definitions.map(def => def.name.value)

        return `File ${ doc.location } contains: ${ docsNames.join(', ') } `
      })
      .join('\n')
    */
    return `${PREFIX}\n\n${result.definitions}`;
  }
}
