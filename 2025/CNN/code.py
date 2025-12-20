from manimlib import *
import numpy as np
from PIL import Image, ImageFilter, ImageOps
import os


class ReceptiveField(Scene):
    """
    Clean Receptive Field Visualization
    - Default dark background
    - Simple colors
    - Educational flow
    - Feature hierarchy explanation at end
    """
    
    def construct(self):

        self.camera.frame.scale(1.2).shift(DOWN*0.5).scale(0.87)
        
        # Simple colors
        GOLD = "#FFD700"
        CORAL = "#FF6B6B"
        MINT = "#90EE90"
        LAVENDER = "#DDA0DD"
        BLUE = "#6699CC"
        
        # ==========================================
        # INTRO: WHAT IS A RECEPTIVE FIELD?
        # ==========================================
        
        title = Text("Receptive Field", font_size=60, weight=BOLD)
        title.set_color(WHITE)
        title.move_to(UP * 2.2)
        
        self.play(Write(title), run_time=1)
        self.wait(0.5)
        
        # Simple visual explanation
        demo_cell = 0.45
        demo_input = VGroup()
        for i in range(5):
            for j in range(5):
                cell = Square(side_length=demo_cell)
                cell.set_fill(BLUE, opacity=0.2)
                cell.set_stroke(BLUE, width=1.5)
                cell.move_to(RIGHT * (j - 2) * demo_cell + DOWN * (i - 2) * demo_cell)
                demo_input.add(cell)
        demo_input.move_to(LEFT * 2.5 + DOWN * 0.3)
        
        # Highlight 3x3 region
        demo_rf = VGroup()
        for i in range(3):
            for j in range(3):
                cell = Square(side_length=demo_cell)
                cell.set_fill(CORAL, opacity=0.7)
                cell.set_stroke(WHITE, width=2)
                cell.move_to(RIGHT * (j - 1) * demo_cell + DOWN * (i - 1) * demo_cell)
                demo_rf.add(cell)
        demo_rf.move_to(demo_input.get_center())
        
        # Single output pixel
        demo_output = Square(side_length=demo_cell * 1.2)
        demo_output.set_fill(GOLD, opacity=0.9)
        demo_output.set_stroke(WHITE, width=2)
        demo_output.move_to(RIGHT * 2.5 + DOWN * 0.3)
        
        # Arrow
        demo_arrow = Arrow(demo_rf.get_right() + RIGHT * 0.3, demo_output.get_left() + LEFT * 0.3,
                          buff=0.1, stroke_width=3)
        demo_arrow.set_color(WHITE)
        
        # Labels
        input_txt = Text("Input Region", font_size=30, weight=BOLD)
        input_txt.set_color(CORAL)
        input_txt.next_to(demo_input, DOWN, buff=0.5)
        
        output_txt = Text("Output Pixel", font_size=30, weight=BOLD)
        output_txt.set_color(GOLD)
        output_txt.next_to(demo_output, DOWN, buff=0.5)
        
        # Definition
        definition = Text(
            "The receptive field is the input region \n     that affects one output pixel",
            font_size=28,
            weight=BOLD
        )
        definition.to_edge(DOWN, buff=0.6).shift(DOWN*0.3)
        
        self.play(FadeIn(demo_input), run_time=0.5)
        self.play(LaggedStartMap(FadeIn, demo_rf, lag_ratio=0.05), run_time=0.4)
        self.play(
            GrowArrow(demo_arrow),
            FadeIn(demo_output, scale=1.2),
            run_time=0.5
        )
        self.play(
            FadeIn(input_txt), FadeIn(output_txt),
            FadeIn(definition, shift=UP * 0.2),
            run_time=0.5
        )
        
        self.wait(2)

        
        # Clear intro
        self.play(
            FadeOut(VGroup(title, demo_input, demo_rf, demo_output, demo_arrow,
                          input_txt, output_txt, definition)),
            run_time=0.5
        )
        
        # ==========================================
        # PART 1: SINGLE 3x3 CONVOLUTION
        # ==========================================
        
        section1 = Text("Single 3x3 Convolution", font_size=38, weight=BOLD)
        section1.set_color(WHITE)
        section1.to_edge(UP, buff=0.45).shift(DOWN*0.69)
        
        self.play(FadeIn(section1), run_time=0.4)
        
        # Input 7x7
        cell_size = 0.48
        input_size = 7
        
        input_grid = VGroup()
        input_cells = {}
        for i in range(input_size):
            for j in range(input_size):
                cell = Square(side_length=cell_size)
                cell.set_fill(BLUE, opacity=0.15)
                cell.set_stroke(BLUE, width=1)
                cell.move_to(
                    RIGHT * (j - input_size/2 + 0.5) * cell_size +
                    DOWN * (i - input_size/2 + 0.5) * cell_size
                )
                input_cells[(i, j)] = cell
                input_grid.add(cell)
        input_grid.move_to(LEFT * 3.5 + DOWN * 1.3)
        
        input_label = Text("Input", font_size=38, weight=BOLD)
        input_label.set_color(BLUE)
        input_label.next_to(input_grid, UP, buff=0.65)
        
        input_dim = Text("7 × 7", font_size=34)
        input_dim.set_color(GREY_B)
        input_dim.next_to(input_label, DOWN, buff=0.12)
        
        input_rf = Text("RF = 1", font_size=34, weight=BOLD)
        input_rf.set_color(GREY_A)
        input_rf.next_to(input_grid, DOWN, buff=0.4)
        
        # Output 5x5
        output_size = 5
        output_grid = VGroup()
        output_cells = {}
        for i in range(output_size):
            for j in range(output_size):
                cell = Square(side_length=cell_size)
                cell.set_fill(MINT, opacity=0.15)
                cell.set_stroke(MINT, width=1)
                cell.move_to(
                    RIGHT * (j - output_size/2 + 0.5) * cell_size +
                    DOWN * (i - output_size/2 + 0.5) * cell_size
                )
                output_cells[(i, j)] = cell
                output_grid.add(cell)
        output_grid.move_to(RIGHT * 3.5 + DOWN * 1.3)
        
        output_label = Text("Output", font_size=38, weight=BOLD)
        output_label.set_color(MINT)
        output_label.next_to(output_grid, UP, buff=0.65)
        
        output_dim = Text("5 × 5", font_size=34)
        output_dim.set_color(GREY_B)
        output_dim.next_to(output_label, DOWN, buff=0.12)
        
        output_rf = Text("RF = 3", font_size=34, weight=BOLD)
        output_rf.set_color(GOLD)
        output_rf.next_to(output_grid, DOWN, buff=0.4)
        
        # Arrow and kernel
        arrow = Arrow(input_grid.get_right() + RIGHT * 0.35,
                     output_grid.get_left() + LEFT * 0.35,
                     buff=0.1, stroke_width=3)
        arrow.set_color(WHITE)
        
        kernel_label = Text("3x3", font_size=34, weight=BOLD)
        kernel_label.set_color(GOLD)
        kernel_label.next_to(arrow, UP, buff=0.18)
        
        # Animate
        self.play(
            LaggedStartMap(FadeIn, input_grid, lag_ratio=0.008),
            FadeIn(input_label), FadeIn(input_dim), FadeIn(input_rf),
            run_time=0.6
        )
        self.play(GrowArrow(arrow), FadeIn(kernel_label), run_time=0.4)
        self.play(
            LaggedStartMap(FadeIn, output_grid, lag_ratio=0.008),
            FadeIn(output_label), FadeIn(output_dim), FadeIn(output_rf),
            run_time=0.6
        )
        
        self.wait(0.6)

        
        # ==========================================
        # SHOW RF CONNECTION WITH LINES
        # ==========================================
        
        out_pos = (2, 2)
        in_i, in_j = out_pos
        
        # Output highlight
        out_highlight = Square(side_length=cell_size)
        out_highlight.set_fill(GOLD, opacity=0.9)
        out_highlight.set_stroke(WHITE, width=2)
        out_highlight.move_to(output_cells[out_pos].get_center())
        
        # Input RF highlight
        rf_cells = VGroup()
        for di in range(3):
            for dj in range(3):
                cell = Square(side_length=cell_size)
                cell.set_fill(CORAL, opacity=0.8)
                cell.set_stroke(WHITE, width=1.5)
                cell.move_to(input_cells[(in_i + di, in_j + dj)].get_center())
                rf_cells.add(cell)
        
        rf_border = Square(side_length=cell_size * 3 + 0.04)
        rf_border.set_stroke(CORAL, width=2.5)
        rf_border.set_fill(opacity=0)
        rf_border.move_to(input_cells[(in_i + 1, in_j + 1)].get_center())
        
        # Connection lines
        lines = VGroup()
        for di in range(3):
            for dj in range(3):
                start = input_cells[(in_i + di, in_j + dj)].get_center()
                end = output_cells[out_pos].get_center()
                line = Line(start, end, stroke_width=1.2)
                line.set_stroke(CORAL, opacity=0.35)
                lines.add(line)
        
        # Animate together
        self.play(
            FadeIn(out_highlight, scale=1.2),
            LaggedStartMap(FadeIn, rf_cells, lag_ratio=0.03),
            ShowCreation(rf_border),
            LaggedStartMap(ShowCreation, lines, lag_ratio=0.02),
            run_time=0.8
        )
        
        self.wait(0.5)
        
        # Move across positions
        positions = [(1, 1), (1, 3), (3, 1), (3, 3), (2, 2)]
        
        for new_pos in positions:
            new_in_i, new_in_j = new_pos
            new_out_center = output_cells[new_pos].get_center()
            new_rf_center = input_cells[(new_in_i + 1, new_in_j + 1)].get_center()
            
            new_rf_cells = VGroup()
            for di in range(3):
                for dj in range(3):
                    cell = Square(side_length=cell_size)
                    cell.set_fill(CORAL, opacity=0.8)
                    cell.set_stroke(WHITE, width=1.5)
                    cell.move_to(input_cells[(new_in_i + di, new_in_j + dj)].get_center())
                    new_rf_cells.add(cell)
            
            new_lines = VGroup()
            for di in range(3):
                for dj in range(3):
                    start = input_cells[(new_in_i + di, new_in_j + dj)].get_center()
                    line = Line(start, new_out_center, stroke_width=1.2)
                    line.set_stroke(CORAL, opacity=0.35)
                    new_lines.add(line)
            
            self.play(
                out_highlight.animate.move_to(new_out_center),
                rf_border.animate.move_to(new_rf_center),
                Transform(rf_cells, new_rf_cells),
                Transform(lines, new_lines),
                run_time=0.35
            )
            self.wait(0.12)
        
        self.wait(0.8)
        
        # ==========================================
        # PART 2: TWO CONVOLUTIONS - NO LINES
        # ==========================================
        
        part1 = VGroup(
            input_grid, input_label, input_dim, input_rf,
            output_grid, output_label, output_dim, output_rf,
            arrow, kernel_label,
            out_highlight, rf_cells, rf_border, lines,
            section1
        )
        self.play(FadeOut(part1), run_time=0.5)
        
        section2 = Text("Two Stacked 3x3 Convolutions", font_size=38, weight=BOLD)
        section2.set_color(WHITE)
        section2.to_edge(UP, buff=0.45).move_to(section1)
        
        self.play(FadeIn(section2), run_time=0.4)


        # Three layers
        lcell = 0.34
        
        # Layer 1: 9x9
        l1_size = 9
        l1_grid = VGroup()
        l1_cells = {}
        for i in range(l1_size):
            for j in range(l1_size):
                cell = Square(side_length=lcell)
                cell.set_fill(BLUE, opacity=0.12)
                cell.set_stroke(BLUE, width=0.8)
                cell.move_to(
                    RIGHT * (j - l1_size/2 + 0.5) * lcell +
                    DOWN * (i - l1_size/2 + 0.5) * lcell
                )
                l1_cells[(i, j)] = cell
                l1_grid.add(cell)
        l1_grid.move_to(LEFT * 4.6 + DOWN * 1.42)
        
        l1_label = Text("Input", font_size=36, weight=BOLD)
        l1_label.set_color(BLUE)
        l1_label.next_to(l1_grid, UP, buff=0.75)
        
        l1_dim = Text("9x9", font_size=35)
        l1_dim.set_color(GREY_B)
        l1_dim.next_to(l1_label, DOWN, buff=0.15)
        
        l1_rf = Text("RF = 1", font_size=35, weight=BOLD)
        l1_rf.set_color(GREY_A)
        l1_rf.next_to(l1_grid, DOWN, buff=0.35)
        
        # Layer 2: 7x7
        l2_size = 7
        l2_grid = VGroup()
        l2_cells = {}
        for i in range(l2_size):
            for j in range(l2_size):
                cell = Square(side_length=lcell)
                cell.set_fill(MINT, opacity=0.12)
                cell.set_stroke(MINT, width=0.8)
                cell.move_to(
                    RIGHT * (j - l2_size/2 + 0.5) * lcell +
                    DOWN * (i - l2_size/2 + 0.5) * lcell
                )
                l2_cells[(i, j)] = cell
                l2_grid.add(cell)
        l2_grid.move_to(RIGHT*0.5 + DOWN * 1.42)
        
        l2_label = Text("Hidden", font_size=36, weight=BOLD)
        l2_label.set_color(MINT)
        l2_label.next_to(l2_grid, UP, buff=0.75)
        
        l2_dim = Text("7x7", font_size=35)
        l2_dim.set_color(GREY_B)
        l2_dim.next_to(l2_label, DOWN, buff=0.15)
        
        l2_rf = Text("RF = 3", font_size=35, weight=BOLD)
        l2_rf.set_color(GREY_A)
        l2_rf.next_to(l2_grid, DOWN, buff=0.42)
        
        # Layer 3: 5x5
        l3_size = 5
        l3_grid = VGroup()
        l3_cells = {}
        for i in range(l3_size):
            for j in range(l3_size):
                cell = Square(side_length=lcell)
                cell.set_fill(LAVENDER, opacity=0.12)
                cell.set_stroke(LAVENDER, width=0.8)
                cell.move_to(
                    RIGHT * (j - l3_size/2 + 0.5) * lcell +
                    DOWN * (i - l3_size/2 + 0.5) * lcell
                )
                l3_cells[(i, j)] = cell
                l3_grid.add(cell)
        l3_grid.move_to(RIGHT * 5.5 + DOWN * 1.42)
            
        l3_label = Text("Output", font_size=36, weight=BOLD)
        l3_label.set_color(LAVENDER)
        l3_label.next_to(l3_grid, UP, buff=0.75)
        
        l3_dim = Text("5x5", font_size=35)
        l3_dim.set_color(GREY_B)
        l3_dim.next_to(l3_label, DOWN, buff=0.15)
        
        l3_rf = Text("RF = 5", font_size=35, weight=BOLD)
        l3_rf.next_to(l3_grid, DOWN, buff=0.42)
        
        # Arrows
        arr1 = Arrow(l1_grid.get_right() + RIGHT * 0.15, l2_grid.get_left() + LEFT * 0.15,
                    buff=0.05, stroke_width=2)
        arr1.set_color(WHITE)
        
        arr2 = Arrow(l2_grid.get_right() + RIGHT * 0.15, l3_grid.get_left() + LEFT * 0.15,
                    buff=0.05, stroke_width=2)
        arr2.set_color(WHITE)
        
        k1 = Text("3x3", font_size=25, weight=BOLD)
        k1.set_color(GOLD)
        k1.next_to(arr1, UP, buff=0.12)
        
        k2 = Text("3x3", font_size=25, weight=BOLD)
        k2.set_color(GOLD)
        k2.next_to(arr2, UP, buff=0.12)
        
        # Animate layers
        self.play(
            LaggedStartMap(FadeIn, l1_grid, lag_ratio=0.003),
            FadeIn(l1_label), FadeIn(l1_dim), FadeIn(l1_rf),
            run_time=0.5
        )
        self.play(
            GrowArrow(arr1), FadeIn(k1),
            LaggedStartMap(FadeIn, l2_grid, lag_ratio=0.003),
            FadeIn(l2_label), FadeIn(l2_dim), FadeIn(l2_rf),
            run_time=0.5
        )
        self.play(
            GrowArrow(arr2), FadeIn(k2),
            LaggedStartMap(FadeIn, l3_grid, lag_ratio=0.003),
            FadeIn(l3_label), FadeIn(l3_dim), FadeIn(l3_rf),
            run_time=0.5
        )
        
        self.wait(0.6)



        # ==========================================
        # HIGHLIGHT RFs - NO LINES
        # ==========================================
        
        # Output pixel
        l3_highlight = Square(side_length=lcell)
        l3_highlight.set_fill(GOLD, opacity=0.9)
        l3_highlight.set_stroke(WHITE, width=2)
        l3_highlight.move_to(l3_cells[(2, 2)].get_center())
        
        # L2 RF: 3x3
        l2_rf_cells = VGroup()
        for di in range(3):
            for dj in range(3):
                cell = Square(side_length=lcell)
                cell.set_fill(CORAL, opacity=0.7)
                cell.set_stroke(WHITE, width=1.2)
                cell.move_to(l2_cells[(2 + di, 2 + dj)].get_center())
                l2_rf_cells.add(cell)
        
        l2_rf_border = Square(side_length=lcell * 3 + 0.03)
        l2_rf_border.set_stroke(CORAL, width=2)
        l2_rf_border.set_fill(opacity=0)
        l2_rf_border.move_to(l2_cells[(3, 3)].get_center())
        
        # L1 RF: 5x5
        l1_rf_cells = VGroup()
        for di in range(5):
            for dj in range(5):
                cell = Square(side_length=lcell)
                cell.set_fill(CORAL, opacity=0.5)
                cell.set_stroke(WHITE, width=0.8)
                cell.move_to(l1_cells[(2 + di, 2 + dj)].get_center())
                l1_rf_cells.add(cell)
        
        l1_rf_border = Square(side_length=lcell * 5 + 0.03)
        l1_rf_border.set_stroke(CORAL, width=2)
        l1_rf_border.set_fill(opacity=0)
        l1_rf_border.move_to(l1_cells[(4, 4)].get_center())
        
        # Animate - NO LINES
        self.play(FadeIn(l3_highlight, scale=1.2), run_time=0.4)
        
        self.play(
            LaggedStartMap(FadeIn, l2_rf_cells, lag_ratio=0.02),
            ShowCreation(l2_rf_border),
            run_time=0.5
        )
        
        self.play(
            LaggedStartMap(FadeIn, l1_rf_cells, lag_ratio=0.008),
            ShowCreation(l1_rf_border),
            run_time=0.5
        )
        
        self.wait(0.8)
        
        # ==========================================
        # MOVE OUTPUT PIXEL - SHOW RF MOVEMENT
        # ==========================================
        
        # Define positions to move through (row, col) in output layer
        # Each position shows how the RF cascades back through layers
        output_positions = [(0, 0), (0, 4), (4, 0), (4, 4), (2, 2)]
        
        for out_row, out_col in output_positions:
            # Calculate new centers
            new_l3_center = l3_cells[(out_row, out_col)].get_center()
            
            # L2 RF center: output position maps to center of 3x3 in L2
            # The output (out_row, out_col) corresponds to L2 cells starting at (out_row, out_col)
            l2_rf_start_row = out_row
            l2_rf_start_col = out_col
            new_l2_rf_center = l2_cells[(l2_rf_start_row + 1, l2_rf_start_col + 1)].get_center()
            
            # L1 RF center: each L2 cell has 3x3 RF, so 3x3 L2 region covers 5x5 L1 region
            # The 5x5 starts at (out_row, out_col) in L1
            l1_rf_start_row = out_row
            l1_rf_start_col = out_col
            new_l1_rf_center = l1_cells[(l1_rf_start_row + 2, l1_rf_start_col + 2)].get_center()
            
            # Create new RF cell groups for L2
            new_l2_rf_cells = VGroup()
            for di in range(3):
                for dj in range(3):
                    cell = Square(side_length=lcell)
                    cell.set_fill(CORAL, opacity=0.7)
                    cell.set_stroke(WHITE, width=1.2)
                    cell.move_to(l2_cells[(l2_rf_start_row + di, l2_rf_start_col + dj)].get_center())
                    new_l2_rf_cells.add(cell)
            
            # Create new RF cell groups for L1
            new_l1_rf_cells = VGroup()
            for di in range(5):
                for dj in range(5):
                    cell = Square(side_length=lcell)
                    cell.set_fill(CORAL, opacity=0.5)
                    cell.set_stroke(WHITE, width=0.8)
                    cell.move_to(l1_cells[(l1_rf_start_row + di, l1_rf_start_col + dj)].get_center())
                    new_l1_rf_cells.add(cell)
            
            # Animate all movements together
            self.play(
                l3_highlight.animate.move_to(new_l3_center),
                l2_rf_border.animate.move_to(new_l2_rf_center),
                Transform(l2_rf_cells, new_l2_rf_cells),
                l1_rf_border.animate.move_to(new_l1_rf_center),
                Transform(l1_rf_cells, new_l1_rf_cells),
                run_time=0.5
            )
            self.wait(1.25)
        
        self.wait(2)

        self.camera.frame.save_state()

        formula_title = Text("Formula", font_size=60, weight=BOLD)
        formula_title.set_color(GOLD)
        formula_title.shift(RIGHT*16+UP*2.2)
        
        formula = Tex(
            r"RF_l = 1 + \sum_{i=1}^{l} (K_i - 1) \times \prod_{j=1}^{i-1} S_j",
            font_size=80
        )
        formula.set_color(WHITE)
        formula.next_to(formula_title, DOWN, buff=1.195).shift(DOWN*0.6)
        
        self.play(Write(formula_title), Write(formula), self.camera.frame.animate.shift(RIGHT*16),run_time=0.6)
        rect = SurroundingRectangle(formula, color=RED, stroke_width=6).scale(1.1)
        self.play(ShowCreation(rect), run_time=0.6)

        self.wait(2)

        self.play(FadeOut(formula_title), FadeOut(formula), FadeOut(rect), self.camera.frame.animate.restore(), run_time=0.6)
        self.wait(1)

        # ==========================================
        # STRIDE DEMONSTRATION - SHOW ONE AT A TIME
        # ==========================================
        
        # Clear previous content
        part2 = VGroup(
            l1_grid, l1_label, l1_dim, l1_rf, l1_rf_cells, l1_rf_border,
            l2_grid, l2_label, l2_dim, l2_rf, l2_rf_cells, l2_rf_border,
            l3_grid, l3_label, l3_dim, l3_rf, l3_highlight,
            arr1, arr2, k1, k2,
            section2
        )
        self.play(FadeOut(part2), run_time=0.5)
        
        stride_title = Text("Effect of Stride on Receptive Field", font_size=38, weight=BOLD)
        stride_title.set_color(WHITE)
        stride_title.to_edge(UP, buff=0.45).shift(DOWN*0.69)
        
        self.play(FadeIn(stride_title), run_time=0.4)
        
        scell = 0.5
        
        # ==========================================
        # FIRST: SHOW STRIDE = 1 (CENTERED)
        # ==========================================

        s1_title = Text("Stride = 1", font_size=42, weight=BOLD)
        s1_title.set_color(MINT)
        s1_title.move_to(UP * 1.5)
        
        # Input 7x7
        s1_input_grid = VGroup()
        for i in range(7):
            for j in range(7):
                cell = Square(side_length=scell)
                cell.set_fill(BLUE, opacity=0.12)
                cell.set_stroke(BLUE, width=0.8)
                cell.move_to(RIGHT * (j - 3) * scell + DOWN * (i - 3) * scell)
                s1_input_grid.add(cell)
        s1_input_grid.move_to(LEFT * 4.5 + DOWN * 1.32)
        
        s1_input_label = Text("Input: 7x7", font_size=40, weight=BOLD)
        s1_input_label.set_color(BLUE)
        s1_input_label.next_to(s1_input_grid, DOWN, buff=0.39)
        
        # Layer 1 output 5x5
        s1_layer1_grid = VGroup()
        for i in range(5):
            for j in range(5):
                cell = Square(side_length=scell)
                cell.set_fill(MINT, opacity=0.12)
                cell.set_stroke(MINT, width=0.8)
                cell.move_to(RIGHT * (j - 2) * scell + DOWN * (i - 2) * scell)
                s1_layer1_grid.add(cell)
        s1_layer1_grid.move_to(DOWN * 1.32 + RIGHT*1)
        
        s1_layer1_label = Text("5x5", font_size=40)
        s1_layer1_label.set_color(MINT)
        s1_layer1_label.next_to(s1_layer1_grid, DOWN, buff=0.39)
        
        s1_rf1 = Text("RF = 3", font_size=26, weight=BOLD)
        s1_rf1.set_color(GOLD)
        s1_rf1.next_to(s1_layer1_grid, UP, buff=0.3)
        
        # Layer 2 output 3x3
        s1_layer2_grid = VGroup()
        for i in range(3):
            for j in range(3):
                cell = Square(side_length=scell)
                cell.set_fill(LAVENDER, opacity=0.12)
                cell.set_stroke(LAVENDER, width=0.8)
                cell.move_to(RIGHT * (j - 1) * scell + DOWN * (i - 1) * scell)
                s1_layer2_grid.add(cell)
        s1_layer2_grid.move_to(RIGHT * 5.34 + DOWN * 1.32)
        
        s1_layer2_label = Text("3x3", font_size=40)
        s1_layer2_label.set_color(LAVENDER)
        s1_layer2_label.next_to(s1_layer2_grid, DOWN, buff=0.39)
        
        s1_rf2 = Text("RF = 5", font_size=26, weight=BOLD)
        s1_rf2.set_color(GOLD)
        s1_rf2.next_to(s1_layer2_grid, UP, buff=0.3)
        
        # Arrows
        s1_arrow1 = Arrow(s1_input_grid.get_right() + RIGHT*0.15, s1_layer1_grid.get_left() + LEFT*0.15, buff=0.05, stroke_width=2)
        s1_arrow1.set_color(WHITE)
        s1_k1 = Text("3x3, s=1", font_size=30, weight=BOLD)
        s1_k1.set_color(GOLD)
        s1_k1.next_to(s1_arrow1, UP, buff=0.1)
        
        s1_arrow2 = Arrow(s1_layer1_grid.get_right() + RIGHT*0.15, s1_layer2_grid.get_left() + LEFT*0.15, buff=0.05, stroke_width=2)
        s1_arrow2.set_color(WHITE)
        s1_k2 = Text("3x3, s=1", font_size=30, weight=BOLD)
        s1_k2.set_color(GOLD)
        s1_k2.next_to(s1_arrow2, UP, buff=0.1)
        
        # Animate stride=1
        self.play(Write(s1_title), run_time=0.3)
        self.play(
            LaggedStartMap(FadeIn, s1_input_grid, lag_ratio=0.005),
            FadeIn(s1_input_label),
            run_time=0.5
        )
        self.play(GrowArrow(s1_arrow1), FadeIn(s1_k1), run_time=0.3)
        self.play(
            LaggedStartMap(FadeIn, s1_layer1_grid, lag_ratio=0.01),
            FadeIn(s1_layer1_label), FadeIn(s1_rf1),
            run_time=0.5
        )
        self.play(GrowArrow(s1_arrow2), FadeIn(s1_k2), run_time=0.3)
        self.play(
            LaggedStartMap(FadeIn, s1_layer2_grid, lag_ratio=0.02),
            FadeIn(s1_layer2_label), FadeIn(s1_rf2),
            run_time=0.5
        )

        
        # Observation for stride=1
        s1_obs = Tex(r"RF  \ grows \ slower! \ (3 \rightarrow 5)", font_size=38, ).set_color(RED_B)
        s1_obs.move_to(stride_title).scale(1.8)
        
        self.play(FadeIn(s1_obs), FadeOut(stride_title), run_time=0.4)
        self.wait(2)
        
        # Fade out stride=1
        s1_group = VGroup(s1_title, s1_input_grid, s1_input_label, 
                          s1_layer1_grid, s1_layer1_label, s1_rf1,
                          s1_layer2_grid, s1_layer2_label, s1_rf2,
                          s1_arrow1, s1_k1, s1_arrow2, s1_k2, s1_obs)
        self.play(FadeOut(s1_group), run_time=0.5)
        
        # ==========================================
        # SECOND: SHOW STRIDE = 2 (CENTERED)
        # ==========================================
        
        s2_title = Text("Stride = 2", font_size=50, weight=BOLD)
        s2_title.set_color(CORAL)
        s2_title.move_to(UP * 1.5)
        
        # Input 7x7
        s2_input_grid = VGroup()
        for i in range(7):
            for j in range(7):
                cell = Square(side_length=scell)
                cell.set_fill(BLUE, opacity=0.12)
                cell.set_stroke(BLUE, width=0.8)
                cell.move_to(RIGHT * (j - 3) * scell + DOWN * (i - 3) * scell)
                s2_input_grid.add(cell)
        s2_input_grid.move_to(LEFT * 4.5 + DOWN * 1.32)
        
        s2_input_label = Text("Input: 7x7", font_size=40, weight=BOLD)
        s2_input_label.set_color(BLUE)
        s2_input_label.next_to(s2_input_grid, DOWN, buff=0.39)
        
        # Layer 1 output 3x3 (stride=2: floor((7-3)/2)+1 = 3)
        s2_layer1_grid = VGroup()
        for i in range(3):
            for j in range(3):
                cell = Square(side_length=scell)
                cell.set_fill(CORAL, opacity=0.12)
                cell.set_stroke(CORAL, width=0.8)
                cell.move_to(RIGHT * (j - 1) * scell + DOWN * (i - 1) * scell)
                s2_layer1_grid.add(cell)
        s2_layer1_grid.move_to(DOWN * 1.32 + RIGHT*1)
        
        s2_layer1_label = Text("3x3", font_size=40)
        s2_layer1_label.set_color(CORAL)
        s2_layer1_label.next_to(s2_layer1_grid, DOWN, buff=0.39)
        
        s2_rf1 = Text("RF = 3", font_size=26, weight=BOLD)
        s2_rf1.set_color(GOLD)
        s2_rf1.next_to(s2_layer1_grid, UP, buff=0.3)
        
        # Layer 2 output 1x1 (stride=1: 3-3+1 = 1)
        s2_layer2_grid = VGroup()
        cell = Square(side_length=scell * 1.5)
        cell.set_fill(LAVENDER, opacity=0.12)
        cell.set_stroke(LAVENDER, width=0.8)
        s2_layer2_grid.add(cell)
        s2_layer2_grid.move_to(RIGHT * 5.34 + DOWN * 1.32)
        
        s2_layer2_label = Text("1x1", font_size=40)
        s2_layer2_label.set_color(LAVENDER)
        s2_layer2_label.next_to(s2_layer2_grid, DOWN, buff=0.39)
        
        s2_rf2 = Text("RF = 7", font_size=26, weight=BOLD)
        s2_rf2.set_color(CORAL)
        s2_rf2.next_to(s2_layer2_grid, UP, buff=0.3)
        
        # Arrows
        s2_arrow1 = Arrow(s2_input_grid.get_right() + RIGHT*0.15, s2_layer1_grid.get_left() + LEFT*0.15, buff=0.05, stroke_width=2)
        s2_arrow1.set_color(WHITE)
        s2_k1 = Text("3x3, s=2", font_size=30, weight=BOLD)
        s2_k1.set_color(GOLD)
        s2_k1.next_to(s2_arrow1, UP, buff=0.1)
        
        s2_arrow2 = Arrow(s2_layer1_grid.get_right() + RIGHT*0.15, s2_layer2_grid.get_left() + LEFT*0.15, buff=0.05, stroke_width=2)
        s2_arrow2.set_color(WHITE)
        s2_k2 = Text("3x3, s=1", font_size=30, weight=BOLD)
        s2_k2.set_color(GOLD)
        s2_k2.next_to(s2_arrow2, UP, buff=0.1)
        
        # Animate stride=2
        self.play(FadeIn(s2_title), run_time=0.3)
        self.play(
            LaggedStartMap(FadeIn, s2_input_grid, lag_ratio=0.005),
            FadeIn(s2_input_label),
            run_time=0.5
        )
        self.play(GrowArrow(s2_arrow1), FadeIn(s2_k1), run_time=0.3)
        self.play(
            LaggedStartMap(FadeIn, s2_layer1_grid, lag_ratio=0.02),
            FadeIn(s2_layer1_label), FadeIn(s2_rf1),
            run_time=0.5
        )
        self.play(GrowArrow(s2_arrow2), FadeIn(s2_k2), run_time=0.3)
        self.play(
            LaggedStartMap(FadeIn, s2_layer2_grid, lag_ratio=0.02),
            FadeIn(s2_layer2_label), FadeIn(s2_rf2),
            run_time=0.5
        )
        
        # Observation for stride=2
        s2_obs = Tex(r"RF  \ grows \ much \ faster! \ (3 \rightarrow 7)", font_size=38, )
        s2_obs.set_color(GREEN_B)
        s2_obs.move_to(stride_title).scale(1.8)
        
        self.play(FadeIn(s2_obs), run_time=0.4)
        self.wait(2)


        # Key insight box
        insight_box = RoundedRectangle(width=10, height=1.5, corner_radius=0.1)
        insight_box.set_fill(BLACK, opacity=0.96)
        insight_box.set_stroke(GOLD, width=2)
        insight_box.to_edge(DOWN, buff=0.3)
        
        insight_text = VGroup(
            Text("Stride > 1 accelerates RF growth", font_size=26, weight=BOLD),
            Text("because each layer covers more input space", font_size=22),
        )
        insight_text[0].set_color(GOLD)
        insight_text[1].set_color(GREY_A)
        insight_text.arrange(DOWN, buff=0.15)
        insight_text.move_to(insight_box.get_center())

        a = VGroup(insight_box, insight_text).move_to(Group(stride_title, s2_title))

        a.scale(1.3)
        
        self.play(FadeOut(s2_obs), FadeOut(s2_title),run_time=0.2)
        self.play(FadeIn(a), run_time=0.5)
        
        self.wait(2)

        
        
        # Clean up stride section
        stride_section = VGroup(
            s2_input_grid, s2_input_label,
            s2_layer1_grid, s2_layer1_label, s2_rf1,
            s2_layer2_grid, s2_layer2_label, s2_rf2,
            s2_arrow1, s2_k1, s2_arrow2, s2_k2,
            insight_box, insight_text
        )
        
        self.play(FadeOut(stride_section), run_time=0.5)


        # ==========================================
        # FEATURE HIERARCHY EXPLANATION
        # ==========================================
        
        # Feature hierarchy section
        feature_title = Text("Why Receptive Field Matters", font_size=42, weight=BOLD)
        feature_title.set_color(WHITE)
        feature_title.to_edge(UP, buff=0.45).shift(DOWN)
        
        self.play(Write(feature_title), run_time=0.5)

        self.wait(1.5)

        # Create layer visualization
        layer_box_w = 3.2
        layer_box_h = 1.9
        
        # Early layer
        early_box = RoundedRectangle(width=layer_box_w, height=layer_box_h, corner_radius=0.1)
        early_box.set_fill(BLUE, opacity=0.2)
        early_box.set_stroke(BLUE, width=2)
        early_box.move_to(LEFT * 4.8 + DOWN * 1.2)
        
        early_title = Text("Early Layers", font_size=30, weight=BOLD)
        early_title.set_color(BLUE)
        early_title.next_to(early_box, UP, buff=0.3)
        
        early_rf = Text("Small RF", font_size=20)
        early_rf.set_color(GREY_A)
        early_rf.move_to(early_box.get_top() + DOWN * 0.38)
        
        early_features = VGroup(
            Text("• Edges", font_size=20),
            Text("• Corners", font_size=20),
            Text("• Simple textures", font_size=20),
        )
        early_features.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        early_features.set_color(GREY_B)
        early_features.next_to(early_rf, DOWN, buff=0.18)
        
        # Middle layer
        mid_box = RoundedRectangle(width=layer_box_w, height=layer_box_h, corner_radius=0.1)
        mid_box.set_fill(MINT, opacity=0.2)
        mid_box.set_stroke(MINT, width=2)
        mid_box.move_to(DOWN * 1.2)
        
        mid_title = Text("Middle Layers", font_size=30, weight=BOLD)
        mid_title.set_color(MINT)
        mid_title.next_to(mid_box, UP, buff=0.3)
        
        mid_rf = Text("Medium RF", font_size=20)
        mid_rf.set_color(GREY_A)
        mid_rf.move_to(mid_box.get_top() + DOWN * 0.38)
        
        mid_features = VGroup(
            Text("• Shapes", font_size=20),
            Text("• Patterns", font_size=20),
            Text("• Object parts", font_size=20),
        )
        mid_features.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        mid_features.set_color(GREY_B)
        mid_features.next_to(mid_rf, DOWN, buff=0.18)
        
        # Deep layer
        deep_box = RoundedRectangle(width=layer_box_w, height=layer_box_h, corner_radius=0.1)
        deep_box.set_fill(LAVENDER, opacity=0.2)
        deep_box.set_stroke(LAVENDER, width=2)
        deep_box.move_to(RIGHT * 4.8 + DOWN * 1.2)
        
        deep_title = Text("Deep Layers", font_size=30, weight=BOLD)
        deep_title.set_color(LAVENDER)
        deep_title.next_to(deep_box, UP, buff=0.3)
        
        deep_rf = Text("Large RF", font_size=20)
        deep_rf.set_color(GREY_A)
        deep_rf.move_to(deep_box.get_top() + DOWN * 0.38)
        
        deep_features = VGroup(
            Text("• Full objects", font_size=20),
            Text("• Faces", font_size=20),
            Text("• Semantic content", font_size=20),
        )
        deep_features.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        deep_features.set_color(GREY_B)
        deep_features.next_to(deep_rf, DOWN, buff=0.18)
        
        # Arrows between boxes
        arr_1 = Arrow(early_box.get_right(), mid_box.get_left(), buff=0.18, stroke_width=2)
        arr_1.set_color(WHITE)
        arr_2 = Arrow(mid_box.get_right(), deep_box.get_left(), buff=0.18, stroke_width=2)
        arr_2.set_color(WHITE)
        
        # Animate
        self.play(
            FadeIn(early_box), FadeIn(early_title),
            FadeIn(early_rf), FadeIn(early_features),
            run_time=0.5
        )
        self.play(
            GrowArrow(arr_1),
            FadeIn(mid_box), FadeIn(mid_title),
            FadeIn(mid_rf), FadeIn(mid_features),
            run_time=0.5
        )
        self.play(
            GrowArrow(arr_2),
            FadeIn(deep_box), FadeIn(deep_title),
            FadeIn(deep_rf), FadeIn(deep_features),
            run_time=0.5
        )
        
        # Key insight
        insight = Tex(
            r"Larger \ receptive \ field  \rightarrow Can \ detect \ more \ complex, \ global \ features",
            font_size=43,
        )
        insight.set_color(GOLD)
        insight.to_edge(DOWN, buff=0.37)
        
        self.play(FadeIn(insight, shift=UP * 0.2), run_time=0.5)
        
        self.wait(3)



        # ==========================================
        # SUMMARY
        # ==========================================
        
        self.play(
            FadeOut(VGroup(
                feature_title,
                early_box, early_title, early_rf, early_features,
                mid_box, mid_title, mid_rf, mid_features,
                deep_box, deep_title, deep_rf, deep_features,
                arr_1, arr_2, insight
            )),
            run_time=0.5
        )
        
        # Final summary
        summary = Text("Summary", font_size=60, weight=BOLD)
        summary.set_color(GOLD)
        summary.to_edge(UP, buff=0.15).shift(DOWN*0.9999)
        
        self.play(Write(summary), run_time=0.4)
        
        # Formula
        final_formula = Tex(
            r"RF_l = 1 + \sum_{i=1}^{l} (K_i - 1) \times \prod_{j=1}^{i-1} S_j",
            font_size=68
        )
        final_formula.set_color(WHITE)
        final_formula.next_to(summary, DOWN, buff=0.35)
        
        self.play(Write(final_formula), run_time=0.5)
        
        # Points
        points = VGroup(
            Text("RF = input region affecting one output pixel", font_size=30),
            Text("Stacking 3x3 kernels grows RF efficiently", font_size=30),
            Text("Stride > 1 accelerates RF growth", font_size=30),
            Text("Early layers: small RF → edges, textures", font_size=30),
            Text("Deep layers: large RF → objects, semantics", font_size=30),
        )
        points.arrange(DOWN, aligned_edge=LEFT, buff=0.199)
        points.next_to(final_formula, DOWN, buff=0.77)
        
        
        for i in range(5):
            self.play(Write(points[i]))
            self.wait(1.5)
        
        self.wait(3)
        
        # Clear summary
        self.play(FadeOut(VGroup(summary, final_formula, points)), run_time=0.5)


