from manimlib import *
import numpy as np

class EWMA(Scene):
    def construct(self):
        self.camera.frame.scale(1.16).shift(UP*0.39)

        self.camera.frame.save_state() 
        

        # 1. Create the text stack
        # We use ellipsis (\vdots) because rendering 365 real lines would crash the video
        theta_stack = VGroup(
            Tex(r"\theta_1 = 3^o \ Celsius"),
            Tex(r"\theta_2 = 4^o \ Celsius"),
            Tex(r"\theta_3 = 4^o \ Celsius"),
            Tex(r":").scale(1.5), # Make dots a bit bigger
            Tex(r"\theta_{200} = 7^o \ Celsius"),
        )
        
        # 2. Arrange and Position
        theta_stack.arrange(DOWN, buff=0.5)
        theta_stack.scale(1.5) # Make text readable
        self.camera.frame.shift(RIGHT*16)
        theta_stack.shift(RIGHT*16+UP*0.33)
        self.play(Write(theta_stack))
        self.wait()

        rect = SurroundingRectangle(theta_stack[0], buff=0.3, stroke_color=YELLOW, stroke_width=4)
        self.play(ShowCreation(rect))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(theta_stack[1], buff=0.3, stroke_color=YELLOW, stroke_width=4)))
        self.wait(2)
        self.play(Transform(rect, SurroundingRectangle(theta_stack[2], buff=0.3, stroke_color=YELLOW, stroke_width=4)))
        self.wait(2)
        self.play(Transform(rect, SurroundingRectangle(theta_stack[-1], buff=0.3, stroke_color=YELLOW, stroke_width=4)))
        self.wait(2)


         # Save the current camera state to return later
        # --- CONFIGURATION ---
        np.random.seed(42) 
        n_points = 180  
        
        # OFFSET: Start at day 15
        days = np.arange(n_points) + 15
        
        # DATA GENERATION
        trend = 10 + 35 * np.sin((days - 15) * np.pi / n_points)
        noise = np.random.normal(0, 4, n_points)
        raw_temps = trend + noise

        # --- AXES SETUP ---
        axes = Axes(
            x_range=[0, 220],  
            y_range=[0, 60],        
            width=12,
            height=7,
            axis_config={
                "include_tip": True,
                "include_ticks": False, 
                "stroke_color": GREY_B,
                "stroke_width": 4, 
            }
        )
        axes.center()

        # --- LABELS ---
        y_label = Tex(r"\theta_t").scale(1.8)
        y_label.next_to(axes.y_axis.get_end(), UP)
        
        x_label = Tex(r"t").scale(2)
        x_label.next_to(axes.x_axis.get_end(), RIGHT)

        labels = VGroup(x_label, y_label)

        # --- PLOTTING OBJECTS ---
        
        # Raw Data (Scatter plot)
        raw_dots = VGroup()
        for day, temp in zip(days, raw_temps):
            dot = Dot(radius=0.08) # Slightly smaller base radius for contrast
            dot.move_to(axes.c2p(day, temp))
            dot.set_color(BLUE_C)
            dot.set_opacity(0.8) 
            raw_dots.add(dot)

        # --- ANIMATION SEQUENCE ---
        
        # 1. Draw Axes
        self.play(
            ShowCreation(axes), 
            self.camera.frame.animate.restore(),
            Write(labels), 
            run_time=1.5
        )
        
        # 2. Show all dots
        self.play(
            GrowFromCenter(raw_dots),
            run_time=1.5
        )

        self.wait(1)

        # --- NEW CODE: THE MOVING HIGHLIGHT ---

        # 1. Create a ValueTracker. 
        # This acts as an invisible cursor moving along the X-axis (from 0 to 220).
        scan_tracker = ValueTracker(0)

        # 2. Define the highlighting logic
        def scan_updater(dots):
            # Get the current position of the "scanner"
            current_x = scan_tracker.get_value()
            
            # Define the width of the highlight beam
            window_width = 30 

            for dot in dots:
                # Convert the dot's screen position back to graph coordinates (x, y)
                # we only care about index [0] which is the x-value (time)
                dot_x_value = axes.p2c(dot.get_center())[0]

                # Check if the dot falls inside the current scan window
                # Logic: Scan moves right. If dot is between (current - window) and (current)
                if current_x - window_width < dot_x_value < current_x:
                    # HIGHLIGHT STATE
                    dot.set_color(YELLOW)
                    dot.set_opacity(1)
                    dot.set_height(0.2) # Make it pop (bigger)
                else:
                    # ORIGINAL STATE
                    dot.set_color(BLUE_C)
                    dot.set_opacity(0.8)
                    dot.set_height(0.16) # Return to normal size (2 * radius)

        # 3. Attach the updater to the group of dots
        # This tells Manim: "Every single frame, run scan_updater on raw_dots"
        raw_dots.add_updater(scan_updater)

        # 4. Animate the tracker moving from left (0) to right (230)
        # The updater will react to this value changing automatically.
        self.play(
            scan_tracker.animate.set_value(230),
            run_time=8,
            rate_func=linear
        )

        # 5. Clean up: remove the updater so they stop checking coordinates
        raw_dots.remove_updater(scan_updater)
        
        # Ensure they are all reset to blue at the very end
        raw_dots.set_color(BLUE_C)
        raw_dots.set_opacity(0.98)

        self.wait(2)

        self.remove(rect)

        a = Tex(r"v_t = \beta v_{t-1} + (1 - \beta) \theta_t").set_color(YELLOW)
        a.scale(1.6).shift(UP*3.87+RIGHT*0.93)

        self.play(Write(a))

        rect = SurroundingRectangle(a, buff=0.3, stroke_color=PINK, stroke_width=4)
        self.play(ShowCreation(rect), FadeOut(theta_stack))
        self.wait(2)

        # We use ellipsis (\vdots) because rendering 365 real lines would crash the video
        v = VGroup(
            # Initialization
            Tex(r"v_0 = 0"), 
            
            # Step 1: Uses theta_1 = 3
            Tex(r"v_1 = \beta v_0 + (1-\beta)(3)"), 
            
            # Step 2: Uses theta_2 = 4
            Tex(r"v_2 = \beta v_1 + (1-\beta)(4)"),
            
            # Step 3: Uses theta_3 = 4
            Tex(r"v_3 = \beta v_2 + (1-\beta)(4)"),
            
            # The vertical dots
            Tex(r":").scale(1.5), 
            
            # Step 200: Uses theta_200 = 7
            Tex(r"v_{200} = \beta v_{199} + (1-\beta)(7)"),
        )
        
        # 2. Arrange and Position
        v.arrange(DOWN, buff=0.5)
        v.scale(1.5) # Make text readable
        v.shift(RIGHT*16+UP*0.43)

        self.play(
            ShowCreation(v[0]),
            self.camera.frame.animate.shift(RIGHT*16)
        )

        self.wait(2)

        self.play(ShowCreation(v[1]))
        self.wait(2)
        self.play(ShowCreation(v[2]))
        self.wait(2)
        self.play(ShowCreation(v[3]))
        self.wait(2)
        self.play(ShowCreation(v[4]))
        self.wait(2)
        self.play(ShowCreation(v[5]))
        self.wait(2)

        window_formula = Tex(
            r"Days \approx \frac{1}{1 - \beta}",
            tex_to_color_map={
                r"\beta": MAROON_B,
                r"Days": YELLOW  # Highlights what this value represents
            }
        ).scale(1.77).next_to(v, RIGHT, buff=0.79)

        self.play(self.camera.frame.animate.shift(RIGHT*3))

        self.play(Write(window_formula))
        self.wait(2)

        self.play(
            Transform(window_formula, Tex(
            r"Days \approx \frac{1}{1 - 0.9}",
            tex_to_color_map={
                r"0.9": MAROON_B,
                r"Days": YELLOW  # Highlights what this value represents
            }
        ).scale(1.77).move_to(window_formula))
        )

        self.wait(2)

        self.play(
            Transform(window_formula, Tex(
            r"Days \approx 10",
            tex_to_color_map={
                r"10": MAROON_B,
                r"Days": YELLOW  # Highlights what this value represents
            }).scale(1.77).move_to(window_formula)
        ))

        self.wait(2)


        self.play(
            Transform(window_formula, Tex(
            r"Days \approx \frac{1}{1 - \beta}",
            tex_to_color_map={
                r"\beta": MAROON_B,
                r"Days": YELLOW  # Highlights what this value represents
            }
        ).scale(1.77).move_to(window_formula)
        ))

        self.wait(2)

        self.play(
            Transform(window_formula, Tex(
            r"Days \approx \frac{1}{1 - 0.99}",
            tex_to_color_map={
                r"0.99": MAROON_B,
                r"Days": YELLOW  # Highlights what this value represents
            }
        ).scale(1.77).move_to(window_formula)
        ))

        self.wait(2)

        self.play(
            Transform(window_formula, Tex(
            r"Days \approx 100",
            tex_to_color_map={
                r"0.99": MAROON_B,
                r"Days": YELLOW  # Highlights what this value represents
            }
        ).scale(1.77).move_to(window_formula)
        ))

        self.wait(2)

        self.play(
            Transform(window_formula, Tex(
            r"Days \approx \frac{1}{1 - \beta}",
            tex_to_color_map={
                r"\beta": MAROON_B,
                r"Days": YELLOW  # Highlights what this value represents
            }
        ).scale(1.77).move_to(window_formula)
        ))

        self.wait(2)

        self.play(
            Transform(window_formula, Tex(
            r"Days \approx \frac{1}{1 - 0.5}",
            tex_to_color_map={
                r"0.5": MAROON_B,
                r"Days": YELLOW  # Highlights what this value represents
            }
        ).scale(1.77).move_to(window_formula)
        ))

        self.wait(2)

        self.play(
            Transform(window_formula, Tex(
            r"Days \approx 2",
            tex_to_color_map={
                r"2": MAROON_B,
                r"Days": YELLOW  # Highlights what this value represents
            }
        ).scale(1.77).move_to(window_formula)
        ))

        self.wait(2)

        # Expanded formula showing the decaying weights
        expanded_formula = Tex(
            r"v_t = (1-\beta)\theta_t + (1-\beta)\beta \theta_{t-1} + (1-\beta)\beta^2 \theta_{t-2} + \dots",
            tex_to_color_map={
                r"v_t": YELLOW,
                r"\theta_t": BLUE,
                r"\theta_{t-1}": BLUE,
                r"\theta_{t-2}": BLUE,
                r"\beta": MAROON_B,
                r"\dots": WHITE
            }
        ).scale(1.4)
        
        # Position and Scale
        expanded_formula.next_to(window_formula, RIGHT, buff=1.43)
        
        # Animation
        self.play(Write(expanded_formula), FadeOut(window_formula),self.camera.frame.animate.shift(RIGHT*15))
        self.wait(2)


        self.play(self.camera.frame.animate.restore(), FadeOut(expanded_formula), FadeOut(v))

        self.wait()

        beta = Tex(r"\beta = 0.9", color=YELLOW).scale(1.99).move_to(a).set_color(YELLOW)

        self.play(FadeOut(rect), FadeOut(a), )

        self.wait(2)




        now_index = 140
        now_day_value = days[now_index]

        vert_line = DashedLine(
            start=axes.c2p(now_day_value, 0),
            end=axes.c2p(now_day_value, 60),
            color=YELLOW
        )
        self.play(ShowCreation(vert_line)) 
        
        # Highlight current dot
        current_dot = raw_dots[now_index]
        self.play(current_dot.animate.set_color(YELLOW).set_height(0.2))

        # 2. Setup Updater on the OLD Beta variable
        
        beta_tracker = ValueTracker(0.9)
        
        # CHANGED HERE: Color is now MAROON_C (not YELLOW)
        beta_val_display = DecimalNumber(0.9, num_decimal_places=2, color=MAROON_C).scale(1.29)
        beta_label_text = Tex(r"\beta =", color=MAROON_C).scale(1.99)
        
        beta_dynamic_group = VGroup(beta_label_text, beta_val_display).arrange(RIGHT, buff=0.37)
        beta_dynamic_group.move_to(beta) # Exact overlap

        self.remove(beta) 
        self.add(beta_dynamic_group)
        
        beta_val_display.add_updater(lambda d: d.set_value(beta_tracker.get_value()))
        self.wait()

        # 3. The Fading Updater
        def decay_visualizer(mob_dots):
            b = beta_tracker.get_value()
            for i, dot in enumerate(mob_dots):
                lag = now_index - i
                if lag < 0:
                    dot.set_opacity(0.1).set_color(GREY)
                elif lag == 0:
                    dot.set_opacity(1).set_color(YELLOW).set_height(0.2)
                else:
                    weight = b ** lag
                    visual_opacity = np.clip(weight, 0.05, 1.0)
                    dot.set_opacity(visual_opacity)
                    new_color = interpolate_color(BLUE_E, YELLOW, visual_opacity)
                    dot.set_color(new_color)
                    dot.set_height(0.16) 

        raw_dots.add_updater(decay_visualizer)
        self.wait(3)

        # 4. Animate Beta
        self.play(beta_tracker.animate.set_value(0.99), run_time=4, rate_func=linear)
        self.wait(3)

        self.play(beta_tracker.animate.set_value(0.5), run_time=4, rate_func=linear)
        self.wait(3)
        
        self.play(beta_tracker.animate.set_value(0.9), run_time=2)

        raw_dots.remove_updater(decay_visualizer)
        self.wait(3)


        self.play(
                    FadeOut(beta_dynamic_group),
                    FadeOut(vert_line),
                    raw_dots.animate.set_color(BLUE_C).set_opacity(0.8),
                    run_time=1
                )
        

        self.wait()

        self.play(FadeIn(beta))
        self.wait(2)

        curve_beta = 0.9
        v_t = 0 # Initialization
        ewma_points = []
        
        # Calculate points
        for i, (day, temp) in enumerate(zip(days, raw_temps)):
            # EWMA Formula
            v_t = curve_beta * v_t + (1 - curve_beta) * temp
            
            # Bias Correction (v_t / (1 - beta^t))
            # This ensures the curve starts at the data level, not at 0
            v_corrected = v_t / (1 - curve_beta**(i + 1))
            
            ewma_points.append(axes.c2p(day, v_corrected))

        # Create the visual curve
        ewma_curve = VMobject()
        ewma_curve.set_points_smoothly(ewma_points)
        ewma_curve.set_color(YELLOW).set_stroke(width=8)

        # Animate it
        self.play(ShowCreation(ewma_curve), run_time=3)
        self.wait(3)



        GREEN = "#1FFF40"


        curve_beta = 0.98
        v_t = 0 # Initialization
        ewma_points = []
        
        # Calculate points
        for i, (day, temp) in enumerate(zip(days, raw_temps)):
            # EWMA Formula
            v_t = curve_beta * v_t + (1 - curve_beta) * temp
            
            # Bias Correction (v_t / (1 - beta^t))
            # This ensures the curve starts at the data level, not at 0
            v_corrected = v_t / (1 - curve_beta**(i + 1))
            
            ewma_points.append(axes.c2p(day, v_corrected))

        # Create the visual curve
        new = VMobject()
        new.set_points_smoothly(ewma_points)
        new.set_color(GREEN).set_stroke(width=8)

        beta1 = Tex(r"\beta = 0.98", color=YELLOW).scale(1.99).move_to(a).set_color(GREEN)

        # Animate it
        self.play(ReplacementTransform(ewma_curve, new), ReplacementTransform(beta, beta1) ,run_time=1.7)
        self.wait(3)


        GREEN = "#FF059B"


        curve_beta = 0.5
        v_t = 0 # Initialization
        ewma_points = []
        
        # Calculate points
        for i, (day, temp) in enumerate(zip(days, raw_temps)):
            # EWMA Formula
            v_t = curve_beta * v_t + (1 - curve_beta) * temp
            
            # Bias Correction (v_t / (1 - beta^t))
            # This ensures the curve starts at the data level, not at 0
            v_corrected = v_t / (1 - curve_beta**(i + 1))
            
            ewma_points.append(axes.c2p(day, v_corrected))

        # Create the visual curve
        new1 = VMobject()
        new1.set_points_smoothly(ewma_points)
        new1.set_color(GREEN).set_stroke(width=8)

        beta2 = Tex(r"\beta = 0.5", color=YELLOW).scale(1.99).move_to(a).set_color(GREEN)

        # Animate it
        self.play(ReplacementTransform(new, new1), ReplacementTransform(beta1, beta2) ,run_time=1.7)
        self.wait(3)


        curve_beta = 0.9
        v_t = 0 # Initialization
        ewma_points = []
        
        # Calculate points
        for i, (day, temp) in enumerate(zip(days, raw_temps)):
            # EWMA Formula
            v_t = curve_beta * v_t + (1 - curve_beta) * temp
            
            # Bias Correction (v_t / (1 - beta^t))
            # This ensures the curve starts at the data level, not at 0
            v_corrected = v_t / (1 - curve_beta**(i + 1))
            
            ewma_points.append(axes.c2p(day, v_corrected))

        # Create the visual curve
        ewma_curve = VMobject()
        ewma_curve.set_points_smoothly(ewma_points)
        ewma_curve.set_color(YELLOW).set_stroke(width=8)

        beta = Tex(r"\beta = 0.9", color=YELLOW).scale(1.99).move_to(a).set_color(YELLOW)


        self.play(ReplacementTransform(new1, ewma_curve), ReplacementTransform(beta2, beta) ,FadeIn(v), run_time=1.7)
        self.wait(3)

        self.play(self.camera.frame.animate.shift(RIGHT*16))
        self.wait(2)
        self.play(self.camera.frame.animate.shift(LEFT*16))
        self.wait(2)


        curve_beta = 0.9
        v_t = 0 # Initialization
        ewma_points = []
        
        # Calculate points
        for i, (day, temp) in enumerate(zip(days, raw_temps)):
            # EWMA Formula
            v_t = curve_beta * v_t + (1 - curve_beta) * temp
            
            # Bias Correction (v_t / (1 - beta^t))
            # This ensures the curve starts at the data level, not at 0
            v_corrected = v_t 
            
            ewma_points.append(axes.c2p(day, v_corrected))

        # Create the visual curve
        a = VMobject()
        a.set_points_smoothly(ewma_points)
        a.set_color("#ff0000").set_stroke(width=8).set_z_index(1)

        # Animate it
        self.play(ShowCreation(a), run_time=3)
        self.wait(3)


        self.play(self.camera.frame.animate.scale(0.5).shift(LEFT*4+DOWN*2))
        self.wait(2)
        
        self.play(self.camera.frame.animate.shift(UP*2+RIGHT*2))
        self.wait(2)

        self.play(self.camera.frame.animate.restore())
        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT*16))

        rect = SurroundingRectangle(v[0], buff=0.3, stroke_color=YELLOW, stroke_width=4)   
        self.play(ShowCreation(rect))
        self.wait(2)   

        self.play(Transform(rect, SurroundingRectangle(v[1], buff=0.3, stroke_color=YELLOW, stroke_width=4)))


        temp = Tex(r"v_1 = 0.9 \times 0 + (1-0.9)(3)").scale(1.5).move_to(v[1])
        temp_1 = SurroundingRectangle(temp, buff=0.3, stroke_color=YELLOW, stroke_width=4)
        
        self.play(
            Transform(v[1], temp),
            Transform(rect, temp_1)
        )

        self.wait(2)

        temp = Tex(r"v_1 = 0.3").scale(1.5).move_to(v[1])
        temp_1 = SurroundingRectangle(temp, buff=0.3, stroke_color=YELLOW, stroke_width=4)
        
        self.play(
            Transform(v[1], temp),
            Transform(rect, temp_1)
        )

        self.wait(2)

        temp = Tex(r"v_2 = 0.9 \times 0.3 + (1-0.9)(4)").scale(1.5).move_to(v[2])
        temp_1 = SurroundingRectangle(temp, buff=0.3, stroke_color=YELLOW, stroke_width=4)
        
        self.play(
            Transform(v[2], temp),
            Transform(rect, temp_1)
        )

        temp = Tex(r"v_2 = 0.67").scale(1.5).move_to(v[2])
        temp_1 = SurroundingRectangle(temp, buff=0.3, stroke_color=YELLOW, stroke_width=4)
        
        self.play(
            Transform(v[2], temp),
            Transform(rect, temp_1)
        )

        self.wait(2)


        temp = Tex(r"v_3 = 0.9 \times 0.67 + (1-0.9)(4)").scale(1.5).move_to(v[3])
        temp_1 = SurroundingRectangle(temp, buff=0.3, stroke_color=YELLOW, stroke_width=4)
        
        self.play(
            Transform(v[3], temp),
            Transform(rect, temp_1)
        )

        temp = Tex(r"v_3 = 1.003").scale(1.5).move_to(v[3])
        temp_1 = SurroundingRectangle(temp, buff=0.3, stroke_color=YELLOW, stroke_width=4)
        
        self.play(
            Transform(v[3], temp),
            Transform(rect, temp_1)
        )

        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(v[-1], buff=0.3, stroke_color=YELLOW, stroke_width=4)))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(Group(v[0], v[3]), buff=0.3, stroke_color=YELLOW, stroke_width=4)))
        self.wait(2)    

        self.play(Transform(rect, SurroundingRectangle(v[1], buff=0.3, stroke_color=YELLOW, stroke_width=4)))
        self.wait(2)       

        self.play(Transform(rect, SurroundingRectangle(v[2], buff=0.3, stroke_color=YELLOW, stroke_width=4)))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(v[3], buff=0.3, stroke_color=YELLOW, stroke_width=4)))
        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT*3))
        
        bias_correction = Tex(
            r"v_t^{corrected} = \frac{v_t}{1 - \beta^t}",
            tex_to_color_map={
                r"t": WHITE     ,     # Time
                r"v_t": YELLOW,      # The Moving Average
                r"\beta": MAROON_B,  # The Weight
            }
        ).scale(1.7)
        
        # Example: placing it centrally or at the top
        bias_correction.next_to(v, RIGHT, buff=0).shift(LEFT*0.34)
        
        self.play(Write(bias_correction))

        self.play(Transform(rect, SurroundingRectangle(bias_correction, buff=0.3, stroke_color=GREEN_B, stroke_width=4)))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(Group(v[0], v[3]), buff=0.3, stroke_color=GREEN_B, stroke_width=4)), FadeOut(bias_correction), self.camera.frame.animate.shift(LEFT*3))
        self.wait(2)    


        temp_a = Tex(r"v_1^{corrected} = 3.0").scale(1.5).move_to(v[1])
        temp_b = Tex(r"v_2^{corrected} = 3.53").scale(1.5).move_to(v[2])
        temp_c = Tex(r"v_3^{corrected} = 3.70").scale(1.5).move_to(v[3])
        
        rect_1 = SurroundingRectangle(Group(temp_a, temp_c, v[0]), buff=0.3, stroke_color=PURPLE, stroke_width=4)

        self.play(
            Transform(v[1], temp_a),
            Transform(v[2], temp_b),
            Transform(v[3], temp_c),
            Transform(rect, rect_1)
        )
        
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(v[-1], buff=0.3, stroke_color=PURPLE, stroke_width=4)))
        self.wait(2)

        self.play(self.camera.frame.animate.restore())

        self.wait(2)


        curve_beta = 0.9
        v_t = 0 # Initialization
        ewma_points = []
        
        # Calculate points
        for i, (day, temp) in enumerate(zip(days, raw_temps)):
            # EWMA Formula
            v_t = curve_beta * v_t + (1 - curve_beta) * temp
            
            # Bias Correction (v_t / (1 - beta^t))
            # This ensures the curve starts at the data level, not at 0
            v_corrected = v_t / (1 - curve_beta**(i + 1))
            
            ewma_points.append(axes.c2p(day, v_corrected))

        # Create the visual curve
        ewma_curve = VMobject()
        ewma_curve.set_points_smoothly(ewma_points)
        ewma_curve.set_color("#ff0000").set_stroke(width=8).set_z_index(1)

        # Animate it
        self.play(Transform(a, ewma_curve), run_time=2.3)
        self.wait(3)

        self.embed()



