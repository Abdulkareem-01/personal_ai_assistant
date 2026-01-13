import nltk
import os

# Tell NLTK where to store data
nltk.data.path.append("/opt/render/nltk_data")

os.makedirs("/opt/render/nltk_data", exist_ok=True)

nltk.download("punkt", download_dir="/opt/render/nltk_data")
nltk.download("stopwords", download_dir="/opt/render/nltk_data")
