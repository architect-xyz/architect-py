import assert from 'node:assert/strict';
import { describe, test } from 'node:test';

describe('test runner starts up', () => {
  test('okay', () => {
    assert.equal(true, true);
  });
});
