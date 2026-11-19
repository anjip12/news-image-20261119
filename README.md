# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/anjip12/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/anjip12/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image that sums up the world's news of Thursday 19 November 2026: a 1024 by 1024 newspaper front page drawn by a program. The lead story is Grand Theft Auto VI rolling out worldwide, with the first-ever Trump-Xi-Putin trilateral in Shenzhen, the widening US-Iran exchanges in the Gulf, Cyclone Akvan bearing down on India's east coast, and NASA's Voyager 1 light-day briefing below it.

## The day in one image

- **Vice City opens its gates** — Grand Theft Auto VI unlocks at midnight local time, New Zealand first, 13 years after GTA V; early reviews put it at Metacritic 99.
- **Three leaders, one table** — Trump, Xi and Putin meet in Shenzhen, the first trilateral of the three presidents, on the sidelines of the APEC summit.
- **Gulf exchanges widen** — US jets hit a missile site on Qeshm Island; Iran's drones reach Kuwait and Bahrain, where defences report interceptions.
- **Cyclone Akvan bears down** — strengthening over the Bay of Bengal, due to cross the Andhra Pradesh coast on 20 November.
- **Voyager, a day of light away** — NASA briefs on Voyager 1, now about 16 billion miles out, a radio signal taking a full day to reach it.

The ticker adds two more items from the day: the House Democrats nominating Hakeem Jeffries for Speaker, and the EU's proposed 45 billion euro Ukraine loan.

## Files

- `gen.py` — draws `entry.png` with Pillow (run locally; it is not part of the graded run).
- `main.py` — the entrypoint: standard library only, it copies the shipped `entry.png` to the output path, so two runs write identical bytes.
- `entry.png` — the finished front page, 1024 by 1024.

## Run it

```sh
python3 gen.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=f7zs4k9v&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
