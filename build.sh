#!/usr/bin/env bash
# 把仓库根目录的 Markdown 与 assets 镜像到 docs/ 供 MkDocs 构建。
# 用法:
#   ./build.sh          # 构建到 site/
#   ./build.sh serve    # 本地预览 (http://127.0.0.1:8000)
set -euo pipefail
cd "$(dirname "$0")"

# 目标镜像目录
rm -rf docs
mkdir -p docs

# 复制内容目录与资源、根级 Markdown（排除 Git/站点相关目录）
for item in 00-preface 01-architecture 02-build 03-run 04-governance \
            05-optimization 06-case-study 07-conclusion assets \
            README.md README_EN.md 2026-agent-survey-report.md; do
  if [ -e "$item" ]; then
    cp -R "$item" docs/
  fi
done

if [ "${1:-build}" = "serve" ]; then
  exec python3 -m mkdocs serve
else
  exec python3 -m mkdocs build --strict
fi
