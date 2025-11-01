from manimlib import *
import numpy as np

PURE_RED = "#FF0000"

class ZeroWeightInitialization(Scene):
    def construct(self):
        self.camera.frame.scale(1.1)

        # ===== INPUT LAYER =====
        input_positions = [UP * 1.5, DOWN * 1.5]
        input_nodes, input_labels = [], []
        for i, pos in enumerate(input_positions):
            node = Circle(radius=0.4, color=GREEN, fill_opacity=1, stroke_width=8, stroke_color=GREEN_B)
            node.move_to(LEFT * 4 + pos)
            input_nodes.append(node)
            label = Tex(f"x_{{{i+1}}}").set_color(BLACK).scale(0.9)
            label.move_to(node.get_center())
            input_labels.append(label)

        # ===== HIDDEN LAYER =====
        hidden_positions = [UP * 1.5, DOWN * 1.5]
        hidden_nodes, hidden_labels = [], []
        for i, pos in enumerate(hidden_positions):
            node = Circle(radius=0.5, color=BLUE_C, fill_opacity=1, stroke_width=8, stroke_color=BLUE_B)
            node.move_to(ORIGIN + pos)
            hidden_nodes.append(node)
            label = Tex(f"a^{{(1)}}_{{{i+1}}}").set_color(BLACK).scale(0.9).set_z_index(1)
            label.move_to(node.get_center())
            hidden_labels.append(label)

        # ===== OUTPUT LAYER =====
        output_node = Circle(radius=0.6, color=BLUE_C, fill_opacity=1, stroke_width=8, stroke_color=BLUE_B)
        output_node.move_to(RIGHT * 4)
        output_label = Tex("a^{(2)}_1").set_color(BLACK).scale(1.0).set_z_index(1)
        output_label.move_to(output_node.get_center())

        # ===== CONNECTIONS + WEIGHT LABELS =====
        weights = []
        w_labels = []
        w_names = ["w_1", "w_2", "w_3", "w_4"]
        w_index = 0

        # Input → Hidden connections
        for i, inp in enumerate(input_nodes):
            for j, hid in enumerate(hidden_nodes):
                line = Line(inp.get_center(), hid.get_center(), color=GREY_B, stroke_opacity=0.9)
                line.set_z_index(-1)
                weights.append(line)

                midpoint = (inp.get_center() + hid.get_center()) / 2
                offset = ORIGIN
                if not (i == j):
                    offset = RIGHT * 0.3 if j == 0 else LEFT * 0.3

                w_label = Tex(w_names[w_index]).scale(1.1)
                w_label.move_to(midpoint + offset)
                w_labels.append(w_label)
                w_index += 1

        # ===== HIDDEN → OUTPUT CONNECTIONS =====
        hidden_to_output = []
        w5 = Tex("w_5").scale(1.1)
        w6 = Tex("w_6").scale(1.1)

        for j, hid in enumerate(hidden_nodes):
            line = Line(hid.get_center(), output_node.get_center(), color=GREY_B, stroke_opacity=0.9)
            line.set_z_index(-1)
            hidden_to_output.append(line)

        # Position w5, w6 near connecting lines
        mid1 = (hidden_nodes[0].get_center() + output_node.get_center()) / 2
        mid2 = (hidden_nodes[1].get_center() + output_node.get_center()) / 2
        w5.move_to(mid1 + UP * 0.4 + LEFT * 0.3)
        w6.move_to(mid2 + DOWN * 0.47 + LEFT * 0.3)
        w_labels.extend([w5, w6])

        # ===== FINE ADJUSTMENTS =====
        w_labels[0].shift(UP * 0.3)
        w_labels[3].shift(DOWN * 0.3)
        w_labels[1].shift(UP * 0.7 + RIGHT * 0.6)
        w_labels[2].shift(DOWN * 0.83 + RIGHT * 0.24)

        # ===== BIASES =====
        bias_arrows, bias_labels = [], []

        # Hidden layer biases
        b1_arrow = Arrow(UP * 0.8, ORIGIN, buff=0, color=GREY_B, stroke_width=3)
        b1_arrow.next_to(hidden_nodes[0], UP, buff=0.14)
        b1_label = Tex(r"b^{(1)}_1").scale(1.1)
        b1_label.next_to(b1_arrow, UP, buff=0.22)

        b2_arrow = Arrow(DOWN * 0.8, ORIGIN, buff=0, color=GREY_B, stroke_width=3)
        b2_arrow.next_to(hidden_nodes[1], DOWN, buff=0.14)
        b2_label = Tex(r"b^{(1)}_2").scale(1.1)
        b2_label.next_to(b2_arrow, DOWN, buff=0.22)

        # Output layer bias
        b3_arrow = Arrow(UP * 0.8, ORIGIN, buff=0, color=GREY_B, stroke_width=3)
        b3_arrow.next_to(output_node, UP, buff=0.14)
        b3_label = Tex(r"b^{(2)}_1").scale(1.1)
        b3_label.next_to(b3_arrow, UP, buff=0.22)

        bias_arrows.extend([b1_arrow, b2_arrow, b3_arrow])
        bias_labels.extend([b1_label, b2_label, b3_label])

        # ===== ANIMATIONS =====
        self.play(
            *[GrowFromCenter(i) for i in input_nodes + hidden_nodes + [output_node]],
            *[GrowFromCenter(j) for j in input_labels + hidden_labels + [output_label]],
            run_time=1
        )
        self.play(*[ShowCreation(i) for i in weights + hidden_to_output], run_time=2)
        self.play(*[GrowFromCenter(k) for k in w_labels], run_time=1)
        self.play(*[GrowArrow(b) for b in bias_arrows], *[FadeIn(lbl) for lbl in bias_labels], run_time=1)

        # ===== OUTPUT ARROW =====
        arrow = Arrow(output_node.get_right() + RIGHT * 0.27, RIGHT * 6, buff=0, stroke_width=3, color=GREY_B)
        self.play(GrowArrow(arrow), run_time=1)
        y_hat = Tex(r"\hat{y}").set_color(WHITE).scale(1.55)
        y_hat.next_to(arrow, RIGHT, buff=0.22)
        self.play(GrowFromCenter(y_hat), self.camera.frame.animate.shift(RIGHT), run_time=1)
        self.wait(2)

        # ===== PULSE HELPERS =====
        def create_glow(center_point, radius=0.12, color=PURE_RED, intensity=0.4):
            g = VGroup()
            for i in range(15):
                rr = radius * (1 + 0.12 * i)
                op = intensity * (1 - i / 15)
                glow_circle = Circle(radius=rr, stroke_opacity=0, fill_color=color, fill_opacity=op)
                glow_circle.move_to(center_point)
                g.add(glow_circle)
            return g

        def create_pulse(point, color=PURE_RED, radius=0.10):
            dot = Dot(radius=radius, color=color, fill_opacity=1).move_to(point)
            glow = create_glow(point, radius=radius * 0.8, color=color, intensity=0.5)
            return VGroup(glow, dot)

        def pulse_stage(lines, extra_lines=None, color=PURE_RED, run_time=1.2):
            """Animate pulses along lines + optional bias arrows (bias → node center)."""
            pulses, anims = [], []
            all_lines = lines + (extra_lines if extra_lines else [])

            for ln in all_lines:
                start = ln.get_start()

                # Bias arrows go to nearest node center
                if isinstance(ln, Arrow):
                    possible_nodes = input_nodes + hidden_nodes + [output_node]
                    end = min(possible_nodes, key=lambda n: np.linalg.norm(n.get_center() - ln.get_end())).get_center()
                else:
                    end = ln.get_end()

                p = create_pulse(start, color=color)
                pulses.append(p)
                self.add(p)
                anims.append(p.animate.move_to(end))

            if anims:
                self.play(*anims, run_time=run_time)
                self.play(*[FadeOut(p) for p in pulses], run_time=0.25)

        # ===== PULSES START (Simultaneous bias + inputs) =====
        self.wait(0.5)
        self.play(self.camera.frame.animate.scale(1.2).shift(DOWN*0.7))
        pulse_stage(weights, extra_lines=[b1_arrow, b2_arrow], color=PURE_RED, run_time=1.5)

        a = Tex("a_1^{(1)} = f(w_1 x_1 + w_2 x_2 + b_1^{(1)})")
        b = Tex("a_2^{(1)} = f(w_3 x_1 + w_4 x_2 + b_2^{(1)})")

        a.next_to(bias_labels[1], DOWN, buff=0.6).scale(1.33).shift(LEFT*3.5)
        b.next_to(a, RIGHT, buff=1.95).scale(1.33)

        self.play(
            TransformFromCopy(hidden_labels[0], a[:5]),
            TransformFromCopy(hidden_labels[1], b[:5]),
        )
        self.wait()

        self.play(FadeIn(a[5:8]), FadeIn(a[-1]), FadeIn(b[5:8]), FadeIn(b[-1]))
        self.wait()

        self.play(
            TransformFromCopy(w_labels[0], a[8:10]),
            TransformFromCopy(w_labels[1], a[13:15]),
            TransformFromCopy(w_labels[2], b[8:10]),
            TransformFromCopy(w_labels[3], b[13:15]),
            TransformFromCopy(input_labels[0], a[10:12]),
            TransformFromCopy(input_labels[1], a[15:17]),
            TransformFromCopy(input_labels[0], b[10:12]),
            TransformFromCopy(input_labels[1], b[15:17]),
            TransformFromCopy(bias_labels[0], a[-6:-1]),
            TransformFromCopy(bias_labels[1], b[-6:-1]),
            FadeIn(a[12:13]), FadeIn(a[17:18]), FadeIn(b[12:13]), FadeIn(b[17:18]),
            run_time=2
        )

        self.wait(2)


        pulse_stage(hidden_to_output, extra_lines=[b3_arrow], color=PURE_RED, run_time=1.5)
        self.wait(0.5)

        c = Tex(r"\hat{y} = a_1^{(2)} = f(w_5 a_1^{(1)} + w_6 a_2^{(1)} + b_1^{(2)})")
        c.next_to(b, DOWN, buff=1.0).scale(1.33).move_to(VGroup(a, b)).scale(1.15)

        self.play(
            FadeOut(a), FadeOut(b), 
            TransformFromCopy(y_hat, c[:2]),
            FadeIn(c[2]),
            TransformFromCopy(output_label, c[3:8]),
        
        )

        self.wait(2)

        self.play(
            FadeIn(c[8])
        )

        self.play(FadeIn(c[9:11]), FadeIn(c[-1])) 

        self.play(
            TransformFromCopy(w5, c[11:13]),
            TransformFromCopy(w6, c[19:21]),
            TransformFromCopy(hidden_labels[0], c[13:18]),
            TransformFromCopy(hidden_labels[1], c[21:26]),
            TransformFromCopy(bias_labels[2], c[-6:-1]),
            FadeIn(c[18]), FadeIn(c[26]),
            run_time=2
        )

        self.wait(2)
        
        d = Tex(r"\hat{y} = f(w_5 f(w_1 x_1 + w_2 x_2 + b_1^{(1)}) + w_6 f(w_3 x_1 + w_4 x_2 + b_2^{(1)}) + b_1^{(2)})").move_to(c).scale(1.12)
        self.play(ReplacementTransform(c, d), run_time=1)

        self.wait(2)

        zero_labels = []
        all_symbols = w_labels + bias_labels
        
        # Create zero versions at the same positions
        for lbl in all_symbols:
            zero_tex = Text("0").scale(1.1)
            zero_tex.move_to(lbl.get_center())
            zero_labels.append(zero_tex)
        
        # Group both for easier animation
        zero_group = VGroup(*zero_labels)
        original_group = VGroup(*all_symbols)
        
        # ===== Fade original labels out, fade zeros in =====
        self.play(
            FadeOut(original_group, shift=UP*0.05),
            FadeIn(zero_group, shift=UP*0.05),
            run_time=1.2
        )
        self.wait(2)
                 
        self.camera.frame.save_state()
        self.wait(2)

        self.play(Transform(d, Tex(r"\hat{y} = f(0 \cdot f(0 \cdot x_1 + 0 \cdot x_2 + 0) + 0 \cdot f(0 \cdot x_1 + 0 \cdot x_2 + 0) + 0)").move_to(d).scale(1.12)))
        
        self.wait(2)
        self.play(Transform(d, Tex(r"\hat{y} = f(0)").move_to(d).scale(1.82)))
        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT*16), d.animate.shift(RIGHT*16+UP*4.5))
        self.wait(2)

        self.play(Transform(d, Tex(r"f(0) \ = \ ReLU(0) \ = \ 0").move_to(d).scale(1.82)))

        self.wait(2)

        self.play(d.animate.shift(UP*1.1))

        e = Tex(r"f'(0) \ = \ ReLU'(0) \ = \ 0").move_to(d).scale(1.82).shift(DOWN*2)
        self.play(Write(e))

        self.wait(2)

        a1 = Tex(r"a^{(1)}_1 = f(w_1 x_1 + w_2 x_2 + b^{(1)}_1)")
        a1.move_to(d).scale(1.85).shift(DOWN*0.3565)

        a2 = Tex(r"a^{(1)}_2 = f(w_3 x_1 + w_4 x_2 + b^{(1)}_2)")
        a2.next_to(a1, DOWN, buff=0.97).scale(1.85)

        self.play(
            FadeIn(VGroup(a1, a2)),
            FadeOut(VGroup(d, e)),
        )

        self.wait(2)

        self.play(
            Transform(a1, Tex(r"a^{(1)}_1 = f(0 \cdot x_1 + 0 \cdot x_2 + 0)").move_to(a1).scale(1.85)),
            Transform(a2, Tex(r"a^{(1)}_2 = f(0 \cdot x_1 + 0 \cdot x_2 + 0)").move_to(a2).scale(1.85)),
        )

        self.wait(2)

        self.play(
            Transform(a1, Tex(r"a^{(1)}_1 = f(0) = 0").move_to(a1).scale(1.85)),
            Transform(a2, Tex(r"a^{(1)}_2 = f(0) = 0").move_to(a2).scale(1.85)),
        )

        self.wait(2)


        a = Tex(r"\frac{\partial L}{\partial w_5} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z^{(2)}} \cdot \frac{\partial z^{(2)}}{\partial w_5}").scale(1.32)

        a.move_to(VGroup(a1, a2)).scale(1.62)

        self.play(FadeOut(VGroup(a1, a2)), FadeIn(a))

        self.wait(2)

        temp = Tex(r"\frac{\partial L}{\partial w_5} = \frac{\partial L}{\partial \hat{y}} \cdot f'(z^{(2)}) \cdot a_1^{(1)}").scale(1.32*1.52)
        temp.move_to(a)
        self.play(Transform(a, temp))
        self.wait(2)



        brace = Brace(a[-16:], DOWN, buff=0.53).set_color(YELLOW)
        self.play(GrowFromCenter(brace))
        self.wait(2)

        temp = Tex(r"\frac{\partial L}{\partial w_5} = \frac{\partial L}{\partial \hat{y}} \cdot f'(0) \cdot f(0)").scale(1.32*1.52)
        temp.move_to(a)
        self.play(Transform(a, temp))
        self.play(FadeOut(brace))
        self.wait(2)

        temp = Tex(r"\frac{\partial L}{\partial w_5} = \frac{\partial L}{\partial \hat{y}} \cdot ReLU'(0) \cdot ReLU(0)").scale(1.32*1.45)
        temp.move_to(a)
        self.play(Transform(a, temp))        
        self.wait(2)

        self.play(Transform(a, Tex(r"\frac{\partial L}{\partial w_5} = \frac{\partial L}{\partial \hat{y}} \cdot 0 \cdot 0 = 0").move_to(a).scale(1.32*1.45)))
        self.wait(2)

        self.play(a.animate.shift(UP*1.699))

        b = Tex(r"w_5 \rightarrow w_5 - \alpha \cdot \frac{\partial L}{\partial w_5}").move_to(a).scale(1.32*1.2).shift(DOWN*2)
        b.shift(DOWN*1.5).scale(1.55).shift(DOWN*0.3333)
        self.play(Write(b))
        self.wait(2)

        self.play(Transform(b, Tex(r"w_5 \rightarrow w_5 - \alpha \cdot 0").move_to(b).scale(1.32*1.2).scale(1.55)), run_time=0.5)
        self.wait(2)

        self.play(Transform(b, Tex(r"w_5 \rightarrow w_5").move_to(b).scale(1.32*1.2).scale(1.85)), run_time=0.5)
        rect = SurroundingRectangle(b, color=YELLOW, buff=0.2).scale(1.1)
        self.play(ShowCreation(rect))
        text = Text("No Update!", ).scale(2).next_to(rect, DOWN, buff=0.97).set_color(RED_B)
        self.play(Write(text))
        self.wait(2)

        c = Tex(r"\frac{\partial L}{\partial w_1} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z^{(2)}} \cdot \frac{\partial z^{(2)}}{\partial a_1^{(1)}} \cdot \frac{\partial a_1^{(1)}}{\partial z_1^{(1)}} \cdot \frac{\partial z_1^{(1)}}{\partial w_1}")
        c.move_to(VGroup(a, b)).scale(1.77).shift(DOWN*0.3299)
        self.play(FadeOut(VGroup(a, b, rect, text)), FadeIn(c))

        self.wait(2)

        temp = Tex(r"\frac{\partial L}{\partial w_1} = \frac{\partial L}{\partial \hat{y}} \cdot f'(z^{(2)}) \cdot w_5 \cdot f'(z_1^{(1)}) \cdot x_1")
        temp.move_to(c).scale(1.77)
        self.play(Transform(c, temp))
        self.wait(2)

        self.play(Transform(c, Tex(r"\frac{\partial L}{\partial w_1} = 0").move_to(c).scale(2.5)))
        self.wait(2)


        a = Tex(r"\hat{y} = f(0)").move_to(c).scale(2.53)
        self.play(FadeOut(c), FadeIn(a))
        self.wait(2)


        self.play(Transform(a, Tex(r"f(0)  = \sigma (0)  =  0.5").move_to(a).scale(2)))

        self.wait(2)

        self.play(a.animate.shift(UP*1.1))

        e = Tex(r"f'(0)  = \sigma '(0)  =  0.25").move_to(d).scale(2).shift(DOWN*2.4)
        self.play(Write(e))


        self.wait(2)

        b = Tex("a_1^{(1)} = \sigma(w_1 x_1 + w_2 x_2 + b_1^{(1)})").move_to(a).scale(1.82)

        c = Tex("a_2^{(1)} = \sigma(w_3 x_1 + w_4 x_2 + b_2^{(1)})").move_to(e).scale(1.82)

        self.play(FadeOut(a), FadeOut(e), FadeIn(b), FadeIn(c))
        self.wait(2)

        self.play(Transform(b, Tex("a_1^{(1)} = \sigma(0 \cdot x_1 + 0 \cdot x_2 + 0)").move_to(b).scale(1.82)),
                  Transform(c, Tex("a_2^{(1)} = \sigma(0 \cdot x_1 + 0 \cdot x_2 + 0)").move_to(c).scale(1.82)))
        self.wait(2)

        self.play(Transform(b, Tex("a_1^{(1)} = \sigma(0) = 0.5").move_to(b).scale(1.82)),
                  Transform(c, Tex("a_2^{(1)} = \sigma(0) = 0.5").move_to(c).scale(1.82)))
        self.wait(2)

        a = Tex(r"\frac{\partial L}{\partial w_5} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z^{(2)}} \cdot \frac{\partial z^{(2)}}{\partial w_5}")
        a.move_to(VGroup(b, c)).scale(1.62).shift(UP*1.54)

        a1 = Tex(r"\frac{\partial L}{\partial w_6} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z^{(2)}} \cdot \frac{\partial z^{(2)}}{\partial w_6}")
        a1.move_to(a).shift(DOWN*3.2).scale(1.62)

        self.play(FadeOut(VGroup(b, c)), FadeIn(a), FadeIn(a1))

        self.wait(2)

        self.play(
            Transform(a, Tex(r"\frac{\partial L}{\partial w_5} = \frac{\partial L}{\partial \hat{y}} \cdot \sigma'(z^{(2)}) \cdot a_1^{(1)}").move_to(a).scale(1.62)),
            Transform(a1, Tex(r"\frac{\partial L}{\partial w_6} = \frac{\partial L}{\partial \hat{y}} \cdot \sigma'(z^{(2)}) \cdot a_2^{(1)}").move_to(a1).scale(1.62)),
        )

        self.wait(2)

        self.play(
            Transform(a, Tex(r"\frac{\partial L}{\partial w_5} = \frac{\partial L}{\partial \hat{y}} \cdot 0.25 \cdot 0.5").move_to(a).scale(1.62)),
            Transform(a1, Tex(r"\frac{\partial L}{\partial w_6} = \frac{\partial L}{\partial \hat{y}} \cdot 0.25 \cdot 0.5").move_to(a1).scale(1.62)),
        )

        self.wait(2)

        rect1 = SurroundingRectangle(a, color=YELLOW, buff=0.2).scale(1.1)
        rect2 = SurroundingRectangle(a1, color=YELLOW, buff=0.2).scale(1.1)
        self.play(ShowCreation(rect1), ShowCreation(rect2))
        
        
        self.wait(2)


        self.play(self.camera.frame.animate.restore().scale(0.83).shift(UP*0.65))
        self.wait(2)

        self.play(
            FadeOut(zero_group, shift=DOWN*0.05),
            FadeIn(original_group, shift=DOWN*0.05),
            run_time=1.2
        )

        temp_a = Circle(stroke_width=6).move_to(w5).set_color("#ff0000").scale(0.5)
        temp_b = Circle(stroke_width=6).move_to(w6).set_color("#ff0000").scale(0.5)
        self.play(
            ShowCreation(temp_a),
            ShowCreation(temp_b),
        )

        self.play(
            w_labels[4].animate.set_color(YELLOW),
            hidden_to_output[0].animate.set_color(YELLOW),
            w_labels[5].animate.set_color(YELLOW),
            hidden_to_output[1].animate.set_color(YELLOW),
            run_time=1
        )

        self.wait(2)

        self.camera.frame.save_state()


        self.play(self.camera.frame.animate.scale(1/0.83).shift(RIGHT*16+DOWN*0.72), FadeOut(VGroup(temp_a, temp_b)))
        self.wait(2)

        b = Tex(r"\frac{\partial L}{\partial w_1} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z^{(2)}} \cdot \frac{\partial z^{(2)}}{\partial a^{(1)}_1} \cdot \frac{\partial a^{(1)}_1}{\partial z^{(1)}_1} \cdot \frac{\partial z^{(1)}_1}{\partial w_1}")
        b.move_to(VGroup(a)).scale(1.27).shift(UP*1.733)

        c = Tex(r"\frac{\partial L}{\partial w_2} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z^{(2)}} \cdot \frac{\partial z^{(2)}}{\partial a^{(1)}_1} \cdot \frac{\partial a^{(1)}_1}{\partial z^{(1)}_1} \cdot \frac{\partial z^{(1)}_1}{\partial w_2}")
        c.move_to(b).scale(1.27).shift(DOWN*2.4)

        d = Tex(r"\frac{\partial L}{\partial w_3} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z^{(2)}} \cdot \frac{\partial z^{(2)}}{\partial a^{(1)}_2} \cdot \frac{\partial a^{(1)}_2}{\partial z^{(1)}_2} \cdot \frac{\partial z^{(1)}_2}{\partial w_3}")
        d.move_to(c).scale(1.27).shift(DOWN*2.4)

        e = Tex(r"\frac{\partial L}{\partial w_4} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z^{(2)}} \cdot \frac{\partial z^{(2)}}{\partial a^{(1)}_2} \cdot \frac{\partial a^{(1)}_2}{\partial z^{(1)}_2} \cdot \frac{\partial z^{(1)}_2}{\partial w_4}")
        e.move_to(d).scale(1.27).shift(DOWN*2.4)

        self.play(FadeOut(VGroup(a, a1, rect1, rect2)), FadeIn(b), FadeIn(c), FadeIn(d), FadeIn(e))

        self.wait(2)

        self.play(
            Transform(b, Tex(r"\frac{\partial L}{\partial w_1} = \frac{\partial L}{\partial \hat{y}} \cdot \sigma'(z^{(2)}) \cdot w_5 \cdot \sigma'(z^{(1)}_1) \cdot x_1").move_to(b).scale(1.27)),
            Transform(c, Tex(r"\frac{\partial L}{\partial w_2} = \frac{\partial L}{\partial \hat{y}} \cdot \sigma'(z^{(2)}) \cdot w_5 \cdot \sigma'(z^{(1)}_1) \cdot x_2").move_to(c).scale(1.27)),
            Transform(d, Tex(r"\frac{\partial L}{\partial w_3} = \frac{\partial L}{\partial \hat{y}} \cdot \sigma'(z^{(2)}) \cdot w_6 \cdot \sigma'(z^{(1)}_2) \cdot x_1").move_to(d).scale(1.27)),
            Transform(e, Tex(r"\frac{\partial L}{\partial w_4} = \frac{\partial L}{\partial \hat{y}} \cdot \sigma'(z^{(2)}) \cdot w_6 \cdot \sigma'(z^{(1)}_2) \cdot x_2").move_to(e).scale(1.27)),
        )

        self.wait(2)

        rect1 = SurroundingRectangle(b, color=YELLOW, buff=0.2).scale(1.1)
        rect2 = SurroundingRectangle(d, color=YELLOW, buff=0.2  ).scale(1.1)
        
        self.play(ShowCreation(rect1), ShowCreation(rect2))
        self.wait(2)

        self.play(
            Transform(rect1, SurroundingRectangle(c, color=YELLOW, buff=0.2).scale(1.1)),
            Transform(rect2, SurroundingRectangle(e, color=YELLOW, buff=0.2  ).scale(1.1)),
        )

        self.wait(2)

        self.play(
            FadeOut(VGroup(b, c, d, e, rect1, rect2)),
            self.camera.frame.animate.restore()       
        )

        temp_a = Circle().move_to(w_labels[0]).set_color("#ff0000").scale(0.5)
        temp_b = Circle().move_to(w_labels[2]).set_color("#ff0000").scale(0.5)

        self.play(
            ShowCreation(temp_a),
            ShowCreation(temp_b),
        )   
        self.play(
            w_labels[0].animate.set_color(PURPLE_C),
            weights[0].animate.set_color(PURPLE_C),
            w_labels[2].animate.set_color(PURPLE_C),
            weights[1].animate.set_color(PURPLE_C),
            run_time=1
        )
        self.wait(2)

        self.play(
            Transform(temp_a, Circle().move_to(w_labels[1]).set_color("#ff0000").scale(0.5)),
            Transform(temp_b, Circle().move_to(w_labels[3]).set_color("#ff0000").scale(0.5)),
        )

        MAROON = "#EF4713"
        self.play(
            w_labels[1].animate.set_color(MAROON),
            weights[2].animate.set_color(MAROON),
            w_labels[3].animate.set_color(MAROON),
            weights[3].animate.set_color(MAROON),
            run_time=1
        )
        self.wait(2)

        self.play(self.camera.frame.animate.shift(UP*0.149), Uncreate(temp_a), Uncreate(temp_b))


        self.play(Indicate(hidden_nodes[0], color="#ff0000"), Indicate(hidden_nodes[1], color="#ff0000"), run_time=0.5)
        self.play(Indicate(hidden_nodes[0], color="#ff0000"), Indicate(hidden_nodes[1], color="#ff0000"), run_time=0.5)
        self.play(Indicate(hidden_nodes[0], color="#ff0000"), Indicate(hidden_nodes[1], color="#ff0000"), run_time=0.5)
        self.play(Indicate(hidden_nodes[0], color="#ff0000"), Indicate(hidden_nodes[1], color="#ff0000"), run_time=0.5)
        
        self.wait(2)

        self.play(FadeOut(VGroup(bias_labels, )), FadeOut(w5), FadeOut(w6), FadeOut(b1_arrow), FadeOut(b2_arrow), FadeOut(b3_arrow), FadeOut(w_labels[0]), FadeOut(w_labels[1]), FadeOut(w_labels[2]), FadeOut(w_labels[3]), )
    
        self.wait(2)

        c = hidden_nodes[0].copy()
        d = hidden_labels[0].copy()

        c.shift(DOWN*1.54)
        d.shift(DOWN*1.54)

        w1 = Line(input_nodes[0].get_center(), c.get_center(), color=GREY_B, stroke_opacity=0.9).set_color(PURPLE_B).set_z_index(-1)
        w2 = Line(input_nodes[1].get_center(), c.get_center(), color=GREY_B, stroke_opacity=0.9).set_color("#ff0000").set_z_index(-1)
        w3 = Line(c.get_center(), output_node.get_center(), color=GREY_B, stroke_opacity=0.9).set_color(YELLOW_C).set_z_index(-1)

        self.play(
            ReplacementTransform(hidden_nodes[0], c),
            ReplacementTransform(hidden_labels[0], d),
            ReplacementTransform(hidden_nodes[1], c),
            ReplacementTransform(hidden_labels[1], d),
            ReplacementTransform(weights[0], w1),
            ReplacementTransform(weights[1], w1),
            ReplacementTransform(weights[2], w2),
            ReplacementTransform(weights[3], w2),
            ReplacementTransform(hidden_to_output[0], w3),
            ReplacementTransform(hidden_to_output[1], w3)
        )


        self.wait(2)

        a = Text("Symmetry breaking problem", weight=BOLD)
        a.next_to(c, DOWN, buff=1.2).scale(1.65).set_color(RED_B).shift(DOWN*1.23+RIGHT*1.4)

        self.play(self.camera.frame.animate.shift(DOWN*1.16), Write(a))
        self.wait(3)


