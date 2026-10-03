# DevOps notes

My working notebook for learning DevOps: concepts, commands, troubleshooting, course material, and practical labs.

**[Latest additions & read later](LATEST.md)** · **[Browse all topics](notes/README.md)** · **[Learning inbox](inbox/README.md)** · **[How to add notes](CONTRIBUTING.md)**

## Daily learning

1. Add a note to its topic, or capture an unfinished idea in `inbox/`.
2. Keep a dated link in **[LATEST.md](LATEST.md)** so it is easy to find later.
3. When you have time, read an unchecked entry and tick it off. Completed entries stay as your learning history.

From the repository root, Python 3.9+ can create a note, link it in the topic index, and add it to the reading queue:

```bash
python3 scripts/new_note.py kubernetes/concepts "Pod disruption budgets"
python3 scripts/new_note.py inbox "Read about OpenTelemetry"
```

You can also copy a [note template](templates/note.md) or [lab template](templates/lab.md) and update the indexes manually. See the [writing guide](CONTRIBUTING.md) for examples.

## Browse by topic

| Area | Topics |
| --- | --- |
| Foundations | [Linux](notes/linux/README.md), [Networking](notes/networking/README.md), [Git](notes/git/README.md), [Scripting](notes/scripting/README.md) |
| Containers | [Docker](notes/docker/README.md), [Kubernetes](notes/kubernetes/README.md) |
| Infrastructure and automation | [Ansible](notes/ansible/README.md), [Terraform](notes/terraform/README.md), [Bicep](notes/bicep/README.md) |
| CI/CD | [GitHub Actions](notes/github-actions/README.md), [Azure DevOps](notes/azure-devops/README.md), [Jenkins](notes/jenkins/README.md) |
| Cloud and operations | [Cloud](notes/cloud/README.md), [Observability](notes/observability/README.md), [Security](notes/security/README.md) |
| Career preparation | [Interview notes](notes/interviews/README.md) |

Each topic has an index. Existing Kubernetes labs, monitoring configurations, Ansible projects, and Terraform exercises keep their files together. Foundation folders provide a home for future notes; related material is linked where available.

## Repository layout

```text
devops-notes/
├── README.md          # Start here
├── LATEST.md          # Dated additions and reading checkboxes
├── CONTRIBUTING.md    # Daily workflow and naming conventions
├── notes/             # Long-term notes and labs, organized by topic
├── inbox/             # Quick captures to sort later
├── templates/         # Note and lab starting points
├── scripts/           # Helper for creating and logging notes
└── .github/           # Repository workflows
```

## Finding and using material

Browse the [topic directory](notes/README.md), use GitHub's file search, or search locally:

```bash
rg -n -i 'ingress' notes/ --glob '*.md'
```

Read a lab's own instructions before running its examples. Existing technical notes and version references have been preserved and have not all been revalidated. New notes should record what was tested and with which versions.

The Azure links and project ideas from the former homepage are in [Azure learning resources](notes/cloud/azure-learning-resources.md). The [reorganization notes](docs/reorganization.md) explain where the original folders moved.
