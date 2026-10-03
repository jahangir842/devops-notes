# GitHub Actions starter: Node.js CI and manual VPS deployment

[GitHub Actions notes](../../notes/github-actions/README.md) · [Analysis of the original example](../../notes/github-actions/ci-cd-reference.md)

Added: 2026-10-03

Copy and adapt these files when setting up a new project or improving an existing one. The concrete example is a root-level npm/TypeScript application deployed to one Linux VPS with Docker Compose. CI and dependency automation can be used independently of CD. These files are reference templates; GitHub does not execute them from this directory.

## Choose the files you need

| Template | Destination in the target repository | Purpose |
| --- | --- | --- |
| [ci.yml](ci.yml) | `.github/workflows/ci.yml` | Install, build, and test PRs and pushes to `main` |
| [cd.yml](cd.yml) | `.github/workflows/cd.yml` | Manually deploy the current `main` commit after successful push CI |
| [dependabot.yml](dependabot.yml) | `.github/dependabot.yml` | Weekly action and npm updates |
| [dependabot-reviewer.yml](dependabot-reviewer.yml) | `.github/workflows/dependabot-reviewer.yml` | Optional review request on Dependabot PRs |

These are copyable workflow templates. They do not implement GitHub's `workflow_call` interface for sharing a centrally maintained workflow across repositories.

From this notes repository, set an absolute destination and copy only the selected files:

```bash
target_repo='/absolute/path/to/your-project'
mkdir -p "$target_repo/.github/workflows"
cp -i templates/github-actions/ci.yml "$target_repo/.github/workflows/ci.yml"
cp -i templates/github-actions/cd.yml "$target_repo/.github/workflows/cd.yml"
cp -i templates/github-actions/dependabot.yml "$target_repo/.github/dependabot.yml"
# Optional:
cp -i templates/github-actions/dependabot-reviewer.yml "$target_repo/.github/workflows/dependabot-reviewer.yml"
```

For an existing project, inspect its workflows first. Merge the useful parts and keep existing required-check names, deployment policies, and Dependabot ecosystems. `cp -i` prompts before replacing a file. Avoid running two workflows that both deploy the same application.

## Customize before use

| Setting | Where to change it | How to choose |
| --- | --- | --- |
| `main` | CI/reviewer branch filters; CD job conditions, ref lookup, CI query, and server fetch | Use the actual deployment branch consistently |
| `ci.yml` | Filename and CD's `/actions/workflows/ci.yml/runs` API path | The API uses the filename, not `name: CI` |
| Node version | Application `.nvmrc` | Use the runtime supported by the project and its Dockerfile |
| Lockfile and commands | CI setup-node inputs and `run` steps | Commit `package-lock.json`; define real `build` and `test` scripts |
| `sandbox` | CD `environment` and GitHub environment settings | Create the exact environment explicitly |
| `sandbox-vps-deploy` | CD concurrency group | All workflows for the same target must share a group |
| `/srv/CHANGE_ME` | CD remote `deploy_dir` | Dedicated server checkout owned by the deployment user |
| `compose.vps.yml` | CD remote `compose_file` | Existing, reviewed Compose configuration in the app repository |
| `http://127.0.0.1:CHANGE_ME/health` | CD remote `health_url` | Actual readiness URL reachable from the VPS; currently requires HTTP 200 |
| Reviewer | Repository Actions variable `DEPENDABOT_REVIEWER` | One username eligible to review this repository's PRs |
| Dependency ecosystems/directories | Dependabot config | Match the project's manifests; remove npm for non-Node projects |

The CD template deliberately exits if `CHANGE_ME` remains. Search the copied files before the first deployment:

```bash
rg -n 'CHANGE_ME|YOUR_GITHUB_USERNAME' .github/
```

The optional username comment can be removed if assignees are unnecessary. Review all settings in the table, even when they do not contain a placeholder.

## Set up CI first