PURE_RED = "#FF0000"
FEATURE_COLOR = "#DA1F1F"

class FeatureExtraction_Explained(Scene):
    
    def construct(self):
        
        # ==========================================
        # STEP 0: Generate feature images from cat.jpeg
        # ==========================================
        
        img = Image.open("cat.jpeg")
        img_gray = img.convert("L")  # Grayscale
        
        # 1. Edge detection
        edges = img_gray.filter(ImageFilter.FIND_EDGES)
        edges = ImageOps.autocontrast(edges)
        edges.save("cat_edges.png")
        
        # 2. Textures (emboss filter)
        texture = img_gray.filter(ImageFilter.EMBOSS)
        texture = ImageOps.autocontrast(texture)
        texture.save("cat_texture.png")
        
        # 3. Shapes/Parts (contour filter)
        shapes = img_gray.filter(ImageFilter.CONTOUR)
        shapes = ImageOps.invert(shapes)
        shapes.save("cat_shapes.png")
        
        # 4. Contrast (edge enhance + sharpen)
        contrast = img_gray.filter(ImageFilter.EDGE_ENHANCE_MORE)
        contrast = ImageOps.autocontrast(contrast)
        contrast.save("cat_contrast.png")
        
        # ==========================================
        # PART 1: Show original cat image
        # ==========================================
        
        cat_img = ImageMobject("cat.jpeg")
        cat_img.set_height(4.5)
        cat_img.move_to(LEFT * 4)
        
        cat_border = SurroundingRectangle(cat_img, color=WHITE, stroke_width=4, buff=0.05)
        cat_label = Text("Original Image", font_size=32, weight=BOLD)
        cat_label.next_to(cat_img, DOWN, buff=0.3)
        
        self.play(FadeIn(cat_img), ShowCreation(cat_border))
        self.play(Write(cat_label))
        self.wait(1)
        
        # ==========================================
        # PART 2: Create all feature images on the right
        # ==========================================
        
        # Colors for each feature
        EDGE_COLOR = RED
        TEXTURE_COLOR = GREEN
        SHAPE_COLOR = BLUE
        CONTRAST_COLOR = YELLOW
        
        # Feature 1: Edges (top-left)
        edges_img = ImageMobject("cat_edges.png")
        edges_img.set_height(2.0)
        edges_img.move_to(RIGHT * 2 + UP * 2)
        edges_border = SurroundingRectangle(edges_img, color=EDGE_COLOR, stroke_width=3, buff=0.05)
        edges_label = Text("Edges", font_size=24, weight=BOLD).set_color(EDGE_COLOR)
        edges_label.next_to(edges_img, DOWN, buff=0.15)
        
        # Feature 2: Textures (top-right)
        texture_img = ImageMobject("cat_texture.png")
        texture_img.set_height(2.0)
        texture_img.move_to(RIGHT * 5.5 + UP * 2)
        texture_border = SurroundingRectangle(texture_img, color=TEXTURE_COLOR, stroke_width=3, buff=0.05)
        texture_label = Text("Textures", font_size=24, weight=BOLD).set_color(TEXTURE_COLOR)
        texture_label.next_to(texture_img, DOWN, buff=0.15)
        
        # Feature 3: Shapes/Parts (bottom-left)
        shapes_img = ImageMobject("cat_shapes.png")
        shapes_img.set_height(2.0)
        shapes_img.move_to(RIGHT * 2 + DOWN * 1.5)
        shapes_border = SurroundingRectangle(shapes_img, color=SHAPE_COLOR, stroke_width=3, buff=0.05)
        shapes_label = Text("Parts", font_size=24, weight=BOLD).set_color(SHAPE_COLOR)
        shapes_label.next_to(shapes_img, DOWN, buff=0.15)
        
        # Feature 4: Contrast (bottom-right)
        contrast_img = ImageMobject("cat_contrast.png")
        contrast_img.set_height(2.0)
        contrast_img.move_to(RIGHT * 5.5 + DOWN * 1.5)
        contrast_border = SurroundingRectangle(contrast_img, color=CONTRAST_COLOR, stroke_width=3, buff=0.05)
        contrast_label = Text("Contrast", font_size=24, weight=BOLD).set_color(CONTRAST_COLOR)
        contrast_label.next_to(contrast_img, DOWN, buff=0.15)
        
        # ==========================================
        # PART 3: Arrows and animations
        # ==========================================
        
        # Arrow to Edges
        arrow_edges = Arrow(
            cat_border.get_right(),
            edges_border.get_left(),
            buff=0.15,
            stroke_width=4
        ).set_color(EDGE_COLOR).set_z_index(3)
        
        self.play(GrowArrow(arrow_edges))
        self.play(
            FadeIn(edges_img),
            ShowCreation(edges_border),
            Write(edges_label),
            run_time=0.8
        )
        self.wait(0.3)
        
        # Arrow to Textures
        arrow_texture = Arrow(
            cat_border.get_right(),
            texture_border.get_left(),
            buff=0.15,
            stroke_width=4
        ).set_color(TEXTURE_COLOR).set_z_index(3)
        
        self.play(GrowArrow(arrow_texture))
        self.play(
            FadeIn(texture_img),
            ShowCreation(texture_border),
            Write(texture_label),
            run_time=0.8
        )
        self.wait(0.3)
        
        # Arrow to Shapes/Parts
        arrow_shapes = Arrow(
            cat_border.get_right(),
            shapes_border.get_left(),
            buff=0.15,
            stroke_width=4
        ).set_color(SHAPE_COLOR).set_z_index(3)
        
        self.play(GrowArrow(arrow_shapes))
        self.play(
            FadeIn(shapes_img),
            ShowCreation(shapes_border),
            Write(shapes_label),
            run_time=0.8
        )
        self.wait(0.3)
        
        # Arrow to Contrast
        arrow_contrast = Arrow(
            cat_border.get_right(),
            contrast_border.get_left(),
            buff=0.15,
            stroke_width=4
        ).set_color(CONTRAST_COLOR).set_z_index(3)
        
        self.play(GrowArrow(arrow_contrast))
        self.play(
            FadeIn(contrast_img),
            ShowCreation(contrast_border),
            Write(contrast_label),
            run_time=0.8
        )
        self.wait(1)

        self.play(FadeOut(arrow_contrast), FadeOut(arrow_edges), FadeOut(arrow_shapes), FadeOut(arrow_texture))
        
        # ==========================================
        # PART 4: Pulse all features together
        # ==========================================
        
        all_borders = VGroup(edges_border, texture_border, shapes_border, contrast_border)
        
        self.play(
            all_borders.animate.set_stroke(width=6),
            rate_func=there_and_back,
            run_time=0.8
        )
        self.play(
            all_borders.animate.set_stroke(width=6),
            rate_func=there_and_back,
            run_time=0.8
        )
        
        self.wait(2)
        
        self.embed()


