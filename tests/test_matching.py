import pytest

from app.core.config import MatchWeights
from app.services.matching import (
    MatchCandidate,
    MatchResult,
    _city_match,
    _instrument_compatibility,
    _level_similarity,
    _normalize_weights,
    calculate_match_score,
    jaccard,
    rank_candidates,
)


# Вспомогательные функции
def make_candidate(
    user_id: int,
    *,
    level: int = 1,
    city: str | None = "Moscow",
    piece_ids: set[int] | None = None,
    instrument_ids: set[int] | None = None,
) -> MatchCandidate:
    return MatchCandidate(
        user_id=user_id,
        level=level,
        city=city,
        piece_ids=piece_ids if piece_ids is not None else set(),
        instrument_ids=instrument_ids if instrument_ids is not None else set(),
    )


DEFAULT_WEIGHTS = {
    "repertoire": 0.5 / 1.1,
    "level": 0.3 / 1.1,
    "city": 0.2 / 1.1,
    "instruments": 0.1 / 1.1,
}

# ---------- jaccard ----------


def test_jaccard_partial_overlap():
    assert jaccard({1, 2, 3}, {2, 3, 4}) == pytest.approx(2 / 4)


def test_jaccard_identical():
    assert jaccard({1, 2}, {1, 2}) == 1.0


def test_jaccard_disjoint():
    assert jaccard({1}, {2}) == 0.0


def test_jaccard_one_empty():
    assert jaccard(set(), {1}) == 0.0
    assert jaccard({1}, set()) == 0.0


def test_jaccard_both_empty():
    assert jaccard(set(), set()) == 0.0


# ---------- level ----------


def test_level_similarity_same():
    assert _level_similarity(1, 1) == 1.0
    assert _level_similarity(4, 4) == 1.0


def test_level_similarity_max_diff():
    assert _level_similarity(1, 4) == 0.0
    assert _level_similarity(4, 1) == 0.0


def test_level_similarity_symmetric():
    assert _level_similarity(2, 4) == pytest.approx(1 / 3)
    assert _level_similarity(4, 2) == pytest.approx(1 / 3)
    assert _level_similarity(1, 2) == pytest.approx(2 / 3)


# ---------- city ----------


def test_city_match_same():
    assert _city_match("Moscow", "Moscow") == 1.0


def test_city_match_different():
    assert _city_match("Moscow", "SPb") == 0.0


def test_city_match_none_is_not_equal():
    # Ваша реализация: None != None для целей матчинга
    assert _city_match(None, None) == 0.0
    assert _city_match(None, "Moscow") == 0.0
    assert _city_match("Moscow", None) == 0.0


# ---------- instruments ----------


def test_instrument_compatibility_identical():
    # jaccard == 1 -> compatibility == 0
    assert _instrument_compatibility({1, 2}, {1, 2}) == 0.0


def test_instrument_compatibility_disjoint():
    # jaccard == 0 -> compatibility == 1
    assert _instrument_compatibility({1}, {2}) == 1.0


def test_instrument_compatibility_partial():
    # intersection = {2}, union = {1,2,3}, jaccard = 1/3 -> compatibility = 2/3
    assert _instrument_compatibility({1, 2}, {2, 3}) == pytest.approx(2 / 3)


def test_instrument_compatibility_both_empty():
    # jaccard == 0 -> compatibility == 1.0
    assert _instrument_compatibility(set(), set()) == 0.0


# ---------- weights ----------


def test_normalize_weights_defaults_sum_to_one():
    w = MatchWeights(repertoire=0.5, level=0.3, city=0.2, instruments=0.1)
    n = _normalize_weights(w)

    assert sum(n.values()) == pytest.approx(1.0)
    assert n["repertoire"] == pytest.approx(0.5 / 1.1)
    assert n["level"] == pytest.approx(0.3 / 1.1)
    assert n["city"] == pytest.approx(0.2 / 1.1)
    assert n["instruments"] == pytest.approx(0.1 / 1.1)


def test_normalize_weights_returns_all_keys():
    w = MatchWeights(repertoire=1.0, level=1.0, city=1.0, instruments=1.0)
    n = _normalize_weights(w)

    assert set(n.keys()) == {"repertoire", "level", "city", "instruments"}
    for v in n.values():
        assert v == pytest.approx(0.25)


def test_normalize_weights_zero_raises():
    w = MatchWeights(repertoire=0.0, level=0.0, city=0.0, instruments=0.0)
    with pytest.raises(ValueError):
        _normalize_weights(w)


# ---------- calculate_match_score ----------


