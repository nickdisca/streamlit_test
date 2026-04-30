#!/bin/bash

WORKFLOW_FILE="$1"
echo "Working on workflow file: $WORKFLOW_FILE" # can use 'gh workflow list' in terminal to inspect names to use

# Get all run IDs
run_ids=$(gh run list --limit 500 --workflow "$WORKFLOW_FILE" --json databaseId -q '.[].databaseId')

# Exit if no runs found
if [[ -z "$run_ids" ]]; then
  echo "No workflow runs found."
  exit 0
fi

# Loop through each run ID
for id in $run_ids; do
  echo "Processing run ID: $id"

  # Delete the run
  gh run delete "$id"
done