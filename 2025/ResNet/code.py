from manimlib import *
import numpy as np


class Introduction(Scene):
    """
    Introduction to Residual Networks: Why do we need them?
    
    This class explains the PROBLEMS that ResNets solve:
    1. What does each layer in a deep network learn?
    2. The degradation problem - deeper networks perform WORSE
    3. Vanishing gradients - why early layers can't learn
    4. Why identity mapping is hard for neural networks
    5. The key insight that makes ResNets work
    
    NO residual blocks or network architecture shown - just the concepts.
    """
    
    def construct(self):

        self.camera.frame.scale(1.15)
        # ==========================================
        # COLOR PALETTE - Premium aesthetic
        # ==========================================
        LAYER_COLOR = "#9B59B6"      # Purple for layers
        ARROW_COLOR = WHITE
        SUCCESS_COLOR = "#2ECC71"    # Green for good
        ERROR_COLOR = "#E74C3C"      # Red for bad/problem
        HIGHLIGHT_COLOR = "#F39C12"  # Orange for emphasis
        INFO_COLOR = "#3498DB"       # Blue for info
        
        # ==========================================
        # PART 1: INTRODUCTION - WHY GO DEEPER?
        # ==========================================
        
        title = Text("Why Do We Need Deeper Networks?", font_size=56, weight=BOLD)
        title.set_color(HIGHLIGHT_COLOR)
        title.to_edge(UP, buff=0.6).shift(DOWN*0.7)
        
        self.play(Write(title), run_time=1)
        self.wait(1)
        
        # Simple intuition
        intuition = Text("More layers = More features = Better accuracy?", 
                        font_size=40, weight=BOLD)
        intuition.set_color(WHITE)
        intuition.next_to(title, DOWN, buff=0.8)
        
        self.play(FadeIn(intuition, shift=UP * 0.3), run_time=0.7)
        self.wait(2)

        
        self.play(FadeOut(intuition), FadeOut(title), run_time=0.5)
        
        # ==========================================
        # PART 2: WHAT DOES EACH LAYER LEARN?
        # ==========================================
        
        layer_title = Text("What Does Each Layer Learn?", font_size=52, weight=BOLD)
        layer_title.set_color(INFO_COLOR)
        layer_title.to_edge(UP, buff=0.5)
        
        self.play(Write(layer_title), run_time=0.8)
        
        # Create visual showing feature hierarchy
        # (title_above, range_inside, features, color)
        layer_data = [
            ("Early Layers", "1-3", "Edges\nColors\nSimple Shapes", "#E74C3C"),
            ("Middle Layers", "4-8", "Textures\nPatterns\nObject Parts", "#F39C12"),
            ("Deep Layers", "9-16", "Features\nObjects\nContext", "#2ECC71"),
            ("Very Deep", "17+", "Abstract \n Concepts\n ", "#9B59B6"),
        ]
        
        feature_blocks = VGroup()
        arrows = VGroup()
        
        start_x = -6
        spacing_x = 4.02
        
        for i, (title, layer_range, features, color) in enumerate(layer_data):
            # Create a feature card
            card = RoundedRectangle(width=2.8, height=2.4, corner_radius=0.12)
            card.set_fill(color, opacity=0.85)
            card.set_stroke(WHITE, width=2.5)
            card.move_to(RIGHT * (start_x + i * spacing_x) + DOWN * 0.3)
            
            # Title ABOVE the rectangle (outside)
            title_text = Text(title, font_size=30, weight=BOLD)
            title_text.set_color(WHITE)
            title_text.next_to(card, UP, buff=0.35)
            
            # Layer range inside card at the top
            range_text = Text(layer_range, font_size=34, weight=BOLD)
            range_text.set_color(WHITE)
            range_text.move_to(card.get_top() + DOWN * 0.37)
            
            # Feature list - create separate lines with bigger font
            feature_lines = features.split("\n")
            feature_group = VGroup()
            for line in feature_lines:
                line_text = Text(line, font_size=24, weight=BOLD)
                line_text.set_color(WHITE)
                feature_group.add(line_text)
            feature_group.arrange(DOWN, buff=0.12)
            feature_group.move_to(card.get_center() + DOWN * 0.2)
            
            feature_blocks.add(VGroup(card, title_text, range_text, feature_group))
            
            # Add arrow
            if i < len(layer_data) - 1:
                arrow = Arrow(
                    card.get_right() + RIGHT * 0.05,
                    card.get_right() + RIGHT * 1.15,
                    buff=0, stroke_width=3, max_tip_length_to_length_ratio=0.3
                ).set_color(WHITE)
                arrows.add(arrow)
        
        # Animate feature blocks one by one
        for i, block in enumerate(feature_blocks):
            self.play(GrowFromCenter(block), run_time=0.5)
            if i < len(arrows):
                self.play(GrowArrow(arrows[i]), run_time=0.3)
        
        self.wait(1)

        
        # Key insight
        hierarchy_insight = Text("Deeper layers = Higher-level abstractions!", 
                                font_size=42, weight=BOLD)
        hierarchy_insight.set_color(SUCCESS_COLOR)
        hierarchy_insight.move_to(DOWN * 3.14)
        
        self.play(FadeIn(hierarchy_insight, shift=UP * 0.2), run_time=0.6)
        self.wait(2)
        
        # Clear
        self.play(
            FadeOut(layer_title), FadeOut(feature_blocks), 
            FadeOut(arrows), FadeOut(hierarchy_insight),
            run_time=0.6
        )
        
        # ==========================================
        # PART 3: THE EXPECTATION
        # ==========================================
        
        expect_title = Text("The Expectation", font_size=65, weight=BOLD)
        expect_title.set_color(SUCCESS_COLOR)
        expect_title.to_edge(UP, buff=0.5)
        
        self.play(Write(expect_title), run_time=0.7)
        
        expectations = [
            "More layers -> Learn more complex features",
            "More layers -> Better generalization",
            "More layers -> Higher accuracy",
        ]
        
        exp_group = VGroup()
        for i, exp in enumerate(expectations):
            text = Text(exp, font_size=39, weight=BOLD)
            text.set_color(WHITE)
            text.move_to(UP * (0.8 - i * 1.0))
            
            check = Text("", font_size=40, weight=BOLD)
            check.set_color(SUCCESS_COLOR)
            check.next_to(text, LEFT, buff=0.3)
            
            exp_group.add(VGroup(check, text))
        
        for item in exp_group:
            self.play(FadeIn(item, shift=RIGHT * 0.3), run_time=0.5)
            self.wait(0.5)
        
        self.wait(1)
        
        # Add the logical conclusion
        conclusion = Text("So a 56-layer network should beat \n       a 20-layer network!", 
                         font_size=50, weight=BOLD)
        conclusion.set_color(INFO_COLOR)
        conclusion.move_to(DOWN * 2.98)
        
        self.play(FadeIn(conclusion, shift=UP * 0.2), run_time=0.6)
        self.wait(2)
        
        self.play(FadeOut(expect_title), FadeOut(exp_group), FadeOut(conclusion), run_time=0.5)
        
        # ==========================================
        # PART 4: THE SHOCKING REALITY
        # ==========================================
        
        reality_title = Text("The Shocking Reality", font_size=62, weight=BOLD)
        reality_title.set_color(ERROR_COLOR)
        reality_title.to_edge(UP, buff=0.5)
        
        self.play(Write(reality_title), run_time=0.7)
        self.wait(0.5)
        
        # Show the actual experimental results text
        experiment = Text("Experiment: 56-layer vs 20-layer network \n           on CIFAR-10 Dataset", 
                         font_size=45, weight=BOLD)
        experiment.set_color(WHITE)
        experiment.next_to(reality_title, DOWN, buff=1)
        
        self.play(FadeIn(experiment), run_time=0.5)
        self.wait(1)
        
        # Results
        result_20 = Text("20-layer:  Error = 7.9%", font_size=46, weight=BOLD)
        result_20.set_color(SUCCESS_COLOR)
        result_20.move_to(UP * 0.3).shift(DOWN)
        
        result_56 = Text("56-layer:  Error = 9.6%", font_size=46, weight=BOLD)
        result_56.set_color(ERROR_COLOR)
        result_56.move_to(DOWN * 0.6).shift(DOWN*1.19)
        
        self.play(FadeIn(result_20, shift=LEFT * 0.3), run_time=0.5)
        self.wait(0.5)
        self.play(FadeIn(result_56, shift=LEFT * 0.3), run_time=0.5)
        self.wait(1)
        
        # Highlight the problem
        problem_box = RoundedRectangle(width=10, height=1.2, corner_radius=0.1)
        problem_box.set_stroke(ERROR_COLOR, width=4)
        problem_box.set_fill(ERROR_COLOR, opacity=0.15)
        problem_box.move_to(DOWN * 2.2).shift(DOWN)
        
        problem_text = Text("Deeper network is WORSE!", font_size=40, weight=BOLD)
        problem_text.set_color(ERROR_COLOR)
        problem_text.move_to(problem_box.get_center())
        
        self.play(GrowFromCenter(problem_box), run_time=0.4)
        self.play(Write(problem_text), run_time=0.5)
        self.wait(2)
        
        self.play(
            FadeOut(reality_title), FadeOut(experiment),
            FadeOut(result_20), FadeOut(result_56),
            FadeOut(problem_box), FadeOut(problem_text),
            run_time=0.6
        )
        
        # ==========================================
        # PART 5: THE DEGRADATION PROBLEM - GRAPH
        # ==========================================
        
        degradation_title = Text("The Degradation Problem", font_size=62, weight=BOLD)
        degradation_title.set_color(ERROR_COLOR)
        degradation_title.to_edge(UP, buff=0.5)
        
        self.play(Write(degradation_title), run_time=0.7)
        self.wait(0.5)
        
        # Create BIGGER graph
        graph_center = DOWN * 0.87
        graph_width = 9
        graph_height = 4.5
        
        # Axes - bigger
        y_axis = Arrow(
            graph_center + DOWN * (graph_height/2) + LEFT * 4.5,
            graph_center + UP * (graph_height/2) + LEFT * 4.5,
            stroke_width=4, buff=0
        ).set_color(WHITE)
        
        x_axis = Arrow(
            graph_center + DOWN * (graph_height/2) + LEFT * 4.5,
            graph_center + DOWN * (graph_height/2) + RIGHT * 4.5,
            stroke_width=4, buff=0
        ).set_color(WHITE)
        
        y_label = Text("Training Error", font_size=32, weight=BOLD)
        y_label.set_color(WHITE)
        y_label.rotate(PI/2)
        y_label.next_to(y_axis, LEFT, buff=0.3)
        
        x_label = Text("Epochs", font_size=39, weight=BOLD)
        x_label.set_color(WHITE)
        x_label.next_to(x_axis, DOWN, buff=0.3)
        
        self.play(ShowCreation(y_axis), ShowCreation(x_axis), run_time=0.5)
        self.play(FadeIn(y_label), FadeIn(x_label), run_time=0.4)
        
        # Create both curves - BIGGER
        base_x = graph_center[0] - 4
        base_y = graph_center[1]
        
        # 20-layer curve (good - lower error)
        shallow_curve = VMobject()
        shallow_points = [
            np.array([base_x, base_y + 1.8, 0]),
            np.array([base_x + 2, base_y + 0.4, 0]),
            np.array([base_x + 4, base_y - 0.5, 0]),
            np.array([base_x + 6, base_y - 1.2, 0]),
            np.array([base_x + 8, base_y - 1.5, 0]),
        ]
        shallow_curve.set_points_smoothly(shallow_points)
        shallow_curve.set_stroke(SUCCESS_COLOR, width=5)
        
        shallow_label = Text("20-layer", font_size=38, weight=BOLD)
        shallow_label.set_color(SUCCESS_COLOR)
        shallow_label.next_to(shallow_curve.get_end(), RIGHT, buff=0.2)
        
        # 56-layer curve (bad - higher error that gets worse)
        deep_curve = VMobject()
        deep_points = [
            np.array([base_x, base_y + 1.8, 0]),
            np.array([base_x + 2, base_y + 0.6, 0]),
            np.array([base_x + 4, base_y + 0.1, 0]),
            np.array([base_x + 6, base_y - 0.2, 0]),
            np.array([base_x + 8, base_y - 0.4, 0]),
        ]
        deep_curve.set_points_smoothly(deep_points)
        deep_curve.set_stroke(ERROR_COLOR, width=5)
        
        deep_label = Text("56-layer", font_size=38, weight=BOLD)
        deep_label.set_color(ERROR_COLOR)
        deep_label.next_to(deep_curve.get_end(), RIGHT, buff=0.2)
        
        self.play(ShowCreation(shallow_curve), run_time=1)
        self.play(FadeIn(shallow_label), run_time=0.3)
        self.wait(0.5)
        
        self.play(ShowCreation(deep_curve), run_time=1)
        self.play(FadeIn(deep_label), run_time=0.3)
        self.wait(1)



        
        # Highlight the gap with two arrows - adjusted for bigger graph
        gap_arrow_up = Arrow(
            np.array([base_x + 7, base_y - 0.8, 0]),
            np.array([base_x + 7, base_y - 1.4, 0]),
            stroke_width=4, buff=0
        ).set_color(HIGHLIGHT_COLOR).shift(UP*0.04)
        
        gap_arrow_down = Arrow(
            np.array([base_x + 7, base_y + 0.2, 0]),
            np.array([base_x + 7, base_y - 0.3, 0]),
            stroke_width=4, buff=0
        ).set_color(HIGHLIGHT_COLOR).rotate(PI).shift(DOWN*0.5)
        
        gap_arrow = VGroup(gap_arrow_up, gap_arrow_down)
        
        gap_label_1 = Text("Degradation Gap", weight=BOLD).next_to(gap_arrow, UP, buff=0.7)
        gap_label_1.set_color(HIGHLIGHT_COLOR)
        
        self.play(GrowFromCenter(gap_arrow), FadeIn(gap_label_1), run_time=0.6)
        self.wait(1)
        
        
        # Clear graph
        graph_elements = VGroup(
            y_axis, x_axis, y_label, x_label,
            shallow_curve, shallow_label, 
            deep_curve, deep_label,
            gap_arrow, gap_label_1
        )
        self.play(FadeOut(graph_elements), FadeOut(degradation_title), run_time=0.6)
        
        # ==========================================
        # PART 6: WHY DOES THIS HAPPEN?
        # ==========================================

        why_title = Text("Why Does Degradation Happen?", font_size=58, weight=BOLD)
        why_title.set_color(HIGHLIGHT_COLOR)
        why_title.to_edge(UP, buff=0.5)
        
        self.play(Write(why_title), run_time=0.7)
        self.wait(0.5)
        
        # The logical argument - wrapped long texts
        argument_points = [
            ("Consider this:", WHITE, 46),
            ("   If 20 layers is optimal, what should extra 36 layers do?", INFO_COLOR, 33),
            ("Ideally: Just pass the input unchanged (identity mapping)", SUCCESS_COLOR, 33),
            ("output = input", GREEN, 47),
            ("Then 56-layer would be AT LEAST as good as 20-layer!", WHITE, 33),
        ]
        
        arg_group = VGroup()
        for i, (text, color, size) in enumerate(argument_points):
            t = Text(text, font_size=size, weight=BOLD)
            t.set_color(color)
            t.move_to(UP * (1.4 - i * 1.0))
            arg_group.add(t)
        
        for item in arg_group:
            self.play(FadeIn(item, shift=UP * 0.2), run_time=0.5)
            self.wait(1)
        
        self.wait(1)
        self.play(FadeOut(arg_group), run_time=0.4)
        
        # The problem reveal
        the_problem = Text("THE PROBLEM:", font_size=48, weight=BOLD)
        the_problem.set_color(ERROR_COLOR)
        the_problem.move_to(UP * 1.5)
        
        problem_statement = Text("Neural networks CANNOT easily learn the identity!", 
                                font_size=38, weight=BOLD)
        problem_statement.set_color(ERROR_COLOR)
        problem_statement.next_to(the_problem, DOWN, buff=0.76)
        
        self.play(Write(the_problem), run_time=0.5)
        self.play(FadeIn(problem_statement, shift=UP * 0.2), run_time=0.6)
        self.wait(1.5)
        
        # Why? - Using numbers instead of bullets, wrapped text
        why_identity_hard = VGroup(
            Text("Why is identity hard?", font_size=38, weight=BOLD),
            Text("1. Weights are randomly initialized", font_size=32),
            Text("2. Networks learn complex transformations", font_size=32),
            Text("3. Optimizer pushes weights\n   towards complex solutions", font_size=32),
        )
        why_identity_hard[0].set_color(HIGHLIGHT_COLOR)
        for item in why_identity_hard[1:]:
            item.set_color(WHITE)
        
        why_identity_hard.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        why_identity_hard.move_to(DOWN * 1.2).shift(DOWN*0.97)
        
        self.play(FadeIn(why_identity_hard[0]), run_time=0.4)
        for item in why_identity_hard[1:]:
            self.play(FadeIn(item, shift=RIGHT * 0.2), run_time=0.4)
        
        self.wait(2)
        
        self.play(
            FadeOut(why_title), FadeOut(the_problem), 
            FadeOut(problem_statement), FadeOut(why_identity_hard),
            run_time=0.5
        )
        
        # ==========================================
        # PART 7: THE VANISHING GRADIENT PROBLEM
        # ==========================================
        
        gradient_title = Text("Another Problem: Vanishing Gradients", font_size=48, weight=BOLD)
        gradient_title.set_color(ERROR_COLOR)
        gradient_title.to_edge(UP, buff=0.5)
        
        self.play(Write(gradient_title), run_time=0.7)
        self.wait(0.5)
        
        # Explain the chain rule - positioned higher
        chain_explanation = VGroup(
            Text("During backpropagation:", font_size=38, weight=BOLD),
            Text("Gradients are multiplied through each layer", font_size=34, weight=BOLD),
        )
        chain_explanation[0].set_color(INFO_COLOR)
        chain_explanation[1].set_color(WHITE)
        chain_explanation.arrange(DOWN, buff=0.4)
        chain_explanation.next_to(gradient_title, DOWN, buff=0.5)
        
        self.play(FadeIn(chain_explanation[0]), run_time=0.4)
        self.play(FadeIn(chain_explanation[1]), run_time=0.4)
        self.wait(1)
        
        # Visual: Gradient getting smaller - NO TEXT inside circles
        gradient_visual = VGroup()
        gradient_sizes = [0.55, 0.45, 0.35, 0.25, 0.16, 0.08]
        start_x = -4.5
        
        for i, size in enumerate(gradient_sizes):
            circle = Circle(radius=size)
            circle.set_fill(ERROR_COLOR, opacity=0.9)
            circle.set_stroke(WHITE, width=2)
            circle.move_to(RIGHT * (start_x + i * 1.8) + DOWN * 0.3)
            
            gradient_visual.add(circle)
        
        # Layer labels BELOW circles, not inside
        layer_labels = VGroup()
        for i, circle in enumerate(gradient_visual):
            label = Text(f"L{len(gradient_sizes)-i}", font_size=30, weight=BOLD)
            label.set_color(WHITE)
            label.next_to(circle, DOWN, buff=0.15)
            layer_labels.add(label)
        
        # Add arrows between
        grad_arrows = VGroup()
        for i in range(len(gradient_visual) - 1):
            arrow = Arrow(
                gradient_visual[i+1].get_left(),
                gradient_visual[i].get_right(),
                buff=0.08, stroke_width=2.5
            ).set_color(WHITE)
            grad_arrows.add(arrow)
        
        # Label positioned to the right, not overlapping
        gradient_flow_label = Text("← Gradient flows backward", font_size=32, weight=BOLD)
        gradient_flow_label.set_color(WHITE)
        gradient_flow_label.next_to(gradient_visual[-3], DOWN, buff=1.5)
        
        self.play(*[GrowFromCenter(g) for g in gradient_visual], run_time=0.8)
        self.play(*[FadeIn(l) for l in layer_labels], run_time=0.4)
        self.play(*[GrowArrow(a) for a in grad_arrows], run_time=0.5)
        self.play(FadeIn(gradient_flow_label), run_time=0.74)
        self.wait(2)

        
        # Problem statement - positioned lower to avoid overlap
        vanish_problem = VGroup(
            Text("By the time gradients reach early layers...", font_size=39, weight=BOLD),
            Text("They're almost ZERO!", font_size=45, weight=BOLD),
        )
        vanish_problem[0].set_color(WHITE)
        vanish_problem[1].set_color(ERROR_COLOR)
        vanish_problem.arrange(DOWN, buff=0.45)
        vanish_problem.move_to(DOWN * 2.0).shift(DOWN*1.1)
        
        self.play(FadeIn(vanish_problem[0]), FadeOut(gradient_flow_label), run_time=0.4)
        self.play(FadeIn(vanish_problem[1], scale=1.2), run_time=0.5)
        self.wait(2)
        
        # Consequence - positioned with proper spacing
        consequence = Text("Early layers can't learn! They stay random!", font_size=40, weight=BOLD)
        consequence.set_color(HIGHLIGHT_COLOR)
        consequence.move_to(DOWN * 3.0)
        
        self.play(FadeIn(consequence, shift=LEFT * 0.2), FadeOut(vanish_problem),run_time=0.5)
        self.wait(2)
        
        # Clear
        self.play(
            FadeOut(gradient_title), FadeOut(chain_explanation),
            FadeOut(gradient_visual), FadeOut(layer_labels), FadeOut(grad_arrows), 
            FadeOut(consequence),
            run_time=0.6
        )
        
        # ==========================================
        # PART 8: THE SOLUTION PREVIEW
        # ==========================================
        
        solution_title = Text("The Solution: A New Insight", font_size=52, weight=BOLD)
        solution_title.set_color(SUCCESS_COLOR)
        solution_title.to_edge(UP, buff=0.6).shift(UP*0.14)
        
        self.play(Write(solution_title), run_time=0.7)
        self.wait(0.5)
        
        # The key insights
        insights = [
            ("The Problem:", ERROR_COLOR),
            ("Learning identity H(x) = x is hard", WHITE),
            ("", WHITE),  # spacer
            ("The Solution:", SUCCESS_COLOR),
            ("Don't ask layers to learn identity", WHITE),
            ("Let them learn the RESIDUAL: F(x) = H(x) - x", INFO_COLOR),
            ("", WHITE),  # spacer
            ("If identity is optimal:", HIGHLIGHT_COLOR),
            ("Layers just need to output F(x) = 0", SUCCESS_COLOR),
            ("Pushing weights to zero is EASY!", SUCCESS_COLOR),
        ]
        
        insight_group = VGroup()
        for i, (text, color) in enumerate(insights):
            if text:
                t = Text(text, font_size=35, weight=BOLD)
                t.set_color(color)
                insight_group.add(t)
        
        insight_group.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        insight_group.move_to(DOWN * 0.5).shift(DOWN*0.23)
        
        for item in insight_group:
            self.play(FadeIn(item, shift=RIGHT * 0.15), run_time=0.4)
            self.wait(0.4)
        
        self.wait(2)

        self.play(FadeOut(solution_title), FadeOut(insight_group), run_time=0.5)
        
        # ==========================================
        # PART 9: FINAL SUMMARY
        # ==========================================
        
        summary_title = Text("Why We Need ResNets", font_size=52, weight=BOLD)
        summary_title.set_color(HIGHLIGHT_COLOR)
        summary_title.to_edge(UP, buff=0.5)
        
        self.play(Write(summary_title), run_time=0.7)
        
        summary_points = [
            ("Deeper networks suffer from degradation", ERROR_COLOR),
            ("Gradients vanish in early layers", ERROR_COLOR),
            ("Networks can't learn identity mappings", ERROR_COLOR),
            ("", WHITE),
            ("Skip connections provide 'gradient highways'", SUCCESS_COLOR),
            ("Learning F(x) = 0 is trivial", SUCCESS_COLOR),
            ("Enables training 100+ layer networks!", SUCCESS_COLOR),
        ]
        
        summary_group = VGroup()
        for text, color in summary_points:
            if text:
                t = Text(text, font_size=35, weight=BOLD)
                t.set_color(color)
                summary_group.add(t)
        
        summary_group.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        summary_group.move_to(DOWN * 0.5)
        
        for item in summary_group:
            self.play(FadeIn(item, shift=LEFT * 0.2), run_time=0.35)
        
        self.wait(1)
     