class Convolution_Over_Volume(ThreeDScene):
    
    def construct(self):
        
        # Set up camera for 3D view
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)
        self.camera.frame.scale(1.3).shift(UP * 0.5)
        
        # ==========================================
        # SETUP: Create 6x6x3 Input Volume (RGB)
        # ==========================================
        
        cell_size = 0.4
        
        # Colors for each channel
        channel_colors = ["#ff0000", "#00ff00", "#0000ff"]  # R, G, B
        
        # Create input volume using 3D cubes
        input_volume = VGroup()
        input_cells = {}
        
        for z in range(3):  # Depth: 0=Red, 1=Green, 2=Blue
            for i in range(6):  # Rows
                for j in range(6):  # Columns
                    cube = Cube(side_length=cell_size)
                    cube.set_fill(channel_colors[z], opacity=0.7)
                    cube.set_stroke(channel_colors[z], width=1)
                    cube.move_to(
                        RIGHT * j * cell_size + 
                        DOWN * i * cell_size + 
                        OUT * z * cell_size
                    )
                    input_cells[(i, j, z)] = cube
                    input_volume.add(cube)
        
        input_volume.center()
        input_volume.move_to(LEFT * 4)
        
        input_label = Text("6 × 6 × 3", font_size=32, weight=BOLD)
        input_label.next_to(input_volume, UP, buff=0.6)
        input_label.rotate(65 * DEGREES, axis=RIGHT)
        
        # ==========================================
        # SETUP: Create 3x3x3 Filter (Yellow)
        # ==========================================
        
        filter_volume = VGroup()
        filter_cells = {}
        
        for z in range(3):
            for i in range(3):
                for j in range(3):
                    cube = Cube(side_length=cell_size)
                    cube.set_fill(YELLOW, opacity=0.85)
                    cube.set_stroke("#ffff00", width=1)
                    cube.move_to(
                        RIGHT * j * cell_size + 
                        DOWN * i * cell_size + 
                        OUT * z * cell_size
                    )
                    filter_cells[(i, j, z)] = cube
                    filter_volume.add(cube)
        
        filter_volume.center()
        filter_volume.move_to(ORIGIN)
        
        filter_label = Text("3 × 3 × 3", font_size=32, weight=BOLD)
        filter_label.set_color(YELLOW)
        filter_label.next_to(filter_volume, UP, buff=0.6)
        filter_label.rotate(65 * DEGREES, axis=RIGHT)
        
        # ==========================================
        # SETUP: Create 4x4x1 Output (White)
        # ==========================================
        
        output_volume = VGroup()
        output_cells = {}
        
        for i in range(4):
            for j in range(4):
                cube = Cube(side_length=cell_size)
                cube.set_fill(WHITE, opacity=0.3)
                cube.set_stroke("#ffffff", width=1)
                cube.move_to(
                    RIGHT * j * cell_size + 
                    DOWN * i * cell_size
                )
                output_cells[(i, j)] = cube
                output_volume.add(cube)
        
        output_volume.center()
        output_volume.move_to(RIGHT * 4)
        
        output_label = Text("4 × 4", font_size=32, weight=BOLD)
        output_label.set_color(WHITE)
        output_label.next_to(output_volume, UP, buff=0.6)
        output_label.rotate(65 * DEGREES, axis=RIGHT)
        
        # ==========================================
        # SETUP: Symbols
        # ==========================================
        
        asterisk = Tex(r"\times", font_size=72)
        asterisk.set_color(WHITE)
        asterisk.move_to(LEFT * 1.8)
        
        equals_sign = Tex(r"=", font_size=72)
        equals_sign.set_color(WHITE)
        equals_sign.move_to(RIGHT * 1.8)
        
        # ==========================================
        # PART 1: Show input volume
        # ==========================================
        
        self.play(
            LaggedStartMap(FadeIn, input_volume, lag_ratio=0.01),
            run_time=2
        )
        
        self.play(
            Write(input_label),
            run_time=1
        )
        self.wait(0.5)
        
        # Rotate camera to show 3D structure
        self.play(
            self.camera.frame.animate.increment_theta(30 * DEGREES),
            run_time=2
        )
        self.play(
            self.camera.frame.animate.increment_theta(-30 * DEGREES),
            run_time=2
        )
        
        # ==========================================
        # PART 2: Show filter
        # ==========================================
        
        self.play(Write(asterisk), run_time=0.5)
        
        self.play(
            LaggedStartMap(FadeIn, filter_volume, lag_ratio=0.02),
            run_time=1.5
        )
        
        self.play(
            Write(filter_label),
            run_time=1
        )
        self.wait(0.5)
        
        # ==========================================
        # PART 3: Show output
        # ==========================================
        
        self.play(Write(equals_sign), run_time=0.5)
        
        self.play(
            LaggedStartMap(FadeIn, output_volume, lag_ratio=0.03),
            run_time=1
        )
        
        self.play(
            Write(output_label),
            run_time=1
        )
        self.wait(1)
        
        # ==========================================
        # PART 4: Move filter over input and convolve
        # ==========================================
        
        self.play(
            FadeOut(asterisk),
            FadeOut(equals_sign),
            FadeOut(filter_label),
            FadeOut(input_label),
            run_time=0.8
        )
        
        # Make filter semi-transparent
        self.play(
            *[cube.animate.set_fill(YELLOW, opacity=0.4) for cube in filter_volume],
            run_time=0.5
        )
        
        # Get reference positions
        # Input cell (1,1,1) is the center of where filter should go first
        # Filter center is at (1,1,1)
        
        # Calculate first position
        # We want filter's center cell (1,1,1) to align with input's (1,1,1)
        input_center_cell = input_cells[(1, 1, 1)]
        filter_center_cell = filter_cells[(1, 1, 1)]
        
        filter_offset = filter_volume.get_center() - filter_center_cell.get_center()
        first_pos = input_center_cell.get_center() + filter_offset
        
        self.play(
            filter_volume.animate.move_to(first_pos),
            run_time=1
        )
        self.wait(0.5)
        
        # ==========================================
        # PART 5: Convolve - fill output cells
        # ==========================================
        
        for out_row in range(4):
            for out_col in range(4):
                # Filter center at input (out_row+1, out_col+1, 1)
                target_input_cell = input_cells[(out_row + 1, out_col + 1, 1)]
                target_pos = target_input_cell.get_center() + filter_offset
                
                # Move filter (skip first)
                if not (out_row == 0 and out_col == 0):
                    self.play(
                        filter_volume.animate.move_to(target_pos),
                        run_time=0.35
                    )
                
                # Fill output cell
                self.play(
                    output_cells[(out_row, out_col)].animate.set_fill(WHITE, opacity=0.9),
                    run_time=0.25
                )
        
        self.wait(1)
        
        # ==========================================
        # PART 6: Restore and final view
        # ==========================================
        
        self.play(
            filter_volume.animate.move_to(ORIGIN),
            run_time=0.8
        )
        
        self.play(
            *[cube.animate.set_fill(YELLOW, opacity=0.85) for cube in filter_volume],
            run_time=0.5
        )
        
        self.play(
            FadeIn(asterisk),
            FadeIn(equals_sign),
            FadeIn(filter_label),
            FadeIn(input_label),
            run_time=0.8
        )
        
        self.wait(1)
        
        # ==========================================
        # PART 7: Final camera rotation to show result
        # ==========================================
        
        self.play(
            self.camera.frame.animate.increment_theta(60 * DEGREES),
            run_time=3
        )
        
        self.wait(1)
        
        # Key insight
        insight = Text("3D Volume → 2D Output", font_size=36, weight=BOLD)
        insight.set_color(TEAL_B)
        insight.to_edge(DOWN, buff=0.5)
        insight.fix_in_frame()
        
        self.play(Write(insight), run_time=1.5)
        
        self.wait(3)


