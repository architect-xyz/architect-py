import { createClient } from 'graphql-http';
import { Client } from './sdk.mjs';

/**
 * This is primarily used for internal library testing purposes
 * @private
 * @returns {Client}
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

  return new Client({ host, apiKey, apiSecret }, createClient);
}
