# Deployment Runbook

## Production target

- Render service: `jacob-wood-cpp-consulting`
- Service ID: `srv-db4v048473hc7398iqtg`
- Source branch: `cpp-consulting-site`
- Public URL: https://jacob-wood-cpp-consulting.onrender.com
- Publish path: repository root (`./`)

## Required validation

Run locally before publication:

```sh
python tools/validate_site.py
```

The validator checks required files, all graphics and Basic HTML pages, internal links and fragments, canonical URLs, sale/regular pricing, sale expiration, no-JavaScript price safety, Stripe URL boundaries, local-card-field prohibition, manifest JSON, sitemap XML, and robots metadata.

GitHub Actions runs the same gate from `.github/workflows/consulting-site.yml` on pushes and pull requests targeting `cpp-consulting-site`. The first workflow run passed on October 13, 2026.

## Current deployment boundary

The Render service was created from the public repository URL rather than a connected Git-provider credential. Render's documented behavior is that public-URL services require manual deployment; automatic deployment requires a connected Git provider.

Do not infer deployment from a successful GitHub push or a successful validation workflow.

## Safe publication procedure

1. Run the validator and require a passing result.
2. Read the current `cpp-consulting-site` branch-head SHA.
3. Read Render's current live deploy and its commit SHA.
4. If both SHAs match and the deploy is `live`, do nothing.
5. If Render is behind, use exactly one authorized deployment route:
   - an existing connected-Git-provider deployment;
   - the protected GitHub Actions deploy hook after its repository secret is configured; or
   - one explicit Render API deploy.
6. Verify the resulting deploy reaches `live` and reports the exact branch-head SHA.
7. Record the commit and deploy IDs in the publication report or blocker issue.

Never recreate the service, change repository visibility, change the hostname, add a paid service, or expose deployment credentials as a workaround.

## Preferred repair

Preserve the existing service and URL:

1. Connect or verify a GitHub deployment credential in Render Account Settings.
2. Ensure the credential can access `tsrnc2/tsrnc2`.
3. Update this service's **Git Credentials** to the connected credential.
4. Push a documentation-only commit to `cpp-consulting-site`.
5. Accept the repair only when Render creates a commit-triggered deploy automatically and that deploy reaches `live` for the exact pushed SHA.

## Protected deploy-hook fallback

The branch already contains a safe fallback in `.github/workflows/consulting-site.yml`. It validates first and calls Render only after a push to `cpp-consulting-site`.

The fallback remains inactive until an authorized operator:

1. Obtains the existing service's secret deploy-hook URL from Render Settings.
2. Stores it only as the GitHub Actions repository secret `RENDER_DEPLOY_HOOK_URL`.
3. Runs or pushes the workflow and verifies the resulting Render deploy serves the exact pushed SHA.

When the secret is absent, the workflow reports a notice and exits successfully without changing production. It never prints the hook URL.

Never commit, log, paste, or copy the secret hook URL into reports, issues, source files, or chat.

## Payment boundary

`checkout-config.js` must stay blank until genuine Stripe Payment Links are created and independently checked. See [`PAYMENTS.md`](PAYMENTS.md) for the exact product, sale, verification, and expiration procedure.

The site must not collect card details or invent payment URLs. Email ordering remains the safe fallback.

## Durable blocker

Track the connected-provider defect and review evidence in [GitHub issue #1](https://github.com/tsrnc2/tsrnc2/issues/1). Close it only after a push-triggered Render deployment reaches `live` for the exact test commit.
