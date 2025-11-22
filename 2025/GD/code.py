from manimlib import *
import numpy as np

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
