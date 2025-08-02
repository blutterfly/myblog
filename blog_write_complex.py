
import streamlit as st
import os
import re
import yaml
from pathlib import Path
import datetime
from collections import defaultdict
import subprocess

DOCS_DIR = Path("docs/myblog")
MKDOCS_YML = "mkdocs.yml"

st.set_page_config(layout="wide")
st.text("📝 MyBlog Editor")

def title_to_filename(title):
    return re.sub(r'\s+', '', title.title()) + ".md"

def update_mkdocs_nav_grouped():
    nav = [{"Home": "index.md"}]
    grouped = defaultdict(list)
    for md_file in sorted(DOCS_DIR.glob("*.md")):
        with open(md_file, "r") as f:
            content = f.read()
        if content.startswith("---"):
            _, meta_block, _ = content.split("---", 2)
            meta = yaml.safe_load(meta_block)
            cat = meta.get("category", "Uncategorized")
            grouped[cat].append({meta.get("title", md_file.stem): f"myblog/{md_file.name}"})
    nav.append({"MyBlog": [{cat: posts} for cat, posts in grouped.items()]})
    with open(MKDOCS_YML, "r") as f:
        config = yaml.safe_load(f)
    config["nav"] = nav
    with open(MKDOCS_YML, "w") as f:
        yaml.dump(config, f, sort_keys=False)

def search_blogs(keyword):
    results = []
    for md_file in DOCS_DIR.glob("*.md"):
        with open(md_file, "r") as f:
            content = f.read()
        if keyword.lower() in content.lower():
            results.append(md_file.name)
    return results

blog_files = sorted(DOCS_DIR.glob("*.md"))
blog_titles = [f.stem for f in blog_files]

selected_file = st.selectbox("📂 Edit Existing Blog", ["(new)"] + blog_titles)
editing = selected_file != "(new)"

if editing:
    with open(DOCS_DIR / f"{selected_file}.md", "r") as f:
        content = f.read()
    if content.startswith("---"):
        _, meta_block, body = content.split('---', 2)
        metadata = yaml.safe_load(meta_block)
        title = metadata.get("title", selected_file)
        category = metadata.get("category", "")
        tags = ", ".join(metadata.get("tags", []))
    else:
        title, category, tags, body = selected_file, "", "", content
else:
    title, body, category, tags = "", "", "", ""

# st.text("🖋 Blog Metadata & Content")
title = st.text_input("Title", value=title)
category = st.selectbox("Category", ["", "Tech", "Travel", "Faith", "Diary", "Tutorial"], index=0 if not category else ["", "Tech", "Travel", "Faith", "Diary", "Tutorial"].index(category))

#st.text("📅 Blog Schedule")
publish_date = st.date_input("Publish Date", value=datetime.date.today())
status = st.radio("Status", ["draft", "published"])

body = st.text_area("✍️ Write Your Blog in Markdown", value=body, height=600, max_chars=4800)

st.markdown("---")
st.text("📄 Live Markdown Preview")
st.markdown(body, unsafe_allow_html=False)

tags = st.text_input("Tags (comma-separated)", value=tags)

st.text("🖼 Upload Image to Use in Blog")

image_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg", "gif"])
if image_file:
    image_path = Path("docs/images") / image_file.name
    image_path.parent.mkdir(parents=True, exist_ok=True)
    with open(image_path, "wb") as f:
        f.write(image_file.getbuffer())
    st.image(str(image_path), caption=image_file.name)
    st.code(f"![{image_file.name}](../images/{image_file.name})", language="markdown")
    st.info("📋 Copy and paste the markdown above into your blog content.")


if st.button("💾 Save Blog"):
    if not title.strip():
        st.error("Title cannot be empty.")
    else:
        filename = title_to_filename(title)
        metadata = {
            "title": title,
            "category": category,
            "tags": [t.strip() for t in tags.split(",") if t.strip()],
        "publish_date": str(publish_date),
        "status": status
        }
        content = f"---\n{yaml.dump(metadata)}---\n{body.strip()}"
        with open(DOCS_DIR / filename, "w") as f:
            f.write(content)
        update_mkdocs_nav_grouped()
        st.success(f"✅ Saved: {filename}")

st.text("🔍 Search Blog Content")
search_term = st.text_input("Enter keyword")
if search_term:
    matches = search_blogs(search_term)
    if matches:
        st.success(f"Found {len(matches)} matches:")
        for match in matches:
            st.markdown(f"- [{match}](myblog/{match})")
    else:
        st.warning("No matches found.")

if st.button("🚀 Commit & Push to GitHub"):
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Update blog content"], check=True)
        subprocess.run(["git", "push"], check=True)
        st.success("✅ Changes pushed to GitHub.")
    except subprocess.CalledProcessError as e:
        st.error(f"Git error: {e}")
