# 白育航 — 个人学术主页

本仓库是我的个人学术主页源码，通过 GitHub Pages 部署在
**[yuhang-bai.github.io](https://yuhang-bai.github.io/)**。

整个网站是**单页静态页面**，其中的论文列表和合作者列表都由一个 BibTeX 文件自动生成。
**没有任何前端框架、构建工具或第三方依赖**——只用到 Python 标准库和一个自包含的
`index.html`。改一改 `publications.bib`、推送上去，网站就会自动重建。

---

## 功能特性

- **论文信息单一数据源**：所有论文都写在 `publications.bib` 里。构建时由一个自带的
  BibTeX 解析器读取（不依赖 `bibtexparser`）。
- **自动分类**：根据条目类型和字段，自动归入 **Preprint（预印本）**、
  **Journal（期刊）**、**Conference（会议）** 三类。
- **智能排序**：按年份从新到旧排列；在期刊一栏中，标记为 *Submitted*（投稿中）的论文
  会自动置顶。
- **作者高亮**：在任意作者列表中出现我的名字时，都会自动**加粗**（匹配时忽略重音符号
  和作者顺序）。
- **合作者去重统计**：自动生成带合作次数的合作者列表。同一篇论文即使同时以预印本、
  期刊、会议三个版本出现，也只**计为一次**——通过「作者集合 + 归一化标题」来判定是否同
  一篇（去掉停用词、折叠重音、还原复数）。
- **可折叠摘要**：带有 `abstract` 字段的条目会生成一个点击展开的 `<details>` 摘要块。
- **`Submitted` 徽章**：`note = {Submitted}` 的条目会显示「投稿中」标记。
- **标题超链接**：带 `url` 字段的条目，标题会直接链接到论文。
- **LaTeX 公式**：标题和摘要中的数学公式由 MathJax 渲染。
- **本地实时预览**：保存文件后自动重建，刷新浏览器即可看到效果。
- **CI 自动构建**：通过 GitHub Actions，推送 `.bib` 改动后自动重新生成并提交
  `index.html`，无需手动构建。
- **SEO 友好**：canonical 链接、Open Graph + Twitter Card 标签、JSON-LD
  `schema.org/Person` 结构化数据、`sitemap.xml`、`robots.txt`，以及 Google 站点验证。
- **响应式、零依赖样式**：内联 CSS，衬线正文字体（STIX Two Text / IBM Plex Sans），
  在手机上也清晰易读。

---

## 工作原理

```
publications.bib  ──►  build_site.py  ──►  index.html
                                            （写入 HTML 标记注释之间）
```

`build_site.py` 解析 BibTeX 文件，并将生成的 HTML **原地注入** `index.html`，
只替换标记注释之间的内容：

| 标记对 | 写入的内容 |
| --- | --- |
| `<!-- PUBS_START -->` … `<!-- PUBS_END -->`     | 完整的论文列表（按类别分组） |
| `<!-- COLLAB_START -->` … `<!-- COLLAB_END -->` | 带次数的合作者列表 |

标记之外的所有内容——页眉、个人简介、样式、链接——都是在 `index.html` 中手动编辑的，
脚本不会改动。

### 分类规则

| BibTeX 条目 | 类别 |
| --- | --- |
| `@unpublished`，或 `journal`/`note` 含 "arxiv" | **Preprint** |
| `@article`                                     | **Journal**  |
| `@inproceedings` / `@conference`               | **Conference** |

---

## 目录结构

```
.
├── index.html                  # 网页本体（手写外壳 + 自动生成区域）
├── publications.bib            # 所有论文的单一数据源
├── build_site.py               # BibTeX → HTML 生成脚本（仅用标准库）
├── preview.py                  # 本地实时预览服务器
├── preview.bat / preview.ps1   # preview.py 的 Windows 启动脚本
├── sitemap.xml                 # SEO 站点地图
├── robots.txt                  # 爬虫规则
├── .nojekyll                   # 告诉 GitHub Pages 跳过 Jekyll 处理
├── google…​.html               # Google Search Console 站点验证文件
└── .github/workflows/
    └── update_pubs.yml         # CI：.bib 改动时重建并提交 index.html
```

---

## 使用方法

### 添加或修改论文

1. 在 `publications.bib` 中添加一个条目，例如：

   ```bibtex
   @article{bai2026example,
     title   = {A Wonderful Theorem},
     author  = {Bai, Yuhang and Coauthor, Some},
     journal = {Journal of Great Results},
     volume  = {1},
     pages   = {1-10},
     url     = {https://example.com/paper}
   }
   ```

   - 已投稿但尚未发表的论文，用 `note = {Submitted}`。
   - 预印本用 `note = {arXiv preprint arXiv:XXXX.XXXXX}`（或直接用 `@unpublished`）。
   - 想要可折叠摘要，就加一个 `abstract = {…}` 字段。

2. 重新生成网页：

   ```bash
   python build_site.py
   ```

3. 同时提交 `publications.bib` **和**更新后的 `index.html`。
   （或者只推送 `.bib` 改动，交给 CI 自动重建——见下文。）

### 本地实时预览

```bash
python preview.py
```

在 Windows 上也可以直接双击 `preview.bat`，或运行 `preview.ps1`。

它会在 **http://127.0.0.1:4000** 启动本地服务，并监听 `publications.bib` 和
`build_site.py`，只要其中任意一个文件发生变化就自动重建——刷新浏览器即可。

---

## 部署（GitHub Pages + CI）

网站通过 GitHub Pages 直接从仓库根目录发布，因此向默认分支的任何推送都会更新线上页面。

[`.github/workflows/update_pubs.yml`](.github/workflows/update_pubs.yml) 中的工作流会
自动保持渲染结果同步：

- **触发条件**：任何修改了 `publications.bib` 或 `build_site.py` 的推送
  （也可在 *Run workflow* 中手动运行）。
- **执行**：`python build_site.py`。
- **提交**：将重新生成的 `index.html` 提交回仓库（仅在确实有变化时）。

实际效果是：你可以直接在 GitHub 网页上编辑 `publications.bib`，一分钟后线上页面就会
自动更新。

---

## 自定义

- **个人简介、联系方式、链接、研究兴趣**——直接编辑 `index.html` 中对应的
  `<section>`。
- **加粗高亮的作者名**——修改 `build_site.py` 顶部的 `TARGET_AUTHOR`。
- **主题配色**——所有样式都在 `index.html` 的 `<style>` 块中；配色作为 CSS 自定义属性
  定义在 `:root` 下。
- **排序 / 分类逻辑**——调整 `build_site.py` 中的 `determine_category()` 和
  `generate_html()` 里的排序键。

---

## 环境要求

- **Python 3.8+**（仅用标准库——无需 `pip install` 任何东西）。
- 现代浏览器。网页字体、MathJax 等通过 CDN 加载，因此渲染页面时需要联网。
