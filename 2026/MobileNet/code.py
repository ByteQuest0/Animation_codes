from manimlib import *
import numpy as np


# ── palette ──────────────────────────────────────────────────────────
CH_COLORS = ["#E74C3C", "#27AE60", "#2980B9"]   # R, G, B channels
FILTER_COLOR = "#F39C12"
POINTWISE_COLOR = "#9B59B6"
DARK_BG = "#1a1a2e"
CARD_BG = "#222244"


def make_grid(rows, cols, cell_size=0.45, fill_color=BLUE, fill_opacity=0.6,
              stroke_color=WHITE, stroke_width=1.5):
    """Create a rows×cols grid of squares."""
    cells = VGroup()
    for r in range(rows):
        for c in range(cols):
            sq = Square(side_length=cell_size)
            sq.set_fill(fill_color, opacity=fill_opacity)
            sq.set_stroke(stroke_color, width=stroke_width)
            cells.add(sq)
    cells.arrange_in_grid(n_rows=rows, n_cols=cols, buff=0)
    return cells


def make_channel_stack(n_channels, rows, cols, cell_size=0.45, colors=None,
                       offset=np.array([0.15, -0.15, 0.0])):
    """Stack multiple grids with a diagonal offset to show depth."""
    colors = colors or CH_COLORS
    layers = VGroup()
    for i in range(n_channels):
        g = make_grid(rows, cols, cell_size=cell_size,
                      fill_color=colors[i % len(colors)], fill_opacity=0.55)
        g.shift(i * offset)
        layers.add(g)
    return layers


def labeled_arrow(start, end, label_text, font_size=28, color=YELLOW):
    """Arrow with a text label above it."""
    arrow = Arrow(start, end, buff=0.1, color=color, stroke_width=3)
    label = Text(label_text, font_size=font_size, color=color)
    label.next_to(arrow, UP, buff=0.15)
    return VGroup(arrow, label)


def create_3d_cuboid(h, w, d, color, pos=ORIGIN, cs=0.04):
    """Isometric 3D cuboid (front + top + right face)."""
    front = Rectangle(width=w * cs, height=h * cs)
    front.set_fill(color, opacity=0.85)
    front.set_stroke(WHITE, width=1.5)
    front.move_to(pos)
    dx = min(d, 20) * cs * 0.4
    dy = min(d, 20) * cs * 0.25
    top = Polygon(
        front.get_corner(UL), front.get_corner(UR),
        front.get_corner(UR) + RIGHT * dx + UP * dy,
        front.get_corner(UL) + RIGHT * dx + UP * dy,
    )
    top.set_fill(interpolate_color(color, WHITE, 0.3), opacity=0.85)
    top.set_stroke(WHITE, width=1.5)
    right_f = Polygon(
        front.get_corner(UR), front.get_corner(DR),
        front.get_corner(DR) + RIGHT * dx + UP * dy,
        front.get_corner(UR) + RIGHT * dx + UP * dy,
    )
    right_f.set_fill(interpolate_color(color, BLACK, 0.2), opacity=0.85)
    right_f.set_stroke(WHITE, width=1.5)
    return VGroup(front, top, right_f)


# ══════════════════════════════════════════════════════════════════════
#  SCENE — Standard (Normal) Convolution
# ══════════════════════════════════════════════════════════════════════

