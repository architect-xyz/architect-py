import type { introspection } from '../src/graphql-env.d.ts';

declare module 'gql.tada' {
  interface setupSchema {
    introspection: introspection;
    scalars: {
      DateTime: string;
      Decimal: string;
      AccountId: string;
      UserId: string;
      OrderId: string;
      MarketId: string;
      VenueId: string;
      RouteId: string;
      ProductId: string;
      Dir: 'buy' | 'sell';
      Str: string;
      OrderSource: string;
    };
  }
}
