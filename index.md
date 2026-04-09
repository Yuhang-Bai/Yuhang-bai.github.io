---
layout: single
author_profile: false
title: "Yuhang Bai"
permalink: /
classes: wide
---
<style>
  @import url("https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Source+Serif+4:opsz,wght@8..60,400;500;600&display=swap");

  .page__title,
  .page__meta,
  .page__share,
  .page__related,
  .author__urls-wrapper {
    display: none !important;
  }

  .page {
    max-width: 1280px;
  }

  .page__inner-wrap {
    width: 100%;
  }

  .page__content {
    font-family: "Source Serif 4", Georgia, serif;
    color: #18212b;
  }

  .page__content p,
  .page__content li {
    font-size: 1.05rem;
    line-height: 1.8;
  }

  .home-shell {
    position: relative;
    padding: 1rem 0 3rem;
  }

  .home-shell::before {
    content: "";
    position: absolute;
    inset: 0 0 auto 0;
    height: 28rem;
    background:
      radial-gradient(circle at top left, rgba(237, 120, 66, 0.18), transparent 30rem),
      radial-gradient(circle at top right, rgba(33, 118, 174, 0.20), transparent 24rem),
      linear-gradient(135deg, #f6efe3 0%, #f4f8fb 52%, #eef4f9 100%);
    border-radius: 2rem;
    z-index: -1;
  }

  .hero-panel {
    display: grid;
    grid-template-columns: minmax(0, 1.45fr) minmax(260px, 0.8fr);
    gap: 2rem;
    align-items: center;
    padding: 2.5rem 2.25rem 2rem;
  }

  .hero-eyebrow {
    margin: 0 0 0.85rem;
    font-family: "Space Grotesk", sans-serif;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #0b5f87;
  }

  .hero-panel h1 {
    margin: 0;
    font-family: "Space Grotesk", sans-serif;
    font-size: clamp(2.7rem, 6vw, 4.6rem);
    line-height: 0.95;
    letter-spacing: -0.05em;
    color: #102033;
  }

  .hero-panel .hero-lead {
    margin: 1.3rem 0 0;
    max-width: 42rem;
    font-size: 1.15rem;
    line-height: 1.85;
    color: #304154;
  }

  .hero-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 0.9rem;
    margin-top: 1.5rem;
  }

  .hero-actions a {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.8rem 1.15rem;
    border-radius: 999px;
    border: 1px solid rgba(16, 32, 51, 0.12);
    background: rgba(255, 255, 255, 0.75);
    color: #102033;
    font-family: "Space Grotesk", sans-serif;
    font-size: 0.95rem;
    font-weight: 500;
    text-decoration: none;
    box-shadow: 0 12px 30px rgba(16, 32, 51, 0.08);
    transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
  }

  .hero-actions a:hover {
    transform: translateY(-2px);
    background: #ffffff;
    box-shadow: 0 16px 34px rgba(16, 32, 51, 0.12);
  }

  .hero-portrait {
    display: flex;
    justify-content: center;
  }

  .hero-portrait-card {
    position: relative;
    width: min(100%, 320px);
    padding: 1rem;
    border-radius: 1.8rem;
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(248, 250, 252, 0.88));
    box-shadow: 0 22px 60px rgba(16, 32, 51, 0.12);
  }

  .hero-portrait-card::after {
    content: "";
    position: absolute;
    inset: auto -1rem -1rem auto;
    width: 6rem;
    height: 6rem;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(237, 120, 66, 0.28), rgba(237, 120, 66, 0));
    z-index: 0;
  }

  .hero-portrait img {
    position: relative;
    z-index: 1;
    display: block;
    width: 100%;
    aspect-ratio: 1 / 1;
    object-fit: cover;
    border-radius: 1.25rem;
  }

  .home-pubs-intro {
    margin: 2rem 0 1rem;
    padding: 1.55rem 1.45rem;
    border-left: 4px solid #ed7842;
    border-radius: 1rem;
    background: linear-gradient(135deg, rgba(237, 120, 66, 0.08), rgba(255, 255, 255, 0.86));
  }

  .home-pubs-intro h2 {
    margin: 0 0 0.45rem;
    font-family: "Space Grotesk", sans-serif;
    font-size: 1.45rem;
    color: #102033;
  }

  .home-pubs-intro p {
    margin: 0;
    color: #425365;
  }

  .page__content > h2,
  .page__content > h3 {
    font-family: "Space Grotesk", sans-serif;
    color: #102033;
  }

  .page__content > h2 {
    margin-top: 2.5rem;
    padding-top: 0.5rem;
    font-size: 2rem;
  }

  .page__content > h3 {
    margin-top: 1.8rem;
    font-size: 1.3rem;
  }

  .page__content a {
    color: #0b5f87;
  }

  .page__content details {
    margin: 0.7rem 0 1.15rem 0.5rem;
    padding: 0.95rem 1rem;
    border-radius: 1rem;
    background: #f7fafc;
    border: 1px solid rgba(16, 32, 51, 0.08);
  }

  .page__content summary {
    font-family: "Space Grotesk", sans-serif;
    font-weight: 500;
    cursor: pointer;
  }

  .page__content blockquote {
    margin: 0.8rem 0 0;
    padding: 0 0 0 1rem;
    border-left: 3px solid rgba(11, 95, 135, 0.24);
    color: #425365;
  }

  .useful-links {
    margin-top: 2.5rem;
  }

  .useful-links ul {
    padding-left: 1.2rem;
  }

  @media (max-width: 900px) {
    .hero-panel {
      grid-template-columns: 1fr;
    }

    .hero-panel {
      padding: 2rem 1.3rem 1.2rem;
    }

    .home-shell::before {
      border-radius: 1.5rem;
      height: 24rem;
    }
  }
