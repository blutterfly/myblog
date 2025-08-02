
import streamlit as st
import os
import re
import yaml
from pathlib import Path

DOCS_DIR = Path("docs/myblog")
MKDOCS_YML = "mkdocs.yml"

def title_to_filename(title):
    return re.sub(r'\s+', '', title.title()) + ".md"

def search_blogs(keyword):
    results = []
    for md_file in DOCS_DIR.glob("*.md"):
        with open(md_file, "r") as f:
            content = f.read()
        if keyword.lower() in content.lower():
            results.append(md_file.name)
    return results

# Compact UI
st.text("📝 MyBlog Editor")

# Blog selection
blog_files = sorted(DOCS_DIR.glob("*.md"))
blog_titles = [f.stem for f in blog_files]
selected_file = st.selectbox("Select Blogs", ["(new)"] + blog_titles)
editing = selected_file != "(new)"

# Load existing
if editing:
    with open(DOCS_DIR / f"{selected_file}.md", "r") as f:
        content = f.read()
    if content.startswith("---"):
        _, meta_block, body = content.split('---', 2)
        metadata = yaml.safe_load(meta_block)
        title = metadata.get("title", selected_file)
    else:
        title, body = selected_file, content
else:
    title, body = "", ""

# Edit Title and Body
title = st.text_input("Title", value=title)
body = st.text_area("Content in Markdown", value=body, height=500)

# Save
if st.button("Save"):
    if not title.strip():
        st.error("Title cannot be empty.")
    else:
        filename = title_to_filename(title)
        metadata = { "title": title }
        content = f"---\n{yaml.dump(metadata)}---\n{body.strip()}"
        with open(DOCS_DIR / filename, "w") as f:
            f.write(content)
        st.success(f"Saved: {filename}")

# Search
st.text("Search Blog Content")
search_term = st.text_input("Search String")
if search_term:
    matches = search_blogs(search_term)
    if matches:
        st.write(f"Found {len(matches)} matches:")
        for match in matches:
            st.markdown(f"- [{match}](myblog/{match})")
    else:
        st.warning("No matches found.")
