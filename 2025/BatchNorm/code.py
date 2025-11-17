from manimlib import *
import numpy as np

class Testing(Scene):

    def construct(self):

        self.camera.frame.scale(1.23).shift(DOWN*2.7)

        xbatch = Tex(r"x = B = \{x_1, x_2, \dots, x_m\}")
        mu = Tex(r"\mu_B = \frac{1}{m}\sum_{i=1}^m x_i")
        var = Tex(r"\sigma_B^2 = \frac{1}{m}\sum_{i=1}^m (x_i - \mu_B)^2")
        xhat = Tex(r"\hat{x}_i = \frac{x_i - \mu_B}{\sqrt{\sigma_B^2 + \varepsilon}}")
        y = Tex(r"y_i = \gamma\,\hat{x}_i + \beta")

        xbatch.scale(1.4).shift(UP*2.3)

        mu.next_to(xbatch, DOWN, buff=0.85).scale(1.34)
        var.next_to(mu, DOWN, buff=0.85).scale(1.34)
        xhat.next_to(var, DOWN, buff=1.25).scale(1.34)
        y.next_to(xhat, DOWN, buff=1.15).scale(1.54)
                

        self.add(y, xhat, var, mu)

        y[3].set_color("#00ff55")
        y[-1].set_color("#ff0000")

        self.wait(2)

        rect = SurroundingRectangle(xhat).scale(1.1)
        self.play(ShowCreation(rect))
        self.wait(2)

        self.play(Transform(
            rect, SurroundingRectangle(Group(mu, var)).scale(1.1)
        ))

        self.wait(2)

        a = Tex(r"""
                 \begin{array}{ccccc}
                 x_1 & x_2 & x_3 & \cdots & x_k \\[8pt]
                 \mu_{1} & \mu_{2} & \mu_{3} & \cdots & \mu_{k} \\[8pt]
                 \sigma^2_{1} & \sigma^2_{2} & \sigma^2_{3} & \cdots & \sigma^2_{k}
                 \end{array}
                 """)
        

        a.shift(RIGHT*14+DOWN*2.66).scale(2)

        self.play(ShowCreation(a[:11]), self.camera.frame.animate.shift(RIGHT*14))
        self.wait(2)

        self.play(TransformFromCopy(a[:11], a[11:22]))
        self.wait(2)

        self.play(TransformFromCopy(a[11:22], a[22:]))
        self.wait(2)

        b = Tex(r"m_t = (1-\alpha)m_{t-1} + \alpha x_t").next_to(a, RIGHT).shift(RIGHT*8)
        b.scale(2.2)

        self.play(ShowCreation(b), self.camera.frame.animate.shift(RIGHT*15.44))
        self.wait(2)


        self.play(Transform(
            b, Tex(r"m_t = \alpha x_t + \alpha(1-\alpha)x_{t-1} + \alpha(1-\alpha)^2 x_{t-2} + \cdots + (1-\alpha)^t m_0").move_to(b).scale(1.23)

        ))

        self.wait(2)


        self.play(FadeOut(b), self.camera.frame.animate.shift(LEFT*15.44))

        self.wait(2)

        self.play(a[11:].animate.shift(UP*0.87), FadeOut(a[:11]))

        brace = Brace(a[11:22], UP, buff=0.7).set_color(YELLOW)
        brace1 = Brace(a[22:], DOWN, buff=0.7).set_color(YELLOW)

        self.play(GrowFromCenter(brace), GrowFromCenter(brace1))

        mu = Tex(r"\mu").scale(1.7).next_to(brace, UP, buff=0.5)
        var = Tex(r"\sigma^2").scale(1.7).next_to(brace1, DOWN, buff=0.5)
       
        self.play(Write(mu), Write(var))
        self.wait()

        self.remove(rect)

        rect = SurroundingRectangle(mu).scale(1.25)
        var = SurroundingRectangle(var).scale(1.1)

        self.play(ShowCreation(rect), ShowCreation(var))

        self.wait(2)


        temp = SurroundingRectangle(xhat).scale(1.12)

        self.play(ReplacementTransform(VGroup(rect, var), temp), self.camera.frame.animate.shift(LEFT*14))


        self.wait(2)


