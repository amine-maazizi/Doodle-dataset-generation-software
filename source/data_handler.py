import pandas as pd
import os


class DataHandler:
    def __init__(self, dataset_dir):
        self.dataset_dir = dataset_dir
        self.data = pd.DataFrame(columns=['img_file', 'label'])


    def clear_dataset(self) -> None:
        if os.path.exists(self.dataset_dir):
            file_list = os.listdir(self.dataset_dir)
            for filename in file_list:
                file_path = os.path.join(self.dataset_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        else:
            os.makedirs(self.dataset_dir)

    def save_img(self, img, path: str) -> None:
        img.save(os.path.join(self.dataset_dir, path))

    def add_to_dataset(self, entry: dict) -> None:
        self.data = pd.concat([self.data, pd.DataFrame(entry)], ignore_index=True)

    def save_to_csv(self):
        self.data.to_csv(os.path.join(self.dataset_dir, 'data.csv'), index=False)