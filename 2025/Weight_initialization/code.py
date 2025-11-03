from manimlib import *
import numpy as np

PURE_RED = "#FF0000"

class RandomInitialization(Scene):
    def construct(self):

        self.camera.frame.scale(1.17).shift(RIGHT*6 + DOWN*1.26)

        HIDDEN_COLOR = BLUE
        WEIGHT_COLOR = PURE_RED

        layer_sizes = [5, 6, 4, 3, 1]
        layer_spacing = 2.5
        neuron_spacing = 1.0

        layers = []

        # ===== CREATE NEURONS =====
        for i, size in enumerate(layer_sizes):
            layer = VGroup()
            for j in range(size):
                neuron = Circle(radius=0.22, color=WHITE, fill_opacity=0.15)
                if i == 0:
                    neuron.set_fill(GREEN, opacity=1).set_stroke(GREEN_B).scale(1.2)
                elif i == len(layer_sizes) - 1:
                    neuron.set_fill(HIDDEN_COLOR, opacity=1).set_stroke(BLUE_B).scale(2)
                else:
                    neuron.set_fill(HIDDEN_COLOR, opacity=1).set_stroke(BLUE_B).scale(1.7)
                neuron.move_to(RIGHT * 1.24 * i * layer_spacing + UP * (j - (size - 1) / 2) * neuron_spacing).set_z_index(1)
                layer.add(neuron)
            layers.append(layer)

        network = VGroup(*layers)

        # ===== CONNECTION CREATOR =====
        def create_connections(layers_mobj):
            conns = VGroup()
            for l1, l2 in zip(layers_mobj[:-1], layers_mobj[1:]):
                for n1 in l1:
                    for n2 in l2:
                        line = Line(
                            n1.get_center(), n2.get_center(),
                            color=WEIGHT_COLOR, stroke_width=1.5
                        ).set_color(GREY_B)
                        conns.add(line)
            return conns
        
        # ===== NEURON GROW + WEIGHT CREATION =====
        self.play(
            LaggedStartMap(GrowFromCenter, network, lag_ratio=0.05, run_time=1.5),
        )
        
        connections = create_connections(layers).set_z_index(-1)
        self.play(
            LaggedStartMap(ShowCreation, connections, lag_ratio=0.01, run_time=2),
        )
        self.wait(2)

        a = Tex(r"w_{ij} \sim \mathcal{N}(\mu,\,\sigma^2)").next_to(layers[1], DOWN)
        a.scale(1.77).shift(DOWN*0.95+RIGHT*2.8)
        
        self.play(ShowCreation(a))
        self.wait(2)

        self.play(Transform(a, Tex(r"w_{ij} \sim \mathcal{N}(0,\,1)").move_to(a).scale(1.77), run_time=0.7))
        self.wait(2)

        self.camera.frame.save_state()

        # ===== AXES =====
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 4, 3.5],
            axis_config={
                "stroke_width": 4,
                "include_tip": True,
                "include_ticks": True,
            },
            x_axis_config={
                "include_numbers": True,
            },
            y_axis_config={
                "include_numbers": False,
            },
        ).scale(2.4).next_to(layers[-1], RIGHT).shift(DOWN * 2.5 + RIGHT * 2.5)

        def fake_normal(x):
            return 7 * (1 / np.sqrt(2 * np.pi)) * np.exp(-x**2 / 2)

        graph = axes.get_graph(fake_normal, x_range=[-4, 4], color=YELLOW, stroke_width=3.2)
        y_label = Text("0.5").scale(1.2).next_to(axes.c2p(0, 3.5), LEFT, buff=0.43)

        # ===== ANIMATION =====
        self.play(ShowCreation(axes), ShowCreation(y_label), self.camera.frame.animate.shift(RIGHT*19).scale(1.37).shift(DOWN*1.27))
        self.play(ShowCreation(graph), run_time=2)
        self.wait(2)

        self.play(self.camera.frame.animate.restore())
        self.wait(2)

        self.play(Transform(a, Tex(r"w_{ij} \sim \mathcal{N}(0,\,1) \cdot 0.01").move_to(a).scale(1.77), run_time=0.7))
        self.wait(2)

        temp = Text("np.random.randn(fan_out * fan_in) * 0.01").move_to(a).scale(1.37)
        temp[10:15].set_color("#ff8808")

        self.play(Transform(a, temp, run_time=0.7))
        self.wait(2)

        rect = SurroundingRectangle(layers[0], fill_color="#ff0000", color="#ff0000", fill_opacity=0.13).scale(1.1)
        self.play(ShowCreation(rect))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(layers[1], fill_color="#ff0000", color="#ff0000", fill_opacity=0.13).scale(1.05)))
        self.wait(2)

        temp = Text("np.random.randn(6*5) * 0.01").move_to(a).scale(1.77)
        temp[10:15].set_color("#ff8808")
        temp_rect = SurroundingRectangle(temp, fill_color="#ff0000", color="#ff0000", fill_opacity=0.01).scale(1.05)
        self.play(Transform(a, temp, run_time=0.7))
        self.play(Transform(rect, temp_rect))
        self.wait(2)

        z = Tex(r"z_i = \sum_j w_{ij} x_j + b_i").move_to(a).scale(1.7).shift(DOWN*0.23)

        self.play(FadeOut(rect), FadeOut(a), FadeIn(z))
        self.wait(2)

        rect = SurroundingRectangle(z[-2:], color="#ff0000")
        self.play(ShowCreation(rect))
        self.wait(2)

        self.play(FadeOut(rect), Transform(z, Tex(r"z_i = \sum_j w_{ij} x_j").move_to(a).scale(1.7)))
        rect = SurroundingRectangle(z[4:], color="#ff0000").scale(1.066)
        self.play(ShowCreation(rect))
        self.wait(2)   

        self.play(FadeOut(rect), FadeOut(z))    

        # ===== HISTOGRAM SIMULATION =====
        
        histograms = VGroup()
        
        # Parameters for histogram appearance
        hist_width = 2
        hist_height = 0.8 * 2.4 * 3.2
        num_bins = 20
        
        # INPUT LAYER HISTOGRAM (Full Gaussian)
        input_layer = layers[0]
        
        # Create x-axis for input
        input_axis = Line(
            LEFT * hist_width/2, 
            RIGHT * hist_width/2,
            stroke_width=3,
            color=WHITE
        )
        input_axis.next_to(input_layer, DOWN, buff=1.71)
        
        # Create bars for input (full Gaussian distribution)
        input_bars = VGroup()
        input_var = 0.5  # Wide Gaussian for input data
        
        for i in range(num_bins):
            x = -2 + (i + 0.5) * (4 / num_bins)  # Range from -2 to 2
            
            height = np.exp(-(x**2) / (2 * input_var**2)) / (input_var * np.sqrt(2 * np.pi))
            height = height * hist_height * 0.5 * input_var
            
            bar = Rectangle(
                width=hist_width / num_bins * 0.9,
                height=height,
                fill_opacity=0.88,
                fill_color=GREEN,
                stroke_width=1,
                stroke_color=GREEN
            )
            
            bar.move_to(input_axis.get_center())
            bar.shift(RIGHT * (x * hist_width/4))
            bar.shift(UP * height/2)
            
            input_bars.add(bar)
        
        # Add labels for input histogram
        input_label = Text("Input data", font_size=46).next_to(input_axis, DOWN, buff=0.7)
        
        input_hist = VGroup(input_axis, input_bars, input_label).shift(DOWN*0.4)
        input_label.shift(UP*0.34)
        histograms.add(input_hist)
        
        # HIDDEN LAYER HISTOGRAMS (tanh(z) with decreasing variance)
        variances = [0.12, 0.08, 0.06]
        
        for layer_idx in range(1, len(layers)-1):  # skip input and output layer
            layer = layers[layer_idx]
            
            # Create x-axis
            axis_line = Line(
                LEFT * hist_width/2, 
                RIGHT * hist_width/2,
                stroke_width=3,
                color=WHITE
            )
            axis_line.next_to(layer, DOWN, buff=1.71)
            
            # Create histogram bars
            bars = VGroup()
            var = variances[layer_idx - 1]
            
            for i in range(num_bins):
                x = -1 + (i + 0.5) * (2 / num_bins)
                
                height = np.exp(-(x**2) / (2 * var**2)) / (var * np.sqrt(2 * np.pi))
                height = height * hist_height * 0.5 * var
                
                bar = Rectangle(
                    width=hist_width / num_bins * 0.9,
                    height=height,
                    fill_opacity=0.88,
                    fill_color=YELLOW,
                    stroke_width=1,
                    stroke_color=YELLOW
                )
                
                bar.move_to(axis_line.get_center())
                bar.shift(RIGHT * (x * hist_width/2))
                bar.shift(UP * height/2)
                
                bars.add(bar)
            
            # Add x-axis labels: -1, 0, 1
            label_minus1 = Text("-1", font_size=28).next_to(axis_line.get_start(), DOWN, buff=0.15)
            label_0 = Text("0", font_size=28).next_to(axis_line.get_center(), DOWN, buff=0.15)
            label_1 = Text("1", font_size=28).next_to(axis_line.get_end(), DOWN, buff=0.15)
            
            # Add tanh label
            tanh_label = Tex(r"\tanh(z)", font_size=46).next_to(axis_line, DOWN, buff=0.7)
            
            hist_group = VGroup(axis_line, bars, label_minus1, label_0, label_1, tanh_label)
            histograms.add(hist_group)
        
        histograms.shift(UP*0.1)
        # Animate all histograms appearing
        # First show input histogram
        self.play(
            FadeIn(input_hist[0]),  # axis
            FadeIn(input_hist[2]),  # "Input data" label
            run_time=0.5
        )
        self.play(
            LaggedStartMap(GrowFromEdge, input_hist[1], edge=DOWN, lag_ratio=0.05),
            run_time=1
        )
        self.wait(1)
        
        # Then show hidden layer histograms one by one
        for hist in histograms[1:]:
            self.play(
                FadeIn(hist[0]),  # axis
                FadeIn(hist[2]),  # -1 label
                FadeIn(hist[3]),  # 0 label
                FadeIn(hist[4]),  # 1 label
                FadeIn(hist[5]),  # tanh label
                run_time=0.5
            )
            self.play(
                LaggedStartMap(GrowFromEdge, hist[1], edge=DOWN, lag_ratio=0.05),
                run_time=1
            )
            self.wait(1)
        self.wait(2)

        rect = SurroundingRectangle(histograms[0], fill_color="#ff0000", color="#ff0000", fill_opacity=0.09).scale(1.05)
        self.play(ShowCreation(rect))

        self.wait(2)
        
        self.play(Transform(rect, SurroundingRectangle(histograms[1], fill_color="#ff0000", color="#ff0000", fill_opacity=0.09).scale(1.05).shift(UP*0.1)))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(histograms[2], fill_color="#ff0000", color="#ff0000", fill_opacity=0.09).scale(1.05)))

        self.play(Transform(rect, SurroundingRectangle(histograms[3], fill_color="#ff0000", color="#ff0000", fill_opacity=0.09).scale(1.05)))
        self.wait(2)

        self.play(FadeOut(rect))


        # Create sigmoid histograms (only bars, reusing existing axes and labels)
        sigmoid_histograms = VGroup()
        
        concentration_factors = [0.04, 0.05, 0.03]
        
        for layer_idx in range(1, len(layers)-1):
            layer = layers[layer_idx]
            
            # Get the existing axis from tanh histograms
            existing_axis = histograms[layer_idx][0]
            
            # Create new sigmoid bars
            bars = VGroup()
            concentration = concentration_factors[layer_idx - 1]
            
            for i in range(num_bins):
                x = 0 + (i + 0.5) * (1 / num_bins)  # Range from 0 to 1
                
                # Gaussian centered at 0.5
                height = np.exp(-((x - 0.5)**2) / (2 * concentration**2)) / (concentration * np.sqrt(2 * np.pi))
                height = height * hist_height * 0.3 * concentration
                
                bar = Rectangle(
                    width=hist_width / num_bins * 0.9,
                    height=height,
                    fill_opacity=0.88,
                    fill_color=YELLOW,
                    stroke_width=1,
                    stroke_color=YELLOW
                )
                
                bar.move_to(existing_axis.get_center())
                bar.shift(RIGHT * ((x - 0.5) * hist_width))
                bar.shift(UP * height/2)
                
                bars.add(bar)
            
            sigmoid_histograms.add(bars)
        
        # Animate: Fade out tanh bars, fade in sigmoid bars, and update labels
        animations = []
        
        for i in range(len(sigmoid_histograms)):
            # Fade out old tanh bars (index 1 in each histogram group)
            animations.append(FadeOut(histograms[i+1][1]))
            # Fade in new sigmoid bars
            animations.append(FadeIn(sigmoid_histograms[i]))
            
            # Transform labels
            # Transform -1 label to 0
            animations.append(Transform(histograms[i+1][2], Text("0", font_size=28).move_to(histograms[i+1][2])))
            # Transform 0 label to 0.5
            animations.append(Transform(histograms[i+1][3], Text("0.5", font_size=28).move_to(histograms[i+1][3])))
            # Transform tanh label to sigma
            animations.append(Transform(histograms[i+1][5], Tex(r"\sigma(z)", font_size=46).move_to(histograms[i+1][5])))
        
        self.play(*animations, run_time=1.5)
        self.wait(2)


        
        for i in range(1,3):
            histograms.remove(histograms[i][1])

        
        self.play(FadeOut(sigmoid_histograms), FadeOut(histograms))


        self.wait(2)

        a = Text("np.random.randn(fan_out * fan_in)").move_to(a).scale(1.57)
        a[10:15].set_color("#ff8808")
        self.play(Write(a))
        self.wait(2)

        z = Tex(r"z_i = \sum_j w_{ij} x_j").move_to(a).scale(1.7).shift(DOWN*0.23)

        self.play(FadeOut(a), FadeIn(z))
        self.wait(2)


        rect = SurroundingRectangle(z[3:], color="#ff0000").scale(1.066)
        self.play(ShowCreation(rect))
        self.wait(2)   

        self.play(FadeOut(rect), FadeOut(z))  
        
        
        saturated_histograms = VGroup()
        
        # INPUT LAYER HISTOGRAM (Same as before)
        input_hist_copy = input_hist.copy()
        saturated_histograms.add(input_hist_copy)

        input_hist_copy.shift(DOWN*0.4)
        # HIDDEN LAYER HISTOGRAMS - Saturated tanh (peaked at -1 and +1)
        saturation_strengths = [0.85, 0.90, 0.93]  # Increasing saturation through layers
        
        for layer_idx in range(1, len(layers)-1):
            layer = layers[layer_idx]
            
            # Create x-axis
            axis_line = Line(
                LEFT * hist_width/2, 
                RIGHT * hist_width/2,
                stroke_width=3,
                color=WHITE
            )
            axis_line.next_to(layer, DOWN, buff=1.71)
            
            # Create histogram bars - bimodal distribution at -1 and +1
            bars = VGroup()
            saturation = saturation_strengths[layer_idx - 1]
            
            for i in range(num_bins):
                x = -1 + (i + 0.5) * (2 / num_bins)
                
                # Bimodal: peaks at -1 and +1, nearly empty in middle
                # Use a mixture of two narrow Gaussians
                left_peak = np.exp(-((x + 1)**2) / (2 * 0.03**2))
                right_peak = np.exp(-((x - 1)**2) / (2 * 0.03**2))
                
                height = (left_peak + right_peak) * saturation * hist_height * 0.4
                
                bar = Rectangle(
                    width=hist_width / num_bins * 0.9,
                    height=height,
                    fill_opacity=0.88,
                    fill_color=YELLOW,
                    stroke_width=1,
                    stroke_color=YELLOW
                )
                
                bar.move_to(axis_line.get_center())
                bar.shift(RIGHT * (x * hist_width/2))
                bar.shift(UP * height/2)
                
                bars.add(bar)
            
            # Add x-axis labels: -1, 0, 1
            label_minus1 = Text("-1", font_size=28).next_to(axis_line.get_start(), DOWN, buff=0.15)
            label_0 = Text("0", font_size=28).next_to(axis_line.get_center(), DOWN, buff=0.15)
            label_1 = Text("1", font_size=28).next_to(axis_line.get_end(), DOWN, buff=0.15)
            
            # Add tanh label
            tanh_label = Tex(r"\tanh(z)", font_size=46).next_to(axis_line, DOWN, buff=0.7)
            
            hist_group = VGroup(axis_line, bars, label_minus1, label_0, label_1, tanh_label)
            saturated_histograms.add(hist_group)
        
        saturated_histograms.shift(UP*0.1)

        saturated_histograms[0][0].shift(UP*0.6)
        saturated_histograms[0][2].shift(UP*0.48)
        saturated_histograms[0][1].shift(UP*0.6)
        # Animate saturated histograms appearing
        self.play(
            FadeIn(saturated_histograms[0][0]),
            FadeIn(saturated_histograms[0][2]),
            run_time=0.5
        )
        self.play(
            LaggedStartMap(GrowFromEdge, saturated_histograms[0][1], edge=DOWN, lag_ratio=0.05),
            run_time=1
        )
        self.wait(1)

        
        for hist in saturated_histograms[1:]:
            self.play(
                FadeIn(hist[0]),
                FadeIn(hist[2]),
                FadeIn(hist[3]),
                FadeIn(hist[4]),
                FadeIn(hist[5]),
                run_time=0.5
            )
            self.play(
                LaggedStartMap(GrowFromEdge, hist[1], edge=DOWN, lag_ratio=0.05),
                run_time=1
            )
            self.wait(0.18)
        self.wait(2)


        self.embed()




        # Create VANISHING gradient histograms for saturated tanh
        vanishing_gradient_histograms = VGroup()
        
        for layer_idx in range(1, len(layers)-1):
            existing_axis = saturated_histograms[layer_idx][0]
            
            bars = VGroup()
            saturation = saturation_strengths[layer_idx - 1]
            
            for i in range(num_bins):
                x = -1 + (i + 0.5) * (2 / num_bins)
                
                # For saturated regions (near ±1), gradient is near 0
                # For middle region (near 0), gradient would be near 1 but there are few neurons
                
                # Bimodal distribution at ±1
                left_peak = np.exp(-((x + 1)**2) / (2 * 0.03**2))
                right_peak = np.exp(-((x - 1)**2) / (2 * 0.03**2))
                
                # Gradient is ~0 at saturation points
                gradient_val = 1 - x**2  # tanh derivative
                
                # Height is high at ±1 (many neurons) but gradient is ~0 there
                height = (left_peak + right_peak) * saturation * hist_height * 0.4 * (gradient_val * 0.1)
                
                bar = Rectangle(
                    width=hist_width / num_bins * 0.9,
                    height=height,
                    fill_opacity=0.88,
                    fill_color=ORANGE,
                    stroke_width=1,
                    stroke_color=ORANGE
                )
                
                bar.move_to(existing_axis.get_center())
                bar.shift(RIGHT * (x * hist_width/2))
                bar.shift(UP * height/2)
                
                bars.add(bar)
            
            vanishing_gradient_histograms.add(bars)
        
        # Transform to gradient histograms
        animations = []
        for i in range(len(vanishing_gradient_histograms)):
            animations.append(Transform(saturated_histograms[i+1][1], vanishing_gradient_histograms[i]))
            animations.append(Transform(
                saturated_histograms[i+1][5], 
                Tex(r"\tanh'(z)", font_size=46).move_to(saturated_histograms[i+1][5])
            ))
        
        self.play(*animations, run_time=1.5)
        self.wait(2)




        # Create SATURATED sigmoid histograms (peaked at 0 and 1)
        saturated_sigmoid_histograms = VGroup()
        
        for layer_idx in range(1, len(layers)-1):
            existing_axis = saturated_histograms[layer_idx][0]
            
            bars = VGroup()
            saturation = saturation_strengths[layer_idx - 1]
            
            for i in range(num_bins):
                x = 0 + (i + 0.5) * (1 / num_bins)  # Range from 0 to 1
                
                # Bimodal: peaks at 0 and 1
                left_peak = np.exp(-((x - 0)**2) / (2 * 0.02**2))
                right_peak = np.exp(-((x - 1)**2) / (2 * 0.02**2))
                
                height = (left_peak + right_peak) * saturation * hist_height * 0.4
                
                bar = Rectangle(
                    width=hist_width / num_bins * 0.9,
                    height=height,
                    fill_opacity=0.88,
                    fill_color=YELLOW,
                    stroke_width=1,
                    stroke_color=YELLOW
                )
                
                bar.move_to(existing_axis.get_center())
                bar.shift(RIGHT * ((x - 0.5) * hist_width))
                bar.shift(UP * height/2)
                
                bars.add(bar)
            
            saturated_sigmoid_histograms.add(bars)
        
        # Animate: Transform to sigmoid
        animations = []
        for i in range(len(saturated_sigmoid_histograms)):
            animations.append(FadeOut(saturated_histograms[i+1][1]))
            animations.append(FadeIn(saturated_sigmoid_histograms[i]))
            animations.append(Transform(saturated_histograms[i+1][2], Text("0", font_size=28).move_to(saturated_histograms[i+1][2])))
            animations.append(Transform(saturated_histograms[i+1][3], Text("0.5", font_size=28).move_to(saturated_histograms[i+1][3])))
            animations.append(Transform(saturated_histograms[i+1][5], Tex(r"\sigma(z)", font_size=46).move_to(saturated_histograms[i+1][5])))
        
        self.play(*animations, run_time=1.5)
        self.wait(2)



        self.play(FadeOut(saturated_histograms), FadeOut(saturated_sigmoid_histograms))
        self.wait(2)

        uniform = Tex(r"w_{ji} \sim \mathcal{U}(-a,\,a)").move_to(a).scale(1.86)
 
        self.play(ShowCreation(uniform))
        self.wait(2)

        self.play(uniform.animate.shift(LEFT*3.5))

        a = Tex(r"Var(w) = \frac{a^2}{3}").scale(1.86).next_to(uniform, RIGHT, buff=0.85)
        self.play(Write(a))
        self.wait(2)

        self.play(FadeOut(a),uniform.animate.shift(RIGHT*3.5) )


        self.play(Transform(uniform, Tex(r"w_{ji} \sim \mathcal{U}\left(-\sqrt{\frac{1}{n}},\,\sqrt{\frac{1}{n}}\right)").scale(1.45).move_to(uniform)))

        self.wait(2)


        self.play(FadeOut(uniform), self.camera.frame.animate.scale(0.92).shift(UP*1.17))
        

        rect = SurroundingRectangle(layers[0], fill_color="#ff0000", color="#ff0000", fill_opacity=0.13).scale(1.1)
        self.play(ShowCreation(rect))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(layers[1], fill_color="#ff0000", color="#ff0000", fill_opacity=0.13).scale(1.1) ))
        self.wait()
        self.play(Transform(rect, SurroundingRectangle(layers[2], fill_color="#ff0000", color="#ff0000", fill_opacity=0.13).scale(1.1) ))
        self.wait()
        self.play(Transform(rect, SurroundingRectangle(layers[3], fill_color="#ff0000", color="#ff0000", fill_opacity=0.13).scale(1.1) ))
        self.wait(2)

        





