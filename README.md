# Company Growth Visualizer

## Overview

The Company Growth Visualizer is a Python-based tool that visualizes the growth of companies over time using Pygame and MoviePy. It generates an animated graph showing the market capitalization of different companies across years, creating a video to illustrate this data dynamically.
It is perfect for YouTube, Instagram and TikTok short videos!

### Example
https://github.com/maxverwiebe/marketcap_short_video_generator/assets/66183307/18cdfbf5-9bda-4c9c-9434-8860beca1748

## Project Structure

```
project_root/
│
├── assets/
│ ├── apple.png
│ ├── nvidia.png
│ └── DIMIS\_\_\_.TTF
│
├── temp/
│ └── (generated frame images)
│
├── output/
│ └── company_growth_pygame.mp4
│
├── src/
│ └── main.py
│
└── README.md
```

### Directories

- `assets/`: Contains static assets like images and fonts.
- `temp/`: Temporary directory for frame images during video generation.
- `output/`: Directory where the final video output is saved.
- `src/`: Source directory for the main Python script.
- `README.md`: This file, providing an overview and instructions.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/maxverwiebe/marketcap_short_video_generator.git
   cd marketcap_short_video_generator
   ```

2. **Set up a virtual environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Navigate to the source directory**:

   ```bash
   cd src
   ```

2. **Run the main script**:

   ```bash
   python main.py
   ```

   This will generate the animation frames in the `temp/` directory and create a video file in the `output/` directory.

## Customization

### Modify the Company Data

To visualize different companies or update the data, modify the `opponents` dictionary in `main.py`:

```python
opponents = {
    'Apple': {
        'data': [7.71, 5.16, 7.88, 26.05, 60.79, 72.98, 174.03, 75.99, 190.98, 297.09, 377.51, 499.69, 500.74, 643.12, 583.61, 608.96, 860.88, 746.07, 1287, 2255, 2901, 2066, 2994, 3003],
        'image': 'apple.png',
        'color': (135, 135, 135)
    },
    'NVIDIA': {
        'data': [6.44, 1.2, 2.5, 3.91, 6.25, 13.15, 18.90, 4.33, 10.36, 8.94, 8.46, 7.66, 9.10, 10.89, 17.73, 57.53, 117.26, 81.43, 144.00, 323.24, 735.27, 364.18, 1223, 3001],
        'image': 'nvidia.png',
        'color': (63, 209, 65)
    },
}
```

data: List of market cap values for each year.
image: The image filename located in the assets/ directory.
color: RGB tuple representing the color for the company in the graph.

### Change the theme

Modify the theme dictionary in main.py to change the appearance:

```python

theme = {
    'gradient1': (230, 230, 230),
    'gradient2': (240, 240, 240),
    'grid': (94, 94, 94),
    'grid_labels': (94, 94, 94),
    'year': (94, 94, 94),
}
```

### Adjust the Years and Speed

Adjust the years list and speed variable to control the range of years and animation speed:

```python
years = list(range(2000, 2025))
speed = 0.5
```

### Depenencies

The project requires the following Python libraries:

- pygame
- numpy
- moviepy
  Install these using the requirements.txt file provided:
  `pip install -r requirements.txt`
