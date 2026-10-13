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

## Validation

Run the dependency-free publication gate:

```sh
python tools/validate_site.py
```

GitHub Actions runs the same validator on pushes and pull requests for this branch. It checks internal links and fragments, graphics/Basic HTML parity, canonical metadata, pricing and sale expiration, conservative no-JavaScript pricing, checkout safety, Stripe URL boundaries, manifest JSON, sitemap XML, and robots metadata.

The workflow also contains a protected Render deploy-hook fallback. It remains inert and exits successfully while the repository secret `RENDER_DEPLOY_HOOK_URL` is absent.

## Evidence policy

Technical claims must remain bounded by the cited source records. Do not turn planned work into implemented work, limited tests into general qualification, or architecture work into production-complete claims.

## Payments

The checkout remains email-only until Stripe is connected and the public Payment Links are independently verified. See [`PAYMENTS.md`](PAYMENTS.md) for the required products, current $400 course sale, regular $1,000 course price, $100 single lesson, verification record, and sale-expiration procedure.

Only public `buy.stripe.com` Payment Links may be committed. Never commit Stripe keys, webhook secrets, customer data, or dashboard credentials.

## Deployment

Render serves the repository root from this branch. The current service was created from a public repository URL, so branch pushes do **not** currently trigger automatic Render deploys even though the service metadata says auto-deploy is enabled. Render requires a connected Git provider for push-triggered deployments.

Until the Git credential or protected deploy-hook fallback is configured:

1. Require a passing site validation run.
2. Compare the branch-head SHA with Render's live deploy commit.
3. Trigger an explicit Render deploy only when production is behind.
4. Verify the resulting deploy reaches `live` for the exact branch-head SHA.

See [`DEPLOYMENT.md`](DEPLOYMENT.md) and [issue #1](https://github.com/tsrnc2/tsrnc2/issues/1).

## Verification history

- 2026-10-13: commit `9562bc07addc76834526f1e100331c33c5105a1c` proved that a branch push did not trigger Render automatically. Explicit deploy `dep-db76sf2vcj2c739860i0` synchronized production to that exact commit.
- 2026-10-13: the first `Consulting site CI` run passed the complete publication validator. Its deploy job safely skipped because `RENDER_DEPLOY_HOOK_URL` was not configured.