class CNN_Intro(Scene):
    
    def construct(self):

        self.camera.frame.shift(RIGHT*6).scale(1.16)
                
        # ==========================================
        # PART 1: Create Neural Network (like original)
        # ==========================================
        
        HIDDEN_COLOR = BLUE
        OUTPUT_COLOR = ORANGE

        layer_sizes = [5, 6, 4, 3, 1]
        layer_spacing = 2.5  # 30% reduced
        neuron_spacing = 1.2

        layers = []

        # ===== CREATE NEURONS =====
        for i, size in enumerate(layer_sizes):
            layer = VGroup()
            for j in range(size):
                neuron = Circle(radius=0.22, color=WHITE, fill_opacity=0.15).set_z_index(1)
                if i == 0:
                    neuron.set_fill(GREEN, opacity=1).set_stroke(GREEN_B).scale(1.2).set_z_index(1)
                elif i == len(layer_sizes) - 1:
                    neuron.set_fill(OUTPUT_COLOR, opacity=1).set_stroke(RED_B).scale(2).set_z_index(1)
                else:
                    neuron.set_fill(HIDDEN_COLOR, opacity=1).set_stroke(BLUE_B).scale(1.7)
                neuron.move_to(RIGHT * 1.24 * i * layer_spacing + UP * (j - (size - 1) / 2) * neuron_spacing).set_z_index(1)
                layer.add(neuron)
            layers.append(layer)

        network = VGroup(*layers)

        # ===== CREATE CONNECTIONS =====
        connections = VGroup()
        for l1, l2 in zip(layers[:-1], layers[1:]):
            for n1 in l1:
                for n2 in l2:
                    line = Line(
                        n1.get_center(), n2.get_center(),
                        color=GREY_B, stroke_width=1.5
                    ).set_z_index(-1)
                    connections.add(line)
        
        connections.set_z_index(-1)

        # ===== ANIMATE: Neurons FIRST, then connections =====
        self.play(
            LaggedStartMap(GrowFromCenter, network, lag_ratio=0.05, run_time=1.5),
        )
        self.play(
            LaggedStartMap(ShowCreation, connections, lag_ratio=0.01, run_time=1.5),
        )
        self.wait(2)

        
        # ==========================================
        # PART 2: Show Image - Move Camera Left
        # ==========================================
        
        gap = 2.0
        conv_width = 2.0
        
        # Load cat image
        image = ImageMobject("cat.jpeg")
        image.set_height(3.0)
        image.next_to(layers[0], LEFT, buff=gap + conv_width + gap)
        
        image_label = Text("Input Image", font_size=44, weight=BOLD)
        image_label.next_to(image, UP, buff=0.47)
        
        # Add border to image
        border = SurroundingRectangle(image, color=MAROON_C, stroke_width=3, buff=0.05)
        
        # Move camera to show image
        self.play(
            self.camera.frame.animate.shift(LEFT * 9).scale(1.17),
            FadeIn(image),
            ShowCreation(border),
            Write(image_label),
            run_time=1.5
        )
        self.wait(1)
        
        # Show image dimensions
        dim_text = Tex(r"100 \times 100 \times 3", font_size=44, color=YELLOW)
        dim_text.next_to(image, DOWN, buff=0.4).scale(1.4).shift(DOWN*0.34)
        
        self.play(Write(dim_text))
        self.wait(2)

        
        # Calculate total inputs
        calc_text = Tex(r"= 30{,}000 \text{ pixels!}", font_size=44, color=PURE_RED)
        calc_text.next_to(dim_text, DOWN, buff=0.3).scale(1.4).shift(DOWN*0.34)
        
        self.play(Write(calc_text))
        
        calc_box = SurroundingRectangle(calc_text, color=PURE_RED, buff=0.12).scale(1.1)
        self.play(ShowCreation(calc_box))
        self.wait(2)
        
        # ==========================================
        # PART 3: Show Direct Input Problem
        # TransformFromCopy(border, VGroup of input neurons)
        # ==========================================
        
        input_neurons = layers[0]
        
        # TransformFromCopy the image border to the input layer VGroup
        # This shows the whole image being fed directly to inputs
        self.play(
            TransformFromCopy(border.copy(), input_neurons.copy().set_stroke(WHITE, width=3)),
            run_time=1
        )
        self.wait(1)
        
        # Show problem text
        problem_text = Text("30,000 inputs → Millions of parameters!", color=PURE_RED, font_size=50).shift(RIGHT*2.6)
        problem_text.next_to(calc_box, DOWN, buff=0.4).shift(RIGHT*5+DOWN*0.56)
        self.play(Write(problem_text), FadeOut(calc_text), FadeOut(calc_box), self.camera.frame.animate.shift(DOWN))
        self.wait(2)

        # ==========================================
        # PART 4: Solution - Conv Layer Feature Extractor
        # ==========================================
        
        # Fade out ALL problem indicators
        self.play(
            FadeOut(problem_text),
            FadeOut(dim_text),
            self.camera.frame.animate.shift(UP*RIGHT*0.4)
        )
        self.wait(1)
        
        # Create Conv Layer box - EQUIDISTANT from image and input layer
        conv_box = RoundedRectangle(
            width=conv_width,
            height=3.5,
            corner_radius=0.25,
            fill_color=FEATURE_COLOR,
            fill_opacity=0.2,
            stroke_color=FEATURE_COLOR,
            stroke_width=4
        )
        # Position exactly in the middle
        conv_center_x = (image.get_right()[0] + layers[0].get_left()[0]) / 2
        conv_box.move_to([conv_center_x, 0, 0])
        
        # Two-line label: CONV \n LAYER
        conv_label = VGroup(
            Text("CONV", font_size=36, color=FEATURE_COLOR, weight=BOLD),
            Text("LAYER", font_size=36, color=FEATURE_COLOR, weight=BOLD),
        )
        conv_label.arrange(DOWN, buff=0.1)
        conv_label.move_to(conv_box.get_center())
        
        # Show conv box
        self.play(ShowCreation(conv_box), run_time=1)
        self.play(Write(conv_label))
        self.wait(0.5)

        
        # Arrow from image to Conv
        arrow1 = Arrow(
            image.get_right(),
            conv_box.get_left(),
            buff=0.15,
            color=WHITE,
            stroke_width=4
        ).set_color(WHITE)
        self.play(GrowArrow(arrow1))
        self.wait(0.5)

        # ==========================================
        # PART 4b: Image -> Conv box (image shrinks to center, then label appears)
        # ==========================================
        
        # Create a copy of image that will move to conv box
        image_copy = image.copy()
        
        # Move and shrink image copy to center of conv box
        self.play(
            image_copy.animate.move_to(conv_box.get_center()).scale(0.24),
            run_time=1.5
        )
        
        # Fade out image copy and show the CONV LAYER text
        self.play(
            FadeOut(image_copy),
            run_time=1
        )
        self.wait(1)
        
        # Feature descriptions below Conv box
        features_text = VGroup(
            Text("• Edge Detection", font_size=40, color=GREY_A, weight=BOLD),
            Text("• Texture Analysis", font_size=40, color=GREY_A, weight=BOLD),
            Text("• Shape Recognition", font_size=40, color=GREY_A, weight=BOLD),
        )
        features_text.arrange(DOWN, aligned_edge=LEFT, buff=0.48)
        features_text.next_to(conv_box, DOWN, buff=1)
        
        self.play(LaggedStartMap(FadeIn, features_text, lag_ratio=0.15))
        self.wait(1)
        
        
        # ==========================================
        # PART 4c: Conv box -> Input neurons
        # Create orange feature circles, then TransformFromCopy to inputs
        # ==========================================
        
        # Create feature circles inside conv box
        feature_circles = VGroup()
        for i in range(5):
            circle = Circle(
                radius=0.18,
                fill_color=PURPLE_C,
                fill_opacity=0.9,
                stroke_width=2,
                stroke_color=WHITE
            )
            y_offset = (2 - i) * 0.55
            circle.move_to(conv_box.get_center() + UP * y_offset)
            feature_circles.add(circle)
        
        self.play(LaggedStartMap(GrowFromCenter, feature_circles, lag_ratio=0.1))
        self.wait(0.5)
        
        # Arrow from Conv to input layer
        arrow2 = Arrow(
            conv_box.get_right(),
            layers[0].get_left(),
            buff=0.15,
            color=WHITE,
            stroke_width=4
        ).set_color(WHITE)
        self.play(GrowArrow(arrow2))
        self.wait(0.5)
        
        # TransformFromCopy: each orange circle -> corresponding input neuron
        self.play(
            *[Transform(feature_circles, neuron)
              for feature_circles, neuron in zip(feature_circles, input_neurons)],
            run_time=2
        )
        self.wait(0.5)
        
        
        # ==========================================
        # PART 5: Show the Benefit
        # ==========================================
        
        # New calculation showing reduced inputs
        new_calc = Tex(r"30{,}000 \rightarrow 256 \text{ features}", font_size=36)
        new_calc.next_to(features_text, DOWN, buff=0.4)
        new_calc[:6].set_color(PURE_RED)
        new_calc[7:].set_color(GREEN)

        new_calc.scale(3).shift(UP*1.4)
        
        self.play(Write(new_calc), FadeOut(features_text))
        
        benefit_box = SurroundingRectangle(new_calc, stroke_width=6).scale(1.23)
        self.play(ShowCreation(benefit_box))
        self.wait(2)


        # Pan camera to show full pipeline
        self.play(
            self.camera.frame.animate.scale(1.32).shift(RIGHT*4.2).shift(DOWN*0.56),
            FadeOut(benefit_box),
            FadeOut(new_calc),
            run_time=1
        )
        self.wait(1)
        
        
        # Final summary at bottom
        summary = VGroup(
            Text("Image", font_size=26),
            Tex(r"\rightarrow", font_size=34),
            Text("Conv Layer", font_size=26, color=FEATURE_COLOR),
            Tex(r"\rightarrow", font_size=34),
            Text("Features", font_size=26, color=GREEN),
            Tex(r"\rightarrow", font_size=34),
            Text("ANN", font_size=26, color=BLUE),
            Tex(r"\rightarrow", font_size=34),
            Text("Output", font_size=26, color=ORANGE),
        )
        summary.arrange(RIGHT, buff=0.2)
        summary.to_edge(DOWN, buff=0.5).scale(2.2).shift(DOWN*2.3+RIGHT*0.8)
        
        self.play(
            LaggedStartMap(FadeIn, summary, lag_ratio=0.1),
            run_time=2
        )
        
        # Highlight the key insight
        insight_box = SurroundingRectangle(summary[2:5], color=YELLOW,).scale(1.044)
        self.play(ShowCreation(insight_box))
        
        insight_text = Text("Reduces complexity!", font_size=56, weight=BOLD).set_color(PURPLE_C)
        insight_text.next_to(insight_box, DOWN, buff=0.5)
        self.play(Write(insight_text))
        
        self.wait(1)
        
        # Checkmark with proper green color
        check = Tex(r"\checkmark", font_size=130)
        check.set_color("#00ff00")
        check.next_to(insight_text, RIGHT, buff=0.6)
        self.play(Write(check))
        
        self.wait(3)


        self.camera.frame.save_state()



        # ==========================================
        # PART 6: NEW - Full CNN Pipeline
        # Keep ANN intact, fade out texts/boxes/arrows, move image left
        # Build Conv -> Pool -> Conv -> Pool -> Features -> ANN
        # ==========================================
        
        # Fade out only the texts, boxes, arrows, conv box - NOT the network
        self.play(
            FadeOut(summary),
            FadeOut(insight_box),
            FadeOut(insight_text),
            FadeOut(check),
            FadeOut(conv_box),
            FadeOut(conv_label),
            FadeOut(arrow1),
            FadeOut(arrow2),
            FadeOut(image_label),
            FadeOut(feature_circles),
            run_time=1.5
        )
        
        # Group image and border together (use Group, not VGroup, because ImageMobject is not a VMobject)
        image_group = Group(image, border)
        
        # Move image+border far to the left
        self.play(
            image_group.animate.shift(LEFT * 15),
            self.camera.frame.animate.scale(1.2).shift(LEFT*13.4),
            run_time=1.5
        )
        self.wait(0.5)

        # ==========================================
        # Helper function to create stacked rounded rects
        # ==========================================
        def create_layer_stack(num_filters, width, height, color, depth_offset=0.15):
            """Create stacked rounded rectangles representing filters/channels"""
            stack = VGroup()
            for i in range(num_filters):
                rect = RoundedRectangle(
                    width=width,
                    height=height,
                    corner_radius=0.12,
                    fill_color=color,
                    fill_opacity=0.7 - i * 0.1,
                    stroke_color=WHITE,
                    stroke_width=2
                )
                rect.shift(RIGHT * i * depth_offset + UP * i * depth_offset * 0.4)
                stack.add(rect)
            return stack



        # ==========================================
        # Create CNN layers positioned between image and ANN input
        # ==========================================
        
        # Calculate positions
        image_right = image_group.get_right()[0]
        ann_input_left = layers[0].get_left()[0]
        total_space = ann_input_left - image_right
        
        # Position layers evenly
        spacing = total_space / 6
        
        # --- CONV LAYER 1 ---
        conv1 = create_layer_stack(4, 2.5, 2.5, MAROON_B, 0.2)
        conv1.next_to(image, RIGHT, buff=1.8)
        conv1_label = Text("Conv1 + ReLU", font_size=40, weight=BOLD)
        conv1_label.next_to(conv1, DOWN, buff=0.5)


        # --- POOL LAYER 1 ---
        pool1 = create_layer_stack(4, 1.8, 1.8, TEAL_B, 0.18)
        pool1.next_to(conv1, RIGHT, buff=1.8)
        pool1_label = Text("Pool1", font_size=40,  weight=BOLD)
        pool1_label.next_to(pool1, DOWN, buff=0.5)
        
        # --- CONV LAYER 2 ---
        conv2 = create_layer_stack(5, 1.5, 1.5, MAROON_B, 0.16)
        conv2.next_to(pool1, RIGHT, buff=1.8)
        conv2_label = Text("Conv2 + ReLU", font_size=40,  weight=BOLD)
        conv2_label.next_to(conv2, DOWN, buff=0.5)
        
        # --- POOL LAYER 2 ---
        pool2 = create_layer_stack(5, 1.0, 1.0, TEAL_B, 0.14)
        pool2.next_to(conv2, RIGHT, buff=1.8)
        pool2_label = Text("Pool2", font_size=40 , weight=BOLD)
        pool2_label.next_to(pool2, DOWN, buff=0.5)


        # --- FEATURE EXTRACTOR (rectangle with circles inside) ---
        feature_box = RoundedRectangle(
            width=1.8,
            height=3.2,
            corner_radius=0.2,
            fill_color=PURPLE,
            fill_opacity=0.3,
            stroke_color=PURPLE_A,
            stroke_width=3
        )
        feature_box.next_to(pool2, RIGHT, buff=1.55)


        # Circles inside showing extracted features
        feature_dots = VGroup()
        for i in range(5):
            dot = Circle(
                radius=0.2,
                fill_color=PURPLE_C,
                fill_opacity=0.9,
                stroke_color=WHITE,
                stroke_width=2
            )
            dot.move_to(feature_box.get_center() + UP * (2 - i) * 0.55)
            feature_dots.add(dot)
        
        feature_label = Text("Features", font_size=40, color=PURPLE_A, weight=BOLD)
        feature_label.next_to(feature_box, DOWN, buff=0.5)
        
        self.camera.frame.save_state()

        self.play(self.camera.frame.animate.scale(0.4).shift(LEFT*6.88+UP*1.55))

        # ==========================================
        # ANIMATE THE PIPELINE (consistent style: arrow first, then layer)
        # ==========================================
        
        # Arrow: Image -> Conv1
        arrow_img_conv1 = Arrow(
            image_group.get_right(),
            conv1.get_left(),
            buff=0.15,
            color=WHITE,
            stroke_width=3
        ).set_color(WHITE)
        
        self.play(GrowArrow(arrow_img_conv1))
        self.wait(0.3)
        
        # Conv1 appears
        self.play(
            LaggedStartMap(FadeIn, conv1, lag_ratio=0.1),
            Write(conv1_label),
            run_time=1
        )
        self.wait(0.3)
        
        # Arrow: Conv1 -> Pool1
        arrow_conv1_pool1 = Arrow(
            conv1.get_right(),
            pool1.get_left(),
            buff=0.15,
            color=WHITE,
            stroke_width=3
        ).set_color(WHITE)
        
        self.play(GrowArrow(arrow_conv1_pool1), self.camera.frame.animate.shift(RIGHT*3))
        self.wait(0.3)
        
        # Pool1 appears
        self.play(
            LaggedStartMap(FadeIn, pool1, lag_ratio=0.1),
            Write(pool1_label),
            run_time=1
        )
        self.wait(0.3)
        
        # Arrow: Pool1 -> Conv2
        arrow_pool1_conv2 = Arrow(
            pool1.get_right(),
            conv2.get_left(),
            buff=0.15,
            color=WHITE,
            stroke_width=3
        ).set_color(WHITE)
        
        self.play(GrowArrow(arrow_pool1_conv2), self.camera.frame.animate.shift(RIGHT*4.7))
        self.wait(0.3)
        
        # Conv2 appears
        self.play(
            LaggedStartMap(FadeIn, conv2, lag_ratio=0.1),
            Write(conv2_label),
            run_time=1
        )
        self.wait(0.3)
        
        # Arrow: Conv2 -> Pool2
        arrow_conv2_pool2 = Arrow(
            conv2.get_right(),
            pool2.get_left(),
            buff=0.15,
            color=WHITE,
            stroke_width=3
        ).set_color(WHITE)
        
        self.play(GrowArrow(arrow_conv2_pool2), self.camera.frame.animate.shift(RIGHT*4.5))
        self.wait(0.3)
        
        # Pool2 appears
        self.play(
            LaggedStartMap(FadeIn, pool2, lag_ratio=0.1),
            Write(pool2_label),
            run_time=1
        )
        self.wait(0.3)
        
        # Arrow: Pool2 -> Features (Flatten)
        arrow_pool2_feat = Arrow(
            pool2.get_right(),
            feature_box.get_left(),
            buff=0.15,
            color=WHITE,
            stroke_width=3
        ).set_color(WHITE)
        flatten_label = Text("Flatten", font_size=18, color=YELLOW, weight=BOLD)
        flatten_label.next_to(arrow_pool2_feat, UP, buff=0.23)
        
        self.play(GrowArrow(arrow_pool2_feat), Write(flatten_label), self.camera.frame.animate.shift(RIGHT*3))
        self.wait(0.3)
        
        # Feature box appears
        self.play(
            ShowCreation(feature_box),
            Write(feature_label),
            run_time=1
        )
        
        # Feature dots appear inside
        self.play(
            LaggedStartMap(GrowFromCenter, feature_dots, lag_ratio=0.1),
            run_time=1
        )
        self.wait(0.3)
        
        # Arrow: Features -> ANN input layer
        arrow_feat_ann = Arrow(
            feature_box.get_right(),
            layers[0].get_left(),
            buff=0.15,
            color=WHITE,
            stroke_width=3
        ).set_color(WHITE)
        
        self.play(GrowArrow(arrow_feat_ann), self.camera.frame.animate.shift(RIGHT*3))
        self.wait(0.5)
        
        # Highlight the connection - features flow into ANN
        self.play(
            *[TransformFromCopy(fd, neuron) 
              for fd, neuron in zip(feature_dots, layers[0])],
            run_time=1.5
        )
        self.wait(2)


        self.play(self.camera.frame.animate.restore().shift(RIGHT*2+DOWN*0.39))
        

        pipeline_text = VGroup(
            Text("Input", font_size=22, color=WHITE),
            Tex(r"\rightarrow", font_size=26),
            Text("Conv", font_size=22, ),
            Tex(r"\rightarrow", font_size=26),
            Text("Pool", font_size=22,),
            Tex(r"\rightarrow", font_size=26),
            Text("Conv", font_size=22, ),
            Tex(r"\rightarrow", font_size=26),
            Text("Pool", font_size=22, ),
            Tex(r"\rightarrow", font_size=26),
            Text("Features", font_size=22, color=PURPLE_A),
            Tex(r"\rightarrow", font_size=26),
            Text("ANN", font_size=22, color=BLUE),
            Tex(r"\rightarrow", font_size=26),
            Text("Output", font_size=22, color=OUTPUT_COLOR),
        )
        pipeline_text.arrange(RIGHT, buff=0.12)
        pipeline_text.scale(2.7).to_edge(DOWN, buff=0.6).shift(RIGHT * 2)
        pipeline_text.next_to(pool1, DOWN, buff=3).shift(DOWN*1.7+RIGHT*3)

        self.play(
            LaggedStartMap(FadeIn, pipeline_text, lag_ratio=0.06),
            run_time=2
        )
        self.wait()

        c = Tex(r"\checkmark").set_color("#00ff00").scale(6.5)
        c.next_to(pipeline_text, DOWN, buff=0.9)

        self.play(GrowFromCenter(c))

        
        self.wait(2)



