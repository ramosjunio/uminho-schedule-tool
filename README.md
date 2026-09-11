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

```text
https://<your-username>.github.io/uminho-schedule-tool/out.ics