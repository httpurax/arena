# Git Push Troubleshooting

## 1. rejected: non-fast-forward
- Cause: Remote contains commits not present locally.
- Fix: Run `git pull --rebase`, then `git push`.

## 2. Permission denied (publickey)
- Cause: SSH key not authorized on the remote.
- Fix: Add your SSH key or switch to HTTPS.

## 3. remote: Repository not found
- Cause: Wrong URL or insufficient permissions.
- Fix: Verify remote URL with `git remote -v` and access rights.

## 4. fatal: The current branch has no upstream branch
- Cause: No tracking branch configured.
- Fix: Run `git push -u origin <branch>`.

## 5. error: failed to push some refs
- Cause: Push rejected due to conflicts or missing updates.
- Fix: Pull, resolve conflicts, then push again.
