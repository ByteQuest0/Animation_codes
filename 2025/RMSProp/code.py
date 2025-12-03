from manimlib import *
import numpy as np


class RMSProp(Scene):
    def construct(self):

        self.camera.frame.scale(1.45).shift(DOWN*0.98)
        # Define a center point higher up for the graph elements
        graph_center = UP * 1.0

        # ---------------------------------------------------------
        # 1. CREATE CONTOURS AND OPTIMAL POINT FIRST
        # ---------------------------------------------------------
        
        contours = VGroup()
        # Create concentric ellipses representing loss contours
        for i in range(1, 9):
            # Making them wider relative to height to emphasize the valley shape
            ellipse = Ellipse(width=i * 2.2, height=i * 0.65)
            ellipse.move_to(graph_center)
            
            # REQUEST: "stroke little bit thicker"
            # Increased width from 2 to 4
            ellipse.set_stroke(color=BLUE_E, width=4, opacity=0.5 + (0.5/10)*i)
            contours.add(ellipse)

        # The optimal minimum point
        optimal_point = Dot(radius=0.15)
        optimal_point.move_to(graph_center)
        # REQUEST: PURE_RED using hex code
        optimal_point.set_color("#FF0000") 
        # REQUEST: "do not write the Text Min" -> Removed label code.

        # Animate Contours and Point appearing
        self.play(
            ShowCreation(contours, lag_ratio=0.1, run_time=2),
            GrowFromCenter(optimal_point)
        )

        # ---------------------------------------------------------
        # 2. FORMULA AND SURROUNDING RECTANGLE SEQUENCE
        # ---------------------------------------------------------
        
        # The update rule formula
        formula = Tex(
            r"\theta_{t+1} = \theta_t - \alpha \frac{\partial L}{\partial \theta_t}",
            font_size=45
        )
        
        # REQUEST: "put the counter on top and the foruale below it"
        # Position formula below the lowest part of the contours
        formula.scale(2.3).next_to(contours, DOWN, buff=1.8)

        # Animate writing the formula
        self.play(Write(formula), run_time=1.5)


        # REQUEST: "do not fade out that fomraule" 
        # (Formula remains on screen for the rest of the scene)

        # ---------------------------------------------------------
        # 3. SUSTAINED UNSTABLE ZIG-ZAG ANIMATION
        # ---------------------------------------------------------
        
        # --- The Math behind the instability ---
        # To ensure it zig-zags persistently without immediately flattening,
        # we define a very steep loss landscape in one direction (Y).
        # Loss Function L = 1x^2 + 35y^2
        # Gradients: dL/dx = 2x,  dL/dy = 70y
        # The stability limit for alpha in the Y direction is 2 / 70 = ~0.0285.
        # If we pick an alpha close to or slightly above this, it will oscillate wildly.
        
        alpha = 0.027 # Just under the limit, causes heavy, sustained oscillation
        
        # Starting position relative to center
        start_offset = np.array([5.5, 1.4, 0])
        current_pos_local = start_offset

        path_points = [graph_center + current_pos_local]
        
        # REQUEST: "use Zig Zag lines not only once and then flat"
        # Increased steps to 40 to show sustained bouncing
        for _ in range(40):
            x_loc, y_loc, _ = current_pos_local
            
            # Calculate Gradients based on our hypothetical loss function
            grad_x = 2 * x_loc
            grad_y = 70 * y_loc # Extremely steep in Y

            # Update step
            new_x_loc = x_loc - alpha * grad_x
            new_y_loc = y_loc - alpha * grad_y
            
            current_pos_local = np.array([new_x_loc, new_y_loc, 0])
            
            # Add global coordinate to path list
            path_points.append(graph_center + current_pos_local)


        # Create the path VMobject
        descent_path = VMobject()
        descent_path.set_points_as_corners(path_points)
        # REQUEST: Yellow Hex Code
        descent_path.set_color("#FFFF00")
        descent_path.set_stroke(width=5) # Thicker path line

        # The moving agent dot
        agent = Dot(color="#FFFF00", radius=0.12).set_color("#FFFF00")
        agent.move_to(path_points[0])

        self.play(FadeIn(agent, scale=0.5))
        
        # Animate the movement
        # Using rate_func=linear makes the bounces look more mechanical and jerky
        self.play(
            ShowCreation(descent_path),
            MoveAlongPath(agent, descent_path),
            run_time=4.5, # Longer runtime for more steps
            rate_func=linear 
        )
        
        self.wait(3)

        self.camera.frame.save_state()

        self.play(self.camera.frame.animate.scale(1.12).shift(RIGHT*1.75))

        axes = Axes(
            x_range=[-0.5, 2.2, 1],
            y_range=[-0.5, 2.2, 1],

            axis_config={"include_tip": True, "stroke_width": 7, "include_ticks": False,},
        ).move_to(contours, RIGHT).shift(RIGHT*3.54)

        self.play(ShowCreation(axes))

        a = Text("w", weight=BOLD).set_color(ORANGE).scale(1.2).next_to(axes, LEFT).shift(RIGHT*0.28)
        b = Text("b", weight=BOLD).set_color(ORANGE).scale(1.2).next_to(axes, DOWN).shift(UP*0.29)

        self.play(Write(a), Write(b))
        self.wait(2)

        brace = Brace(descent_path, RIGHT, stroke_width=5).set_color("#ff1010").shift(RIGHT*0.23)
        self.play(GrowFromCenter(brace))
        self.wait(2)

        self.play(brace.animate.rotate(PI/2).shift(UP*1.7 + LEFT*1.64))
        self.wait(2)

        self.play(FadeOut(agent), FadeOut(descent_path), FadeOut(axes), FadeOut(a), FadeOut(b), FadeOut(brace), self.camera.frame.animate.restore())

        rect = SurroundingRectangle(formula[-7:], stroke_width=7).set_color("#00ff00").scale(1.09)
        self.play(ShowCreation(rect))
        self.wait(2)

        formula1 = Tex(
            r"\theta_{t+1} = \theta_t - \alpha g_t",
            font_size=45
        )
        
        # REQUEST: "put the counter on top and the foruale below it"
        # Position formula below the lowest part of the contours
        formula1.scale(3).next_to(formula, ORIGIN,)
        
        self.play(Uncreate(rect))
        self.play(Transform(formula, formula1))
        self.wait(2)

        a = Tex(r"v_t = \beta v_{t-1} + (1 - \beta) g_t^2", font_size=45)
        a.scale(2.3).shift(RIGHT*20+DOWN).scale(1.47)

        self.play(self.camera.frame.animate.shift(RIGHT*20), ShowCreation(a))

        self.wait(2)

        rect = SurroundingRectangle(a[:2], stroke_width=6).set_color("#00ff00").scale(1.17)
        self.play(ShowCreation(rect))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(a[3:8], stroke_width=6).set_color("#00ff00").scale(1.1)))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(a[9:], stroke_width=6).set_color("#00ff00").scale(1.1)))
        self.wait(2)

        self.play(a[-3:].animate.set_color(YELLOW))
        self.wait(2)

        temp = Tex(r"\theta_{t+1} = \theta_t - \frac{\alpha}{\sqrt{v_t}}\, g_t", font_size=45)
 
        temp.scale(2.7).move_to(formula)

        self.play(a[-3:].animate.set_color(WHITE), Uncreate(rect), self.camera.frame.animate.restore())
        self.play(Transform(formula, temp), )
        self.wait()

        rect = SurroundingRectangle(formula[-8:], stroke_width=6).set_color("#00ff00").scale(1.099)
        self.play(ShowCreation(rect))
        self.wait(2)

        self.play(Uncreate(rect))

        temp = Tex(r"\theta_{t+1} = \theta_t - \frac{\alpha}{\sqrt{v_t + \epsilon}}\, g_t", font_size=45)

        temp.scale(2.7).move_to(formula)

        self.play(Transform(formula, temp), )
        self.wait()

        self.play(formula[-3].animate.set_color(YELLOW))
        self.wait(2)


        GREEN = "#00FF00"
        # We manually define points to create the exact "Fast Horizontal, Low Vertical" look
        # UPDATED: Added more points for extra zig-zags and reduced initial vertical drop
        fake_coords_local = [
            [7.2, 0.32, 0],    # Start
            [6.2, 0, 0],   # Step 1: Big Left, smaller drop than before (-0.5 vs -0.7)
            [5.5, 0.3, 0],    # Start
            [4.2, -0.15, 0],   # Step 1: Big Left, smaller drop than before (-0.5 vs -0.7)
            [3.1, 0.25, 0],   # Step 2: Up
            [2.2, -0.15, 0],  # Step 3: Down
            [1.3, 0.15, 0],   # Step 4: Up (Added extra zig)
            [0.5, -0.05, 0],  # Step 5: Down (Added extra zag)
            [0, 0, 0]         # Hit center
        ]

        # Convert to global points
        mom_points = [graph_center + np.array(p) for p in fake_coords_local]

        # Create the Green Path
        momentum_path = VMobject()
        momentum_path.set_points_as_corners(mom_points)
        momentum_path.set_color(GREEN) 
        momentum_path.set_stroke(width=6)

        # Create the Green Agent
        mom_agent = Dot(color=GREEN, radius=0.15).set_color(GREEN)
        mom_agent.move_to(mom_points[0])

        self.play(FadeIn(mom_agent, scale=0.5))
        
        # Animate the movement showing stable convergence
        # Faster run_time to emphasize "Quick Convergence"
        self.play(
            ShowCreation(momentum_path, rate_func=linear),
            MoveAlongPath(mom_agent, momentum_path, rate_func=lambda t: min(t * 1.788, 1)),
            run_time=4, 
        )
        

        self.play(
            Flash(optimal_point, color=YELLOW, flash_radius=0.7),
            mom_agent.animate.scale(1.2).set_color(PURE_GREEN),
            a.animate.shift(RIGHT),
            run_time=1
        )


        self.wait(2)


        self.play(self.camera.frame.animate.scale(1.12).shift(RIGHT*1.75))

        axes = Axes(
            x_range=[-0.5, 2.2, 1],
            y_range=[-0.5, 2.2, 1],

            axis_config={"include_tip": True, "stroke_width": 7, "include_ticks": False,},
        ).move_to(contours, RIGHT).shift(RIGHT*3.54)

        self.play(ShowCreation(axes))

        a1 = Text("w", weight=BOLD).set_color(ORANGE).scale(1.2).next_to(axes, LEFT).shift(RIGHT*0.28)
        a2 = Text("b", weight=BOLD).set_color(ORANGE).scale(1.2).next_to(axes, DOWN).shift(UP*0.29)

        self.play(Write(a1), Write(a2))
        self.wait(2)

        self.play(FadeOut(mom_agent), FadeOut(momentum_path), FadeIn(descent_path), FadeIn(agent), )

        brace = Brace(descent_path, RIGHT, stroke_width=5).set_color("#ff1010").shift(RIGHT*0.23)
        self.play(GrowFromCenter(brace))
        self.wait(2)

        self.camera.frame.save_state()

        self.play(self.camera.frame.animate.shift(RIGHT*23),a.animate.shift(RIGHT*3.8) )
        self.wait()

        rect = SurroundingRectangle(a[-3:], stroke_width=6).set_color("#00ff00").scale(1.099)
        self.play(ShowCreation(rect))
        self.play(a[-3:].animate.set_color(YELLOW))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(a[:2], stroke_width=7).set_color("#00ff00").scale(1.27)))
        self.wait(2)    

        self.play(self.camera.frame.animate.restore(), Uncreate(rect), a[-3:].animate.set_color(WHITE))
        self.wait()

        rect1 = SurroundingRectangle(formula[-10:], stroke_width=7).set_color("#00ff00").scale(1.05)
        self.play(ShowCreation(rect1))
        self.wait(2)

        self.play(Transform(rect1, SurroundingRectangle(formula[:4], stroke_width=7).set_color("#00ff00").scale(1.15)))
        self.wait(2)
        self.play(Uncreate(rect1))

        self.play(brace.animate.rotate(PI/2).shift(UP*1.7 + LEFT*1.64).scale(0.8))
        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT*23))
        self.wait()

        rect = SurroundingRectangle(a[-3:], stroke_width=6).set_color("#00ff00").scale(1.099)
        self.play(ShowCreation(rect))
        self.play(a[-3:].animate.set_color(YELLOW))
        self.wait(2)

        self.play(self.camera.frame.animate.restore(), Uncreate(rect), a[-3:].animate.set_color(WHITE))
        self.wait()

        rect1 = SurroundingRectangle(formula[-10:], stroke_width=7).set_color("#00ff00").scale(1.05)
        self.play(ShowCreation(rect1))
        self.wait(2)

        self.play(Transform(rect1, SurroundingRectangle(formula[:4], stroke_width=7).set_color("#00ff00").scale(1.15)))
        self.wait(2)
        self.play(Uncreate(rect1), Uncreate(brace))

        self.wait(2)

