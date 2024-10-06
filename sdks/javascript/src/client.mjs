/**
 */
import { createClient } from 'graphql-http';
import { graphql } from 'gql.tada';
import { print } from 'graphql';

export { graphql };

export class Client {
  /**
   * Architect Client SDK class
   *
   * @param {Object} config API client config
   * @param {string} config.host API host
   * @param {string} config.apiKey API Key
   * @param {string} config.apiSecret API Secret
   *
   */
  constructor(config) {
    this.config = config
    /**
     * GraphQL client that can execute queries against the GraphQL Server
     * @type {ReturnType<typeof createClient>}
     * @public
     */
    this.client = createClient({ url: `${config.host}api/graphql` })
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
          variables
        },
        {
          next: (resp) => {
            // @ts-expect-error resp.data may not be provided in error cases
            result = resp.data
          },
          error: (err) => reject(err),
          complete: () => resolve(result),
        },
      );
    });
  }
}
