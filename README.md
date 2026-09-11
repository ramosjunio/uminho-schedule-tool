# UMinho Schedule Tool 📅

A Python tool that scrapes course timetables from the [Universidade do Minho Schedule Portal](https://alunos.uminho.pt/PT/estudantes/Paginas/InfoUteisHorarios.aspx) and exports them into standard `.ics` (iCalendar) and `.json` formats.

> [!NOTE]  
> **Original Work & Attribution:**  
> This project is a fork of [`uminho-schedule-tool`](https://github.com/joaoalves03/uminho-schedule-tool), originally created and developed by **[João Alves (@joaoalves03)](https://github.com/joaoalves03)**. All credit for the core scraping engine, portal form interaction, and schedule parsing belongs to the original author.

---

## ✨ Enhancements in this Fork

This fork builds upon João Alves's original tool by adding automated cloud synchronization and calendar integration:

1. **🤖 Automated Weekly Sync (GitHub Actions):**  
   Runs on a weekly cron schedule (every Saturday morning) to scrape upcoming timetable changes and room reallocations.
2. **🌐 GitHub Pages Calendar Hosting:**  
   Publishes the resulting `.ics` directly to GitHub Pages at a permanent, unauthenticated URL, enabling direct subscription in Google Calendar, Apple Calendar, and Outlook.
3. **🔒 Deterministic RFC-5545 UIDs:**  
   Generates consistent, hash-based event UIDs (`lesson_uid`) so that external calendars correctly track, update, or reschedule existing classes across recurring runs without creating duplicate events.
4. **📝 Human-Readable Class IDs for Notes (Notion):**  
   Adds clean, human-readable tags (e.g., `IO-TP1-20260915-0830` or `CC-PL2-20260915-0830`) directly into the event's visible description field, making it easy to cross-reference lecture notes in Notion or Obsidian.
5. **🛡️ SSL/TLS Intermediate Certificate Workaround:**  
   Resolves the missing intermediate CA certificate issue on UMinho's server (`alunos.uminho.pt`) to ensure clean execution across headless Linux CI environments.
6. **💻 Web Landing Page:**  
   Includes a static dashboard served at the GitHub Pages root with 1-click subscription and direct `.ics`/`.json` downloads.

---

## 📅 Calendar Subscription

Subscribe to your live calendar feed in your calendar app:

`https://<your-username>.github.io/uminho-schedule-tool/out.ics`

### Adding to Google Calendar
1. Open [Google Calendar](https://calendar.google.com) on desktop.
2. In the left sidebar, click **`+`** next to **Other calendars** → **From URL**.
3. Paste the URL above and click **Add calendar**.
4. Google Calendar will periodically fetch updates in the background.

---

## 🍴 Forking & Setting Up for Your Own Course

Want to use this tool for your own degree at UMinho? You can set up your own automated calendar in a few minutes:

1. **Fork this repository** to your own GitHub account.
2. **Configure your degree** in `config.yml`:
   * Change `course_name` to your exact degree name as listed on the UMinho portal (e.g. `"Licenciatura em Engenharia Informática"`).
   * Change `year` to your curricular year (e.g. `1`, `2`, or `3`).
   * Adjust `week.start` and `week.end` dates.
   * Commit and push your changes.
3. **Enable GitHub Actions**:
   * In your fork, click the **Actions** tab at the top.
   * Click the green button: **"I understand my workflows, go ahead and enable them"**.
4. **Run the workflow for the first time**:
   * In the **Actions** tab, click **Update Schedule** on the left.
   * Click **Run workflow** → **Run workflow**.
   * Wait ~1 minute for the run to finish (this creates the `gh-pages` branch).
5. **Activate GitHub Pages**:
   * Go to **Settings** → **Pages** in your repository.
   * Under **Build and deployment** → **Source**, choose **Deploy from a branch**.
   * Select the **`gh-pages`** branch and `/ (root)`, then click **Save**.

Your live calendar feed and landing page will now automatically be hosted at:  
`https://<your-username>.github.io/<your-repo-name>/`

---

## ⚙️ Configuration Reference

Options available in `config.yml`:

```yaml
scraper:
  timeout: 1 # Seconds to wait between weekly requests
  course_name: "Licenciatura em Marketing"
  year: 2
  week:
    start: "2026-09-14"
    end: "2027-06-15"

  # Optional: Filter specific subject names
  # classes:
  #   - "Investigação Operacional"
  #   - "Comportamento do Consumidor"

export:
  json:
    file_name: "out.json"
    indent: true

  ics:
    file_name: "export/out.ics"
```

---

## 🚀 Running Locally

This project uses the [uv package manager](https://docs.astral.sh/uv/):

```bash
# Install dependencies
uv sync --extra ics

# Run scraper
uv run main.py
```

---

## 👥 Credits & Acknowledgments

* **Original Creator:** [João Alves (@joaoalves03)](https://github.com/joaoalves03) — Author of the original [uminho-schedule-tool](https://github.com/joaoalves03/uminho-schedule-tool).
* **Fork Maintainer:** [ramosjunio](https://github.com/ramosjunio) — GitHub Actions CI/CD, GitHub Pages hosting, deterministic UIDs, and Notion reference IDs.
