from huggingface_hub import hf_hub_download
from huggingface_hub import snapshot_download
import joblib

REPO_ID = "kprokofi/act_red_ball_1"
REPO_ID = "kprokofi/lecroc_red_ball_3cams_50"
FILENAME = "."

snapshot_download(repo_id=REPO_ID)

# model = joblib.load(
#     hf_hub_download(repo_id=REPO_ID, filename=FILENAME)
# )