class NormalConvolution(Scene):
    def construct(self):
        INPUT_CLR  = "#4A90D9"
        FILTER_CLR = "#E74C3C"
        OUTPUT_CLR = "#2ECC71"
        ACCENT_CLR = "#F39C12"

        # ── helper: cuboid with visible grid on front face ───
        def gridded_cuboid(h, w, d, color, pos=ORIGIN, cs=0.35):
            fw, fh = w * cs, h * cs
            front = Rectangle(width=fw, height=fh)
            front.set_fill(color, opacity=0.85)
            front.set_stroke(WHITE, width=2)
            front.move_to(pos)
            lines = VGroup()
            for r in range(1, h):
                lines.add(Line(
                    pos + LEFT * fw / 2 + UP * (fh / 2 - r * cs),
                    pos + RIGHT * fw / 2 + UP * (fh / 2 - r * cs),
                    stroke_color=WHITE, stroke_width=1.0,
                    stroke_opacity=0.5,
                ))
            for c in range(1, w):
                lines.add(Line(
                    pos + UP * fh / 2 + RIGHT * (c * cs - fw / 2),
                    pos + DOWN * fh / 2 + RIGHT * (c * cs - fw / 2),
                    stroke_color=WHITE, stroke_width=1.0,
                    stroke_opacity=0.5,
                ))
            dx = min(d, 20) * cs * 0.45
            dy = min(d, 20) * cs * 0.28
            top = Polygon(
                front.get_corner(UL), front.get_corner(UR),
                front.get_corner(UR) + RIGHT * dx + UP * dy,
                front.get_corner(UL) + RIGHT * dx + UP * dy,
            )
            top.set_fill(interpolate_color(color, WHITE, 0.3), opacity=0.85)
            top.set_stroke(WHITE, width=2)
            right_f = Polygon(
                front.get_corner(UR), front.get_corner(DR),
                front.get_corner(DR) + RIGHT * dx + UP * dy,
                front.get_corner(UR) + RIGHT * dx + UP * dy,
            )
            right_f.set_fill(interpolate_color(color, BLACK, 0.2),
                             opacity=0.85)
            right_f.set_stroke(WHITE, width=2)
            return VGroup(front, lines, top, right_f)

        # ── plain cuboid (no grid) for real-network section ──
        def plain_cuboid(h, w, d, color, pos=ORIGIN, cs=0.04,
                         depth_scale=0.4):
            fw, fh = w * cs, h * cs
            front = Rectangle(width=fw, height=fh)
            front.set_fill(color, opacity=0.85)
            front.set_stroke(WHITE, width=2)
            front.move_to(pos)
            dx = min(d, 30) * cs * depth_scale
            dy = min(d, 30) * cs * depth_scale * 0.6
            top = Polygon(
                front.get_corner(UL), front.get_corner(UR),
                front.get_corner(UR) + RIGHT * dx + UP * dy,
                front.get_corner(UL) + RIGHT * dx + UP * dy,
            )
            top.set_fill(interpolate_color(color, WHITE, 0.3), opacity=0.85)
            top.set_stroke(WHITE, width=2)
            right_f = Polygon(
                front.get_corner(UR), front.get_corner(DR),
                front.get_corner(DR) + RIGHT * dx + UP * dy,
                front.get_corner(UR) + RIGHT * dx + UP * dy,
            )
            right_f.set_fill(interpolate_color(color, BLACK, 0.2),
                             opacity=0.85)
            right_f.set_stroke(WHITE, width=2)
            return VGroup(front, top, right_f)

        # ── TITLE ────────────────────────────────────────────
        title = Text("Standard Convolution", font_size=69, weight=BOLD)
        self.play(Write(title), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(title), run_time=0.5)

        # ══════════════════════════════════════════════════════
        # PART 1 — Single filter sliding through input
        # ══════════════════════════════════════════════════════
        CS = 0.40

        # Symmetric layout: input left, output right, filter starts center
        inp_pos = LEFT * 3.5 + UP * 0.4
        inp = gridded_cuboid(5, 5, 4, INPUT_CLR, inp_pos, cs=CS)
        inp_lbl = Text("5x5x4", font_size=40,
                        weight=BOLD, color=INPUT_CLR)
        inp_lbl.next_to(inp, DOWN, buff=0.33)
        inp_tag = Text("Input", font_size=34, weight=BOLD, color=GREY_A)
        inp_tag.next_to(inp_lbl, DOWN, buff=0.33)

        self.play(GrowFromCenter(inp), Write(inp_lbl),
                  FadeIn(inp_tag), run_time=0.8)
        self.wait(0.4)


        # Filter — centered, same Y
        filt_start = UP * 0.4
        filt = gridded_cuboid(3, 3, 4, FILTER_CLR, filt_start, cs=CS)
        filt.set_z_index(10)
        filt_lbl = Text("3x3x4", font_size=40,
                         weight=BOLD, color=FILTER_CLR)
        filt_lbl.next_to(filt, DOWN, buff=0.33)
        filt_tag = Text("Filter", font_size=34, weight=BOLD, color=GREY_A)
        filt_tag.next_to(filt_lbl, DOWN, buff=0.33)

        self.play(FadeIn(filt, shift=LEFT * 0.5),
                  Write(filt_lbl), FadeIn(filt_tag), run_time=0.8)

        depth_note = Text("Filter depth = Input channels = 4",
                          font_size=44, weight=BOLD, color=YELLOW)
        depth_note.to_edge(UP, buff=0.5).shift(DOWN*0.47)
        self.play(FadeIn(depth_note), run_time=0.4)
        self.wait(0.8)
        self.play(FadeOut(depth_note), run_time=0.3)

        # Output grid — right side
        OCS = 0.40
        out_pos = RIGHT * 3.5 + UP * 0.4
        out_cells = VGroup()
        for r in range(3):
            for c in range(3):
                sq = Square(side_length=OCS)
                sq.set_fill(BLACK, opacity=0.3)
                sq.set_stroke(WHITE, width=1.5)
                sq.move_to(out_pos + RIGHT * (c - 1) * OCS
                           + DOWN * (r - 1) * OCS)
                out_cells.add(sq)
        out_lbl = Text("3x3", font_size=32,
                        weight=BOLD, color=OUTPUT_CLR)
        out_lbl.next_to(out_cells, DOWN, buff=0.399)
        out_tag = Text("Output", font_size=34, weight=BOLD, color=GREY_A)
        out_tag.next_to(out_lbl, DOWN, buff=0.33)

        self.play(FadeIn(out_cells), Write(out_lbl),
                  FadeIn(out_tag), self.camera.frame.animate.scale(0.8),run_time=0.6)


        # Make input translucent
        inp_top_c = interpolate_color(INPUT_CLR, WHITE, 0.3)
        inp_side_c = interpolate_color(INPUT_CLR, BLACK, 0.2)

        self.play(
            inp[0].animate.set_fill(INPUT_CLR, opacity=0.20),
            inp[1].animate.set_stroke(opacity=0.15),
            inp[2].animate.set_fill(inp_top_c, opacity=0.20),
            inp[3].animate.set_fill(inp_side_c, opacity=0.20),
            run_time=0.5,
        )

        # Slide filter into input — TransformFromCopy to output
        front_off = filt.get_center() - filt[0].get_center()

        def filt_target(r, c):
            fx = inp_pos[0] + (c - 1) * CS
            fy = inp_pos[1] + (1 - r) * CS
            return np.array([fx, fy, 0.0]) + front_off

        self.play(
            filt.animate.move_to(filt_target(0, 0)),
            FadeOut(filt_lbl), FadeOut(filt_tag),
            run_time=0.8,
        )

        idx = 0
        for r in range(3):
            for c in range(3):
                if idx > 0:
                    self.play(
                        filt.animate.move_to(filt_target(r, c)),
                        run_time=0.28 if idx < 4 else 0.16,
                    )
                # TransformFromCopy: copy of filter flies to output cell
                self.remove(out_cells[idx])
                out_cells[idx].set_fill(OUTPUT_CLR, opacity=0.85)
                self.play(
                    TransformFromCopy(filt, out_cells[idx]),
                    run_time=0.25 if idx < 4 else 0.14,
                )
                if idx == 0:
                    pass
                idx += 1

        # Restore input
        self.play(FadeOut(filt), run_time=0.4)
        self.play(
            inp[0].animate.set_fill(INPUT_CLR, opacity=0.85),
            inp[1].animate.set_stroke(opacity=0.5),
            inp[2].animate.set_fill(inp_top_c, opacity=0.85),
            inp[3].animate.set_fill(inp_side_c, opacity=0.85),
            run_time=0.4,
        )

        self.play(
            VGroup(out_cells, out_lbl, out_tag).animate.shift(LEFT),
            VGroup(inp, inp_lbl, inp_tag).animate.shift(RIGHT*0.99)
        )

        self.wait(2)


        # ══════════════════════════════════════════════════════
        # PART 2 — Multiple filters + FLOPs with braces
        # ══════════════════════════════════════════════════════
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        self.camera.frame.shift(UP*0.68).scale(1.09)

        Y_ROW = 1.5

        # Input at -5, filters centered, output at +5 — filters IN BETWEEN
        inp2 = gridded_cuboid(5, 5, 4, INPUT_CLR,
                               np.array([-5.0, Y_ROW, 0]), cs=0.22)
        inp2.shift(RIGHT*1.73)
        inp2_lbl = Text("5 x 5 x 4", font_size=30, weight=BOLD,
                          color=INPUT_CLR)
        inp2_lbl.next_to(inp2, DOWN, buff=0.22)

        # 5 filters stacked vertically — centered between input and output
        f_cols = ["#E74C3C", "#E91E63", "#FF5722", "#FF9800", "#795548"]
        fstack = VGroup()
        for i in range(5):
            fc = gridded_cuboid(3, 3, 4, f_cols[i], ORIGIN, cs=0.15)
            fstack.add(fc)
        fstack.arrange(DOWN, buff=0.22)
        fstack.move_to(np.array([0.0, Y_ROW, 0]))
        for i, fc in enumerate(fstack):
            fc.set_z_index(5 - i)
        fstack_lbl = Text("(3 x 3 x 4 each)", font_size=22,
                           weight=BOLD, color=FILTER_CLR)
        fstack_lbl.next_to(fstack, DOWN, buff=0.22)

        # Output cuboid at +5
        out2 = gridded_cuboid(3, 3, 5, OUTPUT_CLR,
                               np.array([5.0, Y_ROW, 0]), cs=0.30)
        out2.shift(LEFT*1.89)
        out2_lbl = Text("3 x 3 x 5", font_size=30, weight=BOLD,
                          color=OUTPUT_CLR)
        out2_lbl.next_to(out2, DOWN, buff=0.22)

        # Animate all three together
        self.play(
            GrowFromCenter(inp2), Write(inp2_lbl), 
            run_time=0.7,
        )
        self.play(
            LaggedStart(*[GrowFromCenter(f) for f in fstack],
                         lag_ratio=0.06),
            Write(fstack_lbl),
            run_time=0.9,
        )
        self.play(
            GrowFromCenter(out2), Write(out2_lbl), 
            run_time=0.7,
        )

        self.wait(2)


        # ── FLOPs with labeled braces ────────────────────────
        BY = -1.5

        t_fs = Text("3 x 3 x 4", font_size=28, weight=BOLD, color=FILTER_CLR)
        t_x1 = Text("x", font_size=26, color=GREY_A)
        t_os = Text("3 x 3", font_size=28, weight=BOLD, color=OUTPUT_CLR)
        t_x2 = Text("x", font_size=26, color=GREY_A)
        t_nf = Text("5", font_size=28, weight=BOLD, color=ACCENT_CLR)

        mul_row = VGroup(t_fs, t_x1, t_os, t_x2, t_nf)
        mul_row.arrange(RIGHT, buff=0.35)
        mul_row.move_to(np.array([0, BY, 0])).shift(LEFT*0.5)

        br_fs = Brace(t_fs, DOWN, buff=0.1)
        br_fs.set_color(FILTER_CLR)
        br_fs_lbl = Text("Filter Size", font_size=24,
                          weight=BOLD, color=FILTER_CLR)
        br_fs_lbl.next_to(br_fs, DOWN, buff=0.08)

        br_os = Brace(t_os, DOWN, buff=0.1)
        br_os.set_color(OUTPUT_CLR)
        br_os_lbl = Text("Output Size", font_size=24,
                          weight=BOLD, color=OUTPUT_CLR)
        br_os_lbl.next_to(br_os, DOWN, buff=0.08)

        br_nf = Brace(t_nf, RIGHT, buff=0.1)
        br_nf.set_color(ACCENT_CLR)
        br_nf_lbl = Text("No. of Filters", font_size=22,
                          weight=BOLD, color=ACCENT_CLR)
        br_nf_lbl.next_to(br_nf, RIGHT, buff=0.08)

        # TransformFromCopy from labels to numbers
        self.play(TransformFromCopy(fstack_lbl, t_fs), run_time=0.7)
        self.play(FadeIn(t_x1), run_time=0.15)
        self.play(TransformFromCopy(out2_lbl, t_os), run_time=0.7)
        self.play(FadeIn(t_x2), run_time=0.15)
        self.play(TransformFromCopy(fstack_lbl, t_nf), run_time=0.7)

        self.play(
            GrowFromCenter(br_fs), FadeIn(br_fs_lbl),
            GrowFromCenter(br_os), FadeIn(br_os_lbl),
            GrowFromCenter(br_nf), FadeIn(br_nf_lbl),
            run_time=0.6,
        )
        self.wait(1.5)

        # Total
        total = Text("1,620", font_size=50,
                      weight=BOLD, color="#F1C40F").move_to(VGroup(t_x1, t_x2, t_fs, t_os, t_nf)).shift(DOWN*0.44)
        self.play(ReplacementTransform(VGroup(t_x1, t_x2, t_fs), total), 
        FadeOut(VGroup(br_fs, br_os, br_nf, br_fs_lbl, br_os_lbl, br_nf_lbl, t_os, t_nf) ,run_time=0.7))
        
        self.wait(1.3)



        # ══════════════════════════════════════════════════════
        # PART 3 — Real networks (deep plain cuboids, no grids)
        # ══════════════════════════════════════════════════════
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        self.camera.frame.set_height(9).move_to(DOWN * 0.3)

        real_title = Text("In Real Networks...", font_size=60,
                           weight=BOLD, color=GREY_A)
        real_title.to_edge(UP, buff=0.5).shift(DOWN*0.3)
        self.play(Write(real_title), run_time=0.7)

        # Deep cuboids — no grids, no dimension braces
        real_inp = plain_cuboid(15, 15, 25, INPUT_CLR,
                                 LEFT * 3.5 + UP * 0.3, cs=0.09,
                                 depth_scale=0.55).shift(DOWN*0.34+LEFT*0.7)
        real_inp_lbl = Text("56x56x256", font_size=38,
                             weight=BOLD, color=INPUT_CLR)
        real_inp_lbl.next_to(real_inp, DOWN, buff=0.45)

        real_filt_lbl = Text("128 Filters", font_size=38,
                              weight=BOLD, color=FILTER_CLR)
        real_filt_sub = Text("(3x3x256 each)", font_size=32,
                              weight=BOLD, color=FILTER_CLR)
        real_filt_group = VGroup(real_filt_lbl, real_filt_sub)
        real_filt_group.arrange(DOWN, buff=0.45)
        real_filt_group.next_to(real_inp, RIGHT, buff=0.65)

        real_out = plain_cuboid(14, 14, 15, OUTPUT_CLR,
                                 RIGHT * 3.5 + UP * 0.3, cs=0.09,
                                 depth_scale=0.55)
        real_out_lbl = Text("54x54x128", font_size=38,
                             weight=BOLD, color=OUTPUT_CLR)
        real_out_lbl.next_to(real_out, DOWN, buff=0.45)

        self.play(
            GrowFromCenter(real_inp), Write(real_inp_lbl),
            run_time=0.7,
        )
        self.play(
            Write(real_filt_lbl), FadeIn(real_filt_sub),
            run_time=0.6,
        )
        self.play(
            GrowFromCenter(real_out), Write(real_out_lbl),
            run_time=0.7,
        )
        self.wait(1.5)


        # TransformFromCopy -> FLOPs
        real_flops = Text(
            "~ 860 Million",
            font_size=70, weight=BOLD, color="#E74C3C",
        )
        real_flops.next_to(
            VGroup(real_inp, real_out), DOWN, buff=1.0
        ).shift(DOWN*0.48)

        self.play(
            ShowCreation(real_flops),
            run_time=1.0,
        )
        self.wait(1.3)

        per_layer = Text(
            "...and this is just ONE layer",
            font_size=50, weight=BOLD, color=GREY_A,
        )
        per_layer.next_to(real_flops, DOWN, buff=0.5)
        self.play(FadeIn(per_layer, shift=UP * 0.15), run_time=0.5)
        self.wait(0.5)

        need = Text(
            "We need a cheaper alternative!",
            font_size=50, weight=BOLD, color=YELLOW,
        ).set_color(YELLOW)
        need.next_to(per_layer, DOWN, buff=0.55)
        self.play(Write(need), self.camera.frame.animate.scale(1.1).shift(DOWN*0.65) ,run_time=0.8)
        self.wait(2)