class Pooling(Scene):
    
    def construct(self):
        self.camera.frame.scale(1.0).shift(UP * 0.3)
        
        # ==========================================
        # Title
        # ==========================================
        
        title = Text("Pooling Layers", font_size=48, weight=BOLD)
        title.set_color(BLUE)
        title.to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=1)
        self.wait(1)
        self.play(FadeOut(title), run_time=0.5)
        
        # ==========================================
        # PART 1: MAX POOLING
        # ==========================================
        
        max_title = Text("Max Pooling", font_size=42, weight=BOLD)
        max_title.set_color(RED)
        max_title.to_edge(UP, buff=0.4)
        
        self.play(Write(max_title), run_time=0.8)
        
        # Create input grid (4x4)
        input_values = np.array([
            [1, 3, 2, 1],
            [4, 6, 5, 2],
            [7, 8, 1, 0],
            [2, 3, 4, 5]
        ])
        
        cell_size = 0.8
        
        input_grid = VGroup()
        input_cells = {}
        input_texts = {}
        
        for i in range(4):
            for j in range(4):
                cell = Square(side_length=cell_size)
                cell.set_fill(WHITE, opacity=1)
                cell.set_stroke(BLACK, width=2)
                cell.move_to(RIGHT * j * cell_size + DOWN * i * cell_size)
                
                value = Text(str(input_values[i, j]), font_size=24, weight=BOLD)
                value.set_color(BLACK)
                value.move_to(cell.get_center())
                
                cell_group = VGroup(cell, value)
                input_cells[(i, j)] = cell_group
                input_texts[(i, j)] = value
                input_grid.add(cell_group)
        
        input_grid.center()
        input_grid.move_to(LEFT * 3.5)
        
        input_label = Text("Input (4×4)", font_size=28, weight=BOLD)
        input_label.next_to(input_grid, UP, buff=0.4)
        
        # Pool size and stride info
        pool_info = Text("Pool Size: 2×2, Stride: 2", font_size=29)
        pool_info.set_color(YELLOW)
        pool_info.next_to(input_grid, DOWN, buff=0.4)
        
        # Create output grid (2x2)
        output_grid = VGroup()
        output_cells = {}
        output_texts = {}
        
        for i in range(2):
            for j in range(2):
                cell = Square(side_length=cell_size)
                cell.set_fill(WHITE, opacity=1)
                cell.set_stroke(BLACK, width=2)
                cell.move_to(RIGHT * j * cell_size + DOWN * i * cell_size)
                
                value = Text("?", font_size=24, weight=BOLD)
                value.set_color(BLACK)
                value.move_to(cell.get_center())
                
                output_grid.add(cell)
                output_cells[(i, j)] = cell
                output_texts[(i, j)] = value
        
        output_grid.center()
        output_grid.move_to(RIGHT * 3.5)
        
        for i in range(2):
            for j in range(2):
                output_texts[(i, j)].move_to(output_cells[(i, j)].get_center())
        
        output_label = Text("Output (2×2)", font_size=28, weight=BOLD)
        output_label.next_to(output_grid, UP, buff=0.4)
        
        # Arrow
        arrow = Arrow(input_grid.get_right(), output_grid.get_left(), buff=0.5)
        arrow_label = Text("Max", font_size=39, weight=BOLD)
        arrow_label.set_color(RED)
        arrow_label.next_to(arrow, UP, buff=0.1)
        
        # Show elements
        self.play(
            LaggedStartMap(FadeIn, input_grid, lag_ratio=0.03),
            Write(input_label),
            run_time=1
        )
        
        self.play(Write(pool_info), run_time=0.5)
        
        self.play(GrowArrow(arrow), Write(arrow_label), run_time=0.5)
        
        question_marks = VGroup(*[output_texts[(i, j)] for i in range(2) for j in range(2)])
        self.play(
            LaggedStartMap(FadeIn, output_grid, lag_ratio=0.05),
            LaggedStartMap(FadeIn, question_marks, lag_ratio=0.05),
            Write(output_label),
            run_time=0.8
        )
        
        self.wait(1)
        
        # Create pooling window (2x2 highlight)
        pool_window = VGroup()
        for i in range(2):
            for j in range(2):
                cell = Square(side_length=cell_size)
                cell.set_fill(RED, opacity=0.3)
                cell.set_stroke(RED, width=4)
                cell.move_to(RIGHT * j * cell_size + DOWN * i * cell_size)
                pool_window.add(cell)
        pool_window.move_to(input_cells[(0, 0)][0].get_center() + RIGHT * cell_size/2 + DOWN * cell_size/2)
        pool_window.set_z_index(3)
        
        self.play(FadeIn(pool_window), run_time=0.5)
        
        # Perform max pooling
        pool_positions = [(0, 0), (0, 2), (2, 0), (2, 2)]  # Top-left of each 2x2 region
        output_positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
        
        for idx, (pi, pj) in enumerate(pool_positions):
            # Move window
            target_pos = input_cells[(pi, pj)][0].get_center() + RIGHT * cell_size/2 + DOWN * cell_size/2
            
            if idx > 0:
                self.play(pool_window.animate.move_to(target_pos), run_time=0.5)
            
            # Get max value from 2x2 region
            region_values = [input_values[pi + di, pj + dj] for di in range(2) for dj in range(2)]
            max_val = max(region_values)
            
            # Highlight the max value cell
            max_idx = region_values.index(max_val)
            max_di, max_dj = max_idx // 2, max_idx % 2
            max_cell = input_cells[(pi + max_di, pj + max_dj)][0]
            
            self.play(max_cell.animate.set_fill(RED, opacity=0.5), run_time=0.3)
            
            # Create result
            oi, oj = output_positions[idx]
            result_val = Text(str(max_val), font_size=24, weight=BOLD)
            result_val.set_color(BLACK)
            result_val.move_to(output_cells[(oi, oj)].get_center())
            
            old_q = output_texts[(oi, oj)]
            
            self.play(
                TransformFromCopy(input_texts[(pi + max_di, pj + max_dj)], result_val),
                FadeOut(old_q),
                run_time=0.5
            )
            
            # Reset highlight
            self.play(max_cell.animate.set_fill(WHITE, opacity=1), run_time=0.2)
            
            output_grid.add(result_val)
        
        self.play(FadeOut(pool_window), run_time=0.3)
        
        self.wait(1)
        
        # ==========================================
        # PART 2: AVERAGE POOLING
        # ==========================================
        
        # Fade out max pooling
        self.play(
            FadeOut(input_grid), FadeOut(input_label),
            FadeOut(output_grid), FadeOut(output_label),
            FadeOut(arrow), FadeOut(arrow_label),
            FadeOut(pool_info), FadeOut(max_title),
            run_time=0.8
        )
        
        avg_title = Text("Average Pooling", font_size=42, weight=BOLD)
        avg_title.set_color(GREEN)
        avg_title.to_edge(UP, buff=0.4)
        
        self.play(Write(avg_title), run_time=0.8)
        
        # Create new input grid (4x4)
        avg_input_values = np.array([
            [2, 4, 6, 8],
            [1, 3, 5, 7],
            [8, 6, 4, 2],
            [7, 5, 3, 1]
        ])
        
        avg_input_grid = VGroup()
        avg_input_cells = {}
        avg_input_texts = {}
        
        for i in range(4):
            for j in range(4):
                cell = Square(side_length=cell_size)
                cell.set_fill(WHITE, opacity=1)
                cell.set_stroke(BLACK, width=2)
                cell.move_to(RIGHT * j * cell_size + DOWN * i * cell_size)
                
                value = Text(str(avg_input_values[i, j]), font_size=24, weight=BOLD)
                value.set_color(BLACK)
                value.move_to(cell.get_center())
                
                cell_group = VGroup(cell, value)
                avg_input_cells[(i, j)] = cell_group
                avg_input_texts[(i, j)] = value
                avg_input_grid.add(cell_group)
        
        avg_input_grid.center()
        avg_input_grid.move_to(LEFT * 3.5)
        
        avg_input_label = Text("Input (4×4)", font_size=28, weight=BOLD)
        avg_input_label.next_to(avg_input_grid, UP, buff=0.3)
        
        avg_pool_info = Text("Pool Size: 2×2, Stride: 2", font_size=29)
        avg_pool_info.set_color(YELLOW)
        avg_pool_info.next_to(avg_input_grid, DOWN, buff=0.4)
        
        # Create output grid (2x2)
        avg_output_grid = VGroup()
        avg_output_cells = {}
        avg_output_texts = {}
        
        for i in range(2):
            for j in range(2):
                cell = Square(side_length=cell_size)
                cell.set_fill(WHITE, opacity=1)
                cell.set_stroke(BLACK, width=2)
                cell.move_to(RIGHT * j * cell_size + DOWN * i * cell_size)
                
                value = Text("?", font_size=24, weight=BOLD)
                value.set_color(BLACK)
                value.move_to(cell.get_center())
                
                avg_output_grid.add(cell)
                avg_output_cells[(i, j)] = cell
                avg_output_texts[(i, j)] = value
        
        avg_output_grid.center()
        avg_output_grid.move_to(RIGHT * 3.5)
        
        for i in range(2):
            for j in range(2):
                avg_output_texts[(i, j)].move_to(avg_output_cells[(i, j)].get_center())
        
        avg_output_label = Text("Output (2×2)", font_size=28, weight=BOLD)
        avg_output_label.next_to(avg_output_grid, UP, buff=0.3)
        
        # Arrow
        avg_arrow = Arrow(avg_input_grid.get_right(), avg_output_grid.get_left(), buff=0.5)
        avg_arrow_label = Text("Avg", font_size=39, weight=BOLD)
        avg_arrow_label.set_color(GREEN)
        avg_arrow_label.next_to(avg_arrow, UP, buff=0.1)
        
        # Show elements
        self.play(
            LaggedStartMap(FadeIn, avg_input_grid, lag_ratio=0.03),
            Write(avg_input_label),
            run_time=1
        )
        
        self.play(Write(avg_pool_info), run_time=0.5)
        
        self.play(GrowArrow(avg_arrow), Write(avg_arrow_label), run_time=0.5)
        
        avg_question_marks = VGroup(*[avg_output_texts[(i, j)] for i in range(2) for j in range(2)])
        self.play(
            LaggedStartMap(FadeIn, avg_output_grid, lag_ratio=0.05),
            LaggedStartMap(FadeIn, avg_question_marks, lag_ratio=0.05),
            Write(avg_output_label),
            run_time=0.8
        )
        
        self.wait(1)
        
        # Create pooling window (2x2 highlight) - GREEN for average
        avg_pool_window = VGroup()
        for i in range(2):
            for j in range(2):
                cell = Square(side_length=cell_size)
                cell.set_fill(GREEN, opacity=0.3)
                cell.set_stroke(GREEN, width=4)
                cell.move_to(RIGHT * j * cell_size + DOWN * i * cell_size)
                avg_pool_window.add(cell)
        avg_pool_window.move_to(avg_input_cells[(0, 0)][0].get_center() + RIGHT * cell_size/2 + DOWN * cell_size/2)
        avg_pool_window.set_z_index(3)
        
        self.play(FadeIn(avg_pool_window), run_time=0.5)
        
        # Perform average pooling
        for idx, (pi, pj) in enumerate(pool_positions):
            # Move window
            target_pos = avg_input_cells[(pi, pj)][0].get_center() + RIGHT * cell_size/2 + DOWN * cell_size/2
            
            if idx > 0:
                self.play(avg_pool_window.animate.move_to(target_pos), run_time=0.5)
            
            # Get average value from 2x2 region
            region_values = [avg_input_values[pi + di, pj + dj] for di in range(2) for dj in range(2)]
            avg_val = sum(region_values) / 4
            
            # Highlight all cells in region
            highlight_anims = []
            for di in range(2):
                for dj in range(2):
                    highlight_anims.append(
                        avg_input_cells[(pi + di, pj + dj)][0].animate.set_fill(GREEN, opacity=0.5)
                    )
            self.play(*highlight_anims, run_time=0.3)
            
            # Create result
            oi, oj = output_positions[idx]
            # Format as integer if whole number, else one decimal
            if avg_val == int(avg_val):
                result_str = str(int(avg_val))
            else:
                result_str = f"{avg_val:.1f}"
            
            result_val = Text(result_str, font_size=22, weight=BOLD)
            result_val.set_color(BLACK)
            result_val.move_to(avg_output_cells[(oi, oj)].get_center())
            
            old_q = avg_output_texts[(oi, oj)]
            
            self.play(
                TransformFromCopy(avg_pool_window, result_val),
                FadeOut(old_q),
                run_time=0.5
            )
            
            # Reset highlight
            reset_anims = []
            for di in range(2):
                for dj in range(2):
                    reset_anims.append(
                        avg_input_cells[(pi + di, pj + dj)][0].animate.set_fill(WHITE, opacity=1)
                    )
            self.play(*reset_anims, run_time=0.2)
            
            avg_output_grid.add(result_val)
        
        self.play(FadeOut(avg_pool_window), run_time=0.3)
        
        self.wait(1)
        
        # ==========================================
        # PART 3: FORMULA (simplified)
        # ==========================================
        
        # Fade out average pooling
        self.play(
            FadeOut(avg_input_grid), FadeOut(avg_input_label),
            FadeOut(avg_output_grid), FadeOut(avg_output_label),
            FadeOut(avg_arrow), FadeOut(avg_arrow_label),
            FadeOut(avg_pool_info), FadeOut(avg_title),
            run_time=0.8
        )
        
        formula_title = Text("Output Size Formula", font_size=62, weight=BOLD)
        formula_title.set_color(BLUE)
        formula_title.to_edge(UP, buff=0.5).shift(DOWN*0.18)
        
        self.play(Write(formula_title), run_time=0.8)
        
        self.wait(0.5)

  
        # Full formula with padding
        formula_full = Tex(
            r"Output\ = \left \lfloor \frac{n + 2P - f}{S} \right\rfloor + 1",
            font_size=56
        )
        formula_full.move_to(ORIGIN).scale(1.4)
        
        self.play(Write(formula_full), run_time=1.5)
        
        self.wait(1.5)
        
        # Note about padding being rare
        padding_note = Text("Padding is rarely used in pooling...", font_size=33)
        padding_note.set_color(YELLOW)
        padding_note.next_to(formula_full, DOWN, buff=1.04)
        
        self.play(Write(padding_note), run_time=1)
        
        self.wait(2)
        
        # Simplified formula without padding (P=0)
        formula_simple = Tex(
            r"Output = \left\lfloor \frac{n - f}{S} \right\rfloor + 1",
            font_size=56
        )
        formula_simple.move_to(ORIGIN).scale(1.55)
        
        self.play(
            FadeOut(padding_note),
            run_time=0.5
        )
        
        self.play(
            Transform(formula_full, formula_simple),
            self.camera.frame.animate.shift(UP*0.55),
            run_time=1.2
        )
        
        # Highlight the simplified formula
        box = SurroundingRectangle(formula_full, color=YELLOW, stroke_width=6, ).scale(1.1)
        self.play(ShowCreation(box), run_time=0.5)
        
        self.wait(3)


