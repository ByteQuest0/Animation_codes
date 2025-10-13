from manimlib import *
import numpy as np
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

class RegL1andL2(Scene):
    def construct(self):

        self.camera.frame.shift(UP * 0.23)
        np.random.seed(42)

        self.camera.frame.save_state()
        
        # Main dataset
        num_points = 17
        X = np.linspace(0, 4, num_points)
        y = 0.5 * X**2 - X + 2 + np.random.randn(num_points) * 0.3 + 0.3
        
        X = X[:-2]
        y = y[:-2]
        X += 0.44
        X_ = X.reshape(-1,1)
        
        def poly_fit_predict(X, y, degree):
            poly = PolynomialFeatures(degree)
            X_poly = poly.fit_transform(X)
            model = LinearRegression()
            model.fit(X_poly, y)
            y_pred = model.predict(X_poly)
            return model, y_pred, poly
        
        model_lin, _, _ = poly_fit_predict(X_, y, degree=1)
        model_good, _, _ = poly_fit_predict(X_, y, degree=2)
        overfit_degree = min(8, len(X)-1)
        model_over, _, _ = poly_fit_predict(X_, y, degree=overfit_degree)
        
        axes = Axes(
            x_range=[0,4,1], y_range=[0,8,1],
            width=10, height=6,
            axis_config={"include_tip": True, "include_numbers": False, "tick_size": 0, "stroke_width":6}
        ).move_to(ORIGIN)
        
        data_points = VGroup()
        for i in range(len(X)):
            data_points.add(Dot(axes.c2p(X[i], y[i]), radius=0.13).set_color(YELLOW))
        
        linear_curve = axes.get_graph(lambda x: model_lin.intercept_ + model_lin.coef_[1]*x,
                                      x_range=[0.1,4.4], color=BLUE_C).set_stroke(width=9)
        
        x_start = X[0]-0.06
        x_end = X[-1]+0.06
        def overfit_func(x):
            x_poly = PolynomialFeatures(overfit_degree).fit_transform([[x]])
            return model_over.predict(x_poly)[0]
        overfit_curve = axes.get_graph(overfit_func, x_range=[x_start,x_end], color="#ff0000").set_stroke(width=9)
        
        generalized_curve = axes.get_graph(lambda x: model_good.intercept_ + model_good.coef_[1]*x + model_good.coef_[2]*x**2,
                                           x_range=[0.13,4.13], color="#a305ff").set_stroke(width=9)
        
        y_label = Tex("y", font_size=68).next_to(axes.y_axis.get_top(), UP)
        x_label = Tex("x", font_size=68).next_to(axes.x_axis.get_right(), RIGHT)
        
        # Main animation
        self.play(ShowCreation(axes), Write(x_label), Write(y_label), run_time=1.5)
        self.play(FadeIn(data_points), run_time=1)
        self.play(ShowCreation(linear_curve), run_time=2)
        self.wait(2)
        self.play(Transform(linear_curve, overfit_curve), run_time=1.5)
        self.wait(2)
        self.play(Transform(linear_curve, generalized_curve), run_time=1.5)
        self.wait(2)


        # Move camera further right
        camera_shift = 14*RIGHT + 3.7*RIGHT
        
        # Top small overfit graph (far right)
        small_axes_over = Axes(
            x_range=[0,4,1], y_range=[0,8,1],
            width=5, height=3,
            axis_config={"include_tip": True, "include_numbers": False, "tick_size": 0, "stroke_width":6}
        ).shift(RIGHT*14 + UP*2)
        
        # Dots for top graph
        small_data_points_top = VGroup()
        for i in range(len(X)):
            small_data_points_top.add(Dot(
                small_axes_over.c2p(X[i], y[i]),
                radius=0.08, color=YELLOW
            ).set_color(YELLOW))
        
        small_over_curve = small_axes_over.get_graph(overfit_func, x_range=[x_start,x_end], color="#ff0000").set_stroke(width=8).set_z_index(1)
        over_eq = Tex(
            r"y = w_4 x^4 + w_3 x^3 + w_2 x^2 + w_1 x", font_size=53
        ).next_to(small_axes_over, RIGHT, buff=0.5)
        
        # Bottom small generalized graph (far right)
        small_axes_gen = Axes(
            x_range=[0,4,1], y_range=[0,8,1],
            width=5, height=3,
            axis_config={"include_tip": True, "include_numbers": False, "tick_size": 0, "stroke_width":6}
        ).next_to(small_axes_over, DOWN, buff=1)
        
        # Dots for bottom graph
        small_data_points_bottom = VGroup()
        for i in range(len(X)):
            small_data_points_bottom.add(Dot(
                small_axes_gen.c2p(X[i], y[i]),
                radius=0.08, color=YELLOW
            ).set_color(YELLOW))
        
        small_gen_curve = small_axes_gen.get_graph(
            lambda x: model_good.intercept_ + model_good.coef_[1]*x + model_good.coef_[2]*x**2,
            x_range=[0.13,4.13], color="#a305ff"
        ).set_stroke(width=8).set_z_index(1)
        gen_eq = Tex(
            r"y = w_2 x^2 + w_1 x", font_size=53
        ).next_to(small_axes_gen, RIGHT, buff=1.99)
        

        # Show small graphs, curves, dots, dotted line, and equations
        self.play(
            self.camera.frame.animate.shift(camera_shift).shift(DOWN*0.266).scale(1.045),
            ShowCreation(small_axes_over),
            ShowCreation(small_axes_gen),
            ShowCreation(small_over_curve),
            ShowCreation(small_gen_curve),
            FadeIn(small_data_points_top),
            FadeIn(small_data_points_bottom),
            Write(over_eq),
            Write(gen_eq),
            run_time=2
        )
        
        self.wait(2)

        rect = SurroundingRectangle(over_eq, buff=0.1, color=YELLOW, stroke_width=4).scale(1.08)
        self.play(ShowCreation(rect), run_time=1)
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(gen_eq, buff=0.1, color=YELLOW, stroke_width=4).scale(1.08)), run_time=1)

        self.wait()


        plain_loss = Tex(r"L(\mathbf{w}) = \frac{1}{N} \sum_{i=1}^{N} \left( y_i - \hat{y}_i \right)^2",   font_size=78).set_color(YELLOW)


        self.play(FadeOut(axes), FadeOut(linear_curve), FadeOut(data_points), FadeOut(rect), FadeOut(over_eq), 
                  FadeOut(gen_eq), FadeOut(small_axes_over), FadeOut(small_axes_gen), FadeOut(small_over_curve), 
                  FadeOut(small_gen_curve), FadeOut(small_data_points_top), FadeOut(small_data_points_bottom), FadeOut(x_label), FadeOut(y_label),
                  self.camera.frame.animate.restore(), Write(plain_loss), run_time=1)
        self.wait(2)


        temp = Tex(r"L_2(\mathbf{w}) = \ L(\mathbf{w}) + \lambda \sum_{j=1}^{M} w_j^2", font_size=73)
        temp[6:10].set_color(YELLOW)

        self.play(Transform(plain_loss, temp), run_time=1)
        self.wait(2)

        brace = Brace(plain_loss[-9:], DOWN, buff=0.33).set_color(YELLOW)
        self.play(GrowFromCenter(brace), run_time=1)
        temp1 = Text("penalty term", font_size=46, weight=BOLD).next_to(brace, DOWN, buff=0.34).set_color(PURPLE_C)
        self.play(Write(temp1), run_time=1)

        self.wait(2)
        
        plain_loss[-9].set_color(GREEN),
        self.play( Indicate(plain_loss[-9], color="#00ff00"), run_time=1)
        self.wait(2)

        title = Text("L2 Regularization", font_size=83, weight=BOLD).to_edge(UP).set_color(RED).shift(DOWN*0.33)
        self.play(Write(title), run_time=1)
        self.wait(2)

        temp = Tex(r"L_1(\mathbf{w}) = \ L(\mathbf{w}) + \lambda \sum_{j=1}^{M} |w_j|", font_size=73)
        temp[6:10].set_color(YELLOW)

        self.play(
            Transform(plain_loss, temp), 
            run_time=1)

        self.play(Transform(brace, Brace(plain_loss[-10:], DOWN, buff=0.33).set_color(YELLOW)), Transform(title, Text("L1 Regularization", font_size=83, weight=BOLD).to_edge(UP).set_color(TEAL).shift(DOWN*0.33)), run_time=1)
        self.wait(2)

        l1 = Text("L1", font_size=86, weight=BOLD).set_color(TEAL).to_edge(UP).shift(LEFT*3.3)
        l2 = Text("L2", font_size=86, weight=BOLD).set_color(RED).to_edge(UP).shift(RIGHT*3.3)
        
        self.play(FadeOut(brace), FadeOut(temp1), ReplacementTransform(title, VGroup(l1, l2)), FadeIn(l1), FadeIn(l2), FadeOut(plain_loss), run_time=1)

        l1_loss = Tex(r"L_1(\mathbf{w}) = L(\mathbf{w}) + \lambda \sum_{j=1}^{M} |w_j|").scale(0.9).next_to(l1,  DOWN).shift(DOWN*0.43)
        l2_loss = Tex(r"L_2(\mathbf{w}) = L(\mathbf{w}) + \lambda \sum_{j=1}^{M} w_j^2").scale(0.9).next_to(l2,  DOWN).shift(DOWN*0.43)

        l1_loss[6:10].set_color(YELLOW)
        l2_loss[6:10].set_color(YELLOW)

        self.play(
            TransformFromCopy(l1, l1_loss),
            TransformFromCopy(l2, l2_loss),
        )

        self.wait(2)

        l1_derivative = Tex(r"\frac{\partial L_1}{\partial w_j} = \frac{\partial L}{\partial w_j} + \lambda \cdot sign(w_j)").scale(0.98).next_to(l1_loss, DOWN).shift(DOWN*0.43)
        l2_derivative = Tex(r"\frac{\partial L_2}{\partial w_j} = \frac{\partial L}{\partial w_j} + 2 \lambda w_j").scale(0.98).next_to(l2_loss, DOWN).shift(DOWN*0.43)

        l1_derivative[8:14].set_color(YELLOW)
        l2_derivative[8:14].set_color(YELLOW)


        self.play(
            TransformFromCopy(l1_loss, l1_derivative),
            TransformFromCopy(l2_loss, l2_derivative),
        )

        self.wait()

        brace = Brace(l1_derivative[-10:], DOWN, buff=0.33).set_color(PURPLE_D)
        self.play(GrowFromCenter(brace), run_time=1)
        self.wait(2)

        self.play(Transform(brace, Brace(l2_derivative[-4:], DOWN, buff=0.33).set_color(YELLOW)), run_time=1)
        self.wait(2)

        l1_update = Tex(r"w_j \leftarrow w_j - \eta \left( \frac{\partial L}{\partial w_j} + \lambda \cdot sign(w_j) \right)").scale(0.9).next_to(l1_derivative, DOWN).shift(DOWN*0.63)
        l2_update = Tex(r"w_j \leftarrow w_j - \eta \left( \frac{\partial L}{\partial w_j} + 2 \lambda w_j \right)").scale(0.9).next_to(l2_derivative, DOWN).shift(DOWN*0.63)

        l1_update[8:14].set_color(YELLOW)
        l2_update[8:14].set_color(YELLOW)


        self.play(
            TransformFromCopy(l1_derivative, l1_update),
            TransformFromCopy(l2_derivative, l2_update), FadeOut(brace), FadeOut(temp1)
        )

        self.wait(2)


        camera_shift = 15*RIGHT
        
        # Create axes at same position as camera
        axes_reg = Axes(
            x_range=[-5,5,1], y_range=[-3.6,3.6,1],
            axis_config={
                "include_tip": True,
                "include_numbers": False,
                "tick_size":0,
                "stroke_width":6
            }
        ).shift(15*RIGHT)  # position matches camera shift

        y_label = Tex("w_2", font_size=68).next_to(axes_reg.y_axis.get_top(), UP)
        x_label = Tex("w_1", font_size=68).next_to(axes_reg.x_axis.get_right(), RIGHT)
        
        self.play(ShowCreation(axes_reg), self.camera.frame.animate.shift(camera_shift+UP*0.4).scale(1.14))
        self.play(Write(x_label), Write(y_label), run_time=1)

        self.wait(0.5)

        l1_equation = Tex(r"L_2 \rightarrow w_1^2 + w_2^2 = c", font_size=65).next_to(axes_reg, UP, buff=0.5).shift(LEFT*4.57+DOWN*0.33).set_color(RED)
        l2_equation = Tex(r"L_1 \rightarrow |w_1|  + |w_2| = c", font_size=65).next_to(axes_reg, UP, buff=0.5).shift(RIGHT*4.57+DOWN*0.33).set_color(TEAL)

        self.play(Write(l1_equation), Write(l2_equation), run_time=1)
        self.wait(2)

        self.play(FadeOut(l1_equation), FadeOut(l2_equation), run_time=1)



        # --- Multiple Elliptical Contours representing loss levels ---
        ellipse_center = axes_reg.c2p(2, 1)
        ellipse_group = VGroup()
        
        # Different scale levels (smaller to larger)
        scales = [0.6, 0.86, 1.2, 1.5]
        
        for s in scales:
            e = Ellipse(
                width=4.5 * s, height=2.5 * s,
                color=YELLOW, stroke_width=4
            ).move_to(ellipse_center).rotate(-PI/13).set_color(YELLOW)
            ellipse_group.add(e)
        
        # Shift all ellipses slightly to desired position
        ellipse_group.shift(RIGHT*0.4 + UP*1.45)
        self.wait(2)

        # Animate them in sequence
        for e in ellipse_group:
            self.play(ShowCreation(e), run_time=0.8)
        self.wait(2)
        


        # --- Add L1 diamond centered at origin ---
        l1_diamond = Polygon(
            axes_reg.c2p(0, 2),     # top
            axes_reg.c2p(2, 0),     # right
            axes_reg.c2p(0, -2),    # bottom
            axes_reg.c2p(-2, 0),    # left
            color=TEAL,
            stroke_width=6
        ).set_z_index(2).scale(1.05)

        dot = Dot(ellipse_group.get_center(), color="#ff0000", radius=0.255).set_color("#ff0000")
        text = Text("X", font_size=46, weight=BOLD).move_to(dot).set_z_index(3)
        dot = VGroup(dot, text)
        self.play(ShowCreation(dot), run_time=1)
        self.wait(2)

        PURPLE = PINK
        # Dot center in scene coordinates
        dot_center = dot.get_center()
        
        # Perpendicular projection onto x-axis (same y as axes origin)
        x_axis_y = axes_reg.c2p(0, 0)[1]  # y-coordinate of x-axis line
        x_proj = np.array([dot_center[0], x_axis_y, dot_center[2]])  # same x, y at x-axis
        
        # Perpendicular projection onto y-axis (same x as axes origin)
        y_axis_x = axes_reg.c2p(0, 0)[0]  # x-coordinate of y-axis line
        y_proj = np.array([y_axis_x, dot_center[1], dot_center[2]])  # same y, x at y-axis
        
        # Dashed lines
        line_x = DashedLine(dot_center, x_proj, color=PURPLE, stroke_width=5, dash_length=0.1).set_z_index(-1)
        line_y = DashedLine(dot_center, y_proj, color=PURPLE, stroke_width=5, dash_length=0.1).set_z_index(-1)
        
        # Labels at intersections
        w1_label = Tex(r"w_1^*", font_size=66, color=PURPLE).next_to(x_proj, DOWN, buff=0.2).set_color(PURPLE).set_z_index(4)
        w2_label = Tex(r"w_2^*", font_size=66, color=PURPLE).next_to(y_proj, LEFT, buff=0.2).set_color(PURPLE).set_z_index(4)
        
        # Animate
        self.play(
            ShowCreation(line_x),
            ShowCreation(line_y),
            Write(w1_label),
            Write(w2_label),
            run_time=2
        )
        self.wait(2)

        self.play(FadeOut(line_x), FadeOut(line_y), FadeOut(w1_label), FadeOut(w2_label),  run_time=1)
        self.play(ShowCreation(l1_diamond), run_time=1.5)
        self.wait(2)


        dot1 = Dot(ellipse_group.get_center(), color="#8c00cc", radius=0.255).set_color("#29CA6A").set_z_index(3)
        text = Text("X", font_size=46, weight=BOLD).move_to(dot).set_z_index(3)
        dot_new = VGroup(dot1, text).move_to(l1_diamond.get_top()).set_z_index(3)       
        
        self.play(TransformFromCopy(dot, dot_new))

        self.wait(2)


        self.play(FadeOut(l1_diamond), FadeOut(dot_new))
        self.wait(2)

        # Center of circle in (w1, w2) coordinates
        circle_center = axes_reg.c2p(0, 0)  # adjust position if needed
        
        # Create the L2 contour circle (w1^2 + w2^2 = c)
        circle = Circle(
            radius=2.1,           # controls size of contour
            color=YELLOW,
            stroke_width=6
        ).move_to(circle_center).set_color(RED)
        
        # Optional rotation or shift if you want angled look
        # circle.rotate(-PI/10)
        
        self.play(ShowCreation(circle), run_time=1.5)
        self.wait(2)       
        
        dot1 = Dot(ellipse_group.get_center(), color="#8c00cc", radius=0.255).set_color("#3700fe")
        text = Text("X", font_size=46, weight=BOLD).move_to(dot).set_z_index(3)
        dot_new = VGroup(dot1, text).move_to(l1_diamond.get_top()).shift(DOWN*0.35+RIGHT*1.2).set_z_index(3)     
        
        self.play(TransformFromCopy(dot, dot_new))

        self.wait()

        PURPLE = GREEN
        # Dot center in scene coordinates
        dot_center = dot_new.get_center()
        
        # Perpendicular projection onto x-axis (same y as axes origin)
        x_axis_y = axes_reg.c2p(0, 0)[1]  # y-coordinate of x-axis line
        x_proj = np.array([dot_center[0], x_axis_y, dot_center[2]])  # same x, y at x-axis
        
        # Perpendicular projection onto y-axis (same x as axes origin)
        y_axis_x = axes_reg.c2p(0, 0)[0]  # x-coordinate of y-axis line
        y_proj = np.array([y_axis_x, dot_center[1], dot_center[2]])  # same y, x at y-axis
        
        # Dashed lines
        line_x = DashedLine(dot_center, x_proj, color=PURPLE, stroke_width=5, dash_length=0.1).set_z_index(-1)
        line_y = DashedLine(dot_center, y_proj, color=PURPLE, stroke_width=5, dash_length=0.1).set_z_index(-1)
        
        # Labels at intersections
        w1_label = Tex(r"w_1^*", font_size=56, ).next_to(x_proj, DOWN, buff=0.2).set_color(PURPLE).set_z_index(4)
        w2_label = Tex(r"w_2^*", font_size=56, ).next_to(y_proj, LEFT, buff=0.2).set_color(PURPLE).set_z_index(4)
        
        # Animate
        self.play(
            ShowCreation(line_x),
            ShowCreation(line_y),
            Write(w1_label),
            Write(w2_label),
            run_time=2
        )
        self.wait(2)

        self.play(self.camera.frame.animate.restore())


        self.wait(2)

        l2_text = Tex(r"L_2(\mathbf{w}, \mathbf{b}) = L(\mathbf{w}, \mathbf{b}) + \lambda \sum_{j=1}^{M} w_j^2",font_size=72).shift(UP*1.8)

        l1_text = Tex(r"L_1(\mathbf{w}, \mathbf{b}) = L(\mathbf{w}, \mathbf{b}) + \lambda \sum_{j=1}^{M} |w_j|", font_size=72).next_to(l2_text, DOWN, buff=0.99)

        l2_text[:7].set_color(RED)
        l1_text[:7].set_color(TEAL)

        l2_text[8:14].set_color(YELLOW)
        l1_text[8:14].set_color(YELLOW)

        self.play(FadeIn(VGroup(l1_text, l2_text)), FadeOut(VGroup(l1, l2, l1_derivative, l2_derivative, l1_update, l2_update, l1_loss, l2_loss )))
        self.wait(2)

        # --- L1 Regularization with separate sums ---
        l1_text_sep = Tex(
            r"L_1(\mathbf{w}, \mathbf{b}) = L(\mathbf{w}, \mathbf{b}) + "
            r"\lambda \sum_{j=1}^{M} |w_j| + \lambda \sum_{k=1}^{N} |b_k|",
            font_size=58,
            color=YELLOW
        ).move_to(l1_text)
        
        # --- L2 Regularization with separate sums ---
        l2_text_sep = Tex(
            r"L_2(\mathbf{w}, \mathbf{b}) = L(\mathbf{w}, \mathbf{b}) + "
            r"\lambda \sum_{j=1}^{M} w_j^2 + \lambda \sum_{k=1}^{N} b_k^2",
            font_size=58,
            color=GREEN
        ).move_to(l2_text)  # same position for smooth transform
        
        l2_text_sep[:7].set_color(RED)
        l1_text_sep[:7].set_color(TEAL)

        l2_text_sep[8:14].set_color(YELLOW)
        l1_text_sep[8:14].set_color(YELLOW)


        self.play(Transform(l1_text, l1_text_sep), Transform(l2_text, l2_text_sep), run_time=1.5)

        rect = SurroundingRectangle(l1_text[-10:]).scale(1.03).set_color("#ff0000")
        rect1 = SurroundingRectangle(l2_text[-9:]).scale(1.03).set_color("#ff0000")

        self.play(ShowCreation(rect), ShowCreation(rect1))

        self.wait(2)


        l2_text1 = Tex(r"L_2(\mathbf{w}, \mathbf{b}) = L(\mathbf{w}, \mathbf{b}) + \lambda \sum_{j=1}^{M} w_j^2",font_size=72).shift(UP*1.8)

        l1_text1 = Tex(r"L_1(\mathbf{w}, \mathbf{b}) = L(\mathbf{w}, \mathbf{b}) + \lambda \sum_{j=1}^{M} |w_j|", font_size=72).next_to(l2_text, DOWN, buff=0.99)

        l2_text1[:7].set_color(RED)
        l1_text1[:7].set_color(TEAL)

        l2_text1[8:14].set_color(YELLOW)
        l1_text1[8:14].set_color(YELLOW)   

        self.play(
            Transform(l1_text, l1_text1),
            Transform(l2_text, l2_text1),
            Uncreate(rect),
            Uncreate(rect1)
        )  

        self.wait(2)   