class DepthwiseSeparableConv(Scene):
    def construct(self):
        CLR4 = ["#E74C3C", "#27AE60", "#2980B9", "#F39C12"]
        FCLR, OCLR, ACLR = "#F39C12", "#2ECC71", "#F1C40F"
        PWCLR = "#9B59B6"

        # ── TITLE ──
        title = Text("Depthwise Separable Convolution",
                      font_size=48, weight=BOLD)
        self.play(Write(title), run_time=1.0)
        self.wait(0.8)
        self.play(FadeOut(title), run_time=0.5)


        # ═══════════════════════════════════════════
        # PART 1 — Depthwise Convolution
        # ═══════════════════════════════════════════
        CS = 0.28
        N = 4

        self.camera.frame.set_height(10).move_to(ORIGIN)

        pt = Text("Depthwise Convolution", font_size=60,
                   weight=BOLD).set_color("#E74C3C")
        pt.to_edge(UP, buff=0.3)
        sub = Text("One filter per channel — no mixing",
                    font_size=50, weight=BOLD).set_color(YELLOW)
        sub.next_to(pt, DOWN, buff=0.32)
        self.play(Write(pt), run_time=0.7)
        self.play(FadeIn(sub), run_time=0.4)

        # Stacked 5x5x4 input
        OFF = np.array([0.45, -0.28, 0.0])
        stack = VGroup()
        for i in range(N):
            bg = Rectangle(width=5 * CS, height=5 * CS)
            bg.set_fill(CLR4[i], opacity=1.0)
            bg.set_stroke(width=0)
            g = make_grid(5, 5, cell_size=CS, fill_color=CLR4[i],
                          fill_opacity=1.0, stroke_color=CLR4[i],
                          stroke_width=0)
            bg.move_to(g.get_center())
            layer = VGroup(bg, g)
            layer.shift(i * OFF)
            layer.set_z_index(i)
            stack.add(layer)
        stack.move_to(LEFT * 2.5 + DOWN * 0.6)
        il = Text("5 x 5 x 4", font_size=42, weight=BOLD)
        il.next_to(stack, DOWN, buff=0.35)
        itg = Text("Input", font_size=40, weight=BOLD).set_color(GREY_A)
        itg.next_to(il, DOWN, buff=0.5)

        # Stacked 3x3 filters
        FOFF = np.array([0.35, -0.22, 0.0])
        fstk = VGroup()
        for i in range(N):
            fbg = Rectangle(width=3 * CS, height=3 * CS)
            fbg.set_fill(CLR4[i], opacity=1.0)
            fbg.set_stroke(width=0)
            f = make_grid(3, 3, cell_size=CS, fill_color=CLR4[i],
                          fill_opacity=1.0, stroke_color=CLR4[i],
                          stroke_width=0)
            fbg.move_to(f.get_center())
            flayer = VGroup(fbg, f)
            flayer.shift(i * FOFF)
            flayer.set_z_index(i)
            fstk.add(flayer)
        fstk.move_to(RIGHT * 2.5 + DOWN * 0.6)
        fl = Text("3 x 3 each", font_size=42, weight=BOLD).set_color(FCLR)
        fl.next_to(fstk, DOWN, buff=0.35)
        ftg = Text("4 Filters", font_size=40, weight=BOLD).set_color(GREY_A)
        ftg.next_to(fl, DOWN, buff=0.5)

        self.play(GrowFromCenter(stack), Write(il),
                  FadeIn(itg), run_time=0.8)
        self.play(GrowFromCenter(fstk), Write(fl),
                  FadeIn(ftg), run_time=0.8)
        self.wait(1.6)


        # Fade out title + subtitle BEFORE spreading
        self.play(FadeOut(sub), FadeOut(pt), run_time=0.4)

        self.camera.frame.save_state()


        Y = [3.2, 1.4, -0.4, -2.2]
        XC, XF, XO = -3.5, -0.8, 1.0

        anims = []
        for i in range(N):
            anims.append(stack[i].animate.move_to(
                np.array([XC, Y[i], 0])))
            anims.append(fstk[i].animate.move_to(
                np.array([XF, Y[i], 0])))
        anims += [FadeOut(il), FadeOut(itg), FadeOut(fl), FadeOut(ftg)]
        self.play(*anims, self.camera.frame.animate.scale(0.82).shift(LEFT*1.65+UP*0.44) ,run_time=1.0)

        # Channel labels
        chl = VGroup()
        for i in range(N):
            l = Text("Channel " + str(i + 1) + " ", font_size=42,
                     weight=BOLD).set_color(CLR4[i])
            l.next_to(stack[i], LEFT, buff=0.35)
            chl.add(l)
        self.play(*[FadeIn(l) for l in chl], run_time=0.9)

        # Reveal grid cells on the spread-out channels
        self.play(
            *[stack[i][1].animate.set_stroke(WHITE, width=1.5)
              for i in range(N)],
            *[fstk[i][1].animate.set_stroke(WHITE, width=1.5)
              for i in range(N)],
            run_time=0.5)

        # Output grids (3x3 each, empty)
        ogs = VGroup()
        for i in range(N):
            cells = VGroup()
            bx = XO - 1.0 * CS
            by = Y[i] + 1.0 * CS
            for r in range(3):
                for c in range(3):
                    sq = Square(side_length=CS)
                    sq.set_fill(BLACK, opacity=0.25)
                    sq.set_stroke(WHITE, width=1.0)
                    sq.move_to(np.array([bx + c * CS,
                                         by - r * CS, 0]))
                    cells.add(sq)
            ogs.add(cells)

        ols = VGroup()
        for i in range(N):
            l = Text("3 x 3", font_size=42, weight=BOLD).set_color(CLR4[i])
            l.next_to(ogs[i], RIGHT, buff=0.6)
            ols.add(l)
        self.play(*[FadeIn(g) for g in ogs],
                  *[FadeIn(l) for l in ols], run_time=0.9)

        # ── SIMULTANEOUS convolution on all 4 channels ──
        for i in range(N):
            fstk[i].set_z_index(10)

        self.play(*[c.animate.set_fill(opacity=0.3)
                    for ch in range(N) for c in stack[ch]],
                  run_time=0.5)

        def fp(ch, r, c):
            return np.array([XC + (c - 1) * CS,
                             Y[ch] + (1 - r) * CS, 0])

        # Move all 4 filters to first position simultaneously
        self.play(*[fstk[i].animate.move_to(fp(i, 0, 0))
                    for i in range(N)], run_time=0.5)

        for idx in range(9):
            r, c = divmod(idx, 3)
            if idx > 0:
                t = 0.15 if idx < 4 else 0.06
                self.play(*[fstk[i].animate.move_to(fp(i, r, c))
                            for i in range(N)], run_time=0.25)
            for i in range(N):
                ogs[i][idx].set_fill(CLR4[i], opacity=0.7)
            t2 = 0.12 if idx < 4 else 0.04
            self.play(*[TransformFromCopy(fstk[i], ogs[i][idx])
                        for i in range(N)], run_time=0.25)

        # Restore channels + move filters back
        self.play(
            *[fstk[i].animate.move_to(np.array([XF, Y[i], 0]))
              for i in range(N)],
            *[c.animate.set_fill(opacity=1.0)
              for ch in range(N) for c in stack[ch]],
            run_time=0.4)
        self.wait(1.5)


        # ── Stack back together + show operations ──
        self.play(FadeOut(chl), FadeOut(ols), run_time=0.4)



        U_INP, U_FILT, U_OUT = "#3498DB", "#E67E22", "#2ECC71"
        inp_pos = LEFT * 4.0 + DOWN * 0.3
        filt_pos = DOWN * 0.3
        out_pos = RIGHT * 4.0 + DOWN * 0.3
        SOFF = np.array([0.35, -0.22, 0.0])

        anims = []
        for i in range(N):
            stack[i].set_z_index(i)
            fstk[i].set_z_index(i)
            ogs[i].set_z_index(i)
            anims.append(stack[i].animate.move_to(inp_pos + i * SOFF)
                         .set_stroke(width=0))
            anims.append(fstk[i].animate.move_to(filt_pos + i * SOFF)
                         .set_stroke(width=0))
            anims.append(ogs[i].animate.move_to(out_pos + i * SOFF)
                         .set_stroke(width=0))
        self.play(*anims, self.camera.frame.animate.restore().scale(0.82).shift(DOWN*1.75+RIGHT*0.311) ,run_time=1.0)

        # Compact dimensions below each stack
        inp_dim = Text("5x5x4", font_size=45, weight=BOLD)
        inp_dim.next_to(stack, DOWN, buff=0.44).shift(LEFT*0.85)
        filt_dim = Text("3x3x4", font_size=45, weight=BOLD).set_color(U_FILT)
        filt_dim.next_to(fstk, DOWN, buff=0.44).shift(LEFT*1.7)
        out_dim = Text("3x3x4", font_size=45, weight=BOLD).set_color(U_OUT)
        out_dim.next_to(ogs, DOWN, buff=0.44)

        self.play(FadeIn(inp_dim), FadeIn(filt_dim), FadeIn(out_dim), run_time=0.6)

        # Star between input and filter stacks
        star = Tex(r"\ast").scale(2.5).set_color(YELLOW)
        mid_x = (inp_pos[0] + filt_pos[0]) / 2
        star.move_to(np.array([mid_x, DOWN[1] * 0.3, 0])).shift(RIGHT*0.7+DOWN*0.33)
        self.play(FadeIn(star, scale=1.5), run_time=0.5)

        # Arrow from filter to output
        equals_to = Tex(r"=").scale(2.29).set_color(YELLOW)
        equals_to.move_to(np.array([mid_x, DOWN[1] * 0.3, 0])).shift(RIGHT*4.49+DOWN*0.33)
        self.play(FadeIn(equals_to, scale=1.5), run_time=0.5)
        self.wait(1.5)


        # TransformFromCopy dims into equation
        eq_fs = Text("3 x 3", font_size=34, weight=BOLD).set_color(U_FILT)
        eq_x1 = Text("x", font_size=28).set_color(GREY_A)
        eq_os = Text("3 x 3", font_size=34, weight=BOLD).set_color(U_OUT)
        eq_x2 = Text("x", font_size=28).set_color(GREY_A)
        eq_ch = Text("4", font_size=34, weight=BOLD).set_color(WHITE)
        eq_eq = Text("=", font_size=28).set_color(GREY_A)
        eq_tot = Text("324", font_size=36, weight=BOLD).set_color(YELLOW)

        eqrow = VGroup(eq_fs, eq_x1, eq_os, eq_x2, eq_ch, eq_eq, eq_tot)
        eqrow.arrange(RIGHT, buff=0.25)
        eqrow.to_edge(DOWN, buff=1.4).shift(DOWN*1.7+RIGHT*0.2).scale(1.6)

        self.play(
            TransformFromCopy(filt_dim, eq_fs),
            TransformFromCopy(out_dim, eq_os),
            TransformFromCopy(inp_dim, eq_ch),
            run_time=0.8)
        self.play(FadeIn(eq_x1), FadeIn(eq_x2), run_time=0.9)
        self.play(FadeIn(eq_eq), Write(eq_tot), run_time=0.9)

        self.wait(1)

        # Braces with labels explaining each term
        br_fs = Brace(eq_fs, DOWN, buff=0.1)
        lb_fs = Text("Filter Size", font_size=28, weight=BOLD).set_color(U_FILT)
        lb_fs.next_to(br_fs, DOWN, buff=0.29)

        br_os = Brace(eq_os, DOWN, buff=0.1)
        lb_os = Text("Output Size", font_size=28, weight=BOLD).set_color(U_OUT)
        lb_os.next_to(br_os, DOWN, buff=0.29)

        br_ch = Brace(eq_ch, DOWN, buff=0.1)
        lb_ch = Text("Channels", font_size=28, weight=BOLD).set_color(WHITE)
        lb_ch.next_to(br_ch, DOWN, buff=0.29)

        self.play(
            GrowFromCenter(br_fs), FadeIn(lb_fs),
            GrowFromCenter(br_os), FadeIn(lb_os),
            GrowFromCenter(br_ch), FadeIn(lb_ch),
            self.camera.frame.animate.shift(DOWN*0.7),
            run_time=0.6)
        self.wait(1.5)


        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

        # ═══════════════════════════════════════════
        # PART 2 — Pointwise (1x1) Convolution
        # ═══════════════════════════════════════════
        self.camera.frame.set_height(9).move_to(ORIGIN)

        pt2 = Text("Pointwise (1x1) Convolution", font_size=54,
                    weight=BOLD).set_color(PWCLR)
        pt2.to_edge(UP, buff=0.4)
        d2 = Text("Mix channels with 1x1 filters",
                   font_size=40, weight=BOLD).set_color(YELLOW)
        d2.next_to(pt2, DOWN, buff=0.35)
        self.play(Write(pt2), FadeIn(d2), run_time=0.7)

        PCS = 0.55

        # Input: 3x3x4 cuboid
        pw_inp = make_cuboid_block(3, 3, 4, CLR4,
                                    pos=LEFT * 4.2 + DOWN * 0.9,
                                    cs=PCS)
        pwil = Text("3 x 3 x 4", font_size=34, weight=BOLD)
        pwil.next_to(pw_inp, DOWN, buff=0.35)
        pwit = Text("From Depthwise", font_size=34,
                     weight=BOLD).set_color(GREY_A)
        pwit.next_to(pwil, DOWN, buff=0.25)

        # Filter: 1x1x4 cuboid — all MAROON, single color
        pw_filt = make_cuboid_block(1, 1, 4, [YELLOW] * 4,
                                     pos=DOWN * 0.9,
                                     cs=PCS)
        pw_filt.set_z_index(10)
        pwfl = Text("1 x 1 x 4", font_size=32, weight=BOLD)
        pwfl.next_to(pw_filt, DOWN, buff=0.35)

        # Output: flat 3x3 grid (2D only)
        out_pos = RIGHT * 4.2 + DOWN * 0.9
        pw_out = VGroup()
        for r in range(3):
            for c in range(3):
                sq = Square(side_length=PCS)
                sq.set_fill(BLACK, opacity=0.25)
                sq.set_stroke(WHITE, width=1.5)
                sq.move_to(out_pos + RIGHT * (c - 1) * PCS
                           + DOWN * (r - 1) * PCS)
                pw_out.add(sq)
        pwol = Text("3 x 3 x 1", font_size=32, weight=BOLD)
        pwol.next_to(pw_out, DOWN, buff=0.35)

        self.play(GrowFromCenter(pw_inp), Write(pwil),
                  FadeIn(pwit), run_time=0.7)
        self.play(GrowFromCenter(pw_filt), Write(pwfl),
                  run_time=0.6)
        self.play(FadeIn(pw_out), Write(pwol), run_time=0.5)
        self.wait(1.5)


        # Save filter home position + front-face offset
        pw_filt_home = pw_filt.get_center().copy()
        pw_off = pw_filt.get_center() - pw_filt[0].get_center()

        # Fade labels, zoom in for the sliding
        self.play(FadeOut(pwfl), FadeOut(d2), pt2.animate.shift(DOWN*0.75) ,run_time=0.3)
        mid_x = (pw_inp.get_center()[0] + pw_out.get_center()[0]) / 2
        self.play(
            self.camera.frame.animate.set_height(8)
                .move_to(np.array([mid_x, -0.1, 0])),
            pw_inp[0].animate.set_fill(opacity=0.4),
            run_time=0.5)

        # Slide 1x1x4 filter through each of the 9 input positions
        for idx in range(9):
            target = pw_inp[0][idx].get_center() + pw_off
            t = 0.25 if idx < 4 else 0.12
            self.play(pw_filt.animate.move_to(target), run_time=t)
            self.remove(pw_out[idx])
            pw_out[idx].set_fill(PWCLR, opacity=0.7)
            t2 = 0.18 if idx < 4 else 0.08
            self.play(TransformFromCopy(pw_filt, pw_out[idx]),
                      run_time=t2)

        # Restore input + move filter back + zoom out
        self.play(
            pw_inp[0].animate.set_fill(opacity=0.85),
            pw_filt.animate.move_to(pw_filt_home),
            self.camera.frame.animate.set_height(9).move_to(ORIGIN).shift(DOWN*0.7),
            run_time=0.6)
        pwfl2 = Text("1 x 1 x 4", font_size=32, weight=BOLD)
        pwfl2.next_to(pw_filt, DOWN, buff=0.35)
        self.play(FadeIn(pwfl2), run_time=0.3)

        rpt = Text("Repeat with N filters -> 3 x 3 x N output",
                    font_size=40, weight=BOLD).set_color(YELLOW)
        rpt.to_edge(DOWN, buff=1.35).shift(DOWN*1.7)
        self.play(FadeIn(rpt), run_time=0.4)
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)



        # ═══════════════════════════════════════════
        # PART 3 — Cost Comparison
        # ═══════════════════════════════════════════
        self.camera.frame.set_height(9).move_to(ORIGIN)

        pt3 = Text("Cost Comparison", font_size=64,
                    weight=BOLD).set_color(YELLOW)
        pt3.to_edge(UP, buff=0.4)
        self.play(Write(pt3), run_time=0.7)

        std_h = Text("Standard Convolution", font_size=40,
                      weight=BOLD).set_color(RED)
        std_c = Text("3x3x4  x  3x3  x  5 filters  =  1,620",
                      font_size=30).set_color(RED)
        std_g = VGroup(std_h, std_c)
        std_g.arrange(DOWN, buff=0.44, aligned_edge=LEFT)

        ds_h = Text("Depthwise Separable", font_size=40,
                     weight=BOLD).set_color(GREEN)
        dw_c = Text("Depthwise:  3x3  x  3x3  x  4  =  324", weight=BOLD,
                     font_size=30).set_color(TEAL_B)
        pw_c_txt = Text("Pointwise:  1x1x4  x  3x3  x  5  =  180", weight=BOLD,
                         font_size=30).set_color(PWCLR)
        ds_t = Text("Total:  324 + 180  =  504", weight=BOLD,
                     font_size=30).set_color(GREEN)
        ds_g = VGroup(ds_h, dw_c, pw_c_txt, ds_t)
        ds_g.arrange(DOWN, buff=0.44, aligned_edge=LEFT)

        sav = Text("~ 3.2x cheaper!", font_size=40,
                    weight=BOLD).set_color(YELLOW)

        all_g = VGroup(std_g, ds_g, sav)
        all_g.arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        all_g.move_to(DOWN * 0.74)

        for m in [std_h, std_c, ds_h, dw_c, pw_c_txt, ds_t, sav]:
            self.play(FadeIn(m, shift=RIGHT * 0.2), run_time=0.4)

        box = SurroundingRectangle(sav, buff=0.15,
                                    stroke_width=3).set_color(YELLOW)
        self.play(ShowCreation(box), run_time=0.5)
        self.play(sav.animate.scale(1.1), box.animate.scale(1.1),
                  rate_func=there_and_back, run_time=0.5)
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        
        # ═══════════════════════════════════════════
        # PART 4 — General Formula
        # ═══════════════════════════════════════════
        self.camera.frame.set_height(9).move_to(ORIGIN)

        form_title = Text("General Formula", font_size=64,
                          weight=BOLD).set_color(YELLOW)
        form_title.to_edge(UP, buff=0.5)
        self.play(Write(form_title), run_time=0.7)

        # Formula: Cost Ratio = 1/N + 1/K²
        f_math = Tex(r"Cost \ Ratio \ = \   \frac{1}{N}", "\ + \ ", r"\frac{1}{K^2}")
        f_math.scale(2)
        formula = VGroup(f_math).arrange(RIGHT, buff=0.3)
        formula.move_to(UP * 0.8)
        self.play(Write(formula), run_time=1.0)

        n_label = Text("N = Number of output filters", weight=BOLD,
                        font_size=50).set_color(PURPLE)
        k_label = Text("K = Spatial filter size  (K x K)", weight=BOLD,
                        font_size=50).set_color(MAROON)
        labels = VGroup(n_label, k_label)
        labels.arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        labels.next_to(formula, DOWN, buff=1)
        self.play(FadeIn(n_label), run_time=0.4)
        self.play(FadeIn(k_label), run_time=0.4)
        self.wait(1.8)

        self.camera.frame.save_state()


        # Plug in our values
        ex_math = Tex(r"\frac{1}{5}", r"\ +\ ", r"\frac{1}{9}",
                      r"\ \approx\ 0.31")
        ex_math.scale(2)
        ex_math.move_to(labels).shift(RIGHT*0.53+DOWN*0.07)
        self.play(Write(ex_math), FadeOut(labels),run_time=1.0)
        self.wait(2)

        meaning = Text("Only ~31% of the computation needed!",
                        font_size=47, weight=BOLD).set_color("#2ECC71")
        meaning.next_to(ex_math, DOWN, buff=0.4).shift(LEFT*0.25)
        self.play(FadeIn(meaning), self.camera.frame.animate.shift(DOWN*0.6) ,run_time=0.5)
        self.wait(2.0)


