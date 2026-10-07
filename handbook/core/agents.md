# Working rules for AI collaborators

These rules hold in every repository. A repository's `AGENTS.md` adds only what is specific to it.

1. **Start from the docs.** Read `AGENTS.md`, then the document the task touches (`docs/spec.md`,
   `docs/design.md`, the ADRs). If the docs and the code disagree, fix the docs first and say so in the PR.
2. **One path for a new feature**: `handbook/playbooks/add-feature.md`. No code before the spec text and, for UI, the
   signed-off screen.
3. **Small pull requests**: ideally under 400 changed lines, one concern each; formatting and logic in
   separate commits. Conventional Commits (`handbook/core/process.md`). AI-assisted commits carry a
   `Co-Authored-By` line.
4. **Work on a branch and open a PR.** CI must be green; merge only as the maintainer has authorized.
5. **A decision that changes an established way of working is an ADR** (`handbook/playbooks/write-adr.md`). A decision
   only the maintainer can make is an issue labelled `needs-decision`: describe the options and their cost,
   recommend one, and wait.
6. **Say what was verified.** Report test results, scan results and what was not run, as they are. Never state
   that something is secure or risk-free without a complete scan or walkthrough.
7. **Red lines**
   - Never write a token, key, passphrase, certificate or customer license key into a PR, issue, log, report
     or chat; refer to it by file path and line.
   - Sending anything to an external service, changing signing or release settings, publishing a release and
     deleting history or branches other than your own need the maintainer's confirmation each time.
   - Never modify a user's dotfiles or global Git configuration.
   - No blind staging (`git add -A`, `git commit -a`): check the file list.
8. **UI work follows the gates in `handbook/guides/ui-workflow.md`.** Never choose a design direction for the maintainer. Never
   mark a screen `signed-off` or `accepted` yourself: record those only on the maintainer's explicit words
   (the review tool writes them to `.design-review/decisions.jsonl`). Develop one screen at a time. When spec,
   design and code disagree, stop and ask. Update the ledger in the same PR as the change it records.
9. **Product names stay in the product's repository.** In handbook, templates and shared code use `<Name>`.
10. **Never change the maintainer's saved settings.** While testing or capturing, set behaviour with launch
    arguments or environment variables only. If a saved default was touched, say so and restore the exact value
    read beforehand. Tests do not depend on the machine's saved settings: pin language, locale and time zone in the
    test host.
11. **Worktree hygiene.** Work in your own git worktree under the shared parent directory. Never remove a worktree
    that has unmerged work. Never `git add -A`.
12. **Do not fake what the environment forbids.** If a step cannot be done (locked screen, missing permission), stop
    and report. Do not produce a substitute artefact.