class DataAugmentation(Scene):
    def construct(self):
        # === Title ===
        title = Text("Data Augmentation", font="Arial", color=BLUE).scale(0.9).to_edge(UP)
        self.wait(0.5)

        # === Original image (top center) ===
        original = ImageMobject("cat.jpg")
        original.set_height(2.5)
        original.move_to(UP * 2.2)
        self.play(FadeIn(original))
        self.wait(0.5)

        # === Augmented image filenames ===
        image_names = [
            "cropped.png", "flipped.png", "grayscale.png", "cropped_gray_flipped.png", "blurred.png",
            "brightness.png", "contrast.png", "saturation.png", "hue.png", "combined.png"
        ]

        # === Grid placement (2 rows × 5 columns) ===
        images = []
        start_y = -0.3  # vertical offset for top row
        start_x = -5.0  # horizontal start position

        for i, name in enumerate(image_names):
            img = ImageMobject(name)
            img.set_height(1.6)
            row = i // 5
            col = i % 5
            pos = np.array([start_x + col * 2.5, start_y - row * 2.3, 0])
            img.move_to(pos)
            images.append(img)

        # === Animate appearance (from original copy to each) ===
        for img in images:
            self.play(TransformFromCopy(original, img))
            self.wait(0.2)

        self.wait(2)
        
