import json

with open("data/raw/alternatives.json", "r") as f:
    doc = json.load(f)

content = doc["content"]
raw_chunks = content.split("\n\n")
merged_chunks = []
current = ""

for piece in raw_chunks:
    if len((current + " " + piece).split()) < 200:
        current = current + "\n\n" + piece if current else piece
    else:
        if current:
            merged_chunks.append(current)
        current = piece

if current:
    merged_chunks.append(current)

for i, chunk in enumerate(merged_chunks):
    print(f"--- Chunk {i} ({len(chunk.split())} words) ---")
    print(chunk[:200])
    print()

    chunk_data = []


for i, chunk in enumerate(merged_chunks):
    chunk_data.append({
        "chunk_id": f"{doc['title']}_{i}",
        "text": chunk,
        "source_url": doc["url"],
        "page_title": doc["title"],
        "word_count": len(chunk.split()),
        "chunk_index": i,
    })

with open("data/processed/first-steps_chunks.json", "w") as f:
    json.dump(chunk_data, f, indent=2)

print(f"Created {len(chunk_data)} chunks")