class ZeroWeightInitialization(Scene):
    def construct(self):
        self.camera.frame.scale(1.1)

        # ===== INPUT LAYER =====
        input_positions = [UP * 1.5, DOWN * 1.5]
        input_nodes, input_labels = [], []
        for i, pos in enumerate(input_positions):
            node = Circle(radius=0.4, color=GREEN, fill_opacity=1, stroke_width=8, stroke_color=GREEN_B)
            node.move_to(LEFT * 4 + pos)
            input_nodes.append(node)
            label = Tex(f"x_{{{i+1}}}").set_color(BLACK).scale(0.9)
            label.move_to(node.get_center())
            input_labels.append(label)

        # ===== HIDDEN LAYER =====
        hidden_positions = [UP * 1.5, DOWN * 1.5]
        hidden_nodes, hidden_labels = [], []
        for i, pos in enumerate(hidden_positions):
            node = Circle(radius=0.5, color=BLUE_C, fill_opacity=1, stroke_width=8, stroke_color=BLUE_B)
            node.move_to(ORIGIN + pos)
            hidden_nodes.append(node)
            label = Tex(f"a^{{(1)}}_{{{i+1}}}").set_color(BLACK).scale(0.9).set_z_index(1)
            label.move_to(node.get_center())
            hidden_labels.append(label)

        # ===== OUTPUT LAYER =====
        output_node = Circle(radius=0.6, color=BLUE_C, fill_opacity=1, stroke_width=8, stroke_color=BLUE_B)
        output_node.move_to(RIGHT * 4)
        output_label = Tex("a^{(2)}_1").set_color(BLACK).scale(1.0).set_z_index(1)
        output_label.move_to(output_node.get_center())

        # ===== CONNECTIONS + WEIGHT LABELS =====
        weights = []
        w_labels = []
        w_names = ["w_1", "w_2", "w_3", "w_4"]
        w_index = 0

        # Input → Hidden connections
        for i, inp in enumerate(input_nodes):
            for j, hid in enumerate(hidden_nodes):
                line = Line(inp.get_center(), hid.get_center(), color=GREY_B, stroke_opacity=0.9)
                line.set_z_index(-1)
                weights.append(line)

                midpoint = (inp.get_center() + hid.get_center()) / 2
                offset = ORIGIN
                if not (i == j):
                    offset = RIGHT * 0.3 if j == 0 else LEFT * 0.3

                w_label = Tex(w_names[w_index]).scale(1.1)
                w_label.move_to(midpoint + offset)
                w_labels.append(w_label)
                w_index += 1

        # ===== HIDDEN → OUTPUT CONNECTIONS =====
        hidden_to_output = []
        w5 = Tex("w_5").scale(1.1)
        w6 = Tex("w_6").scale(1.1)

        for j, hid in enumerate(hidden_nodes):
            line = Line(hid.get_center(), output_node.get_center(), color=GREY_B, stroke_opacity=0.9)
            line.set_z_index(-1)
            hidden_to_output.append(line)

        # Position w5, w6 near connecting lines
        mid1 = (hidden_nodes[0].get_center() + output_node.get_center()) / 2
        mid2 = (hidden_nodes[1].get_center() + output_node.get_center()) / 2
        w5.move_to(mid1 + UP * 0.4 + LEFT * 0.3)
        w6.move_to(mid2 + DOWN * 0.47 + LEFT * 0.3)
        w_labels.extend([w5, w6])

        # ===== FINE ADJUSTMENTS =====
        w_labels[0].shift(UP * 0.3)
        w_labels[3].shift(DOWN * 0.3)
        w_labels[1].shift(UP * 0.7 + RIGHT * 0.6)
        w_labels[2].shift(DOWN * 0.83 + RIGHT * 0.24)

        # ===== BIASES =====
        bias_arrows, bias_labels = [], []

        # Hidden layer biases
        b1_arrow = Arrow(UP * 0.8, ORIGIN, buff=0, color=GREY_B, stroke_width=3)
        b1_arrow.next_to(hidden_nodes[0], UP, buff=0.14)
        b1_label = Tex(r"b^{(1)}_1").scale(1.1)
        b1_label.next_to(b1_arrow, UP, buff=0.22)

        b2_arrow = Arrow(DOWN * 0.8, ORIGIN, buff=0, color=GREY_B, stroke_width=3)
        b2_arrow.next_to(hidden_nodes[1], DOWN, buff=0.14)
        b2_label = Tex(r"b^{(1)}_2").scale(1.1)
        b2_label.next_to(b2_arrow, DOWN, buff=0.22)

        # Output layer bias
        b3_arrow = Arrow(UP * 0.8, ORIGIN, buff=0, color=GREY_B, stroke_width=3)
        b3_arrow.next_to(output_node, UP, buff=0.14)
        b3_label = Tex(r"b^{(2)}_1").scale(1.1)
        b3_label.next_to(b3_arrow, UP, buff=0.22)

        bias_arrows.extend([b1_arrow, b2_arrow, b3_arrow])
        bias_labels.extend([b1_label, b2_label, b3_label])

        # ===== ANIMATIONS =====
        self.play(
            *[GrowFromCenter(i) for i in input_nodes + hidden_nodes + [output_node]],
            *[GrowFromCenter(j) for j in input_labels + hidden_labels + [output_label]],
            run_time=1
        )
        self.play(*[ShowCreation(i) for i in weights + hidden_to_output], run_time=2)
        self.play(*[GrowFromCenter(k) for k in w_labels], run_time=1)
        self.play(*[GrowArrow(b) for b in bias_arrows], *[FadeIn(lbl) for lbl in bias_labels], run_time=1)

        # ===== OUTPUT ARROW =====
        arrow = Arrow(output_node.get_right() + RIGHT * 0.27, RIGHT * 6, buff=0, stroke_width=3, color=GREY_B)
        self.play(GrowArrow(arrow), run_time=1)
        y_hat = Tex(r"\hat{y}").set_color(WHITE).scale(1.55)
        y_hat.next_to(arrow, RIGHT, buff=0.22)
        self.play(GrowFromCenter(y_hat), self.camera.frame.animate.shift(RIGHT), run_time=1)
        self.wait(2)

        # ===== PULSE HELPERS =====
        def create_glow(center_point, radius=0.12, color=PURE_RED, intensity=0.4):
            g = VGroup()
            for i in range(15):
                rr = radius * (1 + 0.12 * i)
                op = intensity * (1 - i / 15)
                glow_circle = Circle(radius=rr, stroke_opacity=0, fill_color=color, fill_opacity=op)
                glow_circle.move_to(center_point)
                g.add(glow_circle)
            return g

        def create_pulse(point, color=PURE_RED, radius=0.10):
            dot = Dot(radius=radius, color=color, fill_opacity=1).move_to(point)
            glow = create_glow(point, radius=radius * 0.8, color=color, intensity=0.5)
            return VGroup(glow, dot)

        def pulse_stage(lines, extra_lines=None, color=PURE_RED, run_time=1.2):
            """Animate pulses along lines + optional bias arrows (bias → node center)."""
            pulses, anims = [], []
            all_lines = lines + (extra_lines if extra_lines else [])

            for ln in all_lines:
                start = ln.get_start()

                # Bias arrows go to nearest node center
                if isinstance(ln, Arrow):
                    possible_nodes = input_nodes + hidden_nodes + [output_node]
                    end = min(possible_nodes, key=lambda n: np.linalg.norm(n.get_center() - ln.get_end())).get_center()
                else:
                    end = ln.get_end()

                p = create_pulse(start, color=color)
                pulses.append(p)
                self.add(p)
                anims.append(p.animate.move_to(end))

            if anims:
                self.play(*anims, run_time=run_time)
                self.play(*[FadeOut(p) for p in pulses], run_time=0.25)

        # ===== PULSES START (Simultaneous bias + inputs) =====
        self.wait(0.5)
        self.play(self.camera.frame.animate.scale(1.2).shift(DOWN*0.7))
        pulse_stage(weights, extra_lines=[b1_arrow, b2_arrow], color=PURE_RED, run_time=1.5)

        a = Tex("a_1^{(1)} = f(w_1 x_1 + w_2 x_2 + b_1^{(1)})")
        b = Tex("a_2^{(1)} = f(w_3 x_1 + w_4 x_2 + b_2^{(1)})")

        a.next_to(bias_labels[1], DOWN, buff=0.6).scale(1.33).shift(LEFT*3.5)
        b.next_to(a, RIGHT, buff=1.95).scale(1.33)

        self.play(
            TransformFromCopy(hidden_labels[0], a[:5]),
            TransformFromCopy(hidden_labels[1], b[:5]),
        )
        self.wait()

        self.play(FadeIn(a[5:8]), FadeIn(a[-1]), FadeIn(b[5:8]), FadeIn(b[-1]))
        self.wait()

        self.play(
            TransformFromCopy(w_labels[0], a[8:10]),
            TransformFromCopy(w_labels[1], a[13:15]),
            TransformFromCopy(w_labels[2], b[8:10]),
            TransformFromCopy(w_labels[3], b[13:15]),
            TransformFromCopy(input_labels[0], a[10:12]),
            TransformFromCopy(input_labels[1], a[15:17]),
            TransformFromCopy(input_labels[0], b[10:12]),
            TransformFromCopy(input_labels[1], b[15:17]),
            TransformFromCopy(bias_labels[0], a[-6:-1]),
            TransformFromCopy(bias_labels[1], b[-6:-1]),
            FadeIn(a[12:13]), FadeIn(a[17:18]), FadeIn(b[12:13]), FadeIn(b[17:18]),
            run_time=2
        )

        self.wait(2)


        pulse_stage(hidden_to_output, extra_lines=[b3_arrow], color=PURE_RED, run_time=1.5)
        self.wait(0.5)

        c = Tex(r"\hat{y} = a_1^{(2)} = f(w_5 a_1^{(1)} + w_6 a_2^{(1)} + b_1^{(2)})")
        c.next_to(b, DOWN, buff=1.0).scale(1.33).move_to(VGroup(a, b)).scale(1.15)

        self.play(
            FadeOut(a), FadeOut(b), 
            TransformFromCopy(y_hat, c[:2]),
            FadeIn(c[2]),
            TransformFromCopy(output_label, c[3:8]),
        
        )

        self.wait(2)

        self.play(
            FadeIn(c[8])
        )

        self.play(FadeIn(c[9:11]), FadeIn(c[-1])) 

        self.play(
            TransformFromCopy(w5, c[11:13]),
            TransformFromCopy(w6, c[19:21]),
            TransformFromCopy(hidden_labels[0], c[13:18]),
            TransformFromCopy(hidden_labels[1], c[21:26]),
            TransformFromCopy(bias_labels[2], c[-6:-1]),
            FadeIn(c[18]), FadeIn(c[26]),
            run_time=2
        )

        self.wait(2)
        
        d = Tex(r"\hat{y} = f(w_5 f(w_1 x_1 + w_2 x_2 + b_1^{(1)}) + w_6 f(w_3 x_1 + w_4 x_2 + b_2^{(1)}) + b_1^{(2)})").move_to(c).scale(1.12)
        self.play(ReplacementTransform(c, d), run_time=1)

        self.wait(2)

        zero_labels = []
        all_symbols = w_labels + bias_labels
        
        # Create zero versions at the same positions
        for lbl in all_symbols:
            zero_tex = Text("0").scale(1.1)
            zero_tex.move_to(lbl.get_center())
            zero_labels.append(zero_tex)
        
        # Group both for easier animation
        zero_group = VGroup(*zero_labels)
        original_group = VGroup(*all_symbols)
        
        # ===== Fade original labels out, fade zeros in =====
        self.play(
            FadeOut(original_group, shift=UP*0.05),
            FadeIn(zero_group, shift=UP*0.05),
            run_time=1.2
        )
        self.wait(2)
                 
        self.camera.frame.save_state()
        self.wait(2)

        self.play(Transform(d, Tex(r"\hat{y} = f(0 \cdot f(0 \cdot x_1 + 0 \cdot x_2 + 0) + 0 \cdot f(0 \cdot x_1 + 0 \cdot x_2 + 0) + 0)").move_to(d).scale(1.12)))
        
        self.wait(2)
        self.play(Transform(d, Tex(r"\hat{y} = f(0)").move_to(d).scale(1.82)))
        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT*16), d.animate.shift(RIGHT*16+UP*4.5))
        self.wait(2)

        self.play(Transform(d, Tex(r"f(0) \ = \ ReLU(0) \ = \ 0").move_to(d).scale(1.82)))

        self.wait(2)

        self.play(d.animate.shift(UP*1.1))

        e = Tex(r"f'(0) \ = \ ReLU'(0) \ = \ 0").move_to(d).scale(1.82).shift(DOWN*2)
        self.play(Write(e))

        self.wait(2)

        a1 = Tex(r"a^{(1)}_1 = f(w_1 x_1 + w_2 x_2 + b^{(1)}_1)")
        a1.move_to(d).scale(1.85).shift(DOWN*0.3565)

        a2 = Tex(r"a^{(1)}_2 = f(w_3 x_1 + w_4 x_2 + b^{(1)}_2)")
        a2.next_to(a1, DOWN, buff=0.97).scale(1.85)

        self.play(
            FadeIn(VGroup(a1, a2)),
            FadeOut(VGroup(d, e)),
        )

        self.wait(2)

        self.play(
            Transform(a1, Tex(r"a^{(1)}_1 = f(0 \cdot x_1 + 0 \cdot x_2 + 0)").move_to(a1).scale(1.85)),
            Transform(a2, Tex(r"a^{(1)}_2 = f(0 \cdot x_1 + 0 \cdot x_2 + 0)").move_to(a2).scale(1.85)),
        )

        self.wait(2)

        self.play(
            Transform(a1, Tex(r"a^{(1)}_1 = f(0) = 0").move_to(a1).scale(1.85)),
            Transform(a2, Tex(r"a^{(1)}_2 = f(0) = 0").move_to(a2).scale(1.85)),
        )

        self.wait(2)


        a = Tex(r"\frac{\partial L}{\partial w_5} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z^{(2)}} \cdot \frac{\partial z^{(2)}}{\partial w_5}").scale(1.32)

        a.move_to(VGroup(a1, a2)).scale(1.62)

        self.play(FadeOut(VGroup(a1, a2)), FadeIn(a))

        self.wait(2)

        temp = Tex(r"\frac{\partial L}{\partial w_5} = \frac{\partial L}{\partial \hat{y}} \cdot f'(z^{(2)}) \cdot a_1^{(1)}").scale(1.32*1.52)
        temp.move_to(a)
        self.play(Transform(a, temp))
        self.wait(2)



        brace = Brace(a[-16:], DOWN, buff=0.53).set_color(YELLOW)
        self.play(GrowFromCenter(brace))
        self.wait(2)

        temp = Tex(r"\frac{\partial L}{\partial w_5} = \frac{\partial L}{\partial \hat{y}} \cdot f'(0) \cdot f(0)").scale(1.32*1.52)
        temp.move_to(a)
        self.play(Transform(a, temp))
        self.play(FadeOut(brace))
        self.wait(2)

        temp = Tex(r"\frac{\partial L}{\partial w_5} = \frac{\partial L}{\partial \hat{y}} \cdot ReLU'(0) \cdot ReLU(0)").scale(1.32*1.45)
        temp.move_to(a)
        self.play(Transform(a, temp))        
        self.wait(2)

        self.play(Transform(a, Tex(r"\frac{\partial L}{\partial w_5} = \frac{\partial L}{\partial \hat{y}} \cdot 0 \cdot 0 = 0").move_to(a).scale(1.32*1.45)))
        self.wait(2)

        self.play(a.animate.shift(UP*1.699))

        b = Tex(r"w_5 \rightarrow w_5 - \alpha \cdot \frac{\partial L}{\partial w_5}").move_to(a).scale(1.32*1.2).shift(DOWN*2)
        b.shift(DOWN*1.5).scale(1.55).shift(DOWN*0.3333)
        self.play(Write(b))
        self.wait(2)

        self.play(Transform(b, Tex(r"w_5 \rightarrow w_5 - \alpha \cdot 0").move_to(b).scale(1.32*1.2).scale(1.55)), run_time=0.5)
        self.wait(2)

        self.play(Transform(b, Tex(r"w_5 \rightarrow w_5").move_to(b).scale(1.32*1.2).scale(1.85)), run_time=0.5)
        rect = SurroundingRectangle(b, color=YELLOW, buff=0.2).scale(1.1)
        self.play(ShowCreation(rect))
        text = Text("No Update!", ).scale(2).next_to(rect, DOWN, buff=0.97).set_color(RED_B)
        self.play(Write(text))
        self.wait(2)

        c = Tex(r"\frac{\partial L}{\partial w_1} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z^{(2)}} \cdot \frac{\partial z^{(2)}}{\partial a_1^{(1)}} \cdot \frac{\partial a_1^{(1)}}{\partial z_1^{(1)}} \cdot \frac{\partial z_1^{(1)}}{\partial w_1}")
        c.move_to(VGroup(a, b)).scale(1.77).shift(DOWN*0.3299)
        self.play(FadeOut(VGroup(a, b, rect, text)), FadeIn(c))

        self.wait(2)

        temp = Tex(r"\frac{\partial L}{\partial w_1} = \frac{\partial L}{\partial \hat{y}} \cdot f'(z^{(2)}) \cdot w_5 \cdot f'(z_1^{(1)}) \cdot x_1")
        temp.move_to(c).scale(1.77)
        self.play(Transform(c, temp))
        self.wait(2)

        self.play(Transform(c, Tex(r"\frac{\partial L}{\partial w_1} = 0").move_to(c).scale(2.5)))
        self.wait(2)


        a = Tex(r"\hat{y} = f(0)").move_to(c).scale(2.53)
        self.play(FadeOut(c), FadeIn(a))
        self.wait(2)


        self.play(Transform(a, Tex(r"f(0)  = \sigma (0)  =  0.5").move_to(a).scale(2)))

        self.wait(2)

        self.play(a.animate.shift(UP*1.1))

        e = Tex(r"f'(0)  = \sigma '(0)  =  0.25").move_to(d).scale(2).shift(DOWN*2.4)
        self.play(Write(e))


        self.wait(2)

        b = Tex("a_1^{(1)} = \sigma(w_1 x_1 + w_2 x_2 + b_1^{(1)})").move_to(a).scale(1.82)

        c = Tex("a_2^{(1)} = \sigma(w_3 x_1 + w_4 x_2 + b_2^{(1)})").move_to(e).scale(1.82)

        self.play(FadeOut(a), FadeOut(e), FadeIn(b), FadeIn(c))
        self.wait(2)

        self.play(Transform(b, Tex("a_1^{(1)} = \sigma(0 \cdot x_1 + 0 \cdot x_2 + 0)").move_to(b).scale(1.82)),
                  Transform(c, Tex("a_2^{(1)} = \sigma(0 \cdot x_1 + 0 \cdot x_2 + 0)").move_to(c).scale(1.82)))
        self.wait(2)

        self.play(Transform(b, Tex("a_1^{(1)} = \sigma(0) = 0.5").move_to(b).scale(1.82)),
                  Transform(c, Tex("a_2^{(1)} = \sigma(0) = 0.5").move_to(c).scale(1.82)))
        self.wait(2)

        a = Tex(r"\frac{\partial L}{\partial w_5} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z^{(2)}} \cdot \frac{\partial z^{(2)}}{\partial w_5}")
        a.move_to(VGroup(b, c)).scale(1.62).shift(UP*1.54)

        a1 = Tex(r"\frac{\partial L}{\partial w_6} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z^{(2)}} \cdot \frac{\partial z^{(2)}}{\partial w_6}")
        a1.move_to(a).shift(DOWN*3.2).scale(1.62)

        self.play(FadeOut(VGroup(b, c)), FadeIn(a), FadeIn(a1))

        self.wait(2)

        self.play(
            Transform(a, Tex(r"\frac{\partial L}{\partial w_5} = \frac{\partial L}{\partial \hat{y}} \cdot \sigma'(z^{(2)}) \cdot a_1^{(1)}").move_to(a).scale(1.62)),
            Transform(a1, Tex(r"\frac{\partial L}{\partial w_6} = \frac{\partial L}{\partial \hat{y}} \cdot \sigma'(z^{(2)}) \cdot a_2^{(1)}").move_to(a1).scale(1.62)),
        )

        self.wait(2)

        self.play(
            Transform(a, Tex(r"\frac{\partial L}{\partial w_5} = \frac{\partial L}{\partial \hat{y}} \cdot 0.25 \cdot 0.5").move_to(a).scale(1.62)),
            Transform(a1, Tex(r"\frac{\partial L}{\partial w_6} = \frac{\partial L}{\partial \hat{y}} \cdot 0.25 \cdot 0.5").move_to(a1).scale(1.62)),
        )

        self.wait(2)

        rect1 = SurroundingRectangle(a, color=YELLOW, buff=0.2).scale(1.1)
        rect2 = SurroundingRectangle(a1, color=YELLOW, buff=0.2).scale(1.1)
        self.play(ShowCreation(rect1), ShowCreation(rect2))
        
        
        self.wait(2)


        self.play(self.camera.frame.animate.restore().scale(0.83).shift(UP*0.65))
        self.wait(2)

        self.play(
            FadeOut(zero_group, shift=DOWN*0.05),
            FadeIn(original_group, shift=DOWN*0.05),
            run_time=1.2
        )

        temp_a = Circle(stroke_width=6).move_to(w5).set_color("#ff0000").scale(0.5)
        temp_b = Circle(stroke_width=6).move_to(w6).set_color("#ff0000").scale(0.5)
        self.play(
            ShowCreation(temp_a),
            ShowCreation(temp_b),
        )

        self.play(
            w_labels[4].animate.set_color(YELLOW),
            hidden_to_output[0].animate.set_color(YELLOW),
            w_labels[5].animate.set_color(YELLOW),
            hidden_to_output[1].animate.set_color(YELLOW),
            run_time=1
        )

        self.wait(2)

        self.camera.frame.save_state()


        self.play(self.camera.frame.animate.scale(1/0.83).shift(RIGHT*16+DOWN*0.72), FadeOut(VGroup(temp_a, temp_b)))
        self.wait(2)

        b = Tex(r"\frac{\partial L}{\partial w_1} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z^{(2)}} \cdot \frac{\partial z^{(2)}}{\partial a^{(1)}_1} \cdot \frac{\partial a^{(1)}_1}{\partial z^{(1)}_1} \cdot \frac{\partial z^{(1)}_1}{\partial w_1}")
        b.move_to(VGroup(a)).scale(1.27).shift(UP*1.733)

        c = Tex(r"\frac{\partial L}{\partial w_2} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z^{(2)}} \cdot \frac{\partial z^{(2)}}{\partial a^{(1)}_1} \cdot \frac{\partial a^{(1)}_1}{\partial z^{(1)}_1} \cdot \frac{\partial z^{(1)}_1}{\partial w_2}")
        c.move_to(b).scale(1.27).shift(DOWN*2.4)

        d = Tex(r"\frac{\partial L}{\partial w_3} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z^{(2)}} \cdot \frac{\partial z^{(2)}}{\partial a^{(1)}_2} \cdot \frac{\partial a^{(1)}_2}{\partial z^{(1)}_2} \cdot \frac{\partial z^{(1)}_2}{\partial w_3}")
        d.move_to(c).scale(1.27).shift(DOWN*2.4)

        e = Tex(r"\frac{\partial L}{\partial w_4} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z^{(2)}} \cdot \frac{\partial z^{(2)}}{\partial a^{(1)}_2} \cdot \frac{\partial a^{(1)}_2}{\partial z^{(1)}_2} \cdot \frac{\partial z^{(1)}_2}{\partial w_4}")
        e.move_to(d).scale(1.27).shift(DOWN*2.4)

        self.play(FadeOut(VGroup(a, a1, rect1, rect2)), FadeIn(b), FadeIn(c), FadeIn(d), FadeIn(e))

        self.wait(2)

        self.play(
            Transform(b, Tex(r"\frac{\partial L}{\partial w_1} = \frac{\partial L}{\partial \hat{y}} \cdot \sigma'(z^{(2)}) \cdot w_5 \cdot \sigma'(z^{(1)}_1) \cdot x_1").move_to(b).scale(1.27)),
            Transform(c, Tex(r"\frac{\partial L}{\partial w_2} = \frac{\partial L}{\partial \hat{y}} \cdot \sigma'(z^{(2)}) \cdot w_5 \cdot \sigma'(z^{(1)}_1) \cdot x_2").move_to(c).scale(1.27)),
            Transform(d, Tex(r"\frac{\partial L}{\partial w_3} = \frac{\partial L}{\partial \hat{y}} \cdot \sigma'(z^{(2)}) \cdot w_6 \cdot \sigma'(z^{(1)}_2) \cdot x_1").move_to(d).scale(1.27)),
            Transform(e, Tex(r"\frac{\partial L}{\partial w_4} = \frac{\partial L}{\partial \hat{y}} \cdot \sigma'(z^{(2)}) \cdot w_6 \cdot \sigma'(z^{(1)}_2) \cdot x_2").move_to(e).scale(1.27)),
        )

        self.wait(2)

        rect1 = SurroundingRectangle(b, color=YELLOW, buff=0.2).scale(1.1)
        rect2 = SurroundingRectangle(d, color=YELLOW, buff=0.2  ).scale(1.1)
        
        self.play(ShowCreation(rect1), ShowCreation(rect2))
        self.wait(2)

        self.play(
            Transform(rect1, SurroundingRectangle(c, color=YELLOW, buff=0.2).scale(1.1)),
            Transform(rect2, SurroundingRectangle(e, color=YELLOW, buff=0.2  ).scale(1.1)),
        )

        self.wait(2)

        self.play(
            FadeOut(VGroup(b, c, d, e, rect1, rect2)),
            self.camera.frame.animate.restore()       
        )

        temp_a = Circle().move_to(w_labels[0]).set_color("#ff0000").scale(0.5)
        temp_b = Circle().move_to(w_labels[2]).set_color("#ff0000").scale(0.5)

        self.play(
            ShowCreation(temp_a),
            ShowCreation(temp_b),
        )   
        self.play(
            w_labels[0].animate.set_color(PURPLE_C),
            weights[0].animate.set_color(PURPLE_C),
            w_labels[2].animate.set_color(PURPLE_C),
            weights[1].animate.set_color(PURPLE_C),
            run_time=1
        )
        self.wait(2)

        self.play(
            Transform(temp_a, Circle().move_to(w_labels[1]).set_color("#ff0000").scale(0.5)),
            Transform(temp_b, Circle().move_to(w_labels[3]).set_color("#ff0000").scale(0.5)),
        )

        MAROON = "#EF4713"
        self.play(
            w_labels[1].animate.set_color(MAROON),
            weights[2].animate.set_color(MAROON),
            w_labels[3].animate.set_color(MAROON),
            weights[3].animate.set_color(MAROON),
            run_time=1
        )
        self.wait(2)

        self.play(self.camera.frame.animate.shift(UP*0.149), Uncreate(temp_a), Uncreate(temp_b))


        self.play(Indicate(hidden_nodes[0], color="#ff0000"), Indicate(hidden_nodes[1], color="#ff0000"), run_time=0.5)
        self.play(Indicate(hidden_nodes[0], color="#ff0000"), Indicate(hidden_nodes[1], color="#ff0000"), run_time=0.5)
        self.play(Indicate(hidden_nodes[0], color="#ff0000"), Indicate(hidden_nodes[1], color="#ff0000"), run_time=0.5)
        self.play(Indicate(hidden_nodes[0], color="#ff0000"), Indicate(hidden_nodes[1], color="#ff0000"), run_time=0.5)
        
        self.wait(2)

        self.play(FadeOut(VGroup(bias_labels, )), FadeOut(w5), FadeOut(w6), FadeOut(b1_arrow), FadeOut(b2_arrow), FadeOut(b3_arrow), FadeOut(w_labels[0]), FadeOut(w_labels[1]), FadeOut(w_labels[2]), FadeOut(w_labels[3]), )
    
        self.wait(2)

        c = hidden_nodes[0].copy()
        d = hidden_labels[0].copy()

        c.shift(DOWN*1.54)
        d.shift(DOWN*1.54)

        w1 = Line(input_nodes[0].get_center(), c.get_center(), color=GREY_B, stroke_opacity=0.9).set_color(PURPLE_B).set_z_index(-1)
        w2 = Line(input_nodes[1].get_center(), c.get_center(), color=GREY_B, stroke_opacity=0.9).set_color("#ff0000").set_z_index(-1)
        w3 = Line(c.get_center(), output_node.get_center(), color=GREY_B, stroke_opacity=0.9).set_color(YELLOW_C).set_z_index(-1)

        self.play(
            ReplacementTransform(hidden_nodes[0], c),
            ReplacementTransform(hidden_labels[0], d),
            ReplacementTransform(hidden_nodes[1], c),
            ReplacementTransform(hidden_labels[1], d),
            ReplacementTransform(weights[0], w1),
            ReplacementTransform(weights[1], w1),
            ReplacementTransform(weights[2], w2),
            ReplacementTransform(weights[3], w2),
            ReplacementTransform(hidden_to_output[0], w3),
            ReplacementTransform(hidden_to_output[1], w3)
        )


        self.wait(2)

        a = Text("Symmetry breaking problem", weight=BOLD)
        a.next_to(c, DOWN, buff=1.2).scale(1.65).set_color(RED_B).shift(DOWN*1.23+RIGHT*1.4)

        self.play(self.camera.frame.animate.shift(DOWN*1.16), Write(a))
        self.wait(3)


