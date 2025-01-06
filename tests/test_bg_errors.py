import pytest
import numpy as np

from votekit.ballot_generator import (
    name_PlackettLuce,
    CambridgeSampler,
    Spatial,
    ClusteredSpatial,
)

from votekit.pref_interval import PreferenceInterval


def test_not_cand_and_not_slate_to_cand():
    blocs = {"R": 0.7, "D": 0.3}
    cohesion = {"R": {"R": 0.7, "D": 0.3}, "D": {"D": 0.6, "R": 0.4}}
    alphas = {"R": {"R": 0.5, "D": 1}, "D": {"R": 1, "D": 0.5}}

    with pytest.raises(ValueError):
        name_PlackettLuce(
            bloc_voter_prop=blocs,
            cohesion_parameters=cohesion,
            alphas=alphas,
        )


def test_all_nec_params():
    # missing bloc voter prop
    # bloc_voter_prop={"W": 0.7, "C": 0.3},
    with pytest.raises(ValueError):
        name_PlackettLuce(
            candidates=["W1", "W2", "C1", "C2"],
            pref_intervals_by_bloc={
                "W": {
                    "W": PreferenceInterval({"W1": 0.4, "W2": 0.3}),
                    "C": PreferenceInterval({"C1": 0.2, "C2": 0.1}),
                },
                "C": {
                    "W": PreferenceInterval({"W1": 0.2, "W2": 0.2}),
                    "C": PreferenceInterval({"C1": 0.3, "C2": 0.3}),
                },
            },
            cohesion_parameters={"W": {"W": 0.7, "C": 0.3}, "C": {"C": 0.9, "W": 0.1}},
        )

    # missing pref_intervals
    with pytest.raises(ValueError):
        name_PlackettLuce(
            candidates=["W1", "W2", "C1", "C2"],
            bloc_voter_prop={"W": 0.7, "C": 0.3},
            cohesion_parameters={"W": {"W": 0.7, "C": 0.3}, "C": {"C": 0.9, "W": 0.1}},
        )


def test_incorrect_bloc_props():
    # should sum to 1
    blocs = {"R": 0.7, "D": 0.4}

    cohesion = {"R": {"R": 0.7, "D": 0.3}, "D": {"D": 0.6, "R": 0.4}}
    alphas = {"R": {"R": 0.5, "D": 1}, "D": {"R": 1, "D": 0.5}}
    slate_to_cands = {"R": ["A1", "B1", "C1"], "D": ["A2", "B2"]}

    with pytest.raises(ValueError):
        name_PlackettLuce.from_params(
            slate_to_candidates=slate_to_cands,
            bloc_voter_prop=blocs,
            cohesion_parameters=cohesion,
            alphas=alphas,
        )


def test_Cambridge_maj_bloc_error():
    # need to provide both W_bloc and C_bloc
    with pytest.raises(ValueError):
        CambridgeSampler(
            candidates=["W1", "W2", "C1", "C2"],
            slate_to_candidates={"A": ["W1", "W2"], "B": ["C1", "C2"]},
            pref_intervals_by_bloc={
                "A": {
                    "A": PreferenceInterval({"W1": 0.4, "W2": 0.3}),
                    "B": PreferenceInterval({"C1": 0.2, "C2": 0.1}),
                },
                "B": {
                    "A": PreferenceInterval({"W1": 0.2, "W2": 0.2}),
                    "B": PreferenceInterval({"C1": 0.3, "C2": 0.3}),
                },
            },
            bloc_voter_prop={"A": 0.7, "B": 0.3},
            cohesion_parameters={"A": {"A": 0.7, "B": 0.3}, "B": {"B": 0.9, "A": 0.1}},
            W_bloc="A",
        )
    # must be distinct
    with pytest.raises(ValueError):
        CambridgeSampler(
            candidates=["W1", "W2", "C1", "C2"],
            slate_to_candidates={"A": ["W1", "W2"], "B": ["C1", "C2"]},
            pref_intervals_by_bloc={
                "A": {
                    "A": PreferenceInterval({"W1": 0.4, "W2": 0.3}),
                    "B": PreferenceInterval({"C1": 0.2, "C2": 0.1}),
                },
                "B": {
                    "A": PreferenceInterval({"W1": 0.2, "W2": 0.2}),
                    "B": PreferenceInterval({"C1": 0.3, "C2": 0.3}),
                },
            },
            bloc_voter_prop={"A": 0.7, "B": 0.3},
            cohesion_parameters={"A": {"A": 0.7, "B": 0.3}, "B": {"B": 0.9, "A": 0.1}},
            W_bloc="A",
            C_bloc="A",
        )


def test_spatial_generator():
    candidates = [str(i) for i in range(25)]
    uniform_params = {"low": 0, "high": 1, "size": 2}
    normal_params = {"loc": 0.5, "scale": 0.1, "size": 2}

    def bad_dist(x, y, z):
        return x + y + z

    with pytest.raises(TypeError, match="Invalid kwargs for the voter distribution."):
        Spatial(
            candidates=candidates,
            voter_dist=np.random.normal,
            voter_dist_kwargs=uniform_params,
            candidate_dist=np.random.normal,
            candidate_dist_kwargs=normal_params,
        )

    with pytest.raises(
        TypeError, match="Invalid kwargs for the candidate distribution."
    ):
        Spatial(
            candidates=candidates,
            voter_dist=np.random.normal,
            voter_dist_kwargs=normal_params,
            candidate_dist=np.random.normal,
            candidate_dist_kwargs=uniform_params,
        )

    with pytest.raises(
        TypeError,
        match="Distance function is invalid or "
        "incompatible with voter/candidate distributions.",
    ):
        Spatial(
            candidates=candidates,
            voter_dist=np.random.normal,
            voter_dist_kwargs=normal_params,
            candidate_dist=np.random.normal,
            candidate_dist_kwargs=normal_params,
            distance=bad_dist,
        )


def test_clustered_spatial_generator():
    candidates = [str(i) for i in range(25)]
    uniform_params = {"low": 0, "high": 1, "size": 2}
    normal_params = {"loc": 0.5, "scale": 0.1, "size": 2}

    def bad_dist(x, y, z):
        return x + y + z

    with pytest.raises(TypeError, match="Invalid kwargs for the voter distribution."):
        ClusteredSpatial(
            candidates=candidates,
            voter_dist=np.random.normal,
            voter_dist_kwargs=uniform_params,
            candidate_dist=np.random.normal,
            candidate_dist_kwargs=normal_params,
        )

    with pytest.raises(
        TypeError, match="Invalid kwargs for the candidate distribution."
    ):
        ClusteredSpatial(
            candidates=candidates,
            voter_dist=np.random.normal,
            voter_dist_kwargs=normal_params,
            candidate_dist=np.random.normal,
            candidate_dist_kwargs=uniform_params,
        )

    with pytest.raises(
        TypeError,
        match="Distance function is invalid or "
        "incompatible with voter/candidate distributions.",
    ):
        ClusteredSpatial(
            candidates=candidates,
            voter_dist=np.random.normal,
            voter_dist_kwargs=normal_params,
            candidate_dist=np.random.normal,
            candidate_dist_kwargs=normal_params,
            distance=bad_dist,
        )

    with pytest.raises(ValueError, match="Input voter distribution not supported."):
        ClusteredSpatial(
            candidates=candidates,
            voter_dist=np.random.uniform,
            voter_dist_kwargs=normal_params,
            candidate_dist=np.random.normal,
            candidate_dist_kwargs=normal_params,
        )
