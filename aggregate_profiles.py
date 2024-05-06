#!/usr/bin/env python

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from functools import reduce
from pathlib import Path


@dataclass(frozen=True, kw_only=True)
class SimpleProfile:
    max_footprint_mb: float
    total_elapsed_sec: float
    download_and_stitch_sec: float
    compute_sec: float

    def __add__(self, other: SimpleProfile) -> SimpleProfile:
        return SimpleProfile(
            max_footprint_mb=self.max_footprint_mb + other.max_footprint_mb,
            total_elapsed_sec=self.total_elapsed_sec + other.total_elapsed_sec,
            download_and_stitch_sec=self.download_and_stitch_sec
            + other.download_and_stitch_sec,
            compute_sec=self.compute_sec + other.compute_sec,
        )


def load_profile(profile_path: Path) -> SimpleProfile:
    """
    Load a profile from a file.
    """
    profile_json = json.loads(profile_path.read_text())

    return SimpleProfile(
        max_footprint_mb=profile_json["max_footprint_mb"],
        total_elapsed_sec=profile_json["total_elapsed_sec"],
        download_and_stitch_sec=profile_json["download_and_stitch_sec"],
        compute_sec=profile_json["compute_sec"],
    )


def mean(profiles: Sequence[SimpleProfile]) -> SimpleProfile:
    """
    Compute the mean of a sequence of profiles.
    """
    totals = reduce(lambda p1, p2: p1 + p2, profiles)
    n_profiles = len(profiles)

    return SimpleProfile(
        max_footprint_mb=totals.max_footprint_mb / n_profiles,
        total_elapsed_sec=totals.total_elapsed_sec / n_profiles,
        download_and_stitch_sec=totals.download_and_stitch_sec / n_profiles,
        compute_sec=totals.compute_sec / n_profiles,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.description = "Aggregate simplified profiles into a single, mean profile."
    parser.add_argument(
        "profile",
        type=Path,
        help="path to a simple profile JSON file",
        nargs="+",
        metavar="SIMPLE_PROFILE",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    profiles = [load_profile(p) for p in args.profile]
    mean_profile = mean(profiles)

    print(json.dumps(asdict(mean_profile), indent=2))


if __name__ == "__main__":
    main()
