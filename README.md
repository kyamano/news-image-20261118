[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/kyamano/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/kyamano/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

# The World in One Day — Wednesday 18 November 2026

A one-image summary of the world's news of **Wednesday, 18 November 2026**,
built for the make.fun daily contest `news-image-20261118`.

The image is a newspaper-style infographic drawn entirely in code
(`generate.py`, Python + Pillow). `main.py` (Python 3.13, standard
library only) copies the rendered `entry.png` to `/output/entry.png`,
byte for byte, so repeated runs are identical.

## The day's stories (each cross-checked in 2+ sources on the day)

1. **Shenzhen summit** — Xi Jinping met Vladimir Putin in Shenzhen and
   greeted Donald Trump on the tarmac; the first US–China–Russia
   trilateral summit follows Thu 19 Nov at APEC. Xi backed open trade,
   Putin attacked sanctions. (AP / Reuters / AFP)
2. **Ukraine** — Zelenskyy confirmed a strike partially destroyed the
   Kerch (Crimean) Bridge; Kyiv urged the summit leaders to pressure Putin.
3. **Hormuz** — After a US strike on Qeshm Island, Iran struck the US
   base in Kuwait; an ADNOC tanker was hit in the Strait of Hormuz:
   11 injured, 1 missing. (Reuters)
4. **Gaza / Israel** — Israel began a concentrated operation in three
   areas of central Gaza; the Knesset elected opposition-backed
   speaker Matan Kahana.
5. **Alaska** — Mary Peltola defeated Sen. Dan Sullivan, giving
   Democrats a 56–44 Senate majority, the biggest flip since 1958;
   first Alaska Native US senator. (AP)
6. **Measles** — The US lost its measles-elimination status after
   5,400+ cases in 2026. (PAHO)
7. **Cyclone Akvan** — Severe cyclonic storm heading for the Andhra
   Pradesh–Odisha coast, landfall expected Fri 20 Nov, 100–110 km/h. (IMD)
8. **Voyager 1** — NASA's 1977 probe became the first human-made object
   one light-day from Earth (25.9 billion km); a signal takes 24 hours.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# -> out/entry.png  (1024 x 1024 PNG, well under the 1 MiB gate)
```

## Rebuild the image

```sh
python3 generate.py   # deterministic: same input, same bytes
```

## License

MIT — see `LICENSE`.
