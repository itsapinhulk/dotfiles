#!/usr/bin/env bash

set -euo pipefail

# ── resolve repo root from script location ────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$(realpath "${BASH_SOURCE[0]}")")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "$REPO_ROOT"

# ── helpers ───────────────────────────────────────────────────────────────────
die()  { echo "❌  $*" >&2; exit 1; }
warn() { echo "⚠️  $*" >&2; }
info() { echo "ℹ️  $*"; }
ok()   { echo "✅  $*"; }

usage() {
cat <<EOF
Usage: $0 [--ghcr-path IMAGE] [--docker-hub-path IMAGE] [--skip-confirm] [-h]

Build once and push to one or both registries. At least one path is required.
Each registry receives two tags:  :latest  and  :YYYYMMDD-hhmm-<git-sha>

Registries are skipped (with a warning) if the required token env var is not set

Options:
  --ghcr-path         IMAGE   Image path on ghcr.io    (default: itsapinhulk/devcontainer)
  --docker-hub-path   IMAGE   Image path on Docker Hub  (default: itsapinhulk/devcontainer)
  --skip-confirm      Skip interactive confirmation prompt
  -h, --help          Show this help

Examples:
  $0 --ghcr-path myuser/devcontainer --docker-hub-path myorg/devcontainer
  $0 --skip-confirm   # Push to default repos, without confirmation
EOF
}

# ── argument parsing ──────────────────────────────────────────────────────────
SKIP_CONFIRM=false
GHCR_ROOT="ghcr.io"
GHCR_PATH="itsapinhulk/devcontainer"
DOCKERHUB_ROOT="docker.io"
DOCKERHUB_PATH="itsapinhulk/devcontainer"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip-confirm)       SKIP_CONFIRM=true ;;
    --ghcr-path)          GHCR_PATH="$2"; shift ;;
    --docker-hub-path)    DOCKERHUB_PATH="$2";  shift ;;
    -h|--help)            usage; exit 0 ;;
    *) die "Unknown argument: $1  (run with -h for help)" ;;
  esac
  shift
done

GHCR_FULL_URL="${GHCR_ROOT}/${GHCR_PATH}"
DOCKERHUB_FULL_URL="${DOCKERHUB_ROOT}/${DOCKERHUB_PATH}"

# ── pre-flight: must run from inside a git repo ───────────────────────────────
git rev-parse --git-dir &>/dev/null || die "Not inside a git repository."

# ── pre-flight: refuse if there are uncommitted changes ──────────────────────
if ! git diff --quiet || ! git diff --cached --quiet; then
  die "Uncommitted changes detected. Commit or stash them before building.

$(git status --short)"
fi

ok "Working tree is clean."

# ── gather git metadata ───────────────────────────────────────────────────────
GIT_SHA=$(git rev-parse HEAD)
GIT_SHA_SHORT=$(git rev-parse --short HEAD)
BUILD_DATE=$(date -u +"%Y%m%d-%H%M")

RAW_REMOTE=$(git remote get-url origin 2>/dev/null) \
  || die "No 'origin' remote found."

if [[ "$RAW_REMOTE" =~ ^git@ ]]; then
  REPO_URL=$(echo "$RAW_REMOTE" \
    | sed 's|git@\([^:]*\):\(.*\)|https://\1/\2|' \
    | sed 's|\.git$||')
else
  REPO_URL="${RAW_REMOTE%.git}"
fi
info "Repo URL : $REPO_URL"

# ── resolve tags and check tokens ─────────────────────────────────────────────
# registry_check <label> <path> <token_var>
# Populates BUILD_TAGS and PUSH_REGISTRIES; warns and skips on missing path/token.
DATED_SUFFIX="${BUILD_DATE}-${GIT_SHA_SHORT}"
BUILD_TAGS=()
declare -A PUSH_REGISTRIES   # label → "dated_tag latest_tag"

registry_check() {
  local label="$1" path="$2" token_var="$3"

  if [[ -z "$path" ]]; then
    warn "$label path not provided — skipping."
    return
  fi

  if [[ -z "${!token_var:-}" ]]; then
    warn "\$$token_var not set — skipping push to $label."
    return
  fi

  local dated="${path}:${DATED_SUFFIX}"
  local latest="${path}:latest"
  BUILD_TAGS+=("$dated" "$latest")
  PUSH_REGISTRIES["$label"]="$dated $latest"
}

registry_check "ghcr.io"    "$GHCR_FULL_URL"        "GHCR_TOKEN"
registry_check "Docker Hub" "$DOCKERHUB_FULL_URL"   "DOCKERHUB_TOKEN"

[[ ${#BUILD_TAGS[@]} -eq 0 ]] \
  && die "Nothing to build — all registries were skipped."

# ── confirm ───────────────────────────────────────────────────────────────────
echo ""
echo "  Tags to build & push:"
for tag in "${BUILD_TAGS[@]}"; do echo "    $tag"; done
echo "  Commit : $GIT_SHA"
echo "  Date   : $BUILD_DATE"
echo ""

if [[ "$SKIP_CONFIRM" == false ]]; then
  read -rp "Proceed with build and push? [y/N] " answer
  [[ "$answer" =~ ^[Yy]$ ]] || { echo "Aborted."; exit 0; }
fi

# ── build (once, all tags) ────────────────────────────────────────────────────
info "Building image ..."
TAG_ARGS=()
for tag in "${BUILD_TAGS[@]}"; do TAG_ARGS+=(--tag "$tag"); done

docker build \
  --build-arg "REPO_URL=${REPO_URL}" \
  --build-arg "GIT_SHA=${GIT_SHA}"   \
  --build-arg "BUILD_DATE=${BUILD_DATE}" \
  "${TAG_ARGS[@]}" \
  .

ok "Build complete."

# ── push ──────────────────────────────────────────────────────────────────────
push_registry() {
  local label="$1"; shift; local tags=("$@")
  info "Pushing to $label…"
  for tag in "${tags[@]}"; do
    info "  $tag"
    docker push "$tag"
  done
}

for label in "${!PUSH_REGISTRIES[@]}"; do
  # shellcheck disable=SC2086
  read -ra tags <<< "${PUSH_REGISTRIES[$label]}"
  push_registry "$label" "${tags[@]}"
done

ok "Done."
