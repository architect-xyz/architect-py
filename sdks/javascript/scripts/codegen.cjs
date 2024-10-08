const { oldVisit, PluginFunction, Types } = require('@graphql-codegen/plugin-helpers');
const { transformSchemaAST } = require('@graphql-codegen/schema-ast');
const { createWriteStream } = require('fs');
const { OperationTypeNode, Kind, TypeKind } = require('graphql');
const path = require('path');
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

function log(...args) {
  const file = path.join(__dirname, '..', 'tmp', 'codegen.stdout.log')
  createWriteStream(file).write(`${JSON.stringify(args, null, 2)}\n`);
}

module.exports = {
  /***
   * @param {import('graphql').GraphQLSchema} schema
   * @param {import('graphql').DocumentNode} documents
   * @param {unknown} config
   * @param {unknown} info
   */
  plugin(schema, documents, config) {
    // log(schema.astNode);
    let code = '';
    const result = oldVisit(
      schema.getQueryType().astNode, {
      enter: {
        /*
        OperationTypeDefinition(node) {
          // log('OperationTypeDefinition', JSON.stringify(node));
        },
        Field(node) {
          // log('Field', JSON.stringify(node));
        },
        */

        /**
         * @param {import('graphql').FieldDefinitionNode} node
         */
        FieldDefinition(node) {
          log('FieldDefinition', node);
          code += `
${docblock(node)}
function ${node.name.value}(${args(node)}) {
  return client.execute(graphql('', ${variables(node)}));
}`
        },

        /**
         * @param {import('graphql').OperationDefinitionNode} node
         */
        OperationDefinition(node) {
          code += `
/**
 * ${docblock(node)}
 **/
export function ${node.name.value}() {
  // TODO
}`
          log('append to the code', code)
        },
      },
    });

    return `${PREFIX}${IMPORTS}\n\n${code}`;
  }
}

/**
 * Generate API docblock
 * @param {import('graphql').FieldDefinitionNode} node
 */
function docblock(node) {
  const code = ['/**',
    node.description?.value,
    node.arguments?.map(jsDocParam),
    '**/'].flat().filter(Boolean);

  // special case: emit no docblock if there is no value
  if (code.length === 2) return '';
  return code.join('\n * ')
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
      return kind(t.type)
    }
    case Kind.LIST_TYPE: {
      console.log(t, omitLoc(t));
      return `${kind(t.type)}[]`;
    }
    case Kind.NAMED_TYPE: return t.name.value;
    default: throw new TypeError(`Unexpected kind type k`)
  }
}

/***
 * Generate JSDoc param
  * @param {import('graphql').InputValueDefinitionNode} param
  */
function jsDocParam(param) {
  const type = kind(param.type);
  const paramName = param.type.kind === Kind.NON_NULL_TYPE ? param.name.value : `[${param.name.value}]`
  const description = param.description ? ' ' + param.description.value : ''
  return `@param {${type}} ${paramName}${description}`
}

/***
 * Generate function param
  * @param {import('graphql').FieldDefinitionNode} node
  */
function args(node) {
  return node.arguments ? node.arguments.map(n => n.name.value).join(', ') : '';
}
/***
 * Generate function body variables
  * @param {import('graphql').FieldDefinitionNode} node
  */
function variables(node) {
  return node.arguments ? `{${node.arguments.map(n => n.name.value).join(', ')}}` : 'undefined';
}

/***
  * Helper to print GraphQL AST node without location information
  */
function omitLoc(t) {
  const { loc, ...withoutLoc } = t;
  return withoutLoc
}
