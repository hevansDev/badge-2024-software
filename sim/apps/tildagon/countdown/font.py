import gzip
import json

from ..base.asset_path import ASSET_PATH

font = json.loads(
    gzip.decompress(open(ASSET_PATH + "font.json.gz", "rb").read()).decode()
)
