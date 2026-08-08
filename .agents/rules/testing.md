---
description: Enforce unit testing for new additions and prevent regression of existing tests
always_on: true
---

# Rule: Mandatory Unit Testing & Anti-Regression

1. **New Addition Rule**: For any new functionality added to the codebase (Python scraper or JS frontend), unit tests MUST be written in `test_crawler.py` or `test_frontend.js`.
2. **Regression Check Rule**: Always run `python3 -m unittest test_crawler.py && node test_frontend.js` before declaring a task complete or committing changes.
3. **No Breaking Changes**: Existing tests must never be deleted or commented out to bypass failures. Fix the root cause.
