# SauceDemo Selenium Framework (Python + pytest + Page Object Model)

One scenario, done the way a real team would do it:
Login → Add item to cart → Checkout → Verify order confirmation.

## Project structure

```
saucedemo-framework/
├── pages/                  # Page Object Model - one class per screen
│   ├── base_page.py        # shared wait/click/type helpers
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── conftest.py         # pytest fixture: creates + quits the browser
│   └── test_checkout_flow.py
├── requirements.txt
├── pytest.ini
├── Jenkinsfile
└── .gitignore
```

**Why Page Object Model?** Each screen of the site becomes a class.
The class holds the locators (IDs, CSS selectors) and the actions you can do
on that screen. Your test then reads like plain English (`login_page.login(...)`)
instead of raw Selenium calls. If SauceDemo changes a button's ID tomorrow,
you fix it in ONE place (the page class) instead of every test that clicks it.

## 1. Run it locally

```bash
cd saucedemo-framework
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
pytest
```

A Chrome window will open, run the scenario, and close. An HTML report
lands at `reports/report.html` — open it in a browser to see a pass/fail
summary, exactly like a real CI dashboard shows.

## 2. Push it to GitHub (how real teams version their framework)

```bash
git init
git add .
git commit -m "Initial framework: login-to-checkout flow with POM"
git branch -M main
git remote add origin https://github.com/<your-username>/saucedemo-framework.git
git push -u origin main
```

From here on, the habit real teams follow:
- Create a branch per change: `git checkout -b add-login-negative-test`
- Commit small, working changes
- Push and open a Pull Request instead of pushing straight to `main`
- Someone reviews it, then it gets merged

## 3. Wire it up to Jenkins (how real teams run it automatically)

1. Install Jenkins (or use a Jenkins instance your org already has).
2. Install the "Git" plugin if not already present.
3. New Item → Pipeline → give it a name.
4. Under "Pipeline", choose "Pipeline script from SCM" → SCM: Git →
   paste your GitHub repo URL → Script Path: `Jenkinsfile`.
5. Before your first build: open `tests/conftest.py` and uncomment
   `options.add_argument("--headless=new")` — Jenkins agents have no
   monitor, so the browser must run headless.
6. Click "Build Now". Jenkins will: pull your code → create a venv →
   install dependencies → run pytest → save the HTML report as a
   build artifact you can download from the Jenkins UI.

That's the same loop (commit → push → CI runs tests → see pass/fail)
that runs behind the scenes at most companies, just smaller.

## 4. Once this clicks

Add one page object + one test at a time for other flows (e.g. sorting
products, removing from cart, a locked-out user login). The pattern
never changes — new page class, new locators, one small test.
