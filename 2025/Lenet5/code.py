from manimlib import *
import numpy as np


class LeNet(Scene):
    
    def construct(self):

        self.camera.frame.shift(DOWN)
                
        # ==========================================
        # COLOR PALETTE
        # ==========================================
        
        INPUT_COLOR = "#4A90D9"
        CONV1_COLOR = "#E74C3C"
        POOL1_COLOR = "#F39C12"
        CONV2_COLOR = "#9B59B6"
        POOL2_COLOR = "#1ABC9C"
        FC1_COLOR = "#3498DB"
        FC2_COLOR = "#E91E63"
        OUTPUT_COLOR = "#2ECC71"
        
        # ==========================================
        # TITLE SEQUENCE
        # ==========================================
        
        title = Text("LeNet-5", font_size=120, weight=BOLD)
        title.set_color(WHITE)
        
        subtitle = Text("Yann LeCun et al., 1998", font_size=42)
        subtitle.set_color(GREY_A)
        subtitle.next_to(title, DOWN, buff=0.5)
        
        subtitle2 = Text("The Architecture That Started It All", font_size=36, weight=BOLD)
        subtitle2.set_color(YELLOW)
        subtitle2.next_to(subtitle, DOWN, buff=0.8)
        
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=1)
        self.play(FadeIn(subtitle2, shift=UP * 0.3), run_time=1)
        
        self.wait(2)

        
        # ==========================================
        # HELPER FUNCTIONS
        # ==========================================
        
        def create_digit_four(size=32, cell_size=0.08, position=ORIGIN):
            """Create a stylized digit '4' as a pixel grid"""
            grid = VGroup()
            
            # Create the digit pattern (4 in a 32x32 grid)
            pattern = np.zeros((size, size))
            
            # Draw a stylized "4"
            # Left vertical stem (top part)
            for i in range(6, 18):
                for j in range(8, 12):
                    pattern[i, j] = 1
            
            # Horizontal bar
            for i in range(16, 20):
                for j in range(8, 24):
                    pattern[i, j] = 1
            
            # Right vertical stem (full height)
            for i in range(6, 28):
                for j in range(18, 22):
                    pattern[i, j] = 1
            
            for i in range(size):
                for j in range(size):
                    cell = Square(side_length=cell_size)
                    if pattern[i, j] > 0:
                        intensity = pattern[i, j]
                        cell.set_fill(
                            interpolate_color(BLACK, WHITE, intensity),
                            opacity=1
                        )
                    else:
                        cell.set_fill(BLACK, opacity=1)
                    cell.set_stroke(width=0)
                    cell.move_to(
                        position + 
                        RIGHT * (j - size/2) * cell_size + 
                        DOWN * (i - size/2) * cell_size
                    )
                    grid.add(cell)
            
            return grid
        
        def create_stacked_feature_maps(height, width, num_channels, color, position=ORIGIN, cell_size=0.045, depth_offset=0.12):
            """Create stacked 3D feature maps with visible layers behind each other"""
            layers = VGroup()
            
            for c in range(num_channels):
                # Create a single layer rectangle representing one channel
                layer = Rectangle(
                    width=width * cell_size,
                    height=height * cell_size
                )
                
                # Vary the color slightly for each layer
                layer_color = interpolate_color(color, WHITE, c * 0.03)
                layer.set_fill(layer_color, opacity=0.85 - c * 0.03)
                layer.set_stroke(WHITE, width=1.2)
                
                # Offset each layer diagonally (back layers go UP-RIGHT)
                offset = (num_channels - 1 - c) * depth_offset
                layer.move_to(position + RIGHT * offset + UP * offset * 0.5)
                layer.set_z_index(c)  # Front layers have higher z-index
                
                layers.add(layer)
            
            return layers
        
        def create_3d_cuboid(height, width, depth, color, position=ORIGIN, cell_size=0.04):
            """Create a 3D cuboid (volume block) representation"""
            cuboid = VGroup()
            
            # Front face
            front = Rectangle(width=width * cell_size, height=height * cell_size)
            front.set_fill(color, opacity=0.85)
            front.set_stroke(WHITE, width=1.5)
            front.move_to(position)
            
            # Depth offset for 3D effect
            depth_offset_x = depth * cell_size * 0.4
            depth_offset_y = depth * cell_size * 0.25
            
            # Top face (parallelogram)
            top_points = [
                front.get_corner(UL),
                front.get_corner(UR),
                front.get_corner(UR) + RIGHT * depth_offset_x + UP * depth_offset_y,
                front.get_corner(UL) + RIGHT * depth_offset_x + UP * depth_offset_y,
            ]
            top = Polygon(*top_points)
            top.set_fill(interpolate_color(color, WHITE, 0.3), opacity=0.85)
            top.set_stroke(WHITE, width=1.5)
            
            # Right face (parallelogram)
            right_points = [
                front.get_corner(UR),
                front.get_corner(DR),
                front.get_corner(DR) + RIGHT * depth_offset_x + UP * depth_offset_y,
                front.get_corner(UR) + RIGHT * depth_offset_x + UP * depth_offset_y,
            ]
            right = Polygon(*right_points)
            right.set_fill(interpolate_color(color, BLACK, 0.2), opacity=0.85)
            right.set_stroke(WHITE, width=1.5)
            
            cuboid.add(front, top, right)
            return cuboid
        
        def create_fc_layer(num_neurons, color, position=ORIGIN, vertical=True, spacing=0.25):
            """Create a fully connected layer visualization"""
            neurons = VGroup()
            
            for i in range(num_neurons):
                neuron = Circle(radius=0.12)
                neuron.set_fill(color, opacity=0.9)
                neuron.set_stroke(WHITE, width=2)
                
                if vertical:
                    offset = (i - (num_neurons - 1) / 2) * spacing
                    neuron.move_to(position + DOWN * offset)
                else:
                    offset = (i - (num_neurons - 1) / 2) * spacing
                    neuron.move_to(position + RIGHT * offset)
                
                neurons.add(neuron)
            
            return neurons
        
        def create_nn_layer_block(num_neurons, color, position=ORIGIN, height=2.8, width=0.7):
            """Create a vertical neural network layer block with neurons inside"""
            block = VGroup()
            
            # Container rectangle
            container = RoundedRectangle(
                width=width,
                height=height,
                corner_radius=0.1
            )
            container.set_fill(color, opacity=0.15)
            container.set_stroke(color, width=2.5)
            container.move_to(position)
            
            # Determine how many neurons to show
            if num_neurons <= 10:
                visible_count = num_neurons
                show_ellipsis = False
            else:
                visible_count = 8  # Show 4 on top, 4 on bottom
                show_ellipsis = True
            
            neurons = VGroup()
            usable_height = height - 0.4
            
            if show_ellipsis:
                # Top neurons
                top_spacing = usable_height / 10
                for i in range(4):
                    neuron = Circle(radius=0.08)
                    neuron.set_fill(color, opacity=0.9)
                    neuron.set_stroke(WHITE, width=1.5)
                    y_pos = height/2 - 0.25 - i * top_spacing
                    neuron.move_to(position + UP * y_pos)
                    neurons.add(neuron)
                
                # Ellipsis dots in the middle
                for j in range(3):
                    dot = Dot(radius=0.04, color=WHITE)
                    dot.move_to(position + UP * (0.15 - j * 0.15))
                    neurons.add(dot)
                
                # Bottom neurons
                for i in range(4):
                    neuron = Circle(radius=0.08)
                    neuron.set_fill(color, opacity=0.9)
                    neuron.set_stroke(WHITE, width=1.5)
                    y_pos = -height/2 + 0.25 + (3 - i) * top_spacing
                    neuron.move_to(position + UP * y_pos)
                    neurons.add(neuron)
            else:
                spacing = usable_height / (visible_count + 1)
                for i in range(visible_count):
                    neuron = Circle(radius=0.08)
                    neuron.set_fill(color, opacity=0.9)
                    neuron.set_stroke(WHITE, width=1.5)
                    y_pos = height/2 - 0.2 - spacing * (i + 1)
                    neuron.move_to(position + UP * y_pos)
                    neurons.add(neuron)
            
            block.add(container, neurons)
            return block
        
        def create_arrow_between(start_obj, end_obj, color=WHITE):
            """Create an arrow between two objects"""
            arrow = Arrow(
                start_obj.get_right(),
                end_obj.get_left(),
                buff=0.15,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.15
            )
            arrow.set_color(color)
            return arrow

        
        # ==========================================
        # PART 1: INPUT IMAGE (32x32x1)
        # ==========================================
        
        # Define equal spacing constants for symmetric layout
        LAYER_SPACING = 3.0  # Equal distance between all layers
        
        # Starting position (camera starts here, left of center)
        input_pos = LEFT * 6
        

        section_title = Text("Input Layer", font_size=48, weight=BOLD)
        section_title.set_color(INPUT_COLOR)
        section_title.to_edge(UP, buff=0.5)
        
        
        # Create the digit "4" input
        input_image = create_digit_four(32, 0.055, input_pos)
        
        input_border = SurroundingRectangle(input_image, color=INPUT_COLOR, stroke_width=4, buff=0.05)
        
        input_label = Text("32x32x1", font_size=26, weight=BOLD)
        input_label.set_color(INPUT_COLOR)
        input_label.next_to(input_image, DOWN, buff=0.48)

        self.camera.frame.save_state()
        
        # Animate input appearing
        self.play(
            LaggedStartMap(FadeIn, input_image, lag_ratio=0.001),
            self.camera.frame.animate.scale(0.55).shift(LEFT*6.06+UP*0.82),
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(subtitle2),
            run_time=1.5
        )
        
        self.play(
            ShowCreation(input_border),
            ShowCreation(input_label),
            run_time=1
        )
        
        self.wait(1.5)


        # ==========================================
        # PART 2: CONV1 (6 filters, 5x5, -> 28x28x6)
        # ==========================================
        

        # Conv1 position (equal spacing from input)
        conv1_pos = input_pos + RIGHT * LAYER_SPACING
        
        # Create Conv1 output - first as stacked, then transform to cuboid
        conv1_stacked = create_stacked_feature_maps(
            height=28, width=28, num_channels=6,
            color=CONV1_COLOR, position=conv1_pos, 
            cell_size=0.038, depth_offset=0.1
        )
        
        conv1_output = create_3d_cuboid(
            height=28, width=28, depth=6,
            color=CONV1_COLOR, position=conv1_pos, 
            cell_size=0.038
        )
        
        conv1_out_label = Text("28x28x6", font_size=26, weight=BOLD)
        conv1_out_label.set_color(CONV1_COLOR)
        conv1_out_label.next_to(conv1_stacked, DOWN, buff=0.48)
        
        # Create straight horizontal arrow (WHITE) - Y=0 for perfect alignment
        arrow1 = Arrow(
            np.array([input_border.get_right()[0] + 0.15, 0, 0]),
            np.array([conv1_stacked.get_left()[0] - 0.15, 0, 0]),
            buff=0, stroke_width=3
        )
        arrow1.set_color(WHITE)
        
        # Filter info labels
        filters_label1 = Text("6 Fs", font_size=20, weight=BOLD)
        filters_label1.set_color(YELLOW)
        filters_label1.next_to(arrow1, UP, buff=0.08)
        
        kernel_label1 = Text("5x5,s=1", font_size=18)
        kernel_label1.set_color(GREEN_B)
        kernel_label1.next_to(arrow1, DOWN, buff=0.08)
        
        # Pan camera to the right as we add new layer
        self.play(
            self.camera.frame.animate.shift(RIGHT * LAYER_SPACING / 2),
            GrowArrow(arrow1),
            run_time=1
        )
        self.play(
            FadeIn(filters_label1),
            FadeIn(kernel_label1),
            run_time=1
        )

        self.play(
            LaggedStartMap(FadeIn, conv1_stacked, lag_ratio=0.05),
            Write(conv1_out_label),
            run_time=1
        )
        
        self.wait(2)


        # Transform stacked to 3D cuboid
        conv1_output.move_to(conv1_stacked.get_center())
        conv1_out_label_new = conv1_out_label.copy()
        conv1_out_label_new.next_to(conv1_output, DOWN, buff=0.48)
        
        self.play(
            ReplacementTransform(conv1_stacked, conv1_output),
            Transform(conv1_out_label, conv1_out_label_new),
            run_time=1
        )

        self.wait(2)
        
        # ==========================================
        # PART 3: POOL1 (2x2, stride 2 -> 14x14x6)
        # ==========================================
        

        # Pool1 position (equal spacing from conv1)
        pool1_pos = conv1_pos + RIGHT * LAYER_SPACING
        
        # Create Pool1 output - stacked then cuboid
        pool1_stacked = create_stacked_feature_maps(
            height=14, width=14, num_channels=6,
            color=POOL1_COLOR, position=pool1_pos, 
            cell_size=0.042, depth_offset=0.1
        )
        
        pool1_output = create_3d_cuboid(
            height=14, width=14, depth=6,
            color=POOL1_COLOR, position=pool1_pos, 
            cell_size=0.042
        )
        
        pool1_out_label = Text("14x14x6", font_size=26, weight=BOLD)
        pool1_out_label.set_color(POOL1_COLOR)
        pool1_out_label.next_to(pool1_stacked, DOWN, buff=0.48)
        
        # Create straight horizontal arrow - Y=0 for perfect alignment
        arrow2 = Arrow(
            np.array([conv1_output.get_right()[0] + 0.15, 0, 0]),
            np.array([pool1_stacked.get_left()[0] - 0.15, 0, 0]),
            buff=0, stroke_width=3
        )
        arrow2.set_color(WHITE)
        
        # Arrow labels
        pool_label2 = Text("Pool", font_size=20, weight=BOLD)
        pool_label2.set_color(YELLOW)
        pool_label2.next_to(arrow2, UP, buff=0.08)
        
        stride_label2 = Text("2x2,s=2", font_size=18)
        stride_label2.set_color(GREEN_B)
        stride_label2.next_to(arrow2, DOWN, buff=0.08)
        
        # Pan camera
        self.play(
            self.camera.frame.animate.shift(RIGHT * LAYER_SPACING / 2).shift(RIGHT * LAYER_SPACING / 2),
            GrowArrow(arrow2),
            run_time=0.9
        )

        self.play(
            FadeIn(pool_label2),
            FadeIn(stride_label2),)

        self.wait(2)
        
        self.play(
            LaggedStartMap(FadeIn, pool1_stacked, lag_ratio=0.05),
            Write(pool1_out_label),

            run_time=0.8
        )
        
        self.wait(2)
        
        # Transform stacked to cuboid
        pool1_output.move_to(pool1_stacked.get_center())
        pool1_out_label_new = pool1_out_label.copy()
        pool1_out_label_new.next_to(pool1_output, DOWN, buff=0.48)
        
        self.play(
            ReplacementTransform(pool1_stacked, pool1_output),
            Transform(pool1_out_label, pool1_out_label_new),
            run_time=1
        )

        self.wait(2)
        
        # ==========================================
        # PART 4: CONV2 (16 filters, 5x5 -> 10x10x16)
        # ==========================================
        

        # Conv2 position
        conv2_pos = pool1_pos + RIGHT * LAYER_SPACING
        
        # Create Conv2 output
        conv2_stacked = create_stacked_feature_maps(
            height=10, width=10, num_channels=16,
            color=CONV2_COLOR, position=conv2_pos, 
            cell_size=0.048, depth_offset=0.06
        )
        
        conv2_output = create_3d_cuboid(
            height=10, width=10, depth=16,
            color=CONV2_COLOR, position=conv2_pos, 
            cell_size=0.048
        )
        
        conv2_out_label = Text("10x10x16", font_size=26, weight=BOLD)
        conv2_out_label.set_color(CONV2_COLOR)
        conv2_out_label.next_to(conv2_stacked, DOWN, buff=0.48)
        
        # Straight horizontal arrow - Y=0 for perfect alignment
        arrow3 = Arrow(
            np.array([pool1_output.get_right()[0] + 0.15, 0, 0]),
            np.array([conv2_stacked.get_left()[0] - 0.15, 0, 0]),
            buff=0, stroke_width=3
        )
        arrow3.set_color(WHITE)
        
        # Arrow labels
        filters_label3 = Text("16 Fs", font_size=20, weight=BOLD)
        filters_label3.set_color(YELLOW)
        filters_label3.next_to(arrow3, UP, buff=0.08)
        
        kernel_label3 = Text("5x5, s=1", font_size=18)
        kernel_label3.set_color(GREEN_B)
        kernel_label3.next_to(arrow3, DOWN, buff=0.08)
        
        # Pan camera
        self.play(
            self.camera.frame.animate.shift(RIGHT * LAYER_SPACING / 2).shift(RIGHT * LAYER_SPACING / 1.2),
            GrowArrow(arrow3),
            run_time=0.9
        )

        self.play(
            FadeIn(filters_label3),
            FadeIn(kernel_label3),)
        
        self.play(
            LaggedStartMap(FadeIn, conv2_stacked, lag_ratio=0.03),
            Write(conv2_out_label),
            run_time=0.8
        )
        
        self.wait(2)
        
        # Transform to cuboid
        conv2_output.move_to(conv2_stacked.get_center())
        conv2_out_label_new = conv2_out_label.copy()
        conv2_out_label_new.next_to(conv2_output, DOWN, buff=0.48)
        
        self.play(
            ReplacementTransform(conv2_stacked, conv2_output),
            Transform(conv2_out_label, conv2_out_label_new),
            run_time=0.8
        )

        self.wait(2)

        
        # ==========================================
        # PART 5: POOL2 (2x2, stride 2 -> 5x5x16)
        # ==========================================
        
        # Pool2 position
        pool2_pos = conv2_pos + RIGHT * LAYER_SPACING
        
        # Create Pool2 output
        pool2_stacked = create_stacked_feature_maps(
            height=5, width=5, num_channels=16,
            color=POOL2_COLOR, position=pool2_pos, 
            cell_size=0.065, depth_offset=0.05
        )
        
        pool2_output = create_3d_cuboid(
            height=5, width=5, depth=16,
            color=POOL2_COLOR, position=pool2_pos, 
            cell_size=0.065
        )
        
        pool2_out_label = Text("5x5x16", font_size=26, weight=BOLD)
        pool2_out_label.set_color(POOL2_COLOR)
        pool2_out_label.next_to(pool2_stacked, DOWN, buff=0.48)
        
        # Straight horizontal arrow - Y=0 for perfect alignment
        arrow4 = Arrow(
            np.array([conv2_output.get_right()[0] + 0.15, 0, 0]),
            np.array([pool2_stacked.get_left()[0] - 0.15, 0, 0]),
            buff=0, stroke_width=3
        )
        arrow4.set_color(WHITE)
        
        # Arrow labels
        pool_label4 = Text("Pool", font_size=20, weight=BOLD)
        pool_label4.set_color(YELLOW)
        pool_label4.next_to(arrow4, UP, buff=0.08)
        
        stride_label4 = Text("2x2,s=2", font_size=18)
        stride_label4.set_color(GREEN_B)
        stride_label4.next_to(arrow4, DOWN, buff=0.08)
        
        # Pan camera
        self.play(
            self.camera.frame.animate.shift(RIGHT * LAYER_SPACING / 2),
            GrowArrow(arrow4),
            run_time=0.6
        )

        self.play(
            FadeIn(pool_label4),
            FadeIn(stride_label4),)
        
        self.play(
            LaggedStartMap(FadeIn, pool2_stacked, lag_ratio=0.03),
            run_time=0.8
        )
        
        self.wait(1)
        
        # Transform to cuboid
        pool2_output.move_to(pool2_stacked.get_center())
        pool2_out_label_new = pool2_out_label.copy()
        pool2_out_label_new.next_to(pool2_output, DOWN, buff=0.48)
        
        self.play(
            ReplacementTransform(pool2_stacked, pool2_output),
            Transform(pool2_out_label, pool2_out_label_new),
            run_time=0.8
        )
        
        self.wait(2)

        
        # ==========================================
        # PART 6: FLATTEN + FC1 (120 neurons)
        # ==========================================
        
        # FC1 position
        fc1_pos = pool2_pos + RIGHT*0.87 * LAYER_SPACING
        
        # FC1 layer
        fc1_block = create_nn_layer_block(400, GREEN, fc1_pos, height=2.4, width=0.6)
        
        fc1_label = Text("400", font_size=26, weight=BOLD)
        fc1_label.set_color(GREEN)
        fc1_label.next_to(fc1_block, DOWN, buff=0.48)
        
        # Straight horizontal arrow - Y=0 for perfect alignment
        arrow5 = Arrow(
            np.array([pool2_output.get_right()[0] + 0.15, 0, 0]),
            np.array([fc1_block.get_left()[0] - 0.15, 0, 0]),
            buff=0, stroke_width=3
        )
        arrow5.set_color(WHITE)
        
        # Arrow label
        flatten_label = Text("Flatten", font_size=20, weight=BOLD)
        flatten_label.set_color(YELLOW)
        flatten_label.next_to(arrow5, UP, buff=0.08)
        
        # Pan camera
        self.play(
            self.camera.frame.animate.shift(RIGHT*0.65 * LAYER_SPACING / 0.8),
            GrowArrow(arrow5),
            run_time=0.6
        )
        
        self.play(
            FadeIn(fc1_block, scale=0.9),
            Write(fc1_label),
            FadeIn(flatten_label),
            run_time=0.8
        )
        
        self.wait(2)

        # ==========================================
        # PART 6.5: FLATTEN + FC1 (120 neurons)
        # ==========================================
        
        # FC1 position
        fc1_2_pos = fc1_pos + RIGHT*0.55 * LAYER_SPACING
        
        # FC1 layer
        fc1_2_block = create_nn_layer_block(120, BLUE, fc1_2_pos, height=2.4, width=0.6)
        
        fc1_2_label = Text("120", font_size=26, weight=BOLD)
        fc1_2_label.set_color(BLUE)
        fc1_2_label.next_to(fc1_2_block, DOWN, buff=0.48)
        
        # Straight horizontal arrow - Y=0 for perfect alignment
        arrow5 = Arrow(
            np.array([fc1_block.get_right()[0] + 0.15, 0, 0]),
            np.array([fc1_2_block.get_left()[0] - 0.15, 0, 0]),
            buff=0, stroke_width=3
        )
        arrow5.set_color(WHITE)
        
        # Pan camera
        self.play(
            self.camera.frame.animate.shift(RIGHT * LAYER_SPACING / 0.8),
            GrowArrow(arrow5),
            run_time=0.99
        )
        
        self.play(
            FadeIn(fc1_2_block, scale=0.9),
            Write(fc1_2_label),
            run_time=0.99
        )
        
        self.wait(2)

        # ==========================================
        # PART 7: FC2 (84 neurons)
        # ==========================================
        
        # FC2 position
        fc2_pos = fc1_2_pos + RIGHT*0.788 * LAYER_SPACING * 0.7
        
        # FC2 layer
        fc2_block = create_nn_layer_block(84, BLUE, fc2_pos, height=2.4, width=0.6)
        
        fc2_label = Text("84", font_size=26, weight=BOLD)
        fc2_label.set_color(BLUE)
        fc2_label.next_to(fc2_block, DOWN, buff=0.48)
        
        # Straight horizontal arrow - Y=0 for perfect alignment
        arrow6 = Arrow(
            np.array([fc1_2_block.get_right()[0] + 0.15, 0, 0]),
            np.array([fc2_block.get_left()[0] - 0.15, 0, 0]),
            buff=0, stroke_width=3
        )
        arrow6.set_color(WHITE)
        
        # Pan camera
        self.play(
            self.camera.frame.animate.shift(RIGHT*0.6 * LAYER_SPACING * 0.44),
            GrowArrow(arrow6),
            run_time=0.77
        )
        
        self.play(
            FadeIn(fc2_block, scale=0.9),
            Write(fc2_label),
            run_time=0.8
        )
        
        self.wait(2)

        
        # ==========================================
        # PART 8: OUTPUT (10 classes)
        # ==========================================

        # Output position
        output_pos = fc2_pos + RIGHT*0.77 * LAYER_SPACING * 0.7
        
        # Output layer - taller block for better neuron spacing
        output_block = create_nn_layer_block(10, ORANGE, output_pos, height=2.49, width=0.6)
        
        output_label = Text("10", font_size=26, weight=BOLD)
        output_label.set_color(ORANGE)
        output_label.next_to(output_block, DOWN, buff=0.48)
        
        # Straight horizontal arrow - Y=0 for perfect alignment
        arrow7 = Arrow(
            np.array([fc2_block.get_right()[0] + 0.15, 0, 0]),
            np.array([output_block.get_left()[0] - 0.15, 0, 0]),
            buff=0, stroke_width=3
        )
        arrow7.set_color(WHITE)
        
        # Pan camera and show output
        self.play(
            self.camera.frame.animate.shift(RIGHT*0.43 * LAYER_SPACING * 0.6),
            GrowArrow(arrow7),
            run_time=0.99
        )
        
        self.play(
            FadeIn(output_block, scale=0.9),
            Write(output_label),
            run_time=0.8
        )
        
        self.wait(2)

        self.camera.frame.save_state()

  
        # ==========================================
        # ZOOM OUT TO SHOW FULL ARCHITECTURE
        # ==========================================
        
        # Compute center of entire architecture
        arch_center = (input_pos + output_pos) / 2
        
        overview_title = Text("LeNet-5 Architecture", font_size=88, weight=BOLD).set_color(YELLOW)
        overview_title.to_edge(DOWN, buff=0.5).shift(RIGHT*3.6+DOWN*0.86)

        
        self.play(
            self.camera.frame.animate.scale(2.86).shift(DOWN*1.1+LEFT*8.34),
            ShowCreation(overview_title),
            run_time=1.5
        )
        
        self.wait(2)
        

        a = Text("tan(h) or Sigmoid", font_size=88, weight=BOLD).set_color(MAROON_B)
        a.move_to(overview_title)

        self.play(
            FadeOut(overview_title),
            ShowCreation(a),
            run_time=0.5
        )
        self.wait(2)
        
        self.play(FadeOut(a), run_time=0.5)

        # ==========================================
        # PARAMETER CALCULATION ANIMATION
        # ==========================================
        
        # Save current camera state for restore later
        self.camera.frame.save_state()
        
        # Store all parameter texts for final transform
        param_texts = VGroup()
        total_params = 0
        
        # --- Conv1 Parameters: (5*5*1 + 1) * 6 = 156 ---
        conv1_params = (5*5*1 + 1) * 6  # 156
        total_params += conv1_params
        
        conv1_center = (input_pos + conv1_pos) / 2
        self.play(
            self.camera.frame.animate.scale(0.35).move_to(conv1_center + UP * 0.3),
            run_time=0.8
        )
        
        param_text1 = Text(f"Conv1: (5×5×1+1)×6 = {conv1_params}", font_size=18, weight=BOLD)
        param_text1.set_color(YELLOW)
        param_text1.move_to(conv1_center + UP * 0.6).shift(UP).scale(1.14)
        
        self.play(Write(param_text1), run_time=0.6)
        param_texts.add(param_text1.copy())
        self.wait(2)
        self.play(FadeOut(param_text1), run_time=0.3)
        
        # --- Pool1: No parameters ---
        pool1_center = (conv1_pos + pool1_pos) / 2
        self.play(
            self.camera.frame.animate.move_to(pool1_center + UP * 0.3),
            run_time=0.6
        )
        
        pool1_text = Text("Pool1: No params!", font_size=18, weight=BOLD)
        pool1_text.set_color(TEAL_A)
        pool1_text.move_to(pool1_center + UP * 0.6).shift(UP).scale(1.14)
        
        self.play(Write(pool1_text), run_time=0.5)
        self.wait(2)
        self.play(FadeOut(pool1_text), run_time=0.3)
        
        # --- Conv2 Parameters: (5*5*6 + 1) * 16 = 2,416 ---
        conv2_params = (5*5*6 + 1) * 16  # 2416
        total_params += conv2_params
        
        conv2_center = (pool1_pos + conv2_pos) / 2
        self.play(
            self.camera.frame.animate.move_to(conv2_center + UP * 0.3),
            run_time=0.6
        )
        
        param_text2 = Text(f"Conv2: (5×5×6+1)×16 = {conv2_params:,}", font_size=18, weight=BOLD)
        param_text2.set_color(YELLOW)
        param_text2.move_to(conv2_center + UP * 0.6).shift(UP).scale(1.14)
        
        self.play(Write(param_text2), run_time=0.6)
        param_texts.add(param_text2.copy())
        self.wait(2)
        self.play(FadeOut(param_text2), run_time=0.3)
        
        # --- Pool2: No parameters ---
        pool2_center = (conv2_pos + pool2_pos) / 2
        self.play(
            self.camera.frame.animate.move_to(pool2_center + UP * 0.3),
            run_time=0.6
        )
        
        pool2_text = Text("Pool2: No params!", font_size=18, weight=BOLD)
        pool2_text.set_color(TEAL_A)
        pool2_text.move_to(pool2_center + UP * 0.6).shift(UP).scale(1.14)
        
        self.play(Write(pool2_text), run_time=0.5)
        self.wait(2)
        self.play(FadeOut(pool2_text), run_time=0.3)
        
        # --- Flatten: No parameters (just reshaping) ---
        flatten_center = (pool2_pos + fc1_pos) / 2
        self.play(
            self.camera.frame.animate.move_to(flatten_center + UP * 0.3),
            run_time=0.6
        )
        
        flatten_text = Text("Flatten: No params!", font_size=18, weight=BOLD)
        flatten_text.set_color(TEAL_A)
        flatten_text.move_to(flatten_center + UP * 0.6).shift(UP).scale(1.14)
        
        self.play(Write(flatten_text), self.camera.frame.animate.shift(DOWN*0.26),run_time=0.5)
        self.wait(2)
        self.play(FadeOut(flatten_text), run_time=0.3)
        
        # --- FC1 (400 -> 120): (400+1)*120 = 48,120 ---
        fc1_params = (5*5*16 + 1) * 120  # 48120 (from 5x5x16=400 flattened)
        total_params += fc1_params
        
        fc1_center = (fc1_pos + fc1_2_pos) / 2
        self.play(
            self.camera.frame.animate.move_to(fc1_center + UP * 0.3).shift(DOWN*0.26),
            run_time=0.6
        )
        
        param_text3 = Text(f"(400+1)×120 = {fc1_params:,}", font_size=18, weight=BOLD)
        param_text3.set_color(YELLOW)
        param_text3.move_to(fc1_center + UP * 0.6).shift(UP).scale(1.14)
        
        self.play(Write(param_text3), run_time=0.6)
        param_texts.add(param_text3.copy())
        self.wait(2)
        self.play(FadeOut(param_text3), run_time=0.3)
        
        # --- FC2 (120 -> 84): (120+1)*84 = 10,164 ---
        fc2_params = (120 + 1) * 84  # 10164
        total_params += fc2_params
        
        fc2_center = (fc1_2_pos + fc2_pos) / 2
        self.play(
            self.camera.frame.animate.move_to(fc2_center + UP * 0.3).shift(DOWN*0.26),
            run_time=0.6
        )
        
        param_text4 = Text(f"(120+1)×84 = {fc2_params:,}", font_size=18, weight=BOLD)
        param_text4.set_color(YELLOW)
        param_text4.move_to(fc2_center + UP * 0.6).shift(UP).scale(1.14)
        
        self.play(Write(param_text4), run_time=0.6)
        param_texts.add(param_text4.copy())
        self.wait(2)
        self.play(FadeOut(param_text4), run_time=0.3)
        
        # --- Output (84 -> 10): (84+1)*10 = 850 ---
        output_params = (84 + 1) * 10  # 850
        total_params += output_params
        
        output_center = (fc2_pos + output_pos) / 2
        self.play(
            self.camera.frame.animate.move_to(output_center + UP * 0.3).shift(DOWN*0.26),
            run_time=0.6
        )
        
        param_text5 = Text(f"(84+1)×10 = {output_params}", font_size=18, weight=BOLD)
        param_text5.set_color(YELLOW)
        param_text5.move_to(output_center + UP * 0.6).shift(UP).scale(1.14)
        
        self.play(Write(param_text5), run_time=0.6)
        param_texts.add(param_text5.copy())
        self.wait(2)
        self.play(FadeOut(param_text5), run_time=0.3)
        
        # --- Restore camera and show total ---
        self.play(
            self.camera.frame.animate.restore(),
            run_time=1.2
        )
        
        self.wait(0.5)
        
        # Create total parameters text
        total_text = Text(f"Total Parameters: ~{total_params:,}", font_size=72, weight=BOLD)
        total_text.set_color(YELLOW)
        total_text.move_to(overview_title.get_center())
        
        # Show all elements as VGroup and transform to total
        all_layers = VGroup(
            input_image, input_border, input_label,
            conv1_output, conv1_out_label, arrow1, filters_label1, kernel_label1,
            pool1_output, pool1_out_label, arrow2, pool_label2, stride_label2,
            conv2_output, conv2_out_label, arrow3, filters_label3, kernel_label3,
            pool2_output, pool2_out_label, arrow4, pool_label4, stride_label4,
            fc1_block, fc1_label, arrow5, flatten_label,
            fc1_2_block, fc1_2_label,
            fc2_block, fc2_label, arrow6,
            output_block, output_label, arrow7
        )
        
        self.play(
            ShowCreation(total_text),
            run_time=1
        )
        
        self.wait(2)
        
        # Final flourish - pulse
        self.play(
            total_text.animate.scale(1.1).set_color(WHITE),
            rate_func=there_and_back,
            run_time=0.8
        )
        
        self.wait(2)
        
        self.embed()
