from manimlib import *
import numpy as np

DARK_GRAY = GREY_E
DARK_GREEN = GREEN_E
BROWN = "#824203"


DARK_BLUE = BLUE_E

class BiasVarianceTradeoff(Scene):
    def construct(self):

        # Set white background
        self.camera.frame.scale(0.87).shift(UP*0.5)
        
        # Create the pivot (triangle support)
        pivot = Polygon(
            [-0.5, -1, 0], [0.5, -1, 0], [0, 0.5, 0],
            fill_color=GREY_C,
            fill_opacity=1.0,
            stroke_color=GREY_D,
            stroke_width=3
        )
        
        # Create the see-saw bench (horizontal rectangle)
        bench = Rectangle(
            width=8.0,
            height=0.3,
            fill_color=PURPLE,
            fill_opacity=1.0,
            stroke_color=PURPLE_B,
            stroke_width=3
        )
        bench.move_to([0, 0.65,0])  # Place on top of triangle
        
        # Create rounded squares for Bias and Variance
        bias_square = RoundedRectangle(
            width=1.2,
            height=1.2,
            corner_radius=0.2,
            fill_color=GREEN_B,
            fill_opacity=1.0,
            stroke_color=GREEN,
            stroke_opacity=7,
            stroke_width=10
        )
        
        variance_square = RoundedRectangle(
            width=1.2,
            height=1.2,
            corner_radius=0.2,
            fill_color=MAROON_B,
            fill_opacity=1.0,
            stroke_color=MAROON,
            stroke_opacity=1,
            stroke_width=10
        )
        
        # Create text labels for the squares
        bias_text = Text("B", font_size=88, font="Arial Bold", weight=BOLD)
        bias_text.set_color(BLACK)
        variance_text = Text("V", font_size=88, font="Arial Bold", weight=BOLD)
        variance_text.set_color(BLACK)
        
        # Position squares on the ends of the bench (on top of bench)
        bias_square.move_to([-3.34, 1.44,0])
        variance_square.move_to([3.34, 1.44, 0])
        
        # Position text inside squares
        bias_text.move_to(bias_square.get_center())
        variance_text.move_to(variance_square.get_center())
        
        # Create additional labels
        underfitting_label = Text("Underfitting", font_size=54 , weight=BOLD)
        underfitting_label.set_color(GREEN)
        overfitting_label = Text("Overfitting", font_size=54 , weight=BOLD)
        overfitting_label.set_color(MAROON)
        balanced_label = Text("Optimal Balance", font_size=58, weight= BOLD)
        balanced_label.set_color(BLUE)
        
        # Position labels
        underfitting_label.move_to([-3.5, -1, 0])
        overfitting_label.move_to([3.5, -1, 0])
        balanced_label.move_to([0, -2, 0])
        
        # Group elements that will rotate together
        seesaw_group = VGroup(bench, bias_square, variance_square, bias_text, variance_text)
        

        
        # Add all elements to scene
        self.add(pivot)
        self.play(FadeIn(seesaw_group))
        self.wait(1)
        
        # Function to tilt toward bias (left side down)
        def tilt_to_bias():
            self.play(
                Rotate(seesaw_group, angle=-PI/6, about_point=[0, 0.5, 0]),
                FadeIn(underfitting_label),
                run_time=2
            )
            self.wait(2)
            self.play(FadeOut(underfitting_label))
        # Function to tilt toward variance (right side down)
        def tilt_to_variance():
            self.play(
                Rotate(seesaw_group, angle=PI/3, about_point=[0, 0.5, 0]),
                FadeIn(overfitting_label),
                run_time=2
            )
            self.wait(2)
            self.play(FadeOut(overfitting_label))
        # Function to balance in the middle
        def balance_seesaw():
            self.play(
                Rotate(seesaw_group, angle=-PI/6, about_point=[0, 0.5, 0]),
                FadeIn(balanced_label),
                run_time=2
            )
            self.wait(2)
        
        # Execute the animation sequence
        
        # 1. Tilt toward bias (underfitting)
        tilt_to_bias()
        

        # 2. Tilt toward variance (overfitting)
        tilt_to_variance()
        
        # 3. Balance in the middle (optimal tradeoff)
        balance_seesaw()
        
        self.wait(2)


