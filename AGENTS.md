# Contributor instructions

Keep changes focused and retain release archive licenses and notices. Each PR requires independent docs, tests and simplicity reviews, successful final-head CI, and a final simplicity follow-up on coverage scope. Use the [Kaferry review process](https://github.com/pagrus7/kaferry/blob/main/review/README.md) and its role criteria. Formula-only and Python changes have Go patch coverage N/A; record the compared SHAs and complete changed-file list. Do not claim checks that did not run.

Keep PR descriptions below 2,000 characters with exactly one Changes, Validation, Docs review, Tests review and Simplicity review section. Validation lists only checks beyond CI. Review sections contain Passed, Pending or Failed: reason. Ready PRs require Passed in all three sections. Preserve existing changes. Merge and publish only when requested.
