from manimlib import *
import numpy as np

class OptimizationComparison(Scene):
    def construct(self):
        
        # -------------------------------------------------------------
        # CREATE TWO AXES SIDE BY SIDE (first quadrant only)
        # -------------------------------------------------------------
        
        # Left axes - elliptical (unnormalized)
        left_axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            width=5,
            height=5,
            axis_config={
                "stroke_width": 4,
                "include_tip": True,
                "include_ticks": False,
            }
        ).shift(LEFT * 3.5)
        
        # Right axes - circular (normalized)
        right_axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            width=5,
            height=5,
            axis_config={
                "stroke_width": 4,
                "include_tip": True,
                "include_ticks": False,
            }
        ).shift(RIGHT * 3.5)
        
        # Labels for axes - w on y-axis (left), b on x-axis (right)
        left_w = Tex("w").next_to(left_axes.y_axis, LEFT).scale(1.2)
        left_b = Tex("b").next_to(left_axes.x_axis, RIGHT).scale(1.2)
        right_w = Tex("w").next_to(right_axes.y_axis, LEFT).scale(1.2)
        right_b = Tex("b").next_to(right_axes.x_axis, RIGHT).scale(1.2)
        
        # Center point for contours (shifted right in first quadrant)
        center_point = np.array([2.5, 2.5])
        
        # Define shifts for contours and centers
        left_contour_shift = RIGHT * 0.34
        right_contour_shift = RIGHT * 0.34
        left_center_shift = RIGHT * 0.33
        right_center_shift = RIGHT * 0.35
        
        # -------------------------------------------------------------
        # CREATE ELLIPTICAL CONTOURS (rotated towards origin)
        # -------------------------------------------------------------
        left_contours = VGroup()
        # Rotation angle to point one end towards origin
        angle = np.arctan2(center_point[1], center_point[0]) + PI
        
        for radius in [0.3, 0.6, 0.9, 1.2, 1.5]:
            # Stretched ellipse (wide in one direction, narrow perpendicular)
            ellipse = Ellipse(
                width=radius * 3.5,  # Very wide
                height=radius * 1.0,  # Narrow
                stroke_width=2,
                stroke_color=BLUE,
                stroke_opacity=0.6
            ).rotate(angle).move_to(left_axes.c2p(*center_point))
            left_contours.add(ellipse)

        left_contours.shift(left_contour_shift)
        
        # -------------------------------------------------------------
        # CREATE CIRCULAR CONTOURS
        # -------------------------------------------------------------
        right_contours = VGroup()
        for radius in [0.8, 1.1, 1.4, 1.7, 2]:
            circle = Circle(
                radius=radius * 0.8,
                stroke_width=2,
                stroke_color=BLUE,
                stroke_opacity=0.6
            ).move_to(right_axes.c2p(*center_point))
            right_contours.add(circle)
        
        right_contours.shift(right_contour_shift)
        
        # -------------------------------------------------------------
        # CENTER DOTS (RED - #FF0000)
        # -------------------------------------------------------------
        left_center = Dot(left_axes.c2p(*center_point), radius=0.1, color="#FF0000")
        left_center.set_z_index(5).set_color("#FF0000")
        left_center.shift(left_center_shift)
        
        right_center = Dot(right_axes.c2p(*center_point), radius=0.1, color="#FF0000")
        right_center.set_z_index(5).set_color("#FF0000")
        right_center.shift(right_center_shift)
        
        # -------------------------------------------------------------
        # SHOW INITIAL SETUP
        # -------------------------------------------------------------
        self.play(
            ShowCreation(left_axes),
            ShowCreation(right_axes),
            ShowCreation(left_w),
            ShowCreation(left_b),
            ShowCreation(right_w),
            ShowCreation(right_b),
            run_time=1.5
        )
        self.wait(0.5)
        
        self.play(
            LaggedStart(*[ShowCreation(c) for c in left_contours], lag_ratio=0.15),
            LaggedStart(*[ShowCreation(c) for c in right_contours], lag_ratio=0.15),
            run_time=2
        )
        self.wait(0.5)
        
        self.play(
            GrowFromCenter(left_center),
            GrowFromCenter(right_center),
            run_time=1
        )
        self.wait(1)

        
        # -------------------------------------------------------------
        # OPTIMIZATION PATHS - starting from outermost contour
        # -------------------------------------------------------------
        
        # Calculate starting point on outermost contour (rotated ellipse)
        # For left: point on ellipse at angle pointing away from center
        start_angle = angle  # Along major axis away from origin
        ellipse_a = 1.5 * 3.5 / 2  # semi-major axis in coordinate space
        ellipse_b = 1.5 * 1.0 / 2  # semi-minor axis
        
        # Start point on rotated ellipse
        start_offset_x = ellipse_a * np.cos(start_angle)
        start_offset_y = ellipse_a * np.sin(start_angle)
        start_left = center_point + np.array([start_offset_x, start_offset_y])
        
        # For right: point on outermost circle (radius 2.0, the last one in the list)
        circle_radius = 2.0 * 0.8
        start_right = center_point + circle_radius * np.array([np.cos(start_angle), np.sin(start_angle)])
        
        # Left path: zigzag along the rotated ellipse direction
        left_path_points = [
            start_left,
            center_point + 0.85 * (start_left - center_point) + np.array([0.15, -0.15]),
            center_point + 0.70 * (start_left - center_point) + np.array([-0.12, 0.12]),
            center_point + 0.58 * (start_left - center_point) + np.array([0.10, -0.10]),
            center_point + 0.45 * (start_left - center_point) + np.array([-0.08, 0.08]),
            center_point + 0.34 * (start_left - center_point) + np.array([0.06, -0.06]),
            center_point + 0.25 * (start_left - center_point) + np.array([-0.04, 0.04]),
            center_point + 0.18 * (start_left - center_point) + np.array([0.03, -0.03]),
            center_point + 0.12 * (start_left - center_point) + np.array([-0.02, 0.02]),
            center_point + 0.07 * (start_left - center_point),
            center_point + 0.03 * (start_left - center_point),
            center_point
        ]
        
        # Right path: direct to center
        right_path_points = [
            start_right,
            center_point + 0.75 * (start_right - center_point),
            center_point + 0.50 * (start_right - center_point),
            center_point + 0.25 * (start_right - center_point),
            center_point
        ]
        
        # Create starting dots (smaller) - with shifts applied to match contours
        left_start_dot = Dot(left_axes.c2p(*start_left), radius=0.06, color=YELLOW).set_color(YELLOW)
        left_start_dot.shift(left_contour_shift)
        
        self.play(
            GrowFromCenter(left_start_dot),
            run_time=0.8
        )
        self.wait(0.5)
        
        # -------------------------------------------------------------
        # ANIMATE LEFT PATH (ELLIPSE) FIRST
        # -------------------------------------------------------------
        
        # Create path lines
        left_path_lines = VGroup()
        left_dots = VGroup(left_start_dot).set_color(YELLOW)
        
        # Animate left path
        for i in range(len(left_path_points) - 1):
            p1 = left_path_points[i]
            p2 = left_path_points[i + 1]
            
            line = Line(
                left_axes.c2p(*p1),
                left_axes.c2p(*p2),
                stroke_width=2,
                color=YELLOW
            )
            line.shift(left_contour_shift)
            left_path_lines.add(line)
            
            new_dot = Dot(left_axes.c2p(*p2), radius=0.06, color=YELLOW).set_color(YELLOW)
            new_dot.shift(left_contour_shift)
            left_dots.add(new_dot)
            
            self.play(ShowCreation(line), GrowFromCenter(new_dot), run_time=0.4)
            self.wait(0.1)
        
        self.wait(2)
        
        # -------------------------------------------------------------
        # ANIMATE RIGHT PATH (CIRCLE) AFTER WAIT
        # -------------------------------------------------------------
        
        right_start_dot = Dot(right_axes.c2p(*start_right), radius=0.06, color=YELLOW).set_color(YELLOW)
        right_start_dot.shift(right_contour_shift)
        
        self.play(
            GrowFromCenter(right_start_dot),
            run_time=0.8
        )
        self.wait(0.5)
        
        # Create path lines
        right_path_lines = VGroup()
        right_dots = VGroup(right_start_dot).set_color(YELLOW)
        
        # Animate right path
        for i in range(len(right_path_points) - 1):
            r1 = right_path_points[i]
            r2 = right_path_points[i + 1]
            
            right_line = Line(
                right_axes.c2p(*r1),
                right_axes.c2p(*r2),
                stroke_width=2,
                color=YELLOW
            )
            right_line.shift(right_contour_shift)
            right_path_lines.add(right_line)
            
            right_new_dot = Dot(right_axes.c2p(*r2), radius=0.06, color=YELLOW).set_color(YELLOW)
            right_new_dot.shift(right_contour_shift)
            right_dots.add(right_new_dot)
            
            self.play(ShowCreation(right_line), GrowFromCenter(right_new_dot), run_time=0.4)
            self.wait(0.1)
        
        self.wait(3)


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

