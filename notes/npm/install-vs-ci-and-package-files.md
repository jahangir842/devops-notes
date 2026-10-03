# npm install vs npm ci; package.json vs package-lock.json

Added: 2026-10-03  
Topic: npm  
Status: to-review

## What I learned

`package.json` is the project manifest: it names the package, declares scripts and metadata, and records direct dependencies and the version ranges the project accepts. For example, `^4.2.0` allows compatible releases from 4.2.0 up to (but not including) 5.0.0.

`package-lock.json` is npm's generated record of the resolved dependency tree. It records the concrete package versions and other installation details, including transitive dependencies, so npm can recreate a consistent tree. Commit both files for an application or other project whose installs should be reproducible; do not commit `node_modules`.

| Command | Use it for | Lockfile behavior |
| --- | --- | --- |
| `npm install` | Local development, adding/removing packages, or reconciling dependencies after editing the manifest | Reads the lockfile when it satisfies the manifest; can resolve versions and update the lockfile when dependencies or ranges change. With a package argument, it installs that package and normally saves it to `package.json`. |
| `npm ci` | Clean, repeatable installs in CI, builds, and deployments | Requires a lockfile consistent with `package.json`; errors on mismatch and does not rewrite either file. Removes the existing `node_modules` before installing the whole project. |

## Why it matters

The manifest describes acceptable dependency ranges; the lockfile records the specific dependency tree selected for this project. Using `npm ci` in automation makes an out-of-date lockfile visible as a failure instead of silently resolving a different tree. Use `npm install` during development when intentionally changing dependencies, then review and commit the manifest and lockfile changes together.

## Example or commands

```bash
# Add a dependency during development; updates package.json and package-lock.json
npm install express

# Install the project from its committed lockfile in CI
npm ci

# Update dependencies within the ranges already declared in package.json
npm update
```

If the lockfile was generated using tree-shaping options such as `--legacy-peer-deps` or `--install-links`, use the same options with `npm ci`. A project `.npmrc` can record such settings so local and CI installs agree.

## Verification

Checked npm's current documentation on 2026-10-03. The examples are explanatory; no npm project was installed or tested in this repository.

## Gotchas and follow-up

- Do not hand-edit `package-lock.json`; make dependency changes with npm and inspect the resulting diff.
- `npm ci` installs the complete project, not a single package. To change dependencies, use `npm install <package>` and commit the resulting files.
- Keep the npm version and relevant project configuration consistent across developer machines and CI when install behavior needs to match closely.
- [ ] Try changing a dependency in a sample project, inspect both files, then compare a clean `npm ci` install with `npm install`.

## Sources and related notes

- [npm install](https://docs.npmjs.com/cli/commands/npm-install/)
- [npm ci](https://docs.npmjs.com/cli/commands/npm-ci/)
- [package-lock.json](https://docs.npmjs.com/files/package-lock.json/)
- [GitHub dependency graph and Dependabot](../security/github-dependency-security.md)
