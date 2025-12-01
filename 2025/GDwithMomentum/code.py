from manimlib import *
import numpy as np

class Momentum(Scene):
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

        # REQUEST: "surroudning reacnel over that formalue crate"
        rect = SurroundingRectangle(formula, color="#00ff00", buff=0.2, stroke_width=3).scale(1.08)
        self.play(ShowCreation(rect))

        # REQUEST: "wait 2 second and UNcreate"
        self.wait(2)
        self.play(Uncreate(rect))

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
            run_time=8, # Longer runtime for more steps
            rate_func=linear 
        )
        
        self.wait(3)

        self.play(FadeOut(agent), FadeOut(descent_path))


        
        alpha = 0.0288987 # Just under the limit, causes heavy, sustained oscillation
        
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
            run_time=3.3, # Longer runtime for more steps
            rate_func=linear 
        )
        
        self.wait(3)

        self.play(FadeOut(agent), FadeOut(descent_path))


        momentum_formula = Tex(
            r"v_t = \beta v_{t-1} + (1 - \beta) \frac{\partial L}{\partial \theta_t}",
            font_size=45
        ).shift(RIGHT*20+DOWN).scale(2.8)

        self.play(Write(momentum_formula), self.camera.frame.animate.shift(RIGHT*20), run_time=1)
        self.wait(2)

        rect = SurroundingRectangle(momentum_formula[:2], color="#00ff00", buff=0.2, stroke_width=6).scale(1.08)
        self.play(ShowCreation(rect))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(momentum_formula[3:8], color="#00ff00", buff=0.2, stroke_width=6).scale(1.03)))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(momentum_formula[9:], color="#00ff00", buff=0.2, stroke_width=6).scale(1.03)))
        self.wait(2)

        self.play(Uncreate(rect), self.camera.frame.animate.shift(LEFT*20), )

        rect = SurroundingRectangle(formula[-7:], color="#00ff00", buff=0.2, stroke_width=6).scale(1.016)
        self.play(ShowCreation(rect))
        self.wait(2)


        temp = Tex(r"\theta_{t+1} = \theta_t - \alpha v_t", font_size=45).scale(3.2).move_to(formula,)
        
        self.play(Transform(formula, temp), Uncreate(rect))
        self.wait(2)

        



        # ---------------------------------------------------------
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
        

        # Final Flash to emphasize success
        self.play(
            Flash(optimal_point, color=YELLOW, flash_radius=0.7),
            mom_agent.animate.scale(1.2).set_color(PURE_GREEN),
            run_time=1
        )



        
        self.wait(3)

        self.play(FadeOut(mom_agent), FadeOut(momentum_path))




        self.play(self.camera.frame.animate.shift(RIGHT*20))
        self.wait(2)

        self.play(momentum_formula.animate.shift(DOWN*1.44))

        local_points = [
            np.array([-4, -1.5, 0]),
            np.array([-3,  1.5, 0]),
            np.array([-2, -1.5, 0]),
            np.array([-1,  1.5, 0]),
            np.array([ 0,  0.0, 0]),
            np.array([ 1, -1.5, 0]),
            np.array([ 2,  1.5, 0]),
            np.array([ 3, -1.5, 0]),
            np.array([ 4,  1.5, 0]),
        ]
        
        zigzag = VMobject()
        zigzag.set_points_as_corners(local_points)
        zigzag.set_color(YELLOW)
        zigzag.set_stroke(width=5)
        
        # Place it next to the formula as requested
        zigzag.next_to(momentum_formula, UP, buff=1.5)
        
        self.play(ShowCreation(zigzag), run_time=2)
        self.wait(1)


        # ---------------------------------------------------
        # 2. Create the "Averaged" Target Zig-Zag
        # ---------------------------------------------------
        # Get the current vertices of the zigzag in its final position
        current_vertices = zigzag.get_anchors()        
        # Create new points where the vertical (y) distance is squashed.
        # We multiply the y-coordinate by a small factor (e.g., 0.2) to reduce height.
        averaged_points = []
        vertical_reduction_factor = 0.1
        
        for point in current_vertices:
            # We need to calculate the y-distance relative to the object's center 
            # for correct scaling.
            center_y = zigzag.get_center()[1]
            relative_y = point[1] - center_y
            
            scaled_y = center_y + (relative_y * vertical_reduction_factor)
            
            new_point = np.array([point[0], scaled_y, point[2]])
            averaged_points.append(new_point)
            
        target_zigzag = VMobject()
        target_zigzag.set_points_as_corners(averaged_points)
        # Change color to green to indicate the "stable/averaged" state
        target_zigzag.set_color(GREEN)
        target_zigzag.set_stroke(width=5)


        # ---------------------------------------------------
        # 3. Animate the Transformation
        # ---------------------------------------------------
        label = Text("Averaging out vertical oscillations", font_size=56, weight=BOLD).set_color(PINK)
        label.next_to(zigzag, UP, buff=0.799)

        self.play(Write(label), self.camera.frame.animate.shift(UP*1.4))
        
        self.play(
            Transform(zigzag, target_zigzag),
            label.animate.shift(DOWN*0.6),
            run_time=2,
            rate_func=smooth
        )
        self.wait(3)



        self.play(FadeOut(label), FadeOut(zigzag), self.camera.frame.animate.shift(DOWN*1.4))



        
        bias_formula = Tex(
            r"V_t^{Corrected} = \frac{v_t}{1 - \beta^t}",
            font_size=45
        ).scale(2.8)
        
        # You can position it where you need, for example:
        # bias_formula.next_to(formula, DOWN)
        self.play(momentum_formula.animate.shift(UP*3.5))

        bias_formula.next_to(momentum_formula, DOWN, buff=1.5)

        self.play(Write(bias_formula))

        rect = SurroundingRectangle(bias_formula, color="#ff0000", buff=0.2, stroke_width=6).scale(1.08)
        self.play(ShowCreation(rect))
        self.wait(2)

        self.play(Uncreate(rect))
        a = Cross(bias_formula, stroke_width=6, color="#ff0000").scale(1.2)
        self.play(ShowCreation(a))

        self.wait(2)

        self.play(FadeOut(a), FadeOut(bias_formula), )


        c = Checkmark().scale(1.2).move_to(bias_formula).set_color(GREEN).scale(7).shift(DOWN*0.4)

        self.play(ShowCreation(c), momentum_formula.animate.shift(DOWN*1.48))

        self.wait(2)

        self.camera.frame.save_state()

        self.play(FadeOut(c))


        # NEW SCENE: 1D OPTIMIZATION (GD vs MOMENTUM)
        # ---------------------------------------------------------

        # 1. Shift Camera to new workspace (RIGHT * 40)
        self.play(self.camera.frame.animate.move_to(RIGHT * 40 + UP*1.72).scale(0.9), run_time=2)
        
        # 2. Create the "Wiggly Bowl" Graph
        def bowl_function(x):
            # The +1 lifts it up, the sine adds wiggles, x^2 is the main bowl
            return 0.18 * (x)**2 + 0.4 * np.sin(2 * x) + 1.0

        # Create Axes
        axes_1d = Axes(
            x_range=[-6, 6, 1],
            y_range=[-1, 9, 1],
            width=14, 
            height=8,
            axis_config={"stroke_color": GREY_B}
        )
        axes_1d.move_to(RIGHT * 40 + UP*1.0)

        # Create the visual curve
        wiggly_curve = axes_1d.get_graph(bowl_function, stroke_width=6).set_color(BLUE_E)
        
        self.play(
            ShowCreation(axes_1d),
            ShowCreation(wiggly_curve),
            run_time=1.5
        )
        self.wait(1.5)


        # ---------------------------------------------------------
        # PART A: GRADIENT DESCENT (Step-by-Step with Slope Arrows)
        # ---------------------------------------------------------
        
        gd_label = Text("Plain Gradient Descent", font_size=60, weight=BOLD).set_color(RED)
        gd_label.to_edge(UP).shift(RIGHT*40+UP*2.8)
        self.play(Write(gd_label))

        # Start from LEFT side
        start_x_val = -5.2
        x_val = start_x_val
        learning_rate = 0.7 

        # Create the Ball
        ball = Dot(radius=0.2).set_color("#ff0000")
        start_point = axes_1d.c2p(x_val, bowl_function(x_val))
        ball.move_to(start_point)

        self.play(FadeIn(ball, scale=0.5))
        self.wait(0.5)

        # Iteration Loop for GD
        iterations = 10
        
        for i in range(iterations):
            # 1. Get Current Position
            current_point = axes_1d.c2p(x_val, bowl_function(x_val))
            
            # Calculate Gradient
            dx_small = 0.0001
            dy = bowl_function(x_val + dx_small) - bowl_function(x_val)
            slope = dy / dx_small
            
            # 2. Visual Slope Arrow
            if slope > 0:
                dir_vec = np.array([-1.0, -slope, 0])
            else:
                dir_vec = np.array([1.0, slope, 0])
            
            # Normalize and scale
            dir_vec = dir_vec / np.linalg.norm(dir_vec) * 1.5

            # FIXED: Used tip_config instead of tip_length
            slope_arrow = Arrow(
                start=current_point, 
                end=current_point + dir_vec, 
                buff=0, 
                stroke_width=5,
            ).set_color(YELLOW) 
            
            # Show arrow only if slope is visible
            if np.abs(slope) > 0.05:
                 self.play(ShowCreation(slope_arrow), run_time=0.2)
                 self.wait(0.1)
            
            # 3. Update Position
            x_val = x_val - learning_rate * slope
            new_point = axes_1d.c2p(x_val, bowl_function(x_val))
            
            # Animate Movement
            anims = [ball.animate.move_to(new_point)]
            if np.abs(slope) > 0.05:
                 anims.append(FadeOut(slope_arrow))
                 
            self.play(
                *anims,
                run_time=0.5,
                rate_func=linear
            )
            if i < 9:
                self.wait(0.2)
        
        self.play(Flash(ball, color=WHITE, flash_radius=0.5))

        self.wait(1)
        
        # Fade out GD elements
        self.play(
            FadeOut(ball), 
            FadeOut(gd_label)
        )
        self.wait(2)


        # ---------------------------------------------------------
        # PART B: MOMENTUM (Accelerated, Smooth)
        # ---------------------------------------------------------
        
        mom_label = Text("Momentum", font_size=60, weight=BOLD).set_color(GREEN_C).move_to(gd_label)
        self.play(Write(mom_label))


        # Start from LEFT side again
        x_val_mom = 5.2
        velocity = 0
        beta = 0.9
        lr_mom = 1.05

        # Create Green Ball
        ball_mom = Dot(radius=0.25).set_color(GREEN)
        start_point_mom = axes_1d.c2p(x_val_mom, bowl_function(x_val_mom))
        ball_mom.move_to(start_point_mom)
        
        self.play(FadeIn(ball_mom))

        # Pre-calculate path
        path_points_mom = [start_point_mom]
        
        sim_x = x_val_mom
        sim_v = 0
        
        for _ in range(50): 
            dx_small = 0.0001
            dy = bowl_function(sim_x + dx_small) - bowl_function(sim_x)
            slope = dy / dx_small
            
            sim_v = beta * sim_v + (1 - beta) * slope
            sim_x = sim_x - lr_mom * sim_v
            
            pt = axes_1d.c2p(sim_x, bowl_function(sim_x))
            path_points_mom.append(pt)

        # Create path
        mom_path_visual = VMobject()
        mom_path_visual.set_points_as_corners(path_points_mom)
        mom_path_visual.make_smooth() 
        
        # Animate continuous movement
        self.play(
            MoveAlongPath(ball_mom, mom_path_visual),
            run_time=8, 
            rate_func=linear 
        )
        
        self.play(Flash(ball_mom, color=WHITE, flash_radius=0.5))
        
        self.wait(3)

        self.play(FadeOut(ball_mom))

        self.wait(2)
