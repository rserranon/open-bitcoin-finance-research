import os
import re

# Where your markdown files live
folders = ["books", "articles", "podcasts", "videos"]
output_file = "content/strategic-pillars.md"

pillar_blocks = {}
post_ideas = []

# Patterns
pillar_pattern = re.compile(r"📌 \*\*Pillar - (.*?)\*\*: (.+)")
post_pattern = re.compile(r"🗒 \*\*Post Idea\*\*: (.+)")
linked_pillars_pattern = re.compile(r"🔗 \*\*Pillars\*\*: (.+)")

# Temp store for post idea -> pillar links
post_to_pillars = {}

for folder in folders:
    if not os.path.isdir(folder):
        continue
    for filename in os.listdir(folder):
        if filename.endswith(".md"):
            with open(os.path.join(folder, filename), "r", encoding="utf-8") as f:
                lines = f.readlines()

                current_post_idea = None

                for line in lines:
                    # Pillar highlights
                    pillar_match = pillar_pattern.search(line)
                    if pillar_match:
                        pillar = pillar_match.group(1).strip()
                        content = pillar_match.group(2).strip()
                        pillar_blocks.setdefault(pillar, []).append(f"- {content}")

                    # Post idea
                    post_match = post_pattern.search(line)
                    if post_match:
                        current_post_idea = post_match.group(1).strip()

                    # Pillars linked to post
                    pillar_links = linked_pillars_pattern.search(line)
                    if pillar_links and current_post_idea:
                        linked = [p.strip() for p in pillar_links.group(1).split(",")]
                        post_to_pillars[current_post_idea] = linked
                        post_ideas.append((current_post_idea, linked))
                        current_post_idea = None  # Reset to prevent carry-over

# Write final output
with open(output_file, "w", encoding="utf-8") as f:
    f.write("# Strategic Pillars\n\n")

    # Write pillar blocks
    for pillar, entries in pillar_blocks.items():
        f.write(f"## {pillar}\n")
        for e in entries:
            f.write(f"{e}\n")

        # Add post ideas linked to this pillar
        for post, linked_pillars in post_to_pillars.items():
            if pillar in linked_pillars:
                f.write(f"- 📝 Post: *{post}*\n")
        f.write("\n")

    # Global post idea list
    f.write("## Post Ideas\n\n")
    for post, linked in post_ideas:
        f.write(f"- *{post}*  \n  🔗 Pillars: {', '.join(linked)}\n")

