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
import { execSync } from 'child_process';

function validateEnvironment() {
  // validate releasing from `main` branch
  // validate synced with remote/HEAD
}
function validateAnalysis() {
  // validate types
  // validate code formatting
  const r = execSync('npm run typecheck', {
    cwd: process.cwd(),
  });
  console.log(r.toString('utf8'));
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
  console.error('Error validating release');
}

// Build
