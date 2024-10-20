import { createClient } from './client.mjs';
import * as sdk from './sdk.mjs';
/**
 * @typedef {Object} Config API client config
 * @property {string} host API Host
 * @property {string} apiKey API Key
 * @property {string} apiSecret API Secret
 */

let instantiated = false;
/***
 * Create API config
 *
 * @param {Config} config client config
 * @returns {typeof sdk}
 */
export function create(config) {
  // TODO: update codegen to bind to a config passed in to remove this error
  // case
  // currently we would not support multitenant which would cause very bad bugs
  // something like `import('./sdk.mjs').then(createSdk = createSdk(client));`
  if (instantiated) {
    throw new Error(
      'architect-js does not currently support multiple clients per thread.',
    );
  }

  instantiated = true;
  createClient(config);

  return sdk;
}
