import assert from 'node:assert/strict';
import { describe, test } from 'node:test';

import {
  __createClientWithProcessVars as createClient,
  graphql,
} from '../src/client.mjs';

describe('Client', () => {
  test('can query with types, even though we’re only using javascript', async () => {
    const c = createClient();
    const query = graphql(`query Me { me { __typename userId email } }`);
    const r = await c.execute(query);

    assert.deepEqual(Object.keys(r), ['me']);
    assert.deepEqual(Object.keys(r.me), ['__typename', 'userId', 'email']);
    assert.equal(r.me.__typename, 'Me');
    assert.equal(typeof r.me.userId, 'string');
    assert.equal(typeof r.me.email, 'string');
    /*
    assert.deepEqual(r, {
      me: {
        __typename: 'Me',
        userId: '00000000-0000-0000-0000-000000000000',
        email: 'anonymous@',
        // userTier: 'BROKERAGE_UNSUBSCRIBED'
      },
    });
    */
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

    // create
    const m1 = graphql(`mutation CreateApiKey {
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

  // SKIP becasue we don’t have a valid (test) environment to create orders
  test.skip('mutations: with no field selection return types', async () => {
    const c = createClient();

    // create
    const m1 = graphql(
      `mutation CreateOrder($order: CreateOrder!) { createOrder(order: $order) }`,
    );
    const r1 = await c.execute(m1, {
      order: {
        dir: 'sell',
        market: 'CME',
        quantity: '1',
        orderType: 'STOP_LOSS_LIMIT',
        timeInForce: { instruction: 'GTD' },
      },
    });
    console.log('created order?', r1);
    assert.equal(typeof r1.createOrder, 'string');

    // cleanup / delete
    const m2 = graphql(`mutation CancelOrder($orderId: OrderId!) {
      cancelOrder(orderId: $orderId)
    }`);
    const r2 = await c.execute(m2, { orderId: r1.createOrder });
    console.log('canceled order?', r2);
    assert.deepEqual(typeof r2.cancelOrder, 'string');
    assert.deepEqual(r2.cancelOrder, r1.createOrder);
  });
});
