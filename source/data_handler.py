import pandas as pd
import os

class DataHandler:
    """Manages data for a dataset, including saving images and metadata to CSV."""
    
    def __init__(self, dataset_dir):
        """Initialize a DataHandler with the dataset directory."""
        self.dataset_dir = dataset_dir
        self.data = pd.DataFrame(columns=['img_file', 'label'])

    def clear_dataset(self) -> None:
        """Clear existing dataset files or create the directory if it doesn't exist."""
        if os.path.exists(self.dataset_dir):
            file_list = os.listdir(self.dataset_dir)
            for filename in file_list:
                file_path = os.path.join(self.dataset_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        else:
            os.makedirs(self.dataset_dir)

    def save_img(self, img, path: str) -> None:
        """Save an image to the dataset directory at the specified path."""
        img.save(os.path.join(self.dataset_dir, path))

    def add_to_dataset(self, entry: dict) -> None:
        """Add an entry to the dataset metadata (e.g., image file and label)."""
        self.data = pd.concat([self.data, pd.DataFrame(entry)], ignore_index=True)

    def save_to_csv(self):
        """Save the dataset metadata to a CSV file within the dataset directory."""
        self.data.to_csv(os.path.join(self.dataset_dir, 'data.csv'), index=False)
