/***
 * Pre-release script
 *
 * Overall process:
 *
 * Validation stage
 * * Validate environment
 * * Validate static analysis
 * * Validate quality assertions
 *
 * Build stage
 * * Build docs
 * * ...
 *
 * Release stage
 * * Bump release version (major, minor, patch)
 * * Automate release message
 * * Tag commit as release version
 * * Push tag to github
 * * Push release to npm
 */
import { $ } from 'zx';

function fail(message) {
  console.log(message);
  process.exit(1);
}

async function validateEnvironment() {
  const onMain = (await $`git rev-parse --abbrev-ref HEAD`) === 'main';
  const remoteHead =
    await $`git fetch origin main && git rev-parse origin/main`;
  const localHead = await $`git rev-parse HEAD`;
  const upToDate = remoteHead === localHead;
  if (onMain === false) {
    fail('Must be on main to release');
  } else if (upToDate === false) {
    fail('local main is not up to date with origin/main');
  } else {
    return true;
  }
}

function validateAnalysis() {
  // validate types
  // validate code formatting
  return Promise.all([
    $`npm run typecheck`,
    // TODO biome doesn’t support this option like prettier...probably fine
    // $`biome format --check`
  ]).catch((err) => {
    if (err.stdout.includes('tsc --noEmit')) {
      fail('Types are not valid. Ensure `tsc --noEmit` passes cleanly.');
    } else {
      throw err;
    }
  });
}

function validateQuality() {
  // ensure tests pass
}

// Validation stage
try {
  await Promise.all([
    validateEnvironment(),
    validateAnalysis(),
    validateQuality(),
  ]);
  console.log('Release validated');
} catch (err) {
  console.error('Error validating release', err.message);
}

// Build
