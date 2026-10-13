# Deployment Runbook

## Production target

- Render service: `jacob-wood-cpp-consulting`
- Service ID: `srv-db4v048473hc7398iqtg`
- Source branch: `cpp-consulting-site`
- Public URL: https://jacob-wood-cpp-consulting.onrender.com
- Publish path: repository root (`./`)

## Current deployment boundary

The service was created from the public repository URL rather than a connected Git-provider credential. Render's documented behavior is that public-URL services require manual deployment; automatic deployment requires a connected Git provider.

Do not infer deployment from a successful GitHub push.

## Safe publication procedure

1. Validate the static files and internal links locally or from the repository contents.
2. Read the current `cpp-consulting-site` branch-head SHA.
3. Read Render's current live deploy and its commit SHA.
4. If both SHAs match and the deploy is `live`, do nothing.
5. If Render is behind, trigger one explicit deploy for the existing service.
6. Verify the deploy reaches `live` and reports the exact branch-head SHA.
7. Record the commit and deploy IDs in the publication report or blocker issue.

Never recreate the service, change repository visibility, change the hostname, add a paid service, or expose deployment credentials as a workaround.

## Preferred repair

Preserve the existing service and URL:

1. Connect or verify a GitHub deployment credential in Render Account Settings.
2. Ensure the credential can access `tsrnc2/tsrnc2`.
3. Update this service's **Git Credentials** to the connected credential.
4. Push a documentation-only commit to `cpp-consulting-site`.
5. Accept the repair only when Render creates a commit-triggered deploy automatically and that deploy reaches `live` for the exact pushed SHA.

## Fallback repair

Use a Render deploy hook only when provider-based deployment cannot be repaired:

1. Obtain the existing service's secret deploy-hook URL from Render Settings.
2. Store it only as the GitHub Actions secret `RENDER_DEPLOY_HOOK_URL`.
3. Add a workflow scoped to pushes on `cpp-consulting-site`.
4. Run validation before calling the hook.
5. Never commit, log, or copy the secret hook URL into reports, issues, or chat.

## Payment boundary

`checkout-config.js` must stay blank until two genuine Stripe Payment Links are created and independently checked:

- one 60-minute C/C++ lesson — `$100 USD`
- fourteen-lesson C/C++ course — `$1,000 USD`

The site must not collect card details or invent payment URLs. Email ordering remains the safe fallback.

## Durable blocker

Track the integration defect and review evidence in [GitHub issue #1](https://github.com/tsrnc2/tsrnc2/issues/1).
