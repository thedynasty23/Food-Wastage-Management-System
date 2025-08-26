# Food Wastage Management System

A Streamlit-based data app to manage surplus food donations and reduce waste by connecting **Providers** (restaurants, events, households) with **Receivers** (NGOs, shelters). It supports CRUD operations, simple claims workflow, analytics/graphs, and SQL utilities on top of an included SQLite database and CSV sample data.

> Demo-ready: comes with seed CSVs and a bundled SQLite DB so you can run locally without setup.

---

## ✨ Features

- **Providers & Receivers**: Add, edit, delete entities.
- **Food Listings**: Publish available food with quantities, timings, and locations.
- **Claims**: Receivers can claim listings; track claim status.
- **Analytics**: Basic charts/graphs to monitor activity and impact.
- **SQL Utilities**: Reusable queries and CRUD helpers.
- **Bundled Data**: Sample CSVs + a prebuilt SQLite DB for quick start.

---

## 📁 Repository Structure

```
.
├── app (10).py                 # Main Streamlit app
├── crud (3).py                 # CRUD helper functions
├── graphs (3).py               # Charting/analytics helpers
├── sql_queries (3).py          # Reusable SQL queries
├── food_waste%20 (2).db        # SQLite database (filename contains a space)
├── providers_data (1).csv      # Seed data: providers
├── receivers_data (1).csv      # Seed data: receivers
├── food_listings_data (1).csv  # Seed data: food listings
├── claims_data (1).csv         # Seed data: claims
├── requirements (4).txt        # Python dependencies
└── REPORT (1).md               # Project write-up (optional reading)
```

> Note: The DB file name includes a space (`food_waste%20 (2).db`). You can rename it to `food_waste.db` and update references in code if you prefer.

---

## 🚀 Quickstart (Local)

1. **Clone & enter the project**
   ```bash
   git clone https://github.com/thedynasty23/Food-Wastage-Management-System.git
   cd Food-Wastage-Management-System
   ```

2. **Create & activate a virtual environment (recommended)**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r "requirements (4).txt"
   ```

4. **Run the app**
   ```bash
   streamlit run "app (10).py"
   ```
   Streamlit will print a local URL (usually `http://localhost:8501`). Open it in your browser.

---

## 🧩 How the App is Organized

- **`app (10).py`**  
  The Streamlit UI: navigation, pages (Providers, Receivers, Listings, Claims, Analytics), and wiring across modules.

- **`crud (3).py`**  
  Functions for creating, reading, updating, deleting entities in the DB.

- **`sql_queries (3).py`**  
  Central place for SQL strings/snippets used by the app.

- **`graphs (3).py`**  
  Helper functions that generate charts/plots for the Analytics section.

- **Data & DB**  
  - `*.csv` files seed the app with example rows so you can explore immediately.  
  - `food_waste%20 (2).db` is a ready-to-use SQLite database.

---

## 📊 Data Model (Typical Fields)

While exact schemas are defined in the code/DB, the app usually manages:
- **Providers**: `provider_id`, `name`, `contact`, `address`, `city`
- **Receivers**: `receiver_id`, `name`, `contact`, `address`, `city`
- **Food Listings**: `listing_id`, `provider_id`, `food_type`, `quantity`, `expiry_time`, `status`
- **Claims**: `claim_id`, `listing_id`, `receiver_id`, `claim_time`, `status`

---

## 🛠 Configuration Tips

- **Database path**: If you rename the DB file, make sure `app (10).py` and helpers point to the new filename.
- **CSV imports**: If the app reads CSV seeds, keep them in the project root (or update paths).

---

## ☁️ Deploying on Hugging Face Spaces (Streamlit)

1. **Create a new Space** → Type: *Streamlit*.
2. **Push your code** (same structure as this repo) to the Space.
3. **Add a `requirements.txt`** (you already have `requirements (4).txt`; consider copying/renaming to `requirements.txt` in the Space).
4. **Set the App file** to `app (10).py` (Spaces settings).
5. Deploy — Spaces will build the environment and launch the Streamlit app.

---

## 🧪 Common Tasks

- **Rename DB to a simpler name**
  ```bash
  mv "food_waste%20 (2).db" food_waste.db
  # then update references in code
  ```

- **Export a fresh DB from CSVs**  
  Use helper functions (in `crud (3).py` / `sql_queries (3).py`) to create tables and load CSVs, or add a small bootstrap script.

---

## 🐞 Troubleshooting

- **Streamlit not found** → Reinstall requirements / check venv activation.  
- **DB file not found** → Confirm the path and that the file name matches exactly (mind spaces).  
- **Graphs not rendering** → Verify the data loading step; check `graphs (3).py` functions.

---

## 📖 Report

A project write-up is included as `REPORT (1).md` if you want to share design notes and results with reviewers.

---

## 🤝 Contributing

PRs and issues are welcome. Please:
1. Fork the repo
2. Create a feature branch
3. Commit with clear messages
4. Open a PR describing the change and testing steps

---

## 📄 License

Add your preferred license (e.g., MIT) in a `LICENSE` file.

---

## 📷 Screenshots (Optional)

Create a folder `assets/` and add:
- `assets/home.png`
- `assets/providers.png`
- `assets/listings.png`
- `assets/analytics.png`

Then embed like:
```markdown
![Home](assets/home.png)
```

---

## 🙌 Acknowledgements

Thanks to all contributors and the open-source community.
