import assert from 'node:assert/strict';

import { Client, graphql } from '../src/client.mjs';
export { graphql };

const createClient = () => {
  const host = process.env.ARCHITECT_HOST;
  const apiKey = process.env.ARCHITECT_API_KEY;
  const apiSecret = process.env.ARCHITECT_API_SECRET;
  assert(typeof host === 'string', 'process.env.ARCHITECT_HOST must be defined');
  assert(typeof apiKey === 'string', 'process.env.ARCHITECT_API_KEY must be defined');
  assert(typeof apiSecret === 'string', 'process.env.ARCHITECT_API_SECRET must be defined');

  return new Client({ host, apiKey, apiSecret });
}

export const client = createClient();
