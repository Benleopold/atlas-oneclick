import 'dotenv/config';
import { execSync } from 'child_process';
import fs from 'fs';

const repo = process.env.ATLAS_REPO;
const branch = process.env.ATLAS_BRANCH || 'main';
const token = process.env.ATLAS_PAT;

if (!repo || !token) {
  console.error('Missing ATLAS_REPO or ATLAS_PAT. Check GitHub secrets.');
  process.exit(1);
}

const repoUrl = `https://${token}@github.com/${repo}.git`;

try {
  // Clone if not already present
  if (!fs.existsSync('./repo')) {
    console.log(`Cloning ${repoUrl}`);
    execSync(`git clone --single-branch --branch ${branch} ${repoUrl} repo`, { stdio: 'inherit' });
  }

  // Pull latest changes
  console.log('Pulling latest changes...');
  execSync(`cd repo && git pull origin ${branch}`, { stdio: 'inherit' });

  // Simulate update
  const timestamp = new Date().toISOString();
  fs.writeFileSync('./repo/atlas-heartbeat.txt', `Last update: ${timestamp}\n`);

  // Commit and push update
  console.log('Committing update...');
  execSync(
    `cd repo && git config user.email "atlas@autonomous.ai" && git config user.name "Atlas AI" && git add . && git commit -m "Atlas update at ${timestamp}" && git push origin ${branch}`,
    { stdio: 'inherit' }
  );

  console.log('Atlas GitHub Runner has completed a full update cycle.');
} catch (error) {
  console.error('Runner failed:', error.message);
}