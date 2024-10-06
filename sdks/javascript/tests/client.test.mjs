import assert from 'node:assert/strict';
import { describe, test } from 'node:test';

import { Client } from "../src/client.mjs";

const createClient = () => new Client({
  host: process.env.ARCHITECT_HOST,
  apiKey: process.env.ARCHITECT_API_KEY,
  apiSecret: process.env.ARCHITECT_API_SECRET,
});
describe('Client', () => {
  test('can query', async () => {
    const c = createClient();
    const r = await c.execute(`query Me { me { __typename userId email userTier } }`);
    console.log('Result?', r);
    assert.deepEqual(
      r.data,
      {
        me: {
          __typename: 'Me',
          userId: '00000000-0000-0000-0000-000000000000',
          email: 'anonymous@',
          userTier: 'BROKERAGE_UNSUBSCRIBED'
        }
      }
    );
  });
});
