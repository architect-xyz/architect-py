
import * as sdk from './output.mjs';

console.log('version', await sdk.version());
console.log('me', await sdk.me(['__typename', 'userId', 'email']));