class MobileNetv1(Scene):
    def construct(self):
        CLR = ["#E74C3C", "#27AE60", "#2980B9"]
        DW_CLR = ["#E67E22", "#D35400", "#C0392B"]
        PW_CLR = ["#9B59B6", "#8E44AD", "#7D3C98"]

        self.camera.frame.set_height(10).move_to(ORIGIN)

        CS = 0.28
        OFF = np.array([0.35, -0.22, 0.0])

        # ── TITLE (high above everything) ──
        title = Text("MobileNet V1", font_size=60, weight=BOLD)
        title.to_edge(UP, buff=0.3)

        # ═══════════════════════════════════════════
        # INPUT STACK  (represents 224×224×3)
        # ═══════════════════════════════════════════
        inp_stack = VGroup()
        for i in range(3):
            bg = Rectangle(width=5 * CS, height=5 * CS)
            bg.set_fill(CLR[i], opacity=1.0)
            bg.set_stroke(width=0)
            g = make_grid(5, 5, cell_size=CS, fill_color=CLR[i],
                          fill_opacity=1.0, stroke_color=CLR[i],
                          stroke_width=0)
            bg.move_to(g.get_center())
            layer = VGroup(bg, g)
            layer.shift(i * OFF)
            layer.set_z_index(i)
            inp_stack.add(layer)
        inp_stack.move_to(LEFT * 5.5 + DOWN * 0.5)

        inp_dim = Text("224 x 224 x 3", font_size=35, weight=BOLD, color=WHITE)
        inp_dim.next_to(inp_stack, DOWN, buff=0.35)
        inp_tag = Text("Input", font_size=40, weight=BOLD, color=GREY_A)
        inp_tag.next_to(inp_dim, DOWN, buff=0.35)

        # ═══════════════════════════════════════════
        # DEPTHWISE 3×3 FILTER STACK  (opacity=1)
        # ═══════════════════════════════════════════
        dw_stack = VGroup()
        for i in range(3):
            r = Rectangle(width=3 * CS, height=3 * CS)
            r.set_fill(DW_CLR[i], opacity=1.0)
            r.set_stroke(WHITE, width=1.5)
            r.shift(i * OFF * 0.7)
            r.set_z_index(i)
            dw_stack.add(r)
        dw_stack.move_to(LEFT * 1.0 + DOWN * 0.5)

        dw_dim = Text("3 x 3 Depthwise", font_size=30, weight=BOLD, color=WHITE)
        dw_dim.next_to(dw_stack, DOWN, buff=0.35)

        # BN + ReLU label above DW
        dw_bn = Text("BN + ReLU", font_size=32, weight=BOLD, color="#2ECC71")
        dw_bn.next_to(dw_stack, UP, buff=0.42)

        # ═══════════════════════════════════════════
        # 1×1 POINTWISE CONV — CUBOID
        # ═══════════════════════════════════════════
        pw_cuboid = make_cuboid_block(1, 1, 3, PW_CLR,
                                       pos=ORIGIN, cs=0.55)
        for part in pw_cuboid:
            for sub in part:
                sub.set_fill(opacity=1.0)
        pw_cuboid.move_to(RIGHT * 2.8 + DOWN * 0.5)

        pw_dim = Text("1 x 1 Conv", font_size=30, weight=BOLD, color=WHITE)
        pw_dim.next_to(pw_cuboid, DOWN, buff=0.35)

        # BN + ReLU label above PW
        pw_bn = Text("BN + ReLU", font_size=32, weight=BOLD, color="#2ECC71")
        pw_bn.next_to(pw_cuboid, UP, buff=0.42)

        # ═══════════════════════════════════════════
        # HORIZONTAL ARROWS  (precisely same y)
        # ═══════════════════════════════════════════
        y_arr = inp_stack.get_center()[1]

        arr1 = Arrow(
            np.array([inp_stack.get_right()[0] + 0.2, y_arr, 0]),
            np.array([dw_stack.get_left()[0] - 0.2, y_arr, 0]),
            buff=0, thickness=3, color=WHITE,
        )
        arr2 = Arrow(
            np.array([dw_stack.get_right()[0] + 0.2, y_arr, 0]),
            np.array([pw_cuboid.get_left()[0] - 0.2, y_arr, 0]),
            buff=0, thickness=3, color=WHITE,
        )

        # ═══════════════════════════════════════════
        # ROUNDED RECTANGLE  (encloses DW + BN + arrow + 1×1 + BN)
        # ═══════════════════════════════════════════
        box_group = VGroup(dw_stack, pw_cuboid, arr2, dw_dim, pw_dim,
                           dw_bn, pw_bn)
        bl = box_group.get_left()[0] - 0.5
        br = box_group.get_right()[0] + 0.5
        bt = box_group.get_top()[1] + 0.4
        bb = box_group.get_bottom()[1] - 0.35
        box = RoundedRectangle(
            width=br - bl, height=bt - bb,
            corner_radius=0.25, stroke_width=3, stroke_color=YELLOW,
        )
        box.set_fill(YELLOW, opacity=0.05)
        box.move_to(np.array([(bl + br) / 2, (bt + bb) / 2, 0]))

        times_label = Text(
            "x 13", font_size=58, weight=BOLD, color=YELLOW,
        )
        times_label.next_to(box, DOWN, buff=0.62)

        # ═══════════════════════════════════════════
        # TAIL:  Avg Pool → FC → Softmax
        # ═══════════════════════════════════════════
        TAIL_CLR = "#1ABC9C"
        tail_fs = 30
        TAIL_BUFF = 1.1   # generous spacing

        avg_pool = Text("Avg Pool", font_size=tail_fs, weight=BOLD,
                         color=TAIL_CLR)
        fc_layer = Text("FC", font_size=tail_fs, weight=BOLD,
                         color=TAIL_CLR)
        softmax = Text("Softmax", font_size=tail_fs, weight=BOLD,
                        color=TAIL_CLR)

        # Position them in a row after the box
        avg_pool.next_to(box, RIGHT, buff=TAIL_BUFF)
        avg_pool.set_y(y_arr)
        fc_layer.next_to(avg_pool, RIGHT, buff=TAIL_BUFF)
        fc_layer.set_y(y_arr)
        softmax.next_to(fc_layer, RIGHT, buff=TAIL_BUFF)
        softmax.set_y(y_arr)

        # Small rounded boxes behind each tail label
        def tail_box(label):
            b = SurroundingRectangle(label, buff=0.18, color=TAIL_CLR)
            b.set_fill(TAIL_CLR, opacity=0.1)
            b.round_corners(0.12)
            return b

        avg_box = tail_box(avg_pool)
        fc_box = tail_box(fc_layer)
        sm_box = tail_box(softmax)

        # Arrows between tail elements (horizontal)
        arr3 = Arrow(
            np.array([box.get_right()[0] + 0.08, y_arr, 0]),
            np.array([avg_box.get_left()[0] - 0.08, y_arr, 0]),
            buff=0, thickness=3, color=WHITE,
        )
        arr4 = Arrow(
            np.array([avg_box.get_right()[0] + 0.08, y_arr, 0]),
            np.array([fc_box.get_left()[0] - 0.08, y_arr, 0]),
            buff=0, thickness=3, color=WHITE,
        )
        arr5 = Arrow(
            np.array([fc_box.get_right()[0] + 0.08, y_arr, 0]),
            np.array([sm_box.get_left()[0] - 0.08, y_arr, 0]),
            buff=0, thickness=3, color=WHITE,
        )

        # ═══════════════════════════════════════════
        # ANIMATIONS
        # ═══════════════════════════════════════════
        self.play(Write(title), run_time=0.8)
        self.wait(0.4)

        # Input
        self.play(GrowFromCenter(inp_stack), Write(inp_dim),
                  FadeIn(inp_tag), run_time=0.8)

        self.play(self.camera.frame.animate.scale(0.7).shift(LEFT*2+DOWN))

        self.wait(2)


        # Arrow → DW filter + BN/ReLU
        self.play(GrowArrow(arr1), run_time=0.5)
        self.play(GrowFromCenter(dw_stack), Write(dw_dim),
                  FadeIn(dw_bn), run_time=0.7)

        # Arrow → 1×1 cuboid + BN/ReLU
        self.play(GrowArrow(arr2), self.camera.frame.animate.shift(RIGHT*2) ,run_time=0.5)
        self.play(GrowFromCenter(pw_cuboid), Write(pw_dim),
                  FadeIn(pw_bn), run_time=0.7)
        self.wait(2)

        # Rounded box + ×13
        self.play(ShowCreation(box), run_time=0.6)
        self.play(Write(times_label), run_time=0.5)
        self.wait(1.0)

        # Pan camera right to reveal tail
        self.play(
            self.camera.frame.animate.shift(RIGHT * 5),
            run_time=0.8,
        )

        # Tail: Avg Pool → FC → Softmax
        self.play(GrowArrow(arr3), run_time=0.4)
        self.play(FadeIn(avg_box), Write(avg_pool), run_time=0.5)
        self.play(GrowArrow(arr4), run_time=0.4)
        self.play(FadeIn(fc_box), Write(fc_layer), run_time=0.5)
        self.play(GrowArrow(arr5), self.camera.frame.animate.shift(RIGHT*2) ,run_time=0.4)
        self.play(FadeIn(sm_box), Write(softmax), run_time=0.5)
        self.wait(2.0)

        self.play(self.camera.frame.animate.shift(LEFT*4.61+UP).scale(1.63), title.animate.scale(1.7).shift(RIGHT*2.3))

        self.wait(2)


