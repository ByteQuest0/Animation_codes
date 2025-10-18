from manimlib import *
import numpy as np


class Standardisation(Scene):
    def construct(self):

        self.camera.frame.scale(0.88)

        # -------------------------------------------------------------
        # DATASET: horizontal rectangle (large x variance, small y variance)
        # -------------------------------------------------------------
        np.random.seed(42)

        # Horizontal rectangle in first and second quadrants
        n_points = 50
        x_points = np.random.uniform(-3.5, 3.5, n_points)           
        y_points = np.random.normal(1.5, 0.4, n_points)  # Small y spread

        data_points = np.column_stack([x_points, y_points])

        # -------------------------------------------------------------
        # Compute mean
        # -------------------------------------------------------------
        mean_x = np.mean(data_points[:, 0])
        mean_y = np.mean(data_points[:, 1])
        mean_point = [mean_x, mean_y]

        # -------------------------------------------------------------
        # AXES without number labels (vague)
        # -------------------------------------------------------------
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-4, 4, 1],
            width=8,
            height=6,
            axis_config={
                "stroke_width": 6,
                "include_tip": True,
                "include_ticks": False,
                "numbers_to_exclude": [0],
            }
        )

        # -------------------------------------------------------------
        # DOTS
        # -------------------------------------------------------------
        dots = VGroup()
        for x, y in data_points:
            dot = Dot(axes.c2p(x, y), radius=0.06).set_color(GREEN_D)
            dots.add(dot)

        # Mean dot (red)
        PURE_BLUE = "#FF0000"
        mean_dot = Dot(axes.c2p(*mean_point), radius=0.16).set_color(PURE_BLUE)
        mean_text = Text("X", font_size=36, weight=BOLD).set_color(WHITE).move_to(axes.c2p(*mean_point))
        mean_group = VGroup(mean_dot, mean_text).set_z_index(3)

        # -------------------------------------------------------------
        # ANIMATION: initial points
        # -------------------------------------------------------------
        self.play(
            ShowCreation(axes.x_axis),
            ShowCreation(axes.y_axis),
            run_time=1.5
        )

        self.play(
            LaggedStart(*[GrowFromCenter(dot) for dot in dots], lag_ratio=0.05),
            run_time=3
        )
        self.wait(1)

        self.play(GrowFromCenter(mean_group), run_time=1.2)
        self.wait(2)

        # -------------------------------------------------------------
        # CENTER DATA
        # -------------------------------------------------------------
        centered_data = data_points - np.array([mean_x, mean_y])
        
        centered_dots = VGroup()
        for (x, y) in centered_data:
            new_position = axes.c2p(x, y)
            new_dot = Dot(new_position, radius=0.06).set_color(GREEN_D)
            centered_dots.add(new_dot)

        centered_mean = VGroup(
            Dot(axes.c2p(0, 0), radius=0.16).set_color(MAROON),
            Text("X", font_size=36, weight=BOLD).set_color(WHITE).move_to(axes.c2p(0, 0))
        )

        self.play(
            Transform(dots, centered_dots),
            Transform(mean_group, centered_mean),
            run_time=2.5
        )
        self.wait(2)

        # -------------------------------------------------------------
        # FORMULAS - CENTERING
        # -------------------------------------------------------------
        self.play(self.camera.frame.animate.shift(RIGHT * 3.2))

        mean_tex = Tex(r"\mu = \frac{1}{n} \sum_{i=1}^n x_i").next_to(axes, RIGHT, buff=1.5).scale(1.23).shift(UP * 0.9)
        center_tex = Tex(r"x_i \ \;\leftarrow\; \ x_i - \mu").next_to(mean_tex, DOWN).scale(1.23).shift(DOWN * 0.5)

        self.play(ShowCreation(mean_tex))
        self.wait()
        self.play(ShowCreation(center_tex))
        self.wait(2)

        self.play(self.camera.frame.animate.shift(LEFT * 3.2), FadeOut(VGroup(mean_tex, center_tex)))
        self.wait(2)


        brace = Brace(dots, UP, buff=0.5).set_color(YELLOW)
        brace1 = Brace(dots, LEFT, buff=0.5).set_color(YELLOW).scale(0.88)

        self.play(GrowFromCenter(brace), GrowFromCenter(brace1))
        self.wait(2)

        self.play(FadeOut(brace), FadeOut(brace1))


        # -------------------------------------------------------------
        # VARIANCE FORMULAS
        # -------------------------------------------------------------
        self.play(self.camera.frame.animate.shift(RIGHT * 3.2))

        var_general = Tex(r"\sigma^2 = \frac{1}{n} \sum_{i=1}^{n} (x_i - \mu)^2").next_to(axes, RIGHT, buff=1.5).shift(UP * 0.9+LEFT*0.86)
        self.play(ShowCreation(var_general))
        self.wait(2)

        var_centered = Tex(r"\sigma^2 = \frac{1}{n} \sum_{i=1}^{n} x_i^2").next_to(axes, RIGHT, buff=1.5).scale(1.23).move_to(var_general)
        self.play(Transform(var_general, var_centered))
        self.wait(2)

        var_update = Tex(r"x_i \ \;\leftarrow\; \ \frac{x_i}{\sigma}").next_to(var_centered, DOWN).scale(1.23).shift(DOWN * 0.5)
        self.play(ShowCreation(var_update))
        self.wait(2)

        self.play(self.camera.frame.animate.shift(LEFT * 3.2), FadeOut(VGroup(var_general, var_update)))
        self.wait(2)

        # -------------------------------------------------------------
        # STRETCH DATA to make it square-shaped (normalize)
        # -------------------------------------------------------------
        # Calculate standard deviations
        std_x = np.std(centered_data[:, 0])
        std_y = np.std(centered_data[:, 1])
        
        # Normalize data - stretch/compress from center to make variances equal
        normalized_data = centered_data / np.array([std_x, std_y])
        
        # Create stretched dots
        stretched_dots = VGroup()
        for (x, y) in normalized_data:
            new_position = axes.c2p(x, y)
            new_dot = Dot(new_position, radius=0.06).set_color(BLUE_D)
            stretched_dots.add(new_dot)

        # Stretch the data from center
        self.play(
            Transform(dots, stretched_dots),
            run_time=2.5
        )
        self.wait(3)

