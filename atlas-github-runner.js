name: Atlas GitHub Runner

on:
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    env:
      ATLAS_PAT: ${{ secrets.ATLAS_PAT }}
      ATLAS_REPO: ${{ secrets.ATLAS_REPO }}
      ATLAS_BRANCH: ${{ secrets.ATLAS_BRANCH }}
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Install Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm install

      - name: Run Atlas GitHub Runner
        run: node runner/atlas-github-runner.js