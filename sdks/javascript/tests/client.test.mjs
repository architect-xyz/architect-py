import assert from 'node:assert/strict';
import { describe, test } from 'node:test';

import { Client, graphql } from '../src/client.mjs';

const createClient = () => {
  const host = process.env.ARCHITECT_HOST;
  const apiKey = process.env.ARCHITECT_API_KEY;
  const apiSecret = process.env.ARCHITECT_API_SECRET;
  assert(
    typeof host === 'string',
    'process.env.ARCHITECT_HOST must be defined',
  );
  assert(
    typeof apiKey === 'string',
    'process.env.ARCHITECT_API_KEY must be defined',
  );
  assert(
    typeof apiSecret === 'string',
    'process.env.ARCHITECT_API_SECRET must be defined',
  );

  return new Client({ host, apiKey, apiSecret });
};

describe('Client', () => {
  test('can query with types, even though we’re only using javascript', async () => {
    const c = createClient();
    const query = graphql(`query Me { me { __typename userId email } }`);
    const r = await c.execute(query);

    assert.deepEqual(r, {
      me: {
        __typename: 'Me',
        userId: '00000000-0000-0000-0000-000000000000',
        email: 'anonymous@',
        // userTier: 'BROKERAGE_UNSUBSCRIBED'
      },
    });
  });

  test('type things (mostly) work (RouteId is thought to be “unknown”)', async () => {
    const c = createClient();
    const query = graphql(`query Route($id: RouteId!) {
      route(id: $id) {
        __typename
        id
        name
      }
    }`);
    const r = await c.execute(query, { id: 'hey' });
    assert.deepEqual(r, { route: null });
  });

  // DONT RUN THIS IT WILL CREATE AN ACTUAL ORDER
  test.skip('more type things work', async () => {
    /*
    const c = createClient();
    const mutation = graphql(`mutation CreateOrder($order: CreateOrder!) {
      createOrder(order: $order)
    }`);
    const r = await c.execute(mutation, {
      order: {
        timeInForce: { instruction: 'GTC' },
        dir: 'fixme',
        market: 'fixme',
        quantity: 10,
        orderType: 'LIMIT',
      },
    });
    assert.deepEqual(r, { route: null });
    */
  });

  test('fragments', async () => {
    const c = createClient();

    const f = graphql(`fragment Fields on Venue {
      id
      name
    }`);
    const q = graphql(
      `query Venues {
      venues {
        __typename
        ...Fields
      }
    }`,
      [f],
    );
    const r = await c.execute(q);
    assert.equal(r.venues.length, 5);
    assert.deepEqual(r.venues[0], {
      __typename: 'Venue',
      name: 'CME',
      id: '378aa416-97d3-54ab-9fe4-c09be5a4cb47',
    });
  });

  test('mutations: with known object return types', async () => {
    const c = createClient();
    // TODO: automate these type assertions

    // create
    const m1 = graphql(`mutation M {
      createApiKey {
        __typename
        apiKey
        apiSecret
      }
    }`);
    const r1 = await c.execute(m1);
    assert.equal(r1.createApiKey.__typename, 'ApiKey');

    // cleanup / delete
    const m2 = graphql(`mutation RemoveApiKey($apiKey: String!) {
      removeApiKey(apiKey: $apiKey)
    }`);
    const r2 = await c.execute(m2, { apiKey: r1.createApiKey.apiKey });
    assert.deepEqual(r2, { removeApiKey: true });
  });

  test('mutations: with no field selection return types', async () => {
    const c = createClient();
    // TODO: automate these type assertions

    // create
    const m1 = graphql(
      `mutation CreateOrder($order: CreateOrder!) { createOrder(order: $order) }`,
    );
    const r1 = await c.execute(m1, {
      order: {
        dir: 'sell',
        market: 'CME',
        quantity: '1',
        orderType: 'LIMIT',
        timeInForce: { instruction: 'GTD' },
      },
    });
    assert.equal(r1.createOrder, '');

    // cleanup / delete
    /*
    const m2 = graphql(`mutation RemoveApiKey($apiKey: String!) {
      removeApiKey(apiKey: $apiKey)
    }`);
    const r2 = await c.execute(m2, { apiKey: r1.createApiKey.apiKey });
    assert.deepEqual(r2, { removeApiKey: true });
    */
  });
});

/***
 * FIXME: this is getting an inferred type of with an unknown response value
 * TadaDocumentNode<{ createMmAlgo: unknown; }, { ...CreateMMAlgo }>;
 */
const g = graphql(`
mutation CreateMmAlgo($mmAlgo: CreateMMAlgo!) {
  createMmAlgo(mmAlgo: $mmAlgo)
}`);
g;
// const r = await createClient().execute(g, { mmAlgo: {} });
