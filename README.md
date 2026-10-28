# C/C++ Consulting & Lessons Site

Static consulting, lessons, and Kludge Wagon Haywire companion site for Jacob W. Wood.

## Production

- Site: https://jacob-wood-cpp-consulting.onrender.com
- Host: Render static site
- Source branch: `cpp-consulting-site`
- Default presentation: graphics
- Basic HTML mirrors: `basic/`
- Online payment: fail-closed until verified Stripe Payment Links are configured in `checkout-config.js`

## Pages

- `index.html` — lessons home + Kludge Wagon Haywire overview
- `watch.html` — YouTube episodes, trailer, and Shorts embeds (YT landing for inbound traffic)
- `cast.html` — character / vehicle reference sheets (homage-only)
- `cheatsheets.html` — printable C/C++ mistake PDF downloads
- `course.html` — Safe Native Tooling for LLM Agents in Modern C++
- `experience.html` — experience and technical evidence appendix
- `checkout.html` — lesson pricing and checkout handoff

Each page has a text-only counterpart under `basic/`.

## Pricing

- Single 60-minute lesson: **$100**
- 14-session course: **$1,000** regular; New Year sale **$400** until Jan 1, 2027 PT

## Validation

```sh
python tools/validate_site.py
```

GitHub Actions runs the same validator on pushes and pull requests for this branch. The workflow also contains a protected Render deploy-hook fallback that stays inert while `RENDER_DEPLOY_HOOK_URL` is absent.

## Evidence policy

Technical claims must remain bounded by the cited source records. Do not turn planned work into implemented work, limited tests into general qualification, or architecture work into production-complete claims.

## Branding

Homage branding only. Characters and the Kludge Wagon SR-404 are original. Do not use third-party automotive or TV marks.