class EarlyStoppingAnimation(Scene):
    def construct(self):
        
        self.camera.frame.shift(DOWN*0.63)

        # Create axes without ticks and numbers
        axes = Axes(
            x_range=[0, 50, 10],
            y_range=[0, 1, 0.2],
            width=10,
            height=6,
            axis_config={
                "include_tip": True,
                "include_numbers": False,
                "tick_size": 0,
                "stroke_width": 6,
            }
        )
        axes.shift(DOWN * 0.5)
        
        # Create axis labels
        x_label = Text("Epochs", font_size=46, weight=BOLD).next_to(axes.x_axis, DOWN)
        y_label = Text("Loss", font_size=46, weight=BOLD).next_to(axes.y_axis, LEFT).rotate(90 * DEGREES)
        
        # Define loss functions - both start at y=0.4
        def training_loss(x):
            # Starts at 0.4, decreases and saturates lower
            return 0.4 * np.exp(-0.08 * x) + 0.15
        
        def validation_loss(x):
            # Starts at 0.4, follows training pattern initially but stays higher
            # Then slowly increases after x=20 (not too parabolic)
            base_curve = 0.4 * np.exp(-0.08 * x) + 0.2
            # Add gentle upward curve after epoch 20
            if x > 20:
                upturn = 0.0003 * (x - 20) ** 1.8
            else:
                upturn = 0
            return base_curve + upturn
        
        # Create graphs with increased stroke width
        # RED for training, BLUE for validation
        training_graph = axes.get_graph(
            training_loss,
            x_range=[0, 50],
            color=RED,
            stroke_width=6
        )
        
        validation_graph = axes.get_graph(
            validation_loss,
            x_range=[0, 50],
            color=BLUE,
            stroke_width=6
        )
        
        # Create legend in top right corner
        legend_box = Rectangle(
            width=3.5,
            height=1.2,
            fill_color=BLACK,
            fill_opacity=0.8,
            stroke_color=WHITE,
            stroke_width=2
        )
        legend_box.to_corner(UR, buff=0.5).shift(LEFT*0.45+DOWN*1.2)
        
        # Training loss legend line (RED)
        training_line = Line(
            LEFT * 0.5,
            RIGHT * 0.5,
            color=RED,
            stroke_width=6
        )
        training_line.move_to(legend_box.get_center() + UP * 0.3 + LEFT * 1.2)
        
        training_text = Text("Training", font_size=24, color=WHITE)
        training_text.next_to(training_line, RIGHT, buff=0.2)
        
        # Validation loss legend line (BLUE)
        validation_line = Line(
            LEFT * 0.5,
            RIGHT * 0.5,
            color=BLUE,
            stroke_width=6
        )
        validation_line.move_to(legend_box.get_center() + DOWN * 0.3 + LEFT * 1.2)
        
        validation_text = Text("Testing", font_size=24, color=WHITE)
        validation_text.next_to(validation_line, RIGHT, buff=0.2)
        
        legend_group = VGroup(legend_box, training_line, training_text, validation_line, validation_text)
        legend_box.shift(LEFT*0.5)
        # Animate axes and labels
        self.play(
            FadeIn(axes),
            Write(x_label),
            Write(y_label),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Show legend
        self.play(
            FadeIn(legend_group),
            run_time=1
        )
        self.wait(0.5)
        
        # Create both graphs first
        self.play(
            ShowCreation(training_graph),
            ShowCreation(validation_graph),
            run_time=3
        )
        self.wait(1)
        
        # Create moving dots
        training_dot = Dot(color=RED, radius=0.13).set_color("#20FF33")
        validation_dot = Dot(color=BLUE, radius=0.13).set_color("#20FF33")
        
        # Initialize dots at starting position
        training_dot.move_to(axes.c2p(0, training_loss(0)))
        validation_dot.move_to(axes.c2p(0, validation_loss(0)))
        
        # Create ValueTracker for animation
        epoch_tracker = ValueTracker(0)
        
        # Add updaters for dots to trace along the graphs
        training_dot.add_updater(
            lambda m: m.move_to(
                axes.c2p(epoch_tracker.get_value(), training_loss(epoch_tracker.get_value()))
            )
        )
        
        validation_dot.add_updater(
            lambda m: m.move_to(
                axes.c2p(epoch_tracker.get_value(), validation_loss(epoch_tracker.get_value()))
            )
        )
        
        # Add dots to scene
        self.play(
            FadeIn(training_dot),
            FadeIn(validation_dot),
            run_time=0.5
        )
        
        # Animate dots moving along curves up to early stopping point (epoch 20)
        self.play(
            epoch_tracker.animate.set_value(20),
            run_time=3,
            rate_func=linear
        )
        
        # Pause when validation loss is at minimum
        self.wait(0.8)
        
        # Continue animation to show divergence
        self.play(
            epoch_tracker.animate.set_value(45),
            run_time=2,
            rate_func=linear
        )
        
        self.wait(0.5)
        
        # Remove updaters
        training_dot.clear_updaters()
        validation_dot.clear_updaters()
        
        # Highlight the early stopping point with just a dotted line
        # Create vertical dashed line at epoch 20
        early_stop_line = DashedLine(
            axes.c2p(20, 0),
            axes.c2p(20, 0.8),
            color=YELLOW,
            stroke_width=5,
            dash_length=0.15
        )
        
        # Add "Early Stopping" label ABOVE the line (on top)
        early_stop_label = Text(
            "Early Stopping",
            font_size=48,
            color=YELLOW
        )
        early_stop_label.next_to(axes.c2p(20, 0.8), UP, buff=0.2)
        
        # Animate the dotted line
        self.play(
            ShowCreation(early_stop_line),
            Write(early_stop_label),
            run_time=1.5
        )
        
        self.wait(3)



class DropOutMath(Scene):
    def construct(self):

        a = Tex(r"z^{(l)} = W^{(l)} a^{(l-1)} + b^{(l)}").scale(1.3).shift(UP*1.2)

        self.play(Write(a))
        self.wait(2)

        b = Tex(r"a^{(l)} = f\big(z^{(l)}\big)")
        b.scale(1.3).next_to(a, DOWN, buff=0.8)

        self.play(Write(b))
        self.wait(2)

        self.play( VGroup(a, b).animate.shift(UP*1.35))

        c = Tex(r"r^{(l)}_i \sim \ Bernoulli(1 - p)")
        c.scale(1.3).next_to(b, DOWN, buff=1.14)

        d = Tex(r"P(r^{(l)}_i = 1) = 1 - p, \quad P(r^{(l)}_i = 0) = p")
        d.scale(1.3).next_to(c, DOWN, buff=0.8)

        self.play(Write(c))
        self.wait()

        self.play(Write(d))


        rect = SurroundingRectangle(c, buff=0.3, color=YELLOW)
        self.play(ShowCreation(rect))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(d, buff=0.3, color=YELLOW)))
 
        self.wait(2)

        e = Tex(r"\tilde{a}^{(l)} = r^{(l)} \odot a^{(l)}")

        e.scale(1.99)

        self.play(ReplacementTransform(VGroup(c, d, a, b, rect),e ))

        self.wait(2)

        self.play(e[10].animate.set_color(RED))
        self.wait(2)

        temp = Tex(r"""
        \tilde{a}^{(l)} =
        \begin{bmatrix}
        a^{(l)}_1 \\[7pt]
        a^{(l)}_2 \\[7pt]
        a^{(l)}_3 \\[7pt]
        a^{(l)}_4 \\[7pt]
        a^{(l)}_5 \\[7pt]
        a^{(l)}_6 \\[7pt]
        a^{(l)}_7
        \end{bmatrix}
        \odot
        \begin{bmatrix}
        1 \\[1pt]
        0 \\[1pt]
        1 \\[1pt]
        1 \\[1pt]
        0 \\[1pt]
        1 \\[1pt]
        1 \\[1pt]
        0 \\[1pt]
        1 \\[1pt]
        0
        \end{bmatrix}
        =
        \begin{bmatrix}
        a^{(l)}_1 \\[7pt]
        0 \\[7pt]
        a^{(l)}_3 \\[7pt]
        a^{(l)}_4 \\[7pt]
        0 \\[7pt]
        a^{(l)}_6 \\[7pt]
        0
        \end{bmatrix}
        """).move_to(e)

        aa = e.copy()
        
        self.play(Transform(e, temp))

        self.wait(2)

        self.play(Transform(e, aa))
        self.wait(2)

        aa = Tex(r"\tilde{a}^{(l)} = \frac{r^{(l)} \odot a^{(l)}}{1 - p}").move_to(e).scale(1.99)
        self.play(Transform(e, aa), run_time=0.9)

        self.wait(2)