class NonZeroConstantWeightInitialization(Scene):
    def construct(self):
        self.camera.frame.scale(1.1)

        # ===== INPUT LAYER =====
        input_positions = [UP * 1.5, DOWN * 1.5]
        input_nodes, input_labels = [], []
        for i, pos in enumerate(input_positions):
            node = Circle(radius=0.4, color=GREEN, fill_opacity=1, stroke_width=8, stroke_color=GREEN_B)
            node.move_to(LEFT * 4 + pos)
            input_nodes.append(node)
            label = Tex(f"x_{{{i+1}}}").set_color(BLACK).scale(0.9)
            label.move_to(node.get_center())
            input_labels.append(label)

        # ===== HIDDEN LAYER =====
        hidden_positions = [UP * 1.5, DOWN * 1.5]
        hidden_nodes, hidden_labels = [], []
        for i, pos in enumerate(hidden_positions):
            node = Circle(radius=0.5, color=BLUE_C, fill_opacity=1, stroke_width=8, stroke_color=BLUE_B)
            node.move_to(ORIGIN + pos)
            hidden_nodes.append(node)
            label = Tex(f"a^{{(1)}}_{{{i+1}}}").set_color(BLACK).scale(0.9).set_z_index(1)
            label.move_to(node.get_center())
            hidden_labels.append(label)

        # ===== OUTPUT LAYER =====
        output_node = Circle(radius=0.6, color=BLUE_C, fill_opacity=1, stroke_width=8, stroke_color=BLUE_B)
        output_node.move_to(RIGHT * 4)
        output_label = Tex("a^{(2)}_1").set_color(BLACK).scale(1.0).set_z_index(1)
        output_label.move_to(output_node.get_center())

        # ===== CONNECTIONS + WEIGHT LABELS =====
        weights = []
        w_labels = []
        w_names = ["w_1", "w_2", "w_3", "w_4"]
        w_index = 0

        # Input → Hidden connections
        for i, inp in enumerate(input_nodes):
            for j, hid in enumerate(hidden_nodes):
                line = Line(inp.get_center(), hid.get_center(), color=GREY_B, stroke_opacity=0.9)
                line.set_z_index(-1)
                weights.append(line)

                midpoint = (inp.get_center() + hid.get_center()) / 2
                offset = ORIGIN
                if not (i == j):
                    offset = RIGHT * 0.3 if j == 0 else LEFT * 0.3

                w_label = Tex(w_names[w_index]).scale(1.1)
                w_label.move_to(midpoint + offset)
                w_labels.append(w_label)
                w_index += 1

        # ===== HIDDEN → OUTPUT CONNECTIONS =====
        hidden_to_output = []
        w5 = Tex("w_5").scale(1.1)
        w6 = Tex("w_6").scale(1.1)

        for j, hid in enumerate(hidden_nodes):
            line = Line(hid.get_center(), output_node.get_center(), color=GREY_B, stroke_opacity=0.9)
            line.set_z_index(-1)
            hidden_to_output.append(line)

        # Position w5, w6 near connecting lines
        mid1 = (hidden_nodes[0].get_center() + output_node.get_center()) / 2
        mid2 = (hidden_nodes[1].get_center() + output_node.get_center()) / 2
        w5.move_to(mid1 + UP * 0.4 + LEFT * 0.3)
        w6.move_to(mid2 + DOWN * 0.47 + LEFT * 0.3)
        w_labels.extend([w5, w6])

        # ===== FINE ADJUSTMENTS =====
        w_labels[0].shift(UP * 0.3)
        w_labels[3].shift(DOWN * 0.3)
        w_labels[1].shift(UP * 0.7 + RIGHT * 0.6)
        w_labels[2].shift(DOWN * 0.83 + RIGHT * 0.24)

        # ===== BIASES =====
        bias_arrows, bias_labels = [], []

        # Hidden layer biases
        b1_arrow = Arrow(UP * 0.8, ORIGIN, buff=0, color=GREY_B, stroke_width=3)
        b1_arrow.next_to(hidden_nodes[0], UP, buff=0.14)
        b1_label = Tex(r"b^{(1)}_1").scale(1.1)
        b1_label.next_to(b1_arrow, UP, buff=0.22)

        b2_arrow = Arrow(DOWN * 0.8, ORIGIN, buff=0, color=GREY_B, stroke_width=3)
        b2_arrow.next_to(hidden_nodes[1], DOWN, buff=0.14)
        b2_label = Tex(r"b^{(1)}_2").scale(1.1)
        b2_label.next_to(b2_arrow, DOWN, buff=0.22)

        # Output layer bias
        b3_arrow = Arrow(UP * 0.8, ORIGIN, buff=0, color=GREY_B, stroke_width=3)
        b3_arrow.next_to(output_node, UP, buff=0.14)
        b3_label = Tex(r"b^{(2)}_1").scale(1.1)
        b3_label.next_to(b3_arrow, UP, buff=0.22)

        bias_arrows.extend([b1_arrow, b2_arrow, b3_arrow])
        bias_labels.extend([b1_label, b2_label, b3_label])

        # ===== ANIMATIONS =====
        self.play(
            *[GrowFromCenter(i) for i in input_nodes + hidden_nodes + [output_node]],
            *[GrowFromCenter(j) for j in input_labels + hidden_labels + [output_label]],
            run_time=1
        )
        self.play(*[ShowCreation(i) for i in weights + hidden_to_output], run_time=2)
        self.play(*[GrowFromCenter(k) for k in w_labels], run_time=1)
        self.play(*[GrowArrow(b) for b in bias_arrows], *[FadeIn(lbl) for lbl in bias_labels], run_time=1)

        # ===== OUTPUT ARROW =====
        arrow = Arrow(output_node.get_right() + RIGHT * 0.27, RIGHT * 6, buff=0, stroke_width=3, color=GREY_B)
        self.play(GrowArrow(arrow), run_time=1)
        y_hat = Tex(r"\hat{y}").set_color(WHITE).scale(1.55)
        y_hat.next_to(arrow, RIGHT, buff=0.22)
        self.play(GrowFromCenter(y_hat), self.camera.frame.animate.shift(RIGHT), run_time=1)
        self.wait(2)

        # ===== PULSE HELPERS =====
        def create_glow(center_point, radius=0.12, color=PURE_RED, intensity=0.4):
            g = VGroup()
            for i in range(15):
                rr = radius * (1 + 0.12 * i)
                op = intensity * (1 - i / 15)
                glow_circle = Circle(radius=rr, stroke_opacity=0, fill_color=color, fill_opacity=op)
                glow_circle.move_to(center_point)
                g.add(glow_circle)
            return g

        def create_pulse(point, color=PURE_RED, radius=0.10):
            dot = Dot(radius=radius, color=color, fill_opacity=1).move_to(point)
            glow = create_glow(point, radius=radius * 0.8, color=color, intensity=0.5)
            return VGroup(glow, dot)

        def pulse_stage(lines, extra_lines=None, color=PURE_RED, run_time=1.2):
            """Animate pulses along lines + optional bias arrows (bias → node center)."""
            pulses, anims = [], []
            all_lines = lines + (extra_lines if extra_lines else [])

            for ln in all_lines:
                start = ln.get_start()

                # Bias arrows go to nearest node center
                if isinstance(ln, Arrow):
                    possible_nodes = input_nodes + hidden_nodes + [output_node]
                    end = min(possible_nodes, key=lambda n: np.linalg.norm(n.get_center() - ln.get_end())).get_center()
                else:
                    end = ln.get_end()

                p = create_pulse(start, color=color)
                pulses.append(p)
                self.add(p)
                anims.append(p.animate.move_to(end))

            if anims:
                self.play(*anims, run_time=run_time)
                self.play(*[FadeOut(p) for p in pulses], run_time=0.25)

        # ===== PULSES START (Simultaneous bias + inputs) =====
        self.wait(0.5)
        self.play(self.camera.frame.animate.scale(1.2).shift(DOWN*0.7))
        pulse_stage(weights, extra_lines=[b1_arrow, b2_arrow], color=PURE_RED, run_time=1.5)

        a = Tex("a_1^{(1)} = f(w_1 x_1 + w_2 x_2 + b_1^{(1)})")
        b = Tex("a_2^{(1)} = f(w_3 x_1 + w_4 x_2 + b_2^{(1)})")

        a.next_to(bias_labels[1], DOWN, buff=0.6).scale(1.33).shift(LEFT*3.5)
        b.next_to(a, RIGHT, buff=1.95).scale(1.33)

        self.play(
            TransformFromCopy(hidden_labels[0], a[:5]),
            TransformFromCopy(hidden_labels[1], b[:5]),
        )
        self.wait()

        self.play(FadeIn(a[5:8]), FadeIn(a[-1]), FadeIn(b[5:8]), FadeIn(b[-1]))
        self.wait()

        self.play(
            TransformFromCopy(w_labels[0], a[8:10]),
            TransformFromCopy(w_labels[1], a[13:15]),
            TransformFromCopy(w_labels[2], b[8:10]),
            TransformFromCopy(w_labels[3], b[13:15]),
            TransformFromCopy(input_labels[0], a[10:12]),
            TransformFromCopy(input_labels[1], a[15:17]),
            TransformFromCopy(input_labels[0], b[10:12]),
            TransformFromCopy(input_labels[1], b[15:17]),
            TransformFromCopy(bias_labels[0], a[-6:-1]),
            TransformFromCopy(bias_labels[1], b[-6:-1]),
            FadeIn(a[12:13]), FadeIn(a[17:18]), FadeIn(b[12:13]), FadeIn(b[17:18]),
            run_time=2
        )

        self.wait(2)


        pulse_stage(hidden_to_output, extra_lines=[b3_arrow], color=PURE_RED, run_time=1.5)
        self.wait(0.5)

        c = Tex(r"\hat{y} = a_1^{(2)} = f(w_5 a_1^{(1)} + w_6 a_2^{(1)} + b_1^{(2)})")
        c.next_to(b, DOWN, buff=1.0).scale(1.33).move_to(VGroup(a, b)).scale(1.15)

        self.play(
            FadeOut(a), FadeOut(b), 
            TransformFromCopy(y_hat, c[:2]),
            FadeIn(c[2]),
            TransformFromCopy(output_label, c[3:8]),
        
        )

        self.wait(2)

        self.play(
            FadeIn(c[8])
        )

        self.play(FadeIn(c[9:11]), FadeIn(c[-1])) 

        self.play(
            TransformFromCopy(w5, c[11:13]),
            TransformFromCopy(w6, c[19:21]),
            TransformFromCopy(hidden_labels[0], c[13:18]),
            TransformFromCopy(hidden_labels[1], c[21:26]),
            TransformFromCopy(bias_labels[2], c[-6:-1]),
            FadeIn(c[18]), FadeIn(c[26]),
            run_time=2
        )

        self.wait(2)
        
        d = Tex(r"\hat{y} = f(w_5 f(w_1 x_1 + w_2 x_2 + b_1^{(1)}) + w_6 f(w_3 x_1 + w_4 x_2 + b_2^{(1)}) + b_1^{(2)})").move_to(c).scale(1.12)
        self.play(ReplacementTransform(c, d), run_time=1)

        self.wait(2)

        zero_labels = []
        all_symbols = w_labels + bias_labels
        
        # Create zero versions at the same positions
        for lbl in all_symbols:
            zero_tex = Text("0.5").scale(0.9)
            zero_tex.move_to(lbl.get_center())
            zero_labels.append(zero_tex)
        
        # Group both for easier animation
        zero_group = VGroup(*zero_labels)
        original_group = VGroup(*all_symbols)
        
        # ===== Fade original labels out, fade zeros in =====
        self.play(
            FadeOut(original_group, shift=UP*0.05),
            FadeIn(zero_group, shift=UP*0.05),
            run_time=1.2
        )
        self.wait(2)
                 
        self.camera.frame.save_state()
        self.wait(2)

        self.play(Transform(d, Tex(r"\hat{y} = f(0.5 \cdot f(0.5 \cdot x_1 + 0.5 \cdot x_2 + 0.5) + 0.5 \cdot f(0.5 \cdot x_1 + 0.5 \cdot x_2 + 0.5) + 0.5)").move_to(d)))
        
        self.wait(2)

        a1 = Tex(r"a^{(1)}_1 = f(w_1 x_1 + w_2 x_2 + b^{(1)}_1)")
        a1.move_to(RIGHT*17).scale(1.85).shift(UP*0.3565)

        a2 = Tex(r"a^{(1)}_2 = f(w_3 x_1 + w_4 x_2 + b^{(1)}_2)")
        a2.next_to(a1, DOWN, buff=1.15).scale(1.85)

        self.play(
            FadeIn(VGroup(a1, a2)),
            FadeOut(VGroup(d)),
            self.camera.frame.animate.shift(RIGHT*16)
        )

        self.wait(2)


        self.play(
            Transform(a1, Tex(r"a^{(1)}_1 = f(0.5 \cdot x_1 + 0.5 \cdot x_2 + 0.5)").move_to(a1).scale(1.85)),
            Transform(a2, Tex(r"a^{(1)}_2 = f(0.5 \cdot x_1 + 0.5 \cdot x_2 + 0.5)").move_to(a2).scale(1.85)),
        )

        self.wait(2)


        a = Tex(r"\frac{\partial L}{\partial w_5} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z^{(2)}} \cdot \frac{\partial z^{(2)}}{\partial w_5}").scale(1.32)
        b = Tex(r"\frac{\partial L}{\partial w_6} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z^{(2)}} \cdot \frac{\partial z^{(2)}}{\partial w_6}").scale(1.32)
       
        a.move_to(VGroup(a1, a2)).scale(1.62).shift(UP*1.4)
        b.scale(1.62).next_to(a, DOWN, buff=0.8)

        self.play(FadeOut(VGroup(a1, a2)), FadeIn(a), FadeIn(b))

        self.wait(2)


        temp = Tex(r"\frac{\partial L}{\partial w_5} = \frac{\partial L}{\partial \hat{y}} \cdot f'(z^{(2)}) \cdot a_1^{(1)}").scale(1.32*1.52)
        temp1 = Tex(r"\frac{\partial L}{\partial w_6} = \frac{\partial L}{\partial \hat{y}} \cdot f'(z^{(2)}) \cdot a_2^{(1)}").scale(1.32*1.52)
        temp.move_to(a)
        temp1.move_to(b)
        self.play(Transform(a, temp), Transform(b, temp1))
        self.wait(2)

        rect = SurroundingRectangle(a).scale(1.1)
        rect1 = SurroundingRectangle(b).scale(1.1)

        self.play(ShowCreation(rect), ShowCreation(rect1))

        self.play(
            a[-5:].animate.set_color(RED_C),
            b[-5:].animate.set_color(RED_C),
        )

        self.wait(2)

        self.play(self.camera.frame.animate.shift(LEFT*16).scale(0.8).shift(UP*0.8))



        temp_a = Circle(stroke_width=6).move_to(w5).set_color("#ff0000").scale(0.5)
        temp_b = Circle(stroke_width=6).move_to(w6).set_color("#ff0000").scale(0.5)
        self.play(
            ShowCreation(temp_a),
            ShowCreation(temp_b),
        )

        self.wait(2)

        # ===== Fade original labels out, fade zeros in =====
        self.play(
            FadeIn(original_group, shift=UP*0.05),
            FadeOut(zero_group, shift=UP*0.05),
            run_time=1.2
        )
        self.wait(2)

        self.play(
            w_labels[4].animate.set_color(YELLOW),
            hidden_to_output[0].animate.set_color(YELLOW),
            w_labels[5].animate.set_color(YELLOW),
            hidden_to_output[1].animate.set_color(YELLOW),
            run_time=1
        )

        self.wait(2)

        self.camera.frame.save_state()


        self.wait(2)

        
        self.play(
            temp_a.animate.move_to(w_labels[0]),
            temp_b.animate.move_to(w_labels[2]),
        )


        self.play(
            w_labels[0].animate.set_color(PURPLE_C),
            weights[0].animate.set_color(PURPLE_C),
            w_labels[2].animate.set_color(PURPLE_C),
            weights[1].animate.set_color(PURPLE_C),
            run_time=1
        )
        self.wait(2)

        self.play(
            Transform(temp_a, Circle().move_to(w_labels[1]).set_color("#ff0000").scale(0.5)),
            Transform(temp_b, Circle().move_to(w_labels[3]).set_color("#ff0000").scale(0.5)),
        )

        MAROON = "#EF4713"
        self.play(
            w_labels[1].animate.set_color(MAROON),
            weights[2].animate.set_color(MAROON),
            w_labels[3].animate.set_color(MAROON),
            weights[3].animate.set_color(MAROON),
            run_time=1
        )
        self.wait(2)

        self.play(Uncreate(temp_a), Uncreate(temp_b))


        self.play(Indicate(hidden_nodes[0], color="#ff0000"), Indicate(hidden_nodes[1], color="#ff0000"), run_time=0.5)
        self.play(Indicate(hidden_nodes[0], color="#ff0000"), Indicate(hidden_nodes[1], color="#ff0000"), run_time=0.5)
        self.play(Indicate(hidden_nodes[0], color="#ff0000"), Indicate(hidden_nodes[1], color="#ff0000"), run_time=0.5)
        self.play(Indicate(hidden_nodes[0], color="#ff0000"), Indicate(hidden_nodes[1], color="#ff0000"), run_time=0.5)
        
        self.wait(2)

        self.play(FadeOut(VGroup(bias_labels, )), FadeOut(w5), FadeOut(w6), FadeOut(b1_arrow), FadeOut(b2_arrow), FadeOut(b3_arrow), FadeOut(w_labels[0]), FadeOut(w_labels[1]), FadeOut(w_labels[2]), FadeOut(w_labels[3]), )
    
        self.wait(2)

        c = hidden_nodes[0].copy()
        d = hidden_labels[0].copy()

        c.shift(DOWN*1.54)
        d.shift(DOWN*1.54)

        w1 = Line(input_nodes[0].get_center(), c.get_center(), color=GREY_B, stroke_opacity=0.9).set_color(PURPLE_B).set_z_index(-1)
        w2 = Line(input_nodes[1].get_center(), c.get_center(), color=GREY_B, stroke_opacity=0.9).set_color("#ff0000").set_z_index(-1)
        w3 = Line(c.get_center(), output_node.get_center(), color=GREY_B, stroke_opacity=0.9).set_color(YELLOW_C).set_z_index(-1)

        self.play(
            ReplacementTransform(hidden_nodes[0], c),
            ReplacementTransform(hidden_labels[0], d),
            ReplacementTransform(hidden_nodes[1], c),
            ReplacementTransform(hidden_labels[1], d),
            ReplacementTransform(weights[0], w1),
            ReplacementTransform(weights[1], w1),
            ReplacementTransform(weights[2], w2),
            ReplacementTransform(weights[3], w2),
            ReplacementTransform(hidden_to_output[0], w3),
            ReplacementTransform(hidden_to_output[1], w3)
        )


        self.wait(2)

        a = Text("Symmetry problem !", weight=BOLD)
        a.next_to(c, DOWN, buff=1.2).scale(1.65).set_color(RED_B).shift(DOWN*1.23+RIGHT*1.4)

        self.play(self.camera.frame.animate.shift(DOWN*1.16), Write(a))
        self.wait(3)
