# Project Guidelines: Sobha Neopolis Real Estate Tracker

## 🧪 Mandatory Unit Testing & Anti-Regression Rules

### 1. Test Driven Additions
- Whenever new features, endpoints, scraper logic, calculation rules, or UI components are added or modified, corresponding unit tests **MUST** be added:
  - **Python Backend / Crawler**: Add unit test cases in `test_crawler.py` using `unittest`.
  - **JavaScript Frontend / Utility Logic**: Add unit test cases in `test_frontend.js` using Node.js test runner (`node --test`).

### 2. Pre-Commit Regression Execution
- Before committing or deploying any code changes, the complete unit test suite **MUST** be executed locally:
  ```bash
  python3 -m unittest test_crawler.py && node test_frontend.js
  ```
- **Rule**: All existing unit tests MUST pass with 0 failures before committing.

### 3. Data Integrity & Schema Contracts
- `sobha_listings.json`, `sobha_history.json`, and `purchases.json` must strictly adhere to their required property schemas.
- If a schema change is intentional, update `test_crawler.py` schema assertions to validate the new structure.
- Never comment out, delete, or swallow failing test assertions.

### 4. CI Workflow Protection
- Continuous Integration in `.github/workflows/daily_crawler.yml` automatically runs `test_crawler.py` and `test_frontend.js` on every `push` and `pull_request`.
- A failing test block will halt the CI pipeline and prevent invalid updates from reaching production.
