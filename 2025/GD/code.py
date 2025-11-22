from manimlib import *
import numpy as np

class GradientDescentTypesExplanations(Scene):
    def construct(self):
        # ---------------------------------------------------------
        # Part 1: The General Update Rule
        # ---------------------------------------------------------
        
        # Title for the section
        general_title = Text("The General Weight Update Rule", font_size=41, weight=BOLD)
        general_title.to_edge(UP, buff=1.0).shift(DOWN*0.8)

        # The Formula: w gets w minus alpha times gradient of J
        update_formula = Tex(
            r"w \leftarrow w - \alpha \cdot \frac{\partial J}{\partial w}",
            font_size=80
        )
        update_formula.next_to(general_title, DOWN, buff=1.5)




        # Animate Part 1
        self.play(Write(general_title))
        self.wait(0.5)
        self.play(Write(update_formula))
        self.wait(2)


        # Transition text
        transition_text = Text("The difference is in how we calculate J...", font_size=37).set_color(GREEN)
        transition_text.next_to(update_formula, DOWN, buff=1.0)
        self.play(Write(transition_text), self.camera.frame.animate.shift(DOWN*0.7))
        self.wait(1.5)

        # ---------------------------------------------------------
        # Container for changing content below the main formula
        # ---------------------------------------------------------
        content_box = VGroup()

        # ---------------------------------------------------------
        # Part 2: Batch Gradient Descent (YELLOW_C)
        # ---------------------------------------------------------
        
        batch_title = Text("1. Batch Gradient Descent", color=YELLOW_C, font_size=36).set_color(YELLOW_C)
        
        # Definition of J for Batch: Average over ALL N examples
        # Using standard summation notation
        batch_j_tex = Tex(
            r"J_{Batch} = \frac{1}{N} \sum_{i=1}^{N} L_i",
            font_size=60
        )
        batch_j_tex.set_color_by_tex("J_{Batch}", YELLOW_C)

        batch_desc = Text("Summation over ALL N data points.", font_size=34)
        
        # Iteration vs Epoch info
        # In Batch, one update step uses the whole dataset once.
        batch_epoch_info = VGroup(
            Text("Relationships:", font_size=34, weight=BOLD).set_color(ORANGE),
            Text(r"1 Update (Iteration) = 1 Epoch", font_size=30),
            Text("(An Epoch is one full pass through the dataset)", font_size=25, color=GREY_B)
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)

        # Grouping and positioning
        batch_group = VGroup(batch_title, batch_j_tex, batch_desc, batch_epoch_info)
        batch_group.arrange(DOWN, buff=0.7)
        batch_group.next_to(update_formula, DOWN, buff=1.5)

        # Animate Batch Section
        self.play(
            FadeOut(general_title),
            FadeOut(transition_text),
            FadeOut(update_formula),
            Write(batch_title), self.camera.frame.animate.shift(DOWN*5.52).scale(0.92))
        
        self.wait(0.5)
        self.play(Write(batch_j_tex))
        self.play(Write(batch_desc))
        self.wait(1)
        self.play(Write(batch_epoch_info))
        self.wait(3)


        # ---------------------------------------------------------
        # Part 3: Stochastic Gradient Descent (SGD) (PURE_RED)
        # ---------------------------------------------------------

        sgd_title = Text("2. Stochastic Gradient Descent (SGD)", color=PURE_RED, font_size=36).set_color(PURE_RED)
        
        # Definition of J for SGD: Just one random example's loss
        sgd_j_tex = Tex(
            r"J_{SGD} \approx L_i",
            font_size=60
        )
        sgd_j_tex.set_color_by_tex("J_{SGD}", PURE_RED)
        
        sgd_desc = VGroup(
            Text("Calculated on just ONE random example (i).", font_size=34),
            Text("Very noisy approximation of the true Cost.", font_size=30, color=GREY_B)
        ).arrange(DOWN, buff=0.46)

        # Iteration vs Epoch info
        # In SGD, you need N updates to see N examples.
        sgd_epoch_info = VGroup(
            Text("Relationship:", font_size=34, weight=BOLD).set_color(ORANGE),
            Text(r"N Updates (Iterations) = 1 Epoch", font_size=30),
        ).arrange(DOWN, buff=0.38, aligned_edge=LEFT)

        # Grouping
        sgd_group = VGroup(sgd_title, sgd_j_tex, sgd_desc, sgd_epoch_info)
        sgd_group.arrange(DOWN, buff=0.7)
        sgd_group.move_to(batch_group.get_center())

        # Animate Transition to SGD
        self.play(ReplacementTransform(batch_group, sgd_group))
        self.wait(3)

        # ---------------------------------------------------------
        # Part 4: Mini-Batch Gradient Descent (PURPLE)
        # ---------------------------------------------------------

        mini_title = Text("3. Mini-Batch Gradient Descent", color=PURPLE, font_size=36).set_color(PURPLE_C)
        
        # Definition of J for Mini-Batch: Average over a small batch B
        # We use 'k in B' to denote indices in the current mini-batch
        mini_j_tex = Tex(
            r"J_{MiniBatch} \approx \frac{1}{B} \sum_{k \in B} L_k",
            font_size=60
        )
        mini_j_tex.set_color_by_tex("J_{MiniBatch}", PURPLE_C)

        mini_desc = Text("Subset of size B (e.g., B=32, 64, 128...)", font_size=34)

        # Iteration vs Epoch info
        # If dataset is N=1000 and Batch B=100, it takes 10 updates to finish an epoch.
        mini_epoch_info = VGroup(
            Text("Relationship:", font_size=34, weight=BOLD).set_color(ORANGE),
            Tex(r"\frac{N}{B} \  Updates \ (Iterations) \ = \ 1 \ Epoch", font_size=50),
        ).arrange(DOWN, buff=0.42, aligned_edge=LEFT)

        # Grouping
        mini_group = VGroup(mini_title, mini_j_tex, mini_desc, mini_epoch_info)
        mini_group.arrange(DOWN, buff=0.5)
        mini_group.move_to(sgd_group.get_center())

        # Animate Transition to Mini-Batch
        self.play(ReplacementTransform(sgd_group, mini_group))
        self.wait(4)

