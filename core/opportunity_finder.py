from scoring import calculate_score
from product_utils import product_to_dict


def find_hidden_opportunities(products):
    opportunities = []

    for product in products:
        product_data = product_to_dict(product)
        title = product_data["title"]
        platform = product_data["platform"]
        price = product_data["price"]
        reviews = product_data["reviews"]
        rating = product_data["rating"]
        score = calculate_score(price, reviews, rating, platform)

        is_good_score = score["overall_score"] >= 65
        is_healthy_price = score["price_score"] >= 75
        has_demand_signal = score["demand_score"] >= 50
        has_usable_confidence = score["confidence"] in ("High", "Medium")

        if is_good_score and is_healthy_price and has_demand_signal and has_usable_confidence:
            opportunities.append({
                "title": title,
                "platform": platform,
                "price": price,
                "reviews": reviews,
                "rating": rating,
                "currency": product_data["currency"],
                "listing_id": product_data["listing_id"],
                "product_url": product_data["product_url"],
                "image_url": product_data["image_url"],
                "shop_name": product_data["shop_name"],
                "shop_url": product_data["shop_url"],
                "score": score,
                "reasons": [
                    f"Overall score: {score['overall_score']}/100 ({score['score_label']})",
                    f"Demand score: {score['demand_score']}/100",
                    f"Price score: {score['price_score']}/100",
                    f"Competition score: {score['competition_score']}/100",
                    f"Data confidence: {score['confidence']}",
                ]
            })

    return opportunities