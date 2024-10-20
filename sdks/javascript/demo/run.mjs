import { create as createClient } from '../src/index.mjs';
const config = {
  host: /** @type {string} */ (process.env.ARCHITECT_HOST),
  apiKey: /** @type {string} */ (process.env.ARCHITECT_API_KEY),
  apiSecret: /** @type {string} */ (process.env.ARCHITECT_API_SECRET),
};
const sdk = await createClient(config);

// Queries
const v = await sdk.version();
console.log('version\n', v, '\n');
const m = await sdk.me(['__typename', 'userId', 'email']);
console.log('me\n', m, '\n');

const r = await sdk.route(['id', 'name'], 'Id');
console.log('route\n', r, '\n');
console.log('products\n', await sdk.products(['id', 'name'], ['BTC']), '\n');
const a = await sdk.listApiKeys([
  '__typename',
  'apiKey',
  'created',
  'subject',
  'apiSecret',
]);
console.log('apiKeys\n', a, '\n');

// Mutations
/* 
const key = await sdk.createApiKey([
  'apiSecret',
  'apiKey',
  'subject',
  'created',
]);
console.log('api key', key);
/*
api key {
  __typename: 'ApiKey',
  apiSecret: '<redacted>',
  apiKey: '<redacted>',
  subject: 'anonymous@',
  created: '2024-10-13T14:52:43.835195612Z'
}
*/
/*
const deleteKey = await sdk.removeApiKey(key.apiKey);
console.log('delete key?', deleteKey);
console.log(
  'apiKeys\n',
  await sdk.listApiKeys([
    '__typename',
    'apiKey',
    'created',
    'subject',
    'apiSecret',
  ]),
  '\n',
);

try {
  const h = await sdk.createTelegramApiKey(
    ['apiKey', 'created', 'subject', 'apiSecret'],
    'heyo',
  );
  console.log('telegram', h);
} catch (e) {
  console.log(
    'Telegram failed like expected',
    e && typeof e === 'object' && 'message' in e ? e.message : e,
  );
}
*/