class ConvergenceComparison(Scene):
    def construct(self):
        
        # Create axes
        axes = Axes(
            x_range=[0, 50, 5],   # Iterations
            y_range=[0, 12, 2],   # Cost J
            width=10,
            height=6,
            axis_config={
                "stroke_width": 2,
                "include_tip": True,
                "include_ticks": False,
            },
            x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
            y_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
        )
        axes.set_color(GREY_C)
        axes.to_edge(DOWN, buff=1.0)

        # Add Labels
        x_label = axes.get_x_axis_label("Iterations")
        y_label = axes.get_y_axis_label("J", edge=UP, direction=LEFT, buff=0.2)
        labels = VGroup(x_label, y_label)

        # --- LEGEND SETUP (Updated Widths) ---
        legend_box = VGroup()
        
        # Config: Text, Color, Box Width
        # I increased Batch width to 2.8 as requested
        legend_data = [
            ("Batch", TEAL, 2.8),      # Increased width
            ("SGD", RED, 2.0),
            ("Mini-Batch", GOLD, 3.2) 
        ]
        
        for text_str, color, w in legend_data:
            # Create the container rectangle with custom width
            rect = Rectangle(
                width=w, 
                height=0.8,
                fill_color=BLACK,
                fill_opacity=1,
                stroke_color=TEAL,
                stroke_width=3
            )
            
            text = Text(text_str, font_size=20, color=color)
            line = Line(LEFT, RIGHT, color=color, stroke_width=4).scale(0.5)
            
            content = VGroup(line, text).arrange(RIGHT, buff=0.2)
            content.move_to(rect.get_center())
            
            item = VGroup(rect, content)
            legend_box.add(item)

        # Arrange legend items
        legend_box.arrange(RIGHT, buff=0.64)
        legend_box.to_edge(UP, buff=0.5).shift(RIGHT*0.8)
        
        # --- INITIAL ANIMATION ---
        self.play(Write(axes), Write(labels), run_time=1.5)
        self.play(FadeIn(legend_box, shift=DOWN*0.5), run_time=1.0)
        self.wait(1)

        # ---------------------------------------------------------
        # 2. DATA GENERATION 
        # ---------------------------------------------------------
        iterations = np.linspace(0, 50, 200) 
        
        # 1. BATCH: Smooth decay
        batch_y = 10 * np.exp(-0.1 * iterations)
        batch_points = [axes.c2p(x, y) for x, y in zip(iterations, batch_y)]

        # 2. SGD: Decay + HIGH Noise
        np.random.seed(42)
        sgd_points = []
        for x, y_base in zip(iterations, batch_y):
            noise = np.random.normal(0, 1.2) * (y_base / 10 + 0.2)
            y_final = y_base + noise
            y_final = max(y_final, 0) 
            sgd_points.append(axes.c2p(x, y_final))

        # 3. MINI-BATCH: Decay + MEDIUM Noise
        np.random.seed(10)
        mini_points = []
        for x, y_base in zip(iterations, batch_y):
            noise = np.random.normal(0, 0.4) * (y_base / 10 + 0.2)
            y_final = y_base + noise
            y_final = max(y_final, 0)
            mini_points.append(axes.c2p(x, y_final))

        # ---------------------------------------------------------
        # 3. PLOTTING FUNCTION (Returns the graph object now)
        # ---------------------------------------------------------
        def plot_curve(points, color, legend_index):
            graph_path = VMobject()
            graph_path.set_points_as_corners(points)
            graph_path.set_color(color)
            graph_path.set_stroke(width=3)

            # Highlight Legend
            legend_item = legend_box[legend_index]
            self.play(
                legend_item.animate.scale(1.1).set_stroke(opacity=1),
                run_time=0.5
            )
            
            # Draw Graph
            self.play(
                ShowCreation(graph_path),
                run_time=3.5,
                rate_func=linear
            )
            
            # Un-highlight
            self.play(
                legend_item.animate.scale(1/1.1).set_stroke(opacity=0.5),
                run_time=0.5
            )
            
            return graph_path

        # ---------------------------------------------------------
        # 4. EXECUTE SEQUENCE (With FadeOuts)
        # ---------------------------------------------------------
        
        # 1. Batch (Teal)
        g1 = plot_curve(batch_points, TEAL, 0)
        self.wait(1)
        self.play(FadeOut(g1)) # Clean up before next one
        
        # 2. SGD (Red)
        g2 = plot_curve(sgd_points, RED, 1)
        self.wait(1)
        self.play(FadeOut(g2)) # Clean up before next one
        
        # 3. Mini-Batch (Gold)
        g3 = plot_curve(mini_points, GOLD, 2)
        self.wait(2)