class Validation(Scene):
    def construct(self):
        self.camera.frame.scale(1.17).shift(UP*0.17) # Zoom out

        # Axes
        axes = Axes(
            x_range=[0, 12],
            y_range=[0, 6],
            axis_config={"include_ticks": False, "include_numbers": False, "stroke_width": 8},
        )
        axes.set_color(BLACK)

        x_label = Text("x", weight=BOLD).next_to(axes.x_axis, DOWN).shift(RIGHT * 6 + DOWN * 0.4).scale(1.77).set_color(BLACK)
        y_label = Text("y", weight=BOLD).next_to(axes.y_axis, UP).shift(UP * 0.1).scale(1.7).set_color(BLACK)

        self.play(ShowCreation(axes))
        self.play(Write(x_label), Write(y_label))
        self.wait(1)

        # ----- Dataset with squeezed y-range and scattered points -----
        x_values = np.array([1.5, 2.5, 3.2, 4.0, 4.8, 5.5, 6.3, 7.0, 7.8, 8.5, 9.2, 10.0, 10.5, 11.0, 11.5])
        y_values = np.array([2.2, 3.7, 2.0, 3.4, 3.8, 2.1, 3.3, 3.9, 2.3, 3.5, 2.4, 3.6, 3.2, 2.0, 3.7])

        # Verify lengths
        assert len(x_values) == len(y_values), "x_values and y_values must have the same length"
        
        dots = VGroup(*[
            Dot(axes.coords_to_point(x, y), radius=0.18).set_color(GREY_C)
            for x, y in zip(x_values, y_values)
        ])

        # Verify dots creation
        assert len(dots) == len(x_values), f"Expected {len(x_values)} dots, but got {len(dots)}"

        self.play(LaggedStart(*[ShowCreation(d) for d in dots], lag_ratio=0.05), run_time=2)
        self.wait(1)

        # Split with 60/40 split
        total_points = len(x_values)
        train_count = int(0.6 * total_points)  # 60% training, 40% validation
        all_indices = list(range(total_points))
        np.random.seed(42)  # Set seed for reproducibility
        np.random.shuffle(all_indices)
        
        # Verify indices
        assert max(all_indices) < total_points, f"Indices out of range: {all_indices}"
        
        train_idx = all_indices[:train_count]
        val_idx = all_indices[train_count:]

        # Verify index lengths
        assert len(train_idx) + len(val_idx) == total_points, "Train and validation indices don't cover all points"
        assert max(train_idx) < len(dots), f"Train index out of range: {max(train_idx)}"
        assert max(val_idx) < len(dots), f"Validation index out of range: {max(val_idx)}"

        train_dots = [dots[i] for i in train_idx]
        val_dots = [dots[i] for i in val_idx]

        self.play(*[dot.animate.set_color(GREEN) for dot in train_dots])
        self.play(*[dot.animate.set_color(BLUE) for dot in val_dots])
        self.wait(1)

        self.wait(2)

        # Curve fitting setup
        curve_x = np.linspace(1.5, 11.5, 200)

        def create_curve(fit_y, color=DARK_BLUE, stroke_width=10):
            curve_points = [
                axes.coords_to_point(curve_x[i], fit_y[i])
                for i in range(len(curve_x))
            ]
            curve = VMobject()
            curve.set_color(color)
            curve.set_stroke(width=stroke_width)
            curve.set_points_smoothly(curve_points)
            return curve

        # UNDERFITTING
        self.play(FadeOut(VGroup(*val_dots)), run_time=1.5)
        iteration1_fit_y = np.full_like(curve_x, 3.0)
        current_curve = create_curve(iteration1_fit_y)
        self.play(ShowCreation(current_curve), run_time=1)

        iteration2_fit_y = 2.5 + 0.1 * (curve_x - 6)
        new_curve2 = create_curve(iteration2_fit_y)
        self.play(Transform(current_curve, new_curve2), run_time=0.5)

        iteration3_fit_y = 3.0 + 0.05 * (curve_x - 6)**2
        new_curve3 = create_curve(iteration3_fit_y)
        self.play(Transform(current_curve, new_curve3), run_time=0.5)

        self.play(FadeOut(VGroup(*train_dots)), FadeIn(VGroup(*val_dots)), run_time=1.5)
        underfitting_text = Text("UNDERFITTING", weight=BOLD).scale(1.3).set_color(RED)
        underfitting_text.move_to(UP * 3.5)  # Fixed position
        self.play(ShowCreation(underfitting_text), run_time=1)
        self.wait(3)

        self.play(FadeOut(underfitting_text), FadeOut(VGroup(*val_dots)), FadeIn(VGroup(*train_dots)), run_time=1.5)

        # OVERFITTING polynomial curve
        train_x = x_values[train_idx]
        train_y = y_values[train_idx]
        degree = len(train_x) - 1
        coeffs = np.polyfit(train_x, train_y, deg=degree)
        overfit_y = np.polyval(coeffs, curve_x)
        overfit_y = np.clip(overfit_y, 1.0, 5.5)
        overfit_curve = create_curve(overfit_y)
        self.play(Transform(current_curve, overfit_curve), run_time=1.5)

        self.play(FadeOut(VGroup(*train_dots)), FadeIn(VGroup(*val_dots)), run_time=1.5)
        overfitting_text = Text("OVERFITTING", weight=BOLD).scale(1.3).set_color(RED)
        overfitting_text.move_to(UP * 3.5)  # Fixed position
        self.play(ShowCreation(overfitting_text), run_time=1)
        self.wait(3)

        self.play(FadeOut(overfitting_text), FadeOut(VGroup(*val_dots)), FadeIn(VGroup(*train_dots)), run_time=1.5)

        # JUST RIGHT


        # JUST RIGHT
        goldilocks_y = (
            3.0
            + 0.3 * np.sin(0.5 * curve_x + 0.2)
            + 0.2 * np.sin(1.2 * curve_x)
            + 0.15 * np.sin(0.8 * curve_x + 1.0)
            + 0.12 * np.sin(0.35 * curve_x - 0.3)
            + 0.08 * np.sin(1.5 * curve_x + 0.5)
            - 0.05 * (curve_x - 6.5)**2
            + 0.1 * (curve_x - 6.5)
        )


        goldilocks_curve = create_curve(goldilocks_y).shift(UP*0.234)
        self.play(Transform(current_curve, goldilocks_curve), run_time=1.5)


        self.play(FadeOut(VGroup(*train_dots)), FadeIn(VGroup(*val_dots)), run_time=1.5)
        goldilocks_text = Text("JUST RIGHT", weight=BOLD).scale(1.3).set_color(GREEN)
        goldilocks_text.move_to(UP * 3.5)  # Fixed position
        self.play(ShowCreation(goldilocks_text), run_time=1)
        self.wait(3)

        self.play(FadeOut(VGroup(*val_dots, current_curve, axes, x_label, y_label, goldilocks_text)), run_time=0.5)

        over = Text("High Training Error + High Validation Error", weight=BOLD).to_edge(UP).set_color(BLACK).scale(0.8).shift(DOWN*0.4)
        self.play(ShowCreation(over))
        self.wait(2)
        temp = Text("Underfitting", weight=BOLD).set_color(RED).scale(1.44).next_to(over, DOWN, buff=0.9)
        self.play(ShowCreation(temp))

        self.wait(2)

        under = Text("Low Training Error + High Validation Error", weight=BOLD).next_to(temp, DOWN, buff=1.1).set_color(BLACK).scale(0.8)
        self.play(ShowCreation(under))
        self.wait(2)
        temp1 = Text("OverFitting", weight=BOLD).set_color(RED).scale(1.44).next_to(under, DOWN, buff=0.9)
        self.play(ShowCreation(temp1))
        self.wait(2)

        self.play(FadeOut(VGroup(temp, temp1, over, under)), run_time=0.5)

        first = Text("Validation", weight=BOLD).set_color(BLUE).scale(1.44).next_to(over, DOWN, buff=0.9).shift(UP*1.83)
        self.play(ShowCreation(first))

        temp = Text("Tune Hyperparameters", weight=BOLD).next_to(first, DOWN).set_color(GREEN).shift(DOWN*0.25)
        self.play(ShowCreation(temp))

            # List of hyperparameters as bullet points
        bullets = [
            "• Learning rate",
            "• Number of neurons",
            "• Regularization strength",
            "• Batch size",
            "• Number of epochs",
        ]

        # Create Text objects for each bullet
        bullet_texts = VGroup(*[
            Text(item, weight=BOLD).next_to(temp, DOWN, buff=0.5 + i * 0.5).set_color(BLACK).shift(LEFT*0.8)
            for i, item in enumerate(bullets)
        ])



        # Adjust positions
        for i in range(len(bullet_texts)):
            if i == 0:
                bullet_texts[i].next_to(temp, DOWN, buff=0.7)
            else:
                bullet_texts[i].next_to(bullet_texts[i-1], DOWN, aligned_edge=LEFT)

        # Animate
        for bt in bullet_texts:
            bt.shift(LEFT*0.8)
            self.play(FadeIn(bt), run_time=0.5)
        self.wait(2)

        self.play(FadeOut(VGroup(bullet_texts, temp, first)), run_time=0.5)

        training = Text("Training Data", weight=BOLD).to_edge(UP).set_color(GREEN).scale(1.3).shift(UP*0.4)
        self.play(ShowCreation(training))
        self.wait()
        temp = Text("Training (Updating weights)", weight=BOLD).next_to(training, DOWN, buff=0.55).set_color(BLACK)
        self.play(ShowCreation(temp))

        self.wait(2)

        val = Text("Validation Data", weight=BOLD).to_edge(UP).set_color(BLUE).scale(1.3).next_to(temp, DOWN, buff=0.9)
        self.play(ShowCreation(val))
        self.wait()
        temp1 = Text("Tuning Hyperparameters", weight=BOLD).next_to(val, DOWN, buff=0.55).set_color(BLACK)
        self.play(ShowCreation(temp1))
        self.wait(2)

        test = Text("Testing Data", weight=BOLD).to_edge(UP).set_color(RED).scale(1.3).next_to(temp1, DOWN, buff=0.9)
        self.play(ShowCreation(test))
        self.wait()
        temp2 = Text("Final testing", weight=BOLD).next_to(test, DOWN, buff=0.55).set_color(BLACK)
        self.play(ShowCreation(temp2))

        self.wait(2)
        self.play(FadeOut(VGroup(temp, temp1, temp2, test, training,val )),self.camera.frame.animate.scale(0.93).shift(DOWN*0.23), run_time=0.5)

        #LifeCYcle
        


        # 1. Dataset (bullet)
        dataset = Text("• Dataset", weight=BOLD).scale(0.6).to_edge(UP).set_color(BLACK)
        self.play(Write(dataset))
        self.wait(0.5)

        # 2. Splitting (one text with nested bullets)
        splitting_text = "• Splitting\n   - Training\n   - Validation\n   - Test"
        splitting = Text(splitting_text, weight=BOLD).scale(0.5).next_to(dataset, DOWN, buff=0.6).set_color(BLACK)
        splitting[10:19].set_color(GREEN)
        splitting[19:30].set_color(BLUE)
        splitting[30:40].set_color(RED)
        self.play(Write(splitting))
        self.wait(0.5)



        # 3. Training
        training = Text("• Training (weights updating)", weight=BOLD).scale(0.6).next_to(splitting, DOWN, buff=0.8).set_color(BLACK)
        training[:9].set_color(GREEN)

        # Arrow from splitting to training
        arrow_train = Arrow(splitting.get_bottom(), training.get_top(), buff=0.1)
        arrow_train.set_color(BLACK)
        self.play(GrowArrow(arrow_train))
        self.wait(0.5)

        self.play(Write(training))
        self.wait(0.5)


        # 4. Validation
        validation_text = "• Validation\n   - Error checking"
        validation = Text(validation_text, weight=BOLD).scale(0.5).next_to(training, DOWN, buff=0.8)
        validation.set_color(BLACK)
        # Arrow from training to validation
        arrow_val = Arrow(training.get_bottom(), validation.get_top(), buff=0.1)
        arrow_val.set_color(BLACK)
        self.play(GrowArrow(arrow_val))
        self.play(Write(validation))
        self.wait(0.5)



        # 5. Tune hyperparameters
        tune = Text("• Tune hyperparameters", weight=BOLD).scale(0.6).next_to(validation, DOWN, buff=0.8)
        tune.set_color(BLACK)
        # Arrow from training to validation
        arrow_next = Arrow(validation.get_bottom(), tune.get_top(), buff=0.1)
        arrow_next.set_color(BLACK)
        self.play(GrowArrow(arrow_val))
        self.play(Write(tune))
        self.wait(0.5)

        # Curved arrow looping back to training
        loop_arrow = CurvedArrow(tune.get_left(), training.get_left(), angle=-TAU / 3, stroke_width=6)
        loop_arrow.set_color(BLUE).shift(LEFT*0.1)
        self.play(ShowCreation(loop_arrow))
        self.wait(0.5)

        # 6. Final test
        final_test = Text("• Final test on test set", weight=BOLD).scale(0.6).next_to(tune, DOWN, buff=0.8)
        final_test.set_color(BLACK)
        self.play(Write(final_test))
        self.wait(0.5)

        # Arrow from training to final test
        arrow_test = CurvedArrow(training.get_right(), final_test.get_right(), angle=-TAU / 3 ,stroke_width=8).set_color(RED).shift(RIGHT*0.1)
        self.play(ShowCreation(arrow_test))
        self.wait(2)

        self.wait(2)

