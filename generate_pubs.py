name: Auto Update Publications

on:
  push:
    paths:
      - 'publications.bib'     # 当bib文件更新时触发
      - 'generate_pubs.py'     # 当脚本更新时触发
  workflow_dispatch:           # 允许在网页端手动点击运行

permissions:
  contents: write              # 允许机器人提交代码

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install bibtexparser
          
      - name: Run generation script
        run: python generate_pubs.py
        
      - name: Commit and push changes
        run: |
          git config --global user.name 'github-actions[bot]'
          git config --global user.email 'github-actions[bot]@users.noreply.github.com'
          git add index.md
          # 如果文件有变化则提交并推送，否则跳过
          git diff --quiet && git diff --staged --quiet || (git commit -m "docs: auto-update publications list from bibtex" && git push)
