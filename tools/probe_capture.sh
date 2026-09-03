#!/usr/bin/env bash
set -euo pipefail

echo "== video devices =="
v4l2-ctl --list-devices || true
echo

for node in /dev/video*; do
  [[ -e "$node" ]] || continue
  echo "== $node =="
  v4l2-ctl --device "$node" --all 2>/dev/null | sed -n '1,80p' || true
  echo "-- formats --"
  v4l2-ctl --device "$node" --list-formats-ext 2>/dev/null || true
  echo
done

echo "== media topology =="
for media in /dev/media*; do
  [[ -e "$media" ]] || continue
  echo "-- $media --"
  media-ctl -d "$media" -p 2>/dev/null | sed -n '1,180p' || true
done
