# GitHub dependency graph and Dependabot

Added: 2026-10-03  
Topic: Security  
Status: to-review

## What I learned

GitHub's dependency security features form a sequence:

1. **Dependency graph** identifies packages used by a repository from supported manifest and lock files. It can show direct and transitive dependencies, their versions, licenses, and known vulnerabilities. Build-time dependencies can also be supplied through dependency submission.
2. **Dependabot alerts** compare the graph with the GitHub Advisory Database and flag known vulnerable dependencies already present in the repository.
3. **Dependabot security updates** can open pull requests to move vulnerable dependencies to a patched version after an alert. They can work without a `dependabot.yml` file when enabled in repository settings.
4. **Dependabot version updates** check for newer dependency versions on a configured schedule and open pull requests even when there is no known vulnerability. These require `.github/dependabot.yml` on the default branch.
5. **Dependency review** shows dependency changes in a pull request. The optional dependency review action can fail a check when a pull request introduces a known vulnerable dependency.

The dependency graph feeds alerts, security updates, and dependency review. Version updates inspect package versions separately; they do not depend on the graph.

## Why it matters

An alert tells me about a known issue in dependencies I already use. A security update offers a proposed fix. A version update helps keep packages current before an alert appears. Dependency review helps catch a risky addition during pull request review. Each proposed update still needs CI and human review for breaking changes.

## Example configuration

For a repository with an npm project at its root and workflows in `.github/workflows/`, this illustrative `.github/dependabot.yml` checks both ecosystems weekly:

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    assignees:
      - "jahangir842"
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    assignees:
      - "jahangir842"
```

`assignees` lists GitHub usernames to assign to Dependabot pull requests for that ecosystem. GitHub applies it to both version and security update pull requests (except security updates configured for a non-default target branch). The assignee must have suitable repository access; for a personal repository, that means write access.

Use only entries for ecosystems and manifest locations actually present in the repository. The `github-actions` entry uses `/` even though workflow files live under `.github/workflows/`. This file configures version updates; Dependabot alerts and security updates are enabled separately in **Settings → Advanced Security**. The example's npm entry is illustrative. This repository's [actual Dependabot configuration](../../.github/dependabot.yml) monitors GitHub Actions weekly and assigns its pull requests to `jahangir842`.

## Where to look on GitHub

- **Insights → Dependency graph:** inspect detected dependencies and the files that introduced them.
- **Security → Dependabot alerts:** triage known vulnerabilities and check the affected version and available fix.
- **Pull request → Files changed → dependency review:** inspect added, removed, and updated dependencies before merging.
- **Settings → Advanced Security:** check the dependency graph, alert, and security update settings. Menu labels and availability can vary by repository and plan.

## Gotchas and follow-up

- Coverage depends on supported ecosystems and correctly detected manifests or lock files. A lock file often gives GitHub more precise versions and transitive dependency data. A package missing from the graph is not proof that it is safe.
- Alerts are based on *known* advisories; they are not a complete vulnerability scan of application code or every package risk.
- Security update pull requests and version update pull requests solve different problems. Review the changed manifest and lock file, run tests, and check the resulting dependency tree before merging.
- [ ] Try the settings and example configuration in a repository with a supported package manifest; record which dependencies, alerts, and pull requests appear.

## Verification

Checked GitHub's documentation on 2026-10-03. The YAML was reviewed locally; GitHub has not yet processed this configuration, so pull request assignment has not been observed.

## Sources and related notes

- [GitHub: Supply chain security](https://docs.github.com/en/code-security/concepts/supply-chain-security/supply-chain-security)
- [GitHub: Dependency graph](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-graph)
- [GitHub: Configuring Dependabot alerts](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/configure-dependabot-alerts)
- [GitHub: Configuring Dependabot security updates](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/configure-security-updates)
- [GitHub: Configuring Dependabot version updates](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/configure-version-updates)
- [GitHub: Dependabot `assignees` option](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference#assignees)
- [GitHub: Dependency review](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review)
- [GitHub: Supported dependency graph ecosystems](https://docs.github.com/en/code-security/reference/supply-chain-security/dependency-graph-supported-package-ecosystems)
- [GitHub Actions notes](../github-actions/README.md)