1. Commit `.nvmrc`, `package.json`, and `package-lock.json` in the application repository. Run `npm ci`, `npm run build`, and `CI=true npm test` locally.
2. Ensure tests execute assertions, fail on a broken behavior, and exit instead of watching for changes. A placeholder `npm test` that exits zero makes the deployment gate meaningless.
3. Add linting, type checks, integration tests, or service containers when the application needs them. Keep required checks unconditional; avoid `continue-on-error` and `--if-present` for required tests.
4. Open a PR and confirm CI runs. Merge and confirm a separate **push** CI run completes on `main`.
5. In a branch ruleset/protection rule, require the observed build-and-test check and PR review. Add `merge_group` to CI if using a merge queue. Avoid path filters that leave a required check absent.

The checkout step disables persisted credentials; setup-node caches npm downloads. `npm ci` still installs from the lockfile on each run. For a monorepo, set `defaults.run.working-directory` for shell commands **and** update `node-version-file` and `cache-dependency-path`: action inputs do not inherit the shell working directory. See [checkout](https://github.com/actions/checkout) and [setup-node](https://github.com/actions/setup-node).

## Extend tests and security checks

The starter's `ci.yml` already runs `npm test`. Implement real unit tests in the target application, then add integration tests and critical end-to-end tests where needed. Keep tests in CI initially; split them into separate jobs or workflows when their environments or schedules justify it. See the [reference guidance](../../notes/github-actions/ci-cd-reference.md#tests-security-checks-and-malware-scanning) for the purpose and limits of each check.

| Addition | Where to configure it | Adoption notes |
| --- | --- | --- |
| Lint/type checks and application tests | Steps or jobs in `ci.yml` | Run on PRs and pushes to `main`; use real scripts and fail on errors |
| Dependency review | A PR job or separate PR workflow | Block newly introduced vulnerable dependencies according to the project's policy; complements Dependabot |
| CodeQL/code scanning | GitHub code scanning setup or a configured workflow | Select supported languages and suitable triggers; decide which findings block changes |
| Secret scanning/push protection | Repository security settings where available | These features can be enabled without adding a workflow; use a dedicated scanner if the project needs additional coverage |
| Optional ClamAV scan | A job that scans selected bundled files or release artifacts | Refresh signatures, handle detections and scan errors, and inspect the actual files that will be distributed |

The starter files implement build/test execution and Dependabot automation. The additional scans above are configuration choices to add for the target project. Consult [dependency review](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review), [code scanning](https://docs.github.com/en/code-security/concepts/code-scanning/code-scanning), [secret scanning](https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning), and [ClamAV](https://docs.clamav.net/) for capabilities and availability.

Before treating a new check as required:

1. Identify what it scans: source files, dependency changes, installed packages, or a built artifact. A dependency vulnerability check does not guarantee that packages contain no malware.
2. Choose triggers and failure rules. Essential tests should run on PRs and pushes to `main`. Dependency review is PR-specific; use a suitable scan for any separate main-branch dependency gate. Alert reporting alone may not fail a workflow.
3. Give jobs only necessary permissions, pin added actions to verified full commit SHAs, and keep PR code execution out of `pull_request_target`. See [GitHub's secure use reference](https://docs.github.com/en/actions/reference/security/secure-use).
4. Connect required results to deployment. **CD currently checks only `ci.yml`.** Required jobs inside CI must run and fail the workflow when unsuccessful. For separate required workflows, extend CD's API checks to require the latest relevant run/attempt for the same SHA, branch, and event. Block missing, pending, skipped, cancelled, or failed results; a passing PR check is not automatically a passing push check for the deployed commit.
5. Verify enforcement in the target sandbox: deliberately fail a required test or scan and confirm the PR/deployment is blocked, then fix it and confirm the intended path succeeds. Branch protection controls merging; CD preflight controls this manual deployment path.

Malware scanning is optional for a typical source-code project and more useful when handling binaries, archives, or distributed artifacts. If the application accepts uploads, implement runtime scanning/quarantine too; CI cannot scan files uploaded after deployment. For this notes repository, workflow linting, link checks, and secret scanning are the most useful starting checks.

## Configure GitHub for CD

Create **Settings → Environments → sandbox** and restrict deployment branches to `main`. Add required reviewers if available for the repository and desired for this environment. These controls live in GitHub settings; `environment: sandbox` alone does not configure protection. Review feature availability for your plan in [GitHub's environment reference](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments).

Store these as **environment secrets**:

| Secret | Value |
| --- | --- |
| `SERVER_HOST` | VPS SSH hostname/address reachable from the Actions runner |
| `SERVER_PORT` | SSH port, for example `22` |
| `SERVER_USER` | Dedicated deployment account |
| `SERVER_SSH_KEY` | Private key authorized for that server account |
| `SERVER_FINGERPRINT` | Trusted server host key fingerprint beginning `SHA256:` |

Obtain the fingerprint through a trusted server console, for example `ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub -E sha256`; store the fingerprint field for the host key SSH will negotiate. An unverified `ssh-keyscan` response alone does not establish server identity. The SSH action supports fingerprint checking and explicit remote timeouts; see its [connection parameters](https://github.com/appleboy/ssh-action#connection-settings).

Existing repository secrets with the same names can be used by the job if environment secrets are missing. For a migration, add the environment values, verify deployment, then remove repository copies. GitHub cannot reveal stored secret values for copying.

No PAT is required for preflight: `GITHUB_TOKEN` has `contents: read` and `actions: read`. Git authentication **on the VPS** is separate; a private repository needs its own read-only deploy key or equivalent credential.

## Prepare the VPS once

- Install Bash, Git, `flock` (util-linux), curl, Docker Engine, and Docker Compose with `up --wait` and `--wait-timeout` support. The script explicitly starts Bash.
- Clone the correct application repository into `deploy_dir`; set `origin` correctly and verify the deployment user can fetch `main` without interaction. Use a dedicated full clone with no local tracked-file edits or application submodules requiring extra setup.
- Give the account the required Docker permissions. Docker socket access is powerful host access; use an account dedicated to deployment.
- Provision a server `.env` with required values and restrictive permissions, such as `chmod 600 .env`. Keep it untracked and excluded in `.gitignore` and `.dockerignore`. Use required-variable expressions such as `${DATABASE_URL:?DATABASE_URL is required}` in Compose where appropriate.
- Keep runtime data in named volumes or external storage. Exclude generated files and secrets from the Docker build context.
- Add healthchecks for services that must become ready. Compose waits for running/healthy services; without a healthcheck, running alone does not establish readiness. The additional HTTP check tests the configured endpoint. See [Compose up](https://docs.docker.com/reference/cli/docker/compose/up/).
- Ensure one-off tasks such as migrations/seeding are excluded from normal `compose up`, for example through profiles. Review database migration handling below.
- Ensure the runner can reach SSH. A private-only VPS needs suitable network access, such as a configured tunnel or trusted runner on that network. The health URL runs on the VPS, so it can be private.

The template checks out the exact validated SHA and builds on the server. A source SHA does not prove that a rebuilt image matches one tested in CI. For reproducible release promotion, build once in CI, publish the image, and deploy its immutable digest.

## Migrations and recovery are project decisions

The executable starter assumes **no schema migration is needed**. Add the application's migration procedure before using CD for an app with a database. Do not copy the original demo seed into a shared environment.

For a backward-compatible migration, a possible sequence is: build release images, start/wait for the database, run an idempotent migration from the new release, then start/wait for the application. For example, with actual services named `db` and `migrate`:

```bash
# Illustrative replacement for the rollout section; adapt service names/profiles.
docker compose -f "$compose_file" build
docker compose -f "$compose_file" up -d --wait --wait-timeout 120 db
docker compose -f "$compose_file" run --build --rm migrate
docker compose -f "$compose_file" up -d --build --wait --wait-timeout 120
```

Old containers may still serve traffic while the migration runs. Destructive schema changes need a separate maintenance or staged migration plan, backups, and tested restoration. A failed migration must stop the rollout, but stopping does not undo database changes.

The template has no automatic rollback. A failure can leave changed containers or a new checkout on disk. The logged previous SHA describes the checkout, not proof of the previously healthy release. Inspect `docker compose -f compose.vps.yml ps` and service logs on the server. Avoid pasting secrets from logs into issues.

The normal recovery path for this policy is a reviewed revert/fix on `main`, a successful push CI run, and a new manual deployment. Redeploying an arbitrary old SHA requires a separately designed rollback process that accounts for image availability, configuration, and database compatibility. Manual recovery commands that modify this checkout must hold the same `.git/actions-deploy.lock` lock as CD. Cancellation or a broken SSH connection is not proof that remote work stopped; inspect the server before retrying.

## First deployment and later redeploys

1. Complete customization, server preparation, and GitHub environment setup.
2. Merge the workflow onto the default branch; manual dispatch requires the workflow there. See [workflow_dispatch](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#workflow_dispatch).
3. Wait for push CI on the current `main` tip to pass.
4. Select **Actions → CD → Run workflow → main**. Enter a reason if useful; it is logged, so do not include secrets.
5. Approve the environment deployment if configured. Preflight runs after that approval and verifies the selected SHA is still current.
6. Read the preflight, SSH, and health results, then verify the application's behavior. A passed health endpoint does not cover every feature.

If `main` advances while waiting, start a new deployment after the newer commit passes CI. A rerun retains its original SHA. CD checks branch freshness twice but does not freeze the GitHub branch throughout rollout. CI completion and pushes never start this CD workflow automatically.

## Optional Dependabot review automation

Keep the reviewer workflow only if automatic review requests are useful. Configure `DEPENDABOT_REVIEWER` under repository **Settings → Secrets and variables → Actions → Variables**. Assignment in `dependabot.yml` and requesting review are different actions.

The reviewer job uses only event metadata and the GitHub API. Do not add a checkout of PR code, package installation, scripts from the PR, or PR artifacts to this privileged `pull_request_target` job. It neither approves nor merges updates. Dependabot version updates, alerts, and security updates are separate features; see the [dependency security note](../../notes/security/github-dependency-security.md).

## Troubleshooting

| Symptom | Check |
| --- | --- |
| No Run workflow button | CD is on the default branch and Actions is enabled |
| Preflight fails | Correct `ci.yml` filename, current main SHA, latest matching **push** run completed successfully, token permissions |
| Older run passed but deployment fails | The template requires the latest run/attempt for that commit to succeed |
| Missing secret / SSH failure | Environment name, all five secrets, network/firewall, key authorization, trusted fingerprint |
| Deployment reports a lock conflict | Inspect the other server operation; wait for the lock to release, then retry |
| Fetch or checkout fails | Server repository access, origin, tracked local edits, or main advanced |
| Compose/health fails | Required environment values, build output, service healthchecks, actual readiness route/port |
| Reviewer API returns 403/422 | Token policy, username, reviewer eligibility, repository access, Dependabot restrictions |

GitHub concurrency groups are repository-scoped. With the default pending behavior used here, a newer pending deployment can replace an older pending one; `cancel-in-progress: false` protects a running deployment but is not a FIFO queue. The server lock covers operations that share the checkout and follow the same locking convention. See [GitHub concurrency](https://docs.github.com/en/actions/concepts/workflows-and-actions/concurrency).

## Validation record

Prepared on 2026-10-03. Action SHA/tag pairs were verified through the upstream GitHub repositories. YAML parsing, embedded Bash syntax, 75 local links, whitespace checks, and 12 simulated preflight cases passed. The cases cover a passing run, stale SHA, missing CI, newer failure, incomplete run, wrong event/branch/SHA, cancelled/skipped CI, recovery with a newer success, and API failure. `actionlint` was unavailable locally and its download was blocked by a network/DNS failure, so workflow-specific linting remains to be run.

This repository does not contain the source application's package, Compose services, or VPS, so npm tests and an actual deployment have not been run. Test the copied workflows in the target project's sandbox before relying on them.

After adapting, run `actionlint .github/workflows/ci.yml .github/workflows/cd.yml .github/workflows/dependabot-reviewer.yml` (omit files not copied), then `git diff --check`. Dependabot configuration is not a workflow; validate it separately through YAML checks and Dependabot's update logs after merging.
