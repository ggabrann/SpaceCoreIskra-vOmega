# SpaceCore Iskra v4.0.0 Manual Release Guide

The automated script provided for the "MEGA-CANON" rollout depends on GitHub CLI access and an authenticated environment. This guide captures the exact procedure so it can be executed in a fully privileged shell.

## Prerequisites
- GitHub CLI (`gh`) authenticated for the `ggabrann/SpaceCoreIskra-vOmega` repository with permission to merge pull requests and create releases.
- Local checkout that already contains the `canon/v4.0` pull request branch and passes CI.
- `make` tooling and Python environment prepared to run the existing project release pipeline.

## Step-by-step Procedure
1. **Merge the canonical PR**
   ```bash
   gh pr merge -R ggabrann/SpaceCoreIskra-vOmega canon/v4.0 --squash --delete-branch
   ```
   Ensure the PR is green in CI before running the command.

2. **Update `main` and build the release archive**
   ```bash
   git fetch origin
   git checkout main
   git pull
   make release
   ```
   The `make release` target must produce `Iskra_v4.0.0_MAXIMAL_CANON.zip` and include `KNOWLEDGE_BASE_FULL_V4.txt`.

3. **Publish the GitHub release**
   ```bash
   gh release create v4.0.0 Iskra_v4.0.0_MAXIMAL_CANON.zip \
     -t "v4.0.0" \
     -n "SpaceCore Iskra v4.0.0 (MEGA-CANON Release)" \
     -b "MAXIMAL DENSITY Release. All knowledge consolidated. Archive size constraint met."
   ```
   Verify the archive exists and is at least 5 MB before publishing.

## Notes on the Current Automation Environment
- The managed workspace used for this task does not ship with authenticated GitHub CLI access, so the merge and release steps cannot run directly here.
- All commands above should be executed in a trusted environment that already satisfies the authentication and network requirements.
- After completing the release, record the outcome in the appropriate journals (`JOURNAL.jsonl`, `SHADOW_JOURNAL.jsonl`) and update the decision log as per the project guardrails.

## Verification Checklist
- [ ] Pull request `canon/v4.0` merged into `main` with squash commit.
- [ ] `main` branch contains the latest release artifacts and passes `make ci`.
- [ ] `Iskra_v4.0.0_MAXIMAL_CANON.zip` generated and size ≥ 5 MB.
- [ ] GitHub release `v4.0.0` published with the archive attached.
- [ ] Journals and decision logs updated to reflect the release.
