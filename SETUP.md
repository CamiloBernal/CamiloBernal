# Setup Guide — CamiloBernal GitHub Profile README

This guide explains how to configure all required secrets, run workflows manually, and verify the deployment.

---

## Prerequisites

- Admin access to the [CamiloBernal/CamiloBernal](https://github.com/CamiloBernal/CamiloBernal) repository.
- A [daily.dev](https://app.daily.dev) account with a DevCard generated.
- A GitHub account with permission to create Personal Access Tokens.

---

## Step 1: Configure Repository Secrets

Navigate to: **Repository → Settings → Secrets and variables → Actions → New repository secret**

### Required Secrets

| Secret Name  | Description | Manual Setup Required |
|--------------|-------------|----------------------|
| `GITHUB_TOKEN` | Auto-provided by GitHub Actions. No setup needed. Ensure the workflow has `contents: write` permission (already configured in the workflow YAML). | No |
| `GH_TOKEN` | Personal Access Token (PAT) for GitHub GraphQL/Events API. Needed by `update_activity.py`. | **Yes** |
| `USER_ID` | Your daily.dev DevCard User ID. Needed by `devcard.yml`. | **Yes** |

### How to Create GH_TOKEN

1. Go to: **GitHub → Settings → Developer Settings → Personal Access Tokens → Fine-grained tokens**
2. Click **Generate new token**
3. Set expiration (recommend: 1 year)
4. Repository access: Select **CamiloBernal/CamiloBernal** only (or All repositories)
5. Permissions required:
   - **Contents**: Read-only
   - **Metadata**: Read-only (mandatory)
6. Click **Generate token**
7. Copy the token value and save it as `GH_TOKEN` in repository secrets.

### How to Find USER_ID for daily.dev

1. Go to [https://app.daily.dev/camilobernal](https://app.daily.dev/camilobernal)
2. Navigate to your profile → **DevCard**
3. The DevCard image URL format is: `https://api.daily.dev/devcards/{USER_ID}.png`
4. Copy the `{USER_ID}` portion of the URL.
5. Save it as `USER_ID` in repository secrets.

---

## Step 2: Initial File Setup

The following files must exist before workflows run correctly:

### devcard.png

The `devcard.yml` workflow will automatically create and update `devcard.png`. However, for the README to render on first load, you need a placeholder.

**Option A**: Run the `devcard.yml` workflow manually after setting `USER_ID`:

```
GitHub → Actions → Update daily.dev DevCard → Run workflow
```

**Option B**: Commit a placeholder PNG at `devcard.png` in the root.

### Snake SVG Files

The `snake.yml` workflow generates SVG files and pushes them to the `output` branch. Run it manually after initial setup:

```
GitHub → Actions → Generate Contribution Snake Animation → Run workflow
```

The README references these via:
```
https://raw.githubusercontent.com/CamiloBernal/CamiloBernal/output/github-contribution-grid-snake-dark.svg
https://raw.githubusercontent.com/CamiloBernal/CamiloBernal/output/github-contribution-grid-snake.svg
```

---

## Step 3: Run Workflows Manually (Initial Verification)

Run each workflow in this order to verify everything works:

1. **Snake animation**: `Actions → Generate Contribution Snake Animation → Run workflow`
2. **DevCard update**: `Actions → Update daily.dev DevCard → Run workflow`
3. **README update**: `Actions → Update README — Daily Stats & Content → Run workflow`

Check workflow run logs for any errors.

---

## Step 4: Configure Repository Metadata

In the repository main page:

1. Click the gear icon next to **About**
2. Set **Description**: `Solution Architect | +23 years | FinTech · AI · Cloud Native | Bogotá, Colombia`
3. Set **Website**: `https://www.camilobernal.dev`
4. Add **Topics**:
   - `personal-portfolio`
   - `readme-profile`
   - `solution-architect`
   - `cloud-native`
   - `fintech`
   - `ai-enthusiast`
   - `platform-engineering`
   - `microservices`
   - `developer-profile`
   - `colombia`

---

## Step 5: Pin Featured Repositories

In your GitHub profile settings, pin the following repositories (max 6):

1. `platform-builder`
2. `architype`
3. `hololife`
4. Up to 3 more with the highest stars or most recent activity

---

## Step 6: Verify Deployment

After all workflows have run, verify:

- [ ] README renders correctly on [github.com/CamiloBernal](https://github.com/CamiloBernal)
- [ ] Typing animation SVG loads at the top
- [ ] Profile photo (Funko) is visible and links to camilobernal.dev
- [ ] All badges render with correct colors
- [ ] GitHub stats cards load (may take a few seconds)
- [ ] Snake animation is visible
- [ ] DevCard image loads (links to daily.dev)
- [ ] Blog posts section shows latest 3 articles (or fallback text)
- [ ] Activity section shows recent GitHub events (or fallback text)
- [ ] No broken image links

---

## Scheduled Automation

All workflows run automatically on schedule:

| Workflow | Schedule | Cron |
|----------|----------|------|
| Update README (stats + blog + activity) | Daily at 6:00 AM COT | `0 11 * * *` |
| Update daily.dev DevCard | Daily at 6:00 AM COT | `0 11 * * *` |
| Generate Snake Animation | Daily at 7:00 AM COT | `0 12 * * *` |
| Dependabot (Actions updates) | Weekly | Automatic |

---

## Troubleshooting

### Stats cards show "not found" or are blank

- GitHub readme-stats caches results. Wait a few minutes and hard-refresh.
- Ensure the username `CamiloBernal` is spelled correctly (case-sensitive in some services).

### Snake animation not loading

- Verify the `output` branch exists after running the snake workflow.
- Check workflow logs for permission errors. Ensure `contents: write` is set.

### DevCard shows a broken image

- Confirm `USER_ID` secret is set correctly in repository secrets.
- Run the `devcard.yml` workflow manually and check logs.

### Blog posts not updating

- Verify `https://blog.camilobernal.dev/rss.xml` is publicly accessible.
- Check workflow run logs for the `update_blog_posts.py` step.

### Activity not updating

- Confirm `GH_TOKEN` is set and has not expired.
- The token needs `Contents: Read` and `Metadata: Read` permissions.

---

## File Structure

```
CamiloBernal/                          # Profile repo root
├── README.md                          # Main profile (auto-updated daily)
├── devcard.png                        # daily.dev DevCard (auto-updated daily)
├── llms.txt                           # AI agent discoverability (short)
├── llms-full.txt                      # AI agent full context (RAG)
├── .markdownlint.json                 # Markdownlint config
├── SETUP.md                           # This file
├── .github/
│   ├── dependabot.yml                 # Auto-update Actions versions
│   └── workflows/
│       ├── update-readme.yml          # Master daily update workflow
│       ├── devcard.yml                # daily.dev DevCard updater
│       └── snake.yml                  # Contribution snake generator
├── scripts/
│   ├── update_blog_posts.py           # RSS → README injector
│   └── update_activity.py            # GitHub Events → README injector
├── backups/
│   ├── .gitkeep
│   └── README.backup.md              # Previous README (auto-backup)
├── output/
│   ├── .gitkeep                       # Placeholder (snake SVGs pushed to output branch)
└── public/
    └── images/
        └── camilobernal-geek-funko.png  # Profile avatar (DO NOT overwrite)
```

---

*Built with 💜 from Bogotá, Colombia 🇨🇴 | Automated with GitHub Actions 🤖*
