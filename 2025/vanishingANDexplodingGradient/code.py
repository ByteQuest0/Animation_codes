from manimlib import *
import numpy as np


class VanishingANDexplodingGradient(Scene):
    def construct(self):
        self.camera.frame.scale(1.2).shift(RIGHT)

        # Create 5 input layer nodes (GREEN, radius=0.36)
        input_layer = []
        input_labels = []
        for i in range(5):
            node = Circle(radius=0.36, color=GREEN, fill_opacity=1, stroke_width=6, stroke_color=GREEN_B)
            node.move_to(LEFT * 6 + UP * (2.5 - i * 1.2))
            input_layer.append(node)

            # Add input labels with black color
            label = Tex(f"x_{{{i+1}}}").set_color(BLACK)
            label.move_to(node.get_center())
            input_labels.append(label)

        # Create hidden layer 1 with 4 neurons
        hidden_layer1 = []
        hidden_labels1 = []
        for i in range(4):
            node = Circle(radius=0.5, color=BLUE_C, fill_opacity=1, stroke_width=8, stroke_color=BLUE_B)
            node.move_to(LEFT * 3 + UP * (2.4 - i * 1.6))
            hidden_layer1.append(node)

            # Standard notation: A(Z^[1]_i)
            label = Tex(f"a^{{(1)}}_{{{i+1}}}").set_color(BLACK).scale(0.9)
            label.move_to(node.get_center())
            hidden_labels1.append(label)

        # Create hidden layer 2 with 5 neurons (reduced from 6)
        hidden_layer2 = []
        hidden_labels2 = []
        for i in range(5):  # Changed from 6 to 5
            node = Circle(radius=0.5, color=BLUE_C, fill_opacity=1, stroke_width=8, stroke_color=BLUE_B)
            node.move_to(ORIGIN + UP * (3.2 - i * 1.6))  # Adjusted positioning for 5 neurons
            hidden_layer2.append(node)

            # Standard notation: A(Z^[2]_i)
            label = Tex(f"a^{{(2)}}_{{{i+1}}}").set_color(BLACK).scale(0.9)
            label.move_to(node.get_center())
            hidden_labels2.append(label)

        # Create hidden layer 3 with 3 neurons
        hidden_layer3 = []
        hidden_labels3 = []
        for i in range(3):
            node = Circle(radius=0.5, color=BLUE_C, fill_opacity=1, stroke_width=8, stroke_color=BLUE_B)
            node.move_to(RIGHT * 3 + UP * (1.6 - i * 1.6))
            hidden_layer3.append(node)

            # Standard notation: A(Z^[3]_i)
            label = Tex(f"a^{{(3)}}_{{{i+1}}}").set_color(BLACK).scale(0.9)
            label.move_to(node.get_center())
            hidden_labels3.append(label)

        # Create output layer
        output_node = Circle(radius=0.72, color=BLUE_C, fill_opacity=1, stroke_width=8, stroke_color=BLUE_B)
        output_node.move_to(RIGHT * 6)

        # Add output label scaled by 1.8
        output_label = Tex("a_{1}^{(4)}").set_color(BLACK).scale(1.4)
        output_label.move_to(output_node.get_center())

        # Create all connections
        connections = []

        # Input to Hidden Layer 1
        for input_node in input_layer:
            for hidden_node in hidden_layer1:
                line = Line(input_node.get_center(), hidden_node.get_center(), 
                          stroke_width=2, color=GREY_A, z_index=-1, stroke_opacity=0.6)
                connections.append(line)

        # Hidden Layer 1 to Hidden Layer 2
        for h1_node in hidden_layer1:
            for h2_node in hidden_layer2:
                line = Line(h1_node.get_center(), h2_node.get_center(), 
                          stroke_width=2, color=GREY_A, z_index=-1, stroke_opacity=0.6)
                connections.append(line)

        # Hidden Layer 2 to Hidden Layer 3
        for h2_node in hidden_layer2:
            for h3_node in hidden_layer3:
                line = Line(h2_node.get_center(), h3_node.get_center(), 
                          stroke_width=2, color=GREY_A, z_index=-1, stroke_opacity=0.6)
                connections.append(line)

        # Hidden Layer 3 to Output
        for h3_node in hidden_layer3:
            line = Line(h3_node.get_center(), output_node.get_center(), 
                      stroke_width=2, color=GREY_A, z_index=-1, stroke_opacity=0.6)
            connections.append(line)

        # Store original line properties (ADD THIS RIGHT AFTER CREATING CONNECTIONS)
        original_stroke_widths = [line.stroke_width for line in connections]
        original_colors = [line.get_color() for line in connections]

        # Show the network structure
        all_nodes = input_layer + hidden_layer1 + hidden_layer2 + hidden_layer3 + [output_node]

        self.play(*[ShowCreation(node) for node in all_nodes])
        self.play(*[ShowCreation(line) for line in connections])
        self.wait(1.5)


        # Write input labels first
        self.play(*[Write(label) for label in input_labels])
        self.wait(1)

        # Function to create glow effect around a dot
        def create_glow(center_point, radius=0.15, color=YELLOW, intensity=0.3):
            glow_group = VGroup()
            for i in range(20):
                glow_radius = radius * (1 + i * 0.1)
                opacity = intensity * (1 - i/20)
                glow_circle = Circle(
                    radius=glow_radius, 
                    stroke_opacity=0, 
                    fill_color=color,
                    fill_opacity=opacity
                ).move_to(center_point)
                glow_group.add(glow_circle)
            return glow_group

        # Enhanced pulse creation function
        def create_pulse(start_point, color="#ff0000"):
            # Create the main pulse dot
            pulse = Dot(radius=0.12, color=color, fill_opacity=1)
            pulse.move_to(start_point)

            # Create the enhanced glow effect
            glow = create_glow(start_point, radius=0.1, color=color, intensity=0.4)

            # Combine pulse and glow into a group
            pulse_group = VGroup(glow, pulse)
            return pulse_group

        # SINGLE ITERATION WITH ONE PULSE PER WEIGHT CONNECTION

        # Stage 1: Input to Hidden Layer 1 (5×4 = 20 pulses)
        input_pulses = []


        # Get the specific connections for this stage
        input_to_h1_connections = []
        for input_node in input_layer:
            for h1_node in hidden_layer1:
                for line in connections:
                    start_pos = line.get_start()
                    input_pos = input_node.get_center()
                    h1_pos = h1_node.get_center()
                    if (abs(start_pos[0] - input_pos[0]) < 0.1 and abs(start_pos[1] - input_pos[1]) < 0.1):
                        end_pos = line.get_end()
                        if (abs(end_pos[0] - h1_pos[0]) < 0.1 and abs(end_pos[1] - h1_pos[1]) < 0.1):
                            input_to_h1_connections.append(line)


        for input_node in input_layer:
            for h1_node in hidden_layer1:
                pulse_group = create_pulse(input_node.get_center(), "#ff0000")
                input_pulses.append(pulse_group)
                self.add(pulse_group)

        self.wait(0.3)

        # Move each pulse along its specific weight connection AND color the connections
        h1_animations = []
        for i, pulse_group in enumerate(input_pulses):
            input_idx = i // len(hidden_layer1)
            h1_idx = i % len(hidden_layer1)
            target_pos = hidden_layer1[h1_idx].get_center()

            h1_animations.append(pulse_group.animate.move_to(target_pos))


        # Add connection coloring animations
        for line in input_to_h1_connections:
            h1_animations.append(line.animate.set_stroke(width=5, color="#ff0000"))

        self.play(*h1_animations, run_time=1.5)

        # Fade out and write h1 labels AND reset connection colors
        reset_animations = []
        reset_animations.extend([FadeOut(pulse_group) for pulse_group in input_pulses])
        reset_animations.extend([Write(label) for label in hidden_labels1])


        # Reset connection colors and widths
        for line in input_to_h1_connections:
            line_idx = connections.index(line)
            reset_animations.append(
                line.animate.set_stroke(width=original_stroke_widths[line_idx], 
                                      color=original_colors[line_idx])
            )


        self.play(*reset_animations, run_time=1.0)

        # Stage 2: Hidden Layer 1 to Hidden Layer 2 (4×5 = 20 pulses)
        h1_pulses = []


        # Get the specific connections for this stage
        h1_to_h2_connections = []
        for h1_node in hidden_layer1:
            for h2_node in hidden_layer2:
                for line in connections:
                    start_pos = line.get_start()
                    h1_pos = h1_node.get_center()
                    h2_pos = h2_node.get_center()
                    if (abs(start_pos[0] - h1_pos[0]) < 0.1 and abs(start_pos[1] - h1_pos[1]) < 0.1):
                        end_pos = line.get_end()
                        if (abs(end_pos[0] - h2_pos[0]) < 0.1 and abs(end_pos[1] - h2_pos[1]) < 0.1):
                            h1_to_h2_connections.append(line)

        for h1_node in hidden_layer1:
            for h2_node in hidden_layer2:
                pulse_group = create_pulse(h1_node.get_center(), "#ff0000")
                h1_pulses.append(pulse_group)
                self.add(pulse_group)

        self.wait(0.3)

        # Move each pulse along its weight connection AND color the connections
        h2_animations = []
        for i, pulse_group in enumerate(h1_pulses):
            h1_idx = i // len(hidden_layer2)
            h2_idx = i % len(hidden_layer2)
            target_pos = hidden_layer2[h2_idx].get_center()

            h2_animations.append(pulse_group.animate.move_to(target_pos))


        # Add connection coloring animations
        for line in h1_to_h2_connections:
            h2_animations.append(line.animate.set_stroke(width=5, color="#ff0000"))

        self.play(*h2_animations, run_time=1.5)

        # Fade out and write h2 labels AND reset connection colors
        reset_animations = []
        reset_animations.extend([FadeOut(pulse_group) for pulse_group in h1_pulses])
        reset_animations.extend([Write(label) for label in hidden_labels2])


        # Reset connection colors and widths
        for line in h1_to_h2_connections:
            line_idx = connections.index(line)
            reset_animations.append(
                line.animate.set_stroke(width=original_stroke_widths[line_idx], 
                                      color=original_colors[line_idx])
            )


        self.play(*reset_animations, run_time=1.0)

        # Stage 3: Hidden Layer 2 to Hidden Layer 3 (5×3 = 15 pulses)
        h2_pulses = []


        # Get the specific connections for this stage
        h2_to_h3_connections = []
        for h2_node in hidden_layer2:
            for h3_node in hidden_layer3:
                for line in connections:
                    start_pos = line.get_start()
                    h2_pos = h2_node.get_center()
                    h3_pos = h3_node.get_center()
                    if (abs(start_pos[0] - h2_pos[0]) < 0.1 and abs(start_pos[1] - h2_pos[1]) < 0.1):
                        end_pos = line.get_end()
                        if (abs(end_pos[0] - h3_pos[0]) < 0.1 and abs(end_pos[1] - h3_pos[1]) < 0.1):
                            h2_to_h3_connections.append(line)

        for h2_node in hidden_layer2:
            for h3_node in hidden_layer3:
                pulse_group = create_pulse(h2_node.get_center(), "#ff0000")
                h2_pulses.append(pulse_group)
                self.add(pulse_group)

        self.wait(0.3)

        # Move each pulse along its weight connection AND color the connections
        h3_animations = []
        for i, pulse_group in enumerate(h2_pulses):
            h2_idx = i // len(hidden_layer3)
            h3_idx = i % len(hidden_layer3)
            target_pos = hidden_layer3[h3_idx].get_center()

            h3_animations.append(pulse_group.animate.move_to(target_pos))


        # Add connection coloring animations
        for line in h2_to_h3_connections:
            h3_animations.append(line.animate.set_stroke(width=5, color="#ff0000"))

        self.play(*h3_animations, run_time=1.5)

        # Fade out and write h3 labels AND reset connection colors
        reset_animations = []
        reset_animations.extend([FadeOut(pulse_group) for pulse_group in h2_pulses])
        reset_animations.extend([Write(label) for label in hidden_labels3])


        # Reset connection colors and widths
        for line in h2_to_h3_connections:
            line_idx = connections.index(line)
            reset_animations.append(
                line.animate.set_stroke(width=original_stroke_widths[line_idx], 
                                      color=original_colors[line_idx])
            )


        self.play(*reset_animations, run_time=1.0)

        # Stage 4: Hidden Layer 3 to Output (3×1 = 3 pulses)
        h3_pulses = []


        # Get the specific connections for this stage
        h3_to_output_connections = []
        for h3_node in hidden_layer3:
            for line in connections:
                start_pos = line.get_start()
                h3_pos = h3_node.get_center()
                output_pos = output_node.get_center()
                if (abs(start_pos[0] - h3_pos[0]) < 0.1 and abs(start_pos[1] - h3_pos[1]) < 0.1):
                    end_pos = line.get_end()
                    if (abs(end_pos[0] - output_pos[0]) < 0.1 and abs(end_pos[1] - output_pos[1]) < 0.1):
                        h3_to_output_connections.append(line)

        for h3_node in hidden_layer3:
            pulse_group = create_pulse(h3_node.get_center(), "#ff0000")
            h3_pulses.append(pulse_group)
            self.add(pulse_group)

        self.wait(0.3)

        # Move to output AND color the connections
        output_animations = []
        for pulse_group in h3_pulses:
            output_animations.append(pulse_group.animate.move_to(output_node.get_center()))


        # Add connection coloring animations
        for line in h3_to_output_connections:
            output_animations.append(line.animate.set_stroke(width=5, color="#ff0000"))

        self.play(*output_animations, run_time=1.5)

        # Fade out and write output label AND reset connection colors
        reset_animations = []
        reset_animations.extend([FadeOut(pulse_group) for pulse_group in h3_pulses])
        reset_animations.append(Write(output_label))


        # Reset connection colors and widths
        for line in h3_to_output_connections:
            line_idx = connections.index(line)
            reset_animations.append(
                line.animate.set_stroke(width=original_stroke_widths[line_idx], 
                                      color=original_colors[line_idx])
            )


        self.play(*reset_animations, run_time=1.0)


        output_arrow = Arrow(output_node.get_right(), output_node.get_right()+RIGHT*1.5, stroke_width=4).set_color(WHITE)
        y_hat = Tex(r'\hat{y}').scale(2).next_to(output_arrow, RIGHT, buff=0.33)
        self.play(ShowCreation(output_arrow))
        self.play(ShowCreation(y_hat))

        self.wait(2)




        self.camera.frame.save_state()
        self.camera.frame.restore()


        self.play(self.camera.frame.animate.shift(RIGHT*5))


        temp = Tex(f"a^{{(l)}}_{{m}} \ = f(z^{{(l)}}_{{m}})").next_to(y_hat, RIGHT).shift(RIGHT*0.5)
        temp.scale(1.5).shift(UP*2.36)
        self.play(ShowCreation(temp)) 
        rect  = SurroundingRectangle(temp, color=RED_D).scale(1.04)
        self.play(ShowCreation(rect))
        self.wait(2)

        a = Tex(r"\mathbf{a}^{(l)} = f(W^{(l)} \mathbf{a}^{(l-1)} + \mathbf{b}^{(l)})").move_to(temp).shift(LEFT*1.4).scale(1.34)
        rect1  = SurroundingRectangle(a, color=RED_D).scale(1.04)        
        self.play(Transform(temp, a), Transform(rect, rect1))

        self.wait(2)

        loss_equation = Tex(r"L = \frac{1}{2}(\hat{y} - y)^2").next_to(y_hat, RIGHT).shift(RIGHT*1.12).scale(1.57)
        self.play(ShowCreation(loss_equation), FadeOut(VGroup(temp , rect)))
        rect3  = SurroundingRectangle(loss_equation, color=YELLOW).scale(1.04)
        self.play(ShowCreation(rect3))
        self.wait(2)

        self.play(FadeOut(VGroup(loss_equation, rect3, y_hat, output_arrow )), self.camera.frame.animate.shift(LEFT*6.2))
        self.wait(2)

        # --- Highlight top-most weight in last layer (output layer) ---
        top_weight_last = connections[-3].copy()  # pick the top edge going to output
        top_weight_last.set_stroke(color="#FF0000", width=9)
        self.play(ShowCreation(top_weight_last))
        self.wait(1)


        self.camera.frame.save_state()
        
        # --- Chain rule equation for topmost weight w⁴₁₁ ---
        eq_w4_11 = Tex(
            r"\frac{\partial L}{\partial w^{(4)}_{11}} = "
            r"\frac{\partial L}{\partial a^{(4)}_{1}}"
            r"\cdot \frac{\partial a^{(4)}_{1}}{\partial z^{(4)}_{1}}"
            r"\cdot \frac{\partial z^{(4)}_{1}}{\partial w^{(4)}_{11}}"
        ).scale(1.57)
        
        # Place the equation below the middle (hidden) layer
        eq_w4_11.next_to(hidden_layer2[4], DOWN, buff=0.55)
        
        # Show the equation
        self.play(Write(eq_w4_11), self.camera.frame.animate.scale(1.23).shift(DOWN*1.29))
        self.wait(2)

        self.play(eq_w4_11[21:34].animate.set_color(RED_C))
        self.wait(2)


        # --- Full simplified chain using f'() notation ---
        fprime_full_eq = Tex(
            r"\frac{\partial L}{\partial w^{(4)}_{11}} = "
            r"\frac{\partial L}{\partial a^{(4)}_{1}}"
            r"\cdot f'(z^{(4)}_{1})"
            r"\cdot a^{(3)}_{1}"
        ).scale(1.57)

        fprime_full_eq[21:30].set_color(RED_C)
        
        # Move the new equation exactly to the position of the old one
        fprime_full_eq.move_to(eq_w4_11)
        
        # Transform old chain equation to the simplified f'() version
        self.play(Transform(eq_w4_11, fprime_full_eq))
        self.wait(2)

        # Create the new top weight in the previous layer
        prev_layer_top_weight = connections[-18].copy()  # adjust index based on your connections
        prev_layer_top_weight.set_stroke(color="#FF0000", width=9)  # slightly different bright orange
        
        # Transform old top weight highlight into the new one
        self.play(Transform(top_weight_last, prev_layer_top_weight))
        self.wait(2)
        
        # --- Full chain rule in dy/dx form for previous layer weight (w³₁₁) ---
        eq_prev_chain = Tex(
                    r"\frac{\partial L}{\partial w^{(3)}_{11}} = "
                    r"\frac{\partial L}{\partial a^{(4)}_1} "
                    r"\cdot \frac{\partial a^{(4)}_1}{\partial z^{(4)}_1} "
                    r"\cdot \frac{\partial z^{(4)}_1}{\partial a^{(3)}_1} "
                    r"\cdot \frac{\partial a^{(3)}_1}{\partial z^{(3)}_1} "
                    r"\cdot \frac{\partial z^{(3)}_1}{\partial w^{(3)}_{11}}"
                ).scale(1.52)
                        
        # Move new equation exactly to the old equation's position
        eq_prev_chain.move_to(eq_w4_11)
        
        # Transform the previous equation into this full chain form
        self.play(Transform(eq_w4_11, eq_prev_chain))
        self.wait(2)

        rect = SurroundingRectangle(eq_w4_11[11:48]).scale(1.055)
        self.play(ShowCreation(rect))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(eq_w4_11[49:62]).scale(1.04)))
        self.play(eq_w4_11[49:62].animate.set_color(RED_C), Uncreate(rect))
        self.wait(2)

        simplified_eq = Tex(
            r"\frac{\partial L}{\partial w^{(3)}_{11}} = "
            r"\frac{\partial L}{\partial a^{(4)}_1} \cdot f'(z^{(4)}_1) \cdot w^{(4)}_{11})"
            r"\cdot f'(z^{(3)}_1) \cdot a^{(2)}_1"
        ).scale(1.52)
        
        # Move it to the same position as the old expanded equation
        simplified_eq.move_to(eq_w4_11)
        
        # Transform the old expanded chain into the simplified form
        self.play(Transform(eq_w4_11, simplified_eq))
        self.wait(1)

        self.play(
            eq_w4_11[30:43].animate.set_color(RED_C),
            eq_w4_11[56:67].animate.set_color(RED_C)
        )

        self.wait(2)



        # --- General proportional form for any layer l ---
        general_eq = Tex(
                r"\frac{\partial L}{\partial w_{ij}^{(l)}} \propto \prod_{m=l}^{L} f'\big(z^{(m)}\big)").scale(1.5)
        
        # Move to the same position as the old equation
        general_eq.move_to(eq_w4_11)
        
        # Transform previous simplified layer-specific equation to this general form
        self.play(Transform(eq_w4_11, general_eq), Uncreate(top_weight_last))
        self.wait(3)

        self.camera.frame.save_state()


        # --- Parameters ---
        L_start = 1
        L_end = 9
        f_prime_val = 0.25  # f'(z) ~ 0.2 for demonstration

        # --- Initial Tex: f'(z)^L ---
        grad_expr = Tex(r"f'(z)^L \ =").to_edge(UP).scale(2.5).shift(DOWN*1.8+RIGHT*18)
        self.play(Write(grad_expr), self.camera.frame.animate.shift(RIGHT*20.2))
        self.wait(0.5)

        # --- Transform f'(z)^L to numeric initial values ---
        numeric_expr = Tex(
            f"{f_prime_val}^{{{L_start}}} ="
        ).scale(2.5).move_to(grad_expr.get_center())
        self.play(Transform(grad_expr, numeric_expr))
        self.wait(0.5)

        # --- Show the value dynamically decreasing ---
        grad_value = DecimalNumber(f_prime_val**L_start, num_decimal_places=5).next_to(grad_expr, RIGHT, buff=0.82).scale(1.56).shift(RIGHT*0.14+DOWN*0.07+RIGHT*0.08+DOWN*0.08)
        self.play(FadeIn(grad_value))
        self.wait(0.5)

        for L in range(L_start, L_end + 1):
            new_val = f_prime_val**L
            # Also update the L in the Tex for clarity
            updated_expr = Tex(f"{f_prime_val}^{{{L}}} =").scale(2.5).move_to(grad_expr.get_center())
            self.play(
                Transform(grad_expr, updated_expr),
                grad_value.animate.set_value(new_val),
                run_time=0.7
            )
            self.wait(0.15)
 
        self.wait(2)
        # --- Weight update formula below ---
        w_update = Tex(
            r"w_{new} = w_{old} - \alpha \frac{\partial L}{\partial w_{old}}"
        ).next_to(VGroup(grad_expr, grad_value), DOWN, buff=1.0).scale(3).shift(DOWN*1.85)
        self.play(Write(w_update))
        self.wait(2)

        brace = Brace(w_update[-5:], DOWN, buff=0.43).set_color(YELLOW)
        self.play(ShowCreation(brace))
        temp = Text("Close to 0").next_to(brace, DOWN, buff=0.53).set_color(YELLOW).scale(1.2)
        self.play(Write(temp))
        self.wait(2)

        self.play(Transform(brace, Brace(w_update[-9:], DOWN, buff=0.43).set_color(YELLOW)))
        self.play(Transform(temp, Text("Close to 0").next_to(brace, DOWN, buff=0.53).set_color(YELLOW).scale(1.2)))
        self.wait(2)

        self.play(Transform(brace, Brace(w_update, DOWN, buff=0.43).set_color(YELLOW)))
        self.play(Transform(temp, Text("No Update at all").next_to(brace, DOWN, buff=0.53).set_color(YELLOW).scale(1.2)))
        self.wait(2)

        self.play(FadeOut(VGroup(grad_expr, grad_value, w_update, brace, temp)))


        # --- Parameters ---
        L_start = 1
        L_end = 15
        f_prime_val = 1.25  # f'(z) ~ 0.2 for demonstration

        # --- Initial Tex: f'(z)^L ---
        grad_expr = Tex(r"f'(z)^L \ =").to_edge(UP).scale(2.5).shift(DOWN*1.8+RIGHT*18)
        self.play(Write(grad_expr))
        self.wait(0.5)

        # --- Transform f'(z)^L to numeric initial values ---
        numeric_expr = Tex(
            f"{f_prime_val}^{{{L_start}}} ="
        ).scale(2.5).move_to(grad_expr.get_center())
        self.play(Transform(grad_expr, numeric_expr))
        self.wait(0.5)

        # --- Show the value dynamically decreasing ---
        grad_value = DecimalNumber(f_prime_val**L_start, num_decimal_places=5).next_to(grad_expr, RIGHT, buff=0.82).scale(1.56).shift(RIGHT*0.34+DOWN*0.07+RIGHT*0.08+DOWN*0.08)
        self.play(FadeIn(grad_value))
        self.wait(0.5)

        for L in range(L_start, L_end + 1):
            new_val = f_prime_val**L
            # Also update the L in the Tex for clarity
            updated_expr = Tex(f"{f_prime_val}^{{{L}}} =").scale(2.5).move_to(grad_expr.get_center())
            self.play(
                Transform(grad_expr, updated_expr),
                grad_value.animate.set_value(new_val),
                run_time=0.38
            )
            self.wait(0.15)
        
        self.wait(2)

        # --- Weight update formula below ---
        w_update = Tex(
            r"w_{new} = w_{old} - \alpha \frac{\partial L}{\partial w_{old}}"
        ).next_to(VGroup(grad_expr, grad_value), DOWN, buff=1.0).scale(3).shift(DOWN*1.85)
        self.play(Write(w_update))
        self.wait(2)

        brace = Brace(w_update[-5:], DOWN, buff=0.43).set_color(YELLOW)
        self.play(ShowCreation(brace))
        temp = Text("A Big Value").next_to(brace, DOWN, buff=0.53).set_color(YELLOW).scale(1.2)
        self.play(Write(temp))
        self.wait(2)

        self.play(Transform(brace, Brace(w_update[-9:], DOWN, buff=0.43).set_color(YELLOW)))
        self.play(Transform(temp, Text("A Big Value").next_to(brace, DOWN, buff=0.53).set_color(YELLOW).scale(1.2)))
        self.wait(2)

        self.play(Transform(brace, Brace(w_update, DOWN, buff=0.43).set_color(YELLOW)))
        self.play(Transform(temp, Text("Big & Unstable Updates").next_to(brace, DOWN, buff=0.53).set_color(YELLOW).scale(1.2)))
        self.wait(2)

        

        self.play(self.camera.frame.animate.shift(LEFT*20.2))
        self.wait(2)


        # --- General proportional form for any layer l ---
        general_eq = Tex(
            r"\frac{\partial L}{\partial w_{ij}^{(l)}} \propto \prod_{m=l}^{L} f'\big(z^{(m)}\big) \, W^{(m+1)}"
        ).scale(1.5)
        
        # Move to the same position as the old equation
        general_eq.move_to(eq_w4_11)
        
        # Transform previous simplified layer-specific equation to this general form
        self.play(Transform(eq_w4_11, general_eq), Uncreate(top_weight_last))
        self.wait(3)
        
