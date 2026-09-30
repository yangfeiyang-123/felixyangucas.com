# Feiyang Yang’s personal website

A responsive, dependency-free academic homepage at **https://felixyangucas.com/**.
The source and deployment repository is **yangfeiyang-123/felixyangucas.com**.

## Preview and check

```sh
python3 -m http.server 8000 --bind 127.0.0.1
# In another terminal:
python3 scripts/check.py
node --check script.js
```

Open http://127.0.0.1:8000. There is no package installation or compilation step.
The HTML works without JavaScript; `script.js` only highlights navigation.

## Deployment

The existing GitHub Pages flow builds and deploys the root of `main` using
GitHub’s `pages build and deployment` workflow. Push a reviewed, validated commit
to `main`, check that workflow’s build and deploy jobs for the exact commit, then
verify the custom-domain page. Keep `CNAME` unchanged.

## Content and visual sources

- Name, Felix alias, public contact address, and GitHub link retain the original
  site’s information. No degree, laboratory, advisor, or affiliation is asserted.
- PriDex and MuscleMimic are research projects, described from the owner’s
  supplied research brief. No publication acceptance, author list, performance
  metric, or full-court humanoid capability is asserted.
- TactoForge: [public benchmark documentation](https://github.com/mxp1234/TactoForge)
  and [stamp modality experiment configurations](https://github.com/mxp1234/TactoForge/tree/experiment/stamp-modalities-v2-20260926/configs/experiments/stamp_modalities_v2).
- G1 pipeline: [ME139_Project](https://github.com/yangfeiyang-123/ME139_Project).
  Preserve the distinction between pipeline validation and trained skills.
- Harbor: [public README](https://github.com/yangfeiyang-123/Harbor).
  `assets/harbor.png` is its actual `docs/icon.png`; the source MIT license is
  retained as `assets/Harbor-LICENSE.txt`.
- The four research SVGs are original explanatory schematics, labeled as such.
  They are not experiment screenshots, learned trajectories, or measured results.

## Accessibility and maintenance

Semantic sections, a keyboard skip link, visible focus styles, descriptive image
alternatives, reduced-motion support, and responsive layouts are included.
All assets are local; there are no analytics, cookies, external fonts, or runtime
framework dependencies. Update content in `index.html`, styling in `styles.css`,
and diagrams in `assets/`.

On each push to `main`, `Verify published website` checks the published content and
compares the public HTML, CSS, JavaScript, and image bytes with that commit’s checkout.
It checks HTTPS and the existing HTTP URL, retries CDN propagation, and records
exact hashes. TLS verification is never disabled. A failed HTTPS check is an
explicit workflow failure even if HTTP succeeds.
