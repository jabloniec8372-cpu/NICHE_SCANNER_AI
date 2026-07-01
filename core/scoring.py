def calculate_score(price, reviews):
    score = 0

    if reviews >= 1000:
        score += 60
    elif reviews >= 500:
        score += 45
    elif reviews >= 100:
        score += 30
    else:
        score += 10

    if 15 <= price <= 30:
        score += 30
    else:
        score += 10

    return min(score, 100)
