const { oldVisit: visit } = require('@graphql-codegen/plugin-helpers');
const jsdoc = require('./emit/jsdoc.cjs');
const gql = require('./emit/gql.cjs');
const {
  isPrimitive,
  resolveReturnType,
  resolveArgs,
} = require('./emit/shared.cjs');

/**
 * @typedef {Object} Config
 * @property {{[key: string]: string}} scalars scalar mapping
 */

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

const IMPORTS = `
import { client, graphql } from './client.mjs';
`;

/**
 * Create codegen visitor
 * @param {'query' | 'mutation' | 'subscription'} queryType
 */
function createVisitor(queryType) {
  return {
    leave: {
      /**
       * @param {import('graphql').FieldDefinitionNode} node
       */
      FieldDefinition(node) {
        const fields = isPrimitive(resolveReturnType(node)) ? '' : 'fields, ';
        const vars = variables(node);
        const deserializer =
          queryType === 'query'
            ? `results => results['${node.name.value}']`
            : queryType === 'mutation'
              ? `results => {
    /** @type {Awaited<${resolveReturnType(node)}>} */
    return results['${node.name.value}'];
  }`
              : 'TODO';

        return `${jsdoc.docblock(node)}
export function ${node.name.value}(${fields}${args(node)}) {
  return client.execute(
    graphql(\`${queryType} ${gql.template(node)}\`)${vars ? `,\n${vars}\n` : ''}
  ).then(${deserializer});
}`;
      },
    },
  };
}

module.exports = {
  /***
   * @param {import('graphql').GraphQLSchema} schema
   * @param {import('graphql').DocumentNode} documents
   * @param {Config} _config Plugin configuration
   * @param {unknown} info
   */
  plugin(schema, _documents, _config) {
    const typeMap = schema.getTypeMap();

    const queries = visit(
      schema.getQueryType().astNode,
      createVisitor('query'),
    );
    const mutations = visit(
      schema.getMutationType().astNode,
      createVisitor('mutation'),
    );
    // TODO: subscriptions
    // const subscriptions = visit(schema.getSubscriptionType().astNode, createVisitor('subscription'));

    return `${PREFIX}${IMPORTS}

${jsdoc.typemap(typeMap)}

${queries.fields.join('\n\n')}

${mutations.fields.join('\n\n')}`;
  },
};

/***
 * Generate function body variables
 * @param {import('graphql').FieldDefinitionNode} node
 */
function variables(node) {
  const args = resolveArgs(node);
  return args ? `{${args.map((n) => n.name.value).join(', ')} } ` : '';
}

/***
 * Generate function param
 * @param {import('graphql').FieldDefinitionNode} node
 */
function args(node) {
  const args = resolveArgs(node);
  return args ? args.map((n) => n.name.value).join(', ') : '';
}
