from manimlib import *
import numpy as np


class ConvolutionANDpadding(Scene):
    
    def construct(self):


        self.camera.frame.scale(0.95).shift(LEFT*0.5+UP*0.35)
        
        self.camera.frame.save_state()

        # ==========================================
        # SETUP: Create the input image grid (6x6)
        # ==========================================
        
        np.random.seed(42)
        input_values = np.random.randint(0, 10, (6, 6))
        
        cell_size = 0.7
        
        # Create input grid
        input_grid = VGroup()
        input_cells = {}
        input_texts = {}
        
        for i in range(6):
            for j in range(6):
                cell = Square(side_length=cell_size)
                cell.set_fill(WHITE, opacity=1)
                cell.set_stroke(BLACK, width=2)
                cell.move_to(RIGHT * j * cell_size + DOWN * i * cell_size)
                
                # Text slightly LEFT aligned inside cell
                value = Text(str(input_values[i, j]), font_size=24, weight=BOLD)
                value.set_color(BLACK)
                value.move_to(cell.get_center() + LEFT * 0.12)
                
                cell_group = VGroup(cell, value)
                input_cells[(i, j)] = cell_group
                input_texts[(i, j)] = value
                input_grid.add(cell_group)
        
        # Center input grid vertically at origin, positioned left
        input_grid.center()
        input_grid.move_to(LEFT * 4.15)
        
        input_label = Text("Input Image", font_size=39, weight=BOLD)
        input_label.next_to(input_grid, UP, buff=0.4)
        
        # ==========================================
        # SETUP: Create the kernel (3x3) - YELLOW
        # ==========================================
        
        kernel_values = np.array([
            [-1, 0, 1],
            [-1, 0, 1],
            [-1, 0, 1]
        ])
        
        kernel_grid = VGroup()
        kernel_cells = {}
        kernel_texts = {}
        
        for i in range(3):
            for j in range(3):
                cell = Square(side_length=cell_size)
                cell.set_fill(YELLOW, opacity=1)
                cell.set_stroke(BLACK, width=2)
                cell.move_to(RIGHT * j * cell_size + DOWN * i * cell_size)
                
                # Text slightly RIGHT aligned inside cell
                val = kernel_values[i, j]
                value = Text(str(val), font_size=24, weight=BOLD)
                value.set_color(BLACK)
                value.move_to(cell.get_center() + RIGHT * 0.12)
                
                cell_group = VGroup(cell, value)
                kernel_cells[(i, j)] = cell_group
                kernel_texts[(i, j)] = value
                kernel_grid.add(cell_group)
        
        # Center kernel grid vertically, positioned in middle
        kernel_grid.center()
        kernel_original_pos = ORIGIN
        kernel_grid.move_to(kernel_original_pos)
        
        # Set kernel z_index to +4 so it appears above padding
        kernel_grid.set_z_index(4)
        
        kernel_label = Text("Filter", font_size=36, weight=BOLD)
        kernel_label.set_color(YELLOW)
        kernel_label.next_to(kernel_grid, UP, buff=0.4)
        
        # ==========================================
        # SETUP: Create output grid (4x4) - Right side
        # Question marks are separate, not in output_grid VGroup
        # ==========================================
        
        output_grid = VGroup()
        output_cells = {}
        output_question_marks = {}  # Store question marks separately
        
        for i in range(4):
            for j in range(4):
                cell = Square(side_length=cell_size)
                cell.set_fill(GREEN, opacity=0.3)
                cell.set_stroke(GREEN, width=3)
                cell.move_to(RIGHT * j * cell_size + DOWN * i * cell_size)
                
                value = Text("?", font_size=24, weight=BOLD)
                value.set_color(WHITE)  # WHITE color for output text
                value.move_to(cell.get_center())
                
                # Only add cell to output_grid, not the question mark
                output_grid.add(cell)
                output_cells[(i, j)] = cell
                output_question_marks[(i, j)] = value
        
        # Center output grid vertically, positioned right
        output_grid.center()
        output_grid.move_to(RIGHT * 4.04)
        
        # Position question marks after grid is centered
        for i in range(4):
            for j in range(4):
                output_question_marks[(i, j)].move_to(output_cells[(i, j)].get_center())
        
        output_label = Text("Output", font_size=37, weight=BOLD)
        output_label.set_color(GREEN)
        output_label.next_to(output_grid, UP, buff=0.4)
        
        # ==========================================
        # SETUP: Asterisk and equals sign (centered vertically)
        # ==========================================
        
        asterisk = Tex(r"*", font_size=72)
        asterisk.set_color(WHITE)
        asterisk.move_to(LEFT * 1.559)  # Between input and kernel
        
        equals_sign = Tex(r"=", font_size=72)
        equals_sign.set_color(WHITE)
        equals_sign.move_to(RIGHT * 1.78)  # Between kernel and output
        
        # ==========================================
        # PART 1: Show input grid
        # ==========================================
        
        self.play(
            LaggedStartMap(FadeIn, input_grid, lag_ratio=0.02),
            Write(input_label),
            run_time=1.5
        )
        self.wait(0.5)
        
        # ==========================================
        # PART 2: Show asterisk, then kernel
        # ==========================================
        
        self.play(Write(asterisk))
        self.wait(0.3)
        
        self.play(
            LaggedStartMap(FadeIn, kernel_grid, lag_ratio=0.05),
            Write(kernel_label),
            run_time=1
        )
        self.wait(0.5)


        
        # ==========================================
        # PART 3: Show output grid (empty) with question marks
        # ==========================================
        
        self.play(Write(equals_sign))
        
        # Create a VGroup of question marks for animation
        question_marks_group = VGroup(*[output_question_marks[(i, j)] for i in range(4) for j in range(4)])
        
        self.play(
            LaggedStartMap(FadeIn, output_grid, lag_ratio=0.05),
            LaggedStartMap(FadeIn, question_marks_group, lag_ratio=0.05),
            Write(output_label),
            run_time=1
        )
        self.wait(1)


        # ==========================================
        # PART 4: Fade out asterisk/equals, move kernel over input
        # Make kernel semi-transparent
        # ==========================================
        
        self.play(
            FadeOut(asterisk),
            FadeOut(kernel_label),
            FadeOut(equals_sign),
            run_time=0.8
        )
        
        # Make kernel semi-transparent so input shows through
        self.play(
            *[kernel_cells[(i, j)][0].animate.set_fill(YELLOW, opacity=0.5) 
              for i in range(3) for j in range(3)],
            run_time=0.5
        )
        
        # Position kernel over top-left of input (center at position 1,1)
        first_center = input_cells[(1, 1)][0].get_center()
        
        self.play(
            kernel_grid.animate.move_to(first_center),
            run_time=1
        )
        self.wait(0.5)

        
        
        
        # ==========================================
        # PART 5: First calculation - TransformFromCopy to build equation
        # ==========================================
        
        def compute_conv(input_vals, kernel_vals, row, col):
            total = 0
            for ki in range(3):
                for kj in range(3):
                    total += input_vals[row + ki, col + kj] * kernel_vals[ki, kj]
            return total
        
        conv_result = compute_conv(input_values, kernel_values, 0, 0)
        
        # Equation position
        eq_center = DOWN * 3.37
        
        # Create equation parts: (img × ker) + (img × ker) + ...
        # Calculate positions for 9 terms (3 rows of 3)
        term_positions = []
        for row in range(3):
            for col in range(3):
                x_pos = (col - 1) * 2.2
                y_pos = (1 - row) * 0.6
                term_positions.append(eq_center + RIGHT * x_pos + UP * y_pos)
        
        # Create all multiplication terms
        all_terms = []
        plus_signs = []
        
        for idx, (ki, kj) in enumerate([(i, j) for i in range(3) for j in range(3)]):
            img_val = input_values[ki, kj]
            ker_val = kernel_values[ki, kj]
            
            # Create the term (img × ker)
            open_paren = Text("(", font_size=26)
            open_paren.set_color(WHITE)
            
            img_text = Text(str(img_val), font_size=26, weight=BOLD)
            img_text.set_color(WHITE)
            
            times_sign = Tex(r"\ \times \ ", font_size=46,).set_color("#ff0000")
            times_sign.set_color(WHITE)
            
            ker_text = Text(str(ker_val), font_size=26, weight=BOLD)
            ker_text.set_color(YELLOW)
            
            close_paren = Text(")", font_size=26)
            close_paren.set_color(WHITE)
            
            term = VGroup(open_paren, img_text, times_sign, ker_text, close_paren)
            term.arrange(RIGHT, buff=0.05)
            term.move_to(term_positions[idx])
            all_terms.append(term)
            
            # Add plus signs between terms (except last in each row)
            if (idx + 1) % 3 != 0:
                plus = Tex("+", font_size=26)
                plus.set_color(WHITE)
                plus.move_to(term_positions[idx] + RIGHT * 1.1)
                plus_signs.append(plus)
        
        # TransformFromCopy: pixel values and kernel values -> equation terms
        transform_anims = []
        
        for idx, (ki, kj) in enumerate([(i, j) for i in range(3) for j in range(3)]):
            # Get source texts from the grid
            img_text_src = input_texts[(ki, kj)]
            ker_text_src = kernel_texts[(ki, kj)]
            
            # Transform pixel value to equation (index 1 is img_text in term)
            transform_anims.append(TransformFromCopy(img_text_src, all_terms[idx][1]))
            # Transform kernel value to equation (index 3 is ker_text in term)
            transform_anims.append(TransformFromCopy(ker_text_src, all_terms[idx][3]))
        
        # First show the brackets and multiply signs
        static_parts = []
        for term in all_terms:
            static_parts.extend([term[0], term[2], term[4]])  # (, ×, )
        
        self.play(self.camera.frame.animate.scale(1.1).shift(DOWN*0.69))
        # TransformFromCopy for the numbers (2 seconds)
        self.play(*[FadeIn(p) for p in static_parts],
                  *transform_anims,
                   *[FadeIn(p) for p in plus_signs] ,run_time=2)
        

        
        self.wait(1.2)

        
        # Gather all equation parts
        full_equation = VGroup(*all_terms, *plus_signs)
        
        # Get center of equation for result placement
        eq_center_pos = full_equation.get_center()
        
        # Create result text at equation position, scaled up
        result_text = Text(str(conv_result), font_size=46, weight=BOLD)
        result_text.set_color(WHITE)
        result_text.move_to(eq_center_pos)
        result_text.scale(2)  # Scale up the result
        
        # Transform equation to result using Transform()
        self.play(
            Transform(full_equation, result_text),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Move result to output cell
        final_result = Text(str(conv_result), font_size=24, weight=BOLD)
        final_result.set_color(WHITE)  # WHITE color
        final_result.move_to(output_cells[(0, 0)].get_center())
        
        old_question = output_question_marks[(0, 0)]
        
        self.play(
            ReplacementTransform(full_equation, final_result),
            self.camera.frame.animate.restore(),
            FadeOut(old_question),
            run_time=1
        )
        
        # Add the result number to output_grid
        output_grid.add(final_result)
        
        self.wait(0.5)
        
        # ==========================================
        # PART 6: Continue convolution for remaining cells
        # TransformFromCopy from overlapping region to output
        # NO SurroundingRectangle
        # ==========================================

        # All remaining positions (4x4 output, already did 0,0)
        positions = []
        for i in range(4):
            for j in range(4):
                if not (i == 0 and j == 0):
                    positions.append((i, j))
        
        for out_row, out_col in positions:
            # New kernel center
            new_center = input_cells[(out_row + 1, out_col + 1)][0].get_center()
            
            # Move kernel
            self.play(
                kernel_grid.animate.move_to(new_center),
                run_time=0.6
            )
            
            # Calculate value
            conv_val = compute_conv(input_values, kernel_values, out_row, out_col)
            
            # Create result
            result_val = Text(str(conv_val), font_size=24, weight=BOLD)
            result_val.set_color(WHITE)  # WHITE color
            result_val.move_to(output_cells[(out_row, out_col)].get_center())
            
            old_q = output_question_marks[(out_row, out_col)]
            
            # TransformFromCopy from kernel to output (kernel represents the operation)
            self.play(
                TransformFromCopy(kernel_grid, result_val),
                FadeOut(old_q),
                run_time=0.6
            )
            
            # Add result to output_grid
            output_grid.add(result_val)
        
        self.wait(1)
        
        # ==========================================
        # PART 7: Bring kernel back to original position
        # Restore opacity, fade in asterisk
        # ==========================================
        
        # Move kernel back to original position
        self.play(
            kernel_grid.animate.move_to(kernel_original_pos),
            run_time=0.8
        )
        
        # Restore kernel opacity to 1
        self.play(
            *[kernel_cells[(i, j)][0].animate.set_fill(YELLOW, opacity=1) 
              for i in range(3) for j in range(3)],
            run_time=1
        )
        
        # Fade in asterisk and kernel label
        self.play(
            FadeIn(asterisk),
            FadeIn(kernel_label),
            FadeIn(equals_sign),
            run_time=1
        )
        
        self.wait(0.5)
        
        # Final label for output
        final_label = Text("Feature Map!", font_size=36, weight=BOLD)
        final_label.set_color(GREEN)
        final_label.next_to(output_grid, DOWN, buff=0.4)
        
        self.play(Write(final_label))

        self.camera.frame.save_state()
        
        self.wait(2)

        self.play(self.camera.frame.animate.scale(1.12).shift(DOWN*0.757))

        a = Text("n x n").next_to(input_grid, DOWN, buff=0.8)
        b = Text("f x f").set_color(YELLOW).next_to(kernel_grid, DOWN, buff=0.8)
        c = Text("(n - f + 1) \n     x \n(n - f + 1)").set_color(GREEN).next_to(final_label, DOWN, buff=0.17).scale(0.7)

        self.play(ShowCreation(a))

        self.play(ShowCreation(b))

        self.wait()

        self.play(ShowCreation(c))


        rect = SurroundingRectangle(c, color=RED_C, stroke_width=6).scale(1.16)
        self.play(ShowCreation(rect))

        self.wait(2)

        self.play(
            self.camera.frame.animate.restore(),
            FadeOut(a),
            FadeOut(b),
            FadeOut(c),
            FadeOut(rect)
        )

        self.wait(2)

        
        # First, fade out titles, output grid, equals sign, asterisk, kernel label
        self.play(
            FadeOut(input_label),
            FadeOut(output_label),
            FadeOut(output_grid),
            FadeOut(final_label),
            FadeOut(equals_sign),
            FadeOut(asterisk),
            FadeOut(kernel_label),
            run_time=1
        )
        
        # Move input grid to center-left for better visibility
        self.play(
            input_grid.animate.move_to(LEFT * 2),
            kernel_grid.animate.move_to(RIGHT * 3),
            run_time=1
        )

        self.wait(2)

        # Update input_cells positions reference
        for i in range(6):
            for j in range(6):
                input_cells[(i, j)] = input_grid[i * 6 + j]
        
        self.wait(1.5)



        # ==========================================
        # PART 8a: Show corner cell contribution (top-left)
        # Highlight that corner cell only contributes to ONE output
        # ==========================================
        
        corner_title = Text("Corner pixels contribute to only 1 output", font_size=32, weight=BOLD)
        corner_title.set_color(TEAL_B)
        corner_title.to_edge(UP, buff=0.5).shift(LEFT*0.4)
        self.play(Write(corner_title), self.camera.frame.animate.shift(UP*0.4) ,run_time=1)
        
        # Highlight top-left cell (0,0) in PURPLE
        corner_cell = input_cells[(0, 0)][0]
        self.play(
            corner_cell.animate.set_fill(TEAL_B, opacity=0.8),
            run_time=0.5
        )
        
        # Make kernel semi-transparent and move over input
        self.play(
            *[kernel_cells[(i, j)][0].animate.set_fill(YELLOW, opacity=0.5)
              for i in range(3) for j in range(3)],
            run_time=0.5
        )
        
        # Move kernel to position (1,1) - the only position where corner (0,0) is covered
        kernel_pos_center = input_cells[(1, 1)][0].get_center()
        self.play(
            kernel_grid.animate.move_to(kernel_pos_center),
            run_time=1
        )
        
        # Show indicator text
        one_contrib = Text("Only 1 convolution!", font_size=28, weight=BOLD)
        one_contrib.set_color(TEAL_B)
        one_contrib.next_to(input_grid, RIGHT, buff=0.75)
        self.play(FadeIn(one_contrib), run_time=0.5)
        self.wait(1.5)
        
        # Clean up
        self.play(
            FadeOut(one_contrib),
            corner_cell.animate.set_fill(WHITE, opacity=1),
            run_time=0.5
        )
        self.play(FadeOut(corner_title), run_time=0.5)
        
        # ==========================================
        # PART 8b: Show center cell contribution
        # Center cells contribute to MANY outputs
        # ==========================================
        
        center_title = Text("Center pixels contribute to up to 9 outputs!", font_size=32, weight=BOLD)
        center_title.set_color(GREEN)
        center_title.to_edge(UP, buff=0.5).shift(LEFT*0.4)
        self.play(Write(center_title), run_time=1)
        
        # Highlight center cell (2,2) or (3,3) in PURPLE
        center_cell = input_cells[(2, 2)][0]
        self.play(
            center_cell.animate.set_fill(GREEN, opacity=0.8),
            run_time=0.5
        )
        
        # Show all 9 positions where this cell is covered by kernel
        # Cell (2,2) is covered when kernel center is at (1,1), (1,2), (1,3), (2,1), (2,2), (2,3), (3,1), (3,2), (3,3)
        kernel_positions = [
            (1, 1), (1, 2), (1, 3),
            (2, 1), (2, 2), (2, 3),
            (3, 1), (3, 2), (3, 3)
        ]
        
        count_text = Text("Count: 0", font_size=48, weight=BOLD)
        count_text.set_color(GREEN)
        count_text.next_to(input_grid, RIGHT, buff=1.53)
        self.play(FadeIn(count_text), run_time=0.3)
        
        for idx, (ki, kj) in enumerate(kernel_positions):
            new_center = input_cells[(ki, kj)][0].get_center()
            
            # Update count
            new_count = Text(f"Count: {idx + 1}", font_size=48, weight=BOLD)
            new_count.set_color(GREEN)
            new_count.move_to(count_text)
            
            self.play(
                kernel_grid.animate.move_to(new_center),
                Transform(count_text, new_count),
                run_time=0.4
            )
        
        self.wait(1)
        
        # Final message
        unequal_msg = Text("Unequal contribution = information loss at edges!", font_size=28, weight=BOLD)
        unequal_msg.set_color(RED)
        unequal_msg.move_to(center_title)
        self.play(ReplacementTransform(center_title, unequal_msg), run_time=1)
        self.wait(1.5)
        
        # Clean up
        self.play(
            FadeOut(count_text),
            FadeOut(center_title),
            FadeOut(unequal_msg),
            center_cell.animate.set_fill(WHITE, opacity=1),
            run_time=0.8
        )


        # Move input grid to center-left for better visibility
        self.play(
            input_grid.animate.move_to(LEFT * 2.5),
            kernel_grid.animate.move_to(RIGHT * 3.1),
            self.camera.frame.animate.shift(DOWN*0.4),
            run_time=1
        )

        self.play(
            *[kernel_cells[(i, j)][0].animate.set_fill(YELLOW, opacity=1)
              for i in range(3) for j in range(3)],
            run_time=0.5
        )

        self.wait(2)

        
        padding_title = Text("Solution: Add Padding!", font_size=36, weight=BOLD)
        padding_title.set_color(BLUE)
        padding_title.to_edge(UP, buff=0.5).shift(LEFT*0.4)
        self.play(Write(padding_title), run_time=1)
        self.wait(2)


        # Create padded grid (8x8 with padding of 1)
        padded_size = 8
        padded_grid = VGroup()
        padded_cells = {}
        padded_texts = {}
        
        # First, create the padding border cells (empty, value 0)
        padding_positions = []
        
        # Top and bottom rows
        for j in range(padded_size):
            padding_positions.append((0, j))  # top row
            padding_positions.append((7, j))  # bottom row
        
        # Left and right columns (excluding corners already added)
        for i in range(1, 7):
            padding_positions.append((i, 0))  # left column
            padding_positions.append((i, 7))  # right column
        
        # Create padding cells with "0" text and z_index = -1
        for i, j in padding_positions:
            cell = Square(side_length=cell_size)
            cell.set_fill(WHITE, opacity=1)
            cell.set_stroke(BLACK, width=2)
            cell.move_to(input_grid.get_center() + RIGHT * (j - 3.5) * cell_size + DOWN * (i - 3.5) * cell_size)
            cell.set_z_index(-1)  # Set z_index to -1 for padding cells
            
            value = Text("0", font_size=24, weight=BOLD)
            value.set_color(BLACK)
            value.move_to(cell.get_center() + LEFT * 0.12)
            value.set_z_index(-1)  # Set z_index to -1 for padding text
            
            cell_group = VGroup(cell, value)
            cell_group.set_z_index(-1)  # Set z_index to -1 for the group
            padded_cells[(i, j)] = cell_group
            padded_grid.add(cell_group)
        
        # Show padding growing from center (GrowFromCenter)
        self.play(
            LaggedStartMap(GrowFromCenter, padded_grid, lag_ratio=0.03),
            FadeOut(padding_title),
            run_time=1.5
        )
        
        self.wait(0.5)

        self.camera.frame.save_state()

        self.play(self.camera.frame.animate.scale(1.2).shift(DOWN*0.31+RIGHT*1.57))
        
        # ==========================================
        # PART 9: Make kernel transparent and move over padded input FIRST
        # ==========================================
        
        # Update kernel_cells position reference
        for i in range(3):
            for j in range(3):
                kernel_cells[(i, j)] = kernel_grid[i * 3 + j]
        
        # Now add references for the inner cells (original input, positions 1-6 in padded grid)
        for i in range(6):
            for j in range(6):
                # Map original input cells to padded positions (offset by 1)
                padded_i = i + 1
                padded_j = j + 1
                padded_cells[(padded_i, padded_j)] = input_cells[(i, j)]
        
        # Create padded input values array (8x8)
        padded_values = np.zeros((8, 8), dtype=int)
        for i in range(6):
            for j in range(6):
                padded_values[i + 1, j + 1] = input_values[i, j]
        
        # Make kernel semi-transparent FIRST
        self.play(
            *[kernel_cells[(i, j)][0].animate.set_fill(YELLOW, opacity=0.5)
              for i in range(3) for j in range(3)],
            run_time=0.5
        )
        
        # Get the center position for the combined input (padded + original)
        combined_center = input_grid.get_center()
        
        # Move kernel over the first position (top-left of padded input)
        # Kernel center should be at padded position (1, 1) for first output
        first_kernel_pos = combined_center + RIGHT * (1 - 3.5) * cell_size + DOWN * (1 - 3.5) * cell_size
        
        self.play(
            kernel_grid.animate.move_to(first_kernel_pos),
            run_time=1
        )
        
        self.wait(0.5)
        
        # ==========================================
        # PART 10: NOW Create output grid for padded convolution (6x6)
        # Question marks are separate, not in padded_output_grid VGroup
        # ==========================================
        
        padded_output_grid = VGroup()
        padded_output_cells = {}
        padded_output_question_marks = {}  # Store question marks separately
        
        for i in range(6):
            for j in range(6):
                cell = Square(side_length=cell_size)
                cell.set_fill(GREEN, opacity=0.3)
                cell.set_stroke(GREEN, width=3)
                cell.move_to(RIGHT * j * cell_size + DOWN * i * cell_size)
                
                value = Text("?", font_size=24, weight=BOLD)
                value.set_color(WHITE)
                value.move_to(cell.get_center())
                
                # Only add cell to padded_output_grid, not the question mark
                padded_output_grid.add(cell)
                padded_output_cells[(i, j)] = cell
                padded_output_question_marks[(i, j)] = value
        
        # Position output grid
        padded_output_grid.center()
        padded_output_grid.move_to(RIGHT * 4.5)
        
        # Position question marks after grid is centered
        for i in range(6):
            for j in range(6):
                padded_output_question_marks[(i, j)].move_to(padded_output_cells[(i, j)].get_center())
        
        padded_output_label = Text("Output (Same Size!)", font_size=32, weight=BOLD)
        padded_output_label.set_color(GREEN)
        padded_output_label.next_to(padded_output_grid, UP, buff=0.4)
        
        # Create a VGroup of question marks for animation
        padded_question_marks_group = VGroup(*[padded_output_question_marks[(i, j)] for i in range(6) for j in range(6)])
        
        # Show output grid
        self.play(
            LaggedStartMap(FadeIn, padded_output_grid, lag_ratio=0.02),
            LaggedStartMap(FadeIn, padded_question_marks_group, lag_ratio=0.02),
            Write(padded_output_label),
            run_time=1.5
        )
        self.wait(0.5)
        
        # ==========================================
        # PART 11: Perform convolution on padded input
        # ==========================================
        
        # Compute convolution for padded input
        def compute_padded_conv(padded_vals, kernel_vals, row, col):
            total = 0
            for ki in range(3):
                for kj in range(3):
                    total += padded_vals[row + ki, col + kj] * kernel_vals[ki, kj]
            return total
        
        # Iterate through all 6x6 output positions
        for out_row in range(6):
            for out_col in range(6):
                # Calculate kernel center position
                # Kernel center should be at padded position (out_row + 1, out_col + 1)
                # This corresponds to the center of the 3x3 region starting at (out_row, out_col)
                
                # Calculate position relative to combined grid center
                kernel_center_i = out_row + 1  # in padded coordinates
                kernel_center_j = out_col + 1
                
                # Get actual position on screen
                kernel_target_pos = combined_center + RIGHT * (kernel_center_j - 3.5) * cell_size + DOWN * (kernel_center_i - 3.5) * cell_size
                
                # Move kernel (skip first position since we're already there)
                if not (out_row == 0 and out_col == 0):
                    self.play(
                        kernel_grid.animate.move_to(kernel_target_pos),
                        run_time=0.3
                    )
                
                # Calculate convolution value
                conv_val = compute_padded_conv(padded_values, kernel_values, out_row, out_col)
                
                # Create result text
                result_val = Text(str(conv_val), font_size=24, weight=BOLD)
                result_val.set_color(WHITE)
                result_val.move_to(padded_output_cells[(out_row, out_col)].get_center())
                
                old_q = padded_output_question_marks[(out_row, out_col)]
                
                # TransformFromCopy from kernel to output
                self.play(
                    TransformFromCopy(kernel_grid, result_val),
                    FadeOut(old_q),
                    run_time=0.3
                )
                
                # Add result to padded_output_grid
                padded_output_grid.add(result_val)
        
        self.wait(1)

        
        # ==========================================
        # PART 12: Move output to the right, kernel to center, fade in asterisk and equals
        # ==========================================
        
        # Calculate new positions
        new_output_pos = RIGHT * 7.2  # Move output further right
        new_kernel_pos = RIGHT * 2.5  # Kernel goes in between
        

        # Restore kernel opacity
        self.play(
            *[kernel_cells[(i, j)][0].animate.set_fill(YELLOW, opacity=1)
              for i in range(3) for j in range(3)],
            run_time=0.5
        )
        
        # Move output grid and kernel, fade in symbols
        self.play(
            padded_output_grid.animate.move_to(new_output_pos),
            padded_output_label.animate.next_to(VGroup().move_to(new_output_pos), UP, buff=0.4 + 2.1 * cell_size),
            kernel_grid.animate.move_to(new_kernel_pos),
            padded_output_label.animate.shift(UP*0.5+RIGHT*2.52),
            self.camera.frame.animate.shift(RIGHT*0.95+UP*0.2),
            run_time=1.2
        )

        star = Text("*").next_to(kernel_grid, LEFT, buff=0.45)
        equal = Text("=").next_to(kernel_grid, RIGHT, buff=0.55).scale(1.4)
        self.play(GrowFromCenter(star), GrowFromCenter(equal))


        self.camera.frame.save_state()

        self.wait(1)


        a = Text("(n + 2p - f + 1) x (n + 2p - f + 1)").set_color(GREEN_B)
        a[4].set_color(RED_C)
        a[-6].set_color(RED_C)

        a.next_to(padded_grid, DOWN).shift(RIGHT*4.6+DOWN*0.4).scale(0.9)

        self.play(Write(a), self.camera.frame.animate.shift(DOWN*0.55))

        self.wait(2)


        padding_formula = Text("p = (f - 1) / 2", font_size=52, weight=BOLD)
        padding_formula[3].set_color(YELLOW)
        padding_formula[0].set_color(RED_B)
        padding_formula.next_to(a, DOWN, buff=0.3).move_to(a)

        self.play(Transform(a, padding_formula))
        self.wait(2)
        
        self.play(Uncreate(a), self.camera.frame.animate.restore().shift(LEFT*3.31).scale(0.87), FadeOut(padded_output_grid), FadeOut(padded_output_label), FadeOut(equal))

        self.wait(2)



        self.play(FadeOut(star))

        # kernel opacity
        self.play(
            *[kernel_cells[(i, j)][0].animate.set_fill(YELLOW, opacity=0.5)
              for i in range(3) for j in range(3)],
            run_time=0.5
        )



        # Move kernel to first position
        first_pos = combined_center + RIGHT * (1 - 3.5) * cell_size + DOWN * (1 - 3.5) * cell_size
        self.play(kernel_grid.animate.move_to(first_pos), run_time=0.8)
        
        # Demonstrate stride=1: move 7 times (just sliding, no output)
        stride_1_positions = [
            (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),  # Move right along first row
            (2,1), (2, 2), (2, 3), (2,4), (2,5), (2,6),  # Go down and move left a bit
            (3,1), (3, 2), (3, 3), (3,4),   # Go down and move left a bit
        ]
        
        for ki, kj in stride_1_positions:
            target_pos = combined_center + RIGHT * (kj - 3.5) * cell_size + DOWN * (ki - 3.5) * cell_size
            self.play(
                kernel_grid.animate.move_to(target_pos),
                run_time=0.49
            )
        
        self.wait(2)    


        stride_title = Text("Stride = 1", font_size=50, weight=BOLD)
        stride_title.set_color(ORANGE)
        stride_title.next_to(padded_grid, RIGHT, buff=0.65)
        self.play(Write(stride_title),self.camera.frame.animate.shift(RIGHT*0.6) ,run_time=1)
        self.wait(2)

        self.play(Transform(stride_title, Text("Stride = 2", font_size=50, weight=BOLD).set_color(ORANGE).move_to(stride_title)))
        self.wait(2)


        target_pos = combined_center + RIGHT * (1 - 3.5) * cell_size + DOWN * (1 - 3.5) * cell_size
        self.play(
                kernel_grid.animate.move_to(target_pos),
                run_time=0.49
            )
        self.wait()

        self.camera.frame.save_state()

        self.play(Uncreate(stride_title), self.camera.frame.animate.shift(RIGHT+DOWN*0.14))


        # Create output grid for stride=2 convolution (3x3 output)
        # With 8x8 padded input, 3x3 kernel, stride=2: output = (8-3)/2 + 1 = 3
        stride2_output_grid = VGroup()
        stride2_output_cells = {}
        stride2_output_question_marks = {}
        
        for i in range(3):
            for j in range(3):
                cell = Square(side_length=cell_size)
                cell.set_fill(GREEN, opacity=0.3)
                cell.set_stroke(GREEN, width=3)
                cell.move_to(RIGHT * j * cell_size + DOWN * i * cell_size)
                
                value = Text("?", font_size=24, weight=BOLD)
                value.set_color(WHITE)
                value.move_to(cell.get_center())
                
                stride2_output_grid.add(cell)
                stride2_output_cells[(i, j)] = cell
                stride2_output_question_marks[(i, j)] = value

        
        # Position output grid to the right
        stride2_output_grid.center()
        stride2_output_grid.move_to(RIGHT * 4.5)
        
        # Position question marks after grid is centered
        for i in range(3):
            for j in range(3):
                stride2_output_question_marks[(i, j)].move_to(stride2_output_cells[(i, j)].get_center())
        
        stride2_output_label = Text("Output (Stride=2)", font_size=32, weight=BOLD)
        stride2_output_label.set_color(GREEN)
        stride2_output_label.next_to(stride2_output_grid, UP, buff=0.56)
        
        # Create VGroup of question marks for animation
        stride2_question_marks_group = VGroup(*[stride2_output_question_marks[(i, j)] for i in range(3) for j in range(3)])
        

        self.play(
            LaggedStartMap(FadeIn, stride2_output_grid, lag_ratio=0.05),
            LaggedStartMap(FadeIn, stride2_question_marks_group, lag_ratio=0.05),
            Write(stride2_output_label),
            run_time=1.5
        )
        self.wait(0.5)
        
        # ==========================================
        # Perform stride=2 convolution
        # ==========================================
        
        # With stride=2, kernel positions are at (1,1), (1,3), (1,5), (3,1), (3,3), (3,5), (5,1), (5,3), (5,5)
        # Output positions: (0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)
        
        stride = 2
        
        for out_row in range(3):
            for out_col in range(3):
                # Calculate kernel center position with stride=2
                kernel_center_i = out_row * stride + 1  # in padded coordinates
                kernel_center_j = out_col * stride + 1
                
                # Get actual position on screen
                kernel_target_pos = combined_center + RIGHT * (kernel_center_j - 3.5) * cell_size + DOWN * (kernel_center_i - 3.5) * cell_size
                
                # Move kernel
                self.play(
                    kernel_grid.animate.move_to(kernel_target_pos),
                    run_time=0.5
                )
                
                # Calculate convolution value
                conv_val = compute_padded_conv(padded_values, kernel_values, out_row * stride, out_col * stride)
                
                # Create result text
                result_val = Text(str(conv_val), font_size=24, weight=BOLD)
                result_val.set_color(WHITE)
                result_val.move_to(stride2_output_cells[(out_row, out_col)].get_center())
                
                old_q = stride2_output_question_marks[(out_row, out_col)]
                
                # TransformFromCopy from kernel to output
                self.play(
                    TransformFromCopy(kernel_grid, result_val),
                    FadeOut(old_q),
                    run_time=0.5
                )
                
                # Add result to output grid
                stride2_output_grid.add(result_val)
        
        self.wait(1)
        
        # ==========================================
        # Final cleanup and formula display
        # ==========================================
        
        # Restore kernel opacity
        self.play(
            *[kernel_cells[(i, j)][0].animate.set_fill(YELLOW, opacity=1)
              for i in range(3) for j in range(3)],
            run_time=0.5
        )
        
        # Move kernel back to a nice position
        self.play(
            kernel_grid.animate.shift(RIGHT * 4 + UP),
            stride2_output_grid.animate.shift(RIGHT * 1.6 +DOWN*0.012),
            stride2_output_label.animate.shift(RIGHT*1.6),
            self.camera.frame.animate.scale(1.12).shift(RIGHT*0.7),

            run_time=1
        )
        

        # Add asterisk
        asterisk_stride = Tex(r"*", font_size=72)
        asterisk_stride.set_color(WHITE)
        asterisk_stride.next_to(kernel_grid, LEFT, buff=0.45)
        
        equal = Text("=").next_to(kernel_grid, RIGHT, buff=0.45)
        self.play(FadeIn(asterisk_stride), FadeIn(equal),run_time=0.5)
        
        self.wait(2)
        


class Stride_Convolution(Scene):
    
    def construct(self):
        
        self.camera.frame.shift(LEFT*0.7)

        # ==========================================
        # SETUP: Create the input image grid (7x7)
        # ==========================================
        
        np.random.seed(123)
        input_values = np.random.randint(0, 10, (7, 7))
        
        cell_size = 0.65
        
        # Create input grid
        input_grid = VGroup()
        input_cells = {}
        input_texts = {}
        
        for i in range(7):
            for j in range(7):
                cell = Square(side_length=cell_size)
                cell.set_fill(WHITE, opacity=1)
                cell.set_stroke(BLACK, width=2)
                cell.move_to(RIGHT * j * cell_size + DOWN * i * cell_size)
                
                value = Text(str(input_values[i, j]), font_size=22, weight=BOLD)
                value.set_color(BLACK)
                value.move_to(cell.get_center()+LEFT*0.15)
                
                cell_group = VGroup(cell, value)
                input_cells[(i, j)] = cell_group
                input_texts[(i, j)] = value
                input_grid.add(cell_group)
        
        input_grid.center()
        input_grid.move_to(LEFT * 4.1)

        # ==========================================
        # SETUP: Create the kernel (3x3)
        # ==========================================
        
        kernel_values = np.array([
            [-1, 0, 1],
            [-1, 0, 1],
            [-1, 0, 1]
        ])
        
        kernel_grid = VGroup()
        kernel_cells = {}
        kernel_texts = {}
        
        for i in range(3):
            for j in range(3):
                cell = Square(side_length=cell_size)
                cell.set_fill(YELLOW, opacity=1)
                cell.set_stroke(BLACK, width=2)
                cell.move_to(RIGHT * j * cell_size + DOWN * i * cell_size)
                
                val = kernel_values[i, j]
                value = Text(str(val), font_size=22, weight=BOLD)
                value.set_color(BLACK)
                value.move_to(cell.get_center()+RIGHT*0.1)
                
                cell_group = VGroup(cell, value)
                kernel_cells[(i, j)] = cell_group
                kernel_texts[(i, j)] = value
                kernel_grid.add(cell_group)
        
        kernel_grid.center()
        kernel_grid.move_to(ORIGIN).shift(RIGHT*0.35)
        kernel_grid.set_z_index(4)
        

        # ==========================================
        # SETUP: Create output grid (3x3)
        # With 7x7 input, 3x3 kernel, stride=2: output = (7-3)/2 + 1 = 3
        # ==========================================
        
        output_grid = VGroup()
        output_cells = {}
        output_question_marks = {}
        
        for i in range(3):
            for j in range(3):
                cell = Square(side_length=cell_size)
                cell.set_fill(GREEN, opacity=0.3)
                cell.set_stroke(GREEN, width=3)
                cell.move_to(RIGHT * j * cell_size + DOWN * i * cell_size)
                
                value = Text("?", font_size=22, weight=BOLD)
                value.set_color(WHITE)
                value.move_to(cell.get_center())
                
                output_grid.add(cell)
                output_cells[(i, j)] = cell
                output_question_marks[(i, j)] = value
        
        output_grid.center()
        output_grid.move_to(RIGHT * 3.89)
        
        for i in range(3):
            for j in range(3):
                output_question_marks[(i, j)].move_to(output_cells[(i, j)].get_center())
        

        # ==========================================
        # SETUP: Symbols
        # ==========================================
        
        asterisk = Tex(r"*", font_size=72)
        asterisk.set_color(WHITE)
        asterisk.next_to(kernel_grid, LEFT, buff=0.45)
        
        equals_sign = Tex(r"=", font_size=72)
        equals_sign.set_color(WHITE)
        equals_sign.next_to(kernel_grid, RIGHT, buff=0.45)
        
        # ==========================================
        # PART 1: Show all elements
        # ==========================================
        
        self.play(
            LaggedStartMap(FadeIn, input_grid, lag_ratio=0.02),
            run_time=1.5
        )
        
        self.play(Write(asterisk))
        
        self.play(
            LaggedStartMap(FadeIn, kernel_grid, lag_ratio=0.05),
            run_time=1
        )
        
        self.play(Write(equals_sign))
        
        question_marks_group = VGroup(*[output_question_marks[(i, j)] for i in range(3) for j in range(3)])
        
        self.play(
            LaggedStartMap(FadeIn, output_grid, lag_ratio=0.05),
            LaggedStartMap(FadeIn, question_marks_group, lag_ratio=0.05),
            run_time=1
        )
        self.wait(1)

        # ==========================================
        # PART 2: Show stride label
        # ==========================================
        
        stride_label = Text("Stride = 2", font_size=42, weight=BOLD)
        stride_label.set_color(ORANGE)
        stride_label.to_edge(UP, buff=0.83).shift(UP*0.45)
        
        self.play(Write(stride_label), self.camera.frame.animate.shift(UP*0.55),run_time=1)
        self.wait(1)
        
        # ==========================================
        # PART 3: Fade symbols, move kernel over input
        # ==========================================
        
        self.play(
            FadeOut(asterisk),
            FadeOut(equals_sign),
            run_time=0.8
        )
        
        # Make kernel semi-transparent
        self.play(
            *[kernel_cells[(i, j)][0].animate.set_fill(YELLOW, opacity=0.5)
              for i in range(3) for j in range(3)],
            run_time=0.5
        )
        
        # Position kernel at first position (center at 1,1)
        first_center = input_cells[(1, 1)][0].get_center()
        
        self.play(
            kernel_grid.animate.move_to(first_center),
            run_time=1
        )
        self.wait(0.5)
        
        # ==========================================
        # PART 4: Perform stride=2 convolution
        # ==========================================
        
        def compute_conv(input_vals, kernel_vals, row, col):
            total = 0
            for ki in range(3):
                for kj in range(3):
                    total += input_vals[row + ki, col + kj] * kernel_vals[ki, kj]
            return total
        
        stride = 2
        
        # Kernel positions with stride=2:
        # Top-left of kernel at: (0,0), (0,2), (0,4)
        #                        (2,0), (2,2), (2,4)
        #                        (4,0), (4,2), (4,4)
        # Kernel center at: (1,1), (1,3), (1,5)
        #                   (3,1), (3,3), (3,5)
        #                   (5,1), (5,3), (5,5)
        
        for out_row in range(3):
            for out_col in range(3):
                # Top-left corner of kernel
                kernel_top_left_i = out_row * stride
                kernel_top_left_j = out_col * stride
                
                # Kernel center for positioning
                kernel_center_i = kernel_top_left_i + 1
                kernel_center_j = kernel_top_left_j + 1
                
                # Get target position
                target_center = input_cells[(kernel_center_i, kernel_center_j)][0].get_center()
                
                # Move kernel (skip first since already there)
                if not (out_row == 0 and out_col == 0):
                    self.play(
                        kernel_grid.animate.move_to(target_center),
                        run_time=0.6
                    )
                
                # Calculate convolution value
                conv_val = compute_conv(input_values, kernel_values, kernel_top_left_i, kernel_top_left_j)
                
                # Create result text
                result_val = Text(str(conv_val), font_size=22, weight=BOLD)
                result_val.set_color(WHITE)
                result_val.move_to(output_cells[(out_row, out_col)].get_center())
                
                old_q = output_question_marks[(out_row, out_col)]
                
                # TransformFromCopy from kernel to output
                self.play(
                    TransformFromCopy(kernel_grid, result_val),
                    FadeOut(old_q),
                    run_time=0.6
                )
                
                # Add result to output_grid
                output_grid.add(result_val)
        
        self.wait(1)
        
        # ==========================================
        # PART 5: Restore kernel and show final layout
        # ==========================================
        
        # Move kernel back
        self.play(
            kernel_grid.animate.next_to(asterisk, RIGHT, buff=0.46),
            run_time=0.8
        )
        
        # Restore kernel opacity
        self.play(
            *[kernel_cells[(i, j)][0].animate.set_fill(YELLOW, opacity=1)
              for i in range(3) for j in range(3)],
            run_time=0.5
        )
        
        # Fade in symbols and kernel label
        self.play(
            FadeIn(asterisk),
            FadeIn(equals_sign),
            run_time=0.8
        )
        
        self.wait(1)


        # ==========================================
        # PART 6: Show formula
        # ==========================================
        
        formula = Tex(r"\frac{n + 2p - f}{s} + 1", font_size=42)
        formula[3].set_color(RED_B)    # p
        formula[5].set_color(YELLOW)     # f
        formula[7].set_color(ORANGE)     # s
        formula.scale(1.6)
        formula.to_edge(DOWN).shift(DOWN*0.95)

        self.camera.frame.save_state()
        
        self.play(
            FadeOut(stride_label),
            self.camera.frame.animate.shift(DOWN*1.87),
            Write(formula)
        )

        self.wait(1)

        temp = Tex(r"\left\lfloor \frac{n + 2p - f}{s} \right\rfloor + 1", font_size=42).scale(1.5)
        temp.move_to(formula)
        temp[4].set_color(RED_B)
        temp[6].set_color(YELLOW)
        temp[8].set_color(ORANGE)

        self.play(
            Transform(formula,
                      temp)
        )


        self.wait(2)

        self.play(FadeOut(formula), self.camera.frame.animate.restore().shift(DOWN*0.899+LEFT))
        
        brace = Brace(input_grid, LEFT, buff=0.45)
        brace1 = Brace(input_grid, DOWN, buff=0.45)

        a = Tex("n_h").next_to(brace, LEFT, buff=0.45).scale(1.7)
        b = Tex("n_w").next_to(brace1, DOWN, buff=0.45).scale(1.7)

        self.play(GrowFromCenter(brace), GrowFromCenter(brace1), ShowCreation(a), ShowCreation(b))
        self.wait(2)

        formula_h = Tex(r"n_{out}^{h} = \left\lfloor \frac{n_h + 2p - f_h}{s} \right\rfloor + 1", font_size=42)

        formula_w = Tex(r"n_{out}^{w} = \left\lfloor \frac{n_w + 2p - f_w}{s} \right\rfloor + 1", font_size=42)
    
        self.play(FadeOut(brace), FadeOut(brace1), FadeOut(a), FadeOut(b), self.camera.frame.animate.restore().shift(DOWN*1.6))

        formula_h = Tex(r"n_{out}^{h} = \left\lfloor \frac{n_h + 2p - f}{s} \right\rfloor + 1", font_size=42)

        formula_w = Tex(r"n_{out}^{w} = \left\lfloor \frac{n_w + 2p - f}{s} \right\rfloor + 1", font_size=42)
    
        formula_h.next_to(input_grid, DOWN, buff=0.45).shift(DOWN*0.5).scale(1.2)
        formula_w.scale(1.2).next_to(formula_h, RIGHT, buff=0.9)
        self.play(ShowCreation(formula_h), ShowCreation(formula_w))
        
        rect1 = SurroundingRectangle(formula_w, stroke_width=5).scale(1.09).set_color(RED_D)
        rect2 = SurroundingRectangle(formula_h, stroke_width=5).scale(1.09).set_color(RED_D)

        self.play(ShowCreation(rect1), ShowCreation(rect2))
        self.wait(2)


class Convolution_Over_Volume(Scene):
    
    def construct(self):

        self.camera.frame.shift(LEFT*0.32+UP*0.2)
        # ==========================================
        # SETUP: Create 6x6x3 Input Volume (RGB)
        # ==========================================
        
        cell_size = 0.45
        depth_offset = 0.25  # Offset for 3D effect
        
        # Colors for each channel (fill and stroke)
        channel_colors = [RED, GREEN, BLUE]
        stroke_colors = ["#ff0000", "#00ff00", "#0000ff"]
        channel_names = ["R", "G", "B"]
        
        # ==========================================
        # Create RED layer (channel 0)
        # ==========================================
        red_layer = VGroup()
        for i in range(6):
            for j in range(6):
                cell = Square(side_length=cell_size)
                cell.set_fill(RED, opacity=0.9)
                cell.set_stroke("#ff0000", width=1.5)
                
                x_pos = j * cell_size + (2 - 0) * depth_offset
                y_pos = -i * cell_size + (2 - 0) * depth_offset
                cell.move_to(RIGHT * x_pos + UP * y_pos)
                
                red_layer.add(cell)
        
        # ==========================================
        # Create GREEN layer (channel 1)
        # ==========================================
        green_layer = VGroup()
        for i in range(6):
            for j in range(6):
                cell = Square(side_length=cell_size)
                cell.set_fill(GREEN, opacity=0.9)
                cell.set_stroke("#00ff00", width=1.5)
                
                x_pos = j * cell_size + (2 - 1) * depth_offset
                y_pos = -i * cell_size + (2 - 1) * depth_offset
                cell.move_to(RIGHT * x_pos + UP * y_pos)
                
                green_layer.add(cell)
        
        # ==========================================
        # Create BLUE layer (channel 2)
        # ==========================================
        blue_layer = VGroup()
        for i in range(6):
            for j in range(6):
                cell = Square(side_length=cell_size)
                cell.set_fill(BLUE, opacity=0.9)
                cell.set_stroke("#0000ff", width=1.5)
                
                x_pos = j * cell_size + (2 - 2) * depth_offset
                y_pos = -i * cell_size + (2 - 2) * depth_offset
                cell.move_to(RIGHT * x_pos + UP * y_pos)
                
                blue_layer.add(cell)
        
        # Group all layers
        input_volume = VGroup(red_layer, green_layer, blue_layer)
        input_volume.center()
        input_volume.move_to(LEFT * 4)
        
        # Set z_index so front layers appear on top
        red_layer.set_z_index(3)    # Red (front)
        green_layer.set_z_index(2)  # Green (middle)
        blue_layer.set_z_index(1)   # Blue (back)
        
        input_label = Text("6 x 6 x 3", font_size=32, weight=BOLD)
        input_label.next_to(input_volume, UP, buff=1)
        
        rgb_label = Text("(RGB Image)", font_size=24)
        rgb_label.set_color(GREY_A)
        rgb_label.next_to(input_label, DOWN, buff=0.35)
        
        # ==========================================
        # SETUP: Create RED Filter (3x3)
        # ==========================================
        red_filter = VGroup()
        for i in range(3):
            for j in range(3):
                cell = Square(side_length=cell_size)
                cell.set_fill(YELLOW, opacity=0.85)
                cell.set_stroke("#ffff00", width=2)
                
                # Position relative to center, with depth offset for 3D stacking
                x_pos = (j - 1) * cell_size + (2 - 0) * depth_offset
                y_pos = -(i - 1) * cell_size + (2 - 0) * depth_offset
                cell.move_to(RIGHT * x_pos + UP * y_pos)
                
                red_filter.add(cell)
        
        red_filter.set_z_index(3.5)  # Above red layer (3)
        
        # ==========================================
        # SETUP: Create GREEN Filter (3x3)
        # ==========================================
        green_filter = VGroup()
        for i in range(3):
            for j in range(3):
                cell = Square(side_length=cell_size)
                cell.set_fill(YELLOW, opacity=0.85)
                cell.set_stroke("#ffff00", width=2)
                
                # Position relative to center, with depth offset for 3D stacking
                x_pos = (j - 1) * cell_size + (2 - 1) * depth_offset
                y_pos = -(i - 1) * cell_size + (2 - 1) * depth_offset
                cell.move_to(RIGHT * x_pos + UP * y_pos)
                
                green_filter.add(cell)
        
        green_filter.set_z_index(2.5)  # Above green layer (2)
        
        # ==========================================
        # SETUP: Create BLUE Filter (3x3)
        # ==========================================
        blue_filter = VGroup()
        for i in range(3):
            for j in range(3):
                cell = Square(side_length=cell_size)
                cell.set_fill(YELLOW, opacity=0.85)
                cell.set_stroke("#ffff00", width=2)
                
                # Position relative to center, with depth offset for 3D stacking
                x_pos = (j - 1) * cell_size + (2 - 2) * depth_offset
                y_pos = -(i - 1) * cell_size + (2 - 2) * depth_offset
                cell.move_to(RIGHT * x_pos + UP * y_pos)
                
                blue_filter.add(cell)
        
        blue_filter.set_z_index(1.5)  # Above blue layer (1)
        
        # Group all filters
        all_filters = VGroup(red_filter, green_filter, blue_filter)
        
        filter_label = Text("3 x 3 x 3", font_size=32, weight=BOLD)
        filter_label.set_color(YELLOW)
        filter_label.next_to(all_filters, UP, buff=1)
        
        filter_sublabel = Text("(Filter)", font_size=24)
        filter_sublabel.set_color(YELLOW_A)
        filter_sublabel.next_to(filter_label, DOWN, buff=0.35)
        
        # ==========================================
        # SETUP: Create 4x4 Output (White)
        # ==========================================
        
        output_grid = VGroup()
        output_cells = {}
        
        for i in range(4):
            for j in range(4):
                cell = Square(side_length=cell_size)
                cell.set_fill(WHITE, opacity=0.3)
                cell.set_stroke("#ffffff", width=2)
                cell.move_to(RIGHT * j * cell_size + DOWN * i * cell_size)
                
                output_cells[(i, j)] = cell
                output_grid.add(cell)
        
        output_grid.center()
        output_grid.move_to(RIGHT * 4)
        
        output_label = Text("4 x 4", font_size=32, weight=BOLD)
        output_label.set_color(WHITE)
        output_label.next_to(output_grid, UP, buff=1)
        
        output_sublabel = Text("(Output)", font_size=24)
        output_sublabel.set_color(GREY_A)
        output_sublabel.next_to(output_label, DOWN, buff=0.35)
        
        # ==========================================
        # SETUP: Symbols
        # ==========================================
        
        asterisk = Tex(r"*", font_size=72)
        asterisk.set_color(WHITE)
        asterisk.move_to(LEFT * 1.8)
        
        equals_sign = Tex(r"=", font_size=72)
        equals_sign.set_color(WHITE)
        equals_sign.move_to(RIGHT * 1.8)
        
        # ==========================================
        # PART 1: Show input volume layer by layer
        # ==========================================
        
        # Show blue layer first (back)
        self.play(
            LaggedStartMap(FadeIn, blue_layer, lag_ratio=0.02),
            run_time=1
        )
        
        # Show green layer (middle)
        self.play(
            LaggedStartMap(FadeIn, green_layer, lag_ratio=0.02),
            run_time=1
        )
        
        # Show red layer (front)
        self.play(
            LaggedStartMap(FadeIn, red_layer, lag_ratio=0.02),
            run_time=1
        )
        
        self.play(
            Write(input_label),
            FadeIn(rgb_label),
            run_time=1
        )
        self.wait(0.5)
        
        # ==========================================
        # PART 2: Show filter and symbols
        # ==========================================
        
        self.play(Write(asterisk), run_time=0.5)
        
        self.play(
            LaggedStartMap(FadeIn, all_filters, lag_ratio=0.03),
            run_time=1.5
        )
        
        self.play(
            Write(filter_label),
            FadeIn(filter_sublabel),
            run_time=1
        )
        self.wait(0.5)
        
        # ==========================================
        # PART 3: Show output grid
        # ==========================================
        equals_sign.shift(RIGHT*0.3)
        self.play(Write(equals_sign), run_time=0.5)
        
        self.play(
            LaggedStartMap(FadeIn, output_grid, lag_ratio=0.05),
            run_time=1
        )
        
        self.play(
            Write(output_label),
            FadeIn(output_sublabel),
            run_time=1
        )
        self.wait(1)

        
        # ==========================================
        # PART 4: Move filters over input and convolve
        # ==========================================
        
        # Store initial position of filters
        initial_filter_position = all_filters.get_center()
        
        self.play(
            FadeOut(asterisk),
            FadeOut(equals_sign),
            FadeOut(filter_label),
            FadeOut(filter_sublabel),
            run_time=0.8
        )
        
        # Make filters fully opaque (0.99) and reduce input layer opacity to 0.4
        self.play(
            *[cell.animate.set_fill(YELLOW, opacity=0.99) for cell in red_filter],
            *[cell.animate.set_fill(YELLOW, opacity=0.99) for cell in green_filter],
            *[cell.animate.set_fill(YELLOW, opacity=0.99) for cell in blue_filter],
            *[cell.animate.set_fill(RED, opacity=0.4) for cell in red_layer],
            *[cell.animate.set_fill(GREEN, opacity=0.4) for cell in green_layer],
            *[cell.animate.set_fill(BLUE, opacity=0.4) for cell in blue_layer],
            run_time=0.5
        )
        
        # Calculate first position (kernel center at 1,1 of each layer)
        red_first_pos = red_layer[7].get_center()      # Cell (1,1) of red layer
        green_first_pos = green_layer[7].get_center()  # Cell (1,1) of green layer
        blue_first_pos = blue_layer[7].get_center()    # Cell (1,1) of blue layer
        
        # Move all three filters to their starting positions simultaneously
        self.play(
            red_filter.animate.move_to(red_first_pos),
            green_filter.animate.move_to(green_first_pos),
            blue_filter.animate.move_to(blue_first_pos),
            run_time=1
        )
        self.wait(0.5)
        
        # ==========================================
        # PART 5: Convolve - fill output cells
        # ==========================================
        
        # Iterate through 4x4 output positions
        for out_row in range(4):
            for out_col in range(4):
                # Calculate filter positions for all channels
                target_cell_idx = (out_row + 1) * 6 + (out_col + 1)
                
                red_target_pos = red_layer[target_cell_idx].get_center()
                green_target_pos = green_layer[target_cell_idx].get_center()
                blue_target_pos = blue_layer[target_cell_idx].get_center()
                
                # Move all filters simultaneously (skip first position)
                if not (out_row == 0 and out_col == 0):
                    self.play(
                        red_filter.animate.move_to(red_target_pos),
                        green_filter.animate.move_to(green_target_pos),
                        blue_filter.animate.move_to(blue_target_pos),
                        run_time=0.35
                    )
                
                # Fill output cell
                self.play(
                    output_cells[(out_row, out_col)].animate.set_fill(WHITE, opacity=0.9),
                    run_time=0.25
                )
        
        self.wait(1)
        
        # ==========================================
        # PART 6: Restore filter and final layout
        # ==========================================
        
        
        # Restore filter and input layer opacities
        self.play(
            *[cell.animate.set_fill(RED, opacity=0.9) for cell in red_layer],
            *[cell.animate.set_fill(GREEN, opacity=0.9) for cell in green_layer],
            *[cell.animate.set_fill(BLUE, opacity=0.9) for cell in blue_layer],
            VGroup(red_filter, blue_filter, green_filter).animate.next_to(asterisk, RIGHT, buff=0.8) ,
            run_time=0.5
        )
        self.play(
            *[cell.animate.set_fill(YELLOW, opacity=0.9) for cell in red_filter],
            *[cell.animate.set_fill(YELLOW, opacity=0.9) for cell in green_filter],
            *[cell.animate.set_fill(YELLOW, opacity=0.9) for cell in blue_filter],
        )
        
        self.play(
            FadeIn(asterisk),
            FadeIn(equals_sign),
            FadeIn(filter_label),
            FadeIn(filter_sublabel),
            run_time=0.8
        )
        
        self.wait(1)
        
        # ==========================================
        # PART 7: Key insight text
        # ==========================================
        
        insight = Text("3D Filter collapses volume → 2D Output", font_size=40, weight=BOLD)
        insight.set_color(TEAL_B)
        insight.to_edge(DOWN, buff=0.8)
        
        self.play(Write(insight), self.camera.frame.animate.shift(DOWN*0.5),run_time=1.5)
        
        self.wait(2)

        self.camera.frame.save_state()

        self.play(
            FadeOut(insight),
            FadeOut(output_label),
            FadeOut(filter_label),
            FadeOut(input_label),
            FadeOut(output_sublabel),
            FadeOut(filter_sublabel),
            FadeOut(rgb_label),
            FadeOut(output_grid),
        )

        # ==========================================
        # PART 8: Create Purple and Maroon Filters + Outputs
        # ==========================================
        
        def create_filter_set(filter_color, stroke_color, base_z_index):
            """Helper function to create a 3x3x3 filter set"""
            red_filter_layer = VGroup()
            for i in range(3):
                for j in range(3):
                    cell = Square(side_length=cell_size)
                    cell.set_fill(filter_color, opacity=0.85)
                    cell.set_stroke(stroke_color, width=2)
                    
                    x_pos = (j - 1) * cell_size + (2 - 0) * depth_offset
                    y_pos = -(i - 1) * cell_size + (2 - 0) * depth_offset
                    cell.move_to(RIGHT * x_pos + UP * y_pos)
                    
                    red_filter_layer.add(cell)
            
            red_filter_layer.set_z_index(base_z_index + 0.5)
            
            green_filter_layer = VGroup()
            for i in range(3):
                for j in range(3):
                    cell = Square(side_length=cell_size)
                    cell.set_fill(filter_color, opacity=0.85)
                    cell.set_stroke(stroke_color, width=2)
                    
                    x_pos = (j - 1) * cell_size + (2 - 1) * depth_offset
                    y_pos = -(i - 1) * cell_size + (2 - 1) * depth_offset
                    cell.move_to(RIGHT * x_pos + UP * y_pos)
                    
                    green_filter_layer.add(cell)
            
            green_filter_layer.set_z_index(base_z_index - 0.5)
            
            blue_filter_layer = VGroup()
            for i in range(3):
                for j in range(3):
                    cell = Square(side_length=cell_size)
                    cell.set_fill(filter_color, opacity=0.85)
                    cell.set_stroke(stroke_color, width=2)
                    
                    x_pos = (j - 1) * cell_size + (2 - 2) * depth_offset
                    y_pos = -(i - 1) * cell_size + (2 - 2) * depth_offset
                    cell.move_to(RIGHT * x_pos + UP * y_pos)
                    
                    blue_filter_layer.add(cell)
            
            blue_filter_layer.set_z_index(base_z_index - 1.5)
            
            return VGroup(red_filter_layer, green_filter_layer, blue_filter_layer)
        
        def create_output_grid_filled(fill_color, stroke_color, opacity=0.9):
            """Helper function to create a 4x4 output grid (already filled)"""
            output_grid_new = VGroup()
            
            for i in range(4):
                for j in range(4):
                    cell = Square(side_length=cell_size)
                    cell.set_fill(fill_color, opacity=opacity)
                    cell.set_stroke(stroke_color, width=2)
                    cell.move_to(RIGHT * j * cell_size + DOWN * i * cell_size)
                    
                    output_grid_new.add(cell)
            
            output_grid_new.center()
            return output_grid_new
        
        # Create purple and maroon filter sets
        purple_filters = create_filter_set(PURPLE, "#9370db", 4)
        maroon_filters = create_filter_set(MAROON, "#800000", 0.5)
        
        # Position filters (purple above yellow, maroon below yellow)
        yellow_position = VGroup(red_filter, green_filter, blue_filter).get_center()
        
        purple_filters.move_to(yellow_position + UP * 1.5).shift(UP*0.66)
        maroon_filters.move_to(yellow_position + DOWN * 1.5).shift(DOWN*0.66)
        
        # Create output grids (already filled)
        purple_output = create_output_grid_filled(PURPLE, "#9370db", opacity=0.9)
        maroon_output = create_output_grid_filled(MAROON, "#800000", opacity=0.9)
        
        # Position output grids
        output_position = RIGHT * 4  # Same x position as original output grid
        purple_output.move_to(output_position + UP * 2.3).set_z_index(10)
        maroon_output.move_to(output_position + DOWN * 2.3).set_z_index(-1)
        
        # ==========================================
        # PART 9: Fade in purple and maroon filters with outputs
        # ==========================================
        
        self.play(
            LaggedStartMap(FadeIn, purple_filters, lag_ratio=0.03),
            LaggedStartMap(FadeIn, purple_output, lag_ratio=0.05),
            run_time=1.5
        )
        
        self.wait(0.5)
        
        self.play(
            LaggedStartMap(FadeIn, maroon_filters, lag_ratio=0.03),
            LaggedStartMap(FadeIn, maroon_output, lag_ratio=0.05),
            run_time=1.5
        )
        
        self.wait(1)
        
        # ==========================================
        # PART 10: Stack all output grids together
        # ==========================================
        
        # Recreate the yellow output grid at its current position
        yellow_output = VGroup()
        for i in range(4):
            for j in range(4):
                cell = Square(side_length=cell_size)
                cell.set_fill(YELLOW, opacity=0.9)
                cell.set_stroke("#ffff00", width=2)
                cell.move_to(RIGHT * j * cell_size + DOWN * i * cell_size)
                yellow_output.add(cell)
        
        yellow_output.center()
        yellow_output.move_to(output_position).set_z_index(4)
        
        # Fade in the yellow output
        self.play(LaggedStartMap(FadeIn, yellow_output, lag_ratio=0.05), run_time=1)
        
        self.wait(0.5)
        
        # Stack all three outputs together with 3D depth effect
        stacked_center = output_position
        
        self.play(
            purple_output.animate.move_to(stacked_center + UP * 0.4 + RIGHT * 0.4),
            yellow_output.animate.move_to(stacked_center),
            maroon_output.animate.move_to(stacked_center + DOWN * 0.4 + LEFT * 0.4),
            run_time=1.5
        )
        
        self.wait(1)

        
        # ==========================================
        # PART 11: Final insight
        # ==========================================
        
        insight2 = Text("Multiple Filters → Multiple Feature Maps", font_size=42, weight=BOLD)
        insight2.set_color(TEAL_B)
        insight2.to_edge(DOWN, buff=0.8).shift(DOWN*0.99)
        
        self.play(Write(insight2), self.camera.frame.animate.scale(1.1).shift(DOWN*0.4) ,run_time=1.5)
        
        self.wait(2)

class EdgeDetection(Scene):
    
    def construct(self):

        self.camera.frame.scale(1.05).shift(UP * 0.3)
        self.camera.frame.shift(LEFT*1.6).scale(0.85)
        
        # ==========================================
        # SETUP: Create input image with clear vertical edge (6x6)
        # Left half = 60, Right half = 220
        # ==========================================
        
        # Input with clear vertical edge (left 60, right 220)
        input_values = np.array([
            [60, 60, 60, 220, 220, 220],
            [60, 60, 60, 220, 220, 220],
            [60, 60, 60, 220, 220, 220],
            [60, 60, 60, 220, 220, 220],
            [60, 60, 60, 220, 220, 220],
            [60, 60, 60, 220, 220, 220]
        ])
        
        cell_size = 0.6
        
        # Create input grid
        input_grid = VGroup()
        input_cells = {}
        input_texts = {}
        
        for i in range(6):
            for j in range(6):
                cell = Square(side_length=cell_size)
                cell.set_fill(WHITE, opacity=1)
                cell.set_stroke(BLACK, width=2)
                cell.move_to(RIGHT * j * cell_size + DOWN * i * cell_size)
                
                value = Text(str(input_values[i, j]), font_size=18, weight=BOLD)
                value.set_color(BLACK)
                value.move_to(cell.get_center())
                
                cell_group = VGroup(cell, value)
                input_cells[(i, j)] = cell_group
                input_texts[(i, j)] = value
                input_grid.add(cell_group)
        
        input_grid.center()
        input_grid.move_to(LEFT * 5)
        
        input_label = Text("Input", font_size=32, weight=BOLD)
        input_label.next_to(input_grid, UP, buff=0.3)
        
        # ==========================================
        # SETUP: Vertical edge detection kernel (3x3)
        # ==========================================
        
        vertical_kernel = np.array([
            [-1, 0, 1],
            [-1, 0, 1],
            [-1, 0, 1]
        ])
        
        kernel_grid = VGroup()
        kernel_cells = {}
        kernel_texts = {}
        
        for i in range(3):
            for j in range(3):
                cell = Square(side_length=cell_size)
                cell.set_fill(YELLOW, opacity=1)
                cell.set_stroke(BLACK, width=2)
                cell.move_to(RIGHT * j * cell_size + DOWN * i * cell_size)
                
                val = vertical_kernel[i, j]
                value = Text(str(val), font_size=20, weight=BOLD)
                value.set_color(BLACK)
                value.move_to(cell.get_center())
                
                cell_group = VGroup(cell, value)
                kernel_cells[(i, j)] = cell_group
                kernel_texts[(i, j)] = value
                kernel_grid.add(cell_group)
        
        kernel_grid.center()
        
        # Position kernel using next_to from asterisk
        asterisk = Tex(r"*", font_size=60)
        asterisk.next_to(input_grid, RIGHT, buff=0.5)
        kernel_grid.next_to(asterisk, RIGHT, buff=0.5)
        kernel_grid.set_z_index(4)
        
        kernel_label = Text("Vertical\n Filter", font_size=26, weight=BOLD)
        kernel_label.set_color(YELLOW)
        kernel_label.next_to(kernel_grid, UP, buff=0.3)
        
        # ==========================================
        # SETUP: Output grid (4x4)
        # ==========================================
        
        output_grid = VGroup()
        output_cells = {}
        output_texts = {}
        
        for i in range(4):
            for j in range(4):
                cell = Square(side_length=cell_size)
                cell.set_fill(WHITE, opacity=1)
                cell.set_stroke(BLACK, width=2)
                cell.move_to(RIGHT * j * cell_size + DOWN * i * cell_size)
                
                value = Text("?", font_size=20, weight=BOLD)
                value.set_color(BLACK)
                value.move_to(cell.get_center())
                
                output_grid.add(cell)
                output_cells[(i, j)] = cell
                output_texts[(i, j)] = value
        
        output_grid.center()
        
        # Position equals and output using next_to
        equals_sign = Tex(r"=", font_size=60)
        equals_sign.next_to(kernel_grid, RIGHT, buff=0.5)
        output_grid.next_to(equals_sign, RIGHT, buff=0.5)
        
        # Position question marks
        for i in range(4):
            for j in range(4):
                output_texts[(i, j)].move_to(output_cells[(i, j)].get_center())
        
        output_label = Text("Output", font_size=32, weight=BOLD)
        output_label.next_to(output_grid, UP, buff=0.3)
        
        # ==========================================
        # PART 1: Show all elements
        # ==========================================
        
        self.play(
            LaggedStartMap(FadeIn, input_grid, lag_ratio=0.02),
            Write(input_label),
            run_time=1.2
        )
        
        self.play(Write(asterisk), run_time=0.5)
        
        self.play(
            LaggedStartMap(FadeIn, kernel_grid, lag_ratio=0.05),
            Write(kernel_label),
            run_time=1
        )
        
        self.play(Write(equals_sign), run_time=0.5)
        
        question_marks = VGroup(*[output_texts[(i, j)] for i in range(4) for j in range(4)])
        self.play(
            LaggedStartMap(FadeIn, output_grid, lag_ratio=0.03),
            LaggedStartMap(FadeIn, question_marks, lag_ratio=0.03),
            Write(output_label),
            run_time=1
        )
        
        self.wait(1)

        # ==========================================
        # PART 2: Perform convolution
        # ==========================================
        
        self.play(
            FadeOut(asterisk), FadeOut(equals_sign), FadeOut(kernel_label),
            run_time=0.5
        )
        
        # Make kernel transparent
        self.play(
            *[kernel_cells[(i, j)][0].animate.set_fill(YELLOW, opacity=0.5)
              for i in range(3) for j in range(3)],
            run_time=0.4
        )
        
        def compute_conv(input_vals, kernel_vals, row, col):
            total = 0
            for ki in range(3):
                for kj in range(3):
                    total += input_vals[row + ki, col + kj] * kernel_vals[ki, kj]
            return total
        
        # Store output values for visualization
        output_values = np.zeros((4, 4), dtype=int)
        output_result_texts = {}
        
        for out_row in range(4):
            for out_col in range(4):
                # Move kernel
                center_pos = input_cells[(out_row + 1, out_col + 1)][0].get_center()
                
                self.play(
                    kernel_grid.animate.move_to(center_pos),
                    run_time=0.3
                )
                
                # Calculate value
                conv_val = compute_conv(input_values, vertical_kernel, out_row, out_col)
                output_values[out_row, out_col] = conv_val
                
                # Create result - plain white cell, black text
                result_val = Text(str(conv_val), font_size=18, weight=BOLD)
                result_val.set_color(BLACK)
                result_val.move_to(output_cells[(out_row, out_col)].get_center())
                
                old_q = output_texts[(out_row, out_col)]
                
                self.play(
                    TransformFromCopy(kernel_grid, result_val),
                    FadeOut(old_q),
                    run_time=0.3
                )
                
                output_result_texts[(out_row, out_col)] = result_val
                output_grid.add(result_val)
        
        self.wait(0.5)
        
        # Restore kernel opacity
        self.play(
            *[kernel_cells[(i, j)][0].animate.set_fill(YELLOW, opacity=1)
              for i in range(3) for j in range(3)],
            run_time=0.4
        )
        
        # Move kernel back to next_to(asterisk, RIGHT, buff=0.5)
        self.play(FadeIn(asterisk), run_time=0.3)
        
        # Calculate target position
        kernel_target = asterisk.get_right() + RIGHT * 0.5 + RIGHT * kernel_grid.get_width() / 2
        
        self.play(
            kernel_grid.animate.move_to(kernel_target),
            run_time=0.6
        )
        
        # Update kernel_label position
        kernel_label.next_to(kernel_grid, UP, buff=0.3)
        
        self.play(
            FadeIn(equals_sign), FadeIn(kernel_label),
            run_time=0.5
        )
        
        self.wait(1)

        self.camera.frame.save_state()


        # ==========================================
        # PART 3: Show real grayscale images below
        # ==========================================
        
        self.play(self.camera.frame.animate.shift(DOWN * 1.46).scale(1.15), run_time=1)
        
        # Create "Real Image" visualization below
        real_label = Text("Actual Grayscale Images:", font_size=28, weight=BOLD)
        real_label.set_color(BLUE)
        real_label.move_to(DOWN * 2.8 + LEFT * 0.5)
        
        # Create small grayscale input image representation
        small_cell = 0.35
        
        # Input image (grayscale) - use actual pixel values 60 and 220
        real_input = VGroup()
        for i in range(6):
            for j in range(6):
                cell = Square(side_length=small_cell)
                brightness = input_values[i, j] / 255.0  # Use actual pixel value
                cell.set_fill(interpolate_color(BLACK, WHITE, brightness), opacity=1)
                cell.set_stroke(BLACK, width=0.5)
                cell.move_to(RIGHT * j * small_cell + DOWN * i * small_cell)
                real_input.add(cell)
        real_input.center()
        real_input.next_to(input_grid, DOWN, buff=0.67)
        

        # Filter visualization - YELLOW color for vertical filter
        real_filter = VGroup()
        for i in range(3):
            for j in range(3):
                cell = Square(side_length=small_cell)
                val = vertical_kernel[i, j]
                if val == -1:
                    cell.set_fill(BLACK, opacity=1)
                elif val == 0:
                    cell.set_fill(GREY, opacity=1)
                else:
                    cell.set_fill(WHITE, opacity=1)
                cell.set_stroke(YELLOW, width=2)
                cell.move_to(RIGHT * j * small_cell + DOWN * i * small_cell)
                real_filter.add(cell)
        real_filter.center()
        real_filter.next_to(kernel_grid, DOWN, buff=1).shift(DOWN*1.1).scale(1.4)
        

        # Output visualization (edge detected) - use GREY and WHITE (not black)
        real_output = VGroup()
        out_min = np.min(output_values)
        out_max = np.max(output_values)
        out_range = out_max - out_min if out_max != out_min else 1
        
        for i in range(4):
            for j in range(4):
                cell = Square(side_length=small_cell)
                val = output_values[i, j]
                # Normalize to 0-1 range, then map GREY to WHITE
                normalized = (val - out_min) / out_range
                cell.set_fill(interpolate_color(GREY, WHITE, normalized), opacity=1)
                cell.set_stroke(BLACK, width=0.5)
                cell.move_to(RIGHT * j * small_cell + DOWN * i * small_cell)
                real_output.add(cell)
        real_output.center()
        real_output.next_to(output_grid, DOWN, buff=1.54).scale(1.34)
        
        real_output_label = Text("Edge Detected", font_size=27, weight=BOLD)
        real_output_label.set_color(GREEN)
        real_output_label.next_to(real_output, UP, buff=0.2)
        

        self.play(
            FadeIn(real_input),
            run_time=0.8
        )
        self.play(
            FadeIn(real_filter), 
            run_time=0.8
        )
        self.play(
            FadeIn(real_output), Write(real_output_label),
            run_time=0.8
        )

        self.wait(2)


        # ==========================================
        # PART 4: Transition to Horizontal Edge Detection
        # ==========================================
        
        transition_text = Text("Now: Horizontal Edge Detection", font_size=36, weight=BOLD)
        transition_text.set_color(ORANGE)
        transition_text.move_to(UP * 0.5)
        
        # Fade out current scene
        self.play(
            FadeOut(input_grid), FadeOut(input_label),
            FadeOut(kernel_grid), FadeOut(kernel_label),
            FadeOut(output_grid), FadeOut(output_label),
            FadeOut(asterisk), FadeOut(equals_sign),
            FadeOut(real_input), 
            FadeOut(real_filter), 
            FadeOut(real_output), FadeOut(real_output_label),
            run_time=1
        )
        
        transition_text.shift(LEFT*1.44)
        self.play(Write(transition_text), run_time=1)
        self.wait(1)
  

        # ==========================================
        # PART 5: Create Horizontal Edge Input (top 60, bottom 220)
        # ==========================================
        
        horiz_input_values = np.array([
            [60, 60, 60, 60, 60, 60],
            [60, 60, 60, 60, 60, 60],
            [60, 60, 60, 60, 60, 60],
            [220, 220, 220, 220, 220, 220],
            [220, 220, 220, 220, 220, 220],
            [220, 220, 220, 220, 220, 220]
        ])
        
        # Create new input grid
        horiz_input_grid = VGroup()
        horiz_input_cells = {}
        horiz_input_texts = {}
        
        for i in range(6):
            for j in range(6):
                cell = Square(side_length=cell_size)
                cell.set_fill(WHITE, opacity=1)
                cell.set_stroke(BLACK, width=2)
                cell.move_to(RIGHT * j * cell_size + DOWN * i * cell_size)
                
                value = Text(str(horiz_input_values[i, j]), font_size=18, weight=BOLD)
                value.set_color(BLACK)
                value.move_to(cell.get_center())
                
                cell_group = VGroup(cell, value)
                horiz_input_cells[(i, j)] = cell_group
                horiz_input_texts[(i, j)] = value
                horiz_input_grid.add(cell_group)
        
        horiz_input_grid.center()
        horiz_input_grid.move_to(LEFT * 5)
        
        horiz_input_label = Text("Input", font_size=32, weight=BOLD)
        horiz_input_label.next_to(horiz_input_grid, UP, buff=0.3)
        
        # Horizontal kernel
        horizontal_kernel = np.array([
            [-1, -1, -1],
            [0, 0, 0],
            [1, 1, 1]
        ])
        
        horiz_kernel_grid = VGroup()
        horiz_kernel_cells = {}
        horiz_kernel_texts = {}
        
        for i in range(3):
            for j in range(3):
                cell = Square(side_length=cell_size)
                cell.set_fill(ORANGE, opacity=1)
                cell.set_stroke(BLACK, width=2)
                cell.move_to(RIGHT * j * cell_size + DOWN * i * cell_size)
                
                val = horizontal_kernel[i, j]
                value = Text(str(val), font_size=20, weight=BOLD)
                value.set_color(BLACK)
                value.move_to(cell.get_center())
                
                cell_group = VGroup(cell, value)
                horiz_kernel_cells[(i, j)] = cell_group
                horiz_kernel_texts[(i, j)] = value
                horiz_kernel_grid.add(cell_group)
        
        horiz_kernel_grid.center()
        
        # Position using next_to
        asterisk2 = Tex(r"*", font_size=60)
        asterisk2.next_to(horiz_input_grid, RIGHT, buff=0.5)
        horiz_kernel_grid.next_to(asterisk2, RIGHT, buff=0.5)
        horiz_kernel_grid.set_z_index(4)
        
        horiz_kernel_label = Text("Horizontal\n  Filter", font_size=26, weight=BOLD)
        horiz_kernel_label.set_color(ORANGE)
        horiz_kernel_label.next_to(horiz_kernel_grid, UP, buff=0.3)
        
        # New output grid
        horiz_output_grid = VGroup()
        horiz_output_cells = {}
        horiz_output_texts = {}
        
        for i in range(4):
            for j in range(4):
                cell = Square(side_length=cell_size)
                cell.set_fill(WHITE, opacity=1)
                cell.set_stroke(BLACK, width=2)
                cell.move_to(RIGHT * j * cell_size + DOWN * i * cell_size)
                
                value = Text("?", font_size=20, weight=BOLD)
                value.set_color(BLACK)
                value.move_to(cell.get_center())
                
                horiz_output_grid.add(cell)
                horiz_output_cells[(i, j)] = cell
                horiz_output_texts[(i, j)] = value
        
        horiz_output_grid.center()
        
        # Position using next_to
        equals_sign2 = Tex(r"=", font_size=60)
        equals_sign2.next_to(horiz_kernel_grid, RIGHT, buff=0.5)
        horiz_output_grid.next_to(equals_sign2, RIGHT, buff=0.5)
        
        for i in range(4):
            for j in range(4):
                horiz_output_texts[(i, j)].move_to(horiz_output_cells[(i, j)].get_center())
        
        horiz_output_label = Text("Output", font_size=32, weight=BOLD)
        horiz_output_label.next_to(horiz_output_grid, UP, buff=0.3)
        
        # Show all
        self.play(
            LaggedStartMap(FadeIn, horiz_input_grid, lag_ratio=0.02),
            Write(horiz_input_label),
            FadeOut(transition_text),self.camera.frame.animate.shift(UP * 1.65).scale(1/1.15) ,
            run_time=1
        )
        
        self.play(Write(asterisk2), run_time=0.4)
        
        self.play(
            LaggedStartMap(FadeIn, horiz_kernel_grid, lag_ratio=0.05),
            Write(horiz_kernel_label),
            run_time=0.8
        )
        
        self.play(Write(equals_sign2), run_time=0.4)
        
        horiz_questions = VGroup(*[horiz_output_texts[(i, j)] for i in range(4) for j in range(4)])
        self.play(
            LaggedStartMap(FadeIn, horiz_output_grid, lag_ratio=0.03),
            LaggedStartMap(FadeIn, horiz_questions, lag_ratio=0.03),
            Write(horiz_output_label),
            run_time=0.8
        )
        
        self.wait(1)

        # ==========================================
        # PART 6: Perform horizontal convolution
        # ==========================================
        
        self.play(
            FadeOut(asterisk2), FadeOut(equals_sign2), FadeOut(horiz_kernel_label),
            run_time=0.4
        )
        
        self.play(
            *[horiz_kernel_cells[(i, j)][0].animate.set_fill(ORANGE, opacity=0.5)
              for i in range(3) for j in range(3)],
            run_time=0.3
        )
        
        horiz_output_values = np.zeros((4, 4), dtype=int)
        horiz_output_result_texts = {}
        
        for out_row in range(4):
            for out_col in range(4):
                center_pos = horiz_input_cells[(out_row + 1, out_col + 1)][0].get_center()
                
                self.play(
                    horiz_kernel_grid.animate.move_to(center_pos),
                    run_time=0.25
                )
                
                conv_val = compute_conv(horiz_input_values, horizontal_kernel, out_row, out_col)
                horiz_output_values[out_row, out_col] = conv_val
                
                result_val = Text(str(conv_val), font_size=18, weight=BOLD)
                result_val.set_color(BLACK)
                result_val.move_to(horiz_output_cells[(out_row, out_col)].get_center())
                
                old_q = horiz_output_texts[(out_row, out_col)]
                
                self.play(
                    TransformFromCopy(horiz_kernel_grid, result_val),
                    FadeOut(old_q),
                    run_time=0.25
                )
                
                horiz_output_result_texts[(out_row, out_col)] = result_val
                horiz_output_grid.add(result_val)
        
        self.wait(0.5)
        
        # Restore kernel opacity
        self.play(
            *[horiz_kernel_cells[(i, j)][0].animate.set_fill(ORANGE, opacity=1)
              for i in range(3) for j in range(3)],
            run_time=0.4
        )
        
        # Move kernel back to next_to(asterisk2, RIGHT, buff=0.5)
        self.play(FadeIn(asterisk2), run_time=0.3)
        
        # Calculate target position
        horiz_kernel_target = asterisk2.get_right() + RIGHT * 0.5 + RIGHT * horiz_kernel_grid.get_width() / 2
        
        self.play(
            horiz_kernel_grid.animate.move_to(horiz_kernel_target),
            run_time=0.5
        )
        
        # Update kernel_label position
        horiz_kernel_label.next_to(horiz_kernel_grid, UP, buff=0.3)
        
        self.play(
            FadeIn(equals_sign2), FadeIn(horiz_kernel_label),
            run_time=0.4
        )
        
        self.wait(1)

        self.camera.frame.save_state()
        
        # ==========================================
        # PART 7: Show real grayscale images for horizontal
        # ==========================================
        
        self.play(self.camera.frame.animate.shift(DOWN * 1.5).scale(1.15), run_time=0.8)
        
        real_label2 = Text("Actual Grayscale Images:", font_size=28, weight=BOLD)
        real_label2.set_color(BLUE)
        real_label2.move_to(DOWN * 2.8 + LEFT * 0.5)
        
        small_cell = 0.35
        
        # Input image - use actual pixel values (60 and 220 mapped to 0-255)
        horiz_real_input = VGroup()
        for i in range(6):
            for j in range(6):
                cell = Square(side_length=small_cell)
                brightness = horiz_input_values[i, j] / 255.0  # Use actual pixel value
                cell.set_fill(interpolate_color(BLACK, WHITE, brightness), opacity=1)
                cell.set_stroke(BLACK, width=0.5)
                cell.move_to(RIGHT * j * small_cell + DOWN * i * small_cell)
                horiz_real_input.add(cell)
        horiz_real_input.center()
        horiz_real_input.next_to(input_grid, DOWN, buff=0.77)
        
        
        # Filter - ORANGE stroke for horizontal filter
        horiz_real_filter = VGroup()
        for i in range(3):
            for j in range(3):
                cell = Square(side_length=small_cell)
                val = horizontal_kernel[i, j]
                if val == -1:
                    cell.set_fill(BLACK, opacity=1)
                elif val == 0:
                    cell.set_fill(GREY, opacity=1)
                else:
                    cell.set_fill(WHITE, opacity=1)
                cell.set_stroke(ORANGE, width=2)
                cell.move_to(RIGHT * j * small_cell + DOWN * i * small_cell)
                horiz_real_filter.add(cell)
        horiz_real_filter.center()
        horiz_real_filter.next_to(horiz_kernel_grid, DOWN, buff=1).shift(DOWN).scale(1.4)
        
        # Output - use GREY and WHITE (not black)
        horiz_real_output = VGroup()
        horiz_out_min = np.min(horiz_output_values)
        horiz_out_max = np.max(horiz_output_values)
        horiz_out_range = horiz_out_max - horiz_out_min if horiz_out_max != horiz_out_min else 1
        
        for i in range(4):
            for j in range(4):
                cell = Square(side_length=small_cell)
                val = horiz_output_values[i, j]
                # Map GREY to WHITE
                normalized = (val - horiz_out_min) / horiz_out_range
                cell.set_fill(interpolate_color(GREY, WHITE, normalized), opacity=1)
                cell.set_stroke(BLACK, width=0.5)
                cell.move_to(RIGHT * j * small_cell + DOWN * i * small_cell)
                horiz_real_output.add(cell)
        horiz_real_output.center()
        horiz_real_output.next_to(horiz_output_grid, DOWN, buff=1).shift(DOWN*0.4).scale(1.23)
        
        horiz_real_output_label = Text("Edge Detected", font_size=26, weight=BOLD)
        horiz_real_output_label.set_color(GREEN)
        horiz_real_output_label.next_to(horiz_real_output, UP, buff=0.2)
        

        self.play(
            FadeIn(horiz_real_input), 
            run_time=0.6
        )
        horiz_real_filter.shift(DOWN*0.1).scale(1.1)
        self.play(
            FadeIn(horiz_real_filter), 
            run_time=0.6
        )
        horiz_real_output.shift(DOWN*0.1).scale(1.12).shift(DOWN*0.14)
        self.play(
            FadeIn(horiz_real_output), Write(horiz_real_output_label),
            run_time=0.6
        )
        

        self.wait(3)


class ImageFilters(Scene):
    
    def construct(self):

        self.camera.frame.shift(LEFT*1.1 + UP*1.1)

        # ==========================================
        # Helper: Manual 2D convolution 
        # ==========================================
        
        def convolve2d(image, kernel):
            """Apply 2D convolution with edge padding"""
            kh, kw = kernel.shape
            pad_h, pad_w = kh // 2, kw // 2
            
            # Pad image
            padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='reflect')
            
            h, w = image.shape
            result = np.zeros_like(image, dtype=np.float64)
            
            for i in range(h):
                for j in range(w):
                    region = padded[i:i+kh, j:j+kw]
                    result[i, j] = np.sum(region * kernel)
            
            return result
        
        def apply_filter_rgb(rgb_image, kernel):
            """Apply convolution filter to RGB image"""
            result = np.zeros_like(rgb_image, dtype=np.float64)
            for c in range(3):
                result[:, :, c] = convolve2d(rgb_image[:, :, c].astype(np.float64), kernel)
            return np.clip(result, 0, 255).astype(np.uint8)
        
        # ==========================================
        # Image Generation (Sunset Pixel Art)
        # ==========================================
        
        img_size = 36
        image_rgb = np.zeros((img_size, img_size, 3), dtype=np.uint8)
        
        # Colors
        SKY_TOP = np.array([25, 25, 112])       
        SKY_MID = np.array([255, 100, 50])      
        SKY_LOW = np.array([255, 180, 100])     
        SUN_COLOR = np.array([255, 255, 50])    
        SUN_GLOW = np.array([255, 200, 80])     
        MOUNTAIN1 = np.array([50, 50, 70])      
        MOUNTAIN2 = np.array([70, 60, 90])      
        GRASS = np.array([34, 139, 34])         
        WATER = np.array([30, 144, 255])        
        WATER_LIGHT = np.array([100, 180, 255]) 
        
        # Draw Scenery
        for i in range(img_size):
            for j in range(img_size):
                if i < 8:
                    t = i / 8
                    image_rgb[i, j] = (SKY_TOP * (1-t) + SKY_MID * t).astype(np.uint8)
                elif i < 15:
                    t = (i - 8) / 7
                    image_rgb[i, j] = (SKY_MID * (1-t) + SKY_LOW * t).astype(np.uint8)
                else:
                    image_rgb[i, j] = SKY_LOW
        
        sun_center = (10, 18)
        sun_radius = 4
        for i in range(img_size):
            for j in range(img_size):
                dist = np.sqrt((i - sun_center[0])**2 + (j - sun_center[1])**2)
                if dist < sun_radius:
                    image_rgb[i, j] = SUN_COLOR
                elif dist < sun_radius + 2:
                    t = (dist - sun_radius) / 2
                    image_rgb[i, j] = (SUN_GLOW * (1-t) + image_rgb[i, j] * t).astype(np.uint8)
        
        for j in range(img_size):
            peak1 = 12 - int(7 * np.exp(-((j - 8)**2) / 40))
            for i in range(peak1, 24):
                if i < img_size:
                    image_rgb[i, j] = MOUNTAIN1
            peak2 = 14 - int(5 * np.exp(-((j - 28)**2) / 35))
            for i in range(peak2, 24):
                if i < img_size and not np.array_equal(image_rgb[i, j], MOUNTAIN1):
                    image_rgb[i, j] = MOUNTAIN2
        
        for i in range(24, 30):
            for j in range(img_size):
                wave_offset = 0.5 * np.sin(j * 0.6 + i * 0.4)
                if (j + int(wave_offset * 2)) % 4 < 2:
                    image_rgb[i, j] = WATER
                else:
                    image_rgb[i, j] = WATER_LIGHT
        
        for i in range(30, img_size):
            for j in range(img_size):
                if (i + j) % 3 == 0:
                    image_rgb[i, j] = (GRASS * 0.8).astype(np.uint8)
                else:
                    image_rgb[i, j] = GRASS
        
        np.random.seed(42)
        for _ in range(12):
            si, sj = np.random.randint(0, 6), np.random.randint(0, img_size)
            image_rgb[si, sj] = [255, 255, 255]
        
        # ==========================================
        # Kernels
        # ==========================================
        mean_kernel = np.ones((3, 3)) / 9
        gaussian_kernel = np.array([[1, 2, 1],[2, 4, 2],[1, 2, 1]], dtype=np.float64) / 16
        sharpen_kernel = np.array([[0, -1, 0],[-1, 5, -1],[0, -1, 0]], dtype=np.float64)
        emboss_kernel = np.array([[-2, -1, 0],[-1, 1, 1],[0, 1, 2]], dtype=np.float64)
        edge_kernel = np.array([[0, 1, 0],[1, -4, 1],[0, 1, 0]], dtype=np.float64)
        
        # ==========================================
        # Visualization Helpers
        # ==========================================
        
        def create_pixel_image(rgb_array, cell_size=0.08, position=ORIGIN):
            h, w = rgb_array.shape[:2]
            pixel_grid = VGroup()
            for i in range(h):
                for j in range(w):
                    cell = Square(side_length=cell_size)
                    r, g, b = rgb_array[i, j]
                    color = rgb_to_color([r/255, g/255, b/255])
                    cell.set_fill(color, opacity=1)
                    cell.set_stroke(width=0)
                    cell.move_to(position + RIGHT * (j - w/2) * cell_size + DOWN * (i - h/2) * cell_size)
                    pixel_grid.add(cell)
            return pixel_grid
        
        def create_kernel_grid(kernel, color, k_cell_size=0.85, use_fractions=False):
            kernel_grid = VGroup()
            for i in range(3):
                for j in range(3):
                    cell = Square(side_length=k_cell_size)
                    cell.set_fill(color, opacity=0.7)
                    cell.set_stroke(WHITE, width=2)
                    cell.move_to(RIGHT * (j - 1) * k_cell_size + DOWN * (i - 1) * k_cell_size)
                    
                    val = kernel[i, j]
                    if use_fractions:
                        val_str = "1/9"
                    elif abs(val - round(val)) < 0.001:
                        val_str = str(int(round(val)))
                    else:
                        val_str = f"{val:.2f}"
                    
                    val_text = Text(val_str, font_size=20, weight=BOLD).set_color(WHITE)
                    val_text.move_to(cell.get_center())
                    kernel_grid.add(VGroup(cell, val_text))
            return kernel_grid
        
        # ==========================================
        # SCENE SETUP
        # ==========================================
        
        cell_size = 0.085
        
        title = Text("Image Filters", font_size=44, weight=BOLD).set_color(WHITE)
        title.to_edge(UP, buff=0.35)
        
        # 1. POSITION ORIGINAL IMAGE (FAR LEFT)
        original_pos_center = LEFT * 5.5
        original_image = create_pixel_image(image_rgb, cell_size, original_pos_center)
        
        original_label = Text("Original", font_size=40, weight=BOLD).set_color(WHITE)
        original_label.next_to(original_image, UP, buff=0.45)
        
        self.play(
            LaggedStartMap(FadeIn, original_image, lag_ratio=0.0003),
            Write(original_label),
            run_time=1.5
        )
        self.wait(0.5)

        filters_info = [
            {"name": "Mean Blur", "kernel": mean_kernel, "color": BLUE, "use_fractions": True},
            {"name": "Gaussian Blur", "kernel": gaussian_kernel, "color": TEAL, "use_fractions": False},
            {"name": "Sharpen", "kernel": sharpen_kernel, "color": ORANGE, "use_fractions": False},
            {"name": "Emboss", "kernel": emboss_kernel, "color": PURPLE, "use_fractions": False},
            {"name": "Edge Detection", "kernel": edge_kernel, "color": GREEN, "use_fractions": False},
        ]
        
        # ==========================================
        # FIRST FILTER
        # ==========================================
        
        first_filter = filters_info[0]
        
        # 2. CREATE & SCALE KERNEL ELEMENTS (Middle Section)
        
        # Create elements first
        kernel_grid = create_kernel_grid(first_filter["kernel"], first_filter["color"], use_fractions=first_filter["use_fractions"])
        
        filter_name = Text(first_filter["name"], font_size=56, weight=BOLD) # Slightly larger font base
        filter_name.set_color(first_filter["color"]).shift(UP*1.6)
        
        kernel_label = Text("Kernel", font_size=45, weight=BOLD).shift(UP*0.52) # Slightly larger font base
        kernel_label.set_color(first_filter["color"]).next_to(kernel_grid, UP, buff=0.55)
        
        # Group them to scale together or scale individually
        # You wanted the whole middle filter section scaled by 1.3
        
        
        # Layout Middle Section
        # Position Grid relative to Original
        kernel_grid.next_to(original_image, RIGHT, buff=1.8) 
        
        # Position labels relative to Grid
        kernel_label.next_to(kernel_grid, UP, buff=0.55)
        filter_name.next_to(kernel_label, UP, buff=1.3)
        
        # 3. POSITION OUTPUT (RIGHT OF KERNEL)
        filtered_rgb = apply_filter_rgb(image_rgb, first_filter["kernel"])
        output_image = create_pixel_image(filtered_rgb, cell_size, ORIGIN)
        output_image.next_to(kernel_grid, RIGHT, buff=1.8)
        
        output_pos_center = output_image.get_center()
        
        output_label = Text("Result", font_size=44, weight=BOLD)
        output_label.set_color(first_filter["color"])
        output_label.next_to(output_image, UP, buff=0.45)
        
        self.play(Write(filter_name), run_time=0.5)
        self.play(
            LaggedStartMap(FadeIn, kernel_grid, lag_ratio=0.03),
            Write(kernel_label),
            run_time=0.6
        )



        # Scanning animation
        scan_rect = Rectangle(width=3 * cell_size, height=3 * cell_size)
        scan_rect.set_fill(first_filter["color"], opacity=0.4)
        scan_rect.set_stroke(first_filter["color"], width=3)
        scan_rect.move_to(original_pos_center + UP * (img_size/2 - 1.5) * cell_size + LEFT * (img_size/2 - 1.5) * cell_size)
        scan_rect.set_z_index(15)
        
        self.play(FadeIn(scan_rect), run_time=0.2)
        
        scan_positions = []
        rows_to_scan = 5
        for row in range(rows_to_scan):
            actual_row = row * (img_size - 3) // (rows_to_scan - 1)
            y_pos = original_pos_center[1] + (img_size/2 - 1.5 - actual_row) * cell_size
            if row % 2 == 0:
                for col in [0, img_size - 3]:
                    x_pos = original_pos_center[0] + (-img_size/2 + 1.5 + col) * cell_size
                    scan_positions.append(np.array([x_pos, y_pos, 0]))
            else:
                for col in [img_size - 3, 0]:
                    x_pos = original_pos_center[0] + (-img_size/2 + 1.5 + col) * cell_size
                    scan_positions.append(np.array([x_pos, y_pos, 0]))
        
        for pos in scan_positions:
            self.play(scan_rect.animate.move_to(pos), run_time=0.338, rate_func=linear)
        
        self.play(FadeOut(scan_rect), run_time=0.15)
        
        self.play(
            LaggedStartMap(FadeIn, output_image, lag_ratio=0.0003),
            Write(output_label),
            run_time=0.8
        )
        self.wait(1)
        
        # ==========================================
        # LOOP REMAINING FILTERS
        # ==========================================
        
        for idx in range(1, len(filters_info)):
            filt = filters_info[idx]
            
            # Create new elements with same base sizes
            new_filter_name = Text(filt["name"], font_size=56, weight=BOLD).set_color(filt["color"])
            new_filter_name.move_to(filter_name)
            
            new_kernel_grid = create_kernel_grid(filt["kernel"], filt["color"], use_fractions=filt["use_fractions"])
            new_kernel_grid.move_to(kernel_grid)
            
            new_kernel_label = Text("Kernel", font_size=45, weight=BOLD).set_color(filt["color"]).shift(UP*0.52)
            new_kernel_label.next_to(new_kernel_grid, UP, buff=0.2).move_to(kernel_label)
            
            new_filtered_rgb = apply_filter_rgb(image_rgb, filt["kernel"])
            new_output_image = create_pixel_image(new_filtered_rgb, cell_size, output_pos_center)
            
            new_output_label = Text("Result", font_size=44, weight=BOLD).set_color(filt["color"]).move_to(output_label)
            
            self.play(
                Transform(filter_name, new_filter_name),
                Transform(kernel_grid, new_kernel_grid),
                Transform(kernel_label, new_kernel_label),
                run_time=0.5
            )
            
            # Scan
            scan_rect = Rectangle(width=3 * cell_size, height=3 * cell_size)
            scan_rect.set_fill(filt["color"], opacity=0.4)
            scan_rect.set_stroke(filt["color"], width=3)
            scan_rect.move_to(original_pos_center + UP * (img_size/2 - 1.5) * cell_size + LEFT * (img_size/2 - 1.5) * cell_size)
            scan_rect.set_z_index(5)
            
            self.play(FadeIn(scan_rect), run_time=0.15)
            for pos in scan_positions:
                self.play(scan_rect.animate.move_to(pos), run_time=0.115, rate_func=linear)
            self.play(FadeOut(scan_rect), run_time=0.1)

            new_output_image.move_to(output_image)
            
            self.play(
                Transform(output_image, new_output_image),
                Transform(output_label, new_output_label),
                run_time=0.6
            )
            self.wait(1)
        
        self.wait(1)
        
        # ==========================================
        # FINAL COMPARISON
        # ==========================================
        
        comparison_title = Text("All Filters Comparison", font_size=38, weight=BOLD).set_color(WHITE).to_edge(UP, buff=0.35)
        
        self.play(
            FadeOut(original_image), FadeOut(original_label),
            FadeOut(kernel_grid), FadeOut(kernel_label), FadeOut(filter_name),
            FadeOut(output_image), FadeOut(output_label),
            run_time=0.7
        )
        
        small_cell = 0.055
        positions = [
            LEFT * 4.5 + UP * 0.6,
            LEFT * 0.0 + UP * 0.6,
            RIGHT * 4.5 + UP * 0.6,
            LEFT * 4.5 + DOWN * 2.4,
            LEFT * 0.0 + DOWN * 2.4,
            RIGHT * 4.5 + DOWN * 2.4,
        ]
        
        all_images_data = [("Original", image_rgb, WHITE)]
        for filt in filters_info:
            filtered = apply_filter_rgb(image_rgb, filt["kernel"])
            all_images_data.append((filt["name"], filtered, filt["color"]))
        
        comparison_group = VGroup()
        for i, (name, img_data, color) in enumerate(all_images_data):
            if i >= len(positions): break
            pos = positions[i]
            img = create_pixel_image(img_data, small_cell, pos)
            
            label = Text(name, font_size=30, weight=BOLD).set_color(color).next_to(img, UP, buff=0.3)
            group = VGroup(img, label)
            comparison_group.add(group)

        
        self.play(LaggedStartMap(FadeIn, comparison_group, lag_ratio=0.1), self.camera.frame.animate.shift(DOWN*1.5 + RIGHT*1.1) , run_time=1.5)
        self.wait(2)
