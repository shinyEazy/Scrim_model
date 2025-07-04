import json

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("qa.txt", "w", encoding="utf-8") as f:
    f.write(data.get("choices")[0].get("message").get("content"))

with open("qa.txt", "r", encoding="utf-8") as f:
    qa = f.read()

print(qa)
