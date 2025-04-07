import os
import re

folders = ["books", "articles", "podcasts", "videos"]
output_file = "content/strategic-pillars.md"

pillar_blocks = {}
post_ideas = []
personal_reflections = []
framework_impacts = []

pillar_pattern = re.compile(r"📌 \*\*Pillar - (.*?)\*\*: (.+)")
post_pattern = re.compile(r"🗒 \*\*Post Idea\*\*: (.+)")
linked_pillars_pattern = re.compile(r"🔗 \*\*Pillars\*\*: (.+)")
reflection_start = re.compile(r"## Personal Reflections")
impact_start = re.compile(r"## Framework Impact")

post_to_pillars = {}

def extract_section(lines, start_idx):
    section = []
    for line in lines[start_idx + 1:]:
        if line.startswith("## "):
            break
        if line.strip():
            section.append(line.strip())
    return section

for folder in folders:
    if not os.path.isdir(folder):
        continue
    for filename in os.listdir(folder):
        if filename.endswith(".md"):
            with open(os.path.join(folder, filename), "r", encoding="utf-8") as f:
                lines = f.readlines()
                current_post_idea = None
                post_found_in_file = False

                for idx, line in enumerate(lines):
                    pillar_match = pillar_pattern.search(line)
                    if pillar_match:
                        pillar = pillar_match.group(1).strip()
                        content = pillar_match.group(2).strip()
                        pillar_blocks.setdefault(pillar, []).append(f"- {content}")

                    post_match = post_pattern.search(line)
                    if post_match:
                        current_post_idea = post_match.group(1).strip()
                        post_found_in_file = True

                    pillar_links = linked_pillars_pattern.search(line)
                    if pillar_links and current_post_idea:
                        linked = [p.strip() for p in pillar_links.group(1).split(",")]
                        post_to_pillars[current_post_idea] = linked
                        post_ideas.append((current_post_idea, linked))
                        current_post_idea = None

                    if reflection_start.search(line):
                        personal_reflections.extend(extract_section(lines, idx))

                    if impact_start.search(line):
                        framework_impacts.extend(extract_section(lines, idx))

                if post_found_in_file and current_post_idea:
                    print(f"⚠️  Warning: Post idea '{current_post_idea}' in '{filename}' is missing a linked 🔗 **Pillars** reference.")

# Write the output
with open(output_file, "w", encoding="utf-8") as f:
    f.write("# Strategic Pillars Output\n\n")
    f.write("_Auto-generated from content notes. Grouped by pillar with post ideas linked._\n\n")

    f.write("## 🔹 Pillar Highlights\n\n")
    for pillar, entries in sorted(pillar_blocks.items()):
        f.write(f"### {pillar}\n")
        for e in entries:
            f.write(f"{e}\n")
        for post, linked_pillars in post_to_pillars.items():
            if pillar in linked_pillars:
                f.write(f"- 📝 Post: *{post}*\n")
        f.write("\n")

    f.write("## 🧠 Post Ideas (With Pillar Links)\n\n")
    for post, linked in sorted(post_ideas):
        f.write(f"- *{post}*  \n  🔗 Pillars: {', '.join(linked)}\n")

    f.write("\n## 🪞 Personal Reflections\n\n")
    if personal_reflections:
        for item in personal_reflections:
            f.write(f"- {item}\n")
    else:
        f.write("- No reflections found.\n")

    f.write("\n## 🏗️ Framework Impact\n\n")
    if framework_impacts:
        for item in framework_impacts:
            f.write(f"- {item}\n")
    else:
        f.write("- No framework impact items found.\n")

    f.write("\n## ⚠️ Diagnostics\n")
    missing_links = [
        post for post, linked in post_ideas
        if not linked or all(p not in pillar_blocks for p in linked)
    ]
    if missing_links:
        for post in missing_links:
            f.write(f"- Missing pillar link for: *{post}*\n")
    else:
        f.write("- All post ideas are properly linked.\n")