class DropoutRegularization(Scene):
    def construct(self):
        # Camera + reproducible RNG
        self.camera.frame.scale(1.2).shift(RIGHT*0.8)
        rng = np.random.RandomState(11)

        # Colors
        FWD_COLOR = "#FF0000"                 # forward pulses fixed red
        BWD_EPOCH_COLORS = ["#00FF00", "#7000D9", "#FC12A7", "#EAFF01"]  # per-epoch backprop colors (4 epochs)

        # Pulse helpers (glow aesthetic consistent with project)
        def create_glow(center_point, radius=0.15, color=YELLOW, intensity=0.3):
            g = VGroup()
            for i in range(20):
                rr = radius * (1 + 0.1 * i)
                op = intensity * (1 - i/20)
                g.add(Circle(radius=rr, stroke_opacity=0, fill_color=color, fill_opacity=op).move_to(center_point))
            return g

        def create_pulse(point, color="#ff0000", radius=0.12):
            dot = Dot(radius=radius, color=color, fill_opacity=1).move_to(point)
            glow = create_glow(point, radius=radius*0.83, color=color, intensity=0.4)
            return VGroup(glow, dot)

        # Build nodes with explicit radius tracking
        input_radius = 0.36
        hidden_radius = 0.5
        output_radius = 0.72
        
        input_layer = [Circle(radius=input_radius, color=GREEN, fill_opacity=1, stroke_width=6, stroke_color=GREEN_B).move_to(
            LEFT * 6 + UP * (2.5 - i * 1.2)) for i in range(5)]
        hidden_layer1 = [Circle(radius=hidden_radius, color=BLUE_C, fill_opacity=1, stroke_width=8, stroke_color=BLUE_B).move_to(
            LEFT * 3 + UP * (2.4 - i * 1.6)) for i in range(4)]
        hidden_layer2 = [Circle(radius=hidden_radius, color=BLUE_C, fill_opacity=1, stroke_width=8, stroke_color=BLUE_B).move_to(
            ORIGIN + UP * (3.2 - i * 1.6)) for i in range(5)]
        hidden_layer3 = [Circle(radius=hidden_radius, color=BLUE_C, fill_opacity=1, stroke_width=8, stroke_color=BLUE_B).move_to(
            RIGHT * 3 + UP * (1.6 - i * 1.6)) for i in range(3)]
        output_node = Circle(radius=output_radius, color=BLUE_C, fill_opacity=1, stroke_width=8, stroke_color=BLUE_B).move_to(RIGHT * 6)

        # Fully-connect helper (z_index behind nodes) + connection maps
        def fully_connect_with_map(src, dst):
            lines, cmap = [], {}
            for i, s in enumerate(src):
                for j, d in enumerate(dst):
                    ln = Line(
                        s.get_center(), d.get_center(),
                        stroke_width=2, color=GREY_A, stroke_opacity=0.6
                    ).set_z_index(-1)
                    lines.append(ln)
                    cmap[(i, j)] = ln
            return lines, cmap

        input_to_h1,  conn_in_h1  = fully_connect_with_map(input_layer,   hidden_layer1)
        h1_to_h2,     conn_h1_h2  = fully_connect_with_map(hidden_layer1, hidden_layer2)
        h2_to_h3,     conn_h2_h3  = fully_connect_with_map(hidden_layer2, hidden_layer3)
        h3_to_output, conn_h3_out = [], {}
        for i, h3 in enumerate(hidden_layer3):
            ln = Line(
                h3.get_center(), output_node.get_center(),
                stroke_width=2, color=GREY_A, stroke_opacity=0.6
            ).set_z_index(-1)
            h3_to_output.append(ln)
            conn_h3_out[(i, 0)] = ln

        all_nodes = input_layer + hidden_layer1 + hidden_layer2 + hidden_layer3 + [output_node]
        all_lines = input_to_h1 + h1_to_h2 + h2_to_h3 + h3_to_output

        # Incident mapping: lines per node (for dropout removal/restoration)
        incident = {}
        
        def rebuild_incident_mapping():
            """Rebuild the entire incident mapping from scratch based on current connection maps"""
            # Clear all existing mappings
            incident.clear()
            
            # Initialize for all nodes
            for nd in input_layer + hidden_layer1 + hidden_layer2 + hidden_layer3 + [output_node]:
                incident[id(nd)] = []
            
            # Add lines from connection maps - ONLY if they're currently in the scene
            for (i, j), ln in conn_in_h1.items():
                if ln in self.mobjects:  # Check if line is actually in scene
                    incident[id(input_layer[i])].append(ln)
                    incident[id(hidden_layer1[j])].append(ln)
            
            for (i, j), ln in conn_h1_h2.items():
                if ln in self.mobjects:
                    incident[id(hidden_layer1[i])].append(ln)
                    incident[id(hidden_layer2[j])].append(ln)
            
            for (i, j), ln in conn_h2_h3.items():
                if ln in self.mobjects:
                    incident[id(hidden_layer2[i])].append(ln)
                    incident[id(hidden_layer3[j])].append(ln)
            
            for (i, j), ln in conn_h3_out.items():
                if ln in self.mobjects:
                    incident[id(hidden_layer3[i])].append(ln)
                    incident[id(output_node)].append(ln)
        
        # Initial build
        rebuild_incident_mapping()

        # Storage for node and line properties
        node_props = {}
        line_props = {}
        
        # Store original properties for all nodes
        for i, nd in enumerate(input_layer):
            node_props[id(nd)] = {
                'center': nd.get_center().copy(),
                'radius': input_radius,
                'color': nd.get_color(),
                'fill_opacity': nd.get_fill_opacity(),
                'stroke_width': nd.get_stroke_width(),
                'stroke_color': nd.get_stroke_color(),
            }
        
        for nd in hidden_layer1 + hidden_layer2 + hidden_layer3:
            node_props[id(nd)] = {
                'center': nd.get_center().copy(),
                'radius': hidden_radius,
                'color': nd.get_color(),
                'fill_opacity': nd.get_fill_opacity(),
                'stroke_width': nd.get_stroke_width(),
                'stroke_color': nd.get_stroke_color(),
            }
        
        node_props[id(output_node)] = {
            'center': output_node.get_center().copy(),
            'radius': output_radius,
            'color': output_node.get_color(),
            'fill_opacity': output_node.get_fill_opacity(),
            'stroke_width': output_node.get_stroke_width(),
            'stroke_color': output_node.get_stroke_color(),
        }
        
        # Store original properties for all lines
        for ln in all_lines:
            line_props[id(ln)] = {
                'start': ln.get_start().copy(),
                'end': ln.get_end().copy(),
            }

        # Show network cleanly
        self.play(*[GrowFromCenter(n) for n in all_nodes])
        self.play(*[ShowCreation(l) for l in all_lines])
        self.wait(0.2)

        # Optional minimal UI - START WITH EPOCH 0 AND BOLD TEXT
        p_text     = Text("p = 0.5", weight=BOLD).scale(1.8).to_corner(UR).shift(DOWN*0.2+RIGHT*1.07)
        loss_label = Text("Loss").scale(2.2)
        loss_rect  = SurroundingRectangle(loss_label, fill_color=RED, fill_opacity=0.25, color=RED).scale(1.42).set_z_index(-1)
        loss_group = VGroup(loss_label, loss_rect).to_corner(DR).shift(RIGHT*1.17+UP*0)
        self.play(Write(p_text), Write(loss_label), ShowCreation(loss_rect))




        # Dropout utilities
        def sample_mask(n, p):
            m = (rng.rand(n) > p)
            if not m.any():
                m[rng.randint(0, n)] = True
            return m

        # First-epoch hint: outline dropped nodes then remove outline
        def outline_dropped(layer_nodes, mask):
            rings = []
            for nd, keep in zip(layer_nodes, mask):
                if not keep:
                    rings.append(Circle(radius=nd.get_width()/2, color=RED, stroke_width=15).move_to(nd.get_center()))
            return rings

        # Store properties and remove dropped nodes/lines
        def remove_dropout(layer_nodes, mask):
            nodes = [nd for nd, keep in zip(layer_nodes, mask) if not keep]
            lines = []
            seen = set()
            
            # Rebuild incident mapping first to ensure accuracy
            rebuild_incident_mapping()
            
            # Collect incident lines from the node's incident list
            for nd in nodes:
                node_id = id(nd)
                if node_id in incident:
                    for ln in incident[node_id][:]:
                        if id(ln) not in seen and ln in self.mobjects:  # Only if line is in scene
                            seen.add(id(ln))
                            lines.append(ln)
            
            # Slower fadeout for better visibility
            anims = [FadeOut(ln,) for ln in lines] + [FadeOut(nd,) for nd in nodes]
            if anims:
                self.play(*anims,)
            
            # Remove from scene explicitly
            for ln in lines:
                self.remove(ln)
            for nd in nodes:
                self.remove(nd)
            
            return nodes, lines

        # Recreate nodes and lines from stored properties, preserving backprop colors
        def restore_dropout(layer_nodes, old_nodes, old_lines):
            new_nodes = []
            new_lines = []
            
            # Recreate nodes with original properties
            for old_nd in old_nodes:
                props = node_props[id(old_nd)]
                new_nd = Circle(
                    radius=props['radius'],
                    color=props['color'],
                    fill_opacity=props['fill_opacity'],
                    stroke_width=props['stroke_width'],
                    stroke_color=props['stroke_color']
                ).move_to(props['center'])
                new_nodes.append(new_nd)
                
                # Replace in layer_nodes list
                idx = layer_nodes.index(old_nd)
                layer_nodes[idx] = new_nd
                
                # Copy node properties to new node
                node_props[id(new_nd)] = node_props[id(old_nd)].copy()
            
            # Recreate lines - PRESERVE current colors from backprop
            for old_ln in old_lines:
                # Get stored position
                if id(old_ln) in line_props:
                    props = line_props[id(old_ln)]
                else:
                    props = {
                        'start': old_ln.get_start().copy(),
                        'end': old_ln.get_end().copy(),
                    }
                
                # Get CURRENT color from the old line (preserves backprop color)
                current_color = old_ln.get_color()
                current_width = old_ln.get_stroke_width()
                current_opacity = old_ln.get_stroke_opacity()
                
                new_ln = Line(
                    props['start'], props['end'],
                    stroke_width=current_width,
                    color=current_color,
                    stroke_opacity=current_opacity
                ).set_z_index(-1)
                new_lines.append(new_ln)
                
                # Store new line properties
                line_props[id(new_ln)] = props.copy()
                
                # Update connection maps
                if old_ln in input_to_h1:
                    idx = input_to_h1.index(old_ln)
                    input_to_h1[idx] = new_ln
                    for key, val in list(conn_in_h1.items()):
                        if val is old_ln:
                            conn_in_h1[key] = new_ln
                
                elif old_ln in h1_to_h2:
                    idx = h1_to_h2.index(old_ln)
                    h1_to_h2[idx] = new_ln
                    for key, val in list(conn_h1_h2.items()):
                        if val is old_ln:
                            conn_h1_h2[key] = new_ln
                
                elif old_ln in h2_to_h3:
                    idx = h2_to_h3.index(old_ln)
                    h2_to_h3[idx] = new_ln
                    for key, val in list(conn_h2_h3.items()):
                        if val is old_ln:
                            conn_h2_h3[key] = new_ln
                
                elif old_ln in h3_to_output:
                    idx = h3_to_output.index(old_ln)
                    h3_to_output[idx] = new_ln
                    for key, val in list(conn_h3_out.items()):
                        if val is old_ln:
                            conn_h3_out[key] = new_ln
            
            # Animate creation with slower speed
            anims = [GrowFromCenter(nd,) for nd in new_nodes] + [ShowCreation(ln,) for ln in new_lines]
            if anims:
                self.play(*anims)
            
            # Rebuild entire incident mapping from scratch after restoration
            rebuild_incident_mapping()
            
            return new_nodes, new_lines




        # Forward pulses (respect masks)
        def pulse_stage(src_nodes, dst_nodes, color, src_mask=None, dst_mask=None, run_time=0.75):
            pulses, anims = [], []
            for i, s in enumerate(src_nodes):
                if src_mask is not None and not src_mask[i]:
                    continue
                for j, d in enumerate(dst_nodes):
                    if dst_mask is not None and not dst_mask[j]:
                        continue
                    p = create_pulse(s.get_center(), color)
                    pulses.append(p); self.add(p)
                    anims.append(p.animate.move_to(d.get_center()))
            if anims:
                self.play(*anims, run_time=run_time)
                self.play(*[FadeOut(p) for p in pulses], run_time=0.25)

        # Build edge-color animations for current active pairs in a map
        def edge_color_anims(conn_map, src_mask, dst_mask, color, width=3):
            anims = []
            for (i, j), ln in conn_map.items():
                # Only animate lines that are currently in the scene
                if ln in self.mobjects and (src_mask is None or src_mask[i]) and (dst_mask is None or dst_mask[j]):
                    anims.append(ln.animate.set_stroke(color=color, width=width, opacity=0.95))
            return anims

        # Backprop stage: move pulses and color edges simultaneously
        def backprop_stage(src_nodes, dst_nodes, conn_map, src_mask, dst_mask, color, run_time=0.65):
            pulses, pulse_anims = [], []
            for j, s in enumerate(src_nodes):
                if src_mask is not None and not src_mask[j]:
                    continue
                for i, d in enumerate(dst_nodes):
                    if dst_mask is not None and not dst_mask[i]:
                        continue
                    p = create_pulse(s.get_center(), color)
                    pulses.append(p); self.add(p)
                    pulse_anims.append(p.animate.move_to(d.get_center()))
            color_anims = edge_color_anims(conn_map, dst_mask, src_mask, color, width=3)
            if pulse_anims or color_anims:
                self.play(*(pulse_anims + color_anims), run_time=run_time)
                if pulses:
                    self.play(*[FadeOut(p) for p in pulses], run_time=0.25)

        # Training loop: 4 epochs, restore everything between epochs, new dropout each time
        p = 0.3  # CHANGED TO 0.5
        epoch = 0  # START AT 0
        
        for ep in range(4):
            # Sample masks for hidden layers
            m1 = sample_mask(len(hidden_layer1), p)
            m2 = sample_mask(len(hidden_layer2), p)
            m3 = sample_mask(len(hidden_layer3), p)

            # First epoch only: show red rings where nodes will be dropped
            if ep == 0:
                rings = outline_dropped(hidden_layer1, m1) + outline_dropped(hidden_layer2, m2) + outline_dropped(hidden_layer3, m3)
                if rings:
                    self.play(*[ShowCreation(r) for r in rings],)
                    self.wait(2)
                    self.play(*[Uncreate(r) for r in rings], )
                self.wait()

            # Remove dropped nodes and edges BEFORE forward pass
            d1_nodes, d1_lines = remove_dropout(hidden_layer1, m1)
            d2_nodes, d2_lines = remove_dropout(hidden_layer2, m2)
            d3_nodes, d3_lines = remove_dropout(hidden_layer3, m3)

            # Forward pass: always #FF0000
            pulse_stage(input_layer,     hidden_layer1, FWD_COLOR, None, m1, run_time=0.7)
            pulse_stage(hidden_layer1,   hidden_layer2, FWD_COLOR, m1,   m2, run_time=0.7)
            pulse_stage(hidden_layer2,   hidden_layer3, FWD_COLOR, m2,   m3, run_time=0.7)
            pulse_stage(hidden_layer3,  [output_node], FWD_COLOR, m3,   [True], run_time=0.7)

            # Backprop: single color per epoch; color edges while pulses move
            bwd_color = BWD_EPOCH_COLORS[min(ep, len(BWD_EPOCH_COLORS)-1)]

            # output -> h3
            backprop_stage([output_node], hidden_layer3, conn_h3_out, [True], m3, bwd_color, run_time=0.6)
            # h3 -> h2
            backprop_stage(hidden_layer3, hidden_layer2, conn_h2_h3, m3, m2, bwd_color, run_time=0.6)
            # h2 -> h1
            backprop_stage(hidden_layer2, hidden_layer1, conn_h1_h2, m2, m1, bwd_color, run_time=0.6)
            # h1 -> input
            backprop_stage(hidden_layer1, input_layer,   conn_in_h1, m1, None, bwd_color, run_time=0.6)

            # MODIFIED: Update epoch and scale loss BEFORE restoring dropout nodes
            if ep < 3:  # Only update for the next 3 epochs
                epoch += 1
                self.play(
                    loss_group.animate.scale(0.62),
                    run_time=0.6
                )

            # End of epoch: recreate everything with original properties
            restore_dropout(hidden_layer3, d3_nodes, d3_lines)
            restore_dropout(hidden_layer2, d2_nodes, d2_lines)
            restore_dropout(hidden_layer1, d1_nodes, d1_lines)

        self.wait(0.6)

        
        # FINAL TRAINING VISUALIZATION: White pulses along ALL edges simultaneously
        final_pulses = []
        pulse_anims = []
        color_anims = []
        
        # Process ALL lines from all connection lists
        for ln in input_to_h1:
            start_pt = ln.get_start()
            end_pt = ln.get_end()
            p = create_pulse(start_pt, color=WHITE, radius=0.06)
            final_pulses.append(p)
            self.add(p)
            pulse_anims.append(p.animate.move_to(end_pt))
            color_anims.append(ln.animate.set_stroke(color=WHITE, width=2, opacity=0.9))
        
        for ln in h1_to_h2:
            start_pt = ln.get_start()
            end_pt = ln.get_end()
            p = create_pulse(start_pt, color=WHITE, radius=0.06)
            final_pulses.append(p)
            self.add(p)
            pulse_anims.append(p.animate.move_to(end_pt))
            color_anims.append(ln.animate.set_stroke(color=WHITE, width=2, opacity=0.9))
        
        for ln in h2_to_h3:
            start_pt = ln.get_start()
            end_pt = ln.get_end()
            p = create_pulse(start_pt, color=WHITE, radius=0.06)
            final_pulses.append(p)
            self.add(p)
            pulse_anims.append(p.animate.move_to(end_pt))
            color_anims.append(ln.animate.set_stroke(color=WHITE, width=2, opacity=0.9))
        
        for ln in h3_to_output:
            start_pt = ln.get_start()
            end_pt = ln.get_end()
            p = create_pulse(start_pt, color=WHITE, radius=0.06)
            final_pulses.append(p)
            self.add(p)
            pulse_anims.append(p.animate.move_to(end_pt))
            color_anims.append(ln.animate.set_stroke(color=WHITE, width=2, opacity=0.9))
        
        # Play all animations simultaneously
        if pulse_anims:
            self.play(*(pulse_anims + color_anims), run_time=1.2)
            self.play(*[FadeOut(p) for p in final_pulses], run_time=0.3)

        self.play(FadeOut(loss_group), FadeOut(p_text), run_time=0.8)
        self.camera.frame.save_state()

        self.play(self.camera.frame.animate.shift(LEFT*0.69+DOWN*0.65))
        
        self.wait(1.0)


        # Layer-specific dropout probability visualization
        self.wait(0.5)
        
        # Start with output layer (p=0)
        output_rect = SurroundingRectangle(
            output_node,
            color="#FF0000",
            fill_color="#FF0000",
            fill_opacity=0.4,
            stroke_width=4,
            buff=0.15
        )
        output_p_label = Text("p = 0", weight=BOLD).next_to(output_rect, DOWN, buff=0.5).scale(1.2)
        
        self.play(
            ShowCreation(output_rect),
            Write(output_p_label),
            run_time=0.8
        )
        self.wait(1.2)
        
        # Transform to hidden layer 3 (3 neurons, p=0.3)
        h3_group = VGroup(*hidden_layer3)
        h3_rect = SurroundingRectangle(
            h3_group,
            color="#FF0000",
            fill_color="#FF0000",
            fill_opacity=0.5,
            stroke_width=4,
            buff=0.2
        )
        h3_p_label = Text("p = 0.3", weight=BOLD).next_to(h3_rect, DOWN, buff=0.5).scale(1.2)
        
        self.play(
            Transform(output_rect, h3_rect),
            Transform(output_p_label, h3_p_label),
            run_time=0.9
        )
        self.wait(1.0)
        
        # Transform to hidden layer 2 (5 neurons, p=0.5)
        h2_group = VGroup(*hidden_layer2)
        h2_rect = SurroundingRectangle(
            h2_group,
            color="#FF0000",
            fill_color="#FF0000",
            fill_opacity=0.5,
            stroke_width=4,
            buff=0.2
        )
        h2_p_label = Text("p = 0.5", weight=BOLD).next_to(h2_rect, DOWN, buff=0.5).scale(1.2)
        
        self.play(
            Transform(output_rect, h2_rect),
            Transform(output_p_label, h2_p_label),
            run_time=0.9
        )
        self.wait(1.0)
        
        # Transform to hidden layer 1 (4 neurons, p=0.4)
        h1_group = VGroup(*hidden_layer1)
        h1_rect = SurroundingRectangle(
            h1_group,
            color="#FF0000",
            fill_color="#FF0000",
            fill_opacity=0.6,
            stroke_width=4,
            buff=0.2
        )
        h1_p_label = Text("p = 0.4", weight=BOLD).next_to(h1_rect, DOWN, buff=0.5).scale(1.2)

        self.play(
            Transform(output_rect, h1_rect),
            Transform(output_p_label, h1_p_label),
            run_time=0.9
        )
        self.wait(1.0)
        
        # Transform to input layer (5 neurons, p≈0.1)
        input_group = VGroup(*input_layer)
        input_rect = SurroundingRectangle(
            input_group,
            color="#FF0000",
            fill_color="#FF0000",
            fill_opacity=0.6,
            stroke_width=4,
            buff=0.2
        )
        input_p_label = Text("p ~ 0.1", weight=BOLD).next_to(input_rect, DOWN, buff=0.5).scale(1.2)
        
        self.play(
            Transform(output_rect, input_rect),
            Transform(output_p_label, input_p_label),
            run_time=0.9
        )
        self.wait(1.5)
        

        
        self.wait(1.0)
        

