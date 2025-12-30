from manimlib import *
import numpy as np


class VGG16(Scene):
    
    def construct(self):

        self.camera.frame.shift(DOWN)
                
        # ==========================================
        # COLOR PALETTE
        # ==========================================
        
        INPUT_COLOR = "#4A90D9"
        
        # Block 1 - Warm Red
        CONV1_1_COLOR = "#E74C3C"
        CONV1_2_COLOR = "#C0392B"
        POOL1_COLOR = "#F39C12"
        
        # Block 2 - Purple/Violet
        CONV2_1_COLOR = "#9B59B6"
        CONV2_2_COLOR = "#8E44AD"
        POOL2_COLOR = "#1ABC9C"
        
        # Block 3 - Pink/Magenta
        CONV3_1_COLOR = "#E91E63"
        CONV3_2_COLOR = "#C2185B"
        CONV3_3_COLOR = "#AD1457"
        POOL3_COLOR = "#00BCD4"
        
        # Block 4 - Orange/Brown
        CONV4_1_COLOR = "#FF5722"
        CONV4_2_COLOR = "#E64A19"
        CONV4_3_COLOR = "#D84315"
        POOL4_COLOR = "#795548"
        
        # Block 5 - Teal/Cyan
        CONV5_1_COLOR = "#009688"
        CONV5_2_COLOR = "#00796B"
        CONV5_3_COLOR = "#00695C"
        POOL5_COLOR = "#607D8B"
        
        # FC Layers
        FC1_COLOR = "#2ECC71"
        FC2_COLOR = "#3498DB"
        OUTPUT_COLOR = "#FF9800"
        
        # ==========================================
        # TITLE SEQUENCE
        # ==========================================
        
        title = Text("VGG16", font_size=120, weight=BOLD)
        title.set_color(WHITE)
        
        subtitle = Text("Simonyan & Zisserman, 2014", font_size=42)
        subtitle.set_color(GREY_A)
        subtitle.next_to(title, DOWN, buff=0.5)
        
        subtitle2 = Text("Very Deep CNN for Large-Scale Image Recognition", font_size=32, weight=BOLD)
        subtitle2.set_color(YELLOW)
        subtitle2.next_to(subtitle, DOWN, buff=0.8)
        
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=1)
        self.play(FadeIn(subtitle2, shift=UP * 0.3), run_time=1)
        
        self.wait(2)

        
        # ==========================================
        # HELPER FUNCTIONS
        # ==========================================
        
        def create_3d_cuboid(height, width, depth, color, position=ORIGIN, cell_size=0.04):
            """Create a 3D cuboid (volume block) representation"""
            cuboid = VGroup()
            
            front = Rectangle(width=width * cell_size, height=height * cell_size)
            front.set_fill(color, opacity=0.85)
            front.set_stroke(WHITE, width=1.5)
            front.move_to(position)
            
            depth_offset_x = min(depth, 20) * cell_size * 0.4
            depth_offset_y = min(depth, 20) * cell_size * 0.25
            
            top_points = [
                front.get_corner(UL),
                front.get_corner(UR),
                front.get_corner(UR) + RIGHT * depth_offset_x + UP * depth_offset_y,
                front.get_corner(UL) + RIGHT * depth_offset_x + UP * depth_offset_y,
            ]
            top = Polygon(*top_points)
            top.set_fill(interpolate_color(color, WHITE, 0.3), opacity=0.85)
            top.set_stroke(WHITE, width=1.5)
            
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
        
        def create_nn_layer_block(num_neurons, color, position=ORIGIN, height=2.8, width=0.7):
            """Create a vertical neural network layer block with neurons inside"""
            block = VGroup()
            
            container = RoundedRectangle(
                width=width,
                height=height,
                corner_radius=0.1
            )
            container.set_fill(color, opacity=0.15)
            container.set_stroke(color, width=2.5)
            container.move_to(position)
            
            if num_neurons <= 10:
                visible_count = num_neurons
                show_ellipsis = False
            else:
                visible_count = 8
                show_ellipsis = True
            
            neurons = VGroup()
            usable_height = height - 0.4
            
            if show_ellipsis:
                top_spacing = usable_height / 10
                for i in range(4):
                    neuron = Circle(radius=0.08)
                    neuron.set_fill(color, opacity=0.9)
                    neuron.set_stroke(WHITE, width=1.5)
                    y_pos = height/2 - 0.25 - i * top_spacing
                    neuron.move_to(position + UP * y_pos)
                    neurons.add(neuron)
                
                for j in range(3):
                    dot = Dot(radius=0.04, color=WHITE)
                    dot.move_to(position + UP * (0.15 - j * 0.15))
                    neurons.add(dot)
                
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

        def create_straight_arrow(start_obj, end_obj, y_pos=0):
            """Create a perfectly horizontal arrow at specified y position"""
            start_x = start_obj.get_right()[0] + 0.1
            end_x = end_obj.get_left()[0] - 0.1
            arrow = Arrow(
                np.array([start_x, y_pos, 0]),
                np.array([end_x, y_pos, 0]),
                buff=0, stroke_width=3
            )
            arrow.set_color(WHITE)
            return arrow

        def create_conv_block_arrow_labels(arrow, num_convs, filters, kernel="3x3", stride="1", padding="1"):
            """Create labels for a conv block (multiple convs with same params)"""
            labels = VGroup()
            
            # Filter count (yellow, above arrow)
            filters_label = Text(f"{filters}", font_size=16, weight=BOLD)
            filters_label.set_color(YELLOW)
            filters_label.scale(1.2).next_to(arrow, UP, buff=0.08)
            
            # Kernel size (green)
            filter_label = Text(f"{kernel}", font_size=14)
            filter_label.set_color(GREEN_B)
            filter_label.scale(1.2).next_to(arrow, DOWN, buff=0.1)
            
            # Stride (teal)
            stride_label = Text(f"s = {stride}", font_size=14)
            stride_label.set_color(TEAL_B)
            stride_label.scale(1.2).next_to(filter_label, DOWN, buff=0.1)
            
            # Padding (blue)
            pad_label = Text(f"p = {padding}", font_size=14)
            pad_label.set_color(BLUE_B)
            pad_label.scale(1.2).next_to(stride_label, DOWN, buff=0.1)
            
            # Number of convs indicator (below padding, in parentheses)
            conv_count_label = Text(f"({num_convs} times)", font_size=13)
            conv_count_label.set_color(WHITE)
            conv_count_label.scale(1.1).next_to(pad_label, DOWN, buff=0.1)
            
            labels.add(filters_label, filter_label, stride_label, pad_label, conv_count_label)
            return labels

        def create_pool_arrow_labels(arrow, kernel="2x2", stride="2"):
            """Create labels for a pooling layer"""
            labels = VGroup()
            
            pool_label = Text("MaxPool", font_size=16, weight=BOLD)
            pool_label.set_color(YELLOW)
            pool_label.scale(1.2).next_to(arrow, UP, buff=0.08)
            
            filter_label = Text(f"{kernel}", font_size=14)
            filter_label.set_color(GREEN_B)
            filter_label.scale(1.2).next_to(arrow, DOWN, buff=0.1)
            
            stride_label = Text(f"s = {stride}", font_size=14)
            stride_label.set_color(TEAL_B)
            stride_label.scale(1.2).next_to(filter_label, DOWN, buff=0.1)
            
            labels.add(pool_label, filter_label, stride_label)
            return labels

        
        # ==========================================
        # PART 1: INPUT IMAGE (224x224x3)
        # ==========================================
        
        LAYER_SPACING = 2.5
        ARROW_Y = 0
        
        input_pos = LEFT * 8
        
        self.camera.frame.save_state()
        
        input_image = ImageMobject("cat.jpeg")
        input_image.set_height(1.1)
        input_image.move_to(input_pos)
        input_border = SurroundingRectangle(input_image, color=INPUT_COLOR, stroke_width=4, buff=0.05)
        
        input_label = Text("224x224x3", font_size=22, weight=BOLD)
        input_label.set_color(INPUT_COLOR)
        input_label.next_to(input_image, UP, buff=0.25)
        
        self.play(
            self.camera.frame.animate.scale(0.5).move_to(input_pos),
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(subtitle2),
            run_time=1.2
        )
        
        self.play(
            FadeIn(input_image, scale=0.8),
            run_time=0.8
        )
        
        self.play(
            ShowCreation(input_border),
            Write(input_label),
            run_time=0.8
        )
        
        self.wait(1)

        # ==========================================
        # BLOCK 1: 2x Conv(64, 3x3) -> 224x224x64 -> MaxPool -> 112x112x64
        # ==========================================
        
        # Conv Block 1 Output (after 2 convs)
        conv1_pos = input_pos + RIGHT * LAYER_SPACING
        
        conv1_output = create_3d_cuboid(
            height=224, width=224, depth=64,
            color=CONV1_2_COLOR, position=conv1_pos, 
            cell_size=0.005
        )
        
        conv1_out_label = Text("224x224x64", font_size=20, weight=BOLD)
        conv1_out_label.set_color(CONV1_2_COLOR)
        conv1_out_label.next_to(conv1_output, UP, buff=0.25)
        
        arrow1 = create_straight_arrow(input_border, conv1_output, ARROW_Y)
        arrow1_labels = create_conv_block_arrow_labels(arrow1, 2, 64)
        
        self.play(
            self.camera.frame.animate.move_to((input_pos + conv1_pos) / 2),
            run_time=0.75
        )
        
        self.play(GrowArrow(arrow1), run_time=0.5)
        self.play(FadeIn(arrow1_labels), run_time=0.5)
        self.wait(2)
        
        self.play(TransformFromCopy(input_border, conv1_output), run_time=0.8)
        self.play(Write(conv1_out_label), run_time=0.5)
        self.wait(0.8)

        # Pool 1
        pool1_pos = conv1_pos + RIGHT * LAYER_SPACING
        
        pool1_output = create_3d_cuboid(
            height=112, width=112, depth=64,
            color=POOL1_COLOR, position=pool1_pos, 
            cell_size=0.009
        )
        
        pool1_out_label = Text("112x112x64", font_size=20, weight=BOLD)
        pool1_out_label.set_color(POOL1_COLOR)
        pool1_out_label.next_to(pool1_output, UP, buff=0.25)
        
        arrow_p1 = create_straight_arrow(conv1_output, pool1_output, ARROW_Y)
        pool1_labels = create_pool_arrow_labels(arrow_p1)
        
        self.play(
            self.camera.frame.animate.move_to((conv1_pos + pool1_pos) / 2),
            run_time=0.75
        )
        
        self.play(GrowArrow(arrow_p1), run_time=0.4)
        self.play(FadeIn(pool1_labels), run_time=0.4)
        
        self.play(TransformFromCopy(conv1_output, pool1_output), run_time=0.8)
        self.play(Write(pool1_out_label), run_time=0.5)
        self.wait(0.6)

        # ==========================================
        # BLOCK 2: 2x Conv(128, 3x3) -> 112x112x128 -> MaxPool -> 56x56x128
        # ==========================================
        
        conv2_pos = pool1_pos + RIGHT * LAYER_SPACING
        
        conv2_output = create_3d_cuboid(
            height=112, width=112, depth=128,
            color=CONV2_2_COLOR, position=conv2_pos, 
            cell_size=0.009
        )
        
        conv2_out_label = Text("112x112x128", font_size=20, weight=BOLD)
        conv2_out_label.set_color(CONV2_2_COLOR)
        conv2_out_label.next_to(conv2_output, UP, buff=0.25)
        
        arrow2 = create_straight_arrow(pool1_output, conv2_output, ARROW_Y)
        arrow2_labels = create_conv_block_arrow_labels(arrow2, 2, 128)
        
        self.play(
            self.camera.frame.animate.move_to((pool1_pos + conv2_pos) / 2),
            run_time=0.75
        )
        
        self.play(GrowArrow(arrow2), run_time=0.4)
        self.play(FadeIn(arrow2_labels), run_time=0.4)
        self.wait(2)
        
        self.play(TransformFromCopy(pool1_output, conv2_output), run_time=0.8)
        self.play(Write(conv2_out_label), run_time=0.5)
        self.wait(0.6)

        # Pool 2
        pool2_pos = conv2_pos + RIGHT * LAYER_SPACING
        
        pool2_output = create_3d_cuboid(
            height=56, width=56, depth=128,
            color=POOL2_COLOR, position=pool2_pos, 
            cell_size=0.017
        )
        
        pool2_out_label = Text("56x56x128", font_size=20, weight=BOLD)
        pool2_out_label.set_color(POOL2_COLOR)
        pool2_out_label.next_to(pool2_output, UP, buff=0.25)
        
        arrow_p2 = create_straight_arrow(conv2_output, pool2_output, ARROW_Y)
        pool2_labels = create_pool_arrow_labels(arrow_p2)
        
        self.play(
            self.camera.frame.animate.move_to((conv2_pos + pool2_pos) / 2),
            run_time=0.75
        )
        
        self.play(GrowArrow(arrow_p2), run_time=0.4)
        self.play(FadeIn(pool2_labels), run_time=0.4)
        
        self.play(TransformFromCopy(conv2_output, pool2_output), run_time=0.8)
        self.play(Write(pool2_out_label), run_time=0.5)
        self.wait(0.6)

        # ==========================================
        # BLOCK 3: 3x Conv(256, 3x3) -> 56x56x256 -> MaxPool -> 28x28x256
        # ==========================================
        
        conv3_pos = pool2_pos + RIGHT * LAYER_SPACING
        
        conv3_output = create_3d_cuboid(
            height=56, width=56, depth=256,
            color=CONV3_3_COLOR, position=conv3_pos, 
            cell_size=0.017
        )
        
        conv3_out_label = Text("56x56x256", font_size=20, weight=BOLD)
        conv3_out_label.set_color(CONV3_3_COLOR)
        conv3_out_label.next_to(conv3_output, UP, buff=0.25)
        
        arrow3 = create_straight_arrow(pool2_output, conv3_output, ARROW_Y)
        arrow3_labels = create_conv_block_arrow_labels(arrow3, 3, 256)
        
        self.play(
            self.camera.frame.animate.move_to((pool2_pos + conv3_pos) / 2),
            run_time=0.75
        )
        
        self.play(GrowArrow(arrow3), run_time=0.4)
        self.play(FadeIn(arrow3_labels), run_time=0.4)
        self.wait(2)
        
        self.play(TransformFromCopy(pool2_output, conv3_output), run_time=0.8)
        self.play(Write(conv3_out_label), run_time=0.5)
        self.wait(0.6)

        # Pool 3
        pool3_pos = conv3_pos + RIGHT * LAYER_SPACING
        
        pool3_output = create_3d_cuboid(
            height=28, width=28, depth=256,
            color=POOL3_COLOR, position=pool3_pos, 
            cell_size=0.028
        )
        
        pool3_out_label = Text("28x28x256", font_size=20, weight=BOLD)
        pool3_out_label.set_color(POOL3_COLOR)
        pool3_out_label.next_to(pool3_output, UP, buff=0.25)
        
        arrow_p3 = create_straight_arrow(conv3_output, pool3_output, ARROW_Y)
        pool3_labels = create_pool_arrow_labels(arrow_p3)
        
        self.play(
            self.camera.frame.animate.move_to((conv3_pos + pool3_pos) / 2),
            run_time=0.75
        )
        
        self.play(GrowArrow(arrow_p3), run_time=0.4)
        self.play(FadeIn(pool3_labels), run_time=0.4)
        
        self.play(TransformFromCopy(conv3_output, pool3_output), run_time=0.8)
        self.play(Write(pool3_out_label), run_time=0.5)
        self.wait(0.6)

        # ==========================================
        # BLOCK 4: 3x Conv(512, 3x3) -> 28x28x512 -> MaxPool -> 14x14x512
        # ==========================================
        
        conv4_pos = pool3_pos + RIGHT * LAYER_SPACING
        
        conv4_output = create_3d_cuboid(
            height=28, width=28, depth=512,
            color=CONV4_3_COLOR, position=conv4_pos, 
            cell_size=0.028
        )
        
        conv4_out_label = Text("28x28x512", font_size=20, weight=BOLD)
        conv4_out_label.set_color(CONV4_3_COLOR)
        conv4_out_label.next_to(conv4_output, UP, buff=0.25)
        
        arrow4 = create_straight_arrow(pool3_output, conv4_output, ARROW_Y)
        arrow4_labels = create_conv_block_arrow_labels(arrow4, 3, 512)
        
        self.play(
            self.camera.frame.animate.move_to((pool3_pos + conv4_pos) / 2),
            run_time=0.75
        )
        
        self.play(GrowArrow(arrow4), run_time=0.4)
        self.play(FadeIn(arrow4_labels), run_time=0.4)
        self.wait(2)
        
        self.play(TransformFromCopy(pool3_output, conv4_output), run_time=0.8)
        self.play(Write(conv4_out_label), run_time=0.5)
        self.wait(0.6)

        # Pool 4
        pool4_pos = conv4_pos + RIGHT * LAYER_SPACING
        
        pool4_output = create_3d_cuboid(
            height=14, width=14, depth=512,
            color=POOL4_COLOR, position=pool4_pos, 
            cell_size=0.045
        )
        
        pool4_out_label = Text("14x14x512", font_size=20, weight=BOLD)
        pool4_out_label.set_color(POOL4_COLOR)
        pool4_out_label.next_to(pool4_output, UP, buff=0.25)
        
        arrow_p4 = create_straight_arrow(conv4_output, pool4_output, ARROW_Y)
        pool4_labels = create_pool_arrow_labels(arrow_p4)
        
        self.play(
            self.camera.frame.animate.move_to((conv4_pos + pool4_pos) / 2),
            run_time=0.75
        )
        
        self.play(GrowArrow(arrow_p4), run_time=0.4)
        self.play(FadeIn(pool4_labels), run_time=0.4)
        
        self.play(TransformFromCopy(conv4_output, pool4_output), run_time=0.8)
        self.play(Write(pool4_out_label), run_time=0.5)
        self.wait(0.6)

        # ==========================================
        # BLOCK 5: 3x Conv(512, 3x3) -> 14x14x512 -> MaxPool -> 7x7x512
        # ==========================================
        
        conv5_pos = pool4_pos + RIGHT * LAYER_SPACING
        
        conv5_output = create_3d_cuboid(
            height=14, width=14, depth=512,
            color=CONV5_3_COLOR, position=conv5_pos, 
            cell_size=0.045
        )
        
        conv5_out_label = Text("14x14x512", font_size=20, weight=BOLD)
        conv5_out_label.set_color(CONV5_3_COLOR)
        conv5_out_label.next_to(conv5_output, UP, buff=0.25)
        
        arrow5 = create_straight_arrow(pool4_output, conv5_output, ARROW_Y)
        arrow5_labels = create_conv_block_arrow_labels(arrow5, 3, 512)
        
        self.play(
            self.camera.frame.animate.move_to((pool4_pos + conv5_pos) / 2),
            run_time=0.75
        )
        
        self.play(GrowArrow(arrow5), run_time=0.4)
        self.play(FadeIn(arrow5_labels), run_time=0.4)
        self.wait(2)
        
        self.play(TransformFromCopy(pool4_output, conv5_output), run_time=0.8)
        self.play(Write(conv5_out_label), run_time=0.5)
        self.wait(0.6)

        # Pool 5
        pool5_pos = conv5_pos + RIGHT * LAYER_SPACING
        
        pool5_output = create_3d_cuboid(
            height=7, width=7, depth=512,
            color=POOL5_COLOR, position=pool5_pos, 
            cell_size=0.08
        )
        
        pool5_out_label = Text("7x7x512", font_size=20, weight=BOLD)
        pool5_out_label.set_color(POOL5_COLOR)
        pool5_out_label.next_to(pool5_output, UP, buff=0.25)
        
        arrow_p5 = create_straight_arrow(conv5_output, pool5_output, ARROW_Y)
        pool5_labels = create_pool_arrow_labels(arrow_p5)
        
        self.play(
            self.camera.frame.animate.move_to((conv5_pos + pool5_pos) / 2),
            run_time=0.75
        )
        
        self.play(GrowArrow(arrow_p5), run_time=0.4)
        self.play(FadeIn(pool5_labels), run_time=0.4)
        
        self.play(TransformFromCopy(conv5_output, pool5_output), run_time=0.8)
        self.play(Write(pool5_out_label), run_time=0.5)
        self.wait(0.6)

        # ==========================================
        # FLATTEN LAYER (25088 = 7x7x512)
        # ==========================================
        
        flatten_pos = pool5_pos + RIGHT * LAYER_SPACING
        
        flatten_block = create_nn_layer_block(25088, FC1_COLOR, flatten_pos, height=2.4, width=0.6)
        
        flatten_out_label = Text("25088", font_size=20, weight=BOLD)
        flatten_out_label.set_color(FC1_COLOR)
        flatten_out_label.next_to(flatten_block, UP, buff=0.25)
        
        arrow_flat = create_straight_arrow(pool5_output, flatten_block, ARROW_Y)
        
        flatten_label = Text("Flatten", font_size=14, weight=BOLD)
        flatten_label.set_color(YELLOW)
        flatten_label.scale(1.2).next_to(arrow_flat, UP, buff=0.08)
        
        self.play(
            self.camera.frame.animate.move_to((pool5_pos + flatten_pos) / 2),
            run_time=0.75
        )
        
        self.play(GrowArrow(arrow_flat), run_time=0.4)
        self.play(FadeIn(flatten_label), run_time=0.3)
        self.wait(2)
        
        self.play(TransformFromCopy(pool5_output, flatten_block), run_time=0.8)
        self.play(Write(flatten_out_label), run_time=0.5)
        self.wait(0.6)

        # ==========================================
        # FC1 (4096 neurons)
        # ==========================================
        
        fc1_pos = flatten_pos + RIGHT * LAYER_SPACING * 0.7
        
        fc1_block = create_nn_layer_block(4096, FC2_COLOR, fc1_pos, height=2.4, width=0.6)
        
        fc1_label = Text("4096", font_size=20, weight=BOLD)
        fc1_label.set_color(FC2_COLOR)
        fc1_label.next_to(fc1_block, UP, buff=0.25)
        
        arrow_fc1 = create_straight_arrow(flatten_block, fc1_block, ARROW_Y)
        
        relu_label1 = Text("ReLU", font_size=14, weight=BOLD)
        relu_label1.set_color(YELLOW)
        relu_label1.scale(1.1).next_to(arrow_fc1, UP, buff=0.08)
        
        dropout_label1 = Text("Dropout", font_size=12)
        dropout_label1.set_color(GREY_A)
        dropout_label1.scale(1.0).next_to(arrow_fc1, DOWN, buff=0.1)
        
        self.play(
            self.camera.frame.animate.move_to((flatten_pos + fc1_pos) / 2),
            run_time=0.75
        )
        
        self.play(GrowArrow(arrow_fc1), run_time=0.4)
        self.play(FadeIn(relu_label1), FadeIn(dropout_label1), run_time=0.3)
        
        self.play(GrowFromCenter(fc1_block), run_time=0.6)
        self.play(Write(fc1_label), run_time=0.5)
        
        # FC label below the rectangle
        fc1_type_label = Text("FC", font_size=18, weight=BOLD)
        fc1_type_label.set_color(FC2_COLOR)
        fc1_type_label.next_to(fc1_block, DOWN, buff=0.34)
        self.play(FadeIn(fc1_type_label), run_time=0.3)
        self.wait(0.6)

        # ==========================================
        # FC2 (4096 neurons)
        # ==========================================
        
        fc2_pos = fc1_pos + RIGHT * LAYER_SPACING * 0.7
        
        fc2_block = create_nn_layer_block(4096, FC2_COLOR, fc2_pos, height=2.4, width=0.6)
        
        fc2_label = Text("4096", font_size=20, weight=BOLD)
        fc2_label.set_color(FC2_COLOR)
        fc2_label.next_to(fc2_block, UP, buff=0.25)
        
        arrow_fc2 = create_straight_arrow(fc1_block, fc2_block, ARROW_Y)
        
        relu_label2 = Text("ReLU", font_size=14, weight=BOLD)
        relu_label2.set_color(YELLOW)
        relu_label2.scale(1.1).next_to(arrow_fc2, UP, buff=0.08)
        
        dropout_label2 = Text("Dropout", font_size=12)
        dropout_label2.set_color(GREY_A)
        dropout_label2.scale(1.0).next_to(arrow_fc2, DOWN, buff=0.1)
        
        self.play(
            self.camera.frame.animate.move_to((fc1_pos + fc2_pos) / 2),
            run_time=0.75
        )
        
        self.play(GrowArrow(arrow_fc2), run_time=0.4)
        self.play(FadeIn(relu_label2), FadeIn(dropout_label2), run_time=0.3)
        
        self.play(GrowFromCenter(fc2_block), run_time=0.6)
        self.play(Write(fc2_label), run_time=0.5)
        
        # FC label below the rectangle
        fc2_type_label = Text("FC", font_size=18, weight=BOLD)
        fc2_type_label.set_color(FC2_COLOR)
        fc2_type_label.next_to(fc2_block, DOWN, buff=0.34)
        self.play(FadeIn(fc2_type_label), run_time=0.3)
        self.wait(0.6)

        # ==========================================
        # OUTPUT (1000 classes)
        # ==========================================
        
        output_pos = fc2_pos + RIGHT * LAYER_SPACING * 0.7
        
        output_block = create_nn_layer_block(1000, OUTPUT_COLOR, output_pos, height=2.4, width=0.6)
        
        output_label = Text("1000", font_size=20, weight=BOLD)
        output_label.set_color(OUTPUT_COLOR)
        output_label.next_to(output_block, UP, buff=0.25)
        
        arrow_out = create_straight_arrow(fc2_block, output_block, ARROW_Y)
        
        softmax_label = Text("Softmax", font_size=14, weight=BOLD)
        softmax_label.set_color(YELLOW)
        softmax_label.scale(1.2).next_to(arrow_out, UP, buff=0.08)
        
        self.play(
            self.camera.frame.animate.move_to((fc2_pos + output_pos) / 2),
            run_time=0.75
        )
        
        self.play(GrowArrow(arrow_out), run_time=0.4)
        self.play(FadeIn(softmax_label), run_time=0.3)
        self.wait(2)
        
        self.play(GrowFromCenter(output_block), run_time=0.6)
        self.play(Write(output_label), run_time=0.5)
        self.wait(1.5)

        self.camera.frame.save_state()

        # ==========================================
        # ZOOM OUT TO SHOW FULL ARCHITECTURE
        # ==========================================
        
        arch_center = (input_pos + output_pos) / 2
        
        overview_title = Text("VGG16 Architecture (~138M Parameters)", font_size=86, weight=BOLD)
        overview_title.set_color(YELLOW)
        overview_title.to_edge(DOWN, buff=0.5).shift(RIGHT*10+DOWN*0.8)
        
        self.play(
            self.camera.frame.animate.scale(5.2).move_to(arch_center + DOWN * 0.5).shift(LEFT*0.3),
            FadeIn(overview_title),
            run_time=1.5
        )
        
        self.wait(3)

        self.camera.frame.save_state()

        # ==========================================
        # FINISHING TOUCH: SLOW PAN FROM INPUT TO OUTPUT
        # ==========================================
        
        self.play(
            self.camera.frame.animate.scale(0.2).move_to(input_pos).shift(RIGHT*1.6),
            run_time=1.5
        )
        
        self.play(
            self.camera.frame.animate.move_to(output_pos).shift(LEFT*1.99),
            run_time=35,
        )
        
        self.wait(2)
