#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<USAGE
Usage: $(basename "$0") <github-username>/<repository> [branch]

Environment variables:
  GITHUB_PAT   Personal access token with repo permissions (required)
  REMOTE_NAME  Git remote name to configure (default: origin)

Example:
  GITHUB_PAT=ghp_123 ./scripts/push_with_pat.sh areebh-dotcom/Customer-Support main
USAGE
}

if [[ ${1:-} == "-h" || ${1:-} == "--help" ]]; then
  usage
  exit 0
fi

if [[ $# -lt 1 || $# -gt 2 ]]; then
  usage
  exit 1
fi

: "${GITHUB_PAT:?GITHUB_PAT must be set to a GitHub personal access token}"

REPO_SLUG="$1"
BRANCH="${2:-main}"
REMOTE_NAME="${REMOTE_NAME:-origin}"

REMOTE_URL="https://${GITHUB_PAT}@github.com/${REPO_SLUG}.git"

echo "Configuring remote '${REMOTE_NAME}' for https://github.com/${REPO_SLUG}.git"
if git remote get-url "${REMOTE_NAME}" >/dev/null 2>&1; then
  git remote set-url "${REMOTE_NAME}" "${REMOTE_URL}"
else
  git remote add "${REMOTE_NAME}" "${REMOTE_URL}"
fi

echo "Pushing branch '${BRANCH}' to '${REMOTE_NAME}'"
git push -u "${REMOTE_NAME}" "${BRANCH}"
