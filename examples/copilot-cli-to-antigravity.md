# Conversion Example: GitHub Copilot CLI Skill to Antigravity Skill

---

## 1. Original Copilot CLI Skill (`.github/skills/docker-deploy/SKILL.md`)

```markdown
---
name: docker-deploy
description: Build and push container images
tags: docker, deployment, devops
---

# Docker Deployment

Deploy containerized services.

## Steps
1. Execute `docker build -t app:latest .` using the shell.
2. Tag the container for the remote registry.
3. Push to registry using shell command.
```

---

## 2. Converted Antigravity Skill (`.agents/skills/docker-deploy/SKILL.md`)

```markdown
---
name: docker-deploy
description: >-
  Builds, tags, and deploys Docker container images to remote container registries.
  Use when deploying services, building containers, or running docker workflows.
  Triggers include: "docker build", "docker deploy", "container push", "deploy image".
---

# Docker Deployment Skill

Standardized container build and deployment procedure with validation checks.

## Workflow

1. **Build Container Image**:
   Use `run_command` with synchronous wait to trigger build:
   ```bash
   docker build -t app:latest .
   ```

2. **Tag Image**:
   Apply registry tag:
   ```bash
   docker tag app:latest <registry_url>/app:<version>
   ```

3. **Push Image**:
   Push to registry using `run_command`:
   ```bash
   docker push <registry_url>/app:<version>
   ```

4. **Verify Deployment**:
   Inspect status or query container digest upon successful upload.
```