class TrainingDemo(Scene):
    def construct(self):
        self.camera.frame.scale(1.4)  # Zoom out
        
        # Axes
        axes = Axes(
            x_range=[0, 15],
            y_range=[0, 8],
            axis_config={"include_ticks": False, "include_numbers": False, "stroke_width": 8},
        )
        axes.set_color(BLACK)
        
        x_label = Text("x", weight=BOLD).next_to(axes.x_axis, DOWN).shift(RIGHT * 7.6 + DOWN * 0.4).scale(1.77)
        x_label.set_color(BLACK)
        
        y_label = Text("y", weight=BOLD).next_to(axes.y_axis, UP).shift(UP * 0.1).scale(1.7)
        y_label.set_color(BLACK)
        
        self.play(ShowCreation(axes))
        self.play(Write(x_label), Write(y_label))
        self.wait(1)
        
        # Create fewer but more spaced points
        np.random.seed(10)
        x_values = np.array([
            # Well-spaced points across the range
            1.5, 3.8, 4.2, 5.6, 7.0, 8.4, 9.8, 11.2, 12.6, 14.0,
            2.0, 3.5, 5.0, 6.5, 8.0, 9.5, 11.0, 12.5, 13.8,
            1.8, 3.2, 4.8, 6.2, 7.5, 9.0, 10.5, 12.0, 13.5,
            2.5, 4.0, 5.5, 7.2, 8.8, 10.2, 11.8, 13.2
        ])  # 35 points total - fewer but well distributed
        
        # Create a rough sinusoidal pattern with more variation and noise
        # Base pattern with multiple frequency components and random variations
        # RAISED Y-VALUES BY 0.5 as requested
        y_base = 1.13 * np.sin(0.2 * x_values) + 0.8 * np.sin(1.2 * x_values) + 2.7  # Changed from 2.2 to 2.7
        y_values = y_base + np.random.normal(0, 0.5, size=len(x_values))  # More noise for roughness
        
        # Add some random outliers to make it less strictly sinusoidal
        outlier_indices = [3, 8, 15, 22, 28]
        for idx in outlier_indices:
            if idx < len(y_values):
                y_values[idx] += np.random.normal(0, 0.8)
        
        # Keep y values within bounds - adjusted for higher range
        y_values = np.clip(y_values, 1.0, 5.7)  # Raised from (0.5, 5.2) to (1.0, 5.7)
        
        dots = VGroup(*[
            Dot(axes.coords_to_point(x_values[i], y_values[i]), radius=0.20*1.23).set_color(GREY_C)
            for i in range(len(x_values))
        ])
        
        # Fade in all points initially as GREY
        self.play(LaggedStart(*[ShowCreation(dot) for dot in dots], lag_ratio=0.05), run_time=2)
        self.wait(1)
        
        # Define indices for splits - 6:2:2 ratio with strategic distribution
        # Train: 60% (21 points), Val: 20% (7 points), Test: 20% (7 points)
        total_points = len(x_values)
        train_count = int(0.6 * total_points)  # 21 points
        val_count = int(0.2 * total_points)    # 7 points
        test_count = total_points - train_count - val_count  # 7 points
        
        # Strategic distribution instead of random
        # Sort points by x-value for better distribution
        sorted_indices = np.argsort(x_values)
        
        # Distribute validation and test points evenly across x-range
        train_idx = []
        val_idx = []
        test_idx = []
        
        # Take every 5th point for validation, every 5th+1 for test, rest for training
        for i, idx in enumerate(sorted_indices):
            if i % 5 == 0 and len(val_idx) < val_count:
                val_idx.append(idx)
            elif i % 5 == 1 and len(test_idx) < test_count:
                test_idx.append(idx)
            else:
                train_idx.append(idx)
        
        # Fill remaining slots with training data
        remaining_indices = [idx for idx in sorted_indices if idx not in val_idx + test_idx]
        train_idx.extend(remaining_indices[:train_count - len(train_idx)])
        
        # Sort indices for cleaner visualization
        train_idx.sort()
        val_idx.sort()
        test_idx.sort()
        
        # Animate color changes
        train_dots = [dots[i] for i in train_idx]
        val_dots = [dots[i] for i in val_idx]
        test_dots = [dots[i] for i in test_idx]
        
        self.play(*[dot.animate.set_color(GREEN) for dot in train_dots])
        self.play(*[dot.animate.set_color(BLUE) for dot in val_dots])
        self.play(*[dot.animate.set_color(RED) for dot in test_dots])
        self.wait(1)

        # Create labels for data types
        training_label = Text("Training", weight=BOLD).scale(1).set_color(GREEN)
        validation_label = Text("Validation", weight=BOLD, color=BLUE).scale(1).set_color(BLUE)
        testing_label = Text("Testing", weight=BOLD, color=RED).scale(1).set_color(RED)
        
        # Stack them vertically at the top of the screen
        labels = VGroup(training_label, validation_label, testing_label).arrange(RIGHT, buff=0.7).scale(1.2)
        labels.to_corner(UL).shift(RIGHT*0.3 + UP * 1)
        
        # Show the labels
        self.play(ShowCreation(labels))
        self.wait(2)
        
        # Fade out validation and test points - only keep training
        self.play(FadeOut(VGroup(*val_dots)), FadeOut(VGroup(*test_dots)), FadeOut(labels), run_time=1.5)
        
        # Create curve fitting iterations
        curve_x = np.linspace(1.5, 15, 200)  # Extended range to cover new points
        
        def create_curve(fit_y, color=DARK_BLUE, stroke_width=10):
            curve_points = [
                axes.coords_to_point(curve_x[i], fit_y[i])
                for i in range(len(curve_x))
            ]
            curve = VMobject()
            curve.set_color(color)
            curve.set_stroke(width=stroke_width)
            curve.set_points_smoothly(curve_points)
            return curve
        
        # FIRST TRAINING PASS - 3 iterations (Poor fitting)
        training_label_solo = Text("Training", weight=BOLD, color=GREEN).scale(1.5).set_color(GREEN).shift(RIGHT*0.8+UP*4)
        self.play(FadeIn(training_label_solo))

        
        # Iteration 1: Completely wrong - flat line
        iteration1_fit_y = np.full_like(curve_x, 3.0)  # Flat line, clearly not fitting
        current_curve = create_curve(iteration1_fit_y, DARK_BLUE, 10)
        self.play(ShowCreation(current_curve), run_time=1)
        self.wait(0.5)
        
        # Iteration 2: Wrong slope - linear trend
        iteration2_fit_y = 2.0 + 0.15 * (curve_x - 7.5)  # Linear, still not fitting the pattern
        new_curve2 = create_curve(iteration2_fit_y, DARK_BLUE, 10)
        self.play(Transform(current_curve, new_curve2), run_time=0.5)
        self.wait(0.5)
        
        # Iteration 3: Wrong frequency - very basic wave
        iteration3_fit_y = 2.7 + 0.5 * np.sin(0.15 * curve_x)  # Wrong frequency, clearly not fitting
        new_curve3 = create_curve(iteration3_fit_y, DARK_BLUE, 10)
        self.play(Transform(current_curve, new_curve3), run_time=0.5)
        self.wait(0.5)
        
        # Check validation - should show poor performance
        validation_label_solo = Text("Validation", weight=BOLD, color=BLUE).scale(1.5).set_color(BLUE).move_to(training_label_solo)
        
        self.play(
            FadeOut(VGroup(*train_dots)), 
            FadeOut(training_label_solo),
            FadeIn(VGroup(*val_dots)), 
            FadeIn(validation_label_solo), 
            run_time=1.5
        )
        self.wait(2)  # Wait 2 seconds to see poor validation performance
        
        # SECOND TRAINING PASS - 3 iterations (Better fitting)
        self.play(
            FadeOut(VGroup(*val_dots)), 
            FadeOut(validation_label_solo),
            FadeIn(VGroup(*train_dots)),
            FadeIn(training_label_solo),
            run_time=1
        )
        
        # Iteration 4: Better frequency but wrong amplitude
        iteration4_fit_y = 2.7 + 0.8 * np.sin(0.4 * curve_x)  # Getting closer to correct frequency
        new_curve4 = create_curve(iteration4_fit_y, DARK_BLUE, 10)
        self.play(Transform(current_curve, new_curve4), run_time=0.5)
        self.wait(0.5)
        
        # Iteration 5: Closer to right pattern
        iteration5_fit_y = 2.7 + 1.0 * np.sin(0.5 * curve_x) + 0.3 * np.sin(1.0 * curve_x)  # Multi-frequency, getting better
        new_curve5 = create_curve(iteration5_fit_y, DARK_BLUE, 10)
        self.play(Transform(current_curve, new_curve5), run_time=0.5)
        self.wait(0.5)
        
        # Iteration 6: Much better fit
        iteration6_fit_y = 2.7 + 1.1 * np.sin(0.2 * curve_x) + 0.6 * np.sin(1.1 * curve_x)  # Much closer to data
        new_curve6 = create_curve(iteration6_fit_y, DARK_BLUE, 10)
        self.play(Transform(current_curve, new_curve6), run_time=0.5)
        self.wait(0.5)
        
        # Check validation again - should show better performance
        self.play(
            FadeOut(VGroup(*train_dots)),
            FadeOut(training_label_solo),
            FadeIn(VGroup(*val_dots)), 
            FadeIn(validation_label_solo), 
            run_time=1.5
        )
        self.wait(2)  # Wait 2 seconds to see improved validation performance
        
        # THIRD TRAINING PASS - 3 iterations (Good fitting without overfitting)
        self.play(
            FadeOut(VGroup(*val_dots)), 
            FadeOut(validation_label_solo),
            FadeIn(VGroup(*train_dots)),
            FadeIn(training_label_solo),
            run_time=1
        )
        
        # Iteration 7: Fine-tuning amplitude
        iteration7_fit_y = 2.7 + 1.13 * np.sin(0.2 * curve_x) + 0.75 * np.sin(1.15 * curve_x)  # Fine-tuning
        new_curve7 = create_curve(iteration7_fit_y, DARK_BLUE, 10)
        self.play(Transform(current_curve, new_curve7), run_time=0.5)
        self.wait(0.5)
        
        # Iteration 8: Almost perfect fit
        iteration8_fit_y = 2.7 + 1.13 * np.sin(0.2 * curve_x) + 0.8 * np.sin(1.2 * curve_x) + 0.15 * np.sin(1.8 * curve_x)  # Very close to actual pattern
        new_curve8 = create_curve(iteration8_fit_y, DARK_BLUE, 10)
        self.play(Transform(current_curve, new_curve8), run_time=0.5)
        self.wait(0.5)
        
        # Iteration 9: Final good fit (better fitting but not overfitted)
        final_fit_y = 2.7 + 1.13 * np.sin(0.2 * curve_x) + 0.8 * np.sin(1.2 * curve_x) + 0.2 * np.sin(1.5 * curve_x)  # Better fit for test data
        final_curve = create_curve(final_fit_y, DARK_BLUE, 10)
        self.play(Transform(current_curve, final_curve), run_time=0.5)
        self.wait(1)
        
        # Fade out training data only
        self.play(FadeOut(VGroup(*train_dots)), FadeOut(training_label_solo), run_time=1.5)
        self.wait(1)
        
        # Final testing phase
        testing_label_solo = Text("Testing", weight=BOLD, color=RED).scale(1.5).set_color(RED).move_to(training_label_solo)
        
        self.play(FadeIn(VGroup(*test_dots)), FadeIn(testing_label_solo), run_time=1.5)
        self.wait(3)  # Give time to observe how well the model performs on test data


