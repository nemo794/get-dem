# NASA-Specific Instructions

## Creating a `conda` Environment

To emulate execution of the Get DEM algorithm in the NASA MAAP system, you must
have `conda` installed.  Once installed, you must create the `dem` environment
as follows:

```plain
nasa/build-dev.sh
```

Next, you must activate the environment:

```plain
conda activate dem
```

## Running the Algorithm Locally

At this point, the general form for running the algorithm _locally_, which is
the same form used by the NASA DPS system, is as follows (this assumes that your
current directory is the root of this repository, _not_ the directory containing
these instructions):

```plain
nasa/run.sh 'LEFT BOTTOM RIGHT TOP' 'COMPUTE'
```

where:

- `LEFT` is the left longitude of your desired bounding box
- `BOTTOM` is the bottom latitude of your desired bounding box
- `RIGHT` is the right longitude of your desired bounding box
- `TOP` is the top latitude of your desired bounding box
- `COMPUTE` is a "flag" indicating whether or not you wish to perform
  CPU-intensive, multi-core computations.  If you do _NOT_ wish to perform such
  computations, you must include _empty quotes_ (either single or double).
  Otherwise, any non-empty value (quoted or not) will be interpreted to mean
  that you _do_ wish to perform such computations.

Take careful note of the single quotes (double quotes work as well) surrounding
the entirety of all 4 bounding box coordinates.  These are required in order for
the 4 coordinates to be treated as a single bounding box input value because
they are space-separated.

Here is an example _with_ computation (the "compute" flag is arbitrarily
specified as `true`, but the value is irrelevant; any non-empty value, even
`false`, will trigger computation):

```plain
nasa/run.sh '-118.06817 34.22169 -118.05801 34.22822' true
```

Here is an example using the same bounding box as above, but with _no
computation_ (notice the empty pair of single quotes at the end to signify that
_no_ computation should take place; an empty pair of double quotes works as
well):

```plain
nasa/run.sh '-118.06817 34.22169 -118.05801 34.22822' ''
```

In addition to output written to your console, you will find that the algorithm
creates a directory named `output` and writes the following files there:

- `dem.tif`: GeoTIFF generated by the `sardem` library
- `elapsed.json`: simple file containing the elapsed runtime (seconds) of the
  main functions of the algorithm
- `profile.json`: detailed profiling metrics captured by
  [Scalene](https://github.com/plasma-umass/scalene)
- `simple_profile.json`: minimal set of profile metrics pulled from
  `elapsed.json` and `profile.json`

## Submitting a Batch of Jobs to DPS

To submit a batch of jobs to a specific queue with identical inputs, you may
run the `nasa/jobs submit` command.  To get help for this command, supply the
`-h/--help` option:

```plain
$ nasa/jobs submit -h
Usage: jobs submit -a NAME -v VERSION -u USERNAME -t TAG -q NAME -n INTEGER -o FILE 'LEFT BOTTOM RIGHT TOP'
COMPUTE [-h]

  Submit a job one or more times to the same job queue with the same inputs.

  Options
    -a, --algorithm NAME     Name of the algorithm to run.
    -v, --version VERSION    Version of the algorithm to run.
    -u, --username USERNAME  Username of the user submitting the job(s).
    -t, --tag TAG            A tag to identify the job.  It is recommended that this be indicative of the
                             region covered by the bounding box.
    -q, --queue NAME         Name of the job queue to submit the job to.
    -n, --repeat INTEGER     Number of times to submit the job.
    -o, --output FILE        Name of the file to write the job IDs to.

  Arguments
    'LEFT BOTTOM RIGHT TOP'  Bounding box to process, specified as 'LEFT BOTTOM RIGHT TOP', including the
                             surrounding quotes (either single or double quotes).
    COMPUTE                  Flag to indicate whether or not to incorporate compute-intensive work.  To
                             *avoid* compute-intensive work, specify an empty pair of quotes (either single
                             or double quotes).  Any other value will trigger compute-intensive work.

  Help
    [-h, --help]             Show this message and exit.
```

For example:

```plain
nasa/jobs submit -a get-dem -v develop -u dschuck -t Glacier -q maap-dps-worker-c5.2xlarge \
  -n 3 -o output/glacier__maap-dps-worker-c5.2xlarge.txt '"-115.396 46.020 -110.523 48.995"' true
```

Note the double set of quotes around the bounding box coordinates, specifically
a pair of _single_ quotes surrounding a pair of _double_ quotes surrounding the
coordinates.  This is necessary when there is at least one negative coordinate.
Otherwise, the argument parser attempts to interpret the negative sign as an
option prefix and gets confused.

The file specified for the `-o/--output` option will be populated with the job
IDs of the submitted jobs.  This file may then be used as input for commands
described in the following sections.

## Awaiting Job Completions

Once a batch of jobs is submitted, you may use the `nasa/jobs await` command to
wait for them all to complete (successfully or not) by using the file containing
job IDs, written by the `nasa/jobs submit` command.  Continuing with the example
from the previous section, we can await the submitted jobs as follows:

```plain
nasa/jobs await @output/glacier__maap-dps-worker-c5.2xlarge.txt
```

This will poll the status of each job until every job has a status that is
either "Succeeded" or "Failed".  Once all jobs have completed, the next step is
to locate all of the output directories containing the profile statistics we're
interested in.

## Locating Job Outputs

Once a batch of jobs is complete, we can gather a list of paths to the output
directories, or to a specific file within the directories, by using the
`nasa/jobs locate` command.  Continuing with our example from above, to locate
all of the `simple_profile.json` files from our jobs, we can run the following:

```plain
nasa/jobs -f simple_profile.json @output/glacier__maap-dps-worker-c5.2xlarge.txt
```

This command will simply print the absolute path to `simple_profile.json` for
each successfully completed job from the specified job list.

## Aggregating Simplified Profiles

Finally, we can aggregate simplified profiles produced by a batch of jobs by
passing a set of paths to `simple_profile.json` files to the
`aggregate_profiles.py` script, as follows (continuing our example):

```plain
nasa/jobs -f simple_profile.json @output/glacier__maap-dps-worker-c5.2xlarge.txt \
  | xargs ./aggregate_profiles.py
```