class WhyBatchNorm(Scene):
    def construct(self):

        # --------------------- Camera / Colors ---------------------
        self.camera.frame.scale(1.17).shift(RIGHT*6 + DOWN*1.26)

        HIDDEN_COLOR = BLUE
        WEIGHT_COLOR = PURE_RED

        # --------------------- Network layout ----------------------
        layer_sizes = [5, 4, 5, 3, 1]
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

                neuron.move_to(
                    RIGHT * 1.24 * i * layer_spacing +
                    UP * (j - (size - 1) / 2) * neuron_spacing
                ).set_z_index(1)

                layer.add(neuron)
            layers.append(layer)

        network = VGroup(*layers)

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

        # show network
        self.play(LaggedStartMap(GrowFromCenter, network, lag_ratio=0.05, run_time=1.5))

        connections = create_connections(layers).set_z_index(-1)
        self.play(LaggedStartMap(ShowCreation, connections, lag_ratio=0.01, run_time=2))
        self.wait(1)

        self.camera.frame.save_state()

        # --------------------- INPUT HISTOGRAM ---------------------
        hist_width = 2
        hist_height = 0.8 * 2.4 * 3.2
        num_bins = 20

        input_layer = layers[0]

        input_axis = Line(
            LEFT * hist_width/2,
            RIGHT * hist_width/2,
            stroke_width=3,
            color=WHITE
        )
        input_axis.next_to(input_layer, DOWN, buff=1.71)

        input_bars = VGroup()
        input_var = 0.5

        for i in range(num_bins):
            x = -2 + (i + 0.5) * (4 / num_bins)
            height = np.exp(-(x**2) / (2 * input_var**2)) / (input_var * np.sqrt(2 * np.pi))
            height *= hist_height * 0.5 * input_var

            bar = Rectangle(
                width=hist_width / num_bins * 0.9,
                height=height,
                fill_opacity=0.88,
                fill_color=GREEN,
                stroke_width=0
            )
            bar.move_to(input_axis.get_center() + RIGHT*(x*hist_width/4) + UP*height/2)
            input_bars.add(bar)

        input_label = Text("Input data", font_size=46)
        input_label.next_to(input_axis, DOWN, buff=0.7)

        input_hist = VGroup(input_axis, input_bars, input_label).shift(DOWN * 0.3)

        self.play(ShowCreation(input_hist), run_time=1.4)
        self.wait(2)

        # --------------------- ORIGINAL ICS HISTOGRAMS ---------------------
        def create_histogram(center_mobj, values):
            hist_width = 1.6
            hist_height = 1.0
            num_bins = len(values)

            axis = Line(LEFT*hist_width/2, RIGHT*hist_width/2, stroke_width=3, color=WHITE)
            axis.next_to(center_mobj, DOWN, buff=1.4)

            bars = VGroup()
            for i in range(num_bins):
                h = values[i] * hist_height
                bar = Rectangle(
                    width=hist_width/num_bins*0.9,
                    height=h,
                    fill_opacity=0.95,
                    fill_color=BLUE,
                    stroke_width=0,
                )
                x_shift = -hist_width/2 + (i+0.5)*(hist_width/num_bins)
                bar.move_to(axis.get_center() + RIGHT*x_shift + UP*h/2)
                bars.add(bar)

            return VGroup(axis, bars)

        num_bins = 20
        x = np.linspace(-1, 1, num_bins)

        vals1 = np.exp(-6*(x-0.3)**2); vals1 /= vals1.max()
        vals2 = np.ones(num_bins)*0.6 + 0.25*np.random.rand(num_bins); vals2 /= vals2.max()
        vals3 = np.abs(np.random.randn(num_bins)); vals3 /= vals3.max()

        distributions = [vals1, vals2, vals3]

        hidden_hists = VGroup()
        for idx, layer in enumerate(layers[1:-1]):
            hist = create_histogram(layer, distributions[idx]).shift(DOWN*0.86).scale(1.3)
            hidden_hists.add(hist)

        self.wait()

        # ---------------- ICS original rectangle transitions ----------------
        rect = SurroundingRectangle(layers[0], color="#ff0000", fill_color="#ff0000", fill_opacity=0.2).scale(1.1)
        self.play(ShowCreation(rect))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(layers[1], color="#ff0000", fill_color="#ff0000", fill_opacity=0.2).scale(1.1)))
        self.play(TransformFromCopy(VGroup(input_axis, input_bars), hidden_hists[0]))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(layers[2], color="#ff0000", fill_color="#ff0000", fill_opacity=0.2).scale(1.1)))
        self.play(TransformFromCopy(hidden_hists[0], hidden_hists[1]))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(layers[3], color="#ff0000", fill_color="#ff0000", fill_opacity=0.2).scale(1.1)))
        self.play(TransformFromCopy(hidden_hists[1], hidden_hists[2]))
        self.wait(2)

        self.camera.frame.save_state()

        self.play(self.camera.frame.animate.scale(1.2).shift(DOWN*1.12), Uncreate(rect))

        text = Text("Internal Covariate Shift", weight=BOLD).set_color(RED_C)
        text.scale(2).next_to(hidden_hists[1], DOWN, buff=0.9).shift(DOWN*0.6+LEFT*0.2)

        self.play(ShowCreation(text))
        self.wait(2)

        self.play(Uncreate(text), self.camera.frame.animate.restore(), Uncreate(hidden_hists))
        self.wait(2)

        # ---------------------- BEGIN BATCHNORM PART ----------------------

        input_layer = layers[0]
        hidden_layer1 = layers[1]
        hidden_layer2 = layers[2]
        hidden_layer3 = layers[3]
        output_layer = layers[4]

        original_strokes = [line.get_stroke_width() for line in connections]
        original_colors = [line.get_color() for line in connections]

        # ---------------- glow / pulse helpers ----------------
        def create_glow(center_point, radius=0.15, color=YELLOW, intensity=0.3):
            glow_group = VGroup()
            for i in range(20):
                glow_radius = radius*(1+i*0.1)
                opacity = intensity*(1-i/20)
                circ = Circle(radius=glow_radius, stroke_opacity=0, fill_color=color, fill_opacity=opacity)
                circ.move_to(center_point)
                glow_group.add(circ)
            return glow_group

        def create_pulse(start_point, color="#ff0000"):
            dot = Dot(radius=0.12, color=color, fill_opacity=1).move_to(start_point)
            glow = create_glow(start_point, radius=0.1, color=color, intensity=0.4)
            return VGroup(glow, dot)

        def find_connection_line(a, b, all_conns, tol=0.12):
            for L in all_conns:
                if np.allclose(L.get_start(), a, atol=tol) and np.allclose(L.get_end(), b, atol=tol):
                    return L
            return None

        # ---------------- normalization helper ----------------
        def normalized_distribution(values):
            w = np.array(values)
            kernel = np.exp(-0.5*(np.linspace(-2,2,5)**2))
            kernel /= kernel.sum()
            sm = np.convolve(w, kernel, mode='same')
            bins = np.linspace(-1,1,len(w))
            gauss = np.exp(-3*bins**2); gauss/=gauss.max()
            out = 0.5*(sm/sm.max()) + 0.5*gauss
            return out/out.max()

        # ---------------- create BN pillars (rounded, shorter) ----------------
        def create_bn(left_layer, right_layer, xx=0.8):
            lx = left_layer.get_center()[0]
            rx = right_layer.get_center()[0]
            x = lx*0.3 + rx*0.7

            top = max([n.get_top()[1] for n in left_layer]+[n.get_top()[1] for n in right_layer])
            bottom = min([n.get_bottom()[1] for n in left_layer]+[n.get_bottom()[1] for n in right_layer])
            h = (top-bottom)*xx  # 20% shorter

            pillar = RoundedRectangle(
                width=0.55,
                height=h,
                corner_radius=0.25,
                fill_color=YELLOW,
                fill_opacity=1.0,
                stroke_width=0
            )
            pillar.move_to([x,(top+bottom)/2,0])

            txt = Text("BN", font_size=36, weight=BOLD).set_color(BLACK)
            txt.move_to(pillar.get_center())
            return VGroup(pillar, txt)

        # Show all BN bars at once
        bn1 = create_bn(layers[0], layers[1], xx=0.85)
        bn2 = create_bn(layers[1], layers[2], xx=0.98)
        bn3 = create_bn(layers[2], layers[3])

        self.play(FadeIn(bn1), FadeIn(bn2), FadeIn(bn3), run_time=0.8)
        self.wait(0.2)

        # ---------------- pulse stage ----------------
        def run_stage(src_layer, dst_layer, prev_hist, dist_vals):
            new_vals = normalized_distribution(dist_vals)
            new_hist = create_histogram(dst_layer, new_vals).scale(1.34).shift(DOWN*0.5)

            pulses=[]
            lines=set()

            for s in src_layer:
                for t in dst_layer:
                    L=find_connection_line(s.get_center(), t.get_center(), connections)
                    if L is None: continue
                    p=create_pulse(s.get_center(), "#ff4444")
                    self.add(p)
                    pulses.append((p,L))
                    lines.add(L)

            anims=[]
            for p,L in pulses:
                anims.append(MoveAlongPath(p,L,rate_func=linear))
            for L in lines:
                anims.append(L.animate.set_stroke(width=4,color="#ff4444"))

            self.play(*anims, run_time=0.9)

            # TransformFromCopy WITHOUT removing old histogram
            self.play(TransformFromCopy(prev_hist,new_hist), run_time=0.9)

            # Fade pulses & restore colors
            restores=[]
            for L in lines:
                idx=connections.submobjects.index(L)
                restores.append(L.animate.set_stroke(width=original_strokes[idx],
                                                     color=original_colors[idx]))
            self.play(*[FadeOut(p) for p,_ in pulses],*restores,run_time=0.5)

            return new_hist

        # Run BN stages
        h1 = run_stage(input_layer, hidden_layer1, input_hist, vals1)
        self.wait(0.2)
        h2 = run_stage(hidden_layer1, hidden_layer2, h1, vals2)
        self.wait(0.2)
        h3 = run_stage(hidden_layer2, hidden_layer3, h2, vals3)

        self.wait(1)

        self.play(*[FadeOut(obj) for obj in [input_hist, h1, h2, h3]], run_time=1.0)
        
        # ===================== ADD W^(l), γ^(l), β^(l) BELOW EACH HIDDEN LAYER =====================
        
        def add_params_for_layer(layer, l_index):
            # Create Tex objects
            W_tex = Tex(r"W^{(%d)}" % l_index, font_size=60)
            gamma_tex = Tex(r"\gamma^{(%d)}" % l_index, font_size=60)
            beta_tex  = Tex(r"\beta^{(%d)}"  % l_index, font_size=60)
        
            # Stack them vertically
            param_group = VGroup(W_tex, gamma_tex, beta_tex).arrange(
                direction=DOWN,
                buff=0.22,
                aligned_edge=LEFT
            )
        
            # Position below the layer
            param_group.next_to(layer, DOWN, buff=0.9)
        
            return param_group
        
        
        # Create parameter stacks for each hidden layer
        params_l2 = add_params_for_layer(layers[1], 1)  # for layer 1→2 weights
        params_l3 = add_params_for_layer(layers[2], 2)
        params_l4 = add_params_for_layer(layers[3], 3)
        
        # Animate them in
        self.play(
            FadeIn(params_l2),
            FadeIn(params_l3),
            FadeIn(params_l4),
            run_time=1.2
        )
        

        self.wait(2)

        def update_rules_for_layer():
            W_up = Tex(r"W^{(l)} \leftarrow W^{(l)} - \alpha \frac{\partial L}{\partial W^{(l)}}",  font_size=38)
            g_up = Tex(r"\gamma^{(l)} \leftarrow \gamma^{(l)} - \alpha \frac{\partial L}{\partial \gamma^{(l)}}" , font_size=38)
            b_up = Tex(r"\beta^{(l)} \leftarrow \beta^{(l)} - \alpha \frac{\partial L}{\partial \beta^{(l)}}" , font_size=38)
        
            group = VGroup(W_up, g_up, b_up).arrange(DOWN, buff=0.20)
            return group
        
        a = update_rules_for_layer().scale(2.2).shift(RIGHT*22+DOWN*1.3)

        self.play(self.camera.frame.animate.shift(RIGHT*16), ShowCreation(a))
        self.wait(2)


