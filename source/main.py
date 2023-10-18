"""
Doodle Dataset Generation Application

This application allows users to create a dataset of doodles and apply data augmentation to generate variations of doodles.

Usage:
1. Run this script.
2. Use the canvas to draw a doodle.
3. Enter a label (class) for the doodle.
4. Optionally, activate data augmentation by checking the "Activate Data Augmentation" box.
5. Press Enter to save the doodle and its variations to the dataset.

Press ESC or click the close button to exit the application.

Author: MAAZIZI Amine.
"""

from app import Application

if __name__ == '__main__':
    app = Application()
    app.launch()
    