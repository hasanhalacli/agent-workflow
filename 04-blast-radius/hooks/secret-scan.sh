#!/usr/bin/env bash
# Claude Code PreToolUse hook: blocks Write/Edit containing secret patterns.
# Wire it via settings.example.json in this directory.
input=$(cat)
content=$(echo "$input" | jq -r '.tool_input.content // .tool_input.new_string // ""')

if echo "$content" | grep -qE 'sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{36}|AKIA[0-9A-Z]{16}|-----BEGIN.*PRIVATE'; then
  echo "Blocked: content matches a credential pattern. Use an env var." >&2
  exit 2   # exit 2 = block the action; stderr is fed back to the agent
fi
exit 0
