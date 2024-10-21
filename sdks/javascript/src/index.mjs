import { Client } from './sdk.mjs';
import { createClient } from 'graphql-http';

/**
 * @typedef {Object} Config API client config
 * @property {string} host API Host
 * @property {string} apiKey API Key
 * @property {string} apiSecret API Secret
 */

/**
 * @param {Config} config
 * @returns {Client}
 */
export function create(config) {
  return new Client(config, createClient);
}
