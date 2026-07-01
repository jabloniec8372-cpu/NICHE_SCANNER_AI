import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
KNOWLEDGE_BASE_PATH = PROJECT_ROOT / "core" / "knowledge" / "knowledge_base.json"


def load_knowledge_base():
    with open(KNOWLEDGE_BASE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def detect_topic(title):
    knowledge_base = load_knowledge_base()
    title = title.lower()

    for main_topic, groups in knowledge_base.items():
        for subtopic, keywords in groups.items():
            for keyword in keywords:
                if keyword in title:
                    return main_topic, subtopic, keyword

    return "unknown", "unknown", "unknown"
