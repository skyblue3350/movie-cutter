import argparse
import logging
from datetime import datetime, timedelta
from pathlib import Path

import ffmpeg


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-level", help="log level", choices=["debug", "info", "error"], default="info")
    parser.add_argument("--log-handler", help="log handler type", choices=["file", "stream"], default="stream")
    parser.add_argument("--log-filename", help="named used in file handler", type=Path, default=None)
    parser.add_argument("--log-dir", help="log dir used in file handler", type=Path, default=Path("log"))
    parser.add_argument("--chapter-file", help="chapter file", type=Path, required=True)
    parser.add_argument("--movie", help="movie file", type=Path, required=True)
    parser.add_argument("--yes", "-y", help="ffmpeg overwrite", action="store_true")

    args = parser.parse_args()

    logger = logging.getLogger(__name__)

    if args.log_handler == "file":
        if args.log_filename is None:
            now = datetime.now()
            filename = now.strftime("%Y-%m-%d") + ".log"
        else:
            filename = args.log_filename

        args.log_dir.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(filename=args.log_dir/filename)
    else:
        handler = logging.StreamHandler()

    handler.setFormatter(logging.Formatter("%(asctime)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s"))
    handler.setLevel(args.log_level.upper())
    logger.setLevel(args.log_level.upper())
    logger.addHandler(handler)

    logger.info(args)

    path = Path().exists()

    if not args.chapter_file.exists():
        raise RuntimeError("Chapter file not found")
    if not args.movie.exists():
        raise RuntimeError("Movie file not found")


    f = open(args.movie.with_suffix(".txt"), "w")
    index = timedelta(seconds=0)
    for line in args.chapter_file.open("r"):
        s = line.split()
        if 3 > len(s):
            continue

        start = list(map(int, s[0].split(":")))
        end = list(map(int, s[1].split(":")))

        start_delta = timedelta(hours=start[0], minutes=start[1], seconds=start[2])
        end_delta = timedelta(hours=end[0], minutes=end[1], seconds=end[2])

        stream = ffmpeg.input(args.movie, ss=start_delta.seconds, t=(end_delta-start_delta).seconds)
        stream = ffmpeg.output(stream, f"{args.movie.parent/s[2]}.mp4")

        if args.yes:
            stream = stream.overwrite_output()

        hours, rem = divmod(index.seconds, 3600)
        minutes, seconds = divmod(rem, 60)
        ts = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
        f.write(f"{ts} {s[2]}\n")
        index += end_delta-start_delta

        ffmpeg.run(stream)
