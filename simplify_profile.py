import argparse
import json
from pathlib import Path
from typing import Any


def simplify_profile(scalene_profile: Any, function_timings: Any) -> Any:
    return {
        "max_footprint_mb": scalene_profile["max_footprint_mb"],
        "total_elapsed_sec": scalene_profile["elapsed_time_sec"],
        "download_and_stitch_sec": function_timings.get("get_dem", 0)
        + function_timings.get("read_dem_as_array", 0),
        "compute_sec": function_timings.get("do_computations", 0),
    }


def parse_args() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o",
        "--out_dir",
        dest="out_dir",
        metavar="PATH",
        type=str,
        help="output directory to read and write profile files",
        required=True,
    )

    args = parser.parse_args()

    return args.out_dir


def main() -> None:
    outdir = Path(parse_args())
    scalene_profile = json.loads((outdir / "profile.json").read_text())
    function_timings = json.loads((outdir / "elapsed.json").read_text())
    simple_profile = simplify_profile(scalene_profile, function_timings)
    (outdir / "simple_profile.json").write_text(json.dumps(simple_profile, indent=2))


if __name__ == "__main__":
    main()