class GaussianNormalization(Scene):
    def construct(self):

        self.camera.frame.scale(0.89).shift(DOWN)
        # -------------------------------------------------------------
        # CREATE AXES FOR UNNORMALIZED DATA
        # -------------------------------------------------------------
        
        unnorm_axes = Axes(
            x_range=[-2, 10, 1],
            y_range=[0, 0.5, 0.1],
            width=10,
            height=5,
            axis_config={
                "stroke_width": 3,
                "include_tip": True,
                "include_ticks": True,
            }
        ).shift(DOWN * 0.5)
        

        
        # -------------------------------------------------------------
        # GENERATE GAUSSIAN DATA - UNNORMALIZED
        # -------------------------------------------------------------
        
        # Unnormalized parameters
        original_mean = 5.0
        original_std = 1.5
        
        # More sample points for thinner rectangles
        x_values = np.arange(0, 10, 0.15)
        
        # Gaussian probability density function
        def gaussian(x, mu, sigma):
            return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
        
        # Calculate heights for unnormalized data
        y_values_unnorm = gaussian(x_values, original_mean, original_std)
        
        # Create thin rectangles for unnormalized distribution
        rect_width = 0.12
        unnorm_rects = VGroup()
        
        for x, y in zip(x_values, y_values_unnorm):
            rect = Rectangle(
                width=rect_width,
                height=unnorm_axes.y_axis.get_unit_size() * y,
                stroke_width=1,
                stroke_color=BLUE,
                fill_color=BLUE,
                fill_opacity=0.9
            )
            rect.move_to(unnorm_axes.c2p(x, y/2))
            unnorm_rects.add(rect)
        
        # Statistics text for unnormalized
        unnorm_stats = VGroup(
            Tex(r"\mu = " + f"{original_mean:.1f}", font_size=56, color=YELLOW),
            Tex(r"\sigma = " + f"{original_std:.1f}", font_size=56, color=YELLOW)
        ).arrange(RIGHT, buff=0.5).next_to(unnorm_axes, DOWN, buff=0.5)
        
        # -------------------------------------------------------------
        # CREATE AXES FOR NORMALIZED DATA
        # -------------------------------------------------------------
        
        norm_axes = Axes(
            x_range=[-7, 7, 1],
            y_range=[0, 0.5, 0.1],
            width=10,
            height=5,
            axis_config={
                "stroke_width": 3,
                "include_tip": True,
                "include_ticks": True,
            }
        ).shift(DOWN * 0.5)
        
        # -------------------------------------------------------------
        # GENERATE NORMALIZED DATA
        # -------------------------------------------------------------
        
        # Standardize: z = (x - mean) / std
        x_values_norm = (x_values - original_mean) / original_std
        
        # Normalized distribution (standard normal)
        y_values_norm = gaussian(x_values_norm, 0, 1)
        
        # Create rectangles for normalized distribution
        norm_rects = VGroup()
        
        for x, y in zip(x_values_norm, y_values_norm):
            rect = Rectangle(
                width=rect_width,
                height=norm_axes.y_axis.get_unit_size() * y,
                stroke_width=1,
                stroke_color=GREEN,
                fill_color=GREEN,
                fill_opacity=0.9
            )
            rect.move_to(norm_axes.c2p(x, y/2))
            norm_rects.add(rect)
        
        # Statistics text for normalized
        norm_stats = VGroup(
            Tex(r"\mu = 0.0", font_size=56, color=YELLOW),
            Tex(r"\sigma = 1.0", font_size=56, color=YELLOW)
        ).arrange(RIGHT, buff=0.5).next_to(norm_axes, DOWN, buff=0.5)
        
        # -------------------------------------------------------------
        # ANIMATION SEQUENCE
        # -------------------------------------------------------------
        
        # Show unnormalized axes
        self.play(
            ShowCreation(unnorm_axes),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Draw unnormalized distribution
        self.play(
            LaggedStartMap(FadeIn, unnorm_rects, lag_ratio=0.01),
            run_time=2.5
        )
        self.wait(0.5)
        
        # Show statistics
        self.play(Write(unnorm_stats), run_time=1)
        self.wait(1.5)
        
        # Transform both axes and distributions
        self.play(
            Transform(unnorm_axes, norm_axes),
            Transform(unnorm_rects, norm_rects),
            Transform(unnorm_stats, norm_stats),
            run_time=1
        )
        self.wait(0.5)
        
        self.wait(3)



class BatchNormMath(Scene):


    def construct(self):

        xbatch = Tex(r"x = B = \{x_1, x_2, \dots, x_m\}")
        mu = Tex(r"\mu_B = \frac{1}{m}\sum_{i=1}^m x_i")
        var = Tex(r"\sigma_B^2 = \frac{1}{m}\sum_{i=1}^m (x_i - \mu_B)^2")
        xhat = Tex(r"\hat{x}_i = \frac{x_i - \mu_B}{\sqrt{\sigma_B^2 + \varepsilon}}")
        y = Tex(r"y_i = \gamma\,\hat{x}_i + \beta")

        xbatch.scale(1.4).shift(UP*2.3)

        mu.next_to(xbatch, DOWN, buff=0.85).scale(1.34)

        self.play(ShowCreation(xbatch))

        self.wait(2)

        self.play(ShowCreation(mu))

        self.wait(2)

        var.next_to(mu, DOWN, buff=0.85).scale(1.34)

        self.play(ShowCreation(var))

        self.wait(2)

        xhat.next_to(var, DOWN, buff=1.25).scale(1.34)

        self.camera.frame.save_state()

        self.play(ShowCreation(xhat), self.camera.frame.animate.shift(DOWN*2.6))
        self.wait(2)

        rect = SurroundingRectangle(xhat).scale(1.1)
        self.play(ShowCreation(rect))
        self.wait(2)

        y.next_to(xhat, DOWN, buff=1.55).scale(1.54)

        self.play(ShowCreation(y), self.camera.frame.animate.shift(DOWN*2.6),
                 FadeOut(rect))
        self.wait(2)

        y[3].set_color("#00ff55")
        for i in range(5):
                self.play(Indicate(y[3], color="#00ff55"), run_time=0.5)
                     

        self.wait(2)

        y[-1].set_color("#ff0000")
        for i in range(5):
                self.play(Indicate(y[-1], color="#ff0000"), run_time=0.5)

        self.wait(2)


        a = Tex(r"x_i = z^{(l)} = W^{(l)} a^{(l-1)} + b^{(l)}").shift(RIGHT*11)
        a.scale(1.7)
        self.play(ShowCreation(a), self.camera.frame.animate.restore().shift(RIGHT*11))
        self.wait(2)

        rect = SurroundingRectangle(a[-4:]).scale(1.12)
        self.play(ShowCreation(rect))

        self.wait(2)

        self.play(
              Transform(a, Tex(r"\hat{z}^{(l)} = \frac{z^{(l)} - \mu_B}{\sqrt{\sigma_B^2 + \varepsilon}}").move_to(a).scale(1.88)),
              FadeOut(rect)
        )

        self.wait(2)

        self.play(a.animate.scale(0.7).shift(UP*2.5))
        self.wait(2)

        b = Tex(r"\mu_B = \frac{1}{m}\sum_{i=1}^m z^{(l)}_i").next_to(a, DOWN, buff=1.9).scale(1.7)
        

        self.play(TransformFromCopy(a[-10:-8],b))

        self.wait(2)

        self.play(Transform(b, Tex(r"\mu_B = \frac{1}{m}\sum_{i=1}^m \big(W^{(l)} a_i^{(l-1)} + b^{(l)}\big)").scale(1.7).move_to(b)))
        self.wait(2)

        self.play(Transform(b, Tex(r"\mu_B = \frac{1}{m}\sum_{i=1}^m W^{(l)} a_i^{(l-1)}"
            r"+ \frac{1}{m}\sum_{i=1}^m b^{(l)}").scale(1.45).move_to(b)))
        self.wait(2)

        self.play(Transform(b, Tex(r"\mu_B = W^{(l)}\left(\frac{1}{m}\sum_{i=1}^m a_i^{(l-1)}\right)"
            r"+ \frac{1}{m}\sum_{i=1}^m b^{(l)}").scale(1.35).move_to(b)))
        self.wait(2)


        self.play(Transform(b, Tex(r"\mu_B = W^{(l)}\left(\frac{1}{m}\sum_{i=1}^m a_i^{(l-1)}\right)"
            r"+ \frac{1}{m}\sum_{i=1}^m b^{(l)}").scale(1.35).move_to(b)))
        self.wait(2)



        rect = SurroundingRectangle(b[-12:]).scale(1.1)
        self.play(ShowCreation(rect),)

        self.wait(2)

        self.play(Transform(b, Tex(r"\mu_B = W^{(l)}\bar{a} + b^{(l)}").scale(1.65).move_to(b)), FadeOut(rect))
        self.wait(2)
        

        s3 = Tex(
                r"\hat{z}^{(l)} = "
                r"\frac{\,(W^{(l)} a^{(l-1)} + b^{(l)})"
                r" - \big(W^{(l)}\bar{a} + b^{(l)}\big)\,}"
                r"{\sqrt{\sigma_B^2 + \varepsilon}}"
            ).move_to(b).shift(UP*0.4+LEFT*0.4).scale(1.1)
            
        self.play(ReplacementTransform(VGroup(a,b), s3))

        self.play(Transform(s3, Tex(
                r"\hat{z}^{(l)} = "
                r"\frac{\,W^{(l)}\big(a^{(l-1)} - \bar{a}\big)\,}"
                r"{\sqrt{\sigma_B^2 + \varepsilon}}"
            ).scale(1.65).move_to(s3)),)
        self.wait(2)  

        self.camera.frame.save_state()

        self.play(self.camera.frame.animate.shift(LEFT*11+DOWN*5.5), FadeOut(s3))

        rect = SurroundingRectangle(y[-1]).scale(1.1)

        self.play(ShowCreation(rect))

        self.wait(2)