class NonZeroConstantWeightInitialization(Scene):
    def construct(self):
        self.camera.frame.scale(1.1)

        # ===== INPUT LAYER =====
        input_positions = [UP * 1.5, DOWN * 1.5]
        input_nodes, input_labels = [], []
        for i, pos in enumerate(input_positions):
            node = Circle(radius=0.4, color=GREEN, fill_opacity=1, stroke_width=8, stroke_color=GREEN_B)
            node.move_to(LEFT * 4 + pos)
            input_nodes.append(node)
            label = Tex(f"x_{{{i+1}}}").set_color(BLACK).scale(0.9)
            label.move_to(node.get_center())
            input_labels.append(label)

        # ===== HIDDEN LAYER =====
        hidden_positions = [UP * 1.5, DOWN * 1.5]
        hidden_nodes, hidden_labels = [], []
        for i, pos in enumerate(hidden_positions):
            node = Circle(radius=0.5, color=BLUE_C, fill_opacity=1, stroke_width=8, stroke_color=BLUE_B)
            node.move_to(ORIGIN + pos)
            hidden_nodes.append(node)
            label = Tex(f"a^{{(1)}}_{{{i+1}}}").set_color(BLACK).scale(0.9).set_z_index(1)
            label.move_to(node.get_center())
            hidden_labels.append(label)

        # ===== OUTPUT LAYER =====
        output_node = Circle(radius=0.6, color=BLUE_C, fill_opacity=1, stroke_width=8, stroke_color=BLUE_B)
        output_node.move_to(RIGHT * 4)
        output_label = Tex("a^{(2)}_1").set_color(BLACK).scale(1.0).set_z_index(1)
        output_label.move_to(output_node.get_center())

        # ===== CONNECTIONS + WEIGHT LABELS =====
        weights = []
        w_labels = []
        w_names = ["w_1", "w_2", "w_3", "w_4"]
        w_index = 0

        # Input → Hidden connections
        for i, inp in enumerate(input_nodes):
            for j, hid in enumerate(hidden_nodes):
                line = Line(inp.get_center(), hid.get_center(), color=GREY_B, stroke_opacity=0.9)
                line.set_z_index(-1)
                weights.append(line)

                midpoint = (inp.get_center() + hid.get_center()) / 2
                offset = ORIGIN
                if not (i == j):
                    offset = RIGHT * 0.3 if j == 0 else LEFT * 0.3

                w_label = Tex(w_names[w_index]).scale(1.1)
                w_label.move_to(midpoint + offset)
                w_labels.append(w_label)
                w_index += 1

        # ===== HIDDEN → OUTPUT CONNECTIONS =====
        hidden_to_output = []
        w5 = Tex("w_5").scale(1.1)
        w6 = Tex("w_6").scale(1.1)

        for j, hid in enumerate(hidden_nodes):
            line = Line(hid.get_center(), output_node.get_center(), color=GREY_B, stroke_opacity=0.9)
            line.set_z_index(-1)
            hidden_to_output.append(line)

        # Position w5, w6 near connecting lines
        mid1 = (hidden_nodes[0].get_center() + output_node.get_center()) / 2
        mid2 = (hidden_nodes[1].get_center() + output_node.get_center()) / 2
        w5.move_to(mid1 + UP * 0.4 + LEFT * 0.3)
        w6.move_to(mid2 + DOWN * 0.47 + LEFT * 0.3)
        w_labels.extend([w5, w6])

        # ===== FINE ADJUSTMENTS =====
        w_labels[0].shift(UP * 0.3)
        w_labels[3].shift(DOWN * 0.3)
        w_labels[1].shift(UP * 0.7 + RIGHT * 0.6)
        w_labels[2].shift(DOWN * 0.83 + RIGHT * 0.24)

        # ===== BIASES =====
        bias_arrows, bias_labels = [], []

        # Hidden layer biases
        b1_arrow = Arrow(UP * 0.8, ORIGIN, buff=0, color=GREY_B, stroke_width=3)
        b1_arrow.next_to(hidden_nodes[0], UP, buff=0.14)
        b1_label = Tex(r"b^{(1)}_1").scale(1.1)
        b1_label.next_to(b1_arrow, UP, buff=0.22)

        b2_arrow = Arrow(DOWN * 0.8, ORIGIN, buff=0, color=GREY_B, stroke_width=3)
        b2_arrow.next_to(hidden_nodes[1], DOWN, buff=0.14)
        b2_label = Tex(r"b^{(1)}_2").scale(1.1)
        b2_label.next_to(b2_arrow, DOWN, buff=0.22)

        # Output layer bias
        b3_arrow = Arrow(UP * 0.8, ORIGIN, buff=0, color=GREY_B, stroke_width=3)
        b3_arrow.next_to(output_node, UP, buff=0.14)
        b3_label = Tex(r"b^{(2)}_1").scale(1.1)
        b3_label.next_to(b3_arrow, UP, buff=0.22)

        bias_arrows.extend([b1_arrow, b2_arrow, b3_arrow])
        bias_labels.extend([b1_label, b2_label, b3_label])

        # ===== ANIMATIONS =====
        self.play(
            *[GrowFromCenter(i) for i in input_nodes + hidden_nodes + [output_node]],
            *[GrowFromCenter(j) for j in input_labels + hidden_labels + [output_label]],
            run_time=1
        )
        self.play(*[ShowCreation(i) for i in weights + hidden_to_output], run_time=2)
        self.play(*[GrowFromCenter(k) for k in w_labels], run_time=1)
        self.play(*[GrowArrow(b) for b in bias_arrows], *[FadeIn(lbl) for lbl in bias_labels], run_time=1)

        # ===== OUTPUT ARROW =====
        arrow = Arrow(output_node.get_right() + RIGHT * 0.27, RIGHT * 6, buff=0, stroke_width=3, color=GREY_B)
        self.play(GrowArrow(arrow), run_time=1)
        y_hat = Tex(r"\hat{y}").set_color(WHITE).scale(1.55)
        y_hat.next_to(arrow, RIGHT, buff=0.22)
        self.play(GrowFromCenter(y_hat), self.camera.frame.animate.shift(RIGHT), run_time=1)
        self.wait(2)

        # ===== PULSE HELPERS =====
        def create_glow(center_point, radius=0.12, color=PURE_RED, intensity=0.4):
            g = VGroup()
            for i in range(15):
                rr = radius * (1 + 0.12 * i)
                op = intensity * (1 - i / 15)
                glow_circle = Circle(radius=rr, stroke_opacity=0, fill_color=color, fill_opacity=op)
                glow_circle.move_to(center_point)
                g.add(glow_circle)
            return g

        def create_pulse(point, color=PURE_RED, radius=0.10):
            dot = Dot(radius=radius, color=color, fill_opacity=1).move_to(point)
            glow = create_glow(point, radius=radius * 0.8, color=color, intensity=0.5)
            return VGroup(glow, dot)

        def pulse_stage(lines, extra_lines=None, color=PURE_RED, run_time=1.2):
            """Animate pulses along lines + optional bias arrows (bias → node center)."""
            pulses, anims = [], []
            all_lines = lines + (extra_lines if extra_lines else [])

            for ln in all_lines:
                start = ln.get_start()

                # Bias arrows go to nearest node center
                if isinstance(ln, Arrow):
                    possible_nodes = input_nodes + hidden_nodes + [output_node]
                    end = min(possible_nodes, key=lambda n: np.linalg.norm(n.get_center() - ln.get_end())).get_center()
                else:
                    end = ln.get_end()

                p = create_pulse(start, color=color)
                pulses.append(p)
                self.add(p)
                anims.append(p.animate.move_to(end))

            if anims:
                self.play(*anims, run_time=run_time)
                self.play(*[FadeOut(p) for p in pulses], run_time=0.25)

        # ===== PULSES START (Simultaneous bias + inputs) =====
        self.wait(0.5)
        self.play(self.camera.frame.animate.scale(1.2).shift(DOWN*0.7))
        pulse_stage(weights, extra_lines=[b1_arrow, b2_arrow], color=PURE_RED, run_time=1.5)

        a = Tex("a_1^{(1)} = f(w_1 x_1 + w_2 x_2 + b_1^{(1)})")
        b = Tex("a_2^{(1)} = f(w_3 x_1 + w_4 x_2 + b_2^{(1)})")

        a.next_to(bias_labels[1], DOWN, buff=0.6).scale(1.33).shift(LEFT*3.5)
        b.next_to(a, RIGHT, buff=1.95).scale(1.33)

        self.play(
            TransformFromCopy(hidden_labels[0], a[:5]),
            TransformFromCopy(hidden_labels[1], b[:5]),
        )
        self.wait()

        self.play(FadeIn(a[5:8]), FadeIn(a[-1]), FadeIn(b[5:8]), FadeIn(b[-1]))
        self.wait()

        self.play(
            TransformFromCopy(w_labels[0], a[8:10]),
            TransformFromCopy(w_labels[1], a[13:15]),
            TransformFromCopy(w_labels[2], b[8:10]),
            TransformFromCopy(w_labels[3], b[13:15]),
            TransformFromCopy(input_labels[0], a[10:12]),
            TransformFromCopy(input_labels[1], a[15:17]),
            TransformFromCopy(input_labels[0], b[10:12]),
            TransformFromCopy(input_labels[1], b[15:17]),
            TransformFromCopy(bias_labels[0], a[-6:-1]),
            TransformFromCopy(bias_labels[1], b[-6:-1]),
            FadeIn(a[12:13]), FadeIn(a[17:18]), FadeIn(b[12:13]), FadeIn(b[17:18]),
            run_time=2
        )

        self.wait(2)


        pulse_stage(hidden_to_output, extra_lines=[b3_arrow], color=PURE_RED, run_time=1.5)
        self.wait(0.5)

        c = Tex(r"\hat{y} = a_1^{(2)} = f(w_5 a_1^{(1)} + w_6 a_2^{(1)} + b_1^{(2)})")
        c.next_to(b, DOWN, buff=1.0).scale(1.33).move_to(VGroup(a, b)).scale(1.15)

        self.play(
            FadeOut(a), FadeOut(b), 
            TransformFromCopy(y_hat, c[:2]),
            FadeIn(c[2]),
            TransformFromCopy(output_label, c[3:8]),
        
        )

        self.wait(2)

        self.play(
            FadeIn(c[8])
        )

        self.play(FadeIn(c[9:11]), FadeIn(c[-1])) 

        self.play(
            TransformFromCopy(w5, c[11:13]),
            TransformFromCopy(w6, c[19:21]),
            TransformFromCopy(hidden_labels[0], c[13:18]),
            TransformFromCopy(hidden_labels[1], c[21:26]),
            TransformFromCopy(bias_labels[2], c[-6:-1]),
            FadeIn(c[18]), FadeIn(c[26]),
            run_time=2
        )

        self.wait(2)
        
        d = Tex(r"\hat{y} = f(w_5 f(w_1 x_1 + w_2 x_2 + b_1^{(1)}) + w_6 f(w_3 x_1 + w_4 x_2 + b_2^{(1)}) + b_1^{(2)})").move_to(c).scale(1.12)
        self.play(ReplacementTransform(c, d), run_time=1)

        self.wait(2)

        zero_labels = []
        all_symbols = w_labels + bias_labels
        
        # Create zero versions at the same positions
        for lbl in all_symbols:
            zero_tex = Text("0.5").scale(0.9)
            zero_tex.move_to(lbl.get_center())
            zero_labels.append(zero_tex)
        
        # Group both for easier animation
        zero_group = VGroup(*zero_labels)
        original_group = VGroup(*all_symbols)
        
        # ===== Fade original labels out, fade zeros in =====
        self.play(
            FadeOut(original_group, shift=UP*0.05),
            FadeIn(zero_group, shift=UP*0.05),
            run_time=1.2
        )
        self.wait(2)
                 
        self.camera.frame.save_state()
        self.wait(2)

        self.play(Transform(d, Tex(r"\hat{y} = f(0.5 \cdot f(0.5 \cdot x_1 + 0.5 \cdot x_2 + 0.5) + 0.5 \cdot f(0.5 \cdot x_1 + 0.5 \cdot x_2 + 0.5) + 0.5)").move_to(d)))
        
        self.wait(2)

        a1 = Tex(r"a^{(1)}_1 = f(w_1 x_1 + w_2 x_2 + b^{(1)}_1)")
        a1.move_to(RIGHT*17).scale(1.85).shift(UP*0.3565)

        a2 = Tex(r"a^{(1)}_2 = f(w_3 x_1 + w_4 x_2 + b^{(1)}_2)")
        a2.next_to(a1, DOWN, buff=1.15).scale(1.85)

        self.play(
            FadeIn(VGroup(a1, a2)),
            FadeOut(VGroup(d)),
            self.camera.frame.animate.shift(RIGHT*16)
        )

        self.wait(2)


        self.play(
            Transform(a1, Tex(r"a^{(1)}_1 = f(0.5 \cdot x_1 + 0.5 \cdot x_2 + 0.5)").move_to(a1).scale(1.85)),
            Transform(a2, Tex(r"a^{(1)}_2 = f(0.5 \cdot x_1 + 0.5 \cdot x_2 + 0.5)").move_to(a2).scale(1.85)),
        )

        self.wait(2)


        a = Tex(r"\frac{\partial L}{\partial w_5} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z^{(2)}} \cdot \frac{\partial z^{(2)}}{\partial w_5}").scale(1.32)
        b = Tex(r"\frac{\partial L}{\partial w_6} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z^{(2)}} \cdot \frac{\partial z^{(2)}}{\partial w_6}").scale(1.32)
       
        a.move_to(VGroup(a1, a2)).scale(1.62).shift(UP*1.4)
        b.scale(1.62).next_to(a, DOWN, buff=0.8)

        self.play(FadeOut(VGroup(a1, a2)), FadeIn(a), FadeIn(b))

        self.wait(2)


        temp = Tex(r"\frac{\partial L}{\partial w_5} = \frac{\partial L}{\partial \hat{y}} \cdot f'(z^{(2)}) \cdot a_1^{(1)}").scale(1.32*1.52)
        temp1 = Tex(r"\frac{\partial L}{\partial w_6} = \frac{\partial L}{\partial \hat{y}} \cdot f'(z^{(2)}) \cdot a_2^{(1)}").scale(1.32*1.52)
        temp.move_to(a)
        temp1.move_to(b)
        self.play(Transform(a, temp), Transform(b, temp1))
        self.wait(2)

        rect = SurroundingRectangle(a).scale(1.1)
        rect1 = SurroundingRectangle(b).scale(1.1)

        self.play(ShowCreation(rect), ShowCreation(rect1))

        self.play(
            a[-5:].animate.set_color(RED_C),
            b[-5:].animate.set_color(RED_C),
        )

        self.wait(2)

        self.play(self.camera.frame.animate.shift(LEFT*16).scale(0.8).shift(UP*0.8))



        temp_a = Circle(stroke_width=6).move_to(w5).set_color("#ff0000").scale(0.5)
        temp_b = Circle(stroke_width=6).move_to(w6).set_color("#ff0000").scale(0.5)
        self.play(
            ShowCreation(temp_a),
            ShowCreation(temp_b),
        )

        self.wait(2)

        # ===== Fade original labels out, fade zeros in =====
        self.play(
            FadeIn(original_group, shift=UP*0.05),
            FadeOut(zero_group, shift=UP*0.05),
            run_time=1.2
        )
        self.wait(2)

        self.play(
            w_labels[4].animate.set_color(YELLOW),
            hidden_to_output[0].animate.set_color(YELLOW),
            w_labels[5].animate.set_color(YELLOW),
            hidden_to_output[1].animate.set_color(YELLOW),
            run_time=1
        )

        self.wait(2)

        self.camera.frame.save_state()


        self.wait(2)

        
        self.play(
            temp_a.animate.move_to(w_labels[0]),
            temp_b.animate.move_to(w_labels[2]),
        )


        self.play(
            w_labels[0].animate.set_color(PURPLE_C),
            weights[0].animate.set_color(PURPLE_C),
            w_labels[2].animate.set_color(PURPLE_C),
            weights[1].animate.set_color(PURPLE_C),
            run_time=1
        )
        self.wait(2)

        self.play(
            Transform(temp_a, Circle().move_to(w_labels[1]).set_color("#ff0000").scale(0.5)),
            Transform(temp_b, Circle().move_to(w_labels[3]).set_color("#ff0000").scale(0.5)),
        )

        MAROON = "#EF4713"
        self.play(
            w_labels[1].animate.set_color(MAROON),
            weights[2].animate.set_color(MAROON),
            w_labels[3].animate.set_color(MAROON),
            weights[3].animate.set_color(MAROON),
            run_time=1
        )
        self.wait(2)

        self.play(Uncreate(temp_a), Uncreate(temp_b))


        self.play(Indicate(hidden_nodes[0], color="#ff0000"), Indicate(hidden_nodes[1], color="#ff0000"), run_time=0.5)
        self.play(Indicate(hidden_nodes[0], color="#ff0000"), Indicate(hidden_nodes[1], color="#ff0000"), run_time=0.5)
        self.play(Indicate(hidden_nodes[0], color="#ff0000"), Indicate(hidden_nodes[1], color="#ff0000"), run_time=0.5)
        self.play(Indicate(hidden_nodes[0], color="#ff0000"), Indicate(hidden_nodes[1], color="#ff0000"), run_time=0.5)
        
        self.wait(2)

        self.play(FadeOut(VGroup(bias_labels, )), FadeOut(w5), FadeOut(w6), FadeOut(b1_arrow), FadeOut(b2_arrow), FadeOut(b3_arrow), FadeOut(w_labels[0]), FadeOut(w_labels[1]), FadeOut(w_labels[2]), FadeOut(w_labels[3]), )
    
        self.wait(2)

        c = hidden_nodes[0].copy()
        d = hidden_labels[0].copy()

        c.shift(DOWN*1.54)
        d.shift(DOWN*1.54)

        w1 = Line(input_nodes[0].get_center(), c.get_center(), color=GREY_B, stroke_opacity=0.9).set_color(PURPLE_B).set_z_index(-1)
        w2 = Line(input_nodes[1].get_center(), c.get_center(), color=GREY_B, stroke_opacity=0.9).set_color("#ff0000").set_z_index(-1)
        w3 = Line(c.get_center(), output_node.get_center(), color=GREY_B, stroke_opacity=0.9).set_color(YELLOW_C).set_z_index(-1)

        self.play(
            ReplacementTransform(hidden_nodes[0], c),
            ReplacementTransform(hidden_labels[0], d),
            ReplacementTransform(hidden_nodes[1], c),
            ReplacementTransform(hidden_labels[1], d),
            ReplacementTransform(weights[0], w1),
            ReplacementTransform(weights[1], w1),
            ReplacementTransform(weights[2], w2),
            ReplacementTransform(weights[3], w2),
            ReplacementTransform(hidden_to_output[0], w3),
            ReplacementTransform(hidden_to_output[1], w3)
        )


        self.wait(2)

        a = Text("Symmetry problem !", weight=BOLD)
        a.next_to(c, DOWN, buff=1.2).scale(1.65).set_color(RED_B).shift(DOWN*1.23+RIGHT*1.4)

        self.play(self.camera.frame.animate.shift(DOWN*1.16), Write(a))
        self.wait(3)
