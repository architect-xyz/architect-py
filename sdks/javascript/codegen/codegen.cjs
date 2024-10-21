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
 * @property {'debugging' | 'production'} mode Emitting mode
 */

/**
 * TODO: these comment prefixes are primarily to confirm config and emit
 * differences. Cleanup before releasing.
 */
const PROD_PREFIX = `/**
 * Copyright (c) Architect Financial Technologies, Inc. and affiliates.
 *
 * This source code is licensed under the Apache 2.0 license found in the
 *
 * LICENSE file in the root directory of this source tree.
 */`;

const DEBUG_PREFIX = `/**
 * Temp file for iteratively building the JS SDK codegen
 */`;

const IMPORTS = `
import { print } from 'graphql';
import { graphql } from './client.mjs';
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
        const returnType = resolveReturnType(node);
        const fields = isPrimitive(returnType) ? '' : 'fields, ';
        const vars = variables(node);
        const deserializer = `results => results['${node.name.value}']`;

        return `${jsdoc.docblock(node)}
  async ${node.name.value}(${fields}${args(node)}) {
    return this.execute(
      graphql(\`${queryType} ${gql.template(node)}\`)${vars ? `,\n${vars}\n` : ''}
    ).then(${deserializer});
  }`;
      },
    },
  };
}
const apiOpeningBlock = `
/**
 * @typedef {Object} Config API client config
 * @property {string} host API Host
 * @property {string} apiKey API Key
 * @property {string} apiSecret API Secret
 */

export class Client {
  /**
   * Architect Client SDK class
   *
   * @param {Config} config API client config
   * @param {import('graphql-http')['createClient']} createGraphqlClient
   */
  constructor(config, createGraphqlClient) {
    // Resolve host to the graphql endpoint
    const host = config.host.includes('4567')
      ? config.host
      : config.host.replace(/\\/$/, ':4567/');

    /**
     * GraphQL client that can execute queries against the GraphQL Server
     * @type {import('graphql-http').Client} client
     * @public
     */
    this.client = createGraphqlClient({
      url: \`\${host}graphql\`,
      headers: {
        Authorization: \`Basic \${config.apiKey} \${config.apiSecret}\`,
      },
    });
  }

  /**
   * Typed GraphQL query parser
   *
   * @param {Parameters<typeof graphql>[0]} query GraphQL document string
   * @returns {ReturnType<typeof graphql>}
   */
  parse(query) {
    return graphql(query);
  }

  /**
   * Execute a GraphQL query with typed response
   *
   * @template Result [Result=any]
   * @template Variables [Variables=any]
   *
   * @param {import('gql.tada').TadaDocumentNode<Result, Variables>} query GraphQL document string
   * @param {Variables} [variables] query variables
   * @returns {Promise<Result>}
   */
  async execute(query, variables) {
    let cancel = () => { };
    return new Promise((resolve, reject) => {
      /**
       * @type {Result}
       */
      let result;
      cancel = this.client.subscribe(
        {
          query: print(query),
          // @ts-expect-error Variables type is not quite the same
          variables,
        },
        {
          next: (resp) => {
            // @ts-expect-error resp.data may not be provided in error cases
            result = resp.data;
          },
          error: (err) => reject(err),
          complete: () => resolve(result),
        },
      );
    });
  }
`;

module.exports = {
  /***
   * @param {import('graphql').GraphQLSchema} schema
   * @param {import('graphql').DocumentNode} documents
   * @param {Config} config Plugin configuration
   * @param {unknown} info
   */
  plugin(schema, _documents, config) {
    const PREFIX = config.mode === 'production' ? PROD_PREFIX : DEBUG_PREFIX;

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

${apiOpeningBlock}

  ${queries.fields.join('\n\n')}

  ${mutations.fields.join('\n\n')}
}
`;
  },

  /**
   * @param {import('graphql').GraphQLSchema} _schema
   * @param {import('graphql').DocumentNode} _documents
   * @param {Config} config Plugin configuration
   * @param {string} _outputFile The name of the output file
   * @param {unknown[]} _allPlugins all plugins requested in this specific output file
   */
  validate(_schema, _documents, config, _outputFile, _allPlugins) {
    const errors = [];
    if ('mode' in config) {
      // validate `mode` is of a valid type
      if (config.mode !== 'debugging' && config.mode !== 'production') {
        errors.push(
          `Invalid option provided for "mode". Received "${config.mode}", expected one of ("debugging" | "production")`,
        );
      }
    }
    if (errors.length > 0) {
      throw new Error(errors.join('\n\n'));
    }
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
