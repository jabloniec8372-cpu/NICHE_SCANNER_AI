from scoring import calculate_score


def find_hidden_opportunities(products):
    opportunities = []

    for product in products:
        title, platform, price, reviews, rating = product
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
                "score": score,
                "reasons": [
                    "Strong demand",
                    "Healthy price range",
                    "Good niche score"
                ]
            })

    return opportunities
