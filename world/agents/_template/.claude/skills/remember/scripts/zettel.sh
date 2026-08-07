#!/bin/bash

# Zettelkasten System — per-agent memory
# Each thought is a zettel stored as JSONL line in short_term
# When overflow, each line becomes permanent zettel file

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
SHORT_TERM="$AGENT_ROOT/memory/short_term_memory.jsonl"
ZETTEL_DIR="$AGENT_ROOT/memory/zettels"
ARCHIVE_DIR="$AGENT_ROOT/memory/archives"

mkdir -p "$ZETTEL_DIR" "$ARCHIVE_DIR"

generate_id() {
  echo "$(date -u +%Y%m%d%H%M%S)-$(openssl rand -hex 2)"
}

ACTION="${1:-help}"

case "$ACTION" in
  add)
    TITLE="${2:-}"
    CONTENT="${3:-}"
    TAGS="${4:-}"
    LINKS="${5:-}"

    if [[ -z "$TITLE" || -z "$CONTENT" ]]; then
      echo "Usage: zettel.sh add \"title\" \"content\" [\"tags\"] [\"links\"]" >&2
      exit 1
    fi

    ID=$(generate_id)
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    if [[ -n "$TAGS" ]]; then
      TAGS_JSON=$(printf '%s' "$TAGS" | jq -R 'split(",")' )
    else
      TAGS_JSON="[]"
    fi

    if [[ -n "$LINKS" ]]; then
      LINKS_JSON=$(printf '%s' "$LINKS" | jq -R 'split(",") | map({to: ., type: "related"})')
    else
      LINKS_JSON="[]"
    fi

    ZETTEL=$(jq -cn \
      --arg id "$ID" \
      --arg title "$TITLE" \
      --arg content "$CONTENT" \
      --arg created "$TIMESTAMP" \
      --argjson tags "$TAGS_JSON" \
      --argjson links "$LINKS_JSON" \
      '{
        id: $id,
        title: $title,
        content: $content,
        tags: $tags,
        links: $links,
        created_at: $created,
        status: "fleeting"
      }')

    echo "$ZETTEL" >> "$SHORT_TERM"
    echo "$ID"
    ;;

  count)
    if [[ -f "$SHORT_TERM" ]]; then
      wc -l < "$SHORT_TERM" | tr -d ' '
    else
      echo "0"
    fi
    ;;

  list)
    LIMIT="${2:-10}"
    if [[ -f "$SHORT_TERM" ]]; then
      tail -n "$LIMIT" "$SHORT_TERM" | jq -r '[.id, .title] | @tsv'
    fi
    ;;

  get)
    ID="${2:-}"
    if [[ -z "$ID" ]]; then
      echo "Usage: zettel.sh get <id>" >&2
      exit 1
    fi

    if [[ -f "$SHORT_TERM" ]]; then
      RESULT=$(grep "\"id\":\"$ID\"" "$SHORT_TERM" 2>/dev/null || true)
      if [[ -n "$RESULT" ]]; then
        echo "$RESULT"
        exit 0
      fi
    fi

    if [[ -f "$ZETTEL_DIR/$ID.json" ]]; then
      cat "$ZETTEL_DIR/$ID.json"
      exit 0
    fi

    echo "Zettel not found: $ID" >&2
    exit 1
    ;;

  search)
    QUERY="${2:-}"

    # Empty query = list all zettels (short_term + permanent)
    if [[ -z "$QUERY" ]]; then
      if [[ -f "$SHORT_TERM" ]]; then
        jq -r '[.id, .title] | @tsv' "$SHORT_TERM" 2>/dev/null || true
      fi
      find "$ZETTEL_DIR" -name "*.json" 2>/dev/null | while read -r f; do
        jq -r '[.id, .title] | @tsv' "$f" 2>/dev/null
      done || true
      exit 0
    fi

    if [[ -f "$SHORT_TERM" ]]; then
      grep -i "$QUERY" "$SHORT_TERM" 2>/dev/null | jq -r '[.id, .title] | @tsv' || true
    fi

    find "$ZETTEL_DIR" -name "*.json" 2>/dev/null | while read -r f; do
      if grep -qil "$QUERY" "$f" 2>/dev/null; then
        jq -r '[.id, .title] | @tsv' "$f"
      fi
    done || true
    ;;

  link)
    FROM_ID="${2:-}"
    TO_ID="${3:-}"
    LINK_TYPE="${4:-related}"

    if [[ -z "$FROM_ID" || -z "$TO_ID" ]]; then
      echo "Usage: zettel.sh link <from_id> <to_id> [type]" >&2
      exit 1
    fi

    if [[ -f "$SHORT_TERM" ]]; then
      TEMP=$(mktemp)
      while IFS= read -r line; do
        if echo "$line" | grep -q "\"id\":\"$FROM_ID\""; then
          echo "$line" | jq -c --arg to "$TO_ID" --arg type "$LINK_TYPE" \
            '.links += [{to: $to, type: $type}]'
        else
          echo "$line"
        fi
      done < "$SHORT_TERM" > "$TEMP"
      mv "$TEMP" "$SHORT_TERM"
    fi

    if [[ -f "$ZETTEL_DIR/$FROM_ID.json" ]]; then
      jq --arg to "$TO_ID" --arg type "$LINK_TYPE" \
        '.links += [{to: $to, type: $type}]' \
        "$ZETTEL_DIR/$FROM_ID.json" > "$ZETTEL_DIR/$FROM_ID.json.tmp"
      mv "$ZETTEL_DIR/$FROM_ID.json.tmp" "$ZETTEL_DIR/$FROM_ID.json"
    fi

    echo "Linked $FROM_ID -> $TO_ID ($LINK_TYPE)"
    ;;

  factorize)
    if [[ ! -f "$SHORT_TERM" ]]; then
      echo "No short term memory to factorize"
      exit 0
    fi

    COUNT=$(wc -l < "$SHORT_TERM" | tr -d ' ')
    if [[ "$COUNT" -eq 0 ]]; then
      echo "Short term memory empty"
      exit 0
    fi

    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    cp "$SHORT_TERM" "$ARCHIVE_DIR/${TIMESTAMP}_batch.jsonl"

    FACTORIZED=0
    while IFS= read -r line; do
      ID=$(echo "$line" | jq -r '.id')
      echo "$line" | jq '.status = "permanent"' > "$ZETTEL_DIR/$ID.json"
      FACTORIZED=$((FACTORIZED + 1))
    done < "$SHORT_TERM"

    > "$SHORT_TERM"
    echo "Factorized $FACTORIZED zettels to permanent storage"
    ;;

  stats)
    SHORT_COUNT=0
    PERM_COUNT=0

    if [[ -f "$SHORT_TERM" ]]; then
      SHORT_COUNT=$(wc -l < "$SHORT_TERM" | tr -d ' ')
    fi

    PERM_COUNT=$(find "$ZETTEL_DIR" -name "*.json" 2>/dev/null | wc -l | tr -d ' ')

    echo "Short term: $SHORT_COUNT"
    echo "Permanent: $PERM_COUNT"
    echo "Total: $((SHORT_COUNT + PERM_COUNT))"
    ;;

  help|*)
    cat << 'EOF'
Zettelkasten — Agent Memory System

Usage:
  zettel.sh add "title" "content" ["tags"] ["links"]  - Add thought
  zettel.sh count                                      - Count in short term
  zettel.sh list [n]                                   - List recent
  zettel.sh get <id>                                   - Get zettel
  zettel.sh search <query>                             - Search
  zettel.sh link <from> <to> [type]                    - Link zettels
  zettel.sh factorize                                  - Short term → permanent
  zettel.sh stats                                      - Show stats
EOF
    ;;
esac