</style>

<div class="home-shell">
  <section class="hero-panel">
    <div>
      <p class="hero-eyebrow">Graph Theory · Approximation Algorithms · Random Graphs</p>
      <h1>Yuhang Bai</h1>
      <p class="hero-lead">
        I am a PhD candidate at <strong>Northwestern Polytechnical University (NWPU)</strong>.
        My research focuses on graph theory and theoretical computer science, with particular
        interest in approximation algorithms and random graph theory.
      </p>
      <div class="hero-actions">
        <a href="mailto:yuhang.bai66@gmail.com">Email</a>
        <a href="https://scholar.google.com.hk/citations?user=rznH-g4AAAAJ&hl=zh-CN">Google Scholar</a>
        <a href="#publications">Publications</a>
      </div>
    </div>
    <div class="hero-portrait">
      <div class="hero-portrait-card">
        <img src="/images/profile.png" alt="Portrait of Yuhang Bai">
      </div>
    </div>
  </section>
</div>

<div class="home-pubs-intro" id="publications">
  <h2>Publications</h2>
  <p>
    Papers are grouped by type. This section is generated from BibTeX and keeps the
    current auto-update workflow unchanged.
  </p>
</div>

<!-- PUBS_START -->

## List of papers

### Preprint

[4] **Yuhang Bai**, Gyula O.H. Katona, Zixuan Yang. [Most probably trangle-free graphs](https://arxiv.org/abs/2602.22782). *arXiv preprint arXiv:2602.22782*.

[3] **Yuhang Bai**, Kristóf Bérczi, Johanna K. Siemelink. [Approximating maximum properly colored forests via degree bounded independent sets](https://arxiv.org/abs/2511.18263). *arXiv preprint arXiv:2511.18263*.

[2] Yichen Wang, Zixuan Yang, Xiamiao Zhao, **Yuhang Bai**, Junpeng Zhou. [The Turán number of Berge matchings](https://arxiv.org/abs/2510.05422). *arXiv preprint arXiv:2510.05422*.

[1] **Yuhang Bai**, Kristóf Bérczi, Gergely Csáji, Tamás Schwarcz. [Approximating maximum-size properly colored forests](https://arxiv.org/abs/2402.00834). *arXiv preprint arXiv:2402.00834*.



### Journal

[9] Xiamiao Zhao, Zixuan Yang, Yichen Wang, **Yuhang Bai**, Junpeng Zhou. On Turán-type problems for Berge matchings. *Submitted*.

[8] **Yuhang Bai**, Gyula O.H. Katona, Zixuan Yang. Most probably trangle-free graphs. *Submitted*.

[7] **Yuhang Bai**, Kristóf Bérczi, Johanna K. Siemelink. Approximating maximum properly colored forests via degree bounded independent sets. *Submitted*.

[6] Yichen Wang, Zixuan Yang, Xiamiao Zhao, **Yuhang Bai**, Junpeng Zhou. The Turán number of Berge matchings. *Submitted*.

[5] **Yuhang Bai**, Shenggui Zhang. Properly colored thresholds. *Submitted*.
   <details>
       <summary>Abstract</summary>
       <blockquote>
       We extend both the threshold result of Frankston–Kahn–Narayanan–Park and its strengthening by Spiro to properly colored settings. In addition, we establish threshold results for some properly colored structures in randomly colored randomly perturbed graphs.
       </blockquote>
       </details>

[4] **Yuhang Bai**, Shenggui Zhang, Yandong Bai, Jianhua Tu. The parameterized complexity of properly colored spanning trees problem. *Submitted*.
   <details>
       <summary>Abstract</summary>
       <blockquote>
       A weakly properly colored spanning tree $T$ with fixed root $r$ is a spanning tree in which every path in $T$, from $r$ to any leaf, is a properly colored path. We demonstrate that it is NP-complete to determine whether a planar graph contains a properly colored spanning tree, even for planar graphs with maximum degree four using only two colors. We also investigate the generalized properly colored spanning trees problem, where given a graph that every edge is assigned a set of colors, determine whether the graph contains a properly colored spanning tree, in which no two adjacent edges share a color. Surprisingly, this problem is polynomial-time solvable for trees but NP-hard for partial $2$-trees with each edge assigned at most two colors. Additionally, we prove that it is W[1]-hard to decide whether an edge-colored graph contains a weakly properly colored spanning tree when parameterized by the treewidth. On the positive side, we show that these problems are fixed-parameter tractable when parameterized by combining the treewidth and the number of colors.
       </blockquote>
       </details>

[3] **Yuhang Bai**, Kristóf Bérczi, Gergely Csáji, Tamás Schwarcz. [Approximating maximum-size properly colored forests](https://www.sciencedirect.com/science/article/pii/S0195669825001581). *European Journal of Combinatorics*, 132 (2026), 104269.

[2] Yanni Dong, Hajo Broersma, **Yuhang Bai**, Shenggui Zhang. [The complexity of spanning tree problems involving graphical indices](https://www.sciencedirect.com/science/article/pii/S0166218X24000167). *Discrete Applied Mathematics*, 347, 143-154.

[1] **Yuhang Bai**, Zhiwei Guo, Shenggui Zhang, Yandong Bai. [Linear amortized time enumeration algorithms for compatible Euler trails in edge-colored graphs](https://link.springer.com/article/10.1007/s10878-023-01005-w). *Journal of Combinatorial Optimization*, 45 (2), 73.



### Conference

[1] **Yuhang Bai**, Kristóf Bérczi, Gergely Csáji, Tamás Schwarcz. [Approximating maximum-size properly colored forests](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2024.14). In *32nd Annual European Symposium on Algorithms (ESA 2024)*, 308, 14:1-14:18.



<!-- PUBS_END -->

<section class="useful-links">
  <h2>Useful Links</h2>
  <ul>
    <li><a href="https://matroidunion.org/">Matroid Union</a></li>
  </ul>
</section>