class KernelShowcase(Scene):
    
    def construct(self):
        self.camera.frame.scale(0.85).shift(UP*0.76)
        
        # ==========================================
        # Define all kernels
        # ==========================================
        
        # Mean blur (box blur) 3x3
        mean_kernel = np.ones((3, 3)) / 9
        
        # Gaussian blur 3x3
        gaussian_kernel = np.array([
            [1, 2, 1],
            [2, 4, 2],
            [1, 2, 1]
        ], dtype=np.float64) / 16
        
        # Sharpen kernel
        sharpen_kernel = np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ], dtype=np.float64)
        
        
        # Sobel X (vertical edge)
        sobel_x_kernel = np.array([
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]
        ], dtype=np.float64)
        
        # ==========================================
        # Helper to create kernel grid
        # ==========================================
        
        def create_kernel_grid(kernel, color, k_cell_size=1.1, use_fractions=False):
            """Create a VGroup representing the kernel"""
            kernel_grid = VGroup()
            
            for i in range(3):
                for j in range(3):
                    cell = Square(side_length=k_cell_size)
                    cell.set_fill(color, opacity=0.75)
                    cell.set_stroke(WHITE, width=3)
                    cell.move_to(
                        RIGHT * (j - 1) * k_cell_size + 
                        DOWN * (i - 1) * k_cell_size
                    )
                    
                    val = kernel[i, j]
                    
                    if use_fractions:
                        val_str = "1/9"
                    elif abs(val - round(val)) < 0.001:
                        val_str = str(int(round(val)))
                    else:
                        val_str = f"{val:.2f}"
                    
                    val_text = Text(val_str, font_size=28, weight=BOLD)
                    val_text.set_color(WHITE)
                    val_text.move_to(cell.get_center())
                    
                    kernel_grid.add(VGroup(cell, val_text))
            
            return kernel_grid
        
        def create_learnable_kernel(color, k_cell_size=1):
            """Create kernel with f1, f2, ... f9 labels"""
            kernel_grid = VGroup()
            
            labels = ["f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7", "f_8", "f_9"]
            idx = 0
            
            for i in range(3):
                for j in range(3):
                    cell = Square(side_length=k_cell_size)
                    cell.set_fill(color, opacity=1)
                    cell.set_stroke(BLUE_E, width=3)
                    cell.move_to(
                        RIGHT * (j - 1) * k_cell_size + 
                        DOWN * (i - 1) * k_cell_size
                    )
                    
                    val_text = Tex(labels[idx], font_size=56).set_color(BLACK)
                    val_text.move_to(cell.get_center())
                    
                    kernel_grid.add(VGroup(cell, val_text))
                    idx += 1
            
            return kernel_grid
        
        # ==========================================
        # Define filter info
        # ==========================================
        
        filters_info = [
            {
                "name": "Mean Blur",
                "kernel": mean_kernel,
                "color": BLUE,
                "use_fractions": True,
            },
            {
                "name": "Gaussian Blur",
                "kernel": gaussian_kernel,
                "color": TEAL,
                "use_fractions": False,
            },
            {
                "name": "Sharpen",
                "kernel": sharpen_kernel,
                "color": ORANGE,
                "use_fractions": False,
            },

            {
                "name": "Sobel X",
                "kernel": sobel_x_kernel,
                "color": RED,
                "use_fractions": False,
            },
        ]
        
        # ==========================================
        # Show first kernel
        # ==========================================
        
        first_filter = filters_info[0]
        
        # Title
        title = Text(first_filter["name"], font_size=48, weight=BOLD)
        title.set_color(first_filter["color"])
        title.shift(UP * 2.7)
        
        # Kernel grid
        kernel_grid = create_kernel_grid(
            first_filter["kernel"], 
            first_filter["color"], 
            use_fractions=first_filter["use_fractions"]
        )
        
        self.play(Write(title), run_time=0.7)
        self.play(
            LaggedStartMap(FadeIn, kernel_grid, lag_ratio=0.05),
            run_time=0.8
        )
        
        self.wait(1)
        
        # ==========================================
        # Transform through all kernels
        # ==========================================
        
        for idx in range(1, len(filters_info)):
            filt = filters_info[idx]
            
            # New title
            new_title = Text(filt["name"], font_size=48, weight=BOLD)
            new_title.set_color(filt["color"])
            new_title.shift(UP * 2.7)
            
            # New kernel
            new_kernel_grid = create_kernel_grid(
                filt["kernel"], 
                filt["color"], 
                use_fractions=filt["use_fractions"]
            )
            
            # Transform
            self.play(
                Transform(title, new_title),
                Transform(kernel_grid, new_kernel_grid),
                run_time=0.8
            )
            
            self.wait(1)
        
        self.wait(0.5)
        
        # ==========================================
        # Transform to learnable parameters
        # ==========================================
        
        # New title for learnable
        learnable_title = Text("Learnable Filter", font_size=48, weight=BOLD)
        learnable_title.set_color(YELLOW)
        learnable_title.shift(UP * 2.7)
        
        # Learnable kernel
        learnable_kernel = create_learnable_kernel(YELLOW)
        
        self.play(
            Transform(title, learnable_title),
            Transform(kernel_grid, learnable_kernel),
            run_time=1
        )
        
        self.wait(1.5)


        # ==========================================
        # Add explanation text
        # ==========================================
        
        explanation = Text(
            "These values are learned during backpropagation",
            font_size=28
        )
        explanation.set_color(GREY_A)
        explanation.shift(DOWN * 2.3)
        

        
        self.play(Write(explanation), self.camera.frame.animate.shift(DOWN*0.66),run_time=0.8)
        self.wait(0.5)
        
        self.wait(2)
        

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


