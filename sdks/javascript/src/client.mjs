/**
 */
import { createClient as createGraphqlClient } from 'graphql-http';
import { print } from 'graphql';
import { graphql } from 'gql.tada';

/**
 * @typedef {Object} Config API client config
 * @property {string} host API Host
 * @property {string} apiKey API Key
 * @property {string} apiSecret API Secret
 */

export { graphql };

/** @type {Client} */
export let client;
/**
 * @param {Config} config API client config
 */
export function createClient(config) {
  client = new Client(config);
}

export class Client {
  /**
   * Architect Client SDK class
   *
   * @param {Config} config API client config
   */
  constructor(config) {
    this.config = config;
    /**
     * GraphQL client that can execute queries against the GraphQL Server
     * @type {ReturnType<typeof createGraphqlClient>}
     * @public
     */
    this.client = createGraphqlClient({
      url: `${config.host}api/graphql`,
      headers: {
        Authorization: `Basic ${config.apiKey} ${config.apiSecret}`,
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
   *
   * @template Result [Result=any]
   * @template Variables [Variables=any]
   *
   * @param {import('gql.tada').TadaDocumentNode<Result, Variables>} query GraphQL document string
   * @param {Variables} [variables] query variables
   * @returns {Promise<Result>}
   */
  async execute(query, variables) {
    let cancel = () => {};
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
}

/*
const c = new Client({});
const q = graphql(`query Route($id: RouteId!) {
  route (id: $id) {
    __typename
    id 
    name
  }
}`)
const b = await c.execute(q, { id: 'nah' });
*/
