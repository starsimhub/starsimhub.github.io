#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
npm install
npx eleventy --serve --port=8080