class Normalizatoin(Scene):
    def construct(self):

        self.camera.frame.scale(0.88)

        # -------------------------------------------------------------
        # DATASET: more scattered diagonal cloud with large y-values
        # -------------------------------------------------------------
        np.random.seed(42)

        # Main cluster centered around y=0, diagonal rectangle — more scattered
        n_main = 42
        x_main = np.random.uniform(0.5, 4.5, n_main)           # wider x spread
        y_main = 150 * x_main + np.random.normal(0, 120, n_main)  # large y values, more scatter, centered

        # Extra points to densify diagonal ends
        n_extra = 14
        x_extra = np.random.uniform(0.2, 5.0, n_extra)
        y_extra = 150 * x_extra + np.random.normal(0, 140, n_extra)

        # Few outliers in other quadrants
        outliers = np.array([
            [-1.5, 200],
            [1.2, -300],
            [-2.0, -250],
            [4.5, -200]
        ])

        # Combine all points
        data_points = np.vstack([
            np.column_stack([x_main, y_main]),
            np.column_stack([x_extra, y_extra]),
            outliers
        ])

        # -------------------------------------------------------------
        # Compute mean & avoid overlapping points
        # -------------------------------------------------------------
        mean_x = np.mean(data_points[:, 0])
        mean_y = np.mean(data_points[:, 1])

        adjusted_points = []
        for x, y in data_points:
            if abs(x - mean_x) < 0.15 and abs(y - mean_y) < 50:
                x += 0.25
                y += 30
            adjusted_points.append([x, y])
        data_points = np.array(adjusted_points)
        mean_point = [mean_x, mean_y]

        # -------------------------------------------------------------
        # AXES with different scales
        # -------------------------------------------------------------
        axes = Axes(
            x_range=[-4, 6, 1],
            y_range=[-800, 1000, 200],
            width=8,
            height=6,
            axis_config={
                "stroke_width": 6,
                "include_tip": True,
                "include_ticks": True,
                "tick_size": 0.08,
                "numbers_to_exclude": [0],
            }
        )
        
        # Add axis labels
        axes.add_coordinate_labels(
            num_decimal_places=0,
            excluding=[0]
        )

        # -------------------------------------------------------------
        # DOTS
        # -------------------------------------------------------------
        dots = VGroup()
        for x, y in data_points:
            dot = Dot(axes.c2p(x, y), radius=0.06)
            dot.set_color(GREEN_D)
            dots.add(dot)


        # -------------------------------------------------------------
        # ANIMATION
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

        # -------------------------------------------------------------
        # MIN-MAX NORMALIZATION
        # -------------------------------------------------------------
        
        # Calculate min and max for normalization
        min_x = np.min(data_points[:, 0])
        max_x = np.max(data_points[:, 0])
        min_y = np.min(data_points[:, 1])
        max_y = np.max(data_points[:, 1])
        
        # Normalize data points
        normalized_points = np.zeros_like(data_points)
        normalized_points[:, 0] = (data_points[:, 0] - min_x) / (max_x - min_x)
        normalized_points[:, 1] = (data_points[:, 1] - min_y) / (max_y - min_y)
        
        # Normalize mean point
        normalized_mean = [
            (mean_point[0] - min_x) / (max_x - min_x),
            (mean_point[1] - min_y) / (max_y - min_y)
        ]
        
        # Create new normalized axes with better clarity
        normalized_axes = Axes(
            x_range=[-0.1, 1.3, 1.1],
            y_range=[-0.1, 1.3, 1.1],
            width=8,
            height=6,
            axis_config={
                "stroke_width": 6,
                "include_tip": True,
                "include_ticks": True,
                "tick_size": 0.08,
            }
        ).set_z_index(-1)
        
        normalized_axes.add_coordinate_labels(
            num_decimal_places=1,
            excluding=[-0.1]
        )
        

        
        # Animate transformation simultaneously
        # Transform axes and dots together
        dot_animations = []
        for i, dot in enumerate(dots):
            new_pos = normalized_axes.c2p(*normalized_points[i])
            dot_animations.append(dot.animate.move_to(new_pos))
        
        # Transform mean dot
        new_mean_pos = normalized_axes.c2p(*normalized_mean)
        
        self.play(
            Transform(axes, normalized_axes),
            *dot_animations,
            self.camera.frame.animate.scale(1.05),
            run_time=2.5
        )
        
        self.wait(2)

        eq_scalar = Tex(r"x_i \ \rightarrow\ \ \frac{x_i - x_{\min}}{x_{\max} - x_{\min}}").next_to(axes, RIGHT).shift(RIGHT*0.8)
        
        eq_scalar_general = Tex(r"x \ \;\rightarrow\; \ a + \frac{(x - x_{\min})(b - a)}{x_{\max} - x_{\min}}")

        self.play(self.camera.frame.animate.shift(RIGHT*4), FadeIn(eq_scalar))
        self.wait(2)


        self.play(Transform(eq_scalar, eq_scalar_general.move_to(eq_scalar).shift(LEFT*0.55)))
        self.wait(2)
        self.play(self.camera.frame.animate.shift(LEFT*4), FadeOut(eq_scalar))
        self.wait(2)
