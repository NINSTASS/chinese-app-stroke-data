# chinese-app-stroke-data

Stroke-order data for the Chinese characters used in a small, private
Chinese learning app. Published here because the Arphic Public License
requires modified versions of the data to be freely available.

## Contents

- `hanzi_strokes.json` — stroke outlines and median lines for 517
  characters and components, as bundled with the app.
- `stroke_subset.py` — the script that produces it from `graphics.txt`.
- `ARPHICPL.txt` — the Arphic Public License.

## Source

Cut down from `graphics.txt` of **Make Me a Hanzi**
(<https://github.com/skishore/makemeahanzi>) by Shaunak Kishore, which is
derived from the fonts **Arphic PL KaitiM GB** and **Arphic PL UKai** by
Arphic Technology Co., Ltd.

Changes: only the listed characters are kept, and per character only the
keys `strokes` and `medians`. The stroke data itself is unchanged. The date
of the change is in the `_notice` field of the JSON file.

## Reproduce

```
python3 stroke_subset.py --graphics graphics.txt --chars "<characters>" \
    --out hanzi_strokes.json
```

The character list is the key order of `characters` in `hanzi_strokes.json`.

## License

The data (`hanzi_strokes.json`) is licensed under the Arphic Public
License, see `ARPHICPL.txt`. The script `stroke_subset.py` is licensed
under the MIT License (text in the file header). Both come without any
warranty.
