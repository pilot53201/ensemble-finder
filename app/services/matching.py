from dataclasses import dataclass

from app.core.config import MatchWeights, settings


@dataclass(frozen=True)
class MatchCandidate:
    user_id: int
    level: int
    city: str | None
    piece_ids: set[int]
    instrument_ids: set[int]


@dataclass(frozen=True)
class MatchResult:
    another_user_id: int
    score: float
    common_pieces: set[int]
    breakdown: dict[str, float]


def jaccard(set_a: set[int], set_b: set[int]) -> float:
    return len(set_a & set_b) / len(set_a | set_b) if len(set_a | set_b) > 0 else 0.0


def _level_similarity(lvl_a: int, lvl_b: int) -> float:
    return 1 - abs(lvl_a - lvl_b) / 3


def _city_match(city_a: str | None, city_b: str | None) -> float:
    return 1.0 if city_a == city_b and city_a is not None else 0.0


def _instrument_compatibility(inst_a: set[int], inst_b: set[int]) -> float:
    return 1 - jaccard(inst_a, inst_b)


def _normalize_weights(w: MatchWeights) -> dict[str, float]:
    total = w.repertoire + w.city + w.instruments + w.level
    if total == 0:
        raise ValueError("All weights are zero")

    return {
        "repertoire": w.repertoire / total,
        "level": w.level / total,
        "city": w.city / total,
        "instruments": w.instruments / total,
    }


def calculate_match_score(
    candidate: MatchCandidate,
    target: MatchCandidate,
    weights: dict[str, float] | None = None,
) -> MatchResult:
    if weights is None:
        weights = _normalize_weights(settings.match_weights)

    repertoire_val = jaccard(candidate.piece_ids, target.piece_ids)

    city_val = _city_match(candidate.city, target.city)
    level_val = _level_similarity(candidate.level, target.level)
    instruments_val = _instrument_compatibility(candidate.instrument_ids, target.instrument_ids)

    total_score = (
        weights["repertoire"] * repertoire_val
        + weights["city"] * city_val
        + weights["level"] * level_val
        + weights["instruments"] * instruments_val
    )

    result = MatchResult(
        another_user_id=target.user_id,
        score=total_score,
        common_pieces=candidate.piece_ids & target.piece_ids,
        breakdown={
            "repertoire": repertoire_val,
            "level": level_val,
            "city": city_val,
            "instruments": instruments_val,
            "total": total_score,
        },
    )
    return result


def rank_candidates(
    candidate: MatchCandidate,
    pool: list[MatchCandidate],
    top_k: int = 10,
) -> list[MatchResult]:
    """Rank pool by match score, return top_k results sorted desc."""
    results = [
        calculate_match_score(candidate, target)
        for target in pool
        if target.user_id != candidate.user_id
    ]
    results.sort(key=lambda r: r.score, reverse=True)
    return results[:top_k]
