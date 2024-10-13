import * as sdk from './output.mjs';

console.log('version\n', await sdk.version());
console.log('me\n', await sdk.me(['__typename', 'userId', 'email']), '\n');

console.log('route\n', await sdk.route(['id', 'name'], 'Id'), '\n');
console.log('products\n', await sdk.products(['id', 'name'], ['BTC']), '\n');
const a = await sdk.listApiKeys([
  '__typename',
  'apiKey',
  'created',
  'subject',
  'apiSecret',
]);
console.log('apiKeys\n', a, '\n');