class ResidualNetwork(Scene):
    """
    Visualization of a Residual Network with 3 stacked residual blocks.
    Each block contains: Layer 1 -> ReLU -> Layer 2 -> (+) -> ReLU
    With skip connections from input of each block to the addition circle.
    
    Animation flow: Build entire structure first, rotate it, then animate blocks one by one
    using GrowFromCenter for rectangles, GrowArrow for arrows, ShowCreation for skip.
    """
    
    def construct(self):
        # Color Palette - Premium aesthetic
        PRIMARY = "#E74C3C"
        SECONDARY = "#3498DB"
        SUCCESS = "#2ECC71"
        ACCENT = "#9B59B6"
        INPUT_COLOR = "#3498DB"  # Blue for input
        OUTPUT_COLOR = "#FF9800"  # Orange for output
        
        # Text scale factor
        TEXT_SCALE = 1.33
        
        # Layout constants - CONSISTENT SPACING
        box_width = 4.5
        box_height = 0.9
        vertical_gap = 1.6  # Consistent gap between elements within block
        block_gap = 2.0     # Consistent gap between blocks (averaged)
        arrow_buff = 0.15   # Consistent arrow buffer
        
        # Starting Y position for the network
        start_y = 5
        
        # Collect all elements in a VGroup for rotation
        all_elements = VGroup()
        
        # ==========================================
        # BUILD ENTIRE STRUCTURE (WITHOUT ANIMATING)
        # ==========================================
        
        # ==========================================
        # INPUT LAYER BLOCK (Blue)
        # ==========================================
        input_block = RoundedRectangle(width=box_width, height=box_height, corner_radius=0.15)
        input_block.set_fill(INPUT_COLOR, opacity=0.95)
        input_block.set_stroke(WHITE, width=4)
        input_block.move_to(UP * start_y)
        
        input_text = Text("Input", font_size=34, weight=BOLD)
        input_text.scale(TEXT_SCALE)
        input_text.set_color(WHITE)
        input_text.move_to(input_block.get_center())
        
        all_elements.add(input_block, input_text)
        
        # ==========================================
        # CREATE 3 RESIDUAL BLOCKS - Store references for animation
        # ==========================================
        
        current_y = start_y - block_gap
        layer_counter = 1
        prev_output_point = input_block.get_bottom()
        
        # Store all block data for animation later
        block_data = []
        
        for block_idx in range(3):
            block_info = {}
            
            # ==========================================
            # Layer 1
            # ==========================================
            layer1_y = current_y
            layer1_box = RoundedRectangle(width=box_width, height=box_height, corner_radius=0.15)
            layer1_box.set_fill(ACCENT, opacity=0.95)
            layer1_box.set_stroke(WHITE, width=4)
            layer1_box.move_to(UP * layer1_y)
            
            layer1_text = Text(f"Layer {layer_counter}", font_size=32, weight=BOLD)
            layer1_text.scale(TEXT_SCALE)
            layer1_text.set_color(WHITE)
            layer1_text.move_to(layer1_box.get_center())
            layer_counter += 1
            
            # ==========================================
            # ReLU 1
            # ==========================================
            relu1_y = layer1_y - vertical_gap
            relu1_box = RoundedRectangle(width=box_width, height=0.7, corner_radius=0.12)
            relu1_box.set_fill(SUCCESS, opacity=0.95)
            relu1_box.set_stroke(WHITE, width=4)
            relu1_box.move_to(UP * relu1_y)
            
            relu1_text = Text("ReLU", font_size=30, weight=BOLD)
            relu1_text.scale(TEXT_SCALE)
            relu1_text.set_color(WHITE)
            relu1_text.move_to(relu1_box.get_center())
            
            # ==========================================
            # Layer 2
            # ==========================================
            layer2_y = relu1_y - vertical_gap
            layer2_box = RoundedRectangle(width=box_width, height=box_height, corner_radius=0.15)
            layer2_box.set_fill(ACCENT, opacity=0.95)
            layer2_box.set_stroke(WHITE, width=4)
            layer2_box.move_to(UP * layer2_y)
            
            layer2_text = Text(f"Layer {layer_counter}", font_size=32, weight=BOLD)
            layer2_text.scale(TEXT_SCALE)
            layer2_text.set_color(WHITE)
            layer2_text.move_to(layer2_box.get_center())
            layer_counter += 1
            
            # ==========================================
            # Addition circle
            # ==========================================
            add_y = layer2_y - vertical_gap
            add_circle = Circle(radius=0.5)
            add_circle.set_fill("#E74C3C", opacity=1)
            add_circle.set_stroke(WHITE, width=4)
            add_circle.move_to(UP * add_y)
            
            add_text = Text("+", font_size=48, weight=BOLD)
            add_text.scale(TEXT_SCALE)
            add_text.set_color(WHITE)
            add_text.move_to(add_circle.get_center())
            
            # ==========================================
            # ReLU 2
            # ==========================================
            relu2_y = add_y - vertical_gap
            relu2_box = RoundedRectangle(width=box_width, height=0.7, corner_radius=0.12)
            relu2_box.set_fill(SUCCESS, opacity=0.95)
            relu2_box.set_stroke(WHITE, width=4)
            relu2_box.move_to(UP * relu2_y)
            
            relu2_text = Text("ReLU", font_size=30, weight=BOLD)
            relu2_text.scale(TEXT_SCALE)
            relu2_text.set_color(WHITE)
            relu2_text.move_to(relu2_box.get_center())
            
            # ==========================================
            # Arrows for this block
            # ==========================================
            
            # Arrow from previous block/input to this block's Layer 1
            arrow_to_block = Arrow(
                prev_output_point, 
                layer1_box.get_top(),
                buff=arrow_buff, stroke_width=5, max_tip_length_to_length_ratio=0.1
            ).set_color(WHITE)
            
            # Arrow: Layer 1 → ReLU 1
            arr1 = Arrow(
                layer1_box.get_bottom(), 
                relu1_box.get_top(),
                buff=arrow_buff, stroke_width=5, max_tip_length_to_length_ratio=0.12
            ).set_color(WHITE)
            
            # Arrow: ReLU 1 → Layer 2
            arr2 = Arrow(
                relu1_box.get_bottom(), 
                layer2_box.get_top(),
                buff=arrow_buff, stroke_width=5, max_tip_length_to_length_ratio=0.12
            ).set_color(WHITE)
            
            # Arrow: Layer 2 → Addition circle
            arr_to_add = Arrow(
                layer2_box.get_bottom(), 
                add_circle.get_top(),
                buff=arrow_buff, stroke_width=5, max_tip_length_to_length_ratio=0.1
            ).set_color(WHITE)
            
            # Arrow: Addition → ReLU 2
            arr_add_to_relu = Arrow(
                add_circle.get_bottom(), 
                relu2_box.get_top(),
                buff=arrow_buff, stroke_width=5, max_tip_length_to_length_ratio=0.12
            ).set_color(WHITE)
            
            # ==========================================
            # Skip connection
            # ==========================================
            
            # Branch point - middle of input arrow
            skip_branch_y = (prev_output_point[1] + layer1_box.get_top()[1]) / 2
            skip_start = np.array([0, skip_branch_y, 0])
            
            # Go RIGHT to edge of boxes + offset
            skip_right = np.array([box_width/2 + 1.0, skip_branch_y, 0])
            # Go DOWN to addition level
            skip_down = np.array([skip_right[0], add_circle.get_center()[1], 0])
            # Go LEFT to addition circle right edge
            skip_end = add_circle.get_right() + RIGHT * 0.05
            
            # Create skip path
            skip_path = VMobject()
            skip_path.set_points_as_corners([skip_start, skip_right, skip_down, skip_end])
            skip_path.set_stroke(WHITE, width=4)
            
            # Small dot at branch point
            branch_dot = Dot(radius=0.1, color=WHITE)
            branch_dot.move_to(skip_start)
            
            # Store block info for animation
            block_info['rectangles'] = [layer1_box, layer1_text, relu1_box, relu1_text,
                                        layer2_box, layer2_text, add_circle, add_text,
                                        relu2_box, relu2_text]
            block_info['arrow_to_block'] = arrow_to_block
            block_info['arrows'] = [arr1, arr2, arr_to_add, arr_add_to_relu]
            block_info['skip_path'] = skip_path
            block_info['branch_dot'] = branch_dot
            
            # Add to all_elements for rotation
            all_elements.add(*block_info['rectangles'])
            all_elements.add(arrow_to_block, arr1, arr2, arr_to_add, arr_add_to_relu)
            all_elements.add(skip_path, branch_dot)
            
            block_data.append(block_info)
            
            # Update for next block
            prev_output_point = relu2_box.get_bottom()
            current_y = relu2_y - block_gap
        
        # ==========================================
        # OUTPUT LAYER BLOCK (Orange)
        # ==========================================
        output_y = current_y + 0.5
        output_block = RoundedRectangle(width=box_width, height=box_height, corner_radius=0.15)
        output_block.set_fill(OUTPUT_COLOR, opacity=0.95)
        output_block.set_stroke(WHITE, width=4)
        output_block.move_to(UP * output_y).shift(DOWN*0.63)
        
        output_text = Text("Output", font_size=34, weight=BOLD)
        output_text.scale(TEXT_SCALE)
        output_text.set_color(WHITE)
        output_text.move_to(output_block.get_center())
        
        # Arrow to output block
        arrow_to_output = Arrow(
            prev_output_point,
            output_block.get_top(),
            buff=arrow_buff, stroke_width=5, max_tip_length_to_length_ratio=0.1
        ).set_color(WHITE)
        
        all_elements.add(output_block, output_text, arrow_to_output)
        
        # ==========================================
        # STEP 1: ROTATE ENTIRE STRUCTURE FIRST (90° counter-clockwise)
        # ==========================================
        all_elements.rotate(PI / 2)
        
        # Adjust camera for horizontal layout
        self.camera.frame.scale(1.7).shift(LEFT*6 + DOWN*8.9)
        
        # ==========================================
        # STEP 2: ANIMATE BLOCKS ONE BY ONE (already rotated)
        # Using GrowFromCenter, GrowArrow, ShowCreation as original
        # ==========================================
        
        # Animate INPUT block first
        self.play(
            GrowFromCenter(input_block),
            GrowFromCenter(input_text),
            run_time=0.6
        )
        self.wait(1)
        
        # Animate each residual block
        for block_info in block_data:
            # First: Arrow from previous to this block
            self.play(
                GrowArrow(block_info['arrow_to_block']),
                run_time=0.4
            )
            
            # GrowFromCenter ALL rectangles of this block at once
            self.play(
                *[GrowFromCenter(rect) for rect in block_info['rectangles']],
                run_time=0.8
            )
            
            # Animate all internal arrows at once
            self.play(
                *[GrowArrow(arr) for arr in block_info['arrows']],
                run_time=0.6
            )
            
            # Skip connection animation
            self.play(
                FadeIn(block_info['branch_dot'], scale=0.5),
                run_time=0.15
            )
            self.play(
                ShowCreation(block_info['skip_path']),
                run_time=0.7,
                rate_func=smooth
            )
            
            self.play(self.camera.frame.animate.shift(RIGHT*4.8))


        # Animate OUTPUT block
        self.play(
            GrowArrow(arrow_to_output),
            run_time=0.4
        )
        self.play(
            GrowFromCenter(output_block),
            GrowFromCenter(output_text),
            run_time=0.6
        )
        
        self.wait(2)

        self.play(self.camera.frame.animate.shift(LEFT*7.89).scale(1.28))

        a = Text("Residual Network", font_size=156, weight=BOLD).next_to(all_elements, UP, buff=3.88).set_color(YELLOW)
        self.play(Write(a), self.camera.frame.animate.shift(UP*1.8))
        self.wait(2)

        self.play(FadeOut(a), self.camera.frame.animate.shift(DOWN*4))

        self.wait()

        # ==========================================
        # MATHEMATICAL EXPLANATION: LAYER 5 ACTIVATION
        # ==========================================
     
        eq1 = Tex(
            r"a^{(4)} = ReLU( W^{(4)} a^{(3)} + b^{(4)} + a^{(2)})",
            font_size=150
        )
        eq1.set_color(WHITE)
        eq1.next_to(all_elements, DOWN, buff=2.2)

        eq1[5:9].set_color(GREEN)
        
        self.play(Write(eq1), run_time=1.2)
        self.wait(1.5)

        rect = SurroundingRectangle(eq1[:4], stroke_width=6).scale(1.12)
        self.play(ShowCreation(rect), run_time=0.6)
        
        text3 = Text("Output of 4th Layer", font_size=84, weight=BOLD)
        text3.set_color(YELLOW)
        text3.next_to(eq1, DOWN, buff=1.355)
        
        self.play(FadeIn(text3, shift=LEFT * 0.3), run_time=0.9)
        self.wait(2)

        brace = Brace(eq1[5:9], DOWN, buff=0.55).set_color(YELLOW)

        self.play(ReplacementTransform(rect, brace), FadeOut(text3),)
        self.wait(2)

        self.play(Transform(brace, Brace(eq1[10:23], DOWN, buff=0.55).set_color(YELLOW)), run_time=0.6)
        text3 = Text("Weighted Sum + Bias From Last Layer", font_size=76, weight=BOLD)
        text3.set_color(YELLOW)
        text3.next_to(eq1, DOWN, buff=1.3959)
        
        self.play(FadeIn(text3, shift=LEFT * 0.3), run_time=0.9)
        self.wait(2)

        text4 = Text("Skip Connection From Last Residual Block", font_size=70, weight=BOLD)
        text4.set_color(YELLOW)
        text4.next_to(eq1, DOWN, buff=1.3959)
        
        self.play(Transform(brace, Brace(eq1[-5:-1], DOWN, buff=0.55).set_color(YELLOW)), FadeIn(text4, shift=LEFT * 0.3), FadeOut(text3),run_time=0.9)
        self.wait(2)

        self.play(FadeOut(text4), FadeOut(brace),run_time=0.6) 
        self.wait()

        self.play(eq1.animate.shift(DOWN*1))

        temp = Tex(r"a^{(4)} = ReLU(z^{(4)} + a^{(2)})", font_size=190).set_color(WHITE).move_to(eq1.get_center())

        temp[5:9].set_color(GREEN)

        self.play(Transform(eq1, temp))
        self.wait(2)

        rect = SurroundingRectangle(eq1[15:21], stroke_width=10).scale(1.2)
        self.play(ShowCreation(rect))

        self.wait(2)

        temp = Tex(r"a^{(4)} = ReLU(a^{(2)})", font_size=190).set_color(WHITE).move_to(eq1.get_center())
        temp[5:9].set_color(GREEN)

        self.play(Transform(eq1, temp), FadeOut(rect))
        self.wait(2)

        temp = Tex(r"a^{(4)} = ReLU(z^{(4)} + a^{(2)})", font_size=190).set_color(WHITE).move_to(eq1.get_center())

        temp[5:9].set_color(GREEN)

        self.play(Transform(eq1, temp))
        self.wait(2)

        rect = SurroundingRectangle(eq1[-8], stroke_width=8.4).scale(1.2)
        self.play(ShowCreation(rect))

        self.wait(2)

        # ==========================================
        # DIMENSIONALITY PROBLEM
        # ==========================================
        
        self.play(FadeOut(rect), run_time=0.4)
        
        # Show the dimension issue question
        dim_question = Text("But what if dimensions don't match?", font_size=82, weight=BOLD)
        dim_question.set_color("#E74C3C")
        dim_question.next_to(eq1, DOWN, buff=1.01)
        
        self.play(FadeIn(dim_question, shift=UP * 0.3), self.camera.frame.animate.shift(DOWN*0.8),run_time=0.8)
        self.wait(1.5)
        
        self.play(FadeOut(dim_question), run_time=0.4)
        
        # Show dimension mismatch example
        dim_z = Tex(r"z^{(4)} \in \mathbb{R}^{256}", font_size=120)
        dim_z.set_color(YELLOW)
        dim_z.next_to(eq1, DOWN, buff=1.2).shift(LEFT * 4)
        
        dim_a = Tex(r"a^{(2)} \in \mathbb{R}^{128}", font_size=120)
        dim_a.set_color(MAROON_B)
        dim_a.next_to(eq1, DOWN, buff=1.2).shift(RIGHT * 4)
        
        vs_text = Text("vs", font_size=80, weight=BOLD)
        vs_text.set_color(WHITE)
        vs_text.next_to(eq1, DOWN, buff=1.5)
        
        self.play(
            Write(dim_z),
            Write(dim_a),
            FadeIn(vs_text),
            run_time=1
        )
        self.wait(2)
        

        # Show the problem - can't add!
        problem_text = Text("Can't add vectors of different sizes!", font_size=64, weight=BOLD)
        problem_text.set_color("#E74C3C")
        problem_text.next_to(vs_text, DOWN, buff=1.2)
        
        cross_mark = Tex(r"\times", font_size=250)
        cross_mark.set_color("#E74C3C")
        cross_mark.next_to(problem_text, RIGHT, buff=0.5)
        
        self.play(
            FadeIn(problem_text, shift=UP * 0.2),
            Write(cross_mark),
            self.camera.frame.animate.shift(DOWN*1.2),
            run_time=0.8
        )
        self.wait(2)
        
        # Clear and show solution
        self.play(
            FadeOut(dim_z), FadeOut(dim_a), FadeOut(vs_text),
            FadeOut(problem_text), FadeOut(cross_mark),
            self.camera.frame.animate.shift(UP*1.2),
            run_time=0.5
        )
        
        # ==========================================
        # SOLUTION: PROJECTION MATRIX W_s
        # ==========================================
        
        solution_title = Text("Solution: Projection Matrix", font_size=80, weight=BOLD)
        solution_title.set_color("#2ECC71")
        solution_title.next_to(eq1, DOWN, buff=1.3)
        
        self.play(Write(solution_title), run_time=0.8)
        self.wait(2)
        
        # Show W_s introduction
        ws_text = Tex(r"W_s \in \mathbb{R}^{256 \times 128}", font_size=180)
        ws_text.set_color("#F39C12")
        ws_text.move_to(solution_title.get_center())
        
        self.play(Write(ws_text), FadeOut(solution_title),run_time=0.8)
        self.wait(2)
        
        # Clear and show modified equation
        self.play(FadeOut(ws_text), run_time=0.4)
        
        # Transform to new equation with W_s
        new_eq = Tex(r"a^{(4)} = ReLU(z^{(4)} + W_s \cdot a^{(2)})", font_size=170)
        new_eq.set_color(WHITE)
        new_eq.move_to(eq1.get_center())
        new_eq[5:9].set_color(GREEN)
        new_eq[-8:-6].set_color(ORANGE)
        
        self.play(Transform(eq1, new_eq), run_time=1)
        self.wait(1.5)
        
        
        ws_label = Text("Projection Matrix", font_size=120, weight=BOLD)
        ws_label.set_color(ORANGE)
        ws_label.next_to(eq1, DOWN, buff=1.14)
        
        self.play(
            FadeIn(ws_label, shift=UP * 0.2),
            run_time=0.8
        )
        self.wait(2)
        
        # ==========================================
        # DIMENSION CHECK
        # ==========================================
        
        self.play(FadeOut(ws_label), run_time=0.4)
        
        dim_check_title = Text("Dimension Check:", font_size=110, weight=BOLD)
        dim_check_title.set_color(YELLOW)
        dim_check_title.next_to(eq1, DOWN, buff=1.2)
        
        self.play(Write(dim_check_title), run_time=0.6)
        
        # Show the dimension calculation
        dim_calc = Tex(
            r"W_s \cdot a^{(2)} : (256 \times 128) \cdot (128 \times 1) = (256 \times 1)",
            font_size=120
        )
        dim_calc.set_color(WHITE)
        dim_calc.move_to(dim_check_title)
        
        self.play(Write(dim_calc), FadeOut(dim_check_title),run_time=1.2)
        self.wait(2)
        
        # Show checkmark
        check_mark = Tex(r"\checkmark", font_size=150)
        check_mark.set_color("#2ECC71")
        check_mark.next_to(dim_calc, RIGHT, buff=0.5)
        
        self.play(Write(check_mark), run_time=0.5)
        self.wait(1)
        

        # ==========================================
        # FINAL SUMMARY
        # ==========================================
        
        self.play(
            FadeOut(dim_calc),
            FadeOut(check_mark),
            run_time=0.5
        )
        self.wait(2)

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


