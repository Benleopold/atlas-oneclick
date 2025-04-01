// atlas-github-runner.js

import 'dotenv/config';
import { execSync } from 'child_process';
import fs from 'fs';

const repo = process.env.GITHUB_REPO;
const branch = process.env.GITHUB_BRANCH || 'main';
const token = process.env.GITHUB_PAT;

if (!repo || !token) {
  console.error('Missing GITHUB_REPO or GITHUB_PAT. Check .env file.');
  process.exit(1);
}

const repoUrl = `https://${token}@github.com/${repo}.git`;

try {
  // Clone if not already present
  if (!fs.existsSync('./repo')) {
    console.log(`Cloning ${repo}...`);
    execSync(`git clone --single-branch --branch ${branch} ${repoUrl} repo`, { stdio: 'inherit' });
  }

  // Pull latest changes
  console.log('Pulling latest changes...');
  execSync(`cd repo && git pull origin ${branch}`, { stdio: 'inherit' });

  // Simulated agent commit
  const timestamp = new Date().toISOString();
  fs.writeFileSync('./repo/atlas-heartbeat.txt', `Last update: ${timestamp}\n`);

  console.log('Committing update...');
  execSync(
    `cd repo && git config user.email "atlas@autonomous.ai" && git config user.name "Atlas AI" && git add . && git commit -m "Atlas update at ${timestamp}" && git push origin ${branch}`,
    { stdio: 'inherit' }
  );

  console.log('Atlas GitHub Runner has completed a full update cycle.');
} catch (error) {
  console.error('Runner failed:', error.message);
}