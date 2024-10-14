import { createClient } from './client.mjs';
import * as sdk from './sdk.mjs';
/**
 * @typedef {Object} Config API client config
 * @property {string} host API Host
 * @property {string} apiKey API Key
 * @property {string} apiSecret API Secret
 */

/***
 * Create API config
 *
 * @param {Config} config client config
 * @returns {typeof sdk}
 */
export function create(config) {
  // TODO: update codegen to bind to a config passed in
  // currently we would not support multitenant which would cause very bad bugs
  createClient(config);
  return sdk;
}