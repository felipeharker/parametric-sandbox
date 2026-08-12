import os
import re
import shutil
import zipfile
import csv

def generate_site():
    web_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(web_dir)
    scripts_dir = os.path.join(repo_root, '2_grasshopper_scripts', '0_scripts')
    userobjs_dir = os.path.join(repo_root, '2_grasshopper_scripts', '1_userobjects')
    samples_dir = os.path.join(repo_root, '2_grasshopper_scripts', '2_documentation', 'samples')

    downloads_dir = os.path.join(web_dir, 'downloads')
    images_dir = os.path.join(web_dir, 'images')

    os.makedirs(downloads_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)

    # 1. Create Zip file
    zip_path = os.path.join(downloads_dir, 'alexandria_app.zip')
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for folder in [scripts_dir, userobjs_dir]:
            folder_name = os.path.basename(folder)
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.join(folder_name, os.path.relpath(file_path, folder))
                    zipf.write(file_path, arcname)

    # 2. Gather components from CSV
    csv_path = os.path.join(web_dir, 'component_lib.csv')
    categories = {}

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, skipinitialspace=True)
        for row in reader:
            category = row['category'].strip()
            # If the user changed the name or extension, we'll try to present the script file name without extension
            component_file = row['component'].strip()
            basename = os.path.splitext(component_file)[0]

            name = row.get('web name', component_file).strip()

            img_file = row['img file'].strip()
            description = row['description'].strip()

            has_image = False
            if img_file:
                src_png = os.path.join(samples_dir, img_file)
                if os.path.exists(src_png):
                    dst_png = os.path.join(images_dir, img_file)
                    shutil.copy2(src_png, dst_png)
                    has_image = True

            if category not in categories:
                categories[category] = []

            categories[category].append({
                'name': name,
                'description': description,
                'image': img_file if has_image else None
            })

    # Sort components by name in each category (if not already handled)
    for cat in categories:
        categories[cat] = sorted(categories[cat], key=lambda x: x['name'])

    # 3. Generate HTML
    html_categories = []
    for cat_name in sorted(categories.keys()):
        html_categories.append(f'<div class="category"><h2 class="category-title">{cat_name}</h2>')
        for comp in categories[cat_name]:
            html_categories.append('<div class="component">')
            html_categories.append(f'<div class="component-header"><h3 class="component-title">{comp["name"]}</h3><span class="component-icon">▼</span></div>')
            html_categories.append('<div class="component-content">')
            if comp['description']:
                html_categories.append(f'<p>{comp["description"]}</p>')
            if comp['image']:
                html_categories.append(f'<img class="component-image" src="images/{comp["image"]}" alt="{comp["name"]} Image">')
            html_categories.append('</div>')
            html_categories.append('</div>')
        html_categories.append('</div>')

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Parametric Sandbox</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <h1 class="logo">Parametric Sandbox</h1>
        <nav>
            <a href="index.html">Home</a>
            <a href="https://github.com/felipeharker/parametric-sandbox" target="_blank">Project GitHub</a>
            <a href="downloads/alexandria_app.zip" download>Download App</a>
        </nav>
    </header>
    <main>
        {"".join(html_categories)}
    </main>

    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            const headers = document.querySelectorAll('.component-header');
            headers.forEach(header => {{
                header.addEventListener('click', () => {{
                    const component = header.parentElement;
                    component.classList.toggle('active');
                }});
            }});
        }});
    </script>
</body>
</html>
"""
    with open(os.path.join(web_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("Build successful.")

if __name__ == "__main__":
    generate_site()
