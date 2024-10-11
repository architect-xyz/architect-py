import * as sdk from './output.mjs';

console.log('version', await sdk.version());
console.log('me', await sdk.me(['__typename', 'userId', 'email']));

const c = await sdk.products(['kind', 'id', 'name'], ['hey']);
const m = await sdk.me(['userId', 'email']);
