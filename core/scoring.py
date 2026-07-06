CONFIDENCE_SCORES = {
    "High": 100,
    "Medium": 70,
    "Low": 40,
}

MOCK_PLATFORMS = {
    "amazon handmade",
    "redbubble",
    "society6",
    "teepublic",
}


# Opportunity Score 2.0 combines independent component scores into one 0-100
# score. The weights keep the model understandable: demand matters most, price
# fit and competition follow, while trend and data confidence adjust the result.
def calculate_score(price, reviews, rating=0, platform="", trend_score=0):
    demand_score = calculate_demand_score(reviews, rating, platform)
    competition_score = calculate_competition_score(reviews, platform)
    price_score = calculate_price_score(price)
    clean_trend_score = _clamp_score(trend_score)
    confidence = calculate_data_confidence(platform)
    confidence_score = CONFIDENCE_SCORES[confidence]

    overall_score = round(
        (demand_score * 0.35)
        + (price_score * 0.25)
        + (competition_score * 0.20)
        + (clean_trend_score * 0.10)
        + (confidence_score * 0.10)
    )

    score_label = calculate_score_label(overall_score)
    competition = calculate_competition_label(reviews)

    # Legacy keys remain so older CLI, CSV, and dashboard code keeps working.
    return {
        "overall_score": overall_score,
        "total_score": overall_score,
        "demand_score": demand_score,
        "review_score": demand_score,
        "competition_score": competition_score,
        "price_score": price_score,
        "trend_score": clean_trend_score,
        "rating_score": calculate_rating_score(rating, platform),
        "confidence": confidence,
        "confidence_score": confidence_score,
        "score_label": score_label,
        "score_badge": calculate_score_badge(score_label),
        "competition": competition,
        "opportunity": score_label,
    }


def calculate_demand_score(reviews, rating=0, platform=""):
    clean_reviews = _safe_number(reviews)
    clean_rating = _safe_number(rating)

    if _is_ebay(platform) and clean_reviews == 0 and clean_rating == 0:
        return 25

    if clean_reviews >= 1000:
        review_signal = 90
    elif clean_reviews >= 500:
        review_signal = 75
    elif clean_reviews >= 100:
        review_signal = 55
    elif clean_reviews > 0:
        review_signal = 30
    else:
        review_signal = 15

    rating_signal = calculate_rating_score(clean_rating, platform)
    return round((review_signal * 0.75) + (rating_signal * 0.25))


def calculate_competition_score(reviews, platform=""):
    clean_reviews = _safe_number(reviews)

    if _is_ebay(platform) and clean_reviews == 0:
        return 65

    if clean_reviews >= 1000:
        return 20
    if clean_reviews >= 700:
        return 35
    if clean_reviews >= 300:
        return 55
    if clean_reviews >= 100:
        return 75
    return 90


def calculate_price_score(price):
    clean_price = _safe_number(price)

    if 18 <= clean_price <= 28:
        return 100
    if 15 <= clean_price <= 35:
        return 75
    if 10 <= clean_price <= 40:
        return 55
    return 30


def calculate_rating_score(rating, platform=""):
    clean_rating = _safe_number(rating)

    if _is_ebay(platform) and clean_rating == 0:
        return 0

    if clean_rating >= 4.8:
        return 100
    if clean_rating >= 4.5:
        return 80
    if clean_rating >= 4.0:
        return 60
    if clean_rating >= 3.5:
        return 35
    return 0


def calculate_data_confidence(platform=""):
    clean_platform = str(platform).strip().lower()

    if clean_platform == "etsy":
        return "High"
    if clean_platform == "ebay":
        return "Medium"
    if clean_platform in MOCK_PLATFORMS:
        return "Low"
    return "Low"


def calculate_competition_label(reviews):
    clean_reviews = _safe_number(reviews)

    if clean_reviews >= 1000:
        return "Very High"
    if clean_reviews >= 700:
        return "High"
    if clean_reviews >= 300:
        return "Medium"
    return "Low"


def calculate_score_label(score):
    clean_score = _safe_number(score)

    if clean_score >= 85:
        return "Excellent"
    if clean_score >= 70:
        return "Good"
    if clean_score >= 55:
        return "Average"
    if clean_score >= 40:
        return "Weak"
    return "Poor"


def calculate_score_badge(label):
    badges = {
        "Excellent": "★★★★★ Excellent",
        "Good": "★★★★ Good",
        "Average": "★★★ Average",
        "Weak": "★★ Weak",
        "Poor": "★ Poor",
    }
    return badges.get(label, "★ Poor")


def _is_ebay(platform):
    return str(platform).strip().lower() == "ebay"


def _clamp_score(value):
    return max(0, min(100, round(_safe_number(value))))


def _safe_number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0