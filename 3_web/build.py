import os
import re
import shutil
import zipfile

def extract_metadata_from_python(filepath):
    name = None
    description = None
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Try to find ghenv.Component.Name
    name_match = re.search(r'ghenv\.Component\.Name\s*=\s*["\']([^"\']+)["\']', content)
    if name_match:
        name = name_match.group(1)

    # Try to find ghenv.Component.Description
    desc_match = re.search(r'ghenv\.Component\.Description\s*=\s*["\']([^"\']+)["\']', content)
    if desc_match:
        description = desc_match.group(1)

    return name, description

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

    # 2. Gather components
    categories = {}
    for category in os.listdir(scripts_dir):
        category_path = os.path.join(scripts_dir, category)
        if os.path.isdir(category_path):
            components = []
            for file in os.listdir(category_path):
                if file.endswith('.py') or file.endswith('.cs'):
                    filepath = os.path.join(category_path, file)
                    basename = os.path.splitext(file)[0]

                    name = basename
                    description = ""

                    if file.endswith('.py'):
                        n, d = extract_metadata_from_python(filepath)
                        if n: name = n
                        if d: description = d

                    # Check for image
                    png_filename = f"{basename}.png"
                    src_png = os.path.join(samples_dir, png_filename)
                    has_image = False
                    if os.path.exists(src_png):
                        dst_png = os.path.join(images_dir, png_filename)
                        shutil.copy2(src_png, dst_png)
                        has_image = True

                    components.append({
                        'name': name,
                        'description': description,
                        'image': png_filename if has_image else None
                    })
            if components:
                categories[category] = sorted(components, key=lambda x: x['name'])

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
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            color: #333;
            background-color: #f9f9f9;
        }}
        header {{
            background-color: #fff;
            padding: 1rem;
            border-bottom: 1px solid #ddd;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }}
        .logo {{
            font-size: 1.25rem;
            font-weight: bold;
            margin: 0;
        }}
        nav {{
            display: flex;
            gap: 1rem;
        }}
        nav a {{
            text-decoration: none;
            color: #0066cc;
            font-weight: 500;
        }}
        nav a:hover {{
            text-decoration: underline;
        }}
        main {{
            max-width: 800px;
            margin: 2rem auto;
            padding: 0 1rem;
        }}
        .category {{
            margin-bottom: 2rem;
        }}
        .category-title {{
            text-transform: capitalize;
            border-bottom: 2px solid #333;
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
        }}
        .component {{
            background: #fff;
            border: 1px solid #ddd;
            border-radius: 4px;
            margin-bottom: 0.5rem;
            overflow: hidden;
        }}
        .component-header {{
            padding: 1rem;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #fff;
            transition: background-color 0.2s;
        }}
        .component-header:hover {{
            background-color: #f1f1f1;
        }}
        .component-title {{
            margin: 0;
            font-size: 1rem;
        }}
        .component-icon {{
            font-size: 0.8rem;
            color: #666;
            transition: transform 0.2s;
        }}
        .component.active .component-icon {{
            transform: rotate(180deg);
        }}
        .component-content {{
            display: none;
            padding: 1rem;
            border-top: 1px solid #ddd;
        }}
        .component.active .component-content {{
            display: block;
        }}
        .component-image {{
            max-width: 100%;
            height: auto;
            margin-top: 1rem;
            border-radius: 4px;
            border: 1px solid #eee;
        }}
        @media (max-width: 600px) {{
            header {{
                flex-direction: column;
                align-items: flex-start;
                gap: 1rem;
            }}
        }}
    </style>
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
