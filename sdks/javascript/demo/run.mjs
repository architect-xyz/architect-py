import * as sdk from './output.mjs';

const v = await sdk.version();
console.log('version\n', v, '\n');
const m = await sdk.me(['__typename', 'userId', 'email']);
console.log('me\n', m, '\n');

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
