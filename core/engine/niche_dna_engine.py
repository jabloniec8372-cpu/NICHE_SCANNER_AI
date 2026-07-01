from engine.category_engine import detect_product_type
from engine.topic_engine import detect_topic


def build_niche_dna(title):
    product_type = detect_product_type(title)
    main_topic, subtopic, detected_keyword = detect_topic(title)

    return {
        "title": title,
        "product_type": product_type,
        "main_topic": main_topic,
        "subtopic": subtopic,
        "detected_keyword": detected_keyword,
    }