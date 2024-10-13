import * as sdk from './output.mjs';

// console.log('version', await sdk.version());
// console.log('me', await sdk.me(['__typename', 'userId', 'email']));

console.log('route', await sdk.route(['id', 'name'], 'Id'));
// console.log('products', await sdk.products(['id', 'name'], ['BTC']));
/*
const a = await sdk.listApiKeys([
  '__typename',
  'apiKey',
  'created',
  'subject',
  'apiSecret',
]);
//console.log('api keys', a);
*/

