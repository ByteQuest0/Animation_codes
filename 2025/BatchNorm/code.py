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



class BatchNormMath(Scene):


    def construct(self):

        xbatch = Tex(r"x = B = \{x_1, x_2, \dots, x_m\}")
        mu = Tex(r"\mu_B = \frac{1}{m}\sum_{i=1}^m x_i")
        var = Tex(r"\sigma_B^2 = \frac{1}{m}\sum_{i=1}^m (x_i - \mu_B)^2")
        xhat = Tex(r"\hat{x}_i = \frac{x_i - \mu_B}{\sqrt{\sigma_B^2 + \varepsilon}}")
        y = Tex(r"y_i = \gamma\,\hat{x}_i + \beta")

        xbatch.scale(1.4).shift(UP*2.3)

        mu.next_to(xbatch, DOWN, buff=0.85).scale(1.34)

        self.play(ShowCreation(xbatch))

        self.wait(2)

        self.play(ShowCreation(mu))

        self.wait(2)

        var.next_to(mu, DOWN, buff=0.85).scale(1.34)

        self.play(ShowCreation(var))

        self.wait(2)

        xhat.next_to(var, DOWN, buff=1.25).scale(1.34)

        self.camera.frame.save_state()

        self.play(ShowCreation(xhat), self.camera.frame.animate.shift(DOWN*2.6))
        self.wait(2)

        rect = SurroundingRectangle(xhat).scale(1.1)
        self.play(ShowCreation(rect))
        self.wait(2)

        y.next_to(xhat, DOWN, buff=1.55).scale(1.54)

        self.play(ShowCreation(y), self.camera.frame.animate.shift(DOWN*2.6),
                 FadeOut(rect))
        self.wait(2)

        y[3].set_color("#00ff55")
        for i in range(5):
                self.play(Indicate(y[3], color="#00ff55"), run_time=0.5)
                     

        self.wait(2)

        y[-1].set_color("#ff0000")
        for i in range(5):
                self.play(Indicate(y[-1], color="#ff0000"), run_time=0.5)

        self.wait(2)


        a = Tex(r"x_i = z^{(l)} = W^{(l)} a^{(l-1)} + b^{(l)}").shift(RIGHT*11)
        a.scale(1.7)
        self.play(ShowCreation(a), self.camera.frame.animate.restore().shift(RIGHT*11))
        self.wait(2)

        rect = SurroundingRectangle(a[-4:]).scale(1.12)
        self.play(ShowCreation(rect))

        self.wait(2)

        self.play(
              Transform(a, Tex(r"\hat{z}^{(l)} = \frac{z^{(l)} - \mu_B}{\sqrt{\sigma_B^2 + \varepsilon}}").move_to(a).scale(1.88)),
              FadeOut(rect)
        )

        self.wait(2)

        self.play(a.animate.scale(0.7).shift(UP*2.5))
        self.wait(2)

        b = Tex(r"\mu_B = \frac{1}{m}\sum_{i=1}^m z^{(l)}_i").next_to(a, DOWN, buff=1.9).scale(1.7)
        

        self.play(TransformFromCopy(a[-10:-8],b))

        self.wait(2)

        self.play(Transform(b, Tex(r"\mu_B = \frac{1}{m}\sum_{i=1}^m \big(W^{(l)} a_i^{(l-1)} + b^{(l)}\big)").scale(1.7).move_to(b)))
        self.wait(2)

        self.play(Transform(b, Tex(r"\mu_B = \frac{1}{m}\sum_{i=1}^m W^{(l)} a_i^{(l-1)}"
            r"+ \frac{1}{m}\sum_{i=1}^m b^{(l)}").scale(1.45).move_to(b)))
        self.wait(2)

        self.play(Transform(b, Tex(r"\mu_B = W^{(l)}\left(\frac{1}{m}\sum_{i=1}^m a_i^{(l-1)}\right)"
            r"+ \frac{1}{m}\sum_{i=1}^m b^{(l)}").scale(1.35).move_to(b)))
        self.wait(2)


        self.play(Transform(b, Tex(r"\mu_B = W^{(l)}\left(\frac{1}{m}\sum_{i=1}^m a_i^{(l-1)}\right)"
            r"+ \frac{1}{m}\sum_{i=1}^m b^{(l)}").scale(1.35).move_to(b)))
        self.wait(2)



        rect = SurroundingRectangle(b[-12:]).scale(1.1)
        self.play(ShowCreation(rect),)

        self.wait(2)

        self.play(Transform(b, Tex(r"\mu_B = W^{(l)}\bar{a} + b^{(l)}").scale(1.65).move_to(b)), FadeOut(rect))
        self.wait(2)
        

        s3 = Tex(
                r"\hat{z}^{(l)} = "
                r"\frac{\,(W^{(l)} a^{(l-1)} + b^{(l)})"
                r" - \big(W^{(l)}\bar{a} + b^{(l)}\big)\,}"
                r"{\sqrt{\sigma_B^2 + \varepsilon}}"
            ).move_to(b).shift(UP*0.4+LEFT*0.4).scale(1.1)
            
        self.play(ReplacementTransform(VGroup(a,b), s3))

        self.play(Transform(s3, Tex(
                r"\hat{z}^{(l)} = "
                r"\frac{\,W^{(l)}\big(a^{(l-1)} - \bar{a}\big)\,}"
                r"{\sqrt{\sigma_B^2 + \varepsilon}}"
            ).scale(1.65).move_to(s3)),)
        self.wait(2)  

        self.camera.frame.save_state()

        self.play(self.camera.frame.animate.shift(LEFT*11+DOWN*5.5), FadeOut(s3))

        rect = SurroundingRectangle(y[-1]).scale(1.1)

        self.play(ShowCreation(rect))

        self.wait(2)
