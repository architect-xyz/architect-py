import assert from 'node:assert/strict';
import { describe, test } from 'node:test';

import { Client, graphql } from "../src/client.mjs";

const createClient = () => {
  const host = process.env.ARCHITECT_HOST;
  const apiKey = process.env.ARCHITECT_API_KEY;
  const apiSecret = process.env.ARCHITECT_API_SECRET;
  assert(typeof host === 'string', 'process.env.ARCHITECT_HOST must be defined');
  assert(typeof apiKey === 'string', 'process.env.ARCHITECT_API_KEY must be defined');
  assert(typeof apiSecret === 'string', 'process.env.ARCHITECT_API_SECRET must be defined');

  return new Client({ host, apiKey, apiSecret });
}

describe('Client', () => {
  test('can query with types, even though we’re only using javascript', async () => {
    const c = createClient();
    const query = graphql(`query Me { me { __typename userId email } }`);
    const r = await c.execute(query);

    assert.deepEqual(
      r,
      {
        me: {
          __typename: 'Me',
          userId: '00000000-0000-0000-0000-000000000000',
          email: 'anonymous@',
          // userTier: 'BROKERAGE_UNSUBSCRIBED'
        }
      }
    );
  });
});