def test_score_ideal_but_same_instruments():
    # smoke-кейс из саммари: всё идеально, но инструменты одинаковые -> 0.9091
    a = make_candidate(
        1,
        level=2,
        city="Moscow",
        piece_ids={1, 2, 3},
        instrument_ids={10},
    )
    b = make_candidate(
        2,
        level=2,
        city="Moscow",
        piece_ids={1, 2, 3},
        instrument_ids={10},
    )

    result = calculate_match_score(a, b, weights=DEFAULT_WEIGHTS)

    assert isinstance(result, MatchResult)
    assert result.another_user_id == 2
    assert result.score == pytest.approx(0.9091, abs=1e-4)
    assert result.common_pieces == {1, 2, 3}


def test_score_guitarist_and_pianist_common_piece():
    # smoke-кейс из саммари: 1 общая пьеса из 3, инструменты разные -> 0.697
    a = make_candidate(
        1,
        level=2,
        city="Moscow",
        piece_ids={1, 2},
        instrument_ids={10},
    )
    b = make_candidate(
        2,
        level=2,
        city="Moscow",
        piece_ids={1, 3},
        instrument_ids={20},
    )

    result = calculate_match_score(a, b, weights=DEFAULT_WEIGHTS)

    assert result.score == pytest.approx(0.697, abs=1e-3)
    assert result.common_pieces == {1}


def test_score_breakdown_contains_all_components():
    a = make_candidate(1, piece_ids={1}, instrument_ids={10})
    b = make_candidate(2, piece_ids={1}, instrument_ids={20})

    result = calculate_match_score(a, b, weights=DEFAULT_WEIGHTS)

    assert set(result.breakdown.keys()) == {
        "repertoire",
        "level",
        "city",
        "instruments",
        "total",
    }
    assert result.breakdown["total"] == pytest.approx(result.score)


def test_score_custom_weights_repertoire_only():
    a = make_candidate(1, piece_ids={1, 2}, instrument_ids={10})
    b = make_candidate(2, piece_ids={1, 3}, instrument_ids={20})

    weights = {"repertoire": 1.0, "level": 0.0, "city": 0.0, "instruments": 0.0}
    result = calculate_match_score(a, b, weights=weights)

    assert result.score == pytest.approx(1 / 3)


def test_score_symmetric():
    a = make_candidate(1, level=2, city="Moscow", piece_ids={1, 2}, instrument_ids={10})
    b = make_candidate(2, level=4, city="SPb", piece_ids={2, 3}, instrument_ids={20})

    ab = calculate_match_score(a, b, weights=DEFAULT_WEIGHTS)
    ba = calculate_match_score(b, a, weights=DEFAULT_WEIGHTS)

    assert ab.score == pytest.approx(ba.score)
    assert ab.common_pieces == ba.common_pieces


def test_score_another_user_id_is_target():
    a = make_candidate(1)
    b = make_candidate(99)
    result = calculate_match_score(a, b, weights=DEFAULT_WEIGHTS)
    assert result.another_user_id == 99


# ---------- rank_candidates ----------


def test_rank_candidates_sorted_desc_and_top_k():
    me = make_candidate(
        1,
        level=2,
        city="Moscow",
        piece_ids={1, 2},
        instrument_ids={10},
    )
    best = make_candidate(
        2,
        level=2,
        city="Moscow",
        piece_ids={1, 2},
        instrument_ids={20},
    )
    mid = make_candidate(
        3,
        level=3,
        city="Moscow",
        piece_ids={1, 3},
        instrument_ids={20},
    )
    worst = make_candidate(
        4,
        level=4,
        city="SPb",
        piece_ids={4, 5},
        instrument_ids={10},
    )

    results = rank_candidates(me, [mid, worst, best])

    assert [r.another_user_id for r in results] == [2, 3, 4]
    assert results[0].score >= results[1].score >= results[2].score

    top1 = rank_candidates(me, [mid, worst, best], top_k=1)
    assert len(top1) == 1
    assert top1[0].another_user_id == 2


def test_rank_candidates_excludes_self():
    me = make_candidate(1, piece_ids={1}, instrument_ids={10})
    same_user = make_candidate(1, piece_ids={1}, instrument_ids={10})
    other = make_candidate(2, piece_ids={1}, instrument_ids={20})

    results = rank_candidates(me, [same_user, other])

    assert len(results) == 1
    assert results[0].another_user_id == 2


def test_rank_candidates_empty_pool():
    me = make_candidate(1)
    assert rank_candidates(me, []) == []


def test_rank_candidates_pool_only_self():
    me = make_candidate(1)
    only_self = make_candidate(1)
    assert rank_candidates(me, [only_self]) == []