class ConvLayer(Scene):
    
    def construct(self):
        self.camera.frame.scale(1.15)

        self.camera.frame.scale(0.9*0.9*0.95).shift(LEFT*1.32)
        
        cell_size = 0.35
        depth_offset = 0.18
        
        # ==========================================
        # Helper functions
        # ==========================================
        
        def create_rgb_input():
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
            
            red_layer.set_z_index(3)
            green_layer.set_z_index(2)
            blue_layer.set_z_index(1)
            
            return VGroup(red_layer, green_layer, blue_layer)
        
        def create_3d_filter(color, stroke_color):
            filter_layers = VGroup()
            for layer_idx in range(3):
                layer = VGroup()
                for i in range(3):
                    for j in range(3):
                        cell = Square(side_length=cell_size)
                        cell.set_fill(color, opacity=0.85)
                        cell.set_stroke(stroke_color, width=2)
                        x_pos = (j - 1) * cell_size + (2 - layer_idx) * depth_offset
                        y_pos = -(i - 1) * cell_size + (2 - layer_idx) * depth_offset
                        cell.move_to(RIGHT * x_pos + UP * y_pos)
                        layer.add(cell)
                layer.set_z_index(3.5 - layer_idx)
                filter_layers.add(layer)
            return filter_layers
        
        def create_output_grid(color, stroke_color, opacity=0.7):
            grid = VGroup()
            for i in range(4):
                for j in range(4):
                    cell = Square(side_length=cell_size)
                    cell.set_fill(color, opacity=opacity)
                    cell.set_stroke(stroke_color, width=2)
                    cell.move_to(RIGHT * j * cell_size + DOWN * i * cell_size)
                    grid.add(cell)
            grid.center()
            return grid
        
        def create_stacked_output(colors, stroke_colors, center_pos):
            layers = VGroup()
            for layer_idx, (color, stroke) in enumerate(zip(colors, stroke_colors)):
                layer = VGroup()
                for i in range(4):
                    for j in range(4):
                        cell = Square(side_length=cell_size)
                        cell.set_fill(color, opacity=1)
                        cell.set_stroke(stroke, width=2)
                        x_pos = j * cell_size + (2 - layer_idx) * depth_offset
                        y_pos = -i * cell_size + (2 - layer_idx) * depth_offset
                        cell.move_to(center_pos + RIGHT * x_pos + UP * y_pos)
                        layer.add(cell)
                layer.set_z_index(3 - layer_idx)
                layers.add(layer)
            return layers
        
        # ==========================================
        # PART 1: Show input volume
        # ==========================================
        
        input_volume = create_rgb_input()
        input_volume.center()
        input_volume.move_to(LEFT * 5)
        
        input_label = Text("Input", font_size=26, weight=BOLD)
        input_label.next_to(input_volume, UP, buff=0.5)
        
        self.play(
            LaggedStartMap(FadeIn, input_volume[2], lag_ratio=0.01),
            LaggedStartMap(FadeIn, input_volume[1], lag_ratio=0.01),
            LaggedStartMap(FadeIn, input_volume[0], lag_ratio=0.01),
            Write(input_label),
            run_time=1.5
        )
        
        self.wait(0.5)

        
        # ==========================================
        # PART 2: Show three filters stacked vertically
        # ==========================================
        
        filter1 = create_3d_filter(YELLOW, "#cccc00")
        filter2 = create_3d_filter(ORANGE, "#cc6600")
        filter3 = create_3d_filter(PURPLE, "#8800aa")
        
        filter1.move_to(LEFT * 1.5 + UP * 2.2)
        filter2.move_to(LEFT * 1.5)
        filter3.move_to(LEFT * 1.5 + DOWN * 2.2)
        
        f1_label = Tex(r"F_1", font_size=42).set_color(YELLOW).next_to(filter1, LEFT, buff=0.3)
        f2_label = Tex(r"F_2", font_size=42).set_color(ORANGE).next_to(filter2, LEFT, buff=0.3)
        f3_label = Tex(r"F_3", font_size=42).set_color(PURPLE).next_to(filter3, LEFT, buff=0.3)
        
        asterisk = Tex(r"*", font_size=48).move_to(LEFT * 3.2)
        
        self.play(Write(asterisk), run_time=0.3)
        
        self.play(
            LaggedStartMap(FadeIn, filter1, lag_ratio=0.02),
            LaggedStartMap(FadeIn, filter2, lag_ratio=0.02),
            LaggedStartMap(FadeIn, filter3, lag_ratio=0.02),
            Write(f1_label), Write(f2_label), Write(f3_label),
            run_time=1.2
        )
        
        self.wait(0.5)
        
        # ==========================================
        # PART 3: Show ReLU( [output] + b ) for each filter
        # ==========================================
        
        # Create output grids
        out1 = create_output_grid(YELLOW, "#cccc00", opacity=0.6)
        out2 = create_output_grid(ORANGE, "#cc6600", opacity=0.6)
        out3 = create_output_grid(PURPLE, "#8800aa", opacity=0.6)
        
        out1.move_to(RIGHT * 2 + UP * 2.2)
        out2.move_to(RIGHT * 2)
        out3.move_to(RIGHT * 2 + DOWN * 2.2)
        
        # Create ReLU( [ ] + b ) formula structure for each
        # ReLU( out + b1 )
        
        relu1 = Text("ReLU(", font_size=24, weight=BOLD).set_color("#00ff00")
        plus1 = Tex(r"+", font_size=32)
        b1 = Tex(r"b_1", font_size=32).set_color(YELLOW)
        close1 = Text(")", font_size=24, weight=BOLD).set_color("#00ff00")
        
        relu2 = Text("ReLU(", font_size=24, weight=BOLD).set_color("#00ff00")
        plus2 = Tex(r"+", font_size=32)
        b2 = Tex(r"b_2", font_size=32).set_color(ORANGE)
        close2 = Text(")", font_size=24, weight=BOLD).set_color("#00ff00")
        
        relu3 = Text("ReLU(", font_size=24, weight=BOLD).set_color("#00ff00")
        plus3 = Tex(r"+", font_size=32)
        b3 = Tex(r"b_3", font_size=32).set_color(PURPLE)
        close3 = Text(")", font_size=24, weight=BOLD).set_color("#00ff00")
        
        # Position formula parts around output grids
        relu1.next_to(out1, LEFT, buff=0.15)
        plus1.next_to(out1, RIGHT, buff=0.15)
        b1.next_to(plus1, RIGHT, buff=0.1)
        close1.next_to(b1, RIGHT, buff=0.1)
        
        relu2.next_to(out2, LEFT, buff=0.15)
        plus2.next_to(out2, RIGHT, buff=0.15)
        b2.next_to(plus2, RIGHT, buff=0.1)
        close2.next_to(b2, RIGHT, buff=0.1)
        
        relu3.next_to(out3, LEFT, buff=0.15)
        plus3.next_to(out3, RIGHT, buff=0.15)
        b3.next_to(plus3, RIGHT, buff=0.1)
        close3.next_to(b3, RIGHT, buff=0.1)
        
        formula1 = VGroup(relu1, out1, plus1, b1, close1)
        formula2 = VGroup(relu2, out2, plus2, b2, close2)
        formula3 = VGroup(relu3, out3, plus3, b3, close3)
        
        # Arrows from filters to formulas
        arrow1 = Arrow(filter1.get_right(), relu1.get_left(), buff=0.2, stroke_width=3)
        arrow2 = Arrow(filter2.get_right(), relu2.get_left(), buff=0.2, stroke_width=3)
        arrow3 = Arrow(filter3.get_right(), relu3.get_left(), buff=0.2, stroke_width=3)
        
        self.play(
            GrowArrow(arrow1), GrowArrow(arrow2), GrowArrow(arrow3),
            run_time=0.5
        )

        self.wait(2)

        self.play(
           FadeIn(out1),
           FadeIn(out2),
           FadeIn(out3),
        )

        self.wait(2)

        self.play(
           FadeIn(plus1),
           FadeIn(plus2),
           FadeIn(plus3),
        )


        self.play(
           FadeIn(b1),
           FadeIn(b2),
           FadeIn(b3),
        )

        self.wait(2)
   
        # Show formulas
        self.play(
            Write(relu1), Write(close1),
            Write(relu2), Write(close2),
            Write(relu3), Write(close3),
            run_time=1.5
        )
        
        self.wait(1)

        
        # ==========================================
        # PART 4: Transform entire formula into dark output
        # ==========================================
        
        # Create darker output grids (after ReLU)
        out1_dark = create_output_grid("#fbff24", YELLOW_D, opacity=1).set_z_index(2)
        out2_dark = create_output_grid("#ff8000", "#884400", opacity=1)
        out3_dark = create_output_grid("#9c08ff", PURPLE_D, opacity=1).set_z_index(1)
        
        out1_dark.move_to(RIGHT * 5.2 + UP * 2.2)
        out2_dark.move_to(RIGHT * 5.2)
        out3_dark.move_to(RIGHT * 5.2 + DOWN * 2.2)
        
        # Equals signs
        eq1 = Tex(r"=", font_size=36).next_to(close1, RIGHT, buff=0.32)
        eq2 = Tex(r"=", font_size=36).next_to(close2, RIGHT, buff=0.32)
        eq3 = Tex(r"=", font_size=36).next_to(close3, RIGHT, buff=0.32)
        
        self.play(
            Write(eq1), Write(eq2), Write(eq3),
            run_time=0.3
        )
        self.camera.frame.save_state()
        # Transform formula groups into dark outputs
        self.play(
            TransformFromCopy(formula1, out1_dark),
            TransformFromCopy(formula2, out2_dark),
            TransformFromCopy(formula3, out3_dark),
            self.camera.frame.animate.shift(RIGHT*1.166).scale(1.114),
            run_time=1.5
        )
        
        self.wait(1.5)


        self.play(
            out3_dark.animate.move_to(out2_dark).shift(UP*0.12+RIGHT*0.12),
            FadeOut(eq1),
        )
        self.play(
            out1_dark.animate.move_to(out3_dark).shift(UP*0.12+RIGHT*0.12),
            FadeOut(eq3),

        )

        self.wait(1.4)


        rect1= SurroundingRectangle(Group(input_volume, input_label), stroke_width=5.8).scale(1.06)


        self.wait(0.3)

        a = Text("X").set_color(WHITE).scale(1.5).next_to(rect1, DOWN, buff=0.63)
        self.play(Write(a))
        self.wait(2)
        
        self.camera.frame.save_state()

        self.play(self.camera.frame.animate.scale(1.08).shift(DOWN*0.7))

        self.wait()

        b = Text("W").set_color(WHITE).scale(1.5).next_to(filter3, DOWN, buff=0.63)
        self.play(Write(b))
        self.wait(2)  

        c = Text("RelU(WX + b)").set_color(WHITE).scale(0.87).next_to(b, RIGHT, buff=1.3)

        self.play(
            ReplacementTransform(a, c[5]),
            ReplacementTransform(b, c[6]),
        )

        self.wait(1)

        self.play(FadeIn(c[7]))

        self.play(TransformFromCopy(VGroup(b1,b2,b3), c[8]))
        
        self.wait(2)

        self.play(FadeIn(c[:5]), FadeIn(c[-1]))
        self.wait(2)

        b = Tex("a^{(l)}").set_color(WHITE).scale(1.5).next_to(out2_dark, DOWN, buff=0.63)

        self.play(ReplacementTransform(c,b))

        self.wait(2)

        self.play(FadeOut(b), self.camera.frame.animate.restore())
        self.wait(2)

        a = Text("6x6x3").next_to(input_volume, DOWN, buff=0.43).set_color(WHITE)
        self.play(ShowCreation(a))
        self.wait(2)

        self.play(self.camera.frame.animate.shift(DOWN*0.5))

        b = Text("3x3x3").next_to(filter3, DOWN, buff=0.43).set_color(WHITE).scale(0.8)
        self.play(ShowCreation(b))
        self.wait(2)    

        c = Text("4x4x1").next_to(out3, DOWN, buff=0.43).set_color(WHITE).scale(0.8)
        self.play(ShowCreation(c))
        self.wait(2)    

        d = Text("4x4x3").next_to(out3_dark, DOWN, buff=0.43).set_color(WHITE).scale(0.8)
        self.play(ShowCreation(d))
        self.wait(2)     



        # Transform dimension labels to notation
        a_new = Tex(r"n_H^{(l-1)} \times n_W^{(l-1)} \times n_c^{(l-1)}").scale(0.78).move_to(a).set_color(WHITE)
        b_new = Tex(r"f^{(l)} \times f^{(l)} \times n_c^{(l-1)}").scale(0.96).move_to(b).set_color(WHITE).shift(DOWN*0.04)
        c_new = Tex(r"n_H^{(l)} \times n_W^{(l)} \times 1").scale(0.96).move_to(c).set_color(WHITE).shift(DOWN*0.04)
        d_new = Tex(r"n_H^{(l)} \times n_W^{(l)} \times n_c^{(l)}").scale(0.77).move_to(d).set_color(WHITE).shift(LEFT*0.07)

        self.play(
            Transform(a, a_new),
            Transform(b, b_new),
            Transform(c, c_new),
            Transform(d, d_new),
            run_time=1.5
        )
        
        self.wait()

        YELLOW_B = YELLOW_C

        rect = SurroundingRectangle(a, color=YELLOW_B, stroke_width=3.8).scale(1.06)
        self.play(ShowCreation(rect))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(b, color=YELLOW_B, stroke_width=3.8).scale(1.06)))
        self.wait(2)
        self.play(Transform(rect, SurroundingRectangle(c, color=YELLOW_B, stroke_width=3.8).scale(1.06)))
        self.wait(2)
        self.play(Transform(rect, SurroundingRectangle(d, color=YELLOW_B, stroke_width=3.8).scale(1.06)))
        self.wait(2)
