import glob
import os
import pygame
import numpy as np
import moviepy.editor as mp

# Constants for paths
ASSETS_PATH = "assets/"
TEMP_PATH = "temp/"
OUTPUT_PATH = "output/"

# Ensure temp and output directories exist
os.makedirs(TEMP_PATH, exist_ok=True)
os.makedirs(OUTPUT_PATH, exist_ok=True)

class CompanyGrowthVisualizer:
    def __init__(self, opponents, theme, main_key, speed, years, outputname):
        self.opponents = opponents
        self.theme = theme
        self.main_key = main_key
        self.speed = speed
        self.years = years
        self.outputname = outputname

        pygame.init()
        self.width, self.height = 1080, 1920
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Company Growth Over Time")
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 40)
        self.title_font = pygame.font.Font(None, 80)
        self.year_font = pygame.font.Font(None, 100)
        self.header_font = pygame.font.Font(os.path.join(ASSETS_PATH, "DIMIS___.TTF"), 85)
        self.clock = pygame.time.Clock()

        self.graph_rect = pygame.Rect(100, 400, 880, 1400)
        self.frames = []

        self.load_images()
        self.interpolate_data()

        # Calculate max_frames after interpolating data
        self.max_frames = int(len(self.opponents[self.main_key]['years']) / self.speed)

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)

    def load_images(self):
        for opponent in self.opponents.values():
            opponent['image'] = pygame.image.load(os.path.join(ASSETS_PATH, opponent['image'])).convert_alpha()
            opponent['image'] = pygame.transform.scale(opponent['image'], (60, 60))

    def interpolate_data(self):
        for opponent in self.opponents.values():
            opponent['years'] = np.linspace(self.years[0], self.years[-1], num=len(self.years) * 30)
            original_values = np.interp(opponent['years'], self.years[:-1], opponent['data'])
            noise = np.random.normal(0, 0.01 * original_values, len(original_values))
            opponent['values'] = original_values + noise

    def draw_gradient_background(self):
        for y in range(self.height):
            color = [
                self.theme['gradient1'][i] + (self.theme['gradient2'][i] - self.theme['gradient1'][i]) * y // self.height
                for i in range(3)
            ]
            pygame.draw.line(self.screen, color, (0, y), (self.width, y))

    def draw_team_list(self):
        x_offset = 50
        y_offset = 100
        for name, opponent in self.opponents.items():
            self.screen.blit(opponent['image'], (x_offset, y_offset))
            name_surface = self.font.render(name, True, opponent['color'])
            self.screen.blit(name_surface, (x_offset + 70, y_offset + 15))
            y_offset += 80

    def smooth_position(self, points, window_size=5):
        if len(points) < window_size:
            return points[-1]
        avg_x = np.mean([p[0] for p in points[-window_size:]])
        avg_y = np.mean([p[1] for p in points[-window_size:]])
        return int(avg_x), int(avg_y)

    def draw_frame(self, frame_index):
        year_index = int(frame_index * self.speed)
        self.draw_gradient_background()

        title_surface = self.header_font.render("MarketClash", True, self.BLACK)
        self.screen.blit(title_surface, (self.width // 2 - title_surface.get_width() // 2, 20))

        self.draw_team_list()

        for i in range(0, self.graph_rect.width + 1, 100):
            pygame.draw.line(self.screen, self.GRAY, (self.graph_rect.left + i, self.graph_rect.top),
                             (self.graph_rect.left + i, self.graph_rect.bottom), 1)
        for i in range(0, self.graph_rect.height + 1, 100):
            pygame.draw.line(self.screen, self.GRAY, (self.graph_rect.left, self.graph_rect.bottom - i),
                             (self.graph_rect.right, self.graph_rect.bottom - i), 1)

        pygame.draw.rect(self.screen, self.theme['grid'], self.graph_rect, 2)
        max_value = max(max(opponent['values']) for opponent in self.opponents.values()) * 1.1

        for name, opponent in self.opponents.items():
            color = opponent['color']
            points = []
            for i in range(year_index + 1):
                year = opponent['years'][i]
                value = opponent['values'][i]
                x = self.graph_rect.left + (year - self.years[0]) * self.graph_rect.width / (self.years[-1] - self.years[0])
                y = self.graph_rect.bottom - value * self.graph_rect.height / max_value
                points.append((int(x), int(y)))

            if len(points) > 1:
                pygame.draw.lines(self.screen, color, False, points, 3)

            if points:
                last_point = self.smooth_position(points)
                self.screen.blit(opponent['image'], (last_point[0] - 30, last_point[1] - 60))
                value_text = self.font.render(f"{int(opponent['values'][year_index])}", True, opponent['color'])
                self.screen.blit(value_text, (last_point[0] - 30, last_point[1] - 80))

        for i in range(0, self.graph_rect.width + 1, 100):
            year_label = self.years[0] + i * (self.years[-1] - self.years[0]) / self.graph_rect.width
            label_surface = self.small_font.render(f"{int(year_label)}", True, self.theme['grid_labels'])
            self.screen.blit(label_surface, (self.graph_rect.left + i - 20, self.graph_rect.bottom + 10))

        for i in range(0, self.graph_rect.height + 1, 200):
            value_label = (max_value / 1.1) * (i / self.graph_rect.height)
            label_surface = self.small_font.render(f"{int(value_label)}", True, self.theme['grid_labels'])
            self.screen.blit(label_surface, (self.graph_rect.left - 80, self.graph_rect.bottom - i - 10))

        unit_surface = self.small_font.render("Market Cap (in Billions)", True, self.theme['grid_labels'])
        self.screen.blit(unit_surface, (self.graph_rect.left - 80, self.graph_rect.top - 50))

        year_text = self.year_font.render(f"{int(self.opponents[self.main_key]['years'][year_index])}", True, self.theme['year'])
        self.screen.blit(year_text, (815, 295))

        frame_filename = os.path.join(TEMP_PATH, f"frame_{frame_index:03d}.png")
        pygame.image.save(self.screen, frame_filename)
        self.frames.append(frame_filename)

    def generate_frames(self):
        for frame_index in range(self.max_frames):
            self.draw_frame(frame_index)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
        self.add_final_frames()

    def add_final_frames(self):
        last_frame = self.frames[-1]
        for _ in range(5 * 60):
            self.frames.append(last_frame)

    def create_video(self, output_path):
        clip = mp.ImageSequenceClip(self.frames, fps=60)
        clip.write_videofile(output_path, codec='libx264')

    def cleanup_frames(self, frame_pattern=os.path.join(TEMP_PATH, "frame_*.png")):
        for filename in glob.glob(frame_pattern):
            os.remove(filename)

    def run(self):
        self.generate_frames()
        self.create_video(os.path.join(OUTPUT_PATH, self.outputname))
        pygame.quit()
        self.cleanup_frames()


# Example usage
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

theme = {
    'gradient1': (230, 230, 230),
    'gradient2': (240, 240, 240),
    'grid': (94, 94, 94),
    'grid_labels': (94, 94, 94),
    'year': (94, 94, 94),
}

main_key = "Apple"
speed = 0.5
years = list(range(2000, 2025))
outputname = "company_growth_pygame.mp4"

visualizer = CompanyGrowthVisualizer(opponents, theme, main_key, speed, years, outputname)
visualizer.run()
