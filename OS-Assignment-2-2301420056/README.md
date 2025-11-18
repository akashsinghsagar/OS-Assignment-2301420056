

# 1 — Initialize git inside your assignment folder

Make sure you’re in your assignment directory (`~/os_lab2`):

```bash
cd ~/os_lab2
git init
```

# 2 — Add your files

```bash
git add system_startup_sim.py process_log.txt report.md
git commit -m "OS Lab Assignment 2: Process Simulation with multiprocessing"
```

# 3 — Create a GitHub repo

1. Go to [https://github.com/new](https://github.com/new)
2. Fill in:

   * **Repository name**: `os_lab_assignment2` (or any name you like)
   * Public (unless told otherwise)
   * Don’t initialize with README (we already have files)
3. Click **Create repository**.

GitHub will then show you something like:

```
git remote add origin https://github.com/yourusername/os_lab_assignment2.git
git branch -M main
git push -u origin main
```

# 4 — Connect local folder to GitHub

Copy those commands from GitHub page and run them, for example:

```bash
git remote add origin https://github.com/yourusername/os_lab_assignment2.git
git branch -M main
git push -u origin main
```

# 5 — Verify

```bash
git status
```

should show **nothing to commit, working tree clean**.
Then open your repo link in browser — you’ll see:

* `system_startup_sim.py`
* `process_log.txt`
* `report.md`


