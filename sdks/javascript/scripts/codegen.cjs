const { oldVisit: visit } = require('@graphql-codegen/plugin-helpers');
const { Kind } = require('graphql');
const jsdoc = require('./emit/jsdoc.cjs');
const {
  capitalize,
  omitLoc,
  exhaustive,

  isPrimitive,
  resolveReturnType,
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

module.exports = {
  /***
   * @param {import('graphql').GraphQLSchema} schema
   * @param {import('graphql').DocumentNode} documents
   * @param {Config} config Plugin configuration
   * @param {unknown} info
   */
  plugin(schema, _documents, config) {
    const typeMap = schema.getTypeMap();
    // log(schema.astNode);

    // TODO: schema.getMutationType().astNode
    // TODO: schema.getSubscriptionType().astNode
    const queriesResult = visit(schema.getQueryType().astNode, {
      leave: {
        /**
         * @param {import('graphql').FieldDefinitionNode} node
         */
        FieldDefinition(node) {
          const fields = isPrimitive(resolveReturnType(node)) ? '' : 'fields, ';

          return `${jsdoc.docblock(node)}
export function ${node.name.value}(${fields}${args(node)}) {
  return client.execute(
    graphql(\`${gqlString(node)}\`),
    ${variables(node)}
  );
}`;
        },
      },
    });

    return `${PREFIX}${IMPORTS}

${jsdoc.typemap(typeMap)}
${queriesResult.fields.join('\n\n')}`;
  },
};

/***
 * Generate kind syntax for jsdoc
 * @param {import('graphql').InputValueDefinitionNode['type'} t
 */
function gqlKind(t) {
  switch (t.kind) {
    case Kind.NON_NULL_TYPE: {
      // console.log(t, omitLoc(t));
      // TODO: if not required, emit `[paramName]` syntax
      return `${gqlKind(t.type)}!`;
    }
    case Kind.LIST_TYPE: {
      // console.log(t, omitLoc(t));
      return `[${gqlKind(t.type)}]`;
    }
    case Kind.NAMED_TYPE:
      return t.name.value;
    default:
      throw new TypeError(`Unexpected kind type k`);
  }
}

/***
 * Generate function param
 * @param {import('graphql').FieldDefinitionNode} node
 */
function args(node) {
  return node.arguments?.length > 0
    ? node.arguments.map((n) => n.name.value).join(', ')
    : '';
}

/***
 * Generate function body variables
 * @param {import('graphql').FieldDefinitionNode} node
 */
function variables(node) {
  return node.arguments?.length > 0
    ? `{${node.arguments.map((n) => n.name.value).join(', ')} } `
    : 'undefined';
}

/***
 * Generate graphql string for field
 * @param {import('graphql').FieldDefinitionNode} node
 */
function gqlString(node) {
  /*
  if (node.name.value === 'version') {
    const base = omitLoc(node);
    const name = omitLoc(node.name);
    const type = omitLoc(node.type);
    logOnce('gqlString', JSON.stringify({ ...base, name, type }, null, 4));
  }
  */
  const args = node.arguments?.length > 0 ? node.arguments : null;
  const params = args
    ? '(' +
    args.map((n) => `\$${n.name.value}: ${gqlKind(n.type)}`).join(', ') +
    ')'
    : '';
  const queryParams = args
    ? '(' +
    args.map((n) => `${n.name.value}: \$${n.name.value}`).join(', ') +
    ')'
    : '';
  const fields = resolveReturnValue(node);

  return `query ${capitalize(node.name.value)}${params} {
  ${node.name.value}${queryParams} ${fields}
}`;
}

/***
 * Generate graphql string for field
 * @param {import('graphql').FieldDefinitionNode} node
 */
function resolveReturnValue(node) {
  const responseType = node.type;
  switch (responseType.kind) {
    case Kind.NON_NULL_TYPE:
      return resolveReturnValue(responseType);
    case Kind.LIST_TYPE:
      return resolveReturnValue(responseType);
    case Kind.NAMED_TYPE:
      if (isPrimitive(responseType.name.value)) {
        return '';
      } else {
        // TODO: use fragment for fields
        return "{ __typename ${fields.join(' ')} }";
      }

    default:
      exhaustive(responseType.kind);
  }
}
