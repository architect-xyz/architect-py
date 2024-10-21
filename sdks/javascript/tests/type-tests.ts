import { graphql } from '../src/client.mjs';
import { __createClientWithProcessVars } from '../src/debugging.mjs';

const c = __createClientWithProcessVars();

/**
 * Basic type assertion helpers.
 * We want to ensure our library types maintain great type hinting support
 * */
type Expect<T extends true> = T;
type Equal<X, Y> = (<T>() => T extends X ? 1 : 2) extends <T>() => T extends Y
  ? 1
  : 2
  ? true
  : false;

// TEST: query that returns a primitive resolves correctly
{
  const r = await c.execute(graphql(`query Version { version }`));
  type t = Expect<Equal<typeof r, { version: string }>>;
}

// TEST: basic queries resolve correctly
{
  const query = graphql(`query Me { me { __typename userId email } }`);
  const r1 = await c.execute(query);

  type t1 = Expect<
    Equal<
      typeof r1,
      { me: { __typename: 'Me'; userId: string; email: string } }
    >
  >;

  const r2 = await c.execute(graphql(`query Me { me { __typename userId } }`));
  type t2 = Expect<
    Equal<typeof r2, { me: { __typename: 'Me'; userId: string } }>
  >;

  // @ts-expect-error negative test to ensure that this doesn’t handle
  type t3 = Expect<Equal<typeof r1, { me: { __typename: 'Me' } }>>;
}

// TEST: list queries resolve correctly
{
  const query = graphql(`query Venues { venues { __typename id name } }`);
  const r1 = await c.execute(query);

  type t1 = Expect<
    Equal<
      typeof r1,
      { venues: { __typename: 'Venue'; id: string; name: string }[] }
    >
  >;
  type t2 = Expect<
    Equal<typeof r1.venues, { __typename: 'Venue'; id: string; name: string }[]>
  >;
}

// TEST: mutations with fields and no args resolve correctly
{
  const mut = graphql(`
    mutation CreateApiKey {
      createApiKey { __typename apiKey apiSecret }
    }`);
  const r1 = await c.execute(mut);

  type t1 = Expect<
    Equal<
      typeof r1,
      {
        createApiKey: {
          __typename: 'ApiKey';
          apiKey: string;
          apiSecret: string;
        };
      }
    >
  >;

  // FIXME: this should error
  const r2 = await c.execute(mut, { fail: true });
}

// TEST: mutations with fields and args resolves correctly
{
  const g = graphql(`
mutation CreateMmAlgo($mmAlgo: CreateMMAlgo!) {
  createMmAlgo(mmAlgo: $mmAlgo)
}`);
  const r = await c.execute(g, {
    mmAlgo: {
      name: 'My Algo',
      market: 'CME',
      buyQuantity: '1',
      maxPosition: '3',
      minPosition: '0',
      refDistFrac: '0.5',
      positionTilt: '0.5',
      sellQuantity: '0.25',
      maxImproveBbo: '0.25',
      toleranceFrac: '0.25',
      referencePrice: 'BID_ASK',
      fillLockoutMs: 1000,
      orderLockoutMs: 1000,
      rejectLockoutMs: 1000,
    },
  });

  type t1 = Expect<Equal<typeof r, { createMmAlgo: string }>>;
  // @ts-expect-error just making sure...
  type t2 = Expect<Equal<typeof r, { createMmAlgo: number }>>;

  // FIXME: this should error, args are required
  const r2 = await c.execute(g);
}
