from votekit import Ballot
from fractions import Fraction
import pytest


def test_ballot_init():
    b = Ballot()
    assert not b.ranking
    assert b.weight == Fraction(1)
    assert not b.voter_set
    assert not b.id
    assert not b.scores


def test_ballot_post_init():
    assert isinstance(Ballot(weight=3).weight, Fraction)
    assert isinstance(Ballot(weight=3.2).weight, Fraction)
    assert Ballot(scores={"A": 1, "B": 0}).scores == {"A": Fraction(1)}
    assert Ballot(scores={"A": 1, "B": -1}).scores == {
        "A": Fraction(1),
        "B": Fraction(-1),
    }
    assert isinstance(Ballot(scores={"A": 2, "B": Fraction(2)}).scores["A"], Fraction)
    assert isinstance(Ballot(scores={"A": 2.0, "B": Fraction(2)}).scores["A"], Fraction)

    with pytest.raises(ValueError, match="Invalid literal for Fraction"):
        Ballot(weight="a")
    with pytest.raises(TypeError, match="Score values must be numeric."):
        Ballot(scores={"A": "a"})


def test_ballot_eq():
    b = Ballot(
        ranking=[{"A"}, {"B"}, {"C"}],
        weight=3,
        voter_set={"Chris"},
        id="91010",
        scores={"A": 1, "B": 1 / 2, "C": 0},
    )

    assert b != Ballot(
        weight=3, voter_set={"Chris"}, id="91010", scores={"A": 1, "B": 1 / 2, "C": 0}
    )

    assert b != Ballot(
        ranking=[{"A"}, {"B"}, {"C"}],
        voter_set={"Chris"},
        id="91010",
        scores={"A": 1, "B": 1 / 2, "C": 0},
    )

    assert b != Ballot(
        ranking=[{"A"}, {"B"}, {"C"}],
        weight=3,
        id="91010",
        scores={"A": 1, "B": 1 / 2, "C": 0},
    )

    assert b != Ballot(
        ranking=[{"A"}, {"B"}, {"C"}],
        weight=3,
        voter_set={"Chris"},
        scores={"A": 1, "B": 1 / 2, "C": 0},
    )
    assert b != Ballot(
        ranking=[{"A"}, {"B"}, {"C"}],
        weight=3,
        voter_set={"Chris"},
        id="91010",
    )


def test_ballot_str():
    b = Ballot(
        ranking=[{"A"}, {"B"}, {"C"}],
        weight=3,
        voter_set={"Chris"},
        id="91010",
        scores={"A": 1, "B": 1 / 2, "C": 0},
    )

    assert (
        str(b)
        == "Ranking\n1.) A, \n2.) B, \n3.) C, \nScores\nA: 1.00\nB: 0.50\nWeight: 3"
    )
