/**
 */
import { createClient as createGraphqlClient } from 'graphql-http';
import { print } from 'graphql';
import { initGraphQLTada } from 'gql.tada';
export { readFragment } from 'gql.tada';
/**
 * @typedef { import('./graphql-env.d.ts').introspection } introspection
 */

/**
 * @type {ReturnType<typeof initGraphQLTada<{
 *   introspection: introspection;
 *   scalars: {
 *     Date: string;
 *     DateTime: string;
 *     Decimal: string;
 *     AccountId: string;
 *     UserId: string;
 *     OrderId: string;
 *     MarketId: string;
 *     VenueId: string;
 *     RouteId: string;
 *     ProductId: string;
 *     ComponentId: string;
 *     FillId: string;
 *     Dir: 'buy' | 'sell';
 *     Str: string;
 *     OrderSource: string;
 *   }
 * }>>}
 **/
export const graphql = initGraphQLTada();

/**
 * @typedef {Object} Config API client config
 * @property {string} host API Host
 * @property {string} apiKey API Key
 * @property {string} apiSecret API Secret
 */

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
    // Resolve host to the graphql endpoint
    const host = config.host.includes('4567')
      ? config.host
      : config.host.replace(/\/$/, ':4567/');

    /**
     * GraphQL client that can execute queries against the GraphQL Server
     * @type {ReturnType<typeof createGraphqlClient>}
     * @public
     */
    this.client = createGraphqlClient({
      url: `${host}graphql`,
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
   * @param {Variables} variables query variables
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

/**
 * This is primarily used for internal library testing purposes
 * @private
 */
export function __createClientWithProcessVars() {
  const host = process.env.ARCHITECT_HOST;
  const apiKey = process.env.ARCHITECT_API_KEY;
  const apiSecret = process.env.ARCHITECT_API_SECRET;
  if (typeof host !== 'string') {
    throw new TypeError('process.env.ARCHITECT_HOST must be defined');
  }
  if (typeof apiKey !== 'string') {
    throw new TypeError('process.env.ARCHITECT_API_KEY must be defined');
  }
  if (typeof apiSecret !== 'string') {
    throw new TypeError('process.env.ARCHITECT_API_SECRET must be defined');
  }

  return new Client({ host, apiKey, apiSecret });
}