class DataSplitAnimation(Scene):
    def construct(self):
        # Set white background 
        self.camera.frame.scale(0.8)
        
        # Initial proportions
        initial_props = [0.7, 0.15, 0.15]  # 70%, 15%, 15%
        final_props = [0.6, 0.2, 0.2]     # 60%, 20%, 20%
        
        # Colors for each section
        colors = [GREEN, BLUE, RED]
        initial_values = [70, 15, 15]
        final_values = [60, 20, 20]
        
        # Bar configuration
        bar_width = 8
        bar_height = 1
        bar_position = UP * 0.4
        
        # Create the initial data split bar
        bar_group = self.create_data_split_bar(
            proportions=initial_props,
            colors=colors,
            values=initial_values,
            bar_width=bar_width,
            bar_height=bar_height,
            position=bar_position
        )
        
        # Add to scene
        self.add(bar_group)
        self.wait(1)
        
        # Create final bar configuration (for shapes and braces only)
        final_bar_group = self.create_data_split_bar(
            proportions=final_props,
            colors=colors,
            values=final_values,
            bar_width=bar_width,
            bar_height=bar_height,
            position=bar_position
        )
        
        # Animate transition with simultaneous countdown
        self.animate_with_countdown(
            bar_group, 
            final_bar_group, 
            initial_values, 
            final_values,
            duration=2.0
        )
        
        self.wait(2)

        self.play(self.camera.frame.animate.shift(UP*1.15))

        train = Text("Train: 60% to 80%", weight=BOLD).set_color(BLACK).to_edge(UP).shift(UP*0.24)
        train[:5].set_color(GREEN)
        val = Text("Val: 10% to 20%", weight=BOLD).set_color(BLACK).next_to(train, DOWN, buff=0.45)
        val[:3].set_color(BLUE)
        test = Text("Test: 10% to 20%", weight=BOLD).set_color(BLACK).next_to(val, DOWN, buff=0.45)
        test[:4].set_color(RED)

        self.play(ShowCreation(VGroup(train, val , test)))

        self.wait(2)
        




        self.embed()
    
    def animate_with_countdown(self, initial_group, final_group, initial_vals, final_vals, duration):
        """Animate shapes with Transform and numbers with countdown simultaneously"""
        
        # Get the sections, braces, and texts separately
        initial_sections = initial_group[:3]  # First 3 elements are sections
        initial_braces = initial_group[3:6]   # Next 3 elements are braces
        initial_texts = initial_group[6:9]    # Last 3 elements are texts
        
        final_sections = final_group[:3]
        final_braces = final_group[3:6]
        final_texts = final_group[6:9]
        
        # Store initial and final proportions for interpolation
        initial_props = [0.7, 0.15, 0.15]
        final_props = [0.6, 0.2, 0.2]
        
        # Manual animation with frame-by-frame updates
        frame_rate = 15  # Updates per second
        total_frames = int(duration * frame_rate)
        
        for frame in range(total_frames + 1):
            t = frame / total_frames
            eased_t = self.smooth_ease(t)
            
            # Calculate current proportions
            current_props = []
            for i in range(3):
                start_prop = initial_props[i]
                end_prop = final_props[i]
                current_prop = start_prop + (end_prop - start_prop) * eased_t
                current_props.append(current_prop)
            
            # Create new sections with current proportions
            bar_width = 8
            bar_height = 1
            bar_position = UP * 0.4
            colors = [GREEN, BLUE, RED]
            
            section_widths = [prop * bar_width for prop in current_props]
            current_x = -bar_width / 2
            
            for i in range(3):
                # Create new section with current width
                width = section_widths[i]
                new_section = Rectangle(width=width, height=bar_height)
                new_section.set_color(colors[i])
                new_section.set_fill(colors[i], opacity=1)
                new_section.set_stroke(BLACK, width=1)
                new_section.move_to(bar_position + RIGHT * (current_x + width / 2))
                
                # Update the section
                initial_sections[i].become(new_section)
                
                # Update brace to match new section
                new_brace = Brace(initial_sections[i], DOWN)
                new_brace.set_color(BLACK)
                initial_braces[i].become(new_brace)
                
                current_x += width
            
            # Calculate and update text values
            current_vals = []
            for i in range(3):
                start_val = initial_vals[i]
                end_val = final_vals[i]
                current_val = int(start_val + (end_val - start_val) * eased_t)
                current_vals.append(current_val)
            
            # Update text objects and position them in middle of braces
            for i, text_obj in enumerate(initial_texts):
                new_text = Text(f"{current_vals[i]}%", font_size=36, weight=BOLD)
                new_text.set_color(BLACK)
                new_text.next_to(initial_braces[i], DOWN, buff=0.1)
                text_obj.become(new_text)
            
            # Wait for next frame
            if frame < total_frames:
                self.wait(1 / frame_rate)
    
    def smooth_ease(self, t):
        """Smooth easing function for more natural countdown"""
        return t * t * (3 - 2 * t)  # Smoothstep function
    
    def create_data_split_bar(self, proportions, colors, values, bar_width, bar_height, position):
        """Create a data split bar with sections, braces, and labels"""
        group = VGroup()
        
        # Calculate section widths
        section_widths = [prop * bar_width for prop in proportions]
        
        # Create sections
        sections = []
        current_x = -bar_width / 2  # Start from left edge
        
        for i, (width, color) in enumerate(zip(section_widths, colors)):
            # Create rectangle for this section
            section = Rectangle(width=width, height=bar_height)
            section.set_color(color)
            section.set_fill(color, opacity=1)
            section.set_stroke(BLACK, width=1)
            
            # Position section
            section.move_to(position + RIGHT * (current_x + width / 2))
            sections.append(section)
            
            current_x += width
        
        # Create braces and labels
        braces = []
        texts = []
        
        for i, (width, value) in enumerate(zip(section_widths, values)):
            # Create brace
            brace = Brace(sections[i], DOWN)
            brace.set_color(BLACK)
            braces.append(brace)
            
            # Create label text positioned in middle of brace
            text = Text(f"{value}%", font_size=36, weight=BOLD)
            text.set_color(BLACK)
            text.next_to(brace, DOWN, buff=0.1)
            texts.append(text)
        
        # Add all elements to group
        group.add(*sections)
        group.add(*braces)
        group.add(*texts)
        
        return group
    
    def setup(self):
        """Setup the scene with white background"""
        self.camera.background_color = WHITE

