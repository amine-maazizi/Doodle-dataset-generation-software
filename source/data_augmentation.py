from tensorflow.keras.preprocessing.image import ImageDataGenerator

class DataAugmentation:
    def __init__(self, app_config):
        self.app_config = app_config
        self.datagen = ImageDataGenerator(
            rotation_range=app_config.get('RotationRange'),
            width_shift_range=app_config.get('WidthShiftRange'),
            height_shift_range=app_config.get('HeightShiftRange'),
            shear_range=app_config.get('ShearRange'),
            zoom_range=app_config.get('ZoomRange'),
            horizontal_flip=app_config.get('HorizontalFlip'),
            fill_mode=app_config.get('FillMode')
        )

    def apply_data_augmentation(self, original_arr):
        n = self.app_config.get('NumberOfVersion')
        augmented_data = []
        for _ in range(n):
            transformed_arr = self.datagen.random_transform(original_arr)
            augmented_data.append(transformed_arr)
        return augmented_data