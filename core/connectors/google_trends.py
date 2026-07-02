def _get_trend_req_class():
    try:
        from pytrends.request import TrendReq
        return TrendReq
    except Exception:
        return None


def is_google_trends_available():
    return _get_trend_req_class() is not None


def get_google_trend_score(keyword):
    summary = get_google_trend_summary(keyword)
    return summary["trend_score"]


def get_google_trend_summary(keyword):
    clean_keyword = str(keyword).strip()

    if not clean_keyword:
        return _fallback_summary(
            clean_keyword,
            "Enter a keyword to check Google Trends."
        )

    TrendReq = _get_trend_req_class()

    if TrendReq is None:
        return _fallback_summary(
            clean_keyword,
            "Google Trends is optional. Install pytrends to enable live trend signals."
        )

    try:
        pytrends = TrendReq(hl="en-US", tz=360)
        pytrends.build_payload([clean_keyword], timeframe="today 12-m")
        interest = pytrends.interest_over_time()
    except Exception as error:
        return _fallback_summary(
            clean_keyword,
            f"Google Trends request failed safely: {error}"
        )

    try:
        if interest.empty or clean_keyword not in interest.columns:
            return _fallback_summary(
                clean_keyword,
                "Google Trends did not return enough data for this keyword."
            )

        values = interest[clean_keyword].dropna()

        if values.empty:
            return _fallback_summary(
                clean_keyword,
                "Google Trends returned empty trend data for this keyword."
            )

        trend_score = int(round(float(values.tail(12).mean())))
        trend_score = max(0, min(100, trend_score))
        trend_direction = _get_trend_direction(values)
    except Exception as error:
        return _fallback_summary(
            clean_keyword,
            f"Google Trends data could not be processed safely: {error}"
        )

    return {
        "keyword": clean_keyword,
        "source": "Google Trends",
        "available": True,
        "trend_score": trend_score,
        "trend_direction": trend_direction,
        "message": "Live Google Trends signal loaded."
    }


def _fallback_summary(keyword, message):
    return {
        "keyword": keyword,
        "source": "Google Trends",
        "available": False,
        "trend_score": 0,
        "trend_direction": "Unavailable",
        "message": message
    }


def _get_trend_direction(values):
    if len(values) < 2:
        return "Stable"

    first_half = values.iloc[:max(1, len(values) // 2)]
    second_half = values.iloc[max(1, len(values) // 2):]

    first_average = float(first_half.mean())
    second_average = float(second_half.mean())
    difference = second_average - first_average

    if difference >= 5:
        return "Rising"

    if difference <= -5:
        return "Falling"

    return "Stable"