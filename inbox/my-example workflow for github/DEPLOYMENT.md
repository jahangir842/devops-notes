# CI and sandbox deployment

`.github/workflows/ci.yml` runs on pull requests and pushes to `main`. It installs locked dependencies, builds TypeScript, and runs the current test command. The test command is still a placeholder; #23 owns the real suite and #30 will make it a meaningful gate. CI has no deployment credentials.

`.github/workflows/cd.yml` runs **only when manually started** with `workflow_dispatch`. Select `main` in the Actions UI. CD requires that the selected commit is still the current main tip and has a successful push CI run. PRs, CI completion, pushes, and manual runs from other branches cannot deploy. The VPS fetches and checks out the validated commit. Deployments share one concurrency group.

## GitHub environment

The CD job uses the `sandbox` environment. Its deployment branch policy is configured to allow only `main`; check this under **Settings → Environments → sandbox**. Add any required reviewers there if the team wants approval before sandbox deployment. Environment protection is configured in GitHub, not in workflow YAML.

The SSH action needs these secrets:

| Secret | Meaning |
| --- | --- |
| `SERVER_HOST` | VPS SSH hostname or address |
| `SERVER_PORT` | VPS SSH port |
| `SERVER_USER` | VPS SSH user |
| `SERVER_SSH_KEY` | Private SSH key for that user |

These four secrets currently exist at repository scope. GitHub does not expose their values for migration. Add the same values under **Settings → Environments → sandbox → Environment secrets**, verify a deployment, then delete the repository-scoped copies. Until that move, the CD job can still use the existing repository secrets. The server-local `.env` holds database, JWT, encryption, and optional SMTP values; it is separate from GitHub Actions secrets.

The CD token has `contents: read` and `actions: read` so it can verify the current main ref and successful CI run. CI has only `contents: read`. Third-party actions are pinned to full commit SHAs. Dependabot checks their updates weekly. A successful CI run does not trigger CD.

## Current rollout behavior

CD checks out the validated commit on the VPS, runs `docker compose up -d --build`, runs migrations and demo seeding, then calls `/health`. A remote command failure stops the job. Image provenance, migration ordering, readiness checks, and rollback still need #31 and #32; this workflow split does not claim those controls are complete.

The VPS checkout must allow `git fetch origin main` and have no conflicting tracked-file edits. Its untracked `.env` remains in place when CD checks out the commit. To redeploy, use **Actions → CD → Run workflow**, select `main`, and enter an optional reason.
