from manimlib import *
import numpy as np


class AlexNet(Scene):
    
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
        CONV3_COLOR = "#E91E63"
        CONV4_COLOR = "#FF5722"
        CONV5_COLOR = "#795548"
        POOL3_COLOR = "#607D8B"
        FC1_COLOR = "#2ECC71"      # GREEN
        FC2_COLOR = "#3498DB"      # BLUE
        OUTPUT_COLOR = "#FF9800"   # ORANGE
        
        # ==========================================
        # TITLE SEQUENCE
        # ==========================================
        
        title = Text("AlexNet", font_size=120, weight=BOLD)
        title.set_color(WHITE)
        
        subtitle = Text("Krizhevsky, Sutskever & Hinton, 2012", font_size=42)
        subtitle.set_color(GREY_A)
        subtitle.next_to(title, DOWN, buff=0.5)
        
        subtitle2 = Text("ImageNet Classification with Deep CNNs", font_size=36, weight=BOLD)
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

        
        # ==========================================
        # PART 1: INPUT IMAGE (227x227x3)
        # ==========================================
        
        LAYER_SPACING = 2.5
        ARROW_Y = 0  # All arrows at y=0 for straight horizontal
        
        input_pos = LEFT * 6
        
        self.camera.frame.save_state()
        
        # Use actual cat image
        input_image = ImageMobject("cat.jpeg")
        input_image.set_height(1.1)
        input_image.move_to(input_pos)
        input_border = SurroundingRectangle(input_image, color=INPUT_COLOR, stroke_width=4, buff=0.05)
        
        # Dimension label ABOVE the image
        input_label = Text("227x227x3", font_size=22, weight=BOLD)
        input_label.set_color(INPUT_COLOR)
        input_label.next_to(input_image, UP, buff=0.25)
        
        # Move camera to input position first
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
        # PART 2: CONV1 (96 filters, 11x11, stride 4 -> 55x55x96)
        # ==========================================
        
        conv1_pos = input_pos + RIGHT * LAYER_SPACING
        
        conv1_output = create_3d_cuboid(
            height=55, width=55, depth=96,
            color=CONV1_COLOR, position=conv1_pos, 
            cell_size=0.018
        )
        
        # Dimension label ABOVE the cube
        conv1_out_label = Text("55x55x96", font_size=20, weight=BOLD)
        conv1_out_label.set_color(CONV1_COLOR)
        conv1_out_label.next_to(conv1_output, UP, buff=0.25)
        
        arrow1 = create_straight_arrow(input_border, conv1_output, ARROW_Y)
        
        # Labels: filter count on top of arrow
        filters_label1 = Text("96", font_size=16, weight=BOLD)
        filters_label1.set_color(YELLOW)
        filters_label1.scale(1.2).next_to(arrow1, UP, buff=0.08)
        
        # 3 separate lines below arrow with buff=0.1
        filter_label1 = Text("11x11", font_size=14)
        filter_label1.set_color(GREEN_B)
        filter_label1.scale(1.2).next_to(arrow1, DOWN, buff=0.1)
        
        stride_label1 = Text("s = 4", font_size=14)
        stride_label1.set_color(TEAL_B)
        stride_label1.scale(1.2).next_to(filter_label1, DOWN, buff=0.1)
        
        pad_label1 = Text("p = 0", font_size=14)
        pad_label1.set_color(BLUE_B)
        pad_label1.scale(1.2).next_to(stride_label1, DOWN, buff=0.1)
        
        # Move camera to center between input and conv1
        self.play(
            self.camera.frame.animate.move_to((input_pos + conv1_pos) / 2),
            run_time=0.75
        )
        
        self.play(GrowArrow(arrow1), run_time=0.5)
        self.play(
            FadeIn(filters_label1),
            FadeIn(filter_label1),
            FadeIn(stride_label1),
            FadeIn(pad_label1),
            run_time=0.5
        )
        
        self.wait(2)
        
        self.play(
            GrowFromCenter(conv1_output),
            run_time=0.6
        )
        self.play(
            Write(conv1_out_label),
            run_time=0.5
        )
        
        self.wait(0.8)

        # ==========================================
        # PART 3: POOL1 (3x3, stride 2 -> 27x27x96)
        # ==========================================
        
        pool1_pos = conv1_pos + RIGHT * LAYER_SPACING
        
        pool1_output = create_3d_cuboid(
            height=27, width=27, depth=96,
            color=POOL1_COLOR, position=pool1_pos, 
            cell_size=0.028
        )
        
        pool1_out_label = Text("27x27x96", font_size=20, weight=BOLD)
        pool1_out_label.set_color(POOL1_COLOR)
        pool1_out_label.next_to(pool1_output, UP, buff=0.25)
        
        arrow2 = create_straight_arrow(conv1_output, pool1_output, ARROW_Y)
        
        pool_label2 = Text("MaxPool", font_size=16, weight=BOLD)
        pool_label2.set_color(YELLOW)
        pool_label2.scale(1.2).next_to(arrow2, UP, buff=0.08)
        
        filter_label2 = Text("3x3", font_size=14)
        filter_label2.set_color(GREEN_B)
        filter_label2.scale(1.2).next_to(arrow2, DOWN, buff=0.1)
        
        stride_label2 = Text("s = 2", font_size=14)
        stride_label2.set_color(TEAL_B)
        stride_label2.scale(1.2).next_to(filter_label2, DOWN, buff=0.1)
        
        pad_label2 = Text("p = 0", font_size=14)
        pad_label2.set_color(BLUE_B)
        pad_label2.scale(1.2).next_to(stride_label2, DOWN, buff=0.1)
        
        self.play(
            self.camera.frame.animate.move_to((conv1_pos + pool1_pos) / 2),
            run_time=0.75
        )
        
        self.play(GrowArrow(arrow2), run_time=0.4)
        self.play(
            FadeIn(pool_label2),
            FadeIn(filter_label2),
            FadeIn(stride_label2),
            FadeIn(pad_label2),
            run_time=0.4
        )
        
        self.wait(2)
        
        self.play(
            GrowFromCenter(pool1_output),
            run_time=0.6
        )
        self.play(
            Write(pool1_out_label),
            run_time=0.5
        )
        
        self.wait(0.6)

        # ==========================================
        # PART 4: CONV2 (256 filters, 5x5 -> 27x27x256)
        # ==========================================
        
        conv2_pos = pool1_pos + RIGHT * LAYER_SPACING
        
        conv2_output = create_3d_cuboid(
            height=27, width=27, depth=256,
            color=CONV2_COLOR, position=conv2_pos, 
            cell_size=0.028
        )
        
        conv2_out_label = Text("27x27x256", font_size=20, weight=BOLD)
        conv2_out_label.set_color(CONV2_COLOR)
        conv2_out_label.next_to(conv2_output, UP, buff=0.25)
        
        arrow3 = create_straight_arrow(pool1_output, conv2_output, ARROW_Y)
        
        filters_label3 = Text("256", font_size=16, weight=BOLD)
        filters_label3.set_color(YELLOW)
        filters_label3.scale(1.2).next_to(arrow3, UP, buff=0.08)
        
        filter_label3 = Text("5x5", font_size=14)
        filter_label3.set_color(GREEN_B)
        filter_label3.scale(1.2).next_to(arrow3, DOWN, buff=0.1)
        
        stride_label3 = Text("s = 1", font_size=14)
        stride_label3.set_color(TEAL_B)
        stride_label3.scale(1.2).next_to(filter_label3, DOWN, buff=0.1)
        
        pad_label3 = Text("p = 2", font_size=14)
        pad_label3.set_color(BLUE_B)
        pad_label3.scale(1.2).next_to(stride_label3, DOWN, buff=0.1)
        
        self.play(
            self.camera.frame.animate.move_to((pool1_pos + conv2_pos) / 2),
            run_time=0.75
        )
        
        self.play(GrowArrow(arrow3), run_time=0.4)
        self.play(
            FadeIn(filters_label3),
            FadeIn(filter_label3),
            FadeIn(stride_label3),
            FadeIn(pad_label3),
            run_time=0.4
        )
        
        self.wait(2)
        
        self.play(
            GrowFromCenter(conv2_output),
            run_time=0.6
        )
        self.play(
            Write(conv2_out_label),
            run_time=0.5
        )
        
        self.wait(0.6)

        # ==========================================
        # PART 5: POOL2 (3x3, stride 2 -> 13x13x256)
        # ==========================================
        
        pool2_pos = conv2_pos + RIGHT * LAYER_SPACING
        
        pool2_output = create_3d_cuboid(
            height=13, width=13, depth=256,
            color=POOL2_COLOR, position=pool2_pos, 
            cell_size=0.045
        )
        
        pool2_out_label = Text("13x13x256", font_size=20, weight=BOLD)
        pool2_out_label.set_color(POOL2_COLOR)
        pool2_out_label.next_to(pool2_output, UP, buff=0.25)
        
        arrow4 = create_straight_arrow(conv2_output, pool2_output, ARROW_Y)
        
        pool_label4 = Text("MaxPool", font_size=16, weight=BOLD)
        pool_label4.set_color(YELLOW)
        pool_label4.scale(1.2).next_to(arrow4, UP, buff=0.08)
        
        filter_label4 = Text("3x3", font_size=14)
        filter_label4.set_color(GREEN_B)
        filter_label4.scale(1.2).next_to(arrow4, DOWN, buff=0.1)
        
        stride_label4 = Text("s = 2", font_size=14)
        stride_label4.set_color(TEAL_B)
        stride_label4.scale(1.2).next_to(filter_label4, DOWN, buff=0.1)
        
        pad_label4 = Text("p = 0", font_size=14)
        pad_label4.set_color(BLUE_B)
        pad_label4.scale(1.2).next_to(stride_label4, DOWN, buff=0.1)
        
        self.play(
            self.camera.frame.animate.move_to((conv2_pos + pool2_pos) / 2),
            run_time=0.75
        )
        
        self.play(GrowArrow(arrow4), run_time=0.4)
        self.play(
            FadeIn(pool_label4),
            FadeIn(filter_label4),
            FadeIn(stride_label4),
            FadeIn(pad_label4),
            run_time=0.4
        )
        
        self.wait(2)
        
        self.play(
            GrowFromCenter(pool2_output),
            run_time=0.6
        )
        self.play(
            Write(pool2_out_label),
            run_time=0.5
        )
        
        self.wait(0.6)

        # ==========================================
        # PART 6: CONV3 (384 filters, 3x3 -> 13x13x384)
        # ==========================================
        
        conv3_pos = pool2_pos + RIGHT * LAYER_SPACING
        
        conv3_output = create_3d_cuboid(
            height=13, width=13, depth=384,
            color=CONV3_COLOR, position=conv3_pos, 
            cell_size=0.045
        )
        
        conv3_out_label = Text("13x13x384", font_size=20, weight=BOLD)
        conv3_out_label.set_color(CONV3_COLOR)
        conv3_out_label.next_to(conv3_output, UP, buff=0.25)
        
        arrow5 = create_straight_arrow(pool2_output, conv3_output, ARROW_Y)
        
        filters_label5 = Text("384", font_size=16, weight=BOLD)
        filters_label5.set_color(YELLOW)
        filters_label5.scale(1.2).next_to(arrow5, UP, buff=0.08)
        
        filter_label5 = Text("3x3", font_size=14)
        filter_label5.set_color(GREEN_B)
        filter_label5.scale(1.2).next_to(arrow5, DOWN, buff=0.1)
        
        stride_label5 = Text("s = 1", font_size=14)
        stride_label5.set_color(TEAL_B)
        stride_label5.scale(1.2).next_to(filter_label5, DOWN, buff=0.1)
        
        pad_label5 = Text("p = 1", font_size=14)
        pad_label5.set_color(BLUE_B)
        pad_label5.scale(1.2).next_to(stride_label5, DOWN, buff=0.1)
        
        self.play(
            self.camera.frame.animate.move_to((pool2_pos + conv3_pos) / 2),
            run_time=0.75
        )
        
        self.play(GrowArrow(arrow5), run_time=0.4)
        self.play(
            FadeIn(filters_label5),
            FadeIn(filter_label5),
            FadeIn(stride_label5),
            FadeIn(pad_label5),
            run_time=0.4
        )
        
        self.wait(2)
        
        self.play(
            GrowFromCenter(conv3_output),
            run_time=0.6
        )
        self.play(
            Write(conv3_out_label),
            run_time=0.5
        )
        
        self.wait(0.6)

        # ==========================================
        # PART 7: CONV4 (384 filters, 3x3 -> 13x13x384)
        # ==========================================
        
        conv4_pos = conv3_pos + RIGHT * LAYER_SPACING
        
        conv4_output = create_3d_cuboid(
            height=13, width=13, depth=384,
            color=CONV4_COLOR, position=conv4_pos, 
            cell_size=0.045
        )
        
        conv4_out_label = Text("13x13x384", font_size=20, weight=BOLD)
        conv4_out_label.set_color(CONV4_COLOR)
        conv4_out_label.next_to(conv4_output, UP, buff=0.25)
        
        arrow6 = create_straight_arrow(conv3_output, conv4_output, ARROW_Y)
        
        filters_label6 = Text("384", font_size=16, weight=BOLD)
        filters_label6.set_color(YELLOW)
        filters_label6.scale(1.2).next_to(arrow6, UP, buff=0.08)
        
        filter_label6 = Text("3x3", font_size=14)
        filter_label6.set_color(GREEN_B)
        filter_label6.scale(1.2).next_to(arrow6, DOWN, buff=0.1)
        
        stride_label6 = Text("s = 1", font_size=14)
        stride_label6.set_color(TEAL_B)
        stride_label6.scale(1.2).next_to(filter_label6, DOWN, buff=0.1)
        
        pad_label6 = Text("p = 1", font_size=14)
        pad_label6.set_color(BLUE_B)
        pad_label6.scale(1.2).next_to(stride_label6, DOWN, buff=0.1)
        
        self.play(
            self.camera.frame.animate.move_to((conv3_pos + conv4_pos) / 2),
            run_time=0.75
        )
        
        self.play(GrowArrow(arrow6), run_time=0.4)
        self.play(
            FadeIn(filters_label6),
            FadeIn(filter_label6),
            FadeIn(stride_label6),
            FadeIn(pad_label6),
            run_time=0.4
        )
        
        self.wait(2)
        
        self.play(
            GrowFromCenter(conv4_output),
            run_time=0.6
        )
        self.play(
            Write(conv4_out_label),
            run_time=0.5
        )
        
        self.wait(0.6)

        # ==========================================
        # PART 8: CONV5 (256 filters, 3x3 -> 13x13x256)
        # ==========================================
        
        conv5_pos = conv4_pos + RIGHT * LAYER_SPACING
        
        conv5_output = create_3d_cuboid(
            height=13, width=13, depth=256,
            color=CONV5_COLOR, position=conv5_pos, 
            cell_size=0.045
        )
        
        conv5_out_label = Text("13x13x256", font_size=20, weight=BOLD)
        conv5_out_label.set_color(CONV5_COLOR)
        conv5_out_label.next_to(conv5_output, UP, buff=0.25)
        
        arrow7 = create_straight_arrow(conv4_output, conv5_output, ARROW_Y)
        
        filters_label7 = Text("256", font_size=16, weight=BOLD)
        filters_label7.set_color(YELLOW)
        filters_label7.scale(1.2).next_to(arrow7, UP, buff=0.08)
        
        filter_label7 = Text("3x3", font_size=14)
        filter_label7.set_color(GREEN_B)
        filter_label7.scale(1.2).next_to(arrow7, DOWN, buff=0.1)
        
        stride_label7 = Text("s = 1", font_size=14)
        stride_label7.set_color(TEAL_B)
        stride_label7.scale(1.2).next_to(filter_label7, DOWN, buff=0.1)
        
        pad_label7 = Text("p = 1", font_size=14)
        pad_label7.set_color(BLUE_B)
        pad_label7.scale(1.2).next_to(stride_label7, DOWN, buff=0.1)
        
        self.play(
            self.camera.frame.animate.move_to((conv4_pos + conv5_pos) / 2),
            run_time=0.75
        )
        
        self.play(GrowArrow(arrow7), run_time=0.4)
        self.play(
            FadeIn(filters_label7),
            FadeIn(filter_label7),
            FadeIn(stride_label7),
            FadeIn(pad_label7),
            run_time=0.4
        )
        
        self.wait(2)
        
        self.play(
            GrowFromCenter(conv5_output),
            run_time=0.6
        )
        self.play(
            Write(conv5_out_label),
            run_time=0.5
        )
        
        self.wait(0.6)

        # ==========================================
        # PART 9: POOL3 (3x3, stride 2 -> 6x6x256)
        # ==========================================
        
        pool3_pos = conv5_pos + RIGHT * LAYER_SPACING
        
        pool3_output = create_3d_cuboid(
            height=6, width=6, depth=256,
            color=POOL3_COLOR, position=pool3_pos, 
            cell_size=0.08
        )
        
        pool3_out_label = Text("6x6x256", font_size=20, weight=BOLD)
        pool3_out_label.set_color(POOL3_COLOR)
        pool3_out_label.next_to(pool3_output, UP, buff=0.25)
        
        arrow8 = create_straight_arrow(conv5_output, pool3_output, ARROW_Y)
        
        pool_label8 = Text("MaxPool", font_size=16, weight=BOLD)
        pool_label8.set_color(YELLOW)
        pool_label8.scale(1.2).next_to(arrow8, UP, buff=0.08)
        
        filter_label8 = Text("3x3", font_size=14)
        filter_label8.set_color(GREEN_B)
        filter_label8.scale(1.2).next_to(arrow8, DOWN, buff=0.1)
        
        stride_label8 = Text("s = 2", font_size=14)
        stride_label8.set_color(TEAL_B)
        stride_label8.scale(1.2).next_to(filter_label8, DOWN, buff=0.1)
        
        pad_label8 = Text("p = 0", font_size=14)
        pad_label8.set_color(BLUE_B)
        pad_label8.scale(1.2).next_to(stride_label8, DOWN, buff=0.1)
        
        self.play(
            self.camera.frame.animate.move_to((conv5_pos + pool3_pos) / 2),
            run_time=0.75
        )
        
        self.play(GrowArrow(arrow8), run_time=0.4)
        self.play(
            FadeIn(pool_label8),
            FadeIn(filter_label8),
            FadeIn(stride_label8),
            FadeIn(pad_label8),
            run_time=0.4
        )
        
        self.wait(2)
        
        self.play(
            GrowFromCenter(pool3_output),
            run_time=0.6
        )
        self.play(
            Write(pool3_out_label),
            run_time=0.5
        )
        
        self.wait(0.6)

        # ==========================================
        # PART 10: FLATTEN LAYER (9216 = 6x6x256)
        # ==========================================
        
        flatten_pos = pool3_pos + RIGHT * LAYER_SPACING
        
        # Flattened vector using GREEN color
        flatten_block = create_nn_layer_block(9216, FC1_COLOR, flatten_pos, height=2.4, width=0.6)
        
        flatten_out_label = Text("9216", font_size=20, weight=BOLD)
        flatten_out_label.set_color(FC1_COLOR)
        flatten_out_label.next_to(flatten_block, UP, buff=0.25)
        
        arrow9 = create_straight_arrow(pool3_output, flatten_block, ARROW_Y)
        
        flatten_label = Text("Flatten", font_size=14, weight=BOLD)
        flatten_label.set_color(YELLOW)
        flatten_label.scale(1.2).next_to(arrow9, UP, buff=0.08)
        
        self.play(
            self.camera.frame.animate.move_to((pool3_pos + flatten_pos) / 2),
            run_time=0.75
        )
        
        self.play(GrowArrow(arrow9), run_time=0.4)
        self.play(FadeIn(flatten_label), run_time=0.3)
        
        self.wait(2)
        
        self.play(
            GrowFromCenter(flatten_block),
            run_time=0.6
        )
        self.play(
            Write(flatten_out_label),
            run_time=0.5
        )
        
        self.wait(0.6)

        # ==========================================
        # PART 11: FC1 (4096 neurons)
        # ==========================================
        
        fc1_pos = flatten_pos + RIGHT * LAYER_SPACING * 0.7
        
        fc1_block = create_nn_layer_block(4096, FC2_COLOR, fc1_pos, height=2.4, width=0.6)
        
        fc1_label = Text("4096", font_size=20, weight=BOLD)
        fc1_label.set_color(FC2_COLOR)
        fc1_label.next_to(fc1_block, UP, buff=0.25)
        
        arrow10 = create_straight_arrow(flatten_block, fc1_block, ARROW_Y)
        
        fc_label10 = Text("FC", font_size=16, weight=BOLD)
        fc_label10.set_color(YELLOW)
        fc_label10.scale(1.2).next_to(arrow10, UP, buff=0.08)
        
        self.play(
            self.camera.frame.animate.move_to((flatten_pos + fc1_pos) / 2),
            run_time=0.75
        )
        
        self.play(GrowArrow(arrow10), run_time=0.4)
        self.play(FadeIn(fc_label10), run_time=0.3)
        
        
        self.play(
            GrowFromCenter(fc1_block),
            run_time=0.6
        )
        self.play(
            Write(fc1_label),
            run_time=0.5
        )
        
        self.wait(0.6)

        # ==========================================
        # PART 12: FC2 (4096 neurons)
        # ==========================================
        
        fc2_pos = fc1_pos + RIGHT * LAYER_SPACING * 0.7
        
        fc2_block = create_nn_layer_block(4096, FC2_COLOR, fc2_pos, height=2.4, width=0.6)
        
        fc2_label = Text("4096", font_size=20, weight=BOLD)
        fc2_label.set_color(FC2_COLOR)
        fc2_label.next_to(fc2_block, UP, buff=0.25)
        
        arrow11 = create_straight_arrow(fc1_block, fc2_block, ARROW_Y)
        
        fc_label11 = Text("FC", font_size=16, weight=BOLD)
        fc_label11.set_color(YELLOW)
        fc_label11.scale(1.2).next_to(arrow11, UP, buff=0.08)
        
        self.play(
            self.camera.frame.animate.move_to((fc1_pos + fc2_pos) / 2),
            run_time=0.75
        )
        
        self.play(GrowArrow(arrow11), run_time=0.4)
        self.play(FadeIn(fc_label11), run_time=0.3)
        
        
        self.play(
            GrowFromCenter(fc2_block),
            run_time=0.6
        )
        self.play(
            Write(fc2_label),
            run_time=0.5
        )
        
        self.wait(0.6)

        # ==========================================
        # PART 13: OUTPUT (1000 classes)
        # ==========================================
        
        output_pos = fc2_pos + RIGHT * LAYER_SPACING * 0.7
        
        output_block = create_nn_layer_block(1000, OUTPUT_COLOR, output_pos, height=2.4, width=0.6)
        
        output_label = Text("1000", font_size=20, weight=BOLD)
        output_label.set_color(OUTPUT_COLOR)
        output_label.next_to(output_block, UP, buff=0.25)
        
        arrow12 = create_straight_arrow(fc2_block, output_block, ARROW_Y)
        
        softmax_label = Text("Softmax", font_size=14, weight=BOLD)
        softmax_label.set_color(YELLOW)
        softmax_label.scale(1.2).next_to(arrow12, UP, buff=0.08)
        
        self.play(
            self.camera.frame.animate.move_to((fc2_pos + output_pos) / 2),
            run_time=0.75
        )
        
        self.play(GrowArrow(arrow12), run_time=0.4)
        self.play(FadeIn(softmax_label), run_time=0.3)
        
        self.wait(2)
        
        self.play(
            GrowFromCenter(output_block),
            run_time=0.6
        )
        self.play(
            Write(output_label),
            run_time=0.5
        )
        
        self.wait(1.5)

        self.camera.frame.save_state()


        # ==========================================
        # ZOOM OUT TO SHOW FULL ARCHITECTURE
        # ==========================================
        
        arch_center = (input_pos + output_pos) / 2
        
        overview_title = Text("AlexNet Architecture (~60M Parameters)", font_size=86, weight=BOLD)
        overview_title.set_color(YELLOW)
        overview_title.to_edge(DOWN, buff=0.5).shift(RIGHT*7.9+DOWN*0.8)
        
        self.play(
            self.camera.frame.animate.scale(4.19).move_to(arch_center + DOWN * 0.5).shift(LEFT*0.3),
            FadeIn(overview_title),
            run_time=1.5
        )
        
        self.wait(3)

        self.camera.frame.save_state()

        
        # ==========================================
        # FINISHING TOUCH: SLOW PAN FROM INPUT TO OUTPUT
        # ==========================================
        
        # Zoom in and move to input
        self.play(
            self.camera.frame.animate.scale(0.25).move_to(input_pos).shift(RIGHT*1.6),
            run_time=1.5
        )
        
        # Slow pan from input to output
        self.play(
            self.camera.frame.animate.move_to(output_pos).shift(LEFT*1.99),
            run_time=28,
        )
        
        self.wait(2)
        
        
