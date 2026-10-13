# C/C++ Consulting Site

Static three-page consulting and lesson website for Jacob W. Wood.

## Production

- Site: https://jacob-wood-cpp-consulting.onrender.com
- Host: Render static site
- Source branch: `cpp-consulting-site`
- Default presentation: graphics
- Basic HTML mirrors: `basic/`
- Online payment: fail-closed until verified Stripe Payment Links are configured in `checkout-config.js`

## Pages

- `index.html` — consulting home
- `experience.html` — experience and technical evidence appendix
- `checkout.html` — lesson pricing, curriculum, and checkout handoff

Each page has a text-only counterpart under `basic/`.

## Evidence policy

Technical claims must remain bounded by the cited source records. Do not turn planned work into implemented work, limited tests into general qualification, or architecture work into production-complete claims.

## Deployment

Render serves the repository root from this branch. The current service was created from a public repository URL, so branch pushes do **not** currently trigger automatic deploys even though the service metadata says auto-deploy is enabled. Render requires a connected Git provider for push-triggered deployments.

Until the Git credential is repaired:

1. Compare the branch head SHA with Render's live deploy commit.
2. Trigger an explicit Render deploy only when the live commit is behind.
3. Verify the resulting deploy reaches `live` for the exact branch-head SHA.

See [`DEPLOYMENT.md`](DEPLOYMENT.md) and [issue #1](https://github.com/tsrnc2/tsrnc2/issues/1).

## Deployment verification

- 2026-10-13: commit `9562bc07addc76834526f1e100331c33c5105a1c` proved that a branch push did not trigger Render automatically. Explicit deploy `dep-db76sf2vcj2c739860i0` synchronized production to that exact commit.
