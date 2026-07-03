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
        score = calculate_score(price, reviews, rating)

        is_strong_demand = reviews >= 300
        is_healthy_price = 18 <= price <= 30
        is_good_score = score["total_score"] >= 75

        if is_strong_demand and is_healthy_price and is_good_score:
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
                    "Strong demand",
                    "Healthy price range",
                    "Good niche score"
                ]
            })

    return opportunities
