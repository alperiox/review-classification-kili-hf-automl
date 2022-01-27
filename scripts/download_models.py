import gdown
import shutil
import os

if "models" not in os.listdir():
    os.mkdir("models")

folder_id = "1X_ci2Pwu0-1XbXsaCksQHZF0254TIHiD"
gdown.download_folder(id=folder_id)

downloaded_dir = "User Review Analysis"
for model_dir in os.listdir(downloaded_dir):
    dir_path = os.path.join(downloaded_dir, model_dir)
    shutil.move(dir_path, "models")
os.rmdir("User Review Analysis")