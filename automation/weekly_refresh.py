name: Weekly Data Refresh

on:
  schedule:
    - cron: "0 3 * * 1"   # Every Monday at 3 AM UTC
  workflow_dispatch:

jobs:
  refresh:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v4
      # TODO: later: add steps to run scraper + NLP pipeline