class GradientDescentComparison(Scene):
    def construct(self):

        self.camera.frame.scale(1.08)

        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            width=8,
            height=8,
            axis_config={
                "stroke_width": 3,
                "include_tip": True,
                "include_ticks": False,
            }
        )
        axes.set_color(GREY_C)
        
        # Global Minimum (Center) - PURE GREEN
        center_point = axes.c2p(0, 0)
        minimum_dot = Dot(radius=0.15)
        minimum_dot.move_to(center_point)
        minimum_dot.set_color("#00FF00") 
        minimum_dot.set_z_index(0) 
        
        # Create Circular Contours
        contours = VGroup()
        for r in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
            circle = Circle(
                radius=r,
                stroke_width=4,
                stroke_opacity=0.8
            )
            circle.set_color(BLUE_E)
            circle.move_to(center_point)
            contours.add(circle)

        # --- INITIAL ANIMATION ---
        self.play(
            Write(axes, stroke_width=3),
            run_time=1.5
        )
        self.play(
            LaggedStart(*[ShowCreation(c) for c in contours], lag_ratio=0.1),
            GrowFromCenter(minimum_dot),
            run_time=2.0
        )
        self.wait(1)

        # ---------------------------------------------------------
        # 2. PATH GENERATION LOGIC (Fixed Bounds)
        # ---------------------------------------------------------
        start_coords = np.array([-2.5, 2.5, 0]) 
        
        def get_path_points(type="batch"):
            points = [start_coords]
            curr = start_coords.copy()
            
            # --- CONFIGURATION ---
            if type == "batch":
                steps = 6
                base_noise = 0.0
                learning_rate = 0.35 # Fast, straight
            elif type == "sgd":
                steps = 25  
                base_noise = 0.8  # High enough to zig-zag, low enough to stay on screen
                learning_rate = 0.15 # Pulls to center stronger now
            else: # mini-batch
                steps = 12 
                base_noise = 0.3 
                learning_rate = 0.25 

            initial_distance = np.linalg.norm(start_coords)

            for i in range(steps):
                # Vector pointing to center
                diff = -curr
                dist_to_center = np.linalg.norm(diff)
                
                # --- DIRECTION LOGIC ---
                if type == "batch":
                    direction = diff * learning_rate
                    noise_vec = np.array([0,0,0])
                
                else: 
                    # SGD and Mini-batch
                    direction = diff * learning_rate
                    
                    # Perpendicular vector (for zig-zag)
                    perp = np.array([-diff[1], diff[0], 0])
                    if np.linalg.norm(perp) > 0:
                        perp = perp / np.linalg.norm(perp)
                    
                    # Decay noise as we get closer
                    dist_ratio = dist_to_center / initial_distance
                    decay_factor = max(dist_ratio, 0.2) 
                    
                    local_noise = np.random.normal(0, 1) * base_noise * decay_factor
                    noise_vec = local_noise * perp
                    
                step_update = direction + noise_vec
                curr = curr + step_update
                
                # --- CRITICAL FIX: CLAMPING ---
                # This forces the point to stay inside the visible graph area
                # The graph is -4 to 4, so we clip at 3.8 to be safe.
                curr[0] = np.clip(curr[0], -3.8, 3.8)
                curr[1] = np.clip(curr[1], -3.8, 3.8)
                
                points.append(curr.copy())
            
            # Force convergence at the very end
            points[-1] = np.array([0,0,0]) 
                
            return points

        # ---------------------------------------------------------
        # 3. ANIMATION SEQUENCE
        # ---------------------------------------------------------
        def run_optimization_viz(color_to_use, point_type):
            
            raw_points = get_path_points(point_type)
            path_dots = VGroup()
            path_lines = VGroup()
            
            # Build visual elements
            for i in range(len(raw_points)):
                # Dots setup
                radius = 0.12 if i == 0 else 0.08
                dot = Dot(radius=radius)
                dot.move_to(axes.c2p(*raw_points[i]))
                dot.set_color(color_to_use)
                dot.set_z_index(10) 
                path_dots.add(dot)
                
                if i > 0:
                    line = Line(
                        axes.c2p(*raw_points[i-1]),
                        axes.c2p(*raw_points[i]),
                        stroke_width=4, 
                        stroke_opacity=0.9
                    )
                    line.set_color(color_to_use)
                    line.set_z_index(5) 
                    path_lines.add(line)

            # 1. Show Start
            self.play(FadeIn(path_dots[0]), run_time=0.5)
            
            # 2. Animate Path
            total_run_time = 4.0 # Slightly faster to keep momentum
            step_time = total_run_time / len(path_lines)
            
            for i in range(len(path_lines)):
                self.play(
                    ShowCreation(path_lines[i]),
                    FadeIn(path_dots[i+1]),
                    run_time=step_time,
                    rate_func=linear
                )
            
            # 3. Hold
            self.wait(1.0)
            
            # 4. Cleanup
            self.play(
                FadeOut(path_lines),
                FadeOut(path_dots),
                run_time=0.8
            )
            self.wait(0.2)

        # ---------------------------------------------------------
        # 4. EXECUTE SEQUENCE
        # ---------------------------------------------------------
        
        # 1. Batch GD (Teal)
        run_optimization_viz(YELLOW_C, "batch")
        
        # 2. SGD (Red) 
        np.random.seed(50) # Seed 50 gives a good zig-zag that stays bounded
        run_optimization_viz(PURE_RED, "sgd")
        
        # 3. Mini-Batch GD (Gold)
        np.random.seed(10)
        run_optimization_viz(PURPLE_C, "mini")

        self.wait(2)
