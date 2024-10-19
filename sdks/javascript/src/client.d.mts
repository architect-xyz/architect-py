/**
 * @param {Config} config API client config
 */
export function createClient(config: Config): void;
/**
 * This is primarily used for internal library testing purposes
 * @private
 */
export function __createClientWithProcessVars(): Client;
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
export const graphql: ReturnType<
  typeof initGraphQLTada<{
    introspection: introspection;
    scalars: {
      Date: string;
      DateTime: string;
      Decimal: string;
      AccountId: string;
      UserId: string;
      OrderId: string;
      MarketId: string;
      VenueId: string;
      RouteId: string;
      ProductId: string;
      ComponentId: string;
      FillId: string;
      Dir: 'buy' | 'sell';
      Str: string;
      OrderSource: string;
    };
  }>
>;
/**
 * @typedef {Object} Config API client config
 * @property {string} host API Host
 * @property {string} apiKey API Key
 * @property {string} apiSecret API Secret
 */
/** @type {Client} */
export let client: Client;
export class Client {
  /**
   * Architect Client SDK class
   *
   * @param {Config} config API client config
   */
  constructor(config: Config);
  /**
   * GraphQL client that can execute queries against the GraphQL Server
   * @type {ReturnType<typeof createGraphqlClient>}
   * @public
   */
  public client: ReturnType<typeof createGraphqlClient>;
  /**
   * Typed GraphQL query parser
   *
   * @param {Parameters<typeof graphql>[0]} query GraphQL document string
   * @returns {ReturnType<typeof graphql>}
   */
  parse(query: Parameters<typeof graphql>[0]): ReturnType<typeof graphql>;
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
  execute<Result, Variables>(
    query: import('gql.tada').TadaDocumentNode<Result, Variables>,
    variables?: Variables | undefined,
  ): Promise<Result>;
}
export type introspection = import('./graphql-env.d.ts').introspection;
/**
 * API client config
 */
export type Config = {
  /**
   * API Host
   */
  host: string;
  /**
   * API Key
   */
  apiKey: string;
  /**
   * API Secret
   */
  apiSecret: string;
};
import { initGraphQLTada } from 'gql.tada';
import { createClient as createGraphqlClient } from 'graphql-http';
//# sourceMappingURL=client.d.mts.map
