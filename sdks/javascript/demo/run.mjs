import * as sdk from './output.mjs';

console.log('version', await sdk.version());
console.log('me', await sdk.me(['__typename', 'userId', 'email']));

const p = await sdk.products(['kind', 'id', 'name'], ['hey']);
const a = await sdk.listApiKeys([
  '__typename',
  'apiKey',
  'created',
  'subject',
  'apiSecret',
]);

console.log('products', p);
console.log('api keys', a);
