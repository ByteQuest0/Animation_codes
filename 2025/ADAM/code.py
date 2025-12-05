from manimlib import *
import numpy as np

class ADAM(Scene):
    def construct(self):

        # The update rule formula
        formula = Tex(
            r"\theta_{t+1} = \theta_t - \alpha \frac{\partial L}{\partial \theta_t}",
            font_size=120
        )
        
        self.play(Write(formula))
        self.wait(2)
        self.play(formula[-6:].animate.set_color(RED))
        self.wait(2)

        a = Tex(
            r"\theta_{t+1} = \theta_t - \alpha g_t",
            font_size=120
        )

        self.play(Transform(formula, a))
        self.wait(2)

        m = Tex(r"m_t = \beta_m m_{t-1} + (1 - \beta_m)\, g_t").scale(1.6)
        m.shift(RIGHT*20 +UP*0.9)

        v = Tex(r"v_t = \beta_r v_{t-1} + (1 - \beta_r)\, g_t^2").scale(1.6)
        v.shift(RIGHT*20 + DOWN*1.1)

        self.play(
            ShowCreation(m),
            ShowCreation(v),
            self.camera.frame.animate.shift(RIGHT*20)
        )

        recta = SurroundingRectangle(m, color=GREEN).scale(1.1)
        rectb = SurroundingRectangle(v, color=BLUE).scale(1.1)
        self.play(
            ShowCreation(recta),
            ShowCreation(rectb)
        )
        self.wait()

        m_text = Text("Momentum", font_size=56, weight=BOLD).next_to(recta, UP).set_color(GREEN).shift(UP*0.6)
        v_text = Text("RMSProp", font_size=56, weight=BOLD).next_to(rectb, DOWN).set_color(BLUE).shift(DOWN*0.6)

        self.play(Write(m_text), Write(v_text))
        self.wait(3)

        
        m_bias = Tex(r"\hat{m}_t = \frac{m_t}{1 - \beta_m^{t}}").scale(1.6)
        m_bias.shift(RIGHT*40 +UP*0.3)

        v_bias = Tex(r"\hat{v}_t = \frac{v_t}{1 - \beta_r^{t}}").scale(1.6)
        v_bias.shift(RIGHT*40 + DOWN*2.17)

        self.play(
            ShowCreation(m_bias),
            ShowCreation(v_bias),
            self.camera.frame.animate.shift(RIGHT*20)
        )

        rect_1 = SurroundingRectangle(m_bias, color=GREEN).scale(1.1)
        rect_2 = SurroundingRectangle(v_bias, color=BLUE).scale(1.1)
        self.play(
            ShowCreation(rect_1),
            ShowCreation(rect_2)
        )

        self.wait(2)

        temp = Tex(r"m_0 = 0,\ v_0 = 0").next_to(m_bias, UP, buff=0.7).scale(1.7).shift(UP*0.6)
        self.play(ShowCreation(temp))
        self.wait(2)

        self.play(self.camera.frame.animate.shift(LEFT*40))

        aaa = Tex(r"\theta_{t+1} = \theta_t - \alpha \,\frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \varepsilon}", font_size=100)

        self.play(Transform(formula, aaa))

        self.play(formula.animate.shift(DOWN*1.3))

        aaa = Text("Adam Optimizer", weight=BOLD).to_edge(UP).shift(DOWN*1.2+RIGHT*0.2).set_color("#deff07").scale(1.7)
        self.play(Write(aaa))

        self.wait(2)

        rect = SurroundingRectangle(formula[-11:-8], color=GREEN, stroke_width=5)
        self.play(ShowCreation(rect))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(formula[-7:], color=BLUE, stroke_width=5)))
        self.wait(2)

        self.play(Uncreate(rect))
        self.wait(2)