class OverfittingRegion(Scene):
    def construct(self):

        self.camera.frame.shift(DOWN * 0.63)

        # Create axes
        axes = Axes(
            x_range=[0, 50, 10],
            y_range=[0, 1, 0.2],
            width=10,
            height=6,
            axis_config={
                "include_tip": True,
                "include_numbers": False,
                "tick_size": 0,
                "stroke_width": 6,
            }
        ).shift(DOWN * 0.5)

        # Axis labels
        x_label = Text("Epochs", font_size=46, weight=BOLD).next_to(axes.x_axis, DOWN)
        y_label = Text("Loss", font_size=46, weight=BOLD).next_to(axes.y_axis, LEFT).rotate(90 * DEGREES)

        # Training and validation loss functions
        def training_loss(x):
            return 0.4 * np.exp(-0.08 * x) + 0.15

        def validation_loss(x):
            base_curve = 0.4 * np.exp(-0.08 * x) + 0.2
            if x > 20:
                upturn = 0.0003 * (x - 20) ** 1.8
            else:
                upturn = 0
            return base_curve + upturn

        # Graphs
        training_graph = axes.get_graph(training_loss, x_range=[0, 50], color=RED, stroke_width=6)
        validation_graph = axes.get_graph(validation_loss, x_range=[0, 50], color=BLUE, stroke_width=6)

        # Legend
        legend_box = Rectangle(width=3.5, height=1.2, fill_color=BLACK, fill_opacity=0.8,
                               stroke_color=WHITE, stroke_width=2).to_corner(UR, buff=0.5).shift(LEFT * 0.45 + DOWN * 1.2)
        training_line = Line(LEFT * 0.5, RIGHT * 0.5, color=RED, stroke_width=6)
        validation_line = Line(LEFT * 0.5, RIGHT * 0.5, color=BLUE, stroke_width=6)
        training_line.move_to(legend_box.get_center() + UP * 0.3 + LEFT * 1.2)
        validation_line.move_to(legend_box.get_center() + DOWN * 0.3 + LEFT * 1.2)
        training_text = Text("Training", font_size=24, color=WHITE).next_to(training_line, RIGHT, buff=0.2)
        validation_text = Text("Validation", font_size=24, color=WHITE).next_to(validation_line, RIGHT, buff=0.2)
        legend_group = VGroup(legend_box, training_line, training_text, validation_line, validation_text)

        legend_box.shift(LEFT*0.3)

        # Animate axes + labels
        self.play(FadeIn(axes), Write(x_label), Write(y_label), run_time=1.5)
        self.wait(0.5)
        self.play(FadeIn(legend_group), run_time=1)

        # Draw curves
        self.play(ShowCreation(training_graph), ShowCreation(validation_graph), run_time=3)
        self.wait(1)

        # Moving dots
        training_dot = Dot(color=RED, radius=0.13).set_color("#20FF33")
        validation_dot = Dot(color=BLUE, radius=0.13).set_color("#20FF33")
        training_dot.move_to(axes.c2p(0, training_loss(0)))
        validation_dot.move_to(axes.c2p(0, validation_loss(0)))
        epoch_tracker = ValueTracker(0)

        # Updaters
        training_dot.add_updater(lambda m: m.move_to(
            axes.c2p(epoch_tracker.get_value(), training_loss(epoch_tracker.get_value()))
        ))
        validation_dot.add_updater(lambda m: m.move_to(
            axes.c2p(epoch_tracker.get_value(), validation_loss(epoch_tracker.get_value()))
        ))

        self.play(FadeIn(training_dot), FadeIn(validation_dot), run_time=0.5)

        # Animate until overfitting begins
        self.play(epoch_tracker.animate.set_value(20), run_time=3, rate_func=linear)
        self.wait(0.8)

        # Continue to show overfitting phase
        self.play(epoch_tracker.animate.set_value(45), run_time=2, rate_func=linear)
        self.wait(0.5)

        # Stop updating
        training_dot.clear_updaters()
        validation_dot.clear_updaters()

        # 🌟 Highlight "Overfitting Region" (shorter height)
        # Compute original y coordinates for top and bottom of region
        x_start = axes.c2p(27, 0)[0]
        x_end = axes.c2p(50, 0)[0]
        y_bottom = axes.c2p(0, 0.2)[1]   # Start slightly above x-axis
        y_top = axes.c2p(0, 0.7)[1]      # Reduced height (half the plot)

        overfit_region = Polygon(
            [x_start, y_bottom, 0],
            [x_start, y_top, 0],
            [x_end, y_top, 0],
            [x_end, y_bottom, 0],
            fill_color=YELLOW,
            fill_opacity=0.15,
            stroke_width=0
        ).shift(DOWN)

        overfit_label = Text("Overfitting Region", font_size=46, color=YELLOW)
        overfit_label.next_to(axes.c2p(35, 0.7), UP, buff=0.1).shift(DOWN+RIGHT*0.7)

        # Animate shaded region and label
        self.play(FadeIn(overfit_region, run_time=1.5), Write(overfit_label, run_time=1.5))
        self.wait(3)
