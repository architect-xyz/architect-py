/**
 *
 */
import { createClient } from 'graphql-http';
import { graphql } from 'gql.tada';


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
   * @param {string} query GraphQL document string
   */
  async execute(query) {
    let cancel = () => { }
    return new Promise((resolve, reject) => {
      let result;
      cancel = this.client.subscribe(
        { query, variables: {} },
        {
          next: (data) => result = data,
          error: (err) => reject(err),
          complete: () => resolve(result),
        },
      );
    });
  }
}
