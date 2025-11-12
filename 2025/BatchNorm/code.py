from manimlib import *
import numpy as np

class GaussianNormalization(Scene):
    def construct(self):

        self.camera.frame.scale(0.89).shift(DOWN)
        # -------------------------------------------------------------
        # CREATE AXES FOR UNNORMALIZED DATA
        # -------------------------------------------------------------
        
        unnorm_axes = Axes(
            x_range=[-2, 10, 1],
            y_range=[0, 0.5, 0.1],
            width=10,
            height=5,
            axis_config={
                "stroke_width": 3,
                "include_tip": True,
                "include_ticks": True,
            }
        ).shift(DOWN * 0.5)
        

        
        # -------------------------------------------------------------
        # GENERATE GAUSSIAN DATA - UNNORMALIZED
        # -------------------------------------------------------------
        
        # Unnormalized parameters
        original_mean = 5.0
        original_std = 1.5
        
        # More sample points for thinner rectangles
        x_values = np.arange(0, 10, 0.15)
        
        # Gaussian probability density function
        def gaussian(x, mu, sigma):
            return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
        
        # Calculate heights for unnormalized data
        y_values_unnorm = gaussian(x_values, original_mean, original_std)
        
        # Create thin rectangles for unnormalized distribution
        rect_width = 0.12
        unnorm_rects = VGroup()
        
        for x, y in zip(x_values, y_values_unnorm):
            rect = Rectangle(
                width=rect_width,
                height=unnorm_axes.y_axis.get_unit_size() * y,
                stroke_width=1,
                stroke_color=BLUE,
                fill_color=BLUE,
                fill_opacity=0.9
            )
            rect.move_to(unnorm_axes.c2p(x, y/2))
            unnorm_rects.add(rect)
        
        # Statistics text for unnormalized
        unnorm_stats = VGroup(
            Tex(r"\mu = " + f"{original_mean:.1f}", font_size=56, color=YELLOW),
            Tex(r"\sigma = " + f"{original_std:.1f}", font_size=56, color=YELLOW)
        ).arrange(RIGHT, buff=0.5).next_to(unnorm_axes, DOWN, buff=0.5)
        
        # -------------------------------------------------------------
        # CREATE AXES FOR NORMALIZED DATA
        # -------------------------------------------------------------
        
        norm_axes = Axes(
            x_range=[-7, 7, 1],
            y_range=[0, 0.5, 0.1],
            width=10,
            height=5,
            axis_config={
                "stroke_width": 3,
                "include_tip": True,
                "include_ticks": True,
            }
        ).shift(DOWN * 0.5)
        
        # -------------------------------------------------------------
        # GENERATE NORMALIZED DATA
        # -------------------------------------------------------------
        
        # Standardize: z = (x - mean) / std
        x_values_norm = (x_values - original_mean) / original_std
        
        # Normalized distribution (standard normal)
        y_values_norm = gaussian(x_values_norm, 0, 1)
        
        # Create rectangles for normalized distribution
        norm_rects = VGroup()
        
        for x, y in zip(x_values_norm, y_values_norm):
            rect = Rectangle(
                width=rect_width,
                height=norm_axes.y_axis.get_unit_size() * y,
                stroke_width=1,
                stroke_color=GREEN,
                fill_color=GREEN,
                fill_opacity=0.9
            )
            rect.move_to(norm_axes.c2p(x, y/2))
            norm_rects.add(rect)
        
        # Statistics text for normalized
        norm_stats = VGroup(
            Tex(r"\mu = 0.0", font_size=56, color=YELLOW),
            Tex(r"\sigma = 1.0", font_size=56, color=YELLOW)
        ).arrange(RIGHT, buff=0.5).next_to(norm_axes, DOWN, buff=0.5)
        
        # -------------------------------------------------------------
        # ANIMATION SEQUENCE
        # -------------------------------------------------------------
        
        # Show unnormalized axes
        self.play(
            ShowCreation(unnorm_axes),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Draw unnormalized distribution
        self.play(
            LaggedStartMap(FadeIn, unnorm_rects, lag_ratio=0.01),
            run_time=2.5
        )
        self.wait(0.5)
        
        # Show statistics
        self.play(Write(unnorm_stats), run_time=1)
        self.wait(1.5)
        
        # Transform both axes and distributions
        self.play(
            Transform(unnorm_axes, norm_axes),
            Transform(unnorm_rects, norm_rects),
            Transform(unnorm_stats, norm_stats),
            run_time=1
        )
        self.wait(0.5)
        
        self.wait(3)
        
