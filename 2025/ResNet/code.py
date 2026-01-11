from manimlib import *
import numpy as np


class ResidualBlock(Scene):
    """
    Advanced visualization of Residual Blocks:
    - What is a residual block
    - F(x) + x mathematics
    - Skip connection animation
    - Why it works
    """
    
    def construct(self):
        # Color Palette - Premium aesthetic
        PRIMARY = "#E74C3C"
        SECONDARY = "#3498DB"
        SUCCESS = "#2ECC71"
        WARNING = "#F1C40F"
        ACCENT = "#9B59B6"
        ADD_COLOR = "#FDCB6E"
        DARK_BG = "#0d1117"
        PULSE_COLOR = "#FF0000"  # Bright pure red for pulse
        
        # Zoom out for better view
        self.camera.frame.scale(1.45).shift(DOWN*0.3)
        
        # ==========================================
        # STEP 1: BUILD NORMAL BLOCK (F(x))
        # ==========================================
        
        # Layout constants - GENEROUS spacing
        box_width = 5
        box_height = 1.0
        
        # Input arrow at top - goes directly into weight layer
        input_arrow_start = UP * 4
        input_arrow_end = UP * 2.75
        
        input_arrow = Arrow(
            input_arrow_start, input_arrow_end,
            buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.08
        )
        input_arrow.set_color(WHITE)
        
        # "x" label next to input arrow
        x_label = Text("x", font_size=58, weight=BOLD)
        x_label.scale(1.25)
        x_label.set_color(SECONDARY)
        x_label.next_to(input_arrow, LEFT, buff=0.4)
        
        # Weight Layer 1 (NO blue glow)
        weight1_box = RoundedRectangle(width=box_width, height=box_height, corner_radius=0.15)
        weight1_box.set_fill(ACCENT, opacity=0.95)
        weight1_box.set_stroke(WHITE, width=4)
        weight1_box.move_to(UP * 2.12)
        
        weight1_text = Text("weight layer", font_size=36, weight=BOLD)
        weight1_text.scale(1.25)
        weight1_text.set_color(WHITE)
        weight1_text.move_to(weight1_box.get_center())
        
        # ReLU 1
        relu1_box = RoundedRectangle(width=box_width, height=0.85, corner_radius=0.12)
        relu1_box.set_fill(SUCCESS, opacity=0.95)
        relu1_box.set_stroke(WHITE, width=4)
        relu1_box.move_to(UP * 0.3)
        
        relu1_text = Text("ReLU", font_size=34, weight=BOLD)
        relu1_text.scale(1.25)
        relu1_text.set_color(WHITE)
        relu1_text.move_to(relu1_box.get_center())
        
        # Arrow 1: weight1 → relu1
        arr1 = Arrow(
            weight1_box.get_bottom(), relu1_box.get_top(),
            buff=0.15, stroke_width=5, max_tip_length_to_length_ratio=0.15
        ).set_color(WHITE)
        
        # Weight Layer 2 (NO blue glow)
        weight2_box = RoundedRectangle(width=box_width, height=box_height, corner_radius=0.15)
        weight2_box.set_fill(ACCENT, opacity=0.95)
        weight2_box.set_stroke(WHITE, width=4)
        weight2_box.move_to(DOWN * 1.5)
        
        weight2_text = Text("weight layer", font_size=36, weight=BOLD)
        weight2_text.scale(1.25)
        weight2_text.set_color(WHITE)
        weight2_text.move_to(weight2_box.get_center())
        
        # Arrow 2: relu1 → weight2
        arr2 = Arrow(
            relu1_box.get_bottom(), weight2_box.get_top(),
            buff=0.15, stroke_width=5, max_tip_length_to_length_ratio=0.15
        ).set_color(WHITE)
        
        # ReLU 2 - positioned further down for better spacing
        relu2_box = RoundedRectangle(width=box_width, height=0.85, corner_radius=0.12)
        relu2_box.set_fill(SUCCESS, opacity=0.95)
        relu2_box.set_stroke(WHITE, width=4)
        relu2_box.move_to(DOWN * 3.5)
        
        relu2_text = Text("ReLU", font_size=34, weight=BOLD)
        relu2_text.scale(1.25)
        relu2_text.set_color(WHITE)
        relu2_text.move_to(relu2_box.get_center())
        
        # Arrow 3: weight2 → relu2
        arr3 = Arrow(
            weight2_box.get_bottom(), relu2_box.get_top(),
            buff=0.15, stroke_width=5, max_tip_length_to_length_ratio=0.15
        ).set_color(WHITE)
        
        # Output arrow
        output_arrow = Arrow(
            relu2_box.get_bottom(), relu2_box.get_bottom() + DOWN * 1.0,
            buff=0.1, stroke_width=5, max_tip_length_to_length_ratio=0.12
        ).set_color(WHITE)
        
        # F(x) brace on left side - shown on NORMAL block first
        fx_brace = Brace(VGroup(weight1_box, weight2_box), LEFT, buff=0.3)
        fx_brace.set_color(WARNING)
        
        fx_label = Text("F(x)", font_size=48, weight=BOLD)
        fx_label.scale(1.25)
        fx_label.set_color(WARNING)
        fx_label.next_to(fx_brace, LEFT, buff=0.25)
        
        # ANIMATE NORMAL F(x) BLOCK APPEARING
        # GrowFromCenter each block first, then all arrows at once
        # ==========================================
        
        # Show input arrow and x label
        self.play(
            GrowArrow(input_arrow),
            GrowFromCenter(x_label),
            run_time=0.6
        )
        
        # GrowFromCenter all blocks
        self.play(
            GrowFromCenter(weight1_box),
            GrowFromCenter(weight1_text),
            run_time=0.5
        )
        self.play(
            GrowFromCenter(relu1_box),
            GrowFromCenter(relu1_text),
            run_time=0.4
        )
        self.play(
            GrowFromCenter(weight2_box),
            GrowFromCenter(weight2_text),
            run_time=0.5
        )
        self.play(
            GrowFromCenter(relu2_box),
            GrowFromCenter(relu2_text),
            run_time=0.4
        )
        
        # All arrows at once
        self.play(
            GrowArrow(arr1),
            GrowArrow(arr2),
            GrowArrow(arr3),
            GrowArrow(output_arrow),
            run_time=0.6
        )

        self.wait(2)
        
        # Show F(x) label on normal block
        self.play(
            FadeIn(fx_brace),
            FadeIn(fx_label),
            run_time=0.6
        )
        
        self.wait(2)

        # ==========================================
        # STEP 2: TRANSFORM INTO RESIDUAL BLOCK
        # ==========================================
        
        # Fade out F(x) label first
        self.play(
            FadeOut(fx_brace),
            FadeOut(fx_label),
            run_time=0.8
        )
        
        # Move relu2 further down to make room for addition
        relu2_new_pos = DOWN * 6.0
        
        # Create addition circle - shifted UP a bit
        add_circle = Circle(radius=0.55)
        add_circle.set_fill(RED_B, opacity=1)
        add_circle.set_stroke(WHITE, width=5)
        add_circle.move_to(DOWN * 4.2)
        add_circle.shift(UP * 0.356)  # Shift whole circle up
        
        add_text = Text("+", font_size=56, weight=BOLD)
        add_text.scale(1.25)
        add_text.set_color(BLACK)
        add_text.move_to(add_circle.get_center())
        
        # New arrow from weight2 to addition
        arr_to_add = Arrow(
            weight2_box.get_bottom(), add_circle.get_top(),
            buff=0.15, stroke_width=5, max_tip_length_to_length_ratio=0.1
        ).set_color(WHITE)
        
        # New arrow from addition to relu2
        arr_add_to_relu = Arrow(
            add_circle.get_bottom(), relu2_new_pos + UP * 0.45,
            buff=0.15, stroke_width=5, max_tip_length_to_length_ratio=0.1
        ).set_color(WHITE)
        
        # New output arrow - straight down
        new_output_arrow = Arrow(
            relu2_new_pos + DOWN * 0.45, relu2_new_pos + DOWN * 1.5,
            buff=0.1, stroke_width=5, max_tip_length_to_length_ratio=0.1
        ).set_color(WHITE)
        
        # ==========================================
        # SYMMETRIC SKIP CONNECTION: WHITE lines
        # Branch from MIDDLE of input arrow, not the tip
        # ==========================================
        
        # Branch point - middle of input arrow (between start and end)
        skip_branch_y = (input_arrow_start[1] + input_arrow_end[1]) / 2
        skip_start = np.array([0, skip_branch_y, 0])  # On the arrow line
        
        # Go RIGHT to edge of boxes + offset
        skip_right = np.array([box_width/2 + 1.0, skip_branch_y, 0])
        # Go DOWN to addition level
        skip_down = np.array([skip_right[0], add_circle.get_center()[1], 0])
        # Go LEFT to addition circle
        skip_end = add_circle.get_right() + RIGHT * 0.05
        
        # Create single path with proper corners using VMobject
        skip_path = VMobject()
        skip_path.set_points_as_corners([skip_start, skip_right, skip_down, skip_end])
        skip_path.set_stroke(WHITE, width=5)
        
        # For animation purposes, still keep separate references
        skip_line_right = Line(skip_start, skip_right, stroke_width=5, color=WHITE)
        skip_line_down = Line(skip_right, skip_down, stroke_width=5, color=WHITE)
        skip_line_left = Line(skip_down, skip_end, stroke_width=5, color=WHITE)
        
        # Arrow tip pointing left into addition
        skip_arrow_tip = Arrow(
            skip_down + LEFT * 0.5, skip_end,
            buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.25
        ).set_color(WHITE)
        
        # Small dot at branch point
        branch_dot = Dot(radius=0.12, color=WHITE)
        branch_dot.move_to(skip_start)
        
        # "x" label on skip connection - same style as input x
        skip_x = Text("x", font_size=60, weight=BOLD)
        skip_x.scale(1.25)
        skip_x.set_color(WHITE)
        skip_x.next_to(skip_line_down, RIGHT, buff=0.3).set_color(SECONDARY)
        
        # ==========================================
        # ANIMATE THE TRANSFORMATION
        # ==========================================
        
        # Fade out old arr3 and output arrow
        self.play(
            FadeOut(arr3),
            FadeOut(output_arrow),
            self.camera.frame.animate.scale(1.2).shift(DOWN*1.3),
            run_time=0.8
        )
        
        # Move relu2 down
        self.play(
            relu2_box.animate.move_to(relu2_new_pos),
            relu2_text.animate.move_to(relu2_new_pos),
            run_time=0.8,
            rate_func=smooth
        )
        
        # Show addition circle
        self.play(
            GrowArrow(arr_to_add),
            run_time=0.4
        )
        self.play(
            FadeIn(add_circle, scale=0.8),
            Write(add_text),
            run_time=0.5
        )
        
        # Show the SYMMETRIC skip connection
        self.play(
            FadeIn(branch_dot, scale=0.5),
            run_time=0.2
        )
        
        # Draw skip path with smooth corners using single VMobject
        self.play(
            ShowCreation(skip_path),
            run_time=1.2,
            rate_func=smooth
        )
        
        # Show x label
        self.play(
            FadeIn(skip_x, shift=LEFT * 0.2),
            run_time=0.4
        )
        
        # Connect addition to relu2
        self.play(GrowArrow(arr_add_to_relu), run_time=0.4)
        
        # Show output arrow
        self.play(
            GrowArrow(new_output_arrow),
            run_time=0.3
        )

        
        # Show F(x) brace again
        fx_brace2 = Brace(VGroup(weight1_box, weight2_box), LEFT, buff=0.3)
        fx_brace2.set_color(WARNING)
        fx_label2 = Text("F(x)", font_size=48, weight=BOLD)
        fx_label2.scale(1.25)
        fx_label2.set_color(WARNING)
        fx_label2.next_to(fx_brace2, LEFT, buff=0.25)
        
        self.play(
            FadeIn(fx_brace2),
            FadeIn(fx_label2),

            run_time=0.7
        )
        
        self.wait(0.5)
        
        # ==========================================
        # SINGLE PULSE ANIMATION - BRIGHT RED
        # First through layers (F(x)), then via skip (x)
        # ==========================================
        
        # Pulse through F(x) path first - BIGGER and BRIGHTER
        pulse = Dot(radius=0.28)
        pulse.set_color(PULSE_COLOR)
        pulse.set_stroke(WHITE, width=2, opacity=0.8)  # Glow effect
        pulse.move_to(input_arrow_start + UP * 0.3)  # Start a bit above
        
        self.play(FadeIn(pulse, scale=0.3), run_time=0.2)
        
        # Move through layers
        fx_path = [
            input_arrow_end,
            weight1_box.get_center(),
            relu1_box.get_center(),
            weight2_box.get_center(),
            add_circle.get_center()
        ]
        
        for point in fx_path:
            self.play(
                pulse.animate.move_to(point),
                run_time=0.5,
                rate_func=linear
            )
        
        self.play(FadeOut(pulse, scale=0.3), run_time=0.1)
        
        self.wait(0.3)
        
        # Pulse through skip connection (x) - BIGGER and BRIGHTER
        skip_pulse = Dot(radius=0.28)
        skip_pulse.set_color(PULSE_COLOR)
        skip_pulse.set_stroke(WHITE, width=2, opacity=0.8)
        skip_pulse.move_to(skip_start)
        
        self.play(FadeIn(skip_pulse, scale=0.3), run_time=0.2)
        
        # Move through skip path
        skip_path_points = [skip_right, skip_down, add_circle.get_center()]
        
        for point in skip_path_points:
            self.play(
                skip_pulse.animate.move_to(point),
                run_time=0.6,
                rate_func=linear
            )
        
        # Simple fade out at addition - no flash needed
        self.play(FadeOut(skip_pulse, scale=0.5), run_time=0.15)
        
        # Merged particle continues to output - ENHANCED
        merged = Dot(radius=0.3)
        merged.set_color(YELLOW_C)
        merged.set_stroke(WHITE, width=2, opacity=0.8)
        merged.move_to(add_circle.get_center())
        
        self.play(FadeIn(merged, scale=0.5), run_time=0.2)
        
        # Move through relu2 to output
        self.play(
            merged.animate.move_to(relu2_box.get_center()),
            run_time=0.45,
            rate_func=linear
        )
        self.play(
            merged.animate.move_to(new_output_arrow.get_end()),
            run_time=0.4,
            rate_func=linear
        )
        
        self.play(FadeOut(merged, scale=0.3), run_time=0.1)
        
        # H(x) label - positioned BELOW the output arrow, slightly LEFT
        hx_label = Text("H(x)", font_size=48, weight=BOLD)
        hx_label.scale(1.25)
        hx_label.set_color("#FF9800")
        hx_label.next_to(new_output_arrow.get_end(), DOWN, buff=0.4)
        hx_label.shift(LEFT * 0.14)
        
        # Animate H(x) with GrowFromCenter
        self.play(
            GrowFromCenter(hx_label),
            self.camera.frame.animate.shift(DOWN*0.33).scale(1.06),
            run_time=0.5
        )
        
        self.wait(0.3)
        
        # Move camera to the right to use that space
        self.play(
            self.camera.frame.animate.shift(RIGHT * 5.7),
            run_time=0.8
        )
        
        # Final equation box - further RIGHT to avoid overlap
        eq_box = RoundedRectangle(width=8, height=1.5, corner_radius=0.2)
        eq_box.set_fill(DARK_BG, opacity=0.95)
        eq_box.set_stroke(WARNING, width=4)
        eq_box.move_to(RIGHT * 6.5 + DOWN * 2)
        eq_box.shift(RIGHT * 4.6)  # Further shift right
        eq_box.scale(1.3)
        
        eq_text = Text("H(x) = F(x) + x", font_size=40, weight=BOLD)
        eq_text.scale(1.25)
        eq_text.set_color(WHITE)
        eq_text.move_to(eq_box.get_center())
        eq_text.scale(1.3)
        
        eq_sub = Text("→ Input to next layer", font_size=38, weight=BOLD)
        eq_sub.scale(1.25)
        eq_sub.set_color(RED_B)
        eq_sub.next_to(eq_box, DOWN, buff=0.53)
        eq_sub.scale(1.3)
        
        self.play(
            FadeIn(eq_box),
            Write(eq_text),
            run_time=0.6
        )
        self.play(FadeIn(eq_sub, shift=UP * 0.2), run_time=0.4)
        
        self.wait(4)


