/**
 */
import { initGraphQLTada } from 'gql.tada';
export { readFragment } from 'gql.tada';
/**
 * @typedef { import('./graphql-env.d.ts').introspection } introspection
 */

/**
 * @type {ReturnType<typeof initGraphQLTada<{
 *   introspection: introspection;
 *   scalars: {
 *     Date: string;
 *     DateTime: string;
 *     Decimal: string;
 *     AccountId: string;
 *     UserId: string;
 *     OrderId: string;
 *     MarketId: string;
 *     VenueId: string;
 *     RouteId: string;
 *     ProductId: string;
 *     ComponentId: string;
 *     FillId: string;
 *     Dir: 'buy' | 'sell';
 *     Str: string;
 *     OrderSource: string;
 *   }
 * }>>}
 **/
export const graphql = initGraphQLTada();
