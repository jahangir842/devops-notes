# Repository reorganization

[Home](../README.md) · [Topics](../notes/README.md)

Reorganized on 2026-10-03 for ongoing personal learning.

## Where existing material moved

| Original location | New location |
| --- | --- |
| `Ansible/` | [notes/ansible/](../notes/ansible/README.md) |
| `Docker/` | [notes/docker/](../notes/docker/README.md) |
| `Jenkins/` | [notes/jenkins/](../notes/jenkins/README.md) |
| `azure_devops/` | [notes/azure-devops/](../notes/azure-devops/README.md) |
| `github_actions/` | [notes/github-actions/](../notes/github-actions/README.md) |
| `kubernetes/` | [notes/kubernetes/](../notes/kubernetes/README.md) |
| `terraform/` | [notes/terraform/](../notes/terraform/README.md) |
| `bicep/` | [notes/bicep/](../notes/bicep/README.md) |
| `interviews/` | [notes/interviews/](../notes/interviews/README.md) |
| Homepage Azure resources and project ideas | [Azure learning resources](../notes/cloud/azure-learning-resources.md) |

Markdown and PDF filenames now use lowercase and hyphens, except standard `README.md` filenames. Course PDFs are grouped under each topic's `assignments/` directory.

## Navigation changes

- The old Kubernetes, Ansible, GitHub Actions, Azure DevOps, and Jenkins landing-page content is retained as notes beside the new topic indexes.
- `kubernetes/docs/` is now `notes/kubernetes/concepts/`; `persistance_storage/` is `persistent-storage/`.
- `kubernetes/old/` is now `notes/kubernetes/archive/`.
- The kubeadm `troobleshooting/` folder is now `troubleshooting/`.
- The NGINX demo's `nginx-deployment.yaml.yaml` is now `nginx-deployment.yaml`, matching its guide.
- GitHub Actions runner notes are in `self-hosted-runners/`, workflow examples in `workflows/`, and PR notes in `pull-requests/`.
- Git hooks moved to [Git](../notes/git/README.md).
- Terraform's `AWS_Infra/` is now `aws-infra/`.
- Missing K3s exercise and pattern links are labelled as planned material. The existing Flask lab is linked.
- The monitoring guide's clone and working-directory instructions point to this repository.

## Local files and history

The bundled Flask Python environment was moved with its lab and is now ignored by Git. The local files remain available; future checkouts should recreate the environment from the lab's `requirements.txt`. Moving a virtual environment may invalidate its absolute interpreter paths, so recreate it before use. No Git history was rewritten.

The existing MLflow backup remains with its lab. Ignore rules exclude new generated dumps, environments, credentials, and Terraform state.

The original homepage's link to a missing `LICENSE` was removed. No new license was chosen.

Existing technical content was retained. This reorganization does not certify that the old commands, tool versions, or configurations work in current environments. Labs and cloud workflows were not executed as part of the move.

## Keeping this organized

Follow [the daily workflow](../CONTRIBUTING.md). `LATEST.md` is the reading queue and learning history; Git remains the complete change history. The initial queue uses actual commit dates and does not pretend the reorganization date is when the material was learned.
