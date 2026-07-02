def calculate_score(price, reviews, rating=0):
    """
    Calculate Niche Score.

    Returns:
        dict containing:
        - total_score
        - review_score
        - price_score
        - rating_score
        - competition
        - opportunity
    """

    # -------------------------
    # Review Score (0-50)
    # -------------------------
    if reviews >= 1000:
        review_score = 50
    elif reviews >= 500:
        review_score = 38
    elif reviews >= 100:
        review_score = 25
    else:
        review_score = 8

    # -------------------------
    # Price Score (0-30)
    # -------------------------
    if 18 <= price <= 28:
        price_score = 30
    elif 15 <= price <= 35:
        price_score = 22
    elif 10 <= price <= 40:
        price_score = 15
    else:
        price_score = 8

    # -------------------------
    # Rating Score (0-20)
    # -------------------------
    if rating >= 4.8:
        rating_score = 20
    elif rating >= 4.5:
        rating_score = 15
    elif rating >= 4.0:
        rating_score = 10
    elif rating >= 3.5:
        rating_score = 5
    else:
        rating_score = 0

    total_score = review_score + price_score + rating_score

    # -------------------------
    # Competition Level
    # -------------------------
    if reviews >= 1000:
        competition = "Very High"
    elif reviews >= 700:
        competition = "High"
    elif reviews >= 300:
        competition = "Medium"
    else:
        competition = "Low"

    # -------------------------
    # Opportunity Rating
    # -------------------------
    if total_score >= 90:
        opportunity = "Excellent"
    elif total_score >= 75:
        opportunity = "Very Good"
    elif total_score >= 60:
        opportunity = "Good"
    elif total_score >= 40:
        opportunity = "Average"
    else:
        opportunity = "Weak"

    return {
        "total_score": total_score,
        "review_score": review_score,
        "price_score": price_score,
        "rating_score": rating_score,
        "competition": competition,
        "opportunity": opportunity
    }

