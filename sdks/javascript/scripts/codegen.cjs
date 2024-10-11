const { oldVisit: visit } = require('@graphql-codegen/plugin-helpers');
const { Kind, GraphQLScalarType } = require('graphql');

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

          return `${docblock(node)}
export function ${node.name.value}(${fields}${args(node)}) {
  return client.execute(
    graphql(\`${gqlString(node)}\`,
    ${variables(node)})
  );
}`;
        },
      },
    });

    return `${PREFIX}${IMPORTS}

${jsdocTypemap(typeMap)}
${queriesResult.fields.join('\n\n')}`;
  },
};

/**
 * Generate API docblock
 * @param {import('graphql').FieldDefinitionNode} node
 */
function docblock(node) {
  if (node.name.value === 'version') {
    console.log(resolveReturnValue(node));
  }
  const code = [
    '/**',
    node.description?.value,
    isPrimitive(resolveReturnType(node))
      ? ''
      : ` * @param {Array<keyof import('../src/graphql/graphql.ts').${resolveReturnType(node)}>} fields`,
    node.arguments?.map(jsDocParam),
    '**/',
  ]
    .flat()
    .filter(Boolean);

  // special case: emit no docblock if there is no value
  if (code.length === 2) return '';
  return code.join('\n * ');
}

/***
 *
 * @param {import('graphql').InputValueDefinitionNode['type'} t
 */
function kind(t) {
  switch (t.kind) {
    case Kind.NON_NULL_TYPE: {
      // console.log(t, omitLoc(t));
      // TODO: if not required, emit `[paramName]` syntax
      return kind(t.type);
    }
    case Kind.LIST_TYPE: {
      // console.log(t, omitLoc(t));
      return `${kind(t.type)}[]`;
    }
    case Kind.NAMED_TYPE:
      return t.name.value;
    default:
      throw new TypeError(`Unexpected kind type k`);
  }
}

/***
 * Generate JSDoc param
 * @param {import('graphql').InputValueDefinitionNode} param
 */
function jsDocParam(param) {
  const type = kind(param.type);
  const paramName =
    param.type.kind === Kind.NON_NULL_TYPE
      ? param.name.value
      : `[${param.name.value}]`;
  const description = param.description ? ' ' + param.description.value : '';
  return `@param {${type}} ${paramName}${description}`;
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
    ? `{${node.arguments.map((n) => n.name.value).join(', ')}}`
    : 'undefined';
}

function once(fn) {
  let called = false;
  let result;
  return function (...args) {
    if (called) {
      return result;
    }
    result = fn(...args);
    called = true;
    return result;
  };
}
const logOnce = once(console.log);

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
      args
        .map(
          (n) =>
            `\$${n.name.value}: ${kind(n.type)}${n.type.kind === Kind.NON_NULL_TYPE ? '!' : ''}`,
        )
        .join(', ') +
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
 * @param {import('graphql').FieldDefinitionNode['type']} nodeType
 * @returns Boolean
 */
function isPrimitive(nodeType) {
  // TODO: only NamedType
  switch (nodeType) {
    case 'String':
    case 'Boolean':
    case 'Int':
    case 'Float':
      return true;
    default:
      return false;
  }
}
/***
 * Generate graphql string for field
 * @param {import('graphql').FieldDefinitionNode} node
 */
function resolveReturnType(node) {
  const responseType = node.type;
  switch (responseType.kind) {
    case Kind.NON_NULL_TYPE:
      return resolveReturnType(responseType);
    case Kind.LIST_TYPE:
      return resolveReturnType(responseType);
    case Kind.NAMED_TYPE:
      return responseType.name.value;

    default:
      exhaustive(responseType.kind);
  }
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
      // TODO: fields resolver
      if (isPrimitive(responseType.name.value)) {
        return '';
      } else {
        // console.log('ooookay', omitLoc(node));
        return "{ __typename ${fields.join(' ')} }";
      }

    default:
      exhaustive(responseType.kind);
  }
}

/***
 * Helper to print GraphQL AST node without location information
 */
function omitLoc(t) {
  const { loc, ...withoutLoc } = t;
  return withoutLoc;
}

function capitalize(str) {
  return str[0].toUpperCase() + str.slice(1);
}

/***
 * exhaustive type matcher
 * @param {never} no
 */
function exhaustive(no) {
  throw new TypeError('Unexpected value', JSON.stringify(no));
}

/**
 * Generates jsdoc based typemap for emitted file.
 *
 * @param {ReturnType<import('graphql').GraphQLSchema['getTypeMap']>} typemap
 */
function jsdocTypemap(typemap) {
  let scalars = ['/**'];
  let nonScalars = [];
  Object.entries(typemap).forEach(([key, type]) => {
    // TODO: handle multiple descriptions better
    let description = type.description
      ? ' - ' + type.description.split('\n')[0]
      : '';
    if (type instanceof GraphQLScalarType) {
      return scalars.push(
        ` * @typedef {import('../src/graphql/graphql.ts').Scalars['${key}']['output']} ${key}${description}`,
      );
    } else {
      // ignore graphql native types
      if (key.startsWith('__')) return;

      // TODO: Handle double uppercase the same as the builtin codegen
      return nonScalars.push(
        ` * @typedef {import('../src/graphql/graphql.ts').${key}} ${key}${description}`,
      );
    }
  });
  return scalars.join('\n') + '\n *' + nonScalars.join('\n') + '\n */';
}
