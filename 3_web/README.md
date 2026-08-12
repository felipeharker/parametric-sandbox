# Parametric Sandbox Web

This directory contains the files required for the static website that documents the custom Grasshopper components.

## Building the Website

To build the static files, navigate to this directory and run the `build.py` python script:
```bash
cd 3_web
python3 build.py
```
This script will:
- Zip all the scripts and userobjects into `3_web/downloads/alexandria_app.zip`
- Extract metadata and descriptions from the source files.
- Gather images into `3_web/images/`
- Generate an `index.html` static site.

## Render Hosting Configuration

To host this on Render as a Static Site, use the following configuration settings:

- **Root Directory:** `.` (leave as default root repository path)
- **Build Command:** `cd 3_web && python3 build.py`
- **Publish Directory:** `3_web`

That's it! Render will run the script, generate the files, and serve everything out of the `3_web` directory.
