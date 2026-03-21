"""
Why Sequence Matters — An Introduction to Sequential Data
==========================================================
Run the complete video:
    manimgl a.py SequentialDataFullVideo
    manimgl a.py SequentialDataFullVideo -w --hd
    manimgl a.py SequentialDataFullVideo -w -l

Individual scenes:
    manimgl a.py HookScene
    manimgl a.py AudioScene
    manimgl a.py StockScene
    manimgl a.py SentenceScene
    manimgl a.py TakeawayScene
"""

from manimlib import *
import numpy as np


# ── Color palette ────────────────────────────────────────────────────
WAVE_BLUE     = "#2980B9"
STOCK_GREEN   = "#27AE60"
WORD_BLUE     = "#3498DB"
SHUFFLE_RED   = "#E74C3C"
GOLD_ACCENT   = "#F1C40F"
TEAL_ACCENT   = "#1ABC9C"
DARK_BG       = "#1a1a2e"
CARD_BG       = "#2c3e50"
MEANING_GREEN = "#2ECC71"
SOFT_GRAY     = "#95A5A6"
PURPLE_ACC    = "#8E44AD"


# ── Helper functions ─────────────────────────────────────────────────

def make_word_card(word, font_size=42, fill_color=CARD_BG, text_color=WHITE,
                   stroke_color=WORD_BLUE, height=0.95, corner_radius=0.18):
    """Rounded rectangle card with centered word text."""
    label = Text(word, font_size=font_size, weight=BOLD)
    label.set_color(text_color)
    card_width = max(label.get_width() + 0.6, 1.2)

    card = RoundedRectangle(
        width=card_width, height=height, corner_radius=corner_radius,
    )
    card.set_fill(fill_color, opacity=0.9)
    card.set_stroke(stroke_color, width=3)

    label.move_to(card.get_center())
    return VGroup(card, label)


def make_scene_title(text, color=WHITE, font_size=60):
    """Scene title — clean, no underline."""
    title = Text(text, font_size=font_size, weight=BOLD)
    title.set_color(color)
    title.to_edge(UP, buff=0.45)
    return title


def make_icon_card(icon_mob, label_text, color, width=2.8, height=2.0):
    """Icon inside a subtle rounded card for consistent look."""
    card = RoundedRectangle(width=width, height=height, corner_radius=0.2)
    card.set_fill(DARK_BG, opacity=0.6)
    card.set_stroke(color, width=1.5, opacity=0.4)

    label = Text(label_text, font_size=32, weight=BOLD)
    label.set_color(color)
    icon_mob.move_to(card.get_center() + UP * 0.25)
    label.next_to(icon_mob, DOWN, buff=0.25)

    return VGroup(card, icon_mob, label)


def make_mini_waveform(width=2.0, height=0.6, color=WAVE_BLUE):
    """Small sine-wave icon."""
    wave = VMobject()
    points = []
    n = 60
    for i in range(n + 1):
        x = -width / 2 + (width / n) * i
        y = (height / 2) * np.sin(4 * PI * i / n)
        points.append([x, y, 0])
    wave.set_points_smoothly([np.array(p) for p in points])
    wave.set_stroke(color, width=3)
    return wave


def make_mini_chart(width=2.0, height=0.8, color=STOCK_GREEN):
    """Small upward trending line icon."""
    chart = VMobject()
    xs = np.linspace(0, 1, 20)
    ys = 0.3 * xs + 0.15 * np.sin(xs * 8)
    points = []
    for x, y in zip(xs, ys):
        points.append([
            -width / 2 + x * width,
            -height / 2 + y * height / 0.5,
            0
        ])
    chart.set_points_smoothly([np.array(p) for p in points])
    chart.set_stroke(color, width=3)
    return chart


def make_status_badge(text, color, font_size=28, min_width=3.2):
    """Small rounded badge (like 'Day: 5' or '$120') with background."""
    label = Text(text, font_size=font_size, weight=BOLD)
    label.set_color(WHITE)
    badge_w = max(label.get_width() + 1.0, min_width)
    bg = RoundedRectangle(
        width=badge_w,
        height=label.get_height() + 0.45,
        corner_radius=0.14,
    )
    bg.set_fill(color, opacity=0.25)
    bg.set_stroke(color, width=2)
    label.move_to(bg.get_center())
    return VGroup(bg, label)


# ── Layout validation ────────────────────────────────────────────────
MIN_PADDING = 0.05
MIN_FONT_SIZE = 24


def validate_layout(scene, label="", camera_scale=1.0):
    """Runtime validation: checks bounds, overlap, padding, font size, shape occlusion."""
    half_w = 7.1 * camera_scale
    half_h = 4.0 * camera_scale

    cam_center = scene.camera.frame.get_center()
    cx, cy = cam_center[0], cam_center[1]
    left   = cx - half_w
    right  = cx + half_w
    bottom = cy - half_h
    top    = cy + half_h

    prefix = f"[VALIDATE {label}] " if label else "[VALIDATE] "
    issues = []

    text_mobjects = []
    filled_shapes = []
    seen_ids = set()

    for mob in scene.mobjects:
        _check_recursive(mob, left, right, bottom, top, prefix, issues,
                         text_mobjects, filled_shapes, seen_ids)

    for i in range(len(text_mobjects)):
        for j in range(i + 1, len(text_mobjects)):
            m1, m2 = text_mobjects[i], text_mobjects[j]
            prox = _text_proximity(m1, m2, MIN_PADDING)
            if prox == "overlap":
                issues.append(
                    f"{prefix}OVERLAP: \"{_mob_label(m1)}\" and \"{_mob_label(m2)}\""
                )
            elif prox == "too_close":
                issues.append(
                    f"{prefix}TOO CLOSE (gap < {MIN_PADDING}): "
                    f"\"{_mob_label(m1)}\" and \"{_mob_label(m2)}\""
                )

    for shape in filled_shapes:
        for txt in text_mobjects:
            if _raw_boxes_overlap(shape, txt):
                issues.append(
                    f"{prefix}SHAPE COVERS TEXT: {type(shape).__name__} "
                    f"may obscure \"{_mob_label(txt)}\""
                )

    for iss in issues:
        _safe_print(iss)

    if not issues:
        _safe_print(f"{prefix}OK -- all mobjects in bounds, no overlap, padding OK")

    return len(issues) == 0


def _safe_print(msg):
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode('ascii', errors='replace').decode('ascii'))


def _mob_label(mob):
    raw = None
    if hasattr(mob, 'text') and isinstance(getattr(mob, 'text', None), str):
        raw = mob.text[:40]
    elif hasattr(mob, 'tex_string') and isinstance(getattr(mob, 'tex_string', None), str):
        raw = mob.tex_string[:40]
    if raw is None:
        return type(mob).__name__
    return raw.encode('ascii', errors='replace').decode('ascii')


def _is_text_or_tex(mob):
    if hasattr(mob, 'text') and isinstance(getattr(mob, 'text', None), str):
        return True
    if hasattr(mob, 'tex_string') and isinstance(getattr(mob, 'tex_string', None), str):
        return True
    return False


def _get_fill_opacity(mob):
    if hasattr(mob, 'get_fill_opacity'):
        try:
            fo = mob.get_fill_opacity()
            if hasattr(fo, '__len__'):
                return float(max(fo)) if len(fo) > 0 else 0.0
            return float(fo)
        except Exception:
            pass
    return 0.0


def _check_recursive(mob, left, right, bottom, top, prefix, issues,
                     text_list, filled_shapes, seen_ids):
    mid = id(mob)
    if mid in seen_ids:
        return
    seen_ids.add(mid)

    class_name = type(mob).__name__

    SKIP_TYPES = {"CameraFrame", "Axes", "NumberLine", "NumberPlane",
                  "CoordinateSystem", "ParametricCurve"}
    if class_name in SKIP_TYPES:
        return

    try:
        ul = mob.get_corner(UL)
        dr = mob.get_corner(DR)
    except Exception:
        return

    w = abs(dr[0] - ul[0])
    h = abs(ul[1] - dr[1])
    if w < 0.001 and h < 0.001:
        return

    frame_w = abs(right - left)
    frame_h = abs(top - bottom)
    if w > frame_w * 2 or h > frame_h * 2:
        return

    is_text = _is_text_or_tex(mob)

    if is_text:
        text_list.append(mob)
        font_size = getattr(mob, 'font_size', None)
        if font_size is not None and font_size < MIN_FONT_SIZE:
            issues.append(
                f"{prefix}FONT TOO SMALL: \"{_mob_label(mob)}\" "
                f"font_size={font_size} (min {MIN_FONT_SIZE})"
            )

    if not is_text and _get_fill_opacity(mob) > 0.3 and w > 0.5 and h > 0.5:
        filled_shapes.append(mob)

    EPS = 0.1
    out = (ul[0] < left - EPS or dr[0] > right + EPS or
           dr[1] < bottom - EPS or ul[1] > top + EPS)

    if out:
        vis_l = max(ul[0], left)
        vis_r = min(dr[0], right)
        vis_b = max(dr[1], bottom)
        vis_t = min(ul[1], top)
        vis_w = max(0.0, vis_r - vis_l)
        vis_h = max(0.0, vis_t - vis_b)
        area = w * h if w * h > 0 else 1
        visible_frac = (vis_w * vis_h) / area

        if visible_frac < 0.01:
            severity = "COMPLETELY OFF SCREEN"
        elif visible_frac < 0.5:
            severity = "MOSTLY OFF SCREEN"
        else:
            severity = "OUT OF BOUNDS"

        issues.append(
            f"{prefix}{severity}: {_mob_label(mob) if is_text else class_name} "
            f"ul=({ul[0]:.1f},{ul[1]:.1f}) dr=({dr[0]:.1f},{dr[1]:.1f}) "
            f"visible={visible_frac:.0%} "
            f"frame=({left:.1f},{bottom:.1f})-({right:.1f},{top:.1f})"
        )

    if hasattr(mob, 'submobjects'):
        for sub in mob.submobjects:
            _check_recursive(sub, left, right, bottom, top, prefix, issues,
                             text_list, filled_shapes, seen_ids)


def _text_proximity(m1, m2, min_padding):
    try:
        ul1, dr1 = m1.get_corner(UL), m1.get_corner(DR)
        ul2, dr2 = m2.get_corner(UL), m2.get_corner(DR)
    except Exception:
        return None

    x_sep = max(ul2[0] - dr1[0], ul1[0] - dr2[0])
    y_sep = max(dr2[1] - ul1[1], dr1[1] - ul2[1])

    if x_sep <= 0 and y_sep <= 0:
        return "overlap"

    if x_sep >= 0 and y_sep >= 0:
        gap = (x_sep ** 2 + y_sep ** 2) ** 0.5
    elif x_sep >= 0:
        gap = x_sep
    else:
        gap = y_sep

    if gap < min_padding:
        return "too_close"
    return None


def _raw_boxes_overlap(m1, m2):
    try:
        ul1, dr1 = m1.get_corner(UL), m1.get_corner(DR)
        ul2, dr2 = m2.get_corner(UL), m2.get_corner(DR)
    except Exception:
        return False
    if dr1[0] < ul2[0] or dr2[0] < ul1[0]:
        return False
    if dr1[1] > ul2[1] or dr2[1] > ul1[1]:
        return False
    return True


# =====================================================================
# SCENE 1: The Hook
# =====================================================================

class HookScene(InteractiveScene):

    def construct(self):
        self._build_hook(self)

    @staticmethod
    def _build_hook(scene):

        title = Text("Sequential Data", font_size=84, weight=BOLD)
        title.move_to(UP * 0.5)

        subtitle = Text("When ORDER matters", font_size=46, weight=BOLD)
        subtitle.set_color(GOLD_ACCENT)
        subtitle.next_to(title, DOWN, buff=0.5)

        scene.play(Write(title), run_time=1.0)
        scene.play(FadeIn(subtitle, shift=UP * 0.3), run_time=0.8)
        scene.wait(1.5)

        scene.play(FadeOut(title), FadeOut(subtitle), run_time=0.6)

        # Three category icons — inside styled cards, evenly spaced
        icon_audio = make_icon_card(
            make_mini_waveform(width=1.6, height=0.45, color=WAVE_BLUE),
            "Audio", WAVE_BLUE,
        )
        icon_stock = make_icon_card(
            make_mini_chart(width=3, height=0.5, color=STOCK_GREEN),
            "Stock Price", STOCK_GREEN, width=3.6,
        )
        text_icon = Text("Abc", font_size=40, weight=BOLD)
        text_icon.set_color(WORD_BLUE)
        icon_language = make_icon_card(text_icon, "Language", WORD_BLUE)

        all_icons = VGroup(icon_audio, icon_stock, icon_language)
        all_icons.arrange(RIGHT, buff=0.6)
        all_icons.move_to(UP * 0.6)

        scene.play(LaggedStart(
            FadeIn(icon_audio, shift=UP * 0.3),
            FadeIn(icon_stock, shift=UP * 0.3),
            FadeIn(icon_language, shift=UP * 0.3),
            lag_ratio=0.25, run_time=1.5,
        ))
        scene.wait(0.5)

        bracket = Brace(all_icons, DOWN, buff=0.3)
        bracket.set_color(PURPLE_ACC)
        bracket_label = Text("Sequential Data", font_size=38, weight=BOLD)
        bracket_label.set_color(PURPLE_ACC)
        bracket_label.next_to(bracket, DOWN, buff=0.2)

        scene.play(GrowFromCenter(bracket), Write(bracket_label), run_time=0.8)
        scene.wait(2)

        validate_layout(scene, label="Scene 1 — hook")


# =====================================================================
# SCENE 2: Audio Waveform
# =====================================================================

class AudioScene(InteractiveScene):

    def construct(self):
        self._build_audio_scene(self)

    @staticmethod
    def _build_audio_scene(scene):

        title_grp = make_scene_title("Audio Waveform", color=WAVE_BLUE)

        axes = Axes(
            x_range=(0, 10, 2),
            y_range=(-1.5, 1.5, 0.5),
            width=11, height=3.0,
        )
        axes.shift(DOWN * 0.2)

        x_label = Text("Time", font_size=30, weight=BOLD)
        x_label.set_color(SOFT_GRAY)
        x_label.next_to(axes.x_axis, RIGHT, buff=0.25)
        y_label = Text("Amplitude", font_size=30, weight=BOLD)
        y_label.set_color(SOFT_GRAY)
        y_label.next_to(axes.y_axis, UP, buff=0.25)

        def wave_func(x):
            return np.sin(2 * x) + 0.3 * np.sin(5 * x)

        waveform = axes.get_graph(wave_func, x_range=(0.1, 9.9))
        waveform.set_stroke(WAVE_BLUE, width=5)

        scene.play(FadeIn(title_grp), run_time=0.6)
        scene.play(FadeIn(axes), FadeIn(x_label), FadeIn(y_label), run_time=0.5)
        scene.play(ShowCreation(waveform), run_time=2.0)
        scene.wait(0.5)

        # ==========================================
        # SEQUENTIAL STORYTELLING: playhead + samples one-by-one
        # ==========================================

        np.random.seed(42)
        n_samples = 15
        sample_xs = np.linspace(0.5, 9.5, n_samples)

        # Playhead — solid vertical line
        playhead = Line(axes.c2p(0, -1.5), axes.c2p(0, 1.5))
        playhead.set_stroke(GOLD_ACCENT, width=2.5, opacity=0.9)

        # Sequence row below axes
        seq_label = Text("Sequence:", font_size=30, weight=BOLD)
        seq_label.set_color(WAVE_BLUE)
        seq_label.next_to(axes, DOWN, buff=0.65)
        seq_label.to_edge(LEFT, buff=1.2)
        scene.play(FadeIn(seq_label), run_time=0.4)

        sample_dots = VGroup()
        sample_lines = VGroup()
        value_texts = VGroup()
        original_ys = []

        scene.add(playhead)

        # Build samples one by one with playhead sweep
        for i, sx in enumerate(sample_xs):
            sy = wave_func(sx)
            original_ys.append(sy)
            pt = axes.c2p(sx, sy)
            base_pt = axes.c2p(sx, 0)

            new_playhead = Line(axes.c2p(sx, -1.5), axes.c2p(sx, 1.5))
            new_playhead.set_stroke(GOLD_ACCENT, width=2.5, opacity=0.9)

            line = DashedLine(base_pt, pt, dash_length=0.06)
            line.set_stroke(SOFT_GRAY, width=1.5, opacity=0.4)
            sample_lines.add(line)

            dot = Dot(radius=0.08)
            dot.set_fill(WAVE_BLUE, opacity=1)
            dot.set_stroke(WHITE, width=2)
            dot.move_to(pt)
            sample_dots.add(dot)

            # Value text — show first 6 with proper spacing
            if i < 6:
                val_str = f"{sy:.1f}" if i < 5 else f"{sy:.1f}"
                val_text = Text(val_str, font_size=28, weight=BOLD)
                val_text.set_color(WAVE_BLUE)
                if len(value_texts) == 0:
                    val_text.next_to(seq_label, RIGHT, buff=0.4)
                else:
                    val_text.next_to(value_texts[-1], RIGHT, buff=0.35)
                value_texts.add(val_text)

            anim_list = [Transform(playhead, new_playhead), ShowCreation(line), GrowFromCenter(dot)]
            if i < 6:
                anim_list.append(FadeIn(val_text, shift=UP * 0.1))

            if i < 5:
                scene.play(*anim_list, run_time=0.4)
            elif i < 10:
                scene.play(*anim_list, run_time=0.2)
            else:
                scene.play(*anim_list, run_time=0.1)

        # Add "..." with proper spacing
        dots_text = Text("...", font_size=28, weight=BOLD)
        dots_text.set_color(WAVE_BLUE)
        dots_text.next_to(value_texts[-1], RIGHT, buff=0.4)
        scene.play(FadeIn(dots_text), run_time=0.3)

        # Arrow of time
        time_arrow = Arrow(
            seq_label.get_left() + DOWN * 0.5,
            dots_text.get_right() + DOWN * 0.5 + RIGHT * 0.2,
            stroke_width=3, buff=0,
        )
        time_arrow.set_color(TEAL_ACCENT)
        time_arrow_label = Text("time flows", font_size=28, weight=BOLD)
        time_arrow_label.set_color(TEAL_ACCENT)
        time_arrow_label.next_to(time_arrow, DOWN, buff=0.12)

        scene.play(GrowArrow(time_arrow), FadeIn(time_arrow_label), FadeOut(playhead), run_time=0.6)
        scene.wait(1.5)

        # ==========================================
        # SHUFFLE — destroy the sequence
        # ==========================================

        shuffled_ys = np.random.permutation(original_ys)
        shuffled_positions = [axes.c2p(sx, shuffled_ys[idx]) for idx, sx in enumerate(sample_xs)]

        shuffled_points = [axes.c2p(sx, shuffled_ys[idx]) for idx, sx in enumerate(sample_xs)]
        shuffled_graph = VMobject()
        shuffled_graph.set_points_smoothly(shuffled_points)
        shuffled_graph.set_stroke(SHUFFLE_RED, width=3, opacity=0.6)

        noise_label = Text("Noise!", font_size=56, weight=BOLD)
        noise_label.set_color(SHUFFLE_RED)
        noise_label.next_to(title_grp, DOWN, buff=0.67)
        noise_label.shift(RIGHT * 3.5)

        n_visible = len(value_texts)
        shuffled_vals = VGroup()
        for idx in range(n_visible):
            sv = Text(f"{shuffled_ys[idx]:.1f}", font_size=28, weight=BOLD)
            sv.set_color(SHUFFLE_RED)
            sv.move_to(value_texts[idx].get_center())
            shuffled_vals.add(sv)

        scene.play(
            *[d.animate.move_to(shuffled_positions[idx]) for idx, d in enumerate(sample_dots)],
            *[Transform(value_texts[idx], shuffled_vals[idx]) for idx in range(n_visible)],
            FadeOut(waveform), FadeOut(sample_lines),
            time_arrow.animate.set_color(SHUFFLE_RED),
            FadeOut(time_arrow_label), FadeOut(dots_text),
            run_time=1.5,
        )
        scene.play(ShowCreation(shuffled_graph), run_time=0.8)
        scene.play(
            *[d.animate.set_fill(SHUFFLE_RED) for d in sample_dots],
            FadeIn(noise_label, shift=LEFT * 0.3),
            run_time=0.6,
        )
        scene.wait(2)

        validate_layout(scene, label="Scene 2 — after shuffle")


# =====================================================================
# SCENE 3: Stock Price
# =====================================================================

class StockScene(InteractiveScene):

    def construct(self):
        self._build_stock_scene(self)

    @staticmethod
    def _build_stock_scene(scene):

        title_grp = make_scene_title("Stock Price", color=STOCK_GREEN)

        axes = Axes(
            x_range=(0, 30, 5),
            y_range=(0, 200, 50),
            width=11, height=3.2,
        )
        axes.shift(DOWN * 0.3)

        x_label = Text("Trading Days", font_size=30, weight=BOLD)
        x_label.set_color(SOFT_GRAY)
        x_label.next_to(axes.x_axis, DOWN, buff=0.35)
        x_label.shift(RIGHT * 2)
        y_label = Text("Price ($)", font_size=30, weight=BOLD)
        y_label.set_color(SOFT_GRAY)
        y_label.next_to(axes.y_axis, UP, buff=0.25)

        def stock_func(x):
            return 50 + 4 * x + 10 * np.sin(x * 0.5) - 5 * np.sin(x * 0.8) + 3 * np.sin(x * 1.5)

        scene.play(FadeIn(title_grp), run_time=0.6)
        scene.play(FadeIn(axes), FadeIn(x_label), FadeIn(y_label), run_time=0.5)

        # ==========================================
        # SEQUENTIAL STORYTELLING: build price day by day
        # ==========================================

        # Day counter badge — styled card in top-right
        day_badge = make_status_badge("Day: 0", STOCK_GREEN, font_size=30)
        day_badge.to_edge(RIGHT, buff=0.6)
        day_badge.move_to(day_badge.get_center() * RIGHT + UP * 3.0)

        price_badge = make_status_badge("$50", GOLD_ACCENT, font_size=28)
        price_badge.next_to(day_badge, DOWN, buff=0.15)

        scene.play(FadeIn(day_badge), FadeIn(price_badge), run_time=0.4)

        # Plot points one by one
        n_build = 15
        build_xs = np.linspace(0, 30, n_build)
        build_ys = [stock_func(x) for x in build_xs]

        all_dots = VGroup()
        all_segments = VGroup()

        prev_pt = None
        for i, (bx, by) in enumerate(zip(build_xs, build_ys)):
            pt = axes.c2p(bx, by)

            dot = Dot(radius=0.08, color=WHITE)
            dot.set_fill(STOCK_GREEN, opacity=1)
            dot.set_stroke(WHITE, width=2)
            dot.move_to(pt)
            all_dots.add(dot)

            if prev_pt is not None:
                seg = Line(prev_pt, pt, stroke_width=4)
                seg.set_color(STOCK_GREEN)
                all_segments.add(seg)

            new_day = make_status_badge(f"Day: {int(bx)}", STOCK_GREEN, font_size=30)
            new_day.move_to(day_badge.get_center())
            new_price = make_status_badge(f"${int(by)}", GOLD_ACCENT, font_size=28)
            new_price.next_to(new_day, DOWN, buff=0.15)

            anims = [GrowFromCenter(dot), Transform(day_badge, new_day),
                     Transform(price_badge, new_price)]
            if prev_pt is not None:
                anims.append(ShowCreation(seg))

            if i < 5:
                scene.play(*anims, run_time=0.4)
            elif i < 10:
                scene.play(*anims, run_time=0.2)
            else:
                scene.play(*anims, run_time=0.1)

            prev_pt = pt

        # Fill in smooth curve
        price_line = axes.get_graph(stock_func, x_range=(0, 30))
        price_line.set_stroke(STOCK_GREEN, width=5)

        scene.play(
            FadeOut(all_dots), FadeOut(all_segments),
            ShowCreation(price_line),
            run_time=1.0,
        )
        scene.wait(0.5)

        # "each day depends on what came before"
        dep_start = axes.c2p(4, stock_func(4)) + UP * 0.4
        dep_end = axes.c2p(12, stock_func(12)) + UP * 0.4
        dep_arrow = Arrow(dep_start, dep_end, stroke_width=3, buff=0.1)
        dep_arrow.set_color(GOLD_ACCENT)
        dep_label = Text("depends on\nprevious days", font_size=28, weight=BOLD)
        dep_label.set_color(GOLD_ACCENT)
        dep_label.next_to(dep_arrow, UP, buff=0.25)

        scene.play(GrowArrow(dep_arrow), FadeIn(dep_label), run_time=0.6)
        scene.wait(1)

        # Trend annotations
        uptrend_pt = axes.c2p(8, stock_func(8))
        uptrend_label = Text("Uptrend", font_size=32, weight=BOLD)
        uptrend_label.set_color(STOCK_GREEN)
        uptrend_label.next_to(uptrend_pt, UP, buff=0.35)

        correction_pt = axes.c2p(22, stock_func(22))
        correction_label = Text("Correction", font_size=32, weight=BOLD)
        correction_label.set_color(SHUFFLE_RED)
        correction_label.next_to(correction_pt, DOWN, buff=0.3)

        scene.play(
            FadeOut(dep_arrow), FadeOut(dep_label),
            FadeIn(uptrend_label, shift=UP * 0.2),
            run_time=0.6,
        )
        scene.play(FadeIn(correction_label, shift=UP * 0.2), run_time=0.6)
        scene.wait(1)

        # ==========================================
        # SHUFFLE — destroy the sequence
        # ==========================================

        np.random.seed(42)
        n_pts = 60
        xs = np.linspace(0, 30, n_pts)
        ys = np.array([stock_func(x) for x in xs])
        shuffled_ys = np.random.permutation(ys)

        shuffled_points = [axes.c2p(xs[idx], shuffled_ys[idx]) for idx in range(n_pts)]
        shuffled_line = VMobject()
        shuffled_line.set_points_smoothly(shuffled_points)
        shuffled_line.set_stroke(SHUFFLE_RED, width=3)

        no_pattern_label = Text("No pattern!", font_size=56, weight=BOLD)
        no_pattern_label.set_color(SHUFFLE_RED)
        no_pattern_label.next_to(title_grp, DOWN, buff=0.6)
        no_pattern_label.shift(RIGHT * 3)

        scene.play(
            FadeOut(uptrend_label), FadeOut(correction_label),
            FadeOut(day_badge), FadeOut(price_badge),
            run_time=0.4,
        )
        scene.play(
            FadeOut(price_line),
            FadeIn(shuffled_line),
            run_time=1.5,
        )
        scene.play(FadeIn(no_pattern_label, shift=LEFT * 0.3), run_time=0.6)
        scene.wait(2)

        validate_layout(scene, label="Scene 3 — after shuffle")


# =====================================================================
# SCENE 4: The Sentence — HERO SCENE
# =====================================================================

class SentenceScene(InteractiveScene):

    def construct(self):
        self._build_sentence(self)

    @staticmethod
    def _build_sentence(scene):

        # ==========================================
        # SECTION 1: Build the sentence
        # ==========================================

        words = ["the", "cat", "sat", "on", "the", "mat"]

        word_cards = VGroup()
        for w in words:
            card = make_word_card(w, font_size=40, stroke_color=WORD_BLUE)
            word_cards.add(card)

        word_cards.arrange(RIGHT, buff=0.3)
        word_cards.move_to(UP * 1.2)

        original_positions = [card.get_center().copy() for card in word_cards]

        scene.play(LaggedStart(
            *[FadeIn(card, shift=UP * 0.4) for card in word_cards],
            lag_ratio=0.15, run_time=2.0,
        ))
        scene.wait(0.5)

        # Meaning label
        meaning_text = Text(
            'A cat is sitting on a mat',
            font_size=58, weight=BOLD,
        )
        meaning_text.set_color(MEANING_GREEN)
        meaning_text.next_to(word_cards, DOWN, buff=1.4)

        scene.play(FadeIn(meaning_text, shift=UP * 0.2), run_time=0.8)
        scene.wait(1)

        # ==========================================
        # SECTION 2: Index numbers + reading arrow
        # ==========================================

        index_numbers = VGroup()
        for i, card in enumerate(word_cards):
            # Small circled index badge
            idx_text = Text(str(i + 1), font_size=24, weight=BOLD)
            idx_text.set_color(WHITE)
            idx_circle = Circle(radius=0.18)
            idx_circle.set_fill(WORD_BLUE, opacity=0.3)
            idx_circle.set_stroke(WORD_BLUE, width=1.5)
            idx_text.move_to(idx_circle.get_center())
            idx_badge = VGroup(idx_circle, idx_text)
            idx_badge.next_to(card, UP, buff=0.15)
            index_numbers.add(idx_badge)

        scene.play(LaggedStart(
            *[FadeIn(idx, shift=DOWN * 0.15) for idx in index_numbers],
            lag_ratio=0.08, run_time=1.0,
        ))

        arrow_start = word_cards[0].get_bottom() + DOWN * 0.3 + LEFT * 0.2
        arrow_end = word_cards[-1].get_bottom() + DOWN * 0.3 + RIGHT * 0.2
        reading_arrow = Arrow(
            arrow_start, arrow_end,
            stroke_width=3, buff=0,
        )
        reading_arrow.set_color(TEAL_ACCENT)

        reading_label = Text("Reading order", font_size=28, weight=BOLD)
        reading_label.set_color(TEAL_ACCENT)
        reading_label.next_to(reading_arrow, DOWN, buff=0.12)

        scene.play(GrowArrow(reading_arrow), run_time=0.6)
        scene.play(FadeIn(reading_label), run_time=0.4)
        scene.wait(1.5)

        # ==========================================
        # SECTION 3: SHUFFLE
        # ==========================================

        scene.play(
            FadeOut(reading_arrow), FadeOut(reading_label),
            FadeOut(index_numbers),
            run_time=0.5,
        )

        # Shuffle: rearrange cards but keep EQUAL spacing
        perm = [5, 0, 3, 2, 4, 1]  # new reading order of card indices
        # Build new positions: same y, same buff, just different card order
        total_width = word_cards.get_width()
        center_x = word_cards.get_center()[0]
        center_y = word_cards.get_center()[1]

        # Compute evenly spaced positions for 6 cards (same as original arrangement)
        shuffled_card_widths = [word_cards[perm[j]].get_width() for j in range(len(words))]
        buff_between = 0.3
        total_shuffled_w = sum(shuffled_card_widths) + buff_between * (len(words) - 1)
        start_x = center_x - total_shuffled_w / 2

        card_target_positions = [None] * len(words)
        cur_x = start_x
        for slot in range(len(words)):
            card_idx = perm[slot]
            card_w = word_cards[card_idx].get_width()
            target_x = cur_x + card_w / 2
            card_target_positions[card_idx] = np.array([target_x, center_y, 0])
            cur_x += card_w + buff_between

        shuffle_anims = []
        for i, card in enumerate(word_cards):
            shuffle_anims.append(card.animate.move_to(card_target_positions[i]))
        scene.play(*shuffle_anims, run_time=1.5)

        color_anims = [card[0].animate.set_stroke(SHUFFLE_RED) for card in word_cards]
        fill_anims = [card[0].animate.set_fill(SHUFFLE_RED, opacity=0.15) for card in word_cards]

        broken_meaning = Text(
            'Meaning: ???',
            font_size=60, weight=BOLD,
        )
        broken_meaning.set_color(SHUFFLE_RED)
        broken_meaning.move_to(meaning_text.get_center())

        scene.play(
            *color_anims,
            FadeOut(meaning_text),
            FadeIn(broken_meaning),
            run_time=0.8,
        )
        scene.wait(2)

        # ==========================================
        # SECTION 4: UNSHUFFLE
        # ==========================================

        unshuffle_anims = []
        for i, card in enumerate(word_cards):
            unshuffle_anims.append(card.animate.move_to(original_positions[i]))
        scene.play(*unshuffle_anims, run_time=1.2)

        restore_stroke = [card[0].animate.set_stroke(WORD_BLUE) for card in word_cards]

        restored_meaning = Text(
            'A cat is sitting on a mat',
            font_size=58, weight=BOLD,
        )
        restored_meaning.set_color(MEANING_GREEN)
        restored_meaning.move_to(broken_meaning.get_center())

        scene.play(
            *restore_stroke,
            FadeOut(broken_meaning),
            FadeIn(restored_meaning),
            run_time=0.6,
        )
        scene.wait(1)

        # ==========================================
        # SECTION 5: KEY MESSAGE
        # ==========================================

        scene.play(
            FadeOut(word_cards),
            FadeOut(restored_meaning),
            run_time=0.6,
        )

        key_line1 = Text("In sequential data,", font_size=50)
        key_line1.set_color(WHITE)
        key_line2 = Text("ORDER matters...", font_size=64, weight=BOLD)
        key_line2.set_color(GOLD_ACCENT)
        key_group = VGroup(key_line1, key_line2).arrange(DOWN, buff=0.4)
        key_group.move_to(ORIGIN)

        scene.play(Write(key_line1), run_time=0.8)
        scene.play(Write(key_line2), run_time=1.0)
        scene.wait(3)

        validate_layout(scene, label="Scene 4 — key message")


# =====================================================================
# SCENE 5: The Takeaway
# =====================================================================

class TakeawayScene(InteractiveScene):

    def construct(self):
        self._build_takeaway(self)

    @staticmethod
    def _build_takeaway(scene):

        # Three icon cards with "Order matters" badge
        icon_audio = make_icon_card(
            make_mini_waveform(width=1.4, height=0.4, color=WAVE_BLUE),
            "Audio", WAVE_BLUE, width=2.6, height=1.8,
        )
        icon_stock = make_icon_card(
            make_mini_chart(width=3, height=0.45, color=STOCK_GREEN),
            "Stock Price", STOCK_GREEN, width=3.6, height=1.8,
        )
        text_icon = Text("Abc", font_size=36, weight=BOLD)
        text_icon.set_color(WORD_BLUE)
        icon_language = make_icon_card(text_icon, "Language", WORD_BLUE, width=2.6, height=1.8)

        all_icons = VGroup(icon_audio, icon_stock, icon_language)
        all_icons.arrange(RIGHT, buff=0.5)
        all_icons.move_to(UP * 1.8)

        # Green check badges below each card
        checks = VGroup()
        for icon in all_icons:
            check = Text("Order matters", font_size=26, weight=BOLD)
            check.set_color(MEANING_GREEN)
            check.next_to(icon, DOWN, buff=0.25)
            checks.add(check)

        scene.play(LaggedStart(
            FadeIn(icon_audio, shift=UP * 0.3),
            FadeIn(icon_stock, shift=UP * 0.3),
            FadeIn(icon_language, shift=UP * 0.3),
            lag_ratio=0.2, run_time=1.2,
        ))
        scene.play(LaggedStart(
            *[FadeIn(c, shift=UP * 0.15) for c in checks],
            lag_ratio=0.15, run_time=0.8,
        ))
        scene.wait(1.5)

        # Divider line
        divider = Line(LEFT * 4, RIGHT * 4, stroke_width=1.5)
        divider.set_color(SOFT_GRAY)
        divider.set_opacity(0.3)
        divider.move_to(DOWN * 0.2)
        scene.play(ShowCreation(divider), run_time=0.3)

        question_text = Text(
            "How do neural networks\nlearn from sequences?",
            font_size=40, weight=BOLD,
        )
        question_text.set_color(WHITE)
        question_text.move_to(DOWN * 1.2)

        rnn_teaser = Text(
            "Next: Recurrent Neural Networks (RNNs)",
            font_size=36, weight=BOLD,
        )
        rnn_teaser.set_color(TEAL_ACCENT)
        rnn_teaser.next_to(question_text, DOWN, buff=0.5)

        # Right arrow next to RNN teaser
        rnn_arrow = Arrow(LEFT * 0.3, RIGHT * 0.3, stroke_width=4)
        rnn_arrow.set_color(TEAL_ACCENT)
        rnn_arrow.next_to(rnn_teaser, RIGHT, buff=0.3)

        scene.play(Write(question_text), run_time=1.2)
        scene.wait(0.5)
        scene.play(
            FadeIn(rnn_teaser, shift=UP * 0.3),
            GrowArrow(rnn_arrow),
            run_time=0.8,
        )
        scene.wait(3)

        validate_layout(scene, label="Scene 5 — takeaway")


# =====================================================================
# SCENE 6: Notation & One-Hot Encoding
# =====================================================================
#   Run standalone:
#       manimgl a.py NotationScene
#       manimgl a.py NotationScene -w --hd
# =====================================================================

class NotationScene(InteractiveScene):
    """
    Introduces the x^(t) notation for sequential text, then shows
    One-Hot Encoding as a concrete way to turn words into vectors
    that neural networks can consume.
    """

    def construct(self):
        self._build_notation(self)

    @staticmethod
    def _build_notation(scene):

        VOCAB     = ["the", "cat", "sat", "on", "mat"]
        OHE_VECS  = {
            "the": [1, 0, 0, 0, 0],
            "cat": [0, 1, 0, 0, 0],
            "sat": [0, 0, 1, 0, 0],
            "on":  [0, 0, 0, 1, 0],
            "mat": [0, 0, 0, 0, 1],
        }
        SENTENCE  = ["the", "cat", "sat", "on", "the", "mat"]

        # ── Helper: x^(t) with tight superscript, no space around t ──
        def xsup(t_str, fs_base=34, fs_sup=20, color=GOLD_ACCENT):
            xm = Text("x", font_size=fs_base, weight=BOLD)
            xm.set_color(color)
            sm = Text(f"({t_str})", font_size=fs_sup, weight=BOLD)
            sm.set_color(color)
            sm.next_to(xm, UR, buff=0.02)
            sm.shift(DOWN * xm.get_height() * 0.12)
            return VGroup(xm, sm)

        # ─── ACT 1: Title + sentence + x^(t) notation ────────────────

        title = Text("Representing Text for Neural Networks",
                     font_size=43, weight=BOLD)
        title.set_color(TEAL_ACCENT)
        title.to_edge(UP, buff=0.45)
        title.shift(DOWN * 0.677)
        scene.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.7)
        scene.wait(0.2)

        word_cards = VGroup(*[
            make_word_card(w, font_size=40, stroke_color=WORD_BLUE)
            for w in SENTENCE
        ])
        word_cards.arrange(RIGHT, buff=0.22)
        word_cards.move_to(UP * 1.3)

        scene.play(LaggedStart(
            *[FadeIn(c, shift=UP * 0.35) for c in word_cards],
            lag_ratio=0.12, run_time=1.6,
        ))
        scene.wait(0.3)

        # x^(t) labels — proper tight superscript VGroups
        notations = VGroup()
        for i, card in enumerate(word_cards):
            lbl = xsup(str(i + 1), fs_base=30, fs_sup=24)
            lbl.next_to(card, DOWN, buff=0.22)
            notations.add(lbl)

        scene.play(LaggedStart(
            *[FadeIn(n, shift=UP * 0.12) for n in notations],
            lag_ratio=0.10, run_time=1.4,
        ))
        scene.wait(0.4)

        # Abstract: x^(t) = word at time step t  — (t) is a superscript
        gen_x  = xsup("t", fs_base=38, fs_sup=24, color=PURPLE_ACC)
        gen_eq = Text("  =  word at time step  t", font_size=34)
        gen_eq.set_color(PURPLE_ACC)
        gen_eq.next_to(gen_x, RIGHT, buff=0.3)
        gen_lbl = VGroup(gen_x, gen_eq)
        gen_lbl.next_to(notations, DOWN, buff=0.45)

        scene.play(FadeIn(gen_lbl, shift=UP * 0.15), run_time=0.7)
        scene.wait(2.0)

        validate_layout(scene, label="NotationAct1")

        # ─── TRANSITION: shrink sentence strip to top ─────────────────

        scene.play(
            FadeOut(title), FadeOut(notations), FadeOut(gen_lbl),
            run_time=0.5,
        )
        scene.play(
            word_cards.animate.scale(0.70).to_edge(UP, buff=0.30),
            run_time=0.7,
        )
        scene.wait(0.25)

        # ─── ACT 2: One-Hot Encoding visualization ────────────────────

        ohe_title = Text("One-Hot Encoding", font_size=44, weight=BOLD)
        ohe_title.set_color(TEAL_ACCENT)
        ohe_title.move_to(UP * 1.173)           # shifted down from UP*1.85
        scene.play(Write(ohe_title), run_time=0.9)

        # Brief concept explainer — visible briefly, then fades before grid
        concept = Text(
            "Each unique word  →  a vector of all 0s,  exactly one element = 1",
            font_size=24,
        )
        concept.set_color(SOFT_GRAY)
        concept.next_to(ohe_title, DOWN, buff=0.22)
        scene.play(FadeIn(concept, shift=UP * 0.1), run_time=0.5)
        scene.wait(0.9)
        scene.play(FadeOut(concept), run_time=0.3)

        # ── Grid geometry ──────────────────────────────────────────────

        CELL_W      = 1.10
        CELL_H      = 0.48
        N_VOCAB     = len(VOCAB)
        SHOW_N      = 3
        VOCAB_X     = -4.05
        GRID_CTR_X  = 0.80
        GRID_TOP_Y  = 0.00          # low enough to clear ohe_title

        col_xs = [GRID_CTR_X + (i - (SHOW_N - 1) / 2) * CELL_W
                  for i in range(SHOW_N)]    # [-0.30, 0.80, 1.90]
        row_ys = [GRID_TOP_Y - i * CELL_H
                  for i in range(N_VOCAB)]   # [0.00,-0.48,-0.96,-1.44,-1.92]

        # ── Vocabulary column with index labels ────────────────────────

        vocab_header = Text("Vocabulary", font_size=26, weight=BOLD)
        vocab_header.set_color(SOFT_GRAY)
        vocab_header.move_to(np.array([VOCAB_X, GRID_TOP_Y + 0.50, 0]))

        vocab_labels     = VGroup()
        vocab_idx_labels = VGroup()
        for i, word in enumerate(VOCAB):
            lbl = Text(word, font_size=30, weight=BOLD)
            lbl.set_color(WORD_BLUE)
            lbl.move_to(np.array([VOCAB_X, row_ys[i], 0]))
            vocab_labels.add(lbl)

            idx_lbl = Text(f"[{i}]", font_size=24)
            idx_lbl.set_color(SOFT_GRAY)
            idx_lbl.next_to(lbl, RIGHT, buff=0.15)
            vocab_idx_labels.add(idx_lbl)

        scene.play(FadeIn(vocab_header), run_time=0.4)
        scene.play(LaggedStart(
            *[AnimationGroup(FadeIn(lbl, shift=RIGHT * 0.2), FadeIn(idx))
              for lbl, idx in zip(vocab_labels, vocab_idx_labels)],
            lag_ratio=0.10, run_time=0.9,
        ))
        scene.wait(0.2)

        # ── Column headers x^(1) x^(2) x^(3) using xsup ──────────────

        col_headers = VGroup()
        for i in range(SHOW_N):
            h = Text(f"x({i + 1})", font_size=26, weight=BOLD)
            h.set_color(GOLD_ACCENT)
            h.move_to(np.array([col_xs[i], GRID_TOP_Y + 0.50, 0]))
            col_headers.add(h)

        scene.play(LaggedStart(
            *[FadeIn(h) for h in col_headers],
            lag_ratio=0.15, run_time=0.6,
        ))

        # ── Grid cells — all "0" initially ────────────────────────────

        all_cells = []
        for ci in range(SHOW_N):
            col_cells = []
            for ri in range(N_VOCAB):
                rect = Rectangle(width=CELL_W * 0.90, height=CELL_H * 0.86)
                rect.set_fill(CARD_BG, opacity=0.75)
                rect.set_stroke(SOFT_GRAY, width=1.2, opacity=0.35)
                rect.move_to(np.array([col_xs[ci], row_ys[ri], 0]))

                val = Text("0", font_size=24, weight=BOLD)
                val.set_color(SOFT_GRAY)
                val.set_opacity(0.55)
                val.move_to(rect.get_center())

                col_cells.append((rect, val))
            all_cells.append(col_cells)

        all_rects = VGroup(*[c[0] for col in all_cells for c in col])
        all_vals  = VGroup(*[c[1] for col in all_cells for c in col])

        scene.play(
            LaggedStart(*[FadeIn(r) for r in all_rects],
                        lag_ratio=0.02, run_time=0.7),
        )
        scene.play(
            LaggedStart(*[FadeIn(v) for v in all_vals],
                        lag_ratio=0.01, run_time=0.4),
        )
        scene.wait(0.3)

        # ── Light up the single "1" column by column ──────────────────

        one_val_mobs = []
        for ci in range(SHOW_N):
            word    = SENTENCE[ci]
            vec     = OHE_VECS[word]
            one_idx = vec.index(1)

            rect, val  = all_cells[ci][one_idx]
            vocab_lbl  = vocab_labels[one_idx]
            vocab_idx  = vocab_idx_labels[one_idx]
            col_hdr    = col_headers[ci]

            one_val = Text("1", font_size=24, weight=BOLD)
            one_val.set_color(DARK_BG)
            one_val.move_to(rect.get_center())
            one_val_mobs.append(one_val)

            scene.play(
                rect.animate
                    .set_fill(GOLD_ACCENT, opacity=0.90)
                    .set_stroke(GOLD_ACCENT, width=2.5),
                FadeOut(val),
                FadeIn(one_val),
                vocab_lbl.animate.set_color(GOLD_ACCENT),
                vocab_idx.animate.set_color(GOLD_ACCENT),
                col_hdr.animate.set_color(TEAL_ACCENT),
                run_time=0.55,
            )
            scene.wait(0.35)
            scene.play(
                vocab_lbl.animate.set_color(WORD_BLUE),
                vocab_idx.animate.set_color(SOFT_GRAY),
                run_time=0.22,
            )

        scene.wait(0.3)

        # "..." indicator to the right
        dots_x   = col_xs[-1] + CELL_W * 1.30
        dots_y   = (GRID_TOP_Y + row_ys[-1]) / 2
        dots_mob = Text("...", font_size=30, weight=BOLD)
        dots_mob.set_color(SOFT_GRAY)
        dots_mob.move_to(np.array([dots_x, dots_y, 0]))
        scene.play(FadeIn(dots_mob), run_time=0.4)

        # "One Hot" name explained
        one_hot_note = Text(
            "One '1' per vector  —  that's why it's called  'One-Hot'",
            font_size=25, weight=BOLD,
        )
        one_hot_note.set_color(GOLD_ACCENT)
        one_hot_note.move_to(np.array([0.0, row_ys[-1] - 0.52, 0]))
        scene.play(Write(one_hot_note), run_time=0.9)

        validate_layout(scene, label="NotationOneHot Grid")
        scene.wait(0.5)

        # ─── ACT 3: Key message ───────────────────────────────────────

        msg_y = row_ys[-1] - 1.12

        msg1 = Text("This is one of the ways to represent sequential data",
                    font_size=27, weight=BOLD)
        msg1.set_color(WHITE)
        msg1.move_to(np.array([0.0, msg_y, 0]))

        msg2 = Text("into numbers that Neural Networks can understand.",
                    font_size=27, weight=BOLD)
        msg2.set_color(TEAL_ACCENT)
        msg2.next_to(msg1, DOWN, buff=0.22)

        scene.play(FadeIn(msg1, shift=UP * 0.15), run_time=0.7)
        scene.play(FadeIn(msg2, shift=UP * 0.15), run_time=0.7)
        scene.wait(3.5)

        validate_layout(scene, label="NotationOneHot Final")


# =====================================================================
# FULL VIDEO — All Scenes Combined
# =====================================================================

class SequentialDataFullVideo(InteractiveScene):

    def construct(self):

        # ==============================================================
        # SCENE 1: The Hook  (~25s)
        # ==============================================================
        HookScene._build_hook(self)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        # ==============================================================
        # SCENE 2: Audio Waveform  (~40s)
        # ==============================================================
        AudioScene._build_audio_scene(self)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        # ==============================================================
        # SCENE 3: Stock Price  (~40s)
        # ==============================================================
        StockScene._build_stock_scene(self)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        # ==============================================================
        # SCENE 4: The Sentence — HERO SCENE  (~50s)
        # ==============================================================
        SentenceScene._build_sentence(self)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        # ==============================================================
        # SCENE 5: The Takeaway  (~20s)
        # ==============================================================
        TakeawayScene._build_takeaway(self)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        self.wait(1)


# =====================================================================
# =====================================================================
#
#   VIDEO 2: Why ANNs Fail at Sequential Data
#
#   Run full video:
#       manimgl a.py ANNFailFullVideo
#       manimgl a.py ANNFailFullVideo -w --hd
#       manimgl a.py ANNFailFullVideo -w -l
#
#   Individual scenes:
#       manimgl a.py RecapHookScene
#       manimgl a.py FeedforwardScene
#       manimgl a.py FixedSizeScene
#       manimgl a.py NoMemoryScene
#       manimgl a.py ParamExplosionScene
#       manimgl a.py SlidingWindowScene
#       manimgl a.py SolutionTeaserScene
#
# =====================================================================
# =====================================================================

# ── Additional colors for Video 2 ────────────────────────────────────
ANN_BLUE       = "#3498DB"
HIDDEN_TEAL    = "#1ABC9C"
PROBLEM_RED    = "#E74C3C"
OUTPUT_GOLD    = "#F1C40F"
SOLUTION_GREEN = "#2ECC71"
MEMORY_PURPLE  = "#8E44AD"
WINDOW_AMBER   = "#F39C12"


# ── Helper functions for Video 2 ────────────────────────────────────

def make_nn_node(radius=0.2, fill_color=ANN_BLUE, stroke_color=WHITE, stroke_width=2):
    """Single neural network node."""
    node = Circle(radius=radius)
    node.set_fill(fill_color, opacity=0.9)
    node.set_stroke(stroke_color, width=stroke_width)
    node.set_z_index(3)
    return node


def make_nn_layer(n_nodes, fill_color, spacing=0.6, radius=0.2, label_text=None,
                  label_color=None):
    """Vertical column of nodes with optional label below."""
    nodes = VGroup()
    for i in range(n_nodes):
        node = make_nn_node(radius=radius, fill_color=fill_color)
        nodes.add(node)
    nodes.arrange(DOWN, buff=spacing - 2 * radius)

    result = VGroup(nodes)
    if label_text:
        lbl = Text(label_text, font_size=26, weight=BOLD)
        lbl.set_color(label_color or fill_color)
        lbl.next_to(nodes, DOWN, buff=0.25)
        result.add(lbl)

    return result


def make_nn_connections(layer_a, layer_b, color=SOFT_GRAY, stroke_width=1.5,
                        opacity=0.4):
    """All-to-all lines between two node VGroups."""
    lines = VGroup()
    for na in layer_a:
        for nb in layer_b:
            line = Line(na.get_center(), nb.get_center())
            line.set_stroke(color, width=stroke_width, opacity=opacity)
            line.set_z_index(-2)
            lines.add(line)
    return lines


def make_problem_card(text, width=5.0, color=PROBLEM_RED, font_size=30):
    """Red-bordered card for problem statements."""
    label = Text(text, font_size=font_size, weight=BOLD)
    label.set_color(WHITE)
    card_w = max(label.get_width() + 0.8, width)
    bg = RoundedRectangle(width=card_w, height=label.get_height() + 0.45,
                          corner_radius=0.12)
    bg.set_fill(DARK_BG, opacity=0.8)
    bg.set_stroke(color, width=2.5)
    label.move_to(bg.get_center())
    return VGroup(bg, label)


def make_solution_card(text, width=5.0, color=SOLUTION_GREEN, font_size=30):
    """Green-bordered card for solution statements."""
    label = Text(text, font_size=font_size, weight=BOLD)
    label.set_color(WHITE)
    card_w = max(label.get_width() + 0.8, width)
    bg = RoundedRectangle(width=card_w, height=label.get_height() + 0.45,
                          corner_radius=0.12)
    bg.set_fill(DARK_BG, opacity=0.8)
    bg.set_stroke(color, width=2.5)
    label.move_to(bg.get_center())
    return VGroup(bg, label)


def make_vector_bar(n_slots, slot_labels=None, fill_color=ANN_BLUE,
                    slot_width=0.75, height=0.55):
    """Horizontal vector of n colored slots with optional labels inside.
    Auto-sizes slot_width to fit the widest label."""
    # First pass: create labels and measure widest
    labels = VGroup()
    if slot_labels:
        for i in range(min(n_slots, len(slot_labels))):
            lbl = Text(str(slot_labels[i]), font_size=24, weight=BOLD)
            lbl.set_color(WHITE)
            slot_width = max(slot_width, lbl.get_width() + 0.35)
            labels.add(lbl)

    cells = VGroup()
    for i in range(n_slots):
        cell = Rectangle(width=slot_width, height=height)
        cell.set_fill(fill_color, opacity=0.2)
        cell.set_stroke(fill_color, width=2)
        cells.add(cell)

    cells.arrange(RIGHT, buff=0)

    for i, lbl in enumerate(labels):
        lbl.move_to(cells[i].get_center())

    result = VGroup(cells, labels)
    return result


# =====================================================================


# =====================================================================
# VIDEO 2 — Why ANNs Fail at Sequential Data
#
#   Run:
#       manimgl a.py ANNFailFullVideo
#       manimgl a.py ANNFailFullVideo -w --hd
#       manimgl a.py ANNFailFullVideo -w -l
#
# =====================================================================

class ANNFailFullVideo(InteractiveScene):

    def construct(self):

        # ==============================================================
        # SCENE 1: Quick Recap Hook (~20s)
        # ==============================================================

        # Start directly — no icon recap, jump straight into the question
        question = Text(
            "How do we teach a machine\nto understand sequences?",
            font_size=61, weight=BOLD,
        )
        question.set_color(WHITE)
        question.move_to(UP * 0.9)

        sub_q = Text("Let's see what DOESN'T work.", font_size=54, weight=BOLD)
        sub_q.set_color(PROBLEM_RED)
        sub_q.next_to(question, DOWN, buff=0.85)

        self.play(Write(question), run_time=1.5)
        self.wait(0.5)
        self.play(FadeIn(sub_q, shift=UP * 0.3), run_time=0.8)
        self.wait(2)

        validate_layout(self, label="V2 Scene 1")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        # ==============================================================
        # SCENE 2: The Feedforward ANN (~50s)
        # ==============================================================

        title = make_scene_title("The Feedforward Network", color=ANN_BLUE,
                                 font_size=56)
        title.shift(DOWN * 0.5)

        # Build 4-layer network — compact with larger nodes
        input_layer = make_nn_layer(4, ANN_BLUE, spacing=0.75, radius=0.28,
                                     label_text="Input", label_color=ANN_BLUE)
        hidden1 = make_nn_layer(5, HIDDEN_TEAL, spacing=0.65, radius=0.25,
                                 label_text="Hidden 1", label_color=HIDDEN_TEAL)
        hidden2 = make_nn_layer(5, HIDDEN_TEAL, spacing=0.65, radius=0.25,
                                 label_text="Hidden 2", label_color=HIDDEN_TEAL)
        output_layer = make_nn_layer(2, OUTPUT_GOLD, spacing=0.75, radius=0.28,
                                      label_text="Output", label_color=OUTPUT_GOLD)

        nn_group = VGroup(input_layer, hidden1, hidden2, output_layer)
        nn_group.arrange(RIGHT, buff=1.3)
        nn_group.move_to(DOWN * 0.1)

        input_nodes = input_layer[0]
        h1_nodes = hidden1[0]
        h2_nodes = hidden2[0]
        out_nodes = output_layer[0]

        conn_1 = make_nn_connections(input_nodes, h1_nodes)
        conn_2 = make_nn_connections(h1_nodes, h2_nodes)
        conn_3 = make_nn_connections(h2_nodes, out_nodes)

        self.play(FadeIn(title), run_time=0.6)

        # Build layer by layer with connections
        for layer, conns, nodes in [
            (input_layer, None, input_nodes),
            (hidden1, conn_1, h1_nodes),
            (hidden2, conn_2, h2_nodes),
            (output_layer, conn_3, out_nodes),
        ]:
            anims = [LaggedStart(
                *[GrowFromCenter(n) for n in nodes],
                lag_ratio=0.08, run_time=0.5,
            )]
            if len(layer) > 1:
                anims.append(FadeIn(layer[1], shift=UP * 0.1))
            self.play(*anims, run_time=0.5)
            if conns is not None:
                self.play(LaggedStart(
                    *[ShowCreation(l) for l in conns],
                    lag_ratio=0.005, run_time=0.6,
                ))
                # Push this batch of edges behind the already-drawn nodes
                self.bring_to_back(*list(conns))

        # Final pass: guarantee ALL edges sit behind ALL nodes
        self.bring_to_back(*list(conn_3), *list(conn_2), *list(conn_1))
        self.wait(0.5)

        # Data propagation — bright dots travel along weight edges, layer by layer
        layer_pairs = [
            (input_nodes, h1_nodes, conn_1),
            (h1_nodes, h2_nodes, conn_2),
            (h2_nodes, out_nodes, conn_3),
        ]

        for src_nodes, tgt_nodes, conns in layer_pairs:
            # One dot per EDGE — every connection carries a pulse simultaneously
            dots = VGroup()
            dot_targets = []
            for line in conns:
                d = Dot(radius=0.09)
                d.set_fill("#FF0000", opacity=1)
                d.set_stroke(WHITE, width=1.5)
                d.set_z_index(5)
                d.move_to(line.get_start())
                dots.add(d)
                dot_targets.append(line.get_end())

            # Light up all edges and spawn dots at source ends
            self.play(
                *[GrowFromCenter(d) for d in dots],
                *[l.animate.set_stroke("#FF4444", opacity=0.7, width=2.2)
                  for l in conns],
                run_time=0.2,
            )

            # Every dot travels along its own edge to the target node
            self.play(
                *[d.animate.move_to(t) for d, t in zip(dots, dot_targets)],
                run_time=0.45,
            )

            # Flash target nodes, fade all dots, restore edges
            self.play(
                *[n.animate.set_stroke("#FF0000", width=4) for n in tgt_nodes],
                FadeOut(dots),
                *[l.animate.set_stroke(SOFT_GRAY, opacity=0.4, width=1.5)
                  for l in conns],
                run_time=0.25,
            )
            self.play(
                *[n.animate.set_stroke(WHITE, width=2) for n in tgt_nodes],
                run_time=0.15,
            )

        self.wait(0.5)

        # Forward-only arrow — anchored well below the network's bottom edge
        net_bottom_y = nn_group.get_bottom()[1]
        arrow_y = net_bottom_y - 0.8
        flow_arrow = Arrow(
            np.array([nn_group.get_left()[0] - 0.3, arrow_y, 0]),
            np.array([nn_group.get_right()[0] + 0.3, arrow_y, 0]),
            stroke_width=3, buff=0,
        )
        flow_arrow.set_color("#FF8C00")

        flow_label = Text("Forward only — no looking back", font_size=32,
                           weight=BOLD)
        flow_label.set_color("#FF8C00")
        flow_label.next_to(flow_arrow, DOWN, buff=0.35)

        self.play(GrowArrow(flow_arrow), FadeIn(flow_label, shift=UP * 0.2),
                  run_time=0.8)
        self.wait(1.2)

        # Fade out arrow + label, then fade in the fixed-size badge at the same spot
        fixed_badge = make_status_badge("Fixed: 4 inputs -> 2 outputs",
                                         ANN_BLUE, font_size=28, min_width=5.5)
        fixed_badge.move_to(flow_arrow.get_center() + DOWN * 0.3)

        self.play(
            FadeOut(flow_arrow), FadeOut(flow_label),
            run_time=0.4,
        )
        self.play(FadeIn(fixed_badge, shift=UP * 0.2), run_time=0.5)

        # Glow input nodes to emphasize fixed size
        self.play(
            *[n.animate.set_stroke("#FF9900", width=4) for n in input_nodes],
            run_time=0.4,
        )
        self.play(
            *[n.animate.set_stroke(WHITE, width=2) for n in input_nodes],
            run_time=0.3,
        )
        self.wait(2)

        validate_layout(self, label="V2 Scene 2")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        # ==============================================================
        # SCENE 3: Fixed-Size Problem (~55s)
        # ==============================================================

        title = make_scene_title("Problem 1: Fixed-Size Inputs",
                                  color=PROBLEM_RED, font_size=52)
        title.shift(DOWN * 0.55)
        self.play(FadeIn(title), run_time=0.6)

        # -- SECTION A: 6-word sentence fits perfectly --
        words_6 = ["the", "cat", "sat", "on", "the", "mat"]
        word_cards = VGroup()
        for w in words_6:
            card = make_word_card(w, font_size=38, stroke_color=WORD_BLUE)
            word_cards.add(card)
        word_cards.arrange(RIGHT, buff=0.25)
        word_cards.move_to(UP * 1.0)

        self.play(LaggedStart(
            *[FadeIn(c, shift=UP * 0.4) for c in word_cards],
            lag_ratio=0.12, run_time=1.5,
        ))
        self.wait(0.5)

        # Vector bar (6 slots) with labels — shifted further down for breathing room
        vec_bar = make_vector_bar(6, slot_labels=words_6, fill_color=ANN_BLUE,
                                   height=0.6)
        vec_bar.move_to(DOWN * 1.1)

        flatten_arrow = Arrow(
            word_cards.get_bottom() + DOWN * 0.1,
            vec_bar.get_top() + UP * 0.1,
            stroke_width=4, buff=0.1,
        )
        flatten_arrow.set_color(SOFT_GRAY)

        self.play(GrowArrow(flatten_arrow), run_time=0.4)
        self.play(FadeIn(vec_bar, shift=DOWN * 0.2), run_time=0.6)

        # Green "Fits!" label
        fits_label = Text("Fits!", font_size=44, weight=BOLD)
        fits_label.set_color(MEANING_GREEN)
        fits_label.next_to(vec_bar, DOWN, buff=0.5)

        self.play(FadeIn(fits_label, scale=1.3), run_time=0.4)
        self.wait(1)

        # -- SECTION B: Short sentence — doesn't fit --
        self.play(
            FadeOut(word_cards), FadeOut(flatten_arrow),
            FadeOut(vec_bar), FadeOut(fits_label),
            run_time=0.4,
        )

        short_words = ["I", "agree"]
        short_cards = VGroup()
        for w in short_words:
            card = make_word_card(w, font_size=38, stroke_color=WORD_BLUE)
            short_cards.add(card)
        short_cards.arrange(RIGHT, buff=0.25)
        short_cards.move_to(UP * 1.0)

        short_labels = ["I", "agree", "?", "?", "?", "?"]
        short_vec = make_vector_bar(6, slot_labels=short_labels,
                                     fill_color=ANN_BLUE, height=0.6)
        short_vec.move_to(DOWN * 1.1)

        # Color empty slots red
        for i in range(2, 6):
            short_vec[0][i].set_stroke(PROBLEM_RED, width=2.5)
            short_vec[0][i].set_fill(PROBLEM_RED, opacity=0.15)
        for i in range(2, 6):
            if i < len(short_vec[1]):
                short_vec[1][i].set_color(PROBLEM_RED)

        padding_label = Text("4 empty slots — padding needed!", font_size=38,
                              weight=BOLD)
        padding_label.set_color(PROBLEM_RED)
        padding_label.next_to(short_vec, DOWN, buff=0.5)

        self.play(FadeIn(short_cards, shift=UP * 0.3), run_time=0.5)
        self.play(FadeIn(short_vec), run_time=0.5)
        self.play(FadeIn(padding_label, shift=UP * 0.2), run_time=0.5)

        # Pulse red slots
        self.play(
            *[short_vec[0][i].animate.set_fill(PROBLEM_RED, opacity=0.4)
              for i in range(2, 6)],
            run_time=0.3,
        )
        self.play(
            *[short_vec[0][i].animate.set_fill(PROBLEM_RED, opacity=0.15)
              for i in range(2, 6)],
            run_time=0.3,
        )
        self.wait(1)

        # -- SECTION C: Long sentence — truncated --
        self.play(
            FadeOut(short_cards), FadeOut(short_vec), FadeOut(padding_label),
            run_time=0.4,
        )

        long_text = Text(
            "the quick brown fox jumps over the lazy dog ...",
            font_size=28, weight=BOLD,
        )
        long_text.set_color(WHITE)
        long_text.move_to(UP * 1.0)

        long_labels = ["the", "quick", "brown", "fox", "jumps", "over"]
        long_vec = make_vector_bar(6, slot_labels=long_labels,
                                    fill_color=ANN_BLUE, height=0.6)
        # Shift left so the "lost" text fits to the right without going off screen
        long_vec.move_to(LEFT * 1.4 + DOWN * 1.1)

        # "the lazy dog" shown as lost/cut off — positioned right of the vector
        lost_text = Text("the lazy dog ...", font_size=28, weight=BOLD)
        lost_text.set_color(PROBLEM_RED)
        lost_text.set_opacity(0.6)
        lost_text.next_to(long_vec, RIGHT, buff=0.35)
        # Safety clamp: never go off screen right
        if lost_text.get_right()[0] > 6.8:
            lost_text.shift(LEFT * (lost_text.get_right()[0] - 6.8))

        # Red strikethrough on lost text
        lost_strike = Line(
            lost_text.get_left() + LEFT * 0.1,
            lost_text.get_right() + RIGHT * 0.1,
            stroke_width=3,
        )
        lost_strike.set_color(PROBLEM_RED)

        trunc_label = Text("LOST — truncated!", font_size=42, weight=BOLD)
        trunc_label.set_color(PROBLEM_RED)
        trunc_label.next_to(long_vec, DOWN, buff=0.6)
        trunc_label.shift(DOWN * 0.55)

        self.play(FadeIn(long_text), run_time=0.5)
        self.play(FadeIn(long_vec), run_time=0.5)
        self.play(
            FadeIn(lost_text, shift=RIGHT * 0.3),
            ShowCreation(lost_strike),
            run_time=0.5,
        )
        self.play(FadeIn(trunc_label, shift=UP * 0.2), run_time=0.5)
        self.wait(1.5)

        # -- SECTION D: Mismatch summary --
        self.play(
            FadeOut(long_text), FadeOut(long_vec),
            FadeOut(lost_text), FadeOut(lost_strike),
            FadeOut(trunc_label),
            run_time=0.4,
        )

        # Left: Variable-length sequences
        left_box = RoundedRectangle(width=5.2, height=3.0, corner_radius=0.15)
        left_box.set_fill(DARK_BG, opacity=0.7)
        left_box.set_stroke(WORD_BLUE, width=2.5)
        left_box.move_to(LEFT * 3.3 + DOWN * 0.3)

        left_title = Text("Variable-length\nsequences", font_size=36, weight=BOLD)
        left_title.set_color(WORD_BLUE)
        left_title.move_to(left_box.get_center() + UP * 0.5)

        arr1 = Arrow(LEFT * 0.8, RIGHT * 0.3, stroke_width=3, buff=0)
        arr1.set_color(WAVE_BLUE)
        arr2 = Arrow(LEFT * 0.8, RIGHT * 1.2, stroke_width=3, buff=0)
        arr2.set_color(STOCK_GREEN)
        arr3 = Arrow(LEFT * 0.8, RIGHT * 1.8, stroke_width=3, buff=0)
        arr3.set_color(WORD_BLUE)
        var_arrows = VGroup(arr1, arr2, arr3)
        var_arrows.arrange(DOWN, buff=0.2)
        var_arrows.next_to(left_title, DOWN, buff=0.3)

        # Right: Fixed-size network
        right_box = RoundedRectangle(width=5.2, height=3.0, corner_radius=0.15)
        right_box.set_fill(DARK_BG, opacity=0.7)
        right_box.set_stroke(PROBLEM_RED, width=2.5)
        right_box.move_to(RIGHT * 3.3 + DOWN * 0.3)

        right_title = Text("Fixed-size\nnetwork", font_size=36, weight=BOLD)
        right_title.set_color(PROBLEM_RED)
        right_title.move_to(right_box.get_center() + UP * 0.5)

        fixed_slots = make_vector_bar(4, fill_color=PROBLEM_RED,
                                       slot_width=0.7, height=0.5)
        fixed_slots.next_to(right_title, DOWN, buff=0.35)

        # MISMATCH stamp
        mismatch = Text("MISMATCH", font_size=56, weight=BOLD)
        mismatch.set_color(PROBLEM_RED)
        mismatch.move_to(DOWN * 2.8)

        self.play(
            FadeIn(left_box), FadeIn(left_title),
            FadeIn(right_box), FadeIn(right_title),
            run_time=0.6,
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in var_arrows],
                         lag_ratio=0.15, run_time=0.6),
            FadeIn(fixed_slots),
            run_time=0.6,
        )
        self.play(FadeIn(mismatch, scale=1.5), run_time=0.6)
        self.wait(2)

        validate_layout(self, label="V2 Scene 3")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        # ==============================================================
        # SCENE 4: No Memory (~50s)
        # ==============================================================

        title = make_scene_title("Problem 2: No Memory", color=PROBLEM_RED,
                                 font_size=52)
        title.shift(DOWN * 0.4)
        self.play(FadeIn(title), run_time=0.6)

        # ANN centered for symmetry — slightly bigger
        ann_in = make_nn_layer(3, ANN_BLUE, radius=0.27, spacing=0.75)
        ann_h = make_nn_layer(4, HIDDEN_TEAL, radius=0.27, spacing=0.7)
        ann_out = make_nn_layer(1, OUTPUT_GOLD, radius=0.27, spacing=0.7)
        ann_group = VGroup(ann_in, ann_h, ann_out)
        ann_group.arrange(RIGHT, buff=1.0)
        ann_group.move_to(ORIGIN + UP * 0.2)

        ann_c1 = make_nn_connections(ann_in[0], ann_h[0], stroke_width=1.5,
                                      opacity=0.4)
        ann_c2 = make_nn_connections(ann_h[0], ann_out[0], stroke_width=1.5,
                                      opacity=0.4)

        ann_label = Text("ANN", font_size=32, weight=BOLD)
        ann_label.set_color(ANN_BLUE)
        ann_label.next_to(ann_group, UP, buff=0.25)

        # Day cards on the left
        day_data = [
            ("Day 1: $100", STOCK_GREEN),
            ("Day 2: $105", STOCK_GREEN),
            ("Day 3: $98", STOCK_GREEN),
        ]
        day_cards = VGroup()
        for txt, clr in day_data:
            card = make_status_badge(txt, clr, font_size=30, min_width=3.8)
            day_cards.add(card)
        day_cards.arrange(DOWN, buff=0.3)
        day_cards.move_to(LEFT * 4.2 + UP * 0.2)
        day_cards.scale(0.8)

        # Memory badge
        mem_badge = make_status_badge("Memory: EMPTY", PROBLEM_RED,
                                       font_size=26, min_width=4.0)
        mem_badge.next_to(ann_group, DOWN, buff=0.5)

        self.play(
            FadeIn(ann_group), FadeIn(ann_c1), FadeIn(ann_c2),
            FadeIn(ann_label), run_time=0.6,
        )
        self.bring_to_back(*list(ann_c1), *list(ann_c2))
        self.play(LaggedStart(
            *[FadeIn(c, shift=RIGHT * 0.3) for c in day_cards],
            lag_ratio=0.2, run_time=0.8,
        ))
        self.wait(0.5)

        # -- Day 1 processing --
        day1_copy = day_cards[0].copy()
        self.play(
            day1_copy.animate.move_to(ann_in.get_center()).scale(0.35),
            run_time=0.55,
        )

        # Connections flash bright as data flows
        self.play(
            *[l.animate.set_stroke(color=WHITE, opacity=0.8, width=2.5)
              for l in ann_c1],
            *[l.animate.set_stroke(color=WHITE, opacity=0.8, width=2.5)
              for l in ann_c2],
            run_time=0.2,
        )

        pred_label = Text("Prediction: ?", font_size=30, weight=BOLD)
        pred_label.set_color(OUTPUT_GOLD)
        pred_label.next_to(ann_out, RIGHT, buff=0.75)

        # MEMORY WIPE — connections snap back to dim
        self.play(
            *[l.animate.set_stroke(color=SOFT_GRAY, opacity=0.15, width=1.5)
              for l in ann_c1],
            *[l.animate.set_stroke(color=SOFT_GRAY, opacity=0.15, width=1.5)
              for l in ann_c2],
            FadeOut(day1_copy),
            FadeIn(pred_label),
            run_time=0.4,
        )

        # Memory badge appears
        self.play(FadeIn(mem_badge, shift=UP * 0.2), run_time=0.4)

        # Restore connection opacity for Day 2
        self.play(
            *[l.animate.set_stroke(opacity=0.4, width=1.5, color=SOFT_GRAY)
              for l in ann_c1],
            *[l.animate.set_stroke(opacity=0.4, width=1.5, color=SOFT_GRAY)
              for l in ann_c2],
            run_time=0.2,
        )
        self.wait(0.5)

        # -- Day 2 processing --
        day2_copy = day_cards[1].copy()
        self.play(
            day2_copy.animate.move_to(ann_in.get_center()).scale(0.35),
            run_time=0.5,
        )

        # Connections light up again
        self.play(
            *[l.animate.set_stroke(color=WHITE, opacity=0.8, width=2.5)
              for l in ann_c1],
            *[l.animate.set_stroke(color=WHITE, opacity=0.8, width=2.5)
              for l in ann_c2],
            run_time=0.2,
        )

        # Memory wipe again
        self.play(
            *[l.animate.set_stroke(color=SOFT_GRAY, opacity=0.15, width=1.5)
              for l in ann_c1],
            *[l.animate.set_stroke(color=SOFT_GRAY, opacity=0.15, width=1.5)
              for l in ann_c2],
            FadeOut(day2_copy),
            run_time=0.4,
        )

        # "No idea what Day 1 was!" — placed at bottom center, bg matches text width
        thought_text = Text("No idea what Day 1 was!", font_size=30, weight=BOLD)
        thought_text.set_color(PROBLEM_RED)
        thought_bg = RoundedRectangle(
            width=thought_text.get_width() + 1.0,
            height=thought_text.get_height() + 0.55,
            corner_radius=0.15,
        )
        thought_bg.set_fill(DARK_BG, opacity=0.9)
        thought_bg.set_stroke(PROBLEM_RED, width=2.5)
        thought_text.move_to(thought_bg.get_center())
        thought = VGroup(thought_bg, thought_text)
        thought.next_to(mem_badge, DOWN, buff=0.55)

        self.play(FadeIn(thought, shift=UP * 0.2), run_time=0.5)
        self.wait(1.5)

        # -- Split comparison --
        self.play(*[FadeOut(m) for m in self.mobjects if m is not title],
                  run_time=0.5)

        # Left: what ANN sees
        left_panel = RoundedRectangle(width=5.5, height=3.5, corner_radius=0.15)
        left_panel.set_fill(DARK_BG, opacity=0.6)
        left_panel.set_stroke(PROBLEM_RED, width=2.5)
        left_panel.move_to(LEFT * 3.3 + DOWN * 0.3)

        left_t = Text("What the ANN sees", font_size=32, weight=BOLD)
        left_t.set_color(PROBLEM_RED)
        left_t.next_to(left_panel, UP, buff=0.2)

        # Three isolated dots — no connections
        scat_dots = VGroup()
        for pos in [LEFT * 1.2 + UP * 0.3, DOWN * 0.3,
                    RIGHT * 1.0 + UP * 0.6]:
            d = Dot(radius=0.15)
            d.set_fill(STOCK_GREEN, opacity=1)
            d.set_stroke(WHITE, width=2)
            d.move_to(left_panel.get_center() + pos)
            scat_dots.add(d)

        isolated_label = Text("Isolated points", font_size=39, weight=BOLD)
        isolated_label.set_color(SOFT_GRAY)
        isolated_label.next_to(left_panel, DOWN, buff=0.45)
        isolated_label.shift(DOWN * 0.4)

        # Right: what we need
        right_panel = RoundedRectangle(width=5.5, height=3.5, corner_radius=0.15)
        right_panel.set_fill(DARK_BG, opacity=0.6)
        right_panel.set_stroke(MEANING_GREEN, width=2.5)
        right_panel.move_to(RIGHT * 3.3 + DOWN * 0.3)

        right_t = Text("What we NEED", font_size=32, weight=BOLD)
        right_t.set_color(MEANING_GREEN)
        right_t.next_to(right_panel, UP, buff=0.2)

        # Three connected dots with trend line
        trend_dots = VGroup()
        trend_positions = [LEFT * 1.2 + DOWN * 0.3, UP * 0.1,
                           RIGHT * 1.2 + UP * 0.6]
        for pos in trend_positions:
            d = Dot(radius=0.15)
            d.set_fill(STOCK_GREEN, opacity=1)
            d.set_stroke(WHITE, width=2)
            d.move_to(right_panel.get_center() + pos)
            trend_dots.add(d)

        trend_lines = VGroup()
        for i in range(len(trend_dots) - 1):
            line = Line(trend_dots[i].get_center(),
                        trend_dots[i + 1].get_center())
            line.set_stroke(STOCK_GREEN, width=3)
            trend_lines.add(line)

        trend_arrow = Arrow(
            trend_dots[-1].get_center(),
            trend_dots[-1].get_center() + RIGHT * 0.8 + UP * 0.3,
            stroke_width=3, buff=0.1,
        )
        trend_arrow.set_color(STOCK_GREEN)

        connected_label = Text("Connected trend", font_size=39, weight=BOLD)
        connected_label.set_color(SOFT_GRAY)
        connected_label.next_to(right_panel, DOWN, buff=0.45)
        connected_label.shift(DOWN * 0.4)

        self.play(
            FadeIn(left_panel), FadeIn(left_t),
            FadeIn(right_panel), FadeIn(right_t),
            run_time=0.6,
        )
        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in scat_dots],
                         lag_ratio=0.2, run_time=0.6),
            LaggedStart(*[GrowFromCenter(d) for d in trend_dots],
                         lag_ratio=0.2, run_time=0.6),
        )
        self.play(
            FadeIn(isolated_label),
            LaggedStart(*[ShowCreation(l) for l in trend_lines],
                         lag_ratio=0.3, run_time=0.6),
            GrowArrow(trend_arrow),
            FadeIn(connected_label),
            run_time=0.6,
        )
        self.wait(2.5)

        validate_layout(self, label="V2 Scene 4")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        # ==============================================================
        # SCENE 5: Parameter Explosion (~45s)
        # ==============================================================

        title = make_scene_title("Problem 3: Parameter Explosion",
                                  color=PROBLEM_RED, font_size=48)
        title.shift(DOWN * 0.4)
        self.play(FadeIn(title), run_time=0.6)

        # Table with growing bars
        table_data = [
            ("10",     "5,120",       1.2,  MEANING_GREEN),
            ("100",    "51,200",      2.5,  GOLD_ACCENT),
            ("1,000",  "512,000",     4.0,  WINDOW_AMBER),
            ("10,000", "5,120,000",   7.0,  PROBLEM_RED),
        ]

        h_seq = Text("Sequence Length", font_size=28, weight=BOLD)
        h_seq.set_color(SOFT_GRAY)
        h_par = Text("Parameters", font_size=28, weight=BOLD)
        h_par.set_color(SOFT_GRAY)
        h_seq.move_to(LEFT * 4.5 + UP * 1.8)
        h_par.move_to(LEFT * 1.5 + UP * 1.8)

        self.play(FadeIn(h_seq), FadeIn(h_par), run_time=0.3)

        # All bars start from the same x — aligned column
        BAR_START_X = 0.8   # left edge of all bars
        BAR_END_MAX  = 6.5  # right screen limit
        MAX_BAR_W    = BAR_END_MAX - BAR_START_X  # 5.7 max

        rows = VGroup()
        for idx, (seq, params, bar_w, color) in enumerate(table_data):
            y = 1.0 - idx * 0.85

            seq_text = Text(seq, font_size=32, weight=BOLD)
            seq_text.set_color(WHITE)
            seq_text.move_to(LEFT * 4.5 + UP * y)

            arrow = Arrow(LEFT * 0.4, RIGHT * 0.4, stroke_width=2.5, buff=0)
            arrow.set_color(SOFT_GRAY)
            arrow.move_to(LEFT * 2.8 + UP * y)

            par_text = Text(params, font_size=32, weight=BOLD)
            par_text.set_color(color)
            par_text.move_to(LEFT * 1.2 + UP * y)
            if color == PROBLEM_RED:
                par_text.shift(RIGHT * 0.19)

            # Bar always starts from BAR_START_X, never exceeds screen right
            actual_bar_w = min(bar_w, MAX_BAR_W)
            bar = Rectangle(width=actual_bar_w, height=0.4)
            bar.set_fill(color, opacity=0.6)
            bar.set_stroke(color, width=2)
            bar.move_to(np.array([BAR_START_X + actual_bar_w / 2, y, 0]))

            row = VGroup(seq_text, arrow, par_text, bar)
            rows.add(row)

            rt = 0.3 if idx < 3 else 0.8
            self.play(
                FadeIn(seq_text), GrowArrow(arrow), FadeIn(par_text),
                GrowFromCenter(bar),
                run_time=rt,
            )

        self.wait(1)

        # Audio example
        table_group = VGroup(h_seq, h_par, rows)
        self.play(FadeOut(table_group), run_time=0.4)

        audio_line1 = Text("10 seconds of audio @ 16kHz", font_size=38,
                            weight=BOLD)
        audio_line1.set_color(WAVE_BLUE)
        audio_line1.move_to(UP * 1.8)

        audio_line2 = Text("= 160,000 input samples", font_size=38,
                            weight=BOLD)
        audio_line2.set_color(WAVE_BLUE)
        audio_line2.next_to(audio_line1, DOWN, buff=0.35)

        # Massive red bar — bar and label grow simultaneously, shifted down
        huge_bar = Rectangle(width=12.5, height=0.7)
        huge_bar.set_fill(PROBLEM_RED, opacity=0.5)
        huge_bar.set_stroke(PROBLEM_RED, width=3)
        huge_bar.move_to(DOWN * 0.35)  # UP*0.2 shifted DOWN*0.55

        huge_label = Text("81.9 MILLION parameters (one layer!)",
                           font_size=34, weight=BOLD)
        huge_label.set_color(WHITE)
        huge_label.move_to(huge_bar.get_center())
        huge_combo = VGroup(huge_bar, huge_label)

        self.play(Write(audio_line1), run_time=0.7)
        self.play(Write(audio_line2), run_time=0.7)
        self.play(GrowFromCenter(huge_combo), run_time=1.0)
        self.wait(1)

        # Consequences
        cons = ["Slow training", "Massive memory", "Overfitting"]
        cons_cards = VGroup()
        for txt in cons:
            card = make_problem_card(txt, width=4.0, font_size=32)
            cons_cards.add(card)
        cons_cards.arrange(RIGHT, buff=0.5)
        cons_cards.move_to(DOWN * 1.8)

        self.play(LaggedStart(
            *[FadeIn(c, shift=UP * 0.3) for c in cons_cards],
            lag_ratio=0.2, run_time=1.0,
        ))
        self.wait(2)

        validate_layout(self, label="V2 Scene 5")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        # ==============================================================
        # SCENE 6: The Sliding Window Hack (~45s)
        # ==============================================================

        title = make_scene_title("The Sliding Window Hack",
                                  color=WINDOW_AMBER, font_size=52)
        title.shift(DOWN * 0.4)
        self.play(FadeIn(title), run_time=0.6)

        # Sequence of 12 stock prices
        prices = [100, 105, 98, 110, 107, 115, 112, 120, 118, 125, 122, 130]
        cells = VGroup()
        cell_labels = VGroup()
        cell_w = 0.9
        cell_h = 0.6

        for p in prices:
            cell = Rectangle(width=cell_w, height=cell_h)
            cell.set_fill(DARK_BG, opacity=0.7)
            cell.set_stroke(SOFT_GRAY, width=1.5)
            cells.add(cell)

            lbl = Text(str(p), font_size=22, weight=BOLD)
            lbl.set_color(WHITE)
            cell_labels.add(lbl)

        cells.arrange(RIGHT, buff=0)
        cells.move_to(UP * 0.3)

        for i, lbl in enumerate(cell_labels):
            lbl.move_to(cells[i].get_center())

        self.play(LaggedStart(
            *[FadeIn(VGroup(cells[i], cell_labels[i]))
              for i in range(len(prices))],
            lag_ratio=0.04, run_time=1.0,
        ))

        # Sliding window highlight
        window = RoundedRectangle(
            width=cell_w * 3 + 0.15, height=cell_h + 0.25,
            corner_radius=0.1,
        )
        window.set_fill(WINDOW_AMBER, opacity=0.12)
        window.set_stroke(WINDOW_AMBER, width=3.5)
        window.move_to(cells[1].get_center())

        win_label = Text("Window (size 3)", font_size=28, weight=BOLD)
        win_label.set_color(WINDOW_AMBER)
        win_label.next_to(window, UP, buff=0.3)

        self.play(FadeIn(window), FadeIn(win_label), run_time=0.5)

        # Mini ANN below
        mini_in = make_nn_layer(3, ANN_BLUE, radius=0.25, spacing=0.65)
        mini_h = make_nn_layer(3, HIDDEN_TEAL, radius=0.25, spacing=0.65)
        mini_out = make_nn_layer(1, OUTPUT_GOLD, radius=0.25, spacing=0.65)
        mini_nn = VGroup(mini_in, mini_h, mini_out)
        mini_nn.arrange(RIGHT, buff=0.65)
        mini_nn.move_to(DOWN * 1.74)

        mini_c1 = make_nn_connections(mini_in[0], mini_h[0], stroke_width=1,
                                       opacity=0.3)
        mini_c2 = make_nn_connections(mini_h[0], mini_out[0], stroke_width=1,
                                       opacity=0.3)

        pred_txt = Text("Predict next", font_size=28, weight=BOLD)
        pred_txt.set_color(OUTPUT_GOLD)
        pred_txt.next_to(mini_out, RIGHT, buff=0.4)

        self.play(
            FadeIn(mini_nn), FadeIn(mini_c1), FadeIn(mini_c2),
            FadeIn(pred_txt), run_time=0.5,
        )
        self.bring_to_back(*list(mini_c1), *list(mini_c2))
        self.wait(0.5)

        # Slide the window across
        for _ in range(5):
            self.play(
                window.animate.shift(RIGHT * cell_w),
                win_label.animate.shift(RIGHT * cell_w),
                run_time=0.35,
            )

        self.wait(0.5)

        # Show limitation: long-range dependency
        self.play(
            FadeOut(window), FadeOut(win_label), FadeOut(mini_nn),
            FadeOut(mini_c1), FadeOut(mini_c2), FadeOut(pred_txt),
            run_time=0.3,
        )

        # Highlight early and late cells
        early_rect = SurroundingRectangle(
            VGroup(cells[1], cell_labels[1]),
            color=MEANING_GREEN, buff=0.08,
        )
        early_rect.set_stroke(width=3)
        late_rect = SurroundingRectangle(
            VGroup(cells[9], cell_labels[9]),
            color=MEANING_GREEN, buff=0.08,
        )
        late_rect.set_stroke(width=3)

        # Broken connection line — with more breathing room below cells
        broken_line = DashedLine(
            cells[1].get_center() + DOWN * 0.75,
            cells[9].get_center() + DOWN * 0.75,
            dash_length=0.15,
        )
        broken_line.set_stroke(PROBLEM_RED, width=3)

        x_mark = Text("X", font_size=52, weight=BOLD)
        x_mark.set_color(PROBLEM_RED)
        x_mark.move_to(broken_line.get_center() + DOWN * 0.05)

        cant_see = Text("Can't see! Too far apart", font_size=42, weight=BOLD)
        cant_see.set_color(PROBLEM_RED)
        cant_see.next_to(broken_line, DOWN, buff=0.85)

        self.play(ShowCreation(early_rect), ShowCreation(late_rect), run_time=0.4)
        self.play(ShowCreation(broken_line), FadeIn(x_mark, scale=1.5),
                  run_time=0.6)
        self.play(FadeIn(cant_see, shift=UP * 0.2), run_time=0.5)
        self.wait(1.5)

        # Dilemma
        self.play(*[FadeOut(m) for m in self.mobjects if m is not title],
                  run_time=0.4)

        # Dilemma — two enclosed boxes stacked vertically with VS between
        def make_dilemma_box(txt, color=PROBLEM_RED):
            lbl = Text(txt, font_size=32, weight=BOLD)
            lbl.set_color(WHITE)
            bg = RoundedRectangle(
                width=max(lbl.get_width() + 1.2, 7.5),
                height=lbl.get_height() + 0.55,
                corner_radius=0.14,
            )
            bg.set_fill(DARK_BG, opacity=0.75)
            bg.set_stroke(color, width=2.5)
            lbl.move_to(bg.get_center())
            return VGroup(bg, lbl)

        dilemma_l = make_dilemma_box("Small window  =  miss long patterns")
        vs = Text("VS", font_size=44, weight=BOLD)
        vs.set_color(SOFT_GRAY)
        dilemma_r = make_dilemma_box("Big window  =  parameter explosion")

        stack = VGroup(dilemma_l, vs, dilemma_r)
        stack.arrange(DOWN, buff=0.35)
        stack.move_to(DOWN * 0.5)

        no_win = Text("NO WIN", font_size=60, weight=BOLD)
        no_win.set_color(PROBLEM_RED)
        no_win.next_to(stack, DOWN, buff=0.55)

        self.play(FadeIn(dilemma_l, shift=LEFT * 0.3), run_time=0.5)
        self.play(FadeIn(vs, scale=1.2), run_time=0.3)
        self.play(FadeIn(dilemma_r, shift=RIGHT * 0.3), run_time=0.5)
        self.play(FadeIn(no_win, scale=1.5), run_time=0.6)
        self.wait(2)

        validate_layout(self, label="V2 Scene 6")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        # ==============================================================
        # SCENE 7: Conclusion — ANNs Cannot Handle Sequences (~30s)
        #   (NO RNN — this is ONLY about ANN limitations)
        # ==============================================================

        title = make_scene_title("The Bottom Line", color=WHITE, font_size=56)
        title.shift(DOWN * 0.5)
        self.play(FadeIn(title), run_time=0.6)

        # Three problems displayed as definitive failure cards
        problems = [
            "1.  Fixed-size inputs",
            "2.  No memory",
            "3.  Parameter explosion",
        ]

        prob_cards = VGroup()
        for txt in problems:
            label = Text(txt, font_size=40, weight=BOLD)
            label.set_color(WHITE)
            bg = RoundedRectangle(
                width=max(label.get_width() + 1.2, 9.0),
                height=label.get_height() + 0.5,
                corner_radius=0.15,
            )
            bg.set_fill(DARK_BG, opacity=0.7)
            bg.set_stroke(PROBLEM_RED, width=2.5)
            label.move_to(bg.get_center())
            prob_cards.add(VGroup(bg, label))

        prob_cards.arrange(DOWN, buff=0.35)
        prob_cards.move_to(DOWN * 0.7)

        # Appear one by one with impact
        for card in prob_cards:
            self.play(FadeIn(card, shift=LEFT * 0.4), run_time=0.5)
            self.wait(0.3)

        self.wait(1)

        # Red X overlays
        x_marks = VGroup()
        for card in prob_cards:
            x = Text("X", font_size=60, weight=BOLD)
            x.set_color(PROBLEM_RED)
            x.set_opacity(0.5)
            x.move_to(card[0].get_right() + LEFT * 0.6)
            x_marks.add(x)

        self.play(LaggedStart(
            *[FadeIn(x, scale=2.0) for x in x_marks],
            lag_ratio=0.15, run_time=0.8,
        ))
        self.wait(1.5)

        # Final statement — NO RNN teaser
        self.play(
            FadeOut(prob_cards), FadeOut(x_marks), FadeOut(title),
            run_time=0.6,
        )

        final = Text(
            "Standard neural networks\ncannot handle sequential data.",
            font_size=52, weight=BOLD,
        )
        final.set_color(WHITE)
        final.move_to(ORIGIN)

        self.play(Write(final), run_time=2.0)
        self.wait(4)

        validate_layout(self, label="V2 Scene 7")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        self.wait(1)


# =====================================================================
# SCENE: RNN — Recurrent Neural Networks
# =====================================================================
#   Run standalone:
#       manimgl a.py RNNScene
#       manimgl a.py RNNScene -w --hd
# =====================================================================

# =====================================================================
# SCENE: RNN — Recurrent Neural Networks
# =====================================================================
#   manimgl a.py RNNScene
#   manimgl a.py RNNScene -w --hd
# =====================================================================

# =====================================================================
# SCENE: RNN — Recurrent Neural Networks  v3
# =====================================================================
#   manimgl a.py RNNScene
#   manimgl a.py RNNScene -w --hd
# =====================================================================

RNN_MAROON = "#800020"
RNN_ORANGE = "#FF7700"
RNN_PINK   = "#FF1493"   # deep-pink / fuchsia for Wa / horizontal recurrent

class RNNScene(InteractiveScene):
    def construct(self):
        self._build_rnn(self)

    @staticmethod
    def _build_rnn(scene):

        def slbl(base, sup, fb=52, fs=48, col=WHITE, sw=2.5):
            _bmap = {"\u0177": r"\hat{y}"}
            b_str = _bmap.get(base, base)
            if sup:
                inner = sup.strip("<>")
                inner = {"Tx": r"T_x", "Ty": r"T_y"}.get(inner, inner)
                tex_str = rf"{b_str}^{{\langle {inner} \rangle}}"
            else:
                tex_str = b_str
            t = Tex(tex_str, font_size=fb); t.set_color(col); t.set_stroke(col, width=sw); return t

        RED = "#FF0000"

        # ─── PART 1: Feedforward ANN ──────────────────────────────────

        title_ann = make_scene_title("Feedforward Neural Network",
                                     color=ANN_BLUE, font_size=55)   # scaled up x1.1
        title_ann.shift(DOWN * 0.6)
        scene.play(FadeIn(title_ann), run_time=0.6)

        in_l  = make_nn_layer(3, ANN_BLUE,    spacing=1.0, radius=0.25,
                              label_text="Input",    label_color=ANN_BLUE)
        hd1   = make_nn_layer(4, HIDDEN_TEAL, spacing=1, radius=0.22,
                              label_text="Hidden 1", label_color=HIDDEN_TEAL)
        hd2   = make_nn_layer(4, HIDDEN_TEAL, spacing=1, radius=0.22,
                              label_text="Hidden 2", label_color=HIDDEN_TEAL)
        out_l = make_nn_layer(2, OUTPUT_GOLD, spacing=1, radius=0.25,
                              label_text="Output",   label_color=OUTPUT_GOLD)

        nn_g = VGroup(in_l, hd1, hd2, out_l)
        nn_g.arrange(RIGHT, buff=1.2)
        nn_g.move_to(DOWN * 0.70)

        iN, h1N, h2N, oN = in_l[0], hd1[0], hd2[0], out_l[0]
        c1 = make_nn_connections(iN, h1N)
        c2 = make_nn_connections(h1N, h2N)
        c3 = make_nn_connections(h2N, oN)

        for layer, conn, nodes in [
            (in_l,  None, iN), (hd1, c1, h1N),
            (hd2,   c2,   h2N), (out_l, c3, oN),
        ]:
            anims = [LaggedStart(*[GrowFromCenter(n) for n in nodes],
                                 lag_ratio=0.10, run_time=0.5)]
            if len(layer) > 1:
                anims.append(FadeIn(layer[1], shift=UP * 0.1))
            scene.play(*anims, run_time=0.5)
            if conn is not None:
                scene.play(LaggedStart(*[ShowCreation(l) for l in conn],
                                       lag_ratio=0.005, run_time=0.5))
                scene.bring_to_back(*list(conn))

        scene.bring_to_back(*list(c3), *list(c2), *list(c1))
        scene.wait(1.5)

        # ─── PART 2: Compact block — shifted down, same title ─────────

        x_circ = Circle(radius=0.54)
        x_circ.set_fill(ANN_BLUE, opacity=0.90); x_circ.set_stroke(WHITE, width=2.8)
        h_rect = RoundedRectangle(width=1.50, height=1.50, corner_radius=0.18)
        h_rect.set_fill(HIDDEN_TEAL, opacity=0.90); h_rect.set_stroke(WHITE, width=2.8)
        y_circ = Circle(radius=0.54)
        y_circ.set_fill(OUTPUT_GOLD, opacity=0.90); y_circ.set_stroke(WHITE, width=2.8)

        compact_geo = VGroup(x_circ, h_rect, y_circ)
        compact_geo.arrange(RIGHT, buff=1.2)
        compact_geo.move_to(DOWN * 0.35)    # shifted down

        x_lbl = Text("x", font_size=46, weight=BOLD); x_lbl.set_color(WHITE)
        h_lbl = Text("H", font_size=58, weight=BOLD); h_lbl.set_color(WHITE)
        y_lbl = Text("y", font_size=46, weight=BOLD); y_lbl.set_color(DARK_BG)
        x_lbl.move_to(x_circ.get_center())
        h_lbl.move_to(h_rect.get_center())
        y_lbl.move_to(y_circ.get_center())

        x_mob = VGroup(x_circ, x_lbl)
        h_mob = VGroup(h_rect, h_lbl)
        y_mob = VGroup(y_circ, y_lbl)

        arr_xh = Arrow(x_circ.get_right(), h_rect.get_left(), stroke_width=3, buff=0.08)
        arr_xh.set_color(SOFT_GRAY)
        arr_hy = Arrow(h_rect.get_right(), y_circ.get_left(), stroke_width=3, buff=0.08)
        arr_hy.set_color(SOFT_GRAY)

        # Cross-fade: ANN out, compact in — title_ann stays
        scene.play(
            *[FadeOut(m) for m in [nn_g, c1, c2, c3]],
            FadeIn(x_mob), FadeIn(arr_xh), FadeIn(h_mob), FadeIn(arr_hy), FadeIn(y_mob),
            run_time=1.0,
        )
        scene.wait(0.8)

        # ─── PART 3: Rotate 90° CCW + counter-rotate labels ───────────

        block_grp = VGroup(x_mob, arr_xh, h_mob, arr_hy, y_mob)
        pivot = block_grp.get_center()

        # Fade out ANN title during rotation
        scene.play(
            Rotate(block_grp, angle=PI / 2, about_point=pivot),
            FadeOut(title_ann),
            run_time=1.5,
        )
        scene.wait(0.3)

        scene.play(
            Rotate(x_mob, -PI / 2, about_point=x_mob.get_center()),
            Rotate(h_mob, -PI / 2, about_point=h_mob.get_center()),
            Rotate(y_mob, -PI / 2, about_point=y_mob.get_center()),
            run_time=0.40,
        )
        scene.wait(0.3)

        # Shift entire block LEFT to give room for RNN label on right
        scene.play(block_grp.animate.shift(LEFT * 1.8), run_time=0.5)
        scene.wait(0.3)

        # ─── Self-loop as a SINGLE VMobject path ──────────────────────
        LC = RNN_ORANGE
        LW = 4.5

        hc  = h_mob.get_center().copy()
        hw  = h_mob.get_width() / 2
        lR, lD = 1.0, 1.3

        LP0 = h_mob.get_right().copy()
        LP1 = np.array([hc[0] + hw + lR, hc[1],      0])
        LP2 = np.array([hc[0] + hw + lR, hc[1] - lD, 0])
        LP3 = np.array([hc[0] - hw - lR, hc[1] - lD, 0])
        LP4 = np.array([hc[0] - hw - lR, hc[1],      0])
        LP5 = h_mob.get_left().copy()

        # Single continuous VMobject — no corner artifacts
        loop_path = VMobject()
        loop_path.set_points_as_corners([LP0, LP1, LP2, LP3, LP4])
        loop_path.set_stroke(LC, width=LW*1.84)
        loop_path.set_color(LC)
        loop_path.set_z_index(-1)

        # Arrow for final segment (same stroke_width)
        loop_arr = Arrow(LP4, LP5, stroke_width=LW*0.4, buff=0.0).shift(DOWN*0.05)
        loop_arr.set_color(LC)
        loop_arr.set_stroke(LC, width=LW)
        loop_arr.set_z_index(-1)

        scene.play(ShowCreation(loop_path), run_time=1.0)
        scene.play(GrowArrow(loop_arr), run_time=0.40)

        # "recurrent" label — left of the left vertical segment (LP3→LP4)
        loop_lbl = Text("Recurrent", font_size=36, weight=BOLD)
        loop_lbl.set_color(LC)
        loop_lbl.next_to(loop_path, LEFT, buff=0.25)
        loop_lbl.set_y(hc[1] - lD / 2)   # vertically centered on left segment
        scene.play(FadeIn(loop_lbl), run_time=0.35)

        # RNN title on right side of screen
        rnn_side = Text("(RNN)",
                        font_size=100, weight=BOLD)
        rnn_side.set_color(TEAL_ACCENT)
        rnn_side.move_to(RIGHT * 3.35 + DOWN * 0.0)
        scene.play(Write(rnn_side), run_time=0.9)
        scene.wait(2.0)



        validate_layout(scene, label="RNN compact loop")
        scene.play(*[FadeOut(m) for m in scene.mobjects], run_time=0.8)

        # ─── PART 4: Unrolled RNN (no title) ─────────────────────────

        Y_H  =  0.55
        Y_X  = -1.55
        Y_Y  =  2.65
        Y_A  =  1.10   # activation labels above H-H arrows (lowered)

        A0_X = -5.7           # shifted: further left + 0.5 right offset
        HX   = [-3.3, -0.3,  2.7]
        DOTS =  4.1          # exact midpoint of H3(2.7) and HT(5.5)
        HT   =  5.5

        R_H  = 0.40
        R_A  = 0.52   # bigger activation circles
        R_XY = 0.62   # x/input circles (blue, slightly larger)
        R_Y  = 0.64   # y/output circles (yellow, slightly larger)

        # ── a<0> ──────────────────────────────────────────────────────
        a0c = Circle(radius=R_A)
        a0c.set_fill(MEMORY_PURPLE, opacity=0.92)
        a0c.set_stroke(WHITE, width=2.8)
        a0c.move_to(np.array([A0_X, Y_H, 0]))
        a0t = slbl("a", "<0>", fb=48, fs=48, col=WHITE, sw=1.5)
        a0t.move_to(a0c.get_center())
        a0_mob = VGroup(a0c, a0t)
        a0_zero = Text("(zero)", font_size=24)
        a0_zero.set_color(SOFT_GRAY)
        a0_zero.next_to(a0_mob, DOWN, buff=0.20)
        # a0 shown after pulses and after a1/a2 labels appear

        # ── H / x / y columns ─────────────────────────────────────────
        ALL_HX  = HX + [HT]
        H_TAGS  = ["1", "2", "3", "T"]
        X_TAGS  = ["1", "2", "3", None]   # None -> use Tex for T column
        Y_TAGS  = ["1", "2", "3", None]   # None -> use Tex for T column

        h_nodes, x_mobs, y_mobs = [], [], []
        for tx, htag, xtag, ytag in zip(ALL_HX, H_TAGS, X_TAGS, Y_TAGS):
            hs = RoundedRectangle(width=R_H*2.2, height=R_H*2.2, corner_radius=0.12)
            hs.set_fill(HIDDEN_TEAL, opacity=0.90)
            hs.set_stroke(WHITE, width=2)
            hs.move_to(np.array([tx, Y_H, 0]))
            hl = Tex(r"\mathrm{H}", font_size=60)
            hl.set_color(WHITE); hl.set_stroke(WHITE, width=2.5)
            hl.move_to(hs.get_center())
            h_nodes.append(VGroup(hs, hl))

            xc = Circle(radius=R_XY)
            xc.set_fill(ANN_BLUE, opacity=0.90)
            xc.set_stroke(WHITE, width=2)
            xc.move_to(np.array([tx, Y_X, 0]))
            xl = slbl("x", f"<{xtag if xtag else 'Tx'}>", fb=52, fs=48, col=WHITE, sw=1.5)
            xl.move_to(xc.get_center())
            x_mobs.append(VGroup(xc, xl))

            yc = Circle(radius=R_Y)
            yc.set_fill(OUTPUT_GOLD, opacity=0.90)
            yc.set_stroke(WHITE, width=2)
            yc.move_to(np.array([tx, Y_Y, 0]))
            yl = slbl("\u0177", f"<{ytag if ytag else 'Ty'}>", fb=52, fs=48, col=DARK_BG, sw=1.5)
            yl.move_to(yc.get_center())
            y_mobs.append(VGroup(yc, yl))

        for ti in range(3):
            scene.play(GrowFromCenter(h_nodes[ti]),
                       GrowFromCenter(x_mobs[ti]),
                       GrowFromCenter(y_mobs[ti]), run_time=0.38)

        dots_mob = Tex(r"\cdots", font_size=64)
        dots_mob.set_color(SOFT_GRAY); dots_mob.set_stroke(SOFT_GRAY, width=2.5)
        dots_mob.move_to(np.array([DOTS, Y_H, 0]))
        scene.play(FadeIn(dots_mob), run_time=0.30)
        scene.play(GrowFromCenter(h_nodes[3]),
                   GrowFromCenter(x_mobs[3]),
                   GrowFromCenter(y_mobs[3]), run_time=0.40)
        scene.wait(0.2)

        # ── Wx: x<t> → H<t> — labels on ALL columns ──────────────────
        wx_arrs = VGroup()
        wx_lbls = VGroup()
        for ti in range(4):
            a = Arrow(x_mobs[ti].get_top() + UP * 0.04,
                      h_nodes[ti].get_bottom() + DOWN * 0.04,
                      stroke_width=2.5, buff=0.04)
            a.set_color(ANN_BLUE)
            wx_arrs.add(a)
            lw = Tex(r"W_x", font_size=48)
            lw.set_color(ANN_BLUE)
            lw.next_to(a, RIGHT, buff=0.08)
            wx_lbls.add(lw)

        # ── Wy: H<t> → y<t> — labels on ALL columns ──────────────────
        wy_arrs = VGroup()
        wy_lbls = VGroup()
        for ti in range(4):
            a = Arrow(h_nodes[ti].get_top() + UP * 0.04,
                      y_mobs[ti].get_bottom() + DOWN * 0.04,
                      stroke_width=2.5, buff=0.04)
            a.set_color(OUTPUT_GOLD)
            wy_arrs.add(a)
            lw = Tex(r"W_y", font_size=48)
            lw.set_color(OUTPUT_GOLD)
            lw.next_to(a, RIGHT, buff=0.08)
            wy_lbls.add(lw)

        # ── Direct Wa: H<t> → H<t+1> — Wa BELOW, a<t> circle ABOVE ──
        wa_segs = []
        wa_lbls = VGroup()
        a_circs = []

        def wa_seg(p1, p2, label=None):
            ar = Arrow(p1, p2, stroke_width=2.5, buff=0.04)
            ar.set_color(RNN_PINK)
            wa_segs.append(ar)
            if label:
                lb = Tex(label, font_size=48)
                lb.set_color(RNN_PINK)
                lb.next_to(ar, DOWN, buff=0.12)
                wa_lbls.add(lb)

        wa_seg(a0_mob.get_right()     + RIGHT * 0.04,
               h_nodes[0].get_left() + LEFT  * 0.04, r"W_a")
        wa_seg(h_nodes[0].get_right() + RIGHT * 0.04,
               h_nodes[1].get_left() + LEFT  * 0.04, r"W_a")
        wa_seg(h_nodes[1].get_right() + RIGHT * 0.04,
               h_nodes[2].get_left() + LEFT  * 0.04, r"W_a")
        # No arrow from H3->dots or dots->HT; "..." implies continuation

        # a_texts: plain white activation labels shown after pulses (no circles)
        a_texts = []
        for li, ri in [(0, 1), (1, 2)]:
            mid_x = (HX[li] + HX[ri]) / 2
            ac = Circle(radius=R_A)
            ac.set_fill(MEMORY_PURPLE, opacity=0.90)
            ac.set_stroke(WHITE, width=2.5)
            ac.move_to(np.array([mid_x, Y_A, 0]))
            at = slbl("a", f"<{li+1}>", fb=48, fs=48, col=WHITE, sw=1.5)
            at.move_to(ac.get_center())
            a_circs.append(VGroup(ac, at))
            # plain text label at same position (no circle)
            at2 = slbl("a", f"<{li+1}>", fb=52, fs=48, col=RNN_PINK, sw=1.5)
            at2.move_to(ac.get_center())
            a_texts.append(at2)

        scene.play(
            LaggedStart(*[GrowArrow(a) for a in wx_arrs], lag_ratio=0.2, run_time=0.8),
            LaggedStart(*[FadeIn(l)   for l in wx_lbls], lag_ratio=0.2, run_time=0.8),
        )
        scene.play(
            LaggedStart(*[GrowArrow(a) for a in wa_segs], lag_ratio=0.08, run_time=1.0),
            LaggedStart(*[FadeIn(l)   for l in wa_lbls],  lag_ratio=0.10, run_time=1.0),
        )
        # Show Wy arrows + a0/a1/a2 labels all at the same time
        scene.play(
            LaggedStart(*[GrowArrow(a) for a in wy_arrs], lag_ratio=0.2, run_time=0.8),
            LaggedStart(*[FadeIn(l)   for l in wy_lbls],  lag_ratio=0.2, run_time=0.8),
            GrowFromCenter(a0_mob), FadeIn(a0_zero),
            *[FadeIn(a) for a in a_texts],
        )
        scene.wait(0.5)
        validate_layout(scene, label="RNN unrolled connections")

        # ─── BRIGHT GLOWING PULSES (pure red glow, no node recoloring) ─

        def glow_pulse(start, end):
            outer = Dot(radius=0.20); outer.set_fill("#FF3333", opacity=0.50)
            outer.set_stroke(width=0); outer.set_z_index(6)
            inner = Dot(radius=0.10); inner.set_fill(WHITE, opacity=1.0)
            inner.set_stroke(width=0); inner.set_z_index(7)
            p = VGroup(outer, inner); p.move_to(start)
            scene.play(GrowFromCenter(p), run_time=0.10)
            scene.play(p.animate.move_to(end), run_time=0.36)
            scene.play(FadeOut(p), run_time=0.10)

        SRC_WA = [0, 1, 2]

        for ti in range(3):
            # dual pulse: x→H and a_prev→H simultaneously (no node color change)
            dx = Dot(radius=0.20); dx.set_fill("#FF3333", opacity=0.50)
            dx.set_stroke(width=0); dx.set_z_index(2)
            dx_in = Dot(radius=0.10); dx_in.set_fill(WHITE, opacity=1.0)
            dx_in.set_stroke(width=0); dx_in.set_z_index(3)
            dpx = VGroup(dx, dx_in); dpx.move_to(wx_arrs[ti].get_start())

            da = Dot(radius=0.20); da.set_fill("#FF3333", opacity=0.50)
            da.set_stroke(width=0); da.set_z_index(2)
            da_in = Dot(radius=0.10); da_in.set_fill(WHITE, opacity=1.0)
            da_in.set_stroke(width=0); da_in.set_z_index(3)
            dpa = VGroup(da, da_in); dpa.move_to(wa_segs[SRC_WA[ti]].get_start())

            scene.play(GrowFromCenter(dpx), GrowFromCenter(dpa), run_time=0.12)
            scene.play(dpx.animate.move_to(wx_arrs[ti].get_end()),
                       dpa.animate.move_to(wa_segs[SRC_WA[ti]].get_end()),
                       run_time=0.38)
            scene.play(FadeOut(dpx), FadeOut(dpa), run_time=0.12)

            if ti < 2:
                glow_pulse(wa_segs[ti + 1].get_start() if ti == 0
                           else wa_segs[ti].get_end(),
                           a_circs[ti][0].get_center())
            glow_pulse(wy_arrs[ti].get_start(), wy_arrs[ti].get_end())

        scene.wait(0.5)
        validate_layout(scene, label="RNN pulse done")

        # Zoom out + shift camera slightly down for equations
        scene.play(
            scene.camera.frame.animate.scale(1.25).shift(DOWN * 0.8),
            run_time=0.8,
        )

        # ─── EQUATIONS ────────────────────────────────────────────────
        EQ_Y  = -3.30   # equation rows (more buff from diagram)
        EQ_FS = 48      # font size scaled up ~1.6x

        def etxt(s, col=WHITE, bold=False):
            t = Tex(s, font_size=EQ_FS); t.set_color(col); return t

        scene.play(
            Indicate(h_nodes[1][0],  color=RED,           scale_factor=1.25),
            Indicate(a_texts[0],     color=MEMORY_PURPLE, scale_factor=1.25),
            Indicate(x_mobs[1][0],   color=ANN_BLUE,      scale_factor=1.25),
            run_time=0.7,
        )

        EQ_SUB = 38   # subscript size scaled with EQ_FS

        a2_lhs   = slbl("a", "<2>",  fb=EQ_FS, fs=EQ_SUB, col=RNN_PINK, sw=0)
        eq_sep   = etxt(r"= f(")
        eq_Wa    = etxt(r"W_a",  col=RNN_PINK)
        eq_dot1  = etxt(r"\cdot")
        eq_a1    = slbl("a", "<1>",  fb=EQ_FS, fs=EQ_SUB, col=RNN_PINK, sw=0)
        eq_plus  = etxt(r"+")
        eq_Wx    = etxt(r"W_x",  col=ANN_BLUE)
        eq_dot2  = etxt(r"\cdot")
        eq_x2    = slbl("x", "<2>",  fb=EQ_FS, fs=EQ_SUB, col=ANN_BLUE, sw=0)
        eq_plus2 = etxt(r"+")
        eq_ba    = etxt(r"b_a",  col=RNN_PINK)
        eq_rp    = etxt(r")")

        row1 = VGroup(a2_lhs, eq_sep, eq_Wa, eq_dot1, eq_a1,
                      eq_plus, eq_Wx, eq_dot2, eq_x2, eq_plus2, eq_ba, eq_rp)
        row1.arrange(RIGHT, buff=0.18)
        row1.scale(1.33)
        row1.move_to(np.array([0, EQ_Y, 0])).shift(DOWN*0.15)

        # a2 flies from diagram position to LHS of equation
        a2_lhs_target = a2_lhs.get_center().copy()
        a2_lhs.move_to(a_texts[1].get_center())

        wa_copy = wa_lbls[1].copy()
        a1_copy = a_texts[0].copy()
        wx_copy = wx_lbls[1].copy()
        x2_copy = x_mobs[1][1].copy()

        # Step 1: LHS a<2> flies from diagram to equation
        scene.play(
            a2_lhs.animate.move_to(a2_lhs_target),
            run_time=1.0,
        )
        # Step 2: rest of equation expands
        scene.play(
            FadeIn(eq_sep), FadeIn(eq_dot1),
            FadeIn(eq_plus), FadeIn(eq_dot2),
            FadeIn(eq_plus2), FadeIn(eq_rp),
            Transform(wa_copy, eq_Wa),
            Transform(a1_copy, eq_a1),
            Transform(wx_copy, eq_Wx),
            Transform(x2_copy, eq_x2),
            FadeIn(eq_ba),
            run_time=1.0,
        )
        scene.wait(1.2)

        y2_lhs   = slbl("y", "<2>",  fb=EQ_FS, fs=EQ_SUB, col=OUTPUT_GOLD, sw=0)
        eq_sep2  = etxt(r"= g(")
        eq_Wy    = etxt(r"W_y",  col=OUTPUT_GOLD)
        eq_dot3  = etxt(r"\cdot")
        eq_a2r   = slbl("a", "<2>",  fb=EQ_FS, fs=EQ_SUB, col=RNN_PINK, sw=0)
        eq_plus3 = etxt(r"+")
        eq_by    = etxt(r"b_y",  col=OUTPUT_GOLD)
        eq_rp2   = etxt(r")")

        row2 = VGroup(y2_lhs, eq_sep2, eq_Wy, eq_dot3, eq_a2r, eq_plus3, eq_by, eq_rp2)
        row2.arrange(RIGHT, buff=0.18)
        row2.scale(1.33)
        row2.next_to(row1, DOWN, buff=0.70)

        # y2 flies from diagram position to LHS of equation
        y2_lhs_target = y2_lhs.get_center().copy()
        y2_lhs.move_to(y_mobs[1][1].get_center())

        wy_copy  = wy_lbls[1].copy()
        a2r_copy = a_texts[1].copy()

        # Step 1: LHS y<2> flies from diagram
        scene.play(
            y2_lhs.animate.move_to(y2_lhs_target),
            run_time=1.0,
        )
        # Step 2: rest of y equation
        scene.play(
            FadeIn(eq_sep2), FadeIn(eq_dot3),
            FadeIn(eq_plus3), FadeIn(eq_rp2),
            Transform(wy_copy,  eq_Wy),
            Transform(a2r_copy, eq_a2r),
            FadeIn(eq_by),
            run_time=1.0,
        )
        scene.wait(1.5)

        g_a_lhs  = slbl("a", "<t>",   fb=EQ_FS, fs=EQ_SUB, col=RNN_PINK, sw=0)
        g_sep    = etxt(r"= f(")
        g_Wa     = etxt(r"W_a",  col=RNN_PINK)
        g_dot1   = etxt(r"\cdot")
        g_atm1   = slbl("a", "<t-1>", fb=EQ_FS, fs=EQ_SUB, col=RNN_PINK, sw=0)
        g_plus   = etxt(r"+")
        g_Wx     = etxt(r"W_x",  col=ANN_BLUE)
        g_dot2   = etxt(r"\cdot")
        g_xt     = slbl("x", "<t>",   fb=EQ_FS, fs=EQ_SUB, col=ANN_BLUE, sw=0)
        g_plus2  = etxt(r"+")
        g_ba     = etxt(r"b_a",  col=RNN_PINK)
        g_rp     = etxt(r")")
        grow1 = VGroup(g_a_lhs, g_sep, g_Wa, g_dot1, g_atm1,
                       g_plus, g_Wx, g_dot2, g_xt, g_plus2, g_ba, g_rp)
        grow1.arrange(RIGHT, buff=0.18)
        grow1.scale(1.33)
        grow1.move_to(row1.get_center())

        g_y_lhs  = slbl("y", "<t>",   fb=EQ_FS, fs=EQ_SUB, col=OUTPUT_GOLD, sw=0)
        g_sep2   = etxt(r"= g(")
        g_Wy     = etxt(r"W_y",  col=OUTPUT_GOLD)
        g_dot3   = etxt(r"\cdot")
        g_at     = slbl("a", "<t>",   fb=EQ_FS, fs=EQ_SUB, col=RNN_PINK, sw=0)
        g_plus3  = etxt(r"+")
        g_by     = etxt(r"b_y",  col=OUTPUT_GOLD)
        g_rp2    = etxt(r")")
        grow2 = VGroup(g_y_lhs, g_sep2, g_Wy, g_dot3, g_at, g_plus3, g_by, g_rp2)
        grow2.arrange(RIGHT, buff=0.18)
        grow2.scale(1.33)
        grow2.move_to(row2.get_center())

        scene.play(
            ReplacementTransform(row1,   grow1),
            ReplacementTransform(row2,   grow2),
            FadeOut(wa_copy), FadeOut(a1_copy),
            FadeOut(wx_copy), FadeOut(x2_copy),
            FadeOut(wy_copy), FadeOut(a2r_copy),
            run_time=1.0,
        )
        scene.wait(2.0)

        # Fade out H labels, move a1/a2 into squares (turn white), create a3/aT
        h_label_fades = [FadeOut(h_nodes[i][1]) for i in range(4)]  # fade "H" text

        # a3 and aT labels created at their H positions (appear from nothing)
        a3_txt = slbl("a", "<3>", fb=52, fs=48, col=WHITE, sw=1.5)
        a3_txt.move_to(h_nodes[2].get_center())
        aT_txt = slbl("a", "<Tx>", fb=52, fs=48, col=WHITE, sw=1.5)
        aT_txt.move_to(h_nodes[3].get_center())

        # Widen the HT square to fit a<Tx>
        hT_sq_wide = RoundedRectangle(width=R_H*3.2, height=R_H*2.2, corner_radius=0.12)
        hT_sq_wide.set_fill(HIDDEN_TEAL, opacity=0.90)
        hT_sq_wide.set_stroke(WHITE, width=2)
        hT_sq_wide.move_to(h_nodes[3][0].get_center())

        scene.play(
            *h_label_fades,
            # a1, a2 move into H1, H2 and turn white
            a_texts[0].animate.move_to(h_nodes[0].get_center()).set_color(WHITE),
            a_texts[1].animate.move_to(h_nodes[1].get_center()).set_color(WHITE),
            # a3, aT fade in at H3, HT
            FadeIn(a3_txt), FadeIn(aT_txt),
            # widen HT square simultaneously
            Transform(h_nodes[3][0], hT_sq_wide),
            run_time=1.0,
        )
        scene.wait(2.0)

        # Store refs for BackpropRNN
        scene.rnn_h_nodes = h_nodes
        scene.rnn_x_mobs  = x_mobs
        scene.rnn_y_mobs  = y_mobs
        scene.rnn_a0_mob  = a0_mob
        scene.rnn_wa_segs = wa_segs
        scene.rnn_wx_arrs = wx_arrs
        scene.rnn_wy_arrs = wy_arrs
        scene.rnn_grow1   = grow1
        scene.rnn_grow2   = grow2

        validate_layout(scene, label="RNN forward prop")
# ═══════════════════════════════════════════════════════════════════════════════
#  BackpropRNN — Backpropagation Through Time
#  Starts directly with the unrolled grid (no intro).
#  Hidden state squares use a^<t> labels (not H).
#  Shows: loss labels → backward arrows → gradient pulses
#         → chain rules for Wy, by, Wx, Wa, bx → weight update
# ═══════════════════════════════════════════════════════════════════════════════
class BackpropRNN(InteractiveScene):
    def construct(self):
        # ── Colors (matching RNNTypes) ────────────────────────────────
        HIDDEN_TEAL   = "#1ABC9C"
        ANN_BLUE      = "#2980B9"
        OUTPUT_GOLD   = "#F1C40F"
        RNN_PINK      = "#FF1493"
        BPTT_RED      = "#FF2222"
        LOSS_RED      = "#FF5555"
        MEMORY_PURPLE = "#8B5CF6"
        SOFT_GRAY     = "#AAAAAA"

        EQ_Y  = -4.60
        EQ_FS = 46

        def btex(s, col=WHITE, fs=EQ_FS):
            t = Tex(s, font_size=fs); t.set_color(col); return t

        def pos_eq(eq):
            eq.move_to(np.array([0, EQ_Y, 0]))
            return eq

        # ── Square node helpers (same style as RNNTypes) ──────────────
        R   = 0.40
        CR  = 0.10
        SW  = 2.5
        SQ_SC = 1.25

        Y_H  = -0.20
        Y_X  = -2.30
        Y_Y  =  1.70

        def _sq(pos, col, w=None):
            s = RoundedRectangle(width=(w or R * 2) * SQ_SC,
                                 height=R * 2 * SQ_SC, corner_radius=CR)
            s.set_fill(col, opacity=0.92)
            s.set_stroke(WHITE, width=SW)
            s.move_to(pos)
            return s

        def h_node(pos, t=None, col=HIDDEN_TEAL, tcol=BLACK):
            sq = _sq(pos, col)
            lstr = (r"a^{\langle " + str(t) + r"\rangle}") if t is not None else r"a"
            lb = Tex(lstr, font_size=30)
            lb.set_color(tcol)
            lb.set_stroke(tcol, width=1.2)
            lb.scale(1.6)
            lb.move_to(pos)
            return VGroup(sq, lb)

        def x_node(pos, t=None):
            sq = _sq(pos, ANN_BLUE)
            lstr = (r"x^{\langle " + str(t) + r"\rangle}") if t is not None else r"x"
            lb = Tex(lstr, font_size=30)
            lb.set_color(WHITE)
            lb.set_stroke(WHITE, width=1.2)
            lb.scale(2)
            lb.move_to(pos)
            return VGroup(sq, lb)

        def y_node(pos, t=None):
            sq = _sq(pos, OUTPUT_GOLD)
            lstr = (r"\hat{y}^{\langle " + str(t) + r"\rangle}") if t is not None else r"\hat{y}"
            lb = Tex(lstr, font_size=30)
            lb.set_color(BLACK)
            lb.set_stroke(BLACK, width=1.2)
            lb.scale(1.8)
            lb.move_to(pos)
            return VGroup(sq, lb)

        def mk_arr(a, b, col=SOFT_GRAY):
            ar = Arrow(a, b, buff=0.06, stroke_width=2.5)
            ar.set_color(col)
            return ar

        # ── 1. Build unrolled grid — 4 explicit timesteps ────────────
        T  = 4
        SP = 3.10
        X_OFF = 0.50          # shift grid right to center visual mass (a0 pulls left)
        HX = [-(T - 1) * SP / 2 + i * SP + X_OFF for i in range(T)]
        A0_X = HX[0] - 2.0

        # a<0> initial state (square, purple)
        a0_mob = h_node(np.array([A0_X, Y_H, 0]), t=0, col=MEMORY_PURPLE, tcol=WHITE)
        a0_zero = Text("(zero)", font_size=24, weight=BOLD).set_color(SOFT_GRAY)
        a0_zero.next_to(a0_mob, DOWN, buff=0.20)

        # 4 timestep columns
        h_nodes = [h_node(np.array([HX[i], Y_H, 0]), t=i + 1) for i in range(T)]
        x_mobs  = [x_node(np.array([HX[i], Y_X, 0]), t=i + 1) for i in range(T)]
        y_mobs  = [y_node(np.array([HX[i], Y_Y, 0]), t=i + 1) for i in range(T)]

        # Wx arrows (x → a^<t>)
        wx_arrs = VGroup()
        wx_lbls = VGroup()
        for ti in range(T):
            a = mk_arr(x_mobs[ti].get_top(), h_nodes[ti].get_bottom(), ANN_BLUE)
            wx_arrs.add(a)
            lw = Tex(r"W_x", font_size=42).set_color(ANN_BLUE)
            lw.next_to(a, RIGHT, buff=0.08); wx_lbls.add(lw)

        # Wy arrows (a^<t> → ŷ^<t>)
        wy_arrs = VGroup()
        wy_lbls = VGroup()
        for ti in range(T):
            a = mk_arr(h_nodes[ti].get_top(), y_mobs[ti].get_bottom(), OUTPUT_GOLD)
            wy_arrs.add(a)
            lw = Tex(r"W_y", font_size=42).set_color(OUTPUT_GOLD)
            lw.next_to(a, RIGHT, buff=0.08); wy_lbls.add(lw)

        # Wa recurrent arrows (a^<t-1> → a^<t>)
        wa_segs = []
        wa_lbl_list = []

        def wa_seg_fn(p1, p2, show_lbl=True):
            ar = mk_arr(p1, p2, RNN_PINK)
            wa_segs.append(ar)
            if show_lbl:
                lb = Tex(r"W_a", font_size=42).set_color(RNN_PINK)
                lb.next_to(ar, DOWN, buff=0.12); wa_lbl_list.append(lb)

        wa_seg_fn(a0_mob.get_right(), h_nodes[0].get_left())
        for i in range(T - 1):
            wa_seg_fn(h_nodes[i].get_right(), h_nodes[i + 1].get_left())
        wa_lbls = VGroup(*wa_lbl_list)

        # Appear: all nodes at once, then arrows
        self.play(
            LaggedStart(
                *[FadeIn(m) for m in [a0_mob, a0_zero, *h_nodes,
                                      *x_mobs, *y_mobs]],
                lag_ratio=0.05, run_time=1.0,
            )
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in wx_arrs], lag_ratio=0.12, run_time=0.6),
            LaggedStart(*[GrowArrow(a) for a in wy_arrs], lag_ratio=0.12, run_time=0.6),
            LaggedStart(*[GrowArrow(a) for a in wa_segs], lag_ratio=0.10, run_time=0.7),
            FadeIn(wx_lbls), FadeIn(wy_lbls), FadeIn(wa_lbls),
        )
        self.wait(0.4)

        # Zoom camera — gentler than before
        self.play(
            self.camera.frame.animate.scale(1.28).shift(DOWN * 1.17),
            run_time=0.7,
        )

        # ── Pulse helpers ──────────────────────────────────────────────
        def mk_pulse(col=BPTT_RED, r=0.18):
            o = Dot(radius=r);    o.set_fill(col, opacity=0.65); o.set_stroke(width=0)
            i = Dot(radius=r*.5); i.set_fill(WHITE, opacity=1.0); i.set_stroke(width=0)
            return VGroup(o, i)

        def run_pulse(stops, col=BPTT_RED, rt=0.22):
            p = mk_pulse(col); p.move_to(stops[0])
            self.play(GrowFromCenter(p), run_time=0.08)
            for s in stops[1:]:
                self.play(p.animate.move_to(s), run_time=rt)
            self.play(FadeOut(p), run_time=0.10)

        def restore_h_fills():
            self.play(*[h_nodes[ni][0].animate.set_fill(HIDDEN_TEAL, opacity=0.92)
                        for ni in range(T)], run_time=0.25)

        # ── 2. Loss labels L^<t> — scaled up, more buff ──────────────
        loss_tags = ["1", "2", "3", "4"]
        loss_lbs  = VGroup()
        for i, tag in enumerate(loss_tags):
            lb = Tex(rf"L^{{\langle {tag} \rangle}}", font_size=52)
            lb.set_color(LOSS_RED); lb.set_stroke(LOSS_RED, width=1.5)
            lb.scale(1.27)
            lb.next_to(y_mobs[i], UP, buff=0.40)
            loss_lbs.add(lb)

        # What is L^<t>?
        eq_Ldef = pos_eq(VGroup(
            btex(r"L^{\langle t \rangle}", col=LOSS_RED),
            btex(r"="),
            btex(r"\mathcal{L}(\hat{y}^{\langle t \rangle},\, y^{\langle t \rangle})"),
        ).arrange(RIGHT, buff=0.16).scale(1.70))

        eq_Ltot = pos_eq(VGroup(
            btex(r"L"),
            btex(r"="),
            btex(r"\sum_{t=1}^{4}"),
            btex(r"L^{\langle t \rangle}", col=LOSS_RED),
        ).arrange(RIGHT, buff=0.16).scale(1.70))

        self.play(
            LaggedStart(*[FadeIn(lb, shift=DOWN*0.15) for lb in loss_lbs],
                        lag_ratio=0.25, run_time=1.2)
        )
        self.play(Write(eq_Ldef), run_time=0.9)
        self.wait(1.2)
        self.play(FadeOut(eq_Ldef), run_time=0.4)
        self.play(Write(eq_Ltot), run_time=0.9)
        self.wait(1.0)
        self.play(FadeOut(eq_Ltot), run_time=0.4)

        # ── 3. Backward red arrows — kept visible throughout ──────────
        bk_wy = [
            Arrow(y_mobs[ti].get_bottom() + DOWN*0.04,
                  h_nodes[ti].get_top()   + UP*0.04,
                  stroke_width=3.0, buff=0.08,
                  ).set_color(BPTT_RED).shift(LEFT*0.22)
            for ti in range(T)
        ]
        bk_wx = [
            Arrow(h_nodes[ti].get_bottom() + DOWN*0.04,
                  x_mobs[ti].get_top()     + UP*0.04,
                  stroke_width=3.0, buff=0.08,
                  ).set_color(BPTT_RED).shift(LEFT*0.22)
            for ti in range(T)
        ]
        bk_wa = [
            Arrow(wa_segs[i].get_end()   + RIGHT*0.06,
                  wa_segs[i].get_start() + LEFT*0.06,
                  stroke_width=3.0, buff=0.10,
                  ).set_color(BPTT_RED).shift(UP*0.24)
            for i in range(len(wa_segs))
        ]

        self.play(
            LaggedStart(*[GrowArrow(a) for a in reversed(bk_wy)],
                        lag_ratio=0.20, run_time=1.0),
            LaggedStart(*[GrowArrow(a) for a in reversed(bk_wx)],
                        lag_ratio=0.20, run_time=1.0),
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in reversed(bk_wa)],
                        lag_ratio=0.20, run_time=1.0),
        )
        self.wait(0.5)

        # ── 4. Overview — dramatic BPTT cascade ──────────────────────
        # Pulse from each loss converging backward through hidden states
        for ti in reversed(range(T)):
            p = mk_pulse(BPTT_RED, r=0.20); p.move_to(loss_lbs[ti].get_center())
            self.play(GrowFromCenter(p), run_time=0.06)
            self.play(p.animate.move_to(y_mobs[ti].get_center()), run_time=0.14)
            self.play(
                p.animate.move_to(h_nodes[ti].get_center()),
                h_nodes[ti][0].animate.set_fill(BPTT_RED, opacity=0.75),
                run_time=0.14,
            )
            self.remove(p)
        # Sweep backward
        for ni in range(T - 1, 0, -1):
            self.play(h_nodes[ni - 1][0].animate.set_fill(BPTT_RED, opacity=0.75),
                      run_time=0.16)
        self.wait(0.3)
        restore_h_fills()
        self.wait(0.3)

        # ── Weight update rule — shown FIRST ────────────────────────
        # Flash ALL backward arrows simultaneously
        all_bk = bk_wy + bk_wx + bk_wa
        self.play(
            LaggedStart(*[Indicate(a, color=WHITE, scale_factor=1.15) for a in all_bk],
                        lag_ratio=0.03, run_time=1.2),
        )

        w_upd = pos_eq(VGroup(
            btex(r"W"),
            btex(r"\leftarrow"),
            btex(r"W"),
            btex(r"-\alpha\cdot"),
            btex(r"\frac{\partial L}{\partial W}", col=BPTT_RED),
        ).arrange(RIGHT, buff=0.20).scale(1.70))

        self.play(Write(w_upd), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(w_upd), run_time=0.4)

        # ════════════════════════════════════════════════════════════
        #  5. Chain rules — order: Wy → Wa → Wx → by → ba
        # ════════════════════════════════════════════════════════════

        # ── ∂L/∂Wy (simple — no BPTT) ────────────────────────────────
        # Brief flash to highlight Wy path — NO permanent color change
        self.play(
            LaggedStart(*[Indicate(wy_arrs[i], color=OUTPUT_GOLD, scale_factor=1.25)
                          for i in range(T)], lag_ratio=0.12, run_time=0.7),
        )

        wy_lhs = btex(r"\frac{\partial L}{\partial W_y}", col=OUTPUT_GOLD)
        wy_es  = btex(r"=")
        wy_sm  = btex(r"\sum_{t=1}^{4}")
        wy_t1  = btex(r"\frac{\partial L^{\langle t \rangle}}{\partial \hat{y}^{\langle t \rangle}}",
                      col=LOSS_RED)
        wy_dot = btex(r"\cdot")
        wy_t2  = btex(r"\frac{\partial \hat{y}^{\langle t \rangle}}{\partial W_y}",
                      col=OUTPUT_GOLD)
        wy_full = VGroup(wy_lhs, wy_es, wy_sm, wy_t1, wy_dot, wy_t2) \
            .arrange(RIGHT, buff=0.15).scale(1.38)
        pos_eq(wy_full)

        self.play(Write(wy_lhs), Write(wy_es), Write(wy_sm), run_time=0.8)
        # Parallel pulses: ALL losses → ALL outputs simultaneously
        p_loss = [mk_pulse(LOSS_RED, r=0.16) for _ in range(T)]
        for pi, p in enumerate(p_loss):
            p.move_to(loss_lbs[pi].get_center())
        self.play(*[GrowFromCenter(p) for p in p_loss], run_time=0.08)
        self.play(*[p.animate.move_to(y_mobs[i].get_center())
                    for i, p in enumerate(p_loss)], run_time=0.20)
        self.play(*[FadeOut(p) for p in p_loss], run_time=0.08)
        self.play(Write(wy_t1), run_time=0.6)
        # Parallel pulses: ALL outputs → ALL hidden (gold = Wy path)
        p_out = [mk_pulse(OUTPUT_GOLD, r=0.16) for _ in range(T)]
        for pi, p in enumerate(p_out):
            p.move_to(y_mobs[pi].get_center())
        self.play(*[GrowFromCenter(p) for p in p_out], run_time=0.08)
        self.play(*[p.animate.move_to(h_nodes[i].get_center())
                    for i, p in enumerate(p_out)], run_time=0.20)
        self.play(*[FadeOut(p) for p in p_out], run_time=0.08)
        self.play(FadeIn(wy_dot), Write(wy_t2), run_time=0.6)
        self.wait(2.0)
        self.play(FadeOut(wy_full), run_time=0.4)

        # ── ∂L/∂Wa (BPTT — hardest, chain rule) ──────────────────────
        # Brief flash to highlight Wa path — NO permanent color change
        self.play(
            LaggedStart(*[Indicate(wa_segs[k], color=RNN_PINK, scale_factor=1.25)
                          for k in range(len(wa_segs))], lag_ratio=0.12, run_time=0.7),
        )

        wa_lhs = btex(r"\frac{\partial L}{\partial W_a}", col=RNN_PINK)
        wa_es  = btex(r"=")
        wa_sm  = btex(r"\sum_{t}\sum_{k=1}^{t}")
        wa_t1  = btex(r"\frac{\partial L^{\langle t \rangle}}{\partial a^{\langle t \rangle}}",
                      col=LOSS_RED)
        wa_t2  = btex(r"\cdot\prod_{j=k}^{t-1}"
                      r"\frac{\partial a^{\langle j+1 \rangle}}{\partial a^{\langle j \rangle}}",
                      col=RNN_PINK)
        wa_t3  = btex(r"\cdot\frac{\partial a^{\langle k \rangle}}{\partial W_a}",
                      col=RNN_PINK)
        wa_full = VGroup(wa_lhs, wa_es, wa_sm, wa_t1, wa_t2, wa_t3) \
            .arrange(RIGHT, buff=0.13).scale(1.27)
        pos_eq(wa_full)

        self.play(Write(wa_lhs), Write(wa_es), Write(wa_sm), run_time=0.8)
        # Pulse: loss → ŷ → hidden with node glow
        p = mk_pulse(LOSS_RED, r=0.22); p.move_to(loss_lbs[3].get_center())
        self.play(GrowFromCenter(p), run_time=0.08)
        self.play(p.animate.move_to(y_mobs[3].get_center()), run_time=0.18)
        self.play(
            p.animate.move_to(h_nodes[3].get_center()),
            h_nodes[3][0].animate.set_fill(LOSS_RED, opacity=0.80),
            run_time=0.18,
        )
        self.play(FadeOut(p), run_time=0.06)
        self.play(Write(wa_t1), run_time=0.6)
        # BPTT backward cascade — pink pulse with glow trail
        p2 = mk_pulse(RNN_PINK, r=0.22); p2.move_to(h_nodes[3].get_center())
        self.play(GrowFromCenter(p2), run_time=0.06)
        for k in [2, 1, 0]:
            self.play(
                p2.animate.move_to(h_nodes[k].get_center()),
                h_nodes[k][0].animate.set_fill(RNN_PINK, opacity=0.75),
                run_time=0.22,
            )
        self.play(FadeOut(p2), run_time=0.06)
        self.play(Write(wa_t2), run_time=0.7)
        restore_h_fills()
        # Flash Wa arrows sequentially to show terminal ∂a/∂Wa
        self.play(
            LaggedStart(*[Indicate(wa_segs[k], color=RNN_PINK, scale_factor=1.30)
                          for k in range(len(wa_segs))], lag_ratio=0.30, run_time=0.9),
        )
        self.play(Write(wa_t3), run_time=0.5)
        self.wait(2.0)
        self.play(FadeOut(wa_full), run_time=0.4)

        # ── ∂L/∂Wx (BPTT) ─────────────────────────────────────────────
        # Brief flash to highlight Wx path — NO permanent color change
        self.play(
            LaggedStart(*[Indicate(wx_arrs[i], color=ANN_BLUE, scale_factor=1.25)
                          for i in range(T)], lag_ratio=0.12, run_time=0.7),
        )

        wx_lhs = btex(r"\frac{\partial L}{\partial W_x}", col=ANN_BLUE)
        wx_es  = btex(r"=")
        wx_sm  = btex(r"\sum_{t}\sum_{k=1}^{t}")
        wx_t1  = btex(r"\frac{\partial L^{\langle t \rangle}}{\partial a^{\langle t \rangle}}",
                      col=LOSS_RED)
        wx_t2  = btex(r"\cdot\prod_{j=k}^{t-1}"
                      r"\frac{\partial a^{\langle j+1 \rangle}}{\partial a^{\langle j \rangle}}",
                      col=RNN_PINK)
        wx_t3  = btex(r"\cdot\frac{\partial a^{\langle k \rangle}}{\partial W_x}",
                      col=ANN_BLUE)
        wx_full = VGroup(wx_lhs, wx_es, wx_sm, wx_t1, wx_t2, wx_t3) \
            .arrange(RIGHT, buff=0.13).scale(1.27)
        pos_eq(wx_full)

        self.play(Write(wx_lhs), Write(wx_es), Write(wx_sm), run_time=0.8)
        # Pulse: loss → ŷ → hidden with glow
        p = mk_pulse(LOSS_RED, r=0.22); p.move_to(loss_lbs[3].get_center())
        self.play(GrowFromCenter(p), run_time=0.08)
        self.play(p.animate.move_to(y_mobs[3].get_center()), run_time=0.18)
        self.play(
            p.animate.move_to(h_nodes[3].get_center()),
            h_nodes[3][0].animate.set_fill(LOSS_RED, opacity=0.80),
            run_time=0.18,
        )
        self.play(FadeOut(p), run_time=0.06)
        self.play(Write(wx_t1), run_time=0.6)
        # BPTT backward with glow trail (pink — same recurrent chain)
        p2 = mk_pulse(RNN_PINK, r=0.22); p2.move_to(h_nodes[3].get_center())
        self.play(GrowFromCenter(p2), run_time=0.06)
        for k in [2, 1, 0]:
            self.play(
                p2.animate.move_to(h_nodes[k].get_center()),
                h_nodes[k][0].animate.set_fill(RNN_PINK, opacity=0.75),
                run_time=0.22,
            )
        self.play(FadeOut(p2), run_time=0.06)
        self.play(Write(wx_t2), run_time=0.7)
        restore_h_fills()
        # Blue pulses downward: all hidden → all inputs (Wx terminal term)
        dp = [mk_pulse(ANN_BLUE, r=0.16) for _ in range(T)]
        for pi, d in enumerate(dp):
            d.move_to(h_nodes[pi].get_center())
        self.play(*[GrowFromCenter(d) for d in dp], run_time=0.06)
        self.play(*[d.animate.move_to(x_mobs[i].get_center())
                    for i, d in enumerate(dp)], run_time=0.22)
        self.play(*[FadeOut(d) for d in dp], run_time=0.06)
        self.play(
            LaggedStart(*[Indicate(wx_arrs[k], color=ANN_BLUE, scale_factor=1.30)
                          for k in range(T)], lag_ratio=0.25, run_time=0.8),
        )
        self.play(Write(wx_t3), run_time=0.5)
        self.wait(2.0)
        self.play(FadeOut(wx_full), run_time=0.4)

        # ── ∂L/∂by (no BPTT — no pulses) ─────────────────────────────
        # Brief flash on Wy arrows (same path as Wy)
        self.play(
            LaggedStart(*[Indicate(wy_arrs[i], color=OUTPUT_GOLD, scale_factor=1.20)
                          for i in range(T)], lag_ratio=0.10, run_time=0.5),
        )
        by_lhs = btex(r"\frac{\partial L}{\partial b_y}", col=OUTPUT_GOLD)
        by_es  = btex(r"=")
        by_sm  = btex(r"\sum_{t=1}^{4}")
        by_t1  = btex(r"\frac{\partial L^{\langle t \rangle}}{\partial \hat{y}^{\langle t \rangle}}",
                      col=LOSS_RED)
        by_dot = btex(r"\cdot")
        by_t2  = btex(r"\frac{\partial \hat{y}^{\langle t \rangle}}{\partial b_y}",
                      col=OUTPUT_GOLD)
        by_full = VGroup(by_lhs, by_es, by_sm, by_t1, by_dot, by_t2) \
            .arrange(RIGHT, buff=0.15).scale(1.38)
        pos_eq(by_full)

        self.play(Write(by_full), run_time=1.2)
        self.wait(1.8)
        self.play(FadeOut(by_full), run_time=0.4)

        # ── ∂L/∂ba (BPTT — no pulses) ────────────────────────────────
        # Brief flash on Wa arrows (same path as Wa)
        self.play(
            LaggedStart(*[Indicate(wa_segs[k], color=RNN_PINK, scale_factor=1.20)
                          for k in range(len(wa_segs))], lag_ratio=0.10, run_time=0.5),
        )
        ba_lhs = btex(r"\frac{\partial L}{\partial b_a}", col=RNN_PINK)
        ba_es  = btex(r"=")
        ba_sm  = btex(r"\sum_{t}\sum_{k=1}^{t}")
        ba_t1  = btex(r"\frac{\partial L^{\langle t \rangle}}{\partial a^{\langle t \rangle}}",
                      col=LOSS_RED)
        ba_t2  = btex(r"\cdot\prod_{j=k}^{t-1}"
                      r"\frac{\partial a^{\langle j+1 \rangle}}{\partial a^{\langle j \rangle}}",
                      col=RNN_PINK)
        ba_t3  = btex(r"\cdot\frac{\partial a^{\langle k \rangle}}{\partial b_a}",
                      col=RNN_PINK)
        ba_full = VGroup(ba_lhs, ba_es, ba_sm, ba_t1, ba_t2, ba_t3) \
            .arrange(RIGHT, buff=0.13).scale(1.27)
        pos_eq(ba_full)

        self.play(Write(ba_full), run_time=1.2)
        self.wait(1.8)
        self.play(FadeOut(ba_full), run_time=0.4)

        self.wait(2)

        validate_layout(self, label="BackpropRNN")

class RNNTypes(InteractiveScene):
    def construct(self):
        # Colors
        HIDDEN_TEAL = "#1ABC9C"
        ANN_BLUE    = "#2980B9"
        OUTPUT_GOLD = "#F1C40F"
        RNN_PINK    = "#FF1493"
        ENC_BLUE    = "#1565C0"
        DEC_ORANGE  = "#E67E22"
        CTX_PURPLE  = "#8E44AD"
        SOFT_GRAY   = "#AAAAAA"

        R   = 0.40
        CR  = 0.10
        SW  = 2.5
        Y_X = -1.95
        Y_H = -0.20
        Y_Y =  1.50
        SP  =  2.30

        SQ_SC = 1.25  # square scale factor
        def _sq(pos, col, w=None):
            s = RoundedRectangle(width=(w or R * 2) * SQ_SC, height=R * 2 * SQ_SC, corner_radius=CR)
            s.set_fill(col, opacity=0.92)
            s.set_stroke(WHITE, width=SW)
            s.move_to(pos)
            return s

        def h_node(pos, t=None, col=HIDDEN_TEAL, tcol=BLACK):
            sq = _sq(pos, col)
            lstr = (r"a^{\langle " + str(t) + r"\rangle}") if t is not None else r"a"
            lb = Tex(lstr, font_size=30)
            lb.set_color(tcol)
            lb.set_stroke(tcol, width=1.2)
            lb.scale(1.6)
            lb.move_to(pos)
            return VGroup(sq, lb)

        def x_node(pos, t=None):
            sq = _sq(pos, ANN_BLUE)
            lstr = (r"x^{\langle " + str(t) + r"\rangle}") if t is not None else r"x"
            lb = Tex(lstr, font_size=30)
            lb.set_color(WHITE)
            lb.set_stroke(WHITE, width=1.2)
            lb.scale(2)
            lb.move_to(pos)
            return VGroup(sq, lb)

        def y_node(pos, t=None):
            sq = _sq(pos, OUTPUT_GOLD)
            lstr = (r"\hat{y}^{\langle " + str(t) + r"\rangle}") if t is not None else r"\hat{y}"
            lb = Tex(lstr, font_size=30)
            lb.set_color(BLACK)
            lb.set_stroke(BLACK, width=1.2)
            lb.scale(1.8)
            lb.move_to(pos)
            return VGroup(sq, lb)

        def word_box(word, pos, col, tcol=WHITE, font=None, fs=28, pad=0.40):
            kw = {"font": font} if font else {}
            lb = Text(word, font_size=fs, weight=BOLD, color=tcol, **kw)
            bw = max(lb.get_width() + pad, R * 2 * SQ_SC)
            sq = RoundedRectangle(width=bw, height=R * 2 * SQ_SC, corner_radius=CR)
            sq.set_fill(col, opacity=0.92)
            sq.set_stroke(WHITE, width=SW)
            sq.move_to(pos)
            lb.move_to(pos)
            return VGroup(sq, lb)

        def ctx_node(pos):
            sq = _sq(pos, CTX_PURPLE, w=R * 2)  # same size as other squares
            lb = Tex(r"\mathbf{c}", font_size=38)
            lb.set_color(WHITE)
            lb.set_stroke(WHITE, width=1.2)
            lb.scale(1.6)
            lb.move_to(pos)
            return VGroup(sq, lb)

        def mk_arr(a, b, col=SOFT_GRAY):
            ar = Arrow(a, b, buff=0.06, stroke_width=2.5)
            ar.set_color(col)
            return ar

        def mk_curve(a, b, col=OUTPUT_GOLD, ang=-TAU / 5):
            ar = CurvedArrow(a, b, angle=ang, stroke_width=2.2)
            ar.set_color(col)
            return ar

        def run_pulse(pts, col, rt=0.20):
            dot = Dot(radius=0.13, color=col)
            dot.move_to(pts[0])
            self.add(dot)
            for p in pts[1:]:
                self.play(dot.animate.move_to(p), run_time=rt, rate_func=linear)
            self.remove(dot)

        def sec_title(main, sub=None):
            t = Text(main, font_size=46, weight=BOLD, color=WHITE)
            t.to_edge(UP, buff=0.28)
            if sub:
                s = Text(sub, font_size=27, weight=BOLD, color=SOFT_GRAY)
                s.next_to(t, DOWN, buff=0.28)
                return VGroup(t, s)
            return t

        T  = 4
        HX = [-(T - 1) * SP / 2 + i * SP for i in range(T)]

        # ═══════════════════════════════════════════════════════════
        # 1. ONE-TO-ONE
        # ═══════════════════════════════════════════════════════════
        FRAME_B = -4.0  # bottom of default frame

        t1  = sec_title("One-to-One", "Single input  -  single output  |  No memory")
        x1  = x_node(np.array([0.0, Y_X, 0]))
        a1  = h_node(np.array([0.0, Y_H, 0]))
        y1  = y_node(np.array([0.0, Y_Y, 0]))
        ax1 = mk_arr(x1.get_top(),  a1.get_bottom(), ANN_BLUE)
        ay1 = mk_arr(a1.get_top(),  y1.get_bottom(), OUTPUT_GOLD)
        ex1_y = (x1.get_bottom()[1] + FRAME_B) / 2
        ex1 = Text("e.g.  Image Classification  -  cat vs. dog",
                   font_size=30, weight=BOLD, color=SOFT_GRAY)
        ex1.move_to(np.array([0, ex1_y, 0]))

        self.play(Write(t1), run_time=0.6)
        self.play(FadeIn(x1, shift=UP * 0.2), run_time=0.35)
        self.play(GrowArrow(ax1), FadeIn(a1, shift=UP * 0.2), run_time=0.45)
        self.play(GrowArrow(ay1), FadeIn(y1, shift=UP * 0.2), run_time=0.45)
        self.play(Write(ex1), run_time=0.5)
        run_pulse([x1.get_center(), a1.get_center(), y1.get_center()], ANN_BLUE)
        self.wait(1.8)
        self.play(FadeOut(VGroup(t1, x1, a1, y1, ax1, ay1, ex1)), run_time=0.4)

        # ═══════════════════════════════════════════════════════════
        # 2. ONE-TO-MANY  (curvy feedback arrows)
        # ═══════════════════════════════════════════════════════════
        t2  = sec_title("One-to-Many", "Single input  -  output fed back as next step input")
        x2  = x_node(np.array([HX[0], Y_X, 0]))
        h2  = [h_node(np.array([HX[i], Y_H, 0]), t=i + 1) for i in range(T)]
        y2  = [y_node(np.array([HX[i], Y_Y, 0]), t=i + 1) for i in range(T)]
        ax2 = mk_arr(x2.get_top(), h2[0].get_bottom(), ANN_BLUE)
        ah2 = [mk_arr(h2[i].get_right(), h2[i + 1].get_left(), RNN_PINK) for i in range(T - 1)]
        ay2 = [mk_arr(h2[i].get_top(),  y2[i].get_bottom(), OUTPUT_GOLD) for i in range(T)]
        def s_feedback(y_mob, h_next, col=CTX_PURPLE):
            start = y_mob.get_right()
            end   = h_next.get_bottom()
            mid_x = (start[0] + end[0]) / 2
            tip_h = 0.18
            curve_end = np.array([end[0], end[1] - tip_h, 0])
            low_y = Y_X + 0.3
            SW_FB = 3.5
            # 4 lines: RIGHT → DOWN → RIGHT → UP into triangle
            p1 = np.array([mid_x, start[1], 0])    # end of RIGHT
            p2 = np.array([mid_x, low_y, 0])        # end of DOWN (same x as p1)
            p3 = np.array([end[0], low_y, 0])        # end of RIGHT (same y as p2, same x as triangle)
            p4 = curve_end                            # UP into triangle
            seg1 = Line(start, p1, stroke_width=SW_FB).set_color(col)
            seg2 = Line(p1, p2, stroke_width=SW_FB).set_color(col)
            seg3 = Line(p2, p3, stroke_width=SW_FB).set_color(col)
            seg4 = Line(p3, p4, stroke_width=SW_FB).set_color(col)
            for s in [seg1, seg2, seg3, seg4]:
                s.set_z_index(-2)
            # Upward-pointing triangle
            ts = 0.09
            tip = Polygon(
                end,
                curve_end + LEFT * ts,
                curve_end + RIGHT * ts,
            )
            tip.set_fill(col, opacity=1)
            tip.set_stroke(width=0)
            return VGroup(seg1, seg2, seg3, seg4, tip)

        fb2 = [s_feedback(y2[i], h2[i + 1]) for i in range(T - 1)]

        ex2a = Text("Image / Video Captioning", font_size=28, weight=BOLD, color=OUTPUT_GOLD)
        ex2b = Text("Music & Story Generation", font_size=28, weight=BOLD, color=RNN_PINK)
        ex2_y = (x2.get_bottom()[1] + FRAME_B) / 2
        ex2  = VGroup(ex2a, ex2b).arrange(RIGHT, buff=0.9)
        ex2.move_to(np.array([0, ex2_y, 0]))

        self.play(Write(t2), run_time=0.6)
        self.play(FadeIn(x2), run_time=0.30)
        self.play(GrowArrow(ax2), FadeIn(h2[0]), run_time=0.40)
        for i in range(T - 1):
            self.play(GrowArrow(ah2[i]), FadeIn(h2[i + 1]), run_time=0.32)
        for i in range(T):
            self.play(GrowArrow(ay2[i]), FadeIn(y2[i]), run_time=0.25)
        for fb in fb2:
            self.play(ShowCreation(fb), run_time=0.35)
        self.play(Write(ex2), run_time=0.6)
        run_pulse([x2.get_center()] + [h2[i].get_center() for i in range(T)], RNN_PINK)
        for i in range(T):
            run_pulse([h2[i].get_center(), y2[i].get_center()], OUTPUT_GOLD, rt=0.17)
        self.wait(1.8)
        self.play(FadeOut(VGroup(t2, x2, *h2, *y2, ax2, *ah2, *ay2, *fb2, ex2)), run_time=0.4)

        # ═══════════════════════════════════════════════════════════
        # 3. MANY-TO-ONE
        # ═══════════════════════════════════════════════════════════
        t3  = sec_title("Many-to-One", "Full sequence in  -  single prediction out")
        x3  = [x_node(np.array([HX[i], Y_X, 0]), t=i + 1) for i in range(T)]
        h3  = [h_node(np.array([HX[i], Y_H, 0]), t=i + 1) for i in range(T)]
        y3  = y_node(np.array([HX[-1], Y_Y, 0]))
        ax3 = [mk_arr(x3[i].get_top(), h3[i].get_bottom(), ANN_BLUE) for i in range(T)]
        ah3 = [mk_arr(h3[i].get_right(), h3[i + 1].get_left(), RNN_PINK) for i in range(T - 1)]
        ay3 = mk_arr(h3[-1].get_top(), y3.get_bottom(), OUTPUT_GOLD)

        sent_words = ["I", "love", "this", "movie"]
        s_boxes = []
        for w in sent_words:
            lb = Text(w, font_size=26, weight=BOLD, color=WHITE)
            bw = max(lb.get_width() + 0.38, 0.72)
            sq = RoundedRectangle(width=bw, height=0.72, corner_radius=0.08)
            sq.set_fill(ANN_BLUE, opacity=0.85)
            sq.set_stroke(WHITE, width=2.0)
            lb.move_to(ORIGIN)
            s_boxes.append(VGroup(sq, lb))
        sent_row  = VGroup(*s_boxes).arrange(RIGHT, buff=0.18)
        sw_y = (Y_X - R + FRAME_B) / 2
        sent_row.move_to(np.array([0, sw_y, 0]))
        sent_res  = Text("  Positive  (95%)", font_size=28, weight=BOLD, color=OUTPUT_GOLD)
        sent_darr = Text("->", font_size=28, weight=BOLD, color=SOFT_GRAY)
        sent_rhs  = VGroup(sent_darr, sent_res).arrange(RIGHT, buff=0.10)
        sent_rhs.next_to(sent_row, RIGHT, buff=0.30)
        sent_head = Text("Sentiment Analysis:", font_size=26, weight=BOLD, color=SOFT_GRAY)
        sent_head.next_to(sent_row, LEFT, buff=0.30)
        sent_grp  = VGroup(sent_head, sent_row, sent_rhs)

        self.play(Write(t3), run_time=0.6)
        for i in range(T):
            self.play(FadeIn(x3[i]), GrowArrow(ax3[i]), FadeIn(h3[i]), run_time=0.30)
            if i < T - 1:
                self.play(GrowArrow(ah3[i]), run_time=0.22)
        self.play(GrowArrow(ay3), FadeIn(y3), run_time=0.45)
        self.play(FadeIn(sent_grp, shift=UP * 0.15), run_time=0.6)
        run_pulse([x3[0].get_center()] +
                  [h3[i].get_center() for i in range(T)] + [y3.get_center()],
                  OUTPUT_GOLD)
        self.wait(1.8)
        self.play(FadeOut(VGroup(t3, *x3, *h3, y3, *ax3, *ah3, ay3, sent_grp)), run_time=0.4)

        # ═══════════════════════════════════════════════════════════
        # 4. SEQ2SEQ  (Many-to-Many, encoder-decoder)
        # ═══════════════════════════════════════════════════════════
        self.play(self.camera.frame.animate.scale(1.26).shift(DOWN * 0.20), run_time=0.5)

        t4 = sec_title("Many-to-Many  -  Seq2Seq",
                       "Encoder reads input  |  Decoder generates output of any length")
        t4[0].scale(1.2).shift(UP * 0.15)
        t4[1].scale(1.15).shift(UP * 0.12)

        EY     = Y_H
        ENC_X  = [-6.30, -4.20, -2.10]
        CTX_PX = -0.40
        DEC_X  = [1.10,   3.20,  5.30,  7.40]

        enc_h = [h_node(np.array([ENC_X[i], EY, 0]), col=ENC_BLUE, tcol=WHITE) for i in range(3)]

        eng   = ["I", "love", "music"]
        enc_x = [word_box(eng[i], np.array([ENC_X[i], Y_X, 0]),
                          ANN_BLUE, WHITE, fs=28) for i in range(3)]

        ctx     = ctx_node(np.array([CTX_PX, EY, 0]))
        ctx_txt = Text("context", font_size=24, weight=BOLD, color=WHITE)
        ctx_bg  = RoundedRectangle(
            width=ctx_txt.get_width() + 0.30,
            height=ctx_txt.get_height() + 0.18,
            corner_radius=0.08,
        )
        ctx_bg.set_fill(CTX_PURPLE, opacity=1)
        ctx_bg.set_stroke(WHITE, width=1.5)
        ctx_sub = VGroup(ctx_bg, ctx_txt)
        ctx_sub.next_to(ctx, DOWN, buff=0.22)
        ctx_sub.set_z_index(3)

        dec_h = [h_node(np.array([DEC_X[i], EY, 0]), col=DEC_ORANGE, tcol=WHITE) for i in range(4)]

        hindi = ["\u092e\u0941\u091d\u0947",
                 "\u0938\u0902\u0917\u0940\u0924",
                 "\u092a\u0938\u0902\u0926",
                 "\u0939\u0948"]
        dec_y = [word_box(hindi[i], np.array([DEC_X[i], Y_Y, 0]),
                          OUTPUT_GOLD, BLACK, font="Nirmala UI", fs=26)
                 for i in range(4)]
        for dy in dec_y:
            dy[1].set_color(BLACK)

        arr_ex  = [mk_arr(enc_x[i].get_top(),   enc_h[i].get_bottom(), ANN_BLUE) for i in range(3)]
        arr_eh  = [mk_arr(enc_h[i].get_right(),  enc_h[i + 1].get_left(), ENC_BLUE) for i in range(2)]
        arr_ec  = mk_arr(enc_h[-1].get_right(),  ctx.get_left(),       CTX_PURPLE)
        arr_cd  = mk_arr(ctx.get_right(),         dec_h[0].get_left(), CTX_PURPLE)
        arr_dh  = [mk_arr(dec_h[i].get_right(),  dec_h[i + 1].get_left(), DEC_ORANGE) for i in range(3)]
        arr_dy  = [mk_arr(dec_h[i].get_top(),    dec_y[i].get_bottom(), OUTPUT_GOLD) for i in range(4)]

        enc_lbl  = Text("ENCODER  (3 words)", font_size=26, weight=BOLD, color=ENC_BLUE)
        enc_lbl.scale(1.5)
        enc_lbl.move_to(np.array([np.mean(ENC_X), Y_X - 1.75, 0]))
        dec_lbl  = Text("DECODER  (4 words)", font_size=26, weight=BOLD, color=DEC_ORANGE)
        dec_lbl.scale(1.5)
        dec_lbl.move_to(np.array([np.mean(DEC_X), Y_X - 1.75, 0]))
        div_x    = (ENC_X[-1] + DEC_X[0]) / 2
        div_line = DashedLine(np.array([div_x, Y_X - 2.05, 0]),
                              np.array([div_x, Y_Y + 0.52, 0]),
                              color=SOFT_GRAY, stroke_width=1.5)
        # camera scaled 1.26 shifted DOWN 0.20 → visible bottom ≈ -0.20 - 4.0*1.26 = -5.24
        vis_bot = -0.20 - 4.0 * 1.26
        enc_bot = enc_lbl.get_bottom()[1]
        trans_y = (enc_bot + vis_bot) / 2
        trans_lbl = Tex(r"\text{English} \longrightarrow \text{Hindi (Devanagari)}",
                        font_size=32, color=SOFT_GRAY)
        trans_lbl.move_to(np.array([0, trans_y, 0]))

        self.play(Write(t4), run_time=0.7)
        self.play(FadeIn(enc_lbl), FadeIn(dec_lbl), FadeIn(div_line), run_time=0.5)
        for i in range(3):
            self.play(FadeIn(enc_x[i]), GrowArrow(arr_ex[i]), FadeIn(enc_h[i]), run_time=0.32)
            if i < 2:
                self.play(GrowArrow(arr_eh[i]), run_time=0.22)
        self.play(GrowArrow(arr_ec), FadeIn(ctx), FadeIn(ctx_sub), run_time=0.55)
        self.play(GrowArrow(arr_cd), FadeIn(dec_h[0]), run_time=0.40)
        for i in range(3):
            self.play(GrowArrow(arr_dh[i]), FadeIn(dec_h[i + 1]), run_time=0.30)
        for i in range(4):
            self.play(GrowArrow(arr_dy[i]), FadeIn(dec_y[i]), run_time=0.24)
        self.play(FadeIn(trans_lbl), run_time=0.45)

        run_pulse([enc_x[0].get_center()] +
                  [enc_h[i].get_center() for i in range(3)] +
                  [ctx.get_center()], ENC_BLUE, rt=0.20)
        run_pulse([ctx.get_center()] + [dec_h[i].get_center() for i in range(4)],
                  DEC_ORANGE, rt=0.20)
        for i in range(4):
            run_pulse([dec_h[i].get_center(), dec_y[i].get_center()], OUTPUT_GOLD, rt=0.17)

        self.wait(2.5)
        validate_layout(self, label="RNNTypes", camera_scale=1.26)

class DeepRNN(InteractiveScene):
    def construct(self):
        # ── Colors ───────────────────────────────────────────────────
        HIDDEN_TEAL   = "#1ABC9C"
        OUTPUT_GOLD   = "#F1C40F"
        SOFT_GRAY     = "#AAAAAA"
        INIT_GRAY     = "#555555"

        # Per-layer weight colors (different color = different weight matrix)
        WA_COLS = ["#FF1493", "#9B59B6", "#E67E22"]   # Wa: pink, purple, orange
        WX_COLS = ["#2980B9", "#00BCD4", "#2ECC71"]   # Wx: blue, cyan, green

        EQ_Y  = -6.20
        EQ_FS = 46

        def btex(s, col=WHITE, fs=EQ_FS):
            t = Tex(s, font_size=fs); t.set_color(col); return t

        def pos_eq(eq):
            eq.move_to(np.array([0, EQ_Y, 0]))
            return eq

        # ── Square node helpers ──────────────────────────────────────
        R     = 0.48
        CR    = 0.10
        SW    = 2.5
        SQ_SC = 1.30
        NODE_W = 1.15   # wider rectangle width

        # Vertical positions
        Y_X  = -4.20
        Y_H1 = -1.80
        Y_H2 =  0.20
        Y_H3 =  2.20
        Y_Y  =  4.20
        Y_LAYERS = [Y_H1, Y_H2, Y_H3]
        L = 3

        def _sq(pos, col, w=None):
            s = RoundedRectangle(width=(w or NODE_W) * SQ_SC,
                                 height=R * 2 * SQ_SC, corner_radius=CR)
            s.set_fill(col, opacity=0.92)
            s.set_stroke(WHITE, width=SW)
            s.move_to(pos)
            return s

        def h_node_deep(pos, layer, t, col=HIDDEN_TEAL, tcol=BLACK):
            sq = _sq(pos, col)
            lstr = r"a^{(" + str(layer) + r")\langle " + str(t) + r"\rangle}"
            lb = Tex(lstr, font_size=34)
            lb.set_color(tcol); lb.set_stroke(tcol, width=1.2)
            lb.scale(1.5)
            lb.move_to(pos)
            return VGroup(sq, lb)

        def x_node(pos, t=None):
            sq = _sq(pos, "#2980B9")
            lstr = (r"x^{\langle " + str(t) + r"\rangle}") if t is not None else r"x"
            lb = Tex(lstr, font_size=34)
            lb.set_color(WHITE); lb.set_stroke(WHITE, width=1.2)
            lb.scale(2.1)
            lb.move_to(pos)
            return VGroup(sq, lb)

        def y_node(pos, t=None):
            sq = _sq(pos, OUTPUT_GOLD)
            lstr = (r"\hat{y}^{\langle " + str(t) + r"\rangle}") if t is not None else r"\hat{y}"
            lb = Tex(lstr, font_size=34)
            lb.set_color(BLACK); lb.set_stroke(BLACK, width=1.2)
            lb.scale(1.9)
            lb.move_to(pos)
            return VGroup(sq, lb)

        INIT_PURPLE = "#A855F7"

        def zero_node(pos, layer):
            circ = Circle(radius=0.68)
            circ.set_fill(INIT_PURPLE, opacity=0.88)
            circ.set_stroke(WHITE, width=2.0)
            circ.move_to(pos)
            lstr = r"a^{(" + str(layer) + r")\langle 0\rangle}"
            lb = Tex(lstr, font_size=32)
            lb.set_color(BLACK); lb.set_stroke(BLACK, width=1.0)
            lb.scale(1.3)
            lb.move_to(pos)
            return VGroup(circ, lb)

        def mk_arr(a, b, col=SOFT_GRAY):
            ar = Arrow(a, b, buff=0.06, stroke_width=2.5)
            ar.set_color(col)
            return ar

        # ── 1. Build grid — 3 layers × 4 timesteps ─────────────────
        T   = 4
        SP  = 3.70
        X_OFF = 0.50
        HX = [-(T - 1) * SP / 2 + i * SP + X_OFF for i in range(T)]
        ZERO_X = HX[0] - 2.70

        # x nodes
        x_mobs = [x_node(np.array([HX[i], Y_X, 0]), t=i + 1) for i in range(T)]

        # hidden nodes: h_layers[l][t]
        h_layers = []
        for li in range(L):
            row = [h_node_deep(np.array([HX[ti], Y_LAYERS[li], 0]),
                               layer=li + 1, t=ti + 1) for ti in range(T)]
            h_layers.append(row)

        # y nodes
        y_mobs = [y_node(np.array([HX[i], Y_Y, 0]), t=i + 1) for i in range(T)]

        # Zero initializer nodes (a^(l)<0> = 0)
        z_nodes = [zero_node(np.array([ZERO_X, Y_LAYERS[li], 0]), layer=li + 1) for li in range(L)]
        z_arrs  = [mk_arr(z_nodes[li].get_right(), h_layers[li][0].get_left(), WA_COLS[li])
                   for li in range(L)]

        # ── Vertical arrows — per-layer Wx colors ──────────────────
        # x → layer 1
        wx1_arrs = [mk_arr(x_mobs[ti].get_top(), h_layers[0][ti].get_bottom(), WX_COLS[0])
                    for ti in range(T)]
        # layer l → layer l+1
        wx_inter = []
        for li in range(L - 1):
            arrs = [mk_arr(h_layers[li][ti].get_top(), h_layers[li + 1][ti].get_bottom(), WX_COLS[li + 1])
                    for ti in range(T)]
            wx_inter.append(arrs)
        # layer 3 → ŷ
        wy_arrs = [mk_arr(h_layers[L - 1][ti].get_top(), y_mobs[ti].get_bottom(), OUTPUT_GOLD)
                   for ti in range(T)]

        # ── Recurrent arrows — per-layer Wa colors ─────────────────
        wa_layers = []
        for li in range(L):
            arrs = [mk_arr(h_layers[li][ti].get_right(), h_layers[li][ti + 1].get_left(), WA_COLS[li])
                    for ti in range(T - 1)]
            wa_layers.append(arrs)

        # ── Weight labels — per-layer colors ────────────────────────
        wx_lbl_1 = Tex(r"W_x^{(1)}", font_size=42).set_color(WX_COLS[0])
        wx_lbl_1.next_to(wx1_arrs[1], RIGHT, buff=0.08)
        wx_lbl_2 = Tex(r"W_x^{(2)}", font_size=42).set_color(WX_COLS[1])
        wx_lbl_2.next_to(wx_inter[0][1], RIGHT, buff=0.08)
        wx_lbl_3 = Tex(r"W_x^{(3)}", font_size=42).set_color(WX_COLS[2])
        wx_lbl_3.next_to(wx_inter[1][1], RIGHT, buff=0.08)
        wx_lbls = VGroup(wx_lbl_1, wx_lbl_2, wx_lbl_3)

        wa_lbl_1 = Tex(r"W_a^{(1)}", font_size=42).set_color(WA_COLS[0])
        wa_lbl_1.next_to(wa_layers[0][0], DOWN, buff=0.10)
        wa_lbl_2 = Tex(r"W_a^{(2)}", font_size=42).set_color(WA_COLS[1])
        wa_lbl_2.next_to(wa_layers[1][0], DOWN, buff=0.10)
        wa_lbl_3 = Tex(r"W_a^{(3)}", font_size=42).set_color(WA_COLS[2])
        wa_lbl_3.next_to(wa_layers[2][0], DOWN, buff=0.10)
        wa_lbls = VGroup(wa_lbl_1, wa_lbl_2, wa_lbl_3)

        wy_lbl = Tex(r"W_y", font_size=42).set_color(OUTPUT_GOLD)
        wy_lbl.next_to(wy_arrs[1], RIGHT, buff=0.08)

        # ── 2. Start zoomed out ─────────────────────────────────────
        self.camera.frame.scale(1.65).shift(DOWN * 0.90)

        # ── Appearance animation — bottom up ────────────────────────
        # Zero init nodes
        self.play(LaggedStart(*[FadeIn(z) for z in z_nodes],
                              lag_ratio=0.15, run_time=0.5))
        # x nodes
        self.play(LaggedStart(*[FadeIn(m) for m in x_mobs],
                              lag_ratio=0.08, run_time=0.6))
        # Layer 1
        self.play(
            LaggedStart(*[GrowArrow(a) for a in [z_arrs[0]] + wx1_arrs],
                        lag_ratio=0.08, run_time=0.5),
            LaggedStart(*[FadeIn(h_layers[0][ti]) for ti in range(T)],
                        lag_ratio=0.08, run_time=0.5),
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in wa_layers[0]], lag_ratio=0.10, run_time=0.5),
        )
        # Layer 2
        self.play(
            LaggedStart(*[GrowArrow(a) for a in [z_arrs[1]] + wx_inter[0]],
                        lag_ratio=0.08, run_time=0.5),
            LaggedStart(*[FadeIn(h_layers[1][ti]) for ti in range(T)],
                        lag_ratio=0.08, run_time=0.5),
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in wa_layers[1]], lag_ratio=0.10, run_time=0.5),
        )
        # Layer 3
        self.play(
            LaggedStart(*[GrowArrow(a) for a in [z_arrs[2]] + wx_inter[1]],
                        lag_ratio=0.08, run_time=0.5),
            LaggedStart(*[FadeIn(h_layers[2][ti]) for ti in range(T)],
                        lag_ratio=0.08, run_time=0.5),
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in wa_layers[2]], lag_ratio=0.10, run_time=0.5),
        )
        # Output
        self.play(
            LaggedStart(*[GrowArrow(a) for a in wy_arrs], lag_ratio=0.10, run_time=0.5),
            LaggedStart(*[FadeIn(m) for m in y_mobs], lag_ratio=0.08, run_time=0.5),
        )
        # Labels
        self.play(FadeIn(wx_lbls), FadeIn(wa_lbls), FadeIn(wy_lbl), run_time=0.5)
        self.wait(0.5)

        self.wait(0.5)

        # ════════════════════════════════════════════════════════════
        #  4. Activation example: a^{(2)<2>}
        # ════════════════════════════════════════════════════════════
        target_node     = h_layers[1][1]   # a^{(2)<2>}
        prev_same_layer = h_layers[1][0]   # a^{(2)<1>}
        below_same_time = h_layers[0][1]   # a^{(1)<2>}
        wa_arrow = wa_layers[1][0]
        wx_arrow = wx_inter[0][1]

        self.play(Indicate(target_node, color=WHITE, scale_factor=1.30), run_time=0.6)
        self.play(
            Indicate(prev_same_layer, color=WA_COLS[1], scale_factor=1.25),
            Indicate(wa_arrow, color=WA_COLS[1], scale_factor=1.20),
            run_time=0.6,
        )
        self.play(
            Indicate(below_same_time, color=WX_COLS[1], scale_factor=1.25),
            Indicate(wx_arrow, color=WX_COLS[1], scale_factor=1.20),
            run_time=0.6,
        )
        self.wait(0.3)

        # ── Build activation equation ───────────────────────────────
        eq_lhs   = btex(r"a^{(2)\langle 2 \rangle}", col=HIDDEN_TEAL)
        eq_sep   = btex(r"= f(")
        eq_Wa    = btex(r"W_a^{(2)}", col=WA_COLS[1])
        eq_dot1  = btex(r"\cdot")
        eq_a21   = btex(r"a^{(2)\langle 1 \rangle}", col=WA_COLS[1])
        eq_plus  = btex(r"+")
        eq_Wx    = btex(r"W_x^{(2)}", col=WX_COLS[1])
        eq_dot2  = btex(r"\cdot")
        eq_a12   = btex(r"a^{(1)\langle 2 \rangle}", col=WX_COLS[1])
        eq_plus2 = btex(r"+")
        eq_ba    = btex(r"b_a^{(2)}", col=HIDDEN_TEAL)
        eq_rp    = btex(r")")

        row_eq = VGroup(eq_lhs, eq_sep, eq_Wa, eq_dot1, eq_a21,
                        eq_plus, eq_Wx, eq_dot2, eq_a12, eq_plus2, eq_ba, eq_rp)
        row_eq.arrange(RIGHT, buff=0.14).scale(1.50)
        pos_eq(row_eq)

        # Transform copies from diagram
        lhs_target = eq_lhs.get_center().copy()
        eq_lhs.move_to(target_node[1].get_center())

        wa_copy  = wa_lbl_2.copy()
        a21_copy = prev_same_layer[1].copy()
        wx_copy  = wx_lbl_2.copy()
        a12_copy = below_same_time[1].copy()

        self.play(eq_lhs.animate.move_to(lhs_target), run_time=0.8)
        self.play(
            FadeIn(eq_sep), FadeIn(eq_dot1),
            FadeIn(eq_plus), FadeIn(eq_dot2),
            FadeIn(eq_plus2), FadeIn(eq_rp),
            Transform(wa_copy, eq_Wa),
            Transform(a21_copy, eq_a21),
            Transform(wx_copy, eq_Wx),
            Transform(a12_copy, eq_a12),
            FadeIn(eq_ba),
            run_time=1.0,
        )
        self.wait(2.0)

        # Generalize: specific → general
        g_lhs   = btex(r"a^{(l)\langle t \rangle}", col=HIDDEN_TEAL)
        g_sep   = btex(r"= f(")
        g_Wa    = btex(r"W_a^{(l)}")
        g_dot1  = btex(r"\cdot")
        g_atm1  = btex(r"a^{(l)\langle t-1 \rangle}")
        g_plus  = btex(r"+")
        g_Wx    = btex(r"W_x^{(l)}")
        g_dot2  = btex(r"\cdot")
        g_alm1  = btex(r"a^{(l-1)\langle t \rangle}")
        g_plus2 = btex(r"+")
        g_ba    = btex(r"b_a^{(l)}", col=HIDDEN_TEAL)
        g_rp    = btex(r")")

        grow_eq = VGroup(g_lhs, g_sep, g_Wa, g_dot1, g_atm1,
                         g_plus, g_Wx, g_dot2, g_alm1, g_plus2, g_ba, g_rp)
        grow_eq.arrange(RIGHT, buff=0.14).scale(1.50)
        pos_eq(grow_eq)

        self.play(
            ReplacementTransform(row_eq, grow_eq),
            FadeOut(wa_copy), FadeOut(a21_copy),
            FadeOut(wx_copy), FadeOut(a12_copy),
            run_time=1.0,
        )
        self.wait(2.0)
        self.play(FadeOut(grow_eq), run_time=0.4)

        # ════════════════════════════════════════════════════════════
        #  5. Output example: ŷ^<2> with Transform from diagram
        # ════════════════════════════════════════════════════════════
        out_target = y_mobs[1]          # ŷ^<2>
        out_h_in   = h_layers[2][1]     # a^{(3)<2>}
        out_wy_arr = wy_arrs[1]

        self.play(Indicate(out_target, color=WHITE, scale_factor=1.30), run_time=0.6)
        self.play(
            Indicate(out_h_in, color=HIDDEN_TEAL, scale_factor=1.25),
            Indicate(out_wy_arr, color=OUTPUT_GOLD, scale_factor=1.20),
            run_time=0.6,
        )
        self.wait(0.3)

        oy_lhs  = btex(r"\hat{y}^{\langle 2 \rangle}", col=OUTPUT_GOLD)
        oy_sep  = btex(r"= g(")
        oy_Wy   = btex(r"W_y", col=OUTPUT_GOLD)
        oy_dot  = btex(r"\cdot")
        oy_aL   = btex(r"a^{(3)\langle 2 \rangle}", col=HIDDEN_TEAL)
        oy_plus = btex(r"+")
        oy_by   = btex(r"b_y", col=OUTPUT_GOLD)
        oy_rp   = btex(r")")

        out_row = VGroup(oy_lhs, oy_sep, oy_Wy, oy_dot, oy_aL, oy_plus, oy_by, oy_rp)
        out_row.arrange(RIGHT, buff=0.14).scale(1.50)
        pos_eq(out_row)

        # Transform copies from diagram
        lhs_tgt2 = oy_lhs.get_center().copy()
        oy_lhs.move_to(out_target[1].get_center())

        wy_copy = wy_lbl.copy()
        aL_copy = out_h_in[1].copy()

        self.play(oy_lhs.animate.move_to(lhs_tgt2), run_time=0.8)
        self.play(
            FadeIn(oy_sep), FadeIn(oy_dot),
            FadeIn(oy_plus), FadeIn(oy_rp),
            Transform(wy_copy, oy_Wy),
            Transform(aL_copy, oy_aL),
            FadeIn(oy_by),
            run_time=1.0,
        )
        self.wait(2.0)

        # Generalize output
        go_lhs  = btex(r"\hat{y}^{\langle t \rangle}", col=OUTPUT_GOLD)
        go_sep  = btex(r"= g(")
        go_Wy   = btex(r"W_y", col=OUTPUT_GOLD)
        go_dot  = btex(r"\cdot")
        go_aL   = btex(r"a^{(L)\langle t \rangle}", col=HIDDEN_TEAL)
        go_plus = btex(r"+")
        go_by   = btex(r"b_y", col=OUTPUT_GOLD)
        go_rp   = btex(r")")

        gout_eq = VGroup(go_lhs, go_sep, go_Wy, go_dot, go_aL, go_plus, go_by, go_rp)
        gout_eq.arrange(RIGHT, buff=0.14).scale(1.50)
        pos_eq(gout_eq)

        self.play(
            ReplacementTransform(out_row, gout_eq),
            FadeOut(wy_copy), FadeOut(aL_copy),
            run_time=1.0,
        )
        self.wait(2.0)

        validate_layout(self, label="DeepRNN", camera_scale=1.65)

class BidirectionalRNN(InteractiveScene):
    def construct(self):
        HIDDEN_TEAL = "#1ABC9C"
        OUTPUT_GOLD = "#F1C40F"
        SOFT_GRAY   = "#AAAAAA"
        PURPLE_A    = "#9B59B6"
        PURPLE_B    = "#A855F7"
        FWD_GREEN   = "#2ECC71"
        BWD_ORANGE  = "#E67E22"
        INPUT_BLUE  = "#2980B9"
        WF_COL      = "#FF1493"
        WB_COL      = "#9B59B6"
        WY_COL      = OUTPUT_GOLD

        EQ_Y  = -12.40
        EQ_FS = 44

        def btex(s, col=WHITE, fs=EQ_FS):
            t = Tex(s, font_size=fs); t.set_color(col); return t

        def pos_eq(eq, y=EQ_Y):
            eq.move_to(np.array([0, y, 0])); return eq

        R = 0.70; CR = 0.12; SW = 2.8; SQ_SC = 1.50; NODE_W = 1.50

        WORDS = ["The", "bank", "of", "the", "river"]
        T = len(WORDS)

        Y_X  = -6.40
        Y_H  = -1.60
        Y_Y  =  4.00

        SP = 5.50
        HX = [-(T - 1) * SP / 2 + i * SP for i in range(T)]
        ZERO_X_L = HX[0]  - 5.60
        ZERO_X_R = HX[-1] + 5.60
        ARR_V = 1.05  # vertical offset for fwd/bwd lanes in combined box (= COMB_H*SQ_SC/4)

        def _sq(pos, col, w=None, h=None):
            s = RoundedRectangle(width=(w or NODE_W) * SQ_SC,
                                 height=(h or R * 2) * SQ_SC, corner_radius=CR)
            s.set_fill(col, opacity=0.92); s.set_stroke(WHITE, width=SW)
            s.move_to(pos); return s

        def word_node(pos, word, t):
            lb = Text(word, font_size=48, color=WHITE); lb.scale(2.5)
            tw = max(NODE_W, lb.get_width() / SQ_SC + 0.60)
            sq = _sq(pos, INPUT_BLUE, w=tw); lb.move_to(pos)
            sub = Tex(r"x^{\langle " + str(t) + r"\rangle}", font_size=72)
            sub.set_color(WHITE); sub.set_stroke(WHITE, width=0.8)
            sub.scale(1.9); sub.next_to(sq, DOWN, buff=0.75)
            return VGroup(sq, lb, sub)

        def fwd_only_node(pos, t):
            sq = _sq(pos, HIDDEN_TEAL)
            lstr = r"a^{\langle " + str(t) + r"\rangle}"
            lb = Tex(lstr, font_size=42)
            lb.set_color(BLACK); lb.set_stroke(BLACK, width=1.4)
            lb.scale(1.9 * 1.3); lb.move_to(pos)
            return VGroup(sq, lb)

        COMB_H = R * 4.0

        def combined_node(pos, t):
            sq = _sq(pos, HIDDEN_TEAL, h=COMB_H)
            qh = COMB_H * SQ_SC / 4  # center of upper/lower half
            fwd_lb = Tex(r"\overrightarrow{a}^{\langle " + str(t) + r"\rangle}",
                         font_size=48)
            fwd_lb.set_color(BLACK); fwd_lb.set_stroke(BLACK, width=1.4)
            fwd_lb.scale(1.8); fwd_lb.move_to(pos + UP * qh)
            bwd_lb = Tex(r"\overleftarrow{a}^{\langle " + str(t) + r"\rangle}",
                         font_size=48)
            bwd_lb.set_color(BLACK); bwd_lb.set_stroke(BLACK, width=1.4)
            bwd_lb.scale(1.8); bwd_lb.move_to(pos + DOWN * qh)
            hw = NODE_W * SQ_SC / 2 - 0.12
            div = Line(pos + LEFT * hw, pos + RIGHT * hw,
                       stroke_width=2.0, color=WHITE)
            div.set_opacity(0.35)
            return VGroup(sq, fwd_lb, bwd_lb, div)

        def y_node(pos, t):
            sq = _sq(pos, OUTPUT_GOLD)
            lstr = r"\hat{y}^{\langle " + str(t) + r"\rangle}"
            lb = Tex(lstr, font_size=50)
            lb.set_color(BLACK); lb.set_stroke(BLACK, width=1.2)
            lb.scale(2.1); lb.move_to(pos)
            return VGroup(sq, lb)

        def zero_circle(pos, lstr):
            circ = Circle(radius=1.20 * 1.1)
            circ.set_fill(PURPLE_A, opacity=0.88)
            circ.set_stroke(WHITE, width=2.5); circ.move_to(pos)
            lb = Tex(lstr, font_size=60)
            lb.set_color(BLACK); lb.set_stroke(BLACK, width=1.2)
            lb.scale(1.8); lb.move_to(pos)
            zl = Text("zero", font_size=50, color=PURPLE_A, weight="BOLD")
            zl.scale(1.5); zl.next_to(circ, DOWN, buff=0.49)
            return VGroup(circ, lb, zl)

        def mk_arr(a, b, col=SOFT_GRAY):
            ar = Arrow(a, b, buff=0.06, stroke_width=2.8)
            ar.set_color(col); return ar

        # ── Build nodes ──────────────────────────────────────────────
        x_mobs = [word_node(np.array([HX[i], Y_X, 0]), WORDS[i], i + 1)
                  for i in range(T)]
        fwd_only_mobs = [fwd_only_node(np.array([HX[i], Y_H, 0]), i + 1)
                         for i in range(T)]
        combined_mobs = [combined_node(np.array([HX[i], Y_H, 0]), i + 1)
                         for i in range(T)]
        y_mobs = [y_node(np.array([HX[i], Y_Y, 0]), i + 1)
                  for i in range(T)]

        # Zero circles at their respective lanes (fwd=top, bwd=bottom)
        z_fwd_only = zero_circle(np.array([ZERO_X_L, Y_H, 0]),
                                  r"a^{\langle 0\rangle}")
        z_fwd = zero_circle(np.array([ZERO_X_L, Y_H + ARR_V, 0]),
                             r"\overrightarrow{a}^{\langle 0\rangle}")
        z_bwd = zero_circle(np.array([ZERO_X_R, Y_H - ARR_V, 0]),
                             r"\overleftarrow{a}^{\langle " + str(T + 1) + r"\rangle}")

        # ── Forward-only arrows ──────────────────────────────────────
        # Perfectly horizontal arrow from zero circle to first fwd node
        z_fo_arr = mk_arr(
            np.array([z_fwd_only[0].get_right()[0], Y_H, 0]),
            np.array([fwd_only_mobs[0][0].get_left()[0], Y_H, 0]),
            WF_COL)
        wx_fo_arrs = [mk_arr(x_mobs[i][0].get_top(), fwd_only_mobs[i].get_bottom(), SOFT_GRAY)
                      for i in range(T)]
        wa_fo_arrs = [mk_arr(fwd_only_mobs[i].get_right(), fwd_only_mobs[i + 1].get_left(), WF_COL)
                      for i in range(T - 1)]
        wy_fo_arrs = [mk_arr(fwd_only_mobs[i].get_top(), y_mobs[i].get_bottom(), WY_COL)
                      for i in range(T)]

        # ── Combined arrows — zero circles at their lanes ────────────
        # Forward zero → first box (perfectly horizontal at fwd lane Y)
        fwd_lane_y = Y_H + ARR_V
        z_fwd_arr = mk_arr(
            np.array([z_fwd[0].get_right()[0], fwd_lane_y, 0]),
            np.array([combined_mobs[0][0].get_left()[0], fwd_lane_y, 0]),
            WF_COL)
        # Backward zero → last box (perfectly horizontal at bwd lane Y)
        bwd_lane_y = Y_H - ARR_V
        z_bwd_arr = mk_arr(
            np.array([z_bwd[0].get_left()[0], bwd_lane_y, 0]),
            np.array([combined_mobs[-1][0].get_right()[0], bwd_lane_y, 0]),
            WB_COL)
        wx_c_arrs = [mk_arr(x_mobs[i][0].get_top(), combined_mobs[i].get_bottom(), SOFT_GRAY)
                     for i in range(T)]
        wa_fwd_arrs = [mk_arr(combined_mobs[i].get_right() + UP * ARR_V,
                               combined_mobs[i + 1].get_left() + UP * ARR_V, WF_COL)
                       for i in range(T - 1)]
        wa_bwd_arrs = [mk_arr(combined_mobs[i + 1].get_left() + DOWN * ARR_V,
                               combined_mobs[i].get_right() + DOWN * ARR_V, WB_COL)
                       for i in range(T - 1)]
        wy_c_arrs = [mk_arr(combined_mobs[i].get_top(), y_mobs[i].get_bottom(), WY_COL)
                     for i in range(T)]

        # ── Camera ───────────────────────────────────────────────────
        self.camera.frame.scale(2.90).shift(DOWN * 2.00)

        # ══════════════════════════════════════════════════════════════
        #  PHASE 1: Forward-only RNN
        # ══════════════════════════════════════════════════════════════
        self.play(FadeIn(z_fwd_only), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(m) for m in x_mobs],
                              lag_ratio=0.06, run_time=0.8))
        self.play(
            GrowArrow(z_fo_arr),
            LaggedStart(*[GrowArrow(a) for a in wx_fo_arrs],
                        lag_ratio=0.06, run_time=0.6),
            LaggedStart(*[FadeIn(n) for n in fwd_only_mobs],
                        lag_ratio=0.06, run_time=0.6),
        )
        self.play(LaggedStart(*[GrowArrow(a) for a in wa_fo_arrs],
                              lag_ratio=0.08, run_time=0.6))
        self.play(
            LaggedStart(*[GrowArrow(a) for a in wy_fo_arrs],
                        lag_ratio=0.06, run_time=0.6),
            LaggedStart(*[FadeIn(m) for m in y_mobs],
                        lag_ratio=0.06, run_time=0.6),
        )
        self.wait(1.8)


        # ══════════════════════════════════════════════════════════════
        #  PHASE 2: WHY forward-only fails — "bank" is ambiguous
        # ══════════════════════════════════════════════════════════════
        bank_idx = 1

        self.play(Indicate(x_mobs[bank_idx], color=YELLOW, scale_factor=1.30),
                  run_time=0.7)

        for i in range(bank_idx + 1):
            self.play(Indicate(fwd_only_mobs[i], color=FWD_GREEN,
                               scale_factor=1.15), run_time=0.30)

        # Dim future — forward can't see "of the river"
        future_mobs = []
        for i in range(bank_idx + 1, T):
            future_mobs.extend([x_mobs[i], fwd_only_mobs[i], y_mobs[i],
                                wx_fo_arrs[i], wy_fo_arrs[i]])
            if i < T - 1:
                future_mobs.append(wa_fo_arrs[i])
        if bank_idx < T - 1:
            future_mobs.append(wa_fo_arrs[bank_idx])
        self.play(*[m.animate.set_opacity(0.15) for m in future_mobs],
                  run_time=0.6)

        # "?" above output
        q_mark = Tex(r"?", font_size=100).set_color(YELLOW).scale(1.5)
        q_mark.next_to(y_mobs[bank_idx], UP, buff=0.40)
        self.play(FadeIn(q_mark, scale=1.5), run_time=0.5)

        # Two meanings — shifted right
        meaning1 = Text('"The bank of the river"', font_size=38, color=FWD_GREEN, weight=BOLD)
        meaning1.scale(1.8)
        meaning1.move_to(np.array([HX[2], Y_Y + 3.5, 0])).shift(RIGHT*3.6+UP*0.2)

        meaning2 = Text('"The bank gave me a loan"', font_size=38, color=RED, weight=BOLD)
        meaning2.scale(1.8)
        meaning2.next_to(meaning1, DOWN, buff=0.70)

        self.play(FadeIn(meaning1), run_time=0.4)
        self.play(FadeIn(meaning2), run_time=0.4)

        # "only past context →" — far below, long arrow
        past_lbl = Text("Only past context", font_size=50, color=FWD_GREEN,
                         weight="BOLD")
        past_lbl.scale(2.0)
        past_lbl.move_to(np.array([0, Y_X - 4.5, 0])).shift(DOWN*0.85)
        past_arr = Arrow(np.array([HX[0] - 1.0, Y_X - 3.99, 0]),
                         np.array([HX[-1] + 1.0, Y_X - 3.99, 0]),
                         buff=0, stroke_width=5, color=FWD_GREEN)
        self.play(FadeIn(past_lbl), GrowArrow(past_arr), run_time=0.6)

        self.wait(3.0)


        # Clean up
        self.play(*[m.animate.set_opacity(1.0) for m in future_mobs],
                  FadeOut(past_lbl), FadeOut(past_arr),
                  FadeOut(meaning1), FadeOut(meaning2),
                  run_time=0.4)
        self.wait(0.3)

        # ══════════════════════════════════════════════════════════════
        #  PHASE 3: Transition to bidirectional
        # ══════════════════════════════════════════════════════════════
        fo_stuff = VGroup(z_fwd_only, z_fo_arr,
                          *fwd_only_mobs, *wx_fo_arrs, *wa_fo_arrs, *wy_fo_arrs)
        self.play(FadeOut(fo_stuff), FadeOut(q_mark), run_time=0.5)

        self.play(FadeIn(z_fwd), FadeIn(z_bwd), run_time=0.4)
        self.play(
            GrowArrow(z_fwd_arr),
            LaggedStart(*[GrowArrow(a) for a in wx_c_arrs],
                        lag_ratio=0.04, run_time=0.5),
            LaggedStart(*[FadeIn(n) for n in combined_mobs],
                        lag_ratio=0.04, run_time=0.5),
        )
        self.play(LaggedStart(*[GrowArrow(a) for a in wa_fwd_arrs],
                              lag_ratio=0.06, run_time=0.5))
        self.play(
            GrowArrow(z_bwd_arr),
            LaggedStart(*[GrowArrow(a) for a in wa_bwd_arrs],
                        lag_ratio=0.06, run_time=0.5),
        )
        self.play(LaggedStart(*[GrowArrow(a) for a in wy_c_arrs],
                              lag_ratio=0.04, run_time=0.5))
        self.wait(1.5)

        # Context labels — well clear of diagram
        fwd_lbl = Text("Past context", font_size=50, color=FWD_GREEN,
                        weight="BOLD")
        fwd_lbl.scale(2.0)
        fwd_lbl.move_to(np.array([0, Y_X - 5.23, 0]))
        fwd_arr_lbl = Arrow(np.array([HX[0] - 1.0, Y_X - 3.99, 0]),
                            np.array([HX[-1] + 1.0, Y_X - 3.99, 0]),
                            buff=0, stroke_width=5, color=FWD_GREEN)

        bwd_lbl = Text("Future context", font_size=50, color=BWD_ORANGE,
                         weight="BOLD")
        bwd_lbl.scale(2.0)
        bwd_lbl.move_to(np.array([0, Y_Y + 2.7, 0]))
        bwd_arr_lbl = Arrow(np.array([HX[-1] + 1.0, Y_Y + 3.99, 0]),
                            np.array([HX[0] - 1.0, Y_Y + 3.99, 0]),
                            buff=0, stroke_width=5, color=BWD_ORANGE)

        self.play(FadeIn(fwd_lbl), GrowArrow(fwd_arr_lbl), run_time=0.4)
        self.play(FadeIn(bwd_lbl), GrowArrow(bwd_arr_lbl), run_time=0.4)

        # Forward path to "bank"
        for i in range(bank_idx + 1):
            self.play(Indicate(combined_mobs[i], color=FWD_GREEN,
                               scale_factor=1.10), run_time=0.18)
        # Backward path from "river" to "bank"
        for i in range(T - 1, bank_idx - 1, -1):
            self.play(Indicate(combined_mobs[i], color=BWD_ORANGE,
                               scale_factor=1.10), run_time=0.18)

        self.play(Indicate(y_mobs[bank_idx], color=WHITE, scale_factor=1.25),
                  run_time=0.5)
        self.wait(1.5)

        self.play(FadeOut(fwd_lbl), FadeOut(fwd_arr_lbl),
                  FadeOut(bwd_lbl), FadeOut(bwd_arr_lbl), run_time=0.4)
        self.wait(1.0)

        # ══════════════════════════════════════════════════════════════
        #  PHASE 4: Output equation — expanded
        # ══════════════════════════════════════════════════════════════
        eq_t = 1
        self.play(Indicate(y_mobs[eq_t], color=WHITE, scale_factor=1.25),
                  run_time=0.5)
        self.play(
            Indicate(combined_mobs[eq_t][1], color=FWD_GREEN, scale_factor=1.25),
            Indicate(combined_mobs[eq_t][2], color=BWD_ORANGE, scale_factor=1.25),
            run_time=0.5,
        )

        oy_lhs  = btex(r"\hat{y}^{\langle 2 \rangle}", col=OUTPUT_GOLD).scale(1.89)
        oy_sep  = btex(r"= g(").scale(1.89)
        oy_Wy1  = btex(r"W_y^{\rightarrow}", col=WY_COL).scale(1.89)
        oy_dot1 = btex(r"\cdot").scale(1.89)
        oy_af   = btex(r"\overrightarrow{a}^{\langle 2 \rangle}", col=FWD_GREEN).scale(1.89)
        oy_plus = btex(r"+").scale(1.89)
        oy_Wy2  = btex(r"W_y^{\leftarrow}", col=WY_COL).scale(1.89)
        oy_dot2 = btex(r"\cdot").scale(1.89)
        oy_ab   = btex(r"\overleftarrow{a}^{\langle 2 \rangle}", col=BWD_ORANGE).scale(1.89)
        oy_pl2  = btex(r"+").scale(1.89)
        oy_by   = btex(r"b_y", col=OUTPUT_GOLD).scale(1.89)
        oy_rp   = btex(r")").scale(1.89)

        out_eq = VGroup(oy_lhs, oy_sep, oy_Wy1, oy_dot1, oy_af,
                        oy_plus, oy_Wy2, oy_dot2, oy_ab,
                        oy_pl2, oy_by, oy_rp)
        out_eq.arrange(RIGHT, buff=0.12).scale(1.89)
        pos_eq(out_eq)

        lhs_tgt = oy_lhs.get_center().copy()
        oy_lhs.move_to(y_mobs[eq_t][1].get_center())
        af_copy = combined_mobs[eq_t][1].copy()
        ab_copy = combined_mobs[eq_t][2].copy()

        self.play(oy_lhs.animate.move_to(lhs_tgt), self.camera.frame.animate.shift(DOWN*2) ,run_time=0.7)
        self.play(
            FadeIn(oy_sep), FadeIn(oy_dot1), FadeIn(oy_plus),
            FadeIn(oy_dot2), FadeIn(oy_pl2), FadeIn(oy_rp),
            FadeIn(oy_Wy1), FadeIn(oy_Wy2),
            Transform(af_copy, oy_af),
            Transform(ab_copy, oy_ab),
            FadeIn(oy_by),
            run_time=0.9,
        )
        self.wait(2.0)


        go_lhs  = btex(r"\hat{y}^{\langle t \rangle}", col=OUTPUT_GOLD).scale(1.89)
        go_sep  = btex(r"= g(").scale(1.89)
        go_Wy1  = btex(r"W_y^{\rightarrow}", col=WY_COL).scale(1.89)
        go_dot1 = btex(r"\cdot").scale(1.89)
        go_af   = btex(r"\overrightarrow{a}^{\langle t \rangle}", col=FWD_GREEN).scale(1.89)
        go_plus = btex(r"+").scale(1.89)
        go_Wy2  = btex(r"W_y^{\leftarrow}", col=WY_COL).scale(1.89)
        go_dot2 = btex(r"\cdot").scale(1.89)
        go_ab   = btex(r"\overleftarrow{a}^{\langle t \rangle}", col=BWD_ORANGE).scale(1.89)
        go_pl2  = btex(r"+").scale(1.89)
        go_by   = btex(r"b_y", col=OUTPUT_GOLD).scale(1.89)
        go_rp   = btex(r")").scale(1.89)

        gout = VGroup(go_lhs, go_sep, go_Wy1, go_dot1, go_af,
                      go_plus, go_Wy2, go_dot2, go_ab,
                      go_pl2, go_by, go_rp)
        gout.arrange(RIGHT, buff=0.12).scale(1.89)
        pos_eq(gout)

        self.play(
            ReplacementTransform(out_eq, gout),
            FadeOut(af_copy), FadeOut(ab_copy),
            run_time=0.9,
        )
        self.wait(2.0)
        self.play(FadeOut(gout), run_time=0.4)


        # ══════════════════════════════════════════════════════════════
        #  PHASE 5: Forward activation equation
        # ══════════════════════════════════════════════════════════════
        self.play(Indicate(combined_mobs[eq_t], color=WHITE, scale_factor=1.25),
                  run_time=0.5)

        ef_lhs  = btex(r"\overrightarrow{a}^{\langle 2 \rangle}", col=FWD_GREEN).scale(1.89)
        ef_sep  = btex(r"= f(").scale(1.89)
        ef_Wa   = btex(r"W_{\overrightarrow{a}}", col=WF_COL).scale(1.89)
        ef_dot1 = btex(r"\cdot").scale(1.89)
        ef_at   = btex(r"\overrightarrow{a}^{\langle 1 \rangle}", col=WF_COL).scale(1.89)
        ef_plus = btex(r"+").scale(1.89)
        ef_Wx   = btex(r"W_{\overrightarrow{x}}", col=INPUT_BLUE).scale(1.89)
        ef_dot2 = btex(r"\cdot").scale(1.89)
        ef_xt   = btex(r"x^{\langle 2 \rangle}", col=INPUT_BLUE).scale(1.89)
        ef_pl2  = btex(r"+").scale(1.89)
        ef_ba   = btex(r"b_{\overrightarrow{a}}", col=FWD_GREEN).scale(1.89)
        ef_rp   = btex(r")").scale(1.89)

        fwd_eq = VGroup(ef_lhs, ef_sep, ef_Wa, ef_dot1, ef_at,
                        ef_plus, ef_Wx, ef_dot2, ef_xt,
                        ef_pl2, ef_ba, ef_rp)
        fwd_eq.arrange(RIGHT, buff=0.12).scale(1.89)
        pos_eq(fwd_eq)

        self.play(Write(fwd_eq), run_time=1.0)
        self.wait(2.0)

        gf_lhs  = btex(r"\overrightarrow{a}^{\langle t \rangle}", col=FWD_GREEN).scale(1.89)
        gf_sep  = btex(r"= f(").scale(1.89)
        gf_Wa   = btex(r"W_{\overrightarrow{a}}", col=WF_COL).scale(1.89)
        gf_dot1 = btex(r"\cdot").scale(1.89)
        gf_at   = btex(r"\overrightarrow{a}^{\langle t-1 \rangle}").scale(1.89)
        gf_plus = btex(r"+").scale(1.89)
        gf_Wx   = btex(r"W_{\overrightarrow{x}}", col=INPUT_BLUE).scale(1.89)
        gf_dot2 = btex(r"\cdot").scale(1.89)
        gf_xt   = btex(r"x^{\langle t \rangle}").scale(1.89)
        gf_pl2  = btex(r"+").scale(1.89)
        gf_ba   = btex(r"b_{\overrightarrow{a}}", col=FWD_GREEN).scale(1.89)
        gf_rp   = btex(r")").scale(1.89)

        gfwd = VGroup(gf_lhs, gf_sep, gf_Wa, gf_dot1, gf_at,
                      gf_plus, gf_Wx, gf_dot2, gf_xt,
                      gf_pl2, gf_ba, gf_rp)
        gfwd.arrange(RIGHT, buff=0.12).scale(1.89)
        pos_eq(gfwd)

        self.play(ReplacementTransform(fwd_eq, gfwd), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(gfwd), run_time=0.4)

        # ══════════════════════════════════════════════════════════════
        #  PHASE 6: Limitations of RNNs — text only
        # ══════════════════════════════════════════════════════════════
        # Fade out everything
        all_bidir = VGroup(
            *x_mobs, *combined_mobs, *y_mobs,
            z_fwd, z_bwd, z_fwd_arr, z_bwd_arr,
            *wx_c_arrs, *wa_fwd_arrs, *wa_bwd_arrs, *wy_c_arrs,
        )
        self.play(FadeOut(all_bidir), run_time=0.6)
        self.wait(0.5)

        lim_title = Text("Limitations of RNNs", font_size=65, color=YELLOW,
                          weight="BOLD")
        lim_title.scale(2.2)
        lim_title.move_to(np.array([0, Y_Y + 1.0, 0]))

        lim_data = [
            ("Vanishing / exploding gradients in long sequences", "#E74C3C"),
            ("Slow sequential training — cannot parallelise across timesteps", BWD_ORANGE),
            ("Struggle to capture very long-range dependencies", "#E74C3C"),
            ("Bidirectional RNNs cannot be used for real-time prediction", BWD_ORANGE),
        ]
        lim_groups = []
        for i, (txt, col) in enumerate(lim_data):
            lt = Text(txt, font_size=40, color=WHITE, weight="BOLD")
            lt.scale(1.8)
            yp = Y_H + 2.0 - i * 2.8
            lt.move_to(np.array([0, yp, 0]))
            bg = RoundedRectangle(
                width=lt.get_width() + 1.2,
                height=lt.get_height() + 0.6,
                corner_radius=0.15,
            )
            bg.set_fill(col, opacity=0.18)
            bg.set_stroke(col, width=2.0, opacity=0.6)
            bg.move_to(lt.get_center())
            grp = VGroup(bg, lt)
            lim_groups.append(grp)

        self.play(FadeIn(lim_title), run_time=0.5)
        for lg in lim_groups:
            self.play(FadeIn(lg, shift=RIGHT * 0.5), run_time=0.5)
            self.wait(0.8)
        self.wait(2.0)

        self.play(FadeOut(lim_title), *[FadeOut(g) for g in lim_groups],
                  run_time=0.5)
        self.wait(1.0)
        validate_layout(self, label="BidirectionalRNN", camera_scale=2.90)

        self.wait(2)

class VanishingGradients(InteractiveScene):
    def construct(self):

        self.camera.frame.scale(0.79).shift(LEFT*0.63+UP*0.3)

        HIDDEN_TEAL  = "#1ABC9C"
        PURPLE_B     = "#A855F7"
        LOSS_RED     = "#FF4444"
        GRAD_GREEN   = "#2ECC71"
        EXPLODE_RED  = "#FF1A1A"
        RNN_PINK     = "#FF1493"
        OUTPUT_GOLD  = "#F1C40F"
        ANN_BLUE     = "#2980B9"
        VANISH_GRAY  = "#888888"
        SOFT_GRAY    = "#AAAAAA"
        WORD_COL     = "#CCCCCC"

        R = 0.42; CR = 0.10; SW = 2.5; SQ_SC = 1.28
        T = 6; SP = 2.60
        Y_X  = -3.20   # x labels row
        Y_H  = -1.50   # hidden state row
        Y_Y  =  0.20   # y hat labels row
        Y_L  =  1.45   # individual loss nodes (one per timestep)
        Y_WD = -4.10   # sentence example row

        HX = [-(T - 1) * SP / 2 + i * SP for i in range(T)]

        def _sq(pos, col, opacity=0.92):
            s = RoundedRectangle(width=R * 2 * SQ_SC, height=R * 2 * SQ_SC, corner_radius=CR)
            s.set_fill(col, opacity=opacity); s.set_stroke(WHITE, width=SW)
            s.move_to(pos); return s

        def h_node(pos, t, col=HIDDEN_TEAL):
            sq = _sq(pos, col)
            lb = Tex(r"a^{\langle " + str(t) + r"\rangle}", font_size=28)
            lb.set_color(BLACK); lb.set_stroke(BLACK, width=0.8)
            lb.scale(1.5); lb.move_to(pos)
            return VGroup(sq, lb)

        def x_label(pos, t):
            lb = Tex(r"x^{\langle " + str(t) + r"\rangle}", font_size=32)
            lb.set_color(ANN_BLUE); lb.scale(1.77); lb.move_to(pos)
            return lb

        def y_label(pos, t):
            lb = Tex(r"\hat{y}^{\langle " + str(t) + r"\rangle}", font_size=32)
            lb.set_color(OUTPUT_GOLD); lb.scale(1.77); lb.move_to(pos)
            return lb

        def l_node(pos, t):
            sq = RoundedRectangle(width=R * 2.0 * SQ_SC, height=R * 1.2 * SQ_SC, corner_radius=CR)
            sq.set_fill(LOSS_RED, opacity=0.85); sq.set_stroke(WHITE, width=SW * 0.85)
            sq.move_to(pos)
            lb = Tex(r"\mathcal{L}^{(" + str(t) + r")}", font_size=32)
            lb.set_color(WHITE); lb.scale(1.2); lb.move_to(pos)
            return VGroup(sq, lb)

        def zero_circ(pos, lstr):
            circ = Circle(radius=R * SQ_SC * 0.75)
            circ.set_fill(PURPLE_B, opacity=0.90); circ.set_stroke(WHITE, width=SW)
            circ.move_to(pos)
            lb = Tex(lstr, font_size=24); lb.set_color(BLACK); lb.scale(1.53); lb.move_to(pos)
            return VGroup(circ, lb)

        def mk_arr(a, b, col=SOFT_GRAY, sw=2.5):
            ar = Arrow(a, b, buff=0.06, stroke_width=sw)
            ar.set_color(col); return ar

        def grad_pill(val_str, pos, col):
            bg = RoundedRectangle(width=1.60, height=0.52, corner_radius=0.10)
            bg.set_fill(col, opacity=0.22); bg.set_stroke(col, width=2.0)
            bg.move_to(pos)
            tx = Text(val_str, font_size=20, color=col, weight="BOLD"); tx.move_to(pos)
            return VGroup(bg, tx)

        # ── Build diagram ─────────────────────────────────────────────
        x_mobs    = [x_label(np.array([HX[i], Y_X, 0]), i + 1) for i in range(T)]
        h_mobs    = [h_node(np.array([HX[i], Y_H, 0]), i + 1) for i in range(T)]
        y_mobs    = [y_label(np.array([HX[i], Y_Y, 0]), i + 1) for i in range(T)]
        loss_mobs = [l_node(np.array([HX[i], Y_L,  0]), i + 1) for i in range(T)]

        a0 = zero_circ(np.array([HX[0] - SP, Y_H, 0]), r"a^{\langle 0\rangle}")

        # ── Sentence example ─────────────────────────────────────────
        words     = ["I", "grew", "up", "in", "France", "I speak..."]
        word_mobs = []
        for i, w in enumerate(words):
            wt = Text(w, font_size=26, color=WORD_COL, weight="BOLD")
            wt.scale(1.3)
            wt.move_to(np.array([HX[i], Y_WD, 0]))
            word_mobs.append(wt)

        sep_y = (Y_WD + Y_X) / 2 + 0.05
        sep_line = Line(
            np.array([HX[0] - SP * 0.50, sep_y, 0]),
            np.array([HX[-1] + SP * 0.50, sep_y, 0]),
            stroke_width=1.0, color=SOFT_GRAY,
        )
        sep_line.set_opacity(0.35)

        wx_arrs   = [mk_arr(x_mobs[i].get_top(),    h_mobs[i].get_bottom(),    ANN_BLUE)
                     for i in range(T)]
        wy_arrs   = [mk_arr(h_mobs[i].get_top(),    y_mobs[i].get_bottom(),    OUTPUT_GOLD)
                     for i in range(T)]
        loss_arrs = [mk_arr(y_mobs[i].get_top(),    loss_mobs[i].get_bottom(), LOSS_RED)
                     for i in range(T)]
        wh_arrs   = [mk_arr(h_mobs[i].get_right(),  h_mobs[i+1].get_left(),   RNN_PINK)
                     for i in range(T - 1)]
        a0_arr    = mk_arr(a0.get_right(), h_mobs[0].get_left(), RNN_PINK)

        # gradient lane sits above the loss node row
        lane_y = Y_L + 1.30   # = 2.75 absolute
        GRAD_START_X = HX[-1] + SP * 0.55

        self.camera.frame.scale(1.70).shift(DOWN * 0.75)

        # ── Phase 1: Build diagram ────────────────────────────────────
        self.play(LaggedStart(*[FadeIn(m) for m in word_mobs], lag_ratio=0.08, run_time=0.60))
        self.play(FadeIn(sep_line), run_time=0.25)
        self.play(FadeIn(a0), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(m) for m in x_mobs], lag_ratio=0.06, run_time=0.5))
        self.play(
            GrowArrow(a0_arr),
            LaggedStart(*[GrowArrow(a) for a in wx_arrs], lag_ratio=0.06, run_time=0.5),
            LaggedStart(*[FadeIn(n) for n in h_mobs],     lag_ratio=0.06, run_time=0.5),
        )
        self.play(LaggedStart(*[GrowArrow(a) for a in wh_arrs], lag_ratio=0.08, run_time=0.5))
        self.play(
            LaggedStart(*[GrowArrow(a) for a in wy_arrs],  lag_ratio=0.06, run_time=0.5),
            LaggedStart(*[FadeIn(m) for m in y_mobs],      lag_ratio=0.06, run_time=0.5),
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in loss_arrs], lag_ratio=0.06, run_time=0.5),
            LaggedStart(*[FadeIn(m) for m in loss_mobs],    lag_ratio=0.06, run_time=0.5),
        )
        self.wait(0.5)

        # Forward flash
        for i in range(T):
            self.play(Indicate(h_mobs[i], color=RNN_PINK, scale_factor=1.14), run_time=0.09)
        for i in range(T):
            self.play(Indicate(loss_mobs[i], color=LOSS_RED, scale_factor=1.16), run_time=0.09)
        self.wait(0.6)

        # ── Phase 2: Vanishing ────────────────────────────────────────
        v_vals   = ["1.00", "0.25", "0.06", "0.02", "0.00", "~0"]
        v_cols   = [GRAD_GREEN, "#88CC55", "#AAAA33", "#BBAA22", "#998822", VANISH_GRAY]
        v_scales = [1.00, 0.80, 0.60, 0.40, 0.24, 0.10]

        bp_v_arrs = []; bp_v_lbls = []
        for idx, i in enumerate(range(T - 1, -1, -1)):
            sc = v_scales[idx]; col = v_cols[idx]
            x_to = HX[i]
            x_fr = HX[i+1] if i < T - 1 else GRAD_START_X
            a = mk_arr(np.array([x_fr, lane_y, 0]), np.array([x_to, lane_y, 0]),
                       col, sw=max(3.5 * sc, 0.3))
            a.set_opacity(max(0.12, sc)); bp_v_arrs.append(a)
            lbl = grad_pill(v_vals[idx], np.array([x_to, lane_y + 0.50, 0]), col)
            lbl.scale(max(sc * 0.85 + 0.15, 0.30)); bp_v_lbls.append(lbl)
            self.play(GrowArrow(a), FadeIn(lbl), run_time=0.22)
            if idx >= 3:
                self.play(h_mobs[i].animate.set_opacity(0.20), run_time=0.14)
            if idx >= 4:
                self.play(word_mobs[i].animate.set_opacity(0.12), run_time=0.14)

        self.wait(2.2)
        self.play(
            *[FadeOut(m) for m in bp_v_arrs + bp_v_lbls],
            *[h_mobs[i].animate.set_opacity(1.0) for i in range(T)],
            *[word_mobs[i].animate.set_opacity(1.0) for i in range(T)],
            run_time=0.4,
        )
        self.wait(0.4)

        # ── Phase 3: Exploding ────────────────────────────────────────
        e_vals   = ["1.0", "2.1", "4.4", "9.2", "19", "40!"]
        e_scales = [1.00, 1.18, 1.38, 1.60, 1.86, 2.15]

        bp_e_arrs = []; bp_e_lbls = []
        for idx, i in enumerate(range(T - 1, -1, -1)):
            sc   = e_scales[idx]
            x_to = HX[i]
            x_fr = HX[i+1] if i < T - 1 else GRAD_START_X
            a = mk_arr(np.array([x_fr, lane_y, 0]), np.array([x_to, lane_y, 0]),
                       EXPLODE_RED, sw=min(3.5 * sc, 10.0))
            a.set_opacity(min(1.0, 0.48 + sc * 0.24)); bp_e_arrs.append(a)
            lbl = grad_pill(e_vals[idx], np.array([x_to, lane_y + 0.50, 0]), EXPLODE_RED)
            lbl.scale(min(sc * 0.80 + 0.20, 1.60)); bp_e_lbls.append(lbl)
            self.play(GrowArrow(a), FadeIn(lbl), run_time=0.22)
            if idx >= 4:
                self.play(Indicate(h_mobs[i], color=EXPLODE_RED, scale_factor=1.26),
                          run_time=0.20)

        self.wait(2.5)
        self.play(
            *[FadeOut(m) for m in bp_e_arrs + bp_e_lbls],
            run_time=0.5,
        )
        self.wait(1.0)
        validate_layout(self, label="VanishingGradients", camera_scale=1.70)

class VanillaRNNCell(InteractiveScene):
    def construct(self):
        self.camera.frame.scale(1.25)

        # ── Colors ────────────────────────────────────────────────────────
        C_CELL_FILL = "#1E8449"
        C_CELL_STK  = "#0B5233"
        C_TANH_FILL = "#8B0000"
        C_TANH_STK  = "#C0392B"
        C_SOFT_FILL = "#B7440A"
        C_SOFT_STK  = "#7D3108"
        C_A_FILL    = "#7D3C98"
        C_A_STK     = "#4A235A"
        C_H         = "#5DADE2"
        C_X         = "#F4D03F"

        # ── Helpers ───────────────────────────────────────────────────────
        def ln(a, b, col, sw=3.0):
            l = Line(a, b, stroke_width=sw).set_color(col)
            l.z_index = -1
            return l

        def mk_pulse(col="#FF3333", r=0.18):
            o = Dot(radius=r)
            o.set_fill(col, opacity=0.65)
            o.set_stroke(width=0)
            o.set_z_index(6)
            i = Dot(radius=r * 0.5)
            i.set_fill(WHITE, opacity=1.0)
            i.set_stroke(width=0)
            i.set_z_index(7)
            return VGroup(o, i)

        # ── Positions ─────────────────────────────────────────────────────
        TANH_P = np.array([ 0.00,  0.10, 0])
        MERG_P = np.array([ 0.00, -1.20, 0])
        AIN_P  = np.array([-5.00, -1.20, 0])
        AOUT_P = np.array([ 5.00,  0.10, 0])
        X_P    = np.array([ 0.00, -3.80, 0])
        SOFT_P = np.array([ 0.00,  2.40, 0])
        YHAT_P = np.array([ 0.00,  3.80, 0])

        # ── Green cell box ────────────────────────────────────────────────
        cell_box = RoundedRectangle(width=5.6, height=4.0, corner_radius=0.42)
        cell_box.set_fill(C_CELL_FILL, opacity=0.16)
        cell_box.set_stroke(C_CELL_STK, width=4.5)
        cell_box.move_to(np.array([0.00, -0.80, 0]))

        # ── Tanh circle — INSIDE ─────────────────────────────────────────
        tanh_bg = Circle(radius=0.80)
        tanh_bg.set_fill(C_TANH_FILL, opacity=0.97)
        tanh_bg.set_stroke(C_TANH_STK, width=4.0)
        tanh_bg.move_to(TANH_P)
        tanh_lbl = Text("T", font_size=68, weight="BOLD")
        tanh_lbl.set_color(WHITE)
        tanh_lbl.scale(1.25)
        tanh_lbl.move_to(TANH_P)
        tanh_node = VGroup(tanh_bg, tanh_lbl)

        # ── a_{t-1} purple rectangle — OUTSIDE left ──────────────────────
        a_in_box = RoundedRectangle(width=1.80, height=0.90, corner_radius=0.18)
        a_in_box.set_fill(C_A_FILL, opacity=0.90)
        a_in_box.set_stroke(C_A_STK, width=3.0)
        a_in_box.move_to(AIN_P)
        a_in_lbl = Tex(r"a_{t-1}", font_size=44)
        a_in_lbl.set_color(WHITE)
        a_in_lbl.scale(1.25)
        a_in_lbl.move_to(AIN_P)
        a_in_node = VGroup(a_in_box, a_in_lbl)

        # ── a_t purple rectangle — OUTSIDE right ─────────────────────────
        a_out_box = RoundedRectangle(width=1.40, height=0.90, corner_radius=0.18)
        a_out_box.set_fill(C_A_FILL, opacity=0.90)
        a_out_box.set_stroke(C_A_STK, width=3.0)
        a_out_box.move_to(AOUT_P)
        a_out_lbl = Tex(r"a_t", font_size=44)
        a_out_lbl.set_color(WHITE)
        a_out_lbl.scale(1.25)
        a_out_lbl.move_to(AOUT_P)
        a_out_node = VGroup(a_out_box, a_out_lbl)

        # ── x input node — OUTSIDE below ─────────────────────────────────
        x_circ = Circle(radius=0.42)
        x_circ.set_fill(C_X, opacity=0.97)
        x_circ.set_stroke(WHITE, width=2.5)
        x_circ.move_to(X_P)
        x_lbl = Text("x", font_size=46, weight="BOLD")
        x_lbl.set_color(BLACK)
        x_lbl.scale(1.25)
        x_lbl.move_to(X_P)
        x_node = VGroup(x_circ, x_lbl)

        # ── Softmax — OUTSIDE above box ──────────────────────────────────
        soft_box = RoundedRectangle(width=2.80, height=0.85, corner_radius=0.22)
        soft_box.set_fill(C_SOFT_FILL, opacity=0.97)
        soft_box.set_stroke(C_SOFT_STK, width=2.5)
        soft_box.move_to(SOFT_P)
        soft_lbl = Text("softmax", font_size=32, weight="BOLD")
        soft_lbl.set_color(WHITE)
        soft_lbl.scale(1.25)
        soft_lbl.move_to(SOFT_P)
        soft_node = VGroup(soft_box, soft_lbl)

        # ── y-hat (yellow circle, black text) — OUTSIDE above softmax ────
        yhat_circ = Circle(radius=0.48)
        yhat_circ.set_fill(C_X, opacity=0.97)
        yhat_circ.set_stroke(WHITE, width=2.5)
        yhat_circ.move_to(YHAT_P)
        yhat_lbl = Tex(r"\hat{y}", font_size=48)
        yhat_lbl.set_color(BLACK)
        yhat_lbl.scale(1.25)
        yhat_lbl.move_to(YHAT_P)
        yhat_node = VGroup(yhat_circ, yhat_lbl)

        # ── Lines (all z_index=-1, behind shapes) ────────────────────────
        l_ain   = ln(a_in_node.get_right(), MERG_P,                 C_H)
        l_xin   = ln(x_node.get_top(),      MERG_P,                 C_X)
        l_merge = ln(MERG_P,                TANH_P,                  WHITE)
        l_tnhs  = ln(tanh_bg.get_top(),     soft_box.get_bottom(),   WHITE)
        l_syh   = ln(soft_box.get_top(),    yhat_node.get_bottom(),  WHITE)
        l_hout  = ln(tanh_bg.get_right(),   a_out_node.get_left(),   C_H)

        # ══════════════════════════════════════════════════════════════════
        # PHASE 1 — GrowFromCenter all shapes first
        # ══════════════════════════════════════════════════════════════════
        self.play(GrowFromCenter(cell_box), run_time=0.55)
        self.play(
            GrowFromCenter(a_in_node),
            GrowFromCenter(a_out_node),
            GrowFromCenter(x_node),
            GrowFromCenter(tanh_node),
            GrowFromCenter(soft_node),
            GrowFromCenter(yhat_node),
            run_time=0.60,
        )
        self.wait(0.20)

        # ══════════════════════════════════════════════════════════════════
        # PHASE 2 — Draw all connecting lines
        # ══════════════════════════════════════════════════════════════════
        self.play(
            ShowCreation(l_ain),
            ShowCreation(l_xin),
            ShowCreation(l_merge),
            run_time=0.55,
        )
        self.play(
            ShowCreation(l_hout),
            ShowCreation(l_tnhs),
            ShowCreation(l_syh),
            run_time=0.55,
        )
        self.wait(0.30)

        # ══════════════════════════════════════════════════════════════════
        # PHASE 3 — Single slow pulse pass
        # ══════════════════════════════════════════════════════════════════

        # Dual input: a_{t-1} pulse + x pulse converge at merge
        pa = mk_pulse(C_H, r=0.20)
        pa.move_to(a_in_node.get_center())
        px = mk_pulse(C_X, r=0.20)
        px.move_to(x_node.get_center())
        self.play(GrowFromCenter(pa), GrowFromCenter(px), run_time=0.12)
        self.play(
            pa.animate.move_to(MERG_P),
            px.animate.move_to(MERG_P),
            run_time=0.60,
        )
        self.play(FadeOut(pa), FadeOut(px), run_time=0.10)

        # Merged pulse rises into tanh center
        pm = mk_pulse(WHITE, r=0.22)
        pm.move_to(MERG_P)
        self.play(GrowFromCenter(pm), run_time=0.10)
        self.play(pm.animate.move_to(TANH_P), run_time=0.45)
        self.play(FadeOut(pm), run_time=0.10)

        # Tanh activates
        self.play(
            Indicate(tanh_node, color=WHITE, scale_factor=1.12),
            run_time=0.35,
        )

        # Split: hidden-out + softmax path simultaneously
        ph = mk_pulse(C_H, r=0.20)
        ph.move_to(TANH_P)
        ps = mk_pulse(WHITE, r=0.20)
        ps.move_to(TANH_P)
        self.play(GrowFromCenter(ph), GrowFromCenter(ps), run_time=0.10)
        self.play(
            ph.animate.move_to(a_out_node.get_center()),
            ps.animate.move_to(soft_node.get_center()),
            run_time=0.60,
        )
        self.play(FadeOut(ph), FadeOut(ps), run_time=0.10)

        # Softmax -> y-hat
        py = mk_pulse(C_X, r=0.20)
        py.move_to(soft_node.get_center())
        self.play(GrowFromCenter(py), run_time=0.10)
        self.play(py.animate.move_to(yhat_node.get_center()), run_time=0.40)
        self.play(FadeOut(py), run_time=0.10)

        self.wait(1.00)

        validate_layout(self, label="VanillaRNN", camera_scale=1.25)


class LSTMCell(InteractiveScene):
    def construct(self):
        self.camera.frame.scale(1.50)

        # ── Colors ────────────────────────────────────────────────────────
        C_CELL_FILL = "#1E8449"
        C_CELL_STK  = "#0B5233"
        C_SIG       = "#F39C12"
        C_SIG_S     = "#D68910"
        C_TANH_FILL = "#8B0000"
        C_TANH_STK  = "#C0392B"
        C_ADD_GRN   = "#27AE60"
        C_CSTR      = "#3498DB"
        C_CSTR_STK  = "#1A5276"
        C_A_FILL    = "#7D3C98"
        C_A_STK     = "#4A235A"
        C_XT        = "#5DADE2"
        C_YHAT      = "#F4D03F"
        C_PULSE     = "#FFA500"

        # ── Shifts: left + down for inside elements ──────────────────────
        SX = -0.80
        SY = -0.40

        # ── Bright pulse colors (lighter/vivid versions) ─────────────────
        C_A_BRIGHT    = "#C39BD3"   # bright purple
        C_XT_BRIGHT   = "#85C1E9"   # bright blue
        C_SIG_BRIGHT  = "#F5B041"   # bright orange
        C_TANH_BRIGHT = "#E74C3C"   # bright red
        C_CSTR_BRIGHT = "#5DADE2"   # bright blue
        C_YHAT_BRIGHT = "#F9E154"   # bright yellow

        # ── Helpers ───────────────────────────────────────────────────────
        def ln(a, b, col, sw=4.5):
            l = Line(a, b, stroke_width=sw).set_color(col)
            l.z_index = -1
            return l

        def mk_pulse(col=C_PULSE, r=0.25):
            o = Dot(radius=r)
            o.set_fill(col, opacity=0.80)
            o.set_stroke(width=0)
            o.set_z_index(6)
            i = Dot(radius=r * 0.48)
            i.set_fill(WHITE, opacity=1.0)
            i.set_stroke(width=0)
            i.set_z_index(7)
            return VGroup(o, i)

        def run_p(start, end, col=C_PULSE, rt=0.40):
            p = mk_pulse(col)
            p.move_to(start)
            self.play(GrowFromCenter(p), run_time=0.08)
            self.play(p.animate.move_to(end), run_time=rt)
            self.play(FadeOut(p), run_time=0.08)

        def sigma_circ(pos, r=0.60, fs=44):
            bg = Circle(radius=r)
            bg.set_fill(C_SIG, opacity=0.97)
            bg.set_stroke(C_SIG_S, width=3.5)
            bg.move_to(pos)
            lbl = Tex(r"\sigma", font_size=fs)
            lbl.set_color(WHITE); lbl.scale(2.0); lbl.move_to(pos)
            return bg, lbl, VGroup(bg, lbl)

        def tanh_circ(pos, r=0.50, fs=44):
            bg = Circle(radius=r)
            bg.set_fill(C_TANH_FILL, opacity=0.97)
            bg.set_stroke(C_TANH_STK, width=3.5)
            bg.move_to(pos)
            lbl = Text("T", font_size=fs, weight="BOLD")
            lbl.set_color(WHITE); lbl.scale(1.25); lbl.move_to(pos)
            return bg, lbl, VGroup(bg, lbl)

        def op_node(pos, is_mult=True, r=0.45, fs=52):
            bg = Circle(radius=r)
            if is_mult:
                bg.set_fill(WHITE, opacity=0.97)
                bg.set_stroke("#999999", width=4.5)
                lbl = Tex(r"\times", font_size=fs)
                lbl.set_color(BLACK)
                lbl.set_stroke(BLACK, width=2.0)
            else:
                bg.set_fill(C_ADD_GRN, opacity=0.97)
                bg.set_stroke(WHITE, width=4.5)
                lbl = Text("+", font_size=fs, weight="BOLD")
                lbl.set_color(WHITE)
            bg.move_to(pos)
            lbl.scale(1.25); lbl.move_to(pos)
            return bg, lbl, VGroup(bg, lbl)

        # ── Description text (pure math, top) ───────────────────────────
        DESC_P = np.array([0.0, 4.70, 0])
        desc_ref = [None]

        def show_desc(txt):
            new_t = Tex(txt, font_size=92)
            new_t.set_color(WHITE)
            new_t.move_to(DESC_P)
            if desc_ref[0] is not None:
                self.play(FadeOut(desc_ref[0]), FadeIn(new_t), run_time=0.28)
            else:
                self.play(FadeIn(new_t), run_time=0.28)
            desc_ref[0] = new_t

        def clear_desc():
            if desc_ref[0] is not None:
                self.play(FadeOut(desc_ref[0]), run_time=0.25)
                desc_ref[0] = None

        # ── Inside positions (shifted left+down) ─────────────────────────
        CONC_P   = np.array([ 0.00 + SX, -2.35 + SY, 0])
        BRANCH_P = np.array([ 5.00 + SX,  2.50 + SY, 0])
        BUS_Y    = -1.80 + SY
        BUS_P_L  = np.array([-3.80 + SX, BUS_Y, 0])
        BUS_P_R  = np.array([ 3.20 + SX, BUS_Y, 0])
        BUS_P_M  = np.array([ 0.00 + SX, BUS_Y, 0])

        # Elbow Y for L-shaped gate→xinp lines (same as xinp center Y)
        ELBOW_Y = 1.20 + SY
        SI_ELBOW = np.array([-1.20 + SX, ELBOW_Y, 0])
        TG_ELBOW = np.array([ 1.20 + SX, ELBOW_Y, 0])

        # Branch for y_hat — same Y as xout/aout so line is straight
        YHAT_BR = np.array([5.70, -0.30 + SY, 0])

        # ══════════════════════════════════════════════════════════════════
        #  BUILD ALL SHAPES
        # ══════════════════════════════════════════════════════════════════

        cell_box = RoundedRectangle(width=12.0, height=7.0, corner_radius=0.50)
        cell_box.set_fill(C_CELL_FILL, opacity=0.16)
        cell_box.set_stroke(C_CELL_STK, width=4.5)
        cell_box.move_to(ORIGIN)
        cell_box.set_z_index(-4)

        # C-stream ops
        xf_bg, xf_lbl, xf_node = op_node(
            np.array([-3.80 + SX, 2.50 + SY, 0]), is_mult=True)
        add_bg, add_lbl, add_node = op_node(
            np.array([0.00 + SX, 2.50 + SY, 0]), is_mult=False)

        # 4 Gates
        sf_bg, sf_lbl, sf_node = sigma_circ(np.array([-3.80 + SX, -0.30 + SY, 0]))
        si_bg, si_lbl, si_node = sigma_circ(np.array([-1.20 + SX, -0.30 + SY, 0]))
        tg_bg, tg_lbl, tg_node = tanh_circ(np.array([ 1.20 + SX, -0.30 + SY, 0]))
        so_bg, so_lbl, so_node = sigma_circ(np.array([ 3.20 + SX, -0.30 + SY, 0]))

        # Gate labels — bold, left of riser
        glbl_f = Tex(r"f", font_size=38)
        glbl_f.scale(2.0)
        glbl_f.set_color(WHITE)
        glbl_f.next_to(sf_bg, DOWN, buff=0.12)
        glbl_f.shift(LEFT * 0.30)

        glbl_i = Tex(r"i", font_size=38)
        glbl_i.scale(2.0)
        glbl_i.set_color(WHITE)
        glbl_i.next_to(si_bg, DOWN, buff=0.12)
        glbl_i.shift(LEFT * 0.30)

        glbl_c = Tex(r"\tilde{c}", font_size=38)
        glbl_c.scale(2.0)
        glbl_c.set_color(WHITE)
        glbl_c.next_to(tg_bg, DOWN, buff=0.12)
        glbl_c.shift(LEFT * 0.30)

        glbl_o = Tex(r"o", font_size=38)
        glbl_o.scale(2.0)
        glbl_o.set_color(WHITE)
        glbl_o.next_to(so_bg, DOWN, buff=0.12)
        glbl_o.shift(LEFT * 0.30)

        # Input multiply
        xinp_bg, xinp_lbl, xinp_node = op_node(
            np.array([0.00 + SX, 1.20 + SY, 0]), is_mult=True, r=0.42, fs=48)

        # Output path
        tc_bg, tc_lbl, tc_node = tanh_circ(
            np.array([5.00 + SX, 1.50 + SY, 0]), r=0.42, fs=38)
        xout_bg, xout_lbl, xout_node = op_node(
            np.array([5.00 + SX, -0.30 + SY, 0]), is_mult=True, r=0.42, fs=48)

        # Concat dot
        conc_dot = Circle(radius=0.12)
        conc_dot.set_fill(WHITE, opacity=1.0)
        conc_dot.set_stroke(WHITE, width=2.0)
        conc_dot.move_to(CONC_P)

        # ── Outside elements (NOT shifted, except xt X aligned) ──────────
        def blue_rect(pos, w, tex_str):
            bx = RoundedRectangle(width=w, height=0.85, corner_radius=0.18)
            bx.set_fill(C_CSTR, opacity=0.90)
            bx.set_stroke(C_CSTR_STK, width=3.0)
            bx.move_to(pos)
            lb = Tex(tex_str, font_size=38)
            lb.set_color(WHITE); lb.scale(1.30); lb.move_to(pos)
            return VGroup(bx, lb)

        def purp_rect(pos, w, tex_str):
            bx = RoundedRectangle(width=w, height=0.90, corner_radius=0.18)
            bx.set_fill(C_A_FILL, opacity=0.90)
            bx.set_stroke(C_A_STK, width=3.0)
            bx.move_to(pos)
            lb = Tex(tex_str, font_size=44)
            lb.set_color(WHITE); lb.scale(1.50); lb.move_to(pos)
            return VGroup(bx, lb)

        cin_node  = blue_rect(np.array([-8.00,  2.50 + SY, 0]), 1.80, r"C_{t-1}")
        cout_node = blue_rect(np.array([ 8.00,  2.50 + SY, 0]), 1.40, r"C_t")
        ain_node  = purp_rect(np.array([-8.00, -2.35 + SY, 0]), 2.10, r"a_{t-1}")
        aout_node = purp_rect(np.array([ 8.00, -0.30 + SY, 0]), 1.70, r"a_t")

        # x_t — aligned X with CONC_P so line is straight up
        xt_circ = Circle(radius=0.55)
        xt_circ.set_fill(C_XT, opacity=0.97)
        xt_circ.set_stroke(WHITE, width=5.5)
        xt_circ.move_to(np.array([0.00 + SX, -5.00, 0]))
        xt_lbl = Tex(r"x_t", font_size=50)
        xt_lbl.set_color(BLACK); xt_lbl.scale(1.50)
        xt_lbl.move_to(xt_circ.get_center())
        xt_node = VGroup(xt_circ, xt_lbl)

        # y_hat — yellow, further down (no overlap)
        yhat_circ = Circle(radius=0.50)
        yhat_circ.set_fill(C_YHAT, opacity=0.97)
        yhat_circ.set_stroke(WHITE, width=5.0)
        yhat_circ.move_to(np.array([5.70, -4.50, 0]))
        yhat_lbl = Tex(r"\hat{y}", font_size=44)
        yhat_lbl.set_color(BLACK); yhat_lbl.scale(1.30)
        yhat_lbl.move_to(yhat_circ.get_center())
        yhat_node = VGroup(yhat_circ, yhat_lbl)

        # ══════════════════════════════════════════════════════════════════
        #  LINES  (all z_index=-1, sw=4.5)
        # ══════════════════════════════════════════════════════════════════

        # C stream
        l_c1 = ln(cin_node.get_right(),  xf_bg.get_left(),    C_CSTR)
        l_c2 = ln(xf_bg.get_right(),    add_bg.get_left(),    C_CSTR)
        l_c3 = ln(add_bg.get_right(),   BRANCH_P,             C_CSTR)
        l_c4 = ln(BRANCH_P,             cout_node.get_left(), C_CSTR)

        # Gate -> ops
        l_sf_xf    = ln(sf_bg.get_top(),   xf_bg.get_bottom(),   C_SIG)
        l_xinp_add = ln(xinp_bg.get_top(), add_bg.get_bottom(),  WHITE)

        # L-shaped: sigma_i -> xinp (up then right) — rounded corner
        R_CORN = 0.25
        si_start = si_bg.get_top()
        si_end   = xinp_bg.get_left()
        l_si_up = ln(si_start, SI_ELBOW + DOWN * R_CORN, C_SIG)
        l_si_corner = ArcBetweenPoints(
            SI_ELBOW + DOWN * R_CORN, SI_ELBOW + RIGHT * R_CORN,
            angle=-TAU / 4,
        )
        l_si_corner.set_stroke(C_SIG, width=4.5)
        l_si_corner.z_index = -1
        l_si_h = ln(SI_ELBOW + RIGHT * R_CORN, si_end, C_SIG)

        # L-shaped: tanh_g -> xinp (up then left) — rounded corner
        tg_start = tg_bg.get_top()
        tg_end   = xinp_bg.get_right()
        l_tg_up = ln(tg_start, TG_ELBOW + DOWN * R_CORN, C_TANH_FILL)
        l_tg_corner = ArcBetweenPoints(
            TG_ELBOW + DOWN * R_CORN, TG_ELBOW + LEFT * R_CORN,
            angle=TAU / 4,
        )
        l_tg_corner.set_stroke(C_TANH_FILL, width=4.5)
        l_tg_corner.z_index = -1
        l_tg_h = ln(TG_ELBOW + LEFT * R_CORN, tg_end, C_TANH_FILL)

        # Output path
        l_br_tc   = ln(BRANCH_P,           tc_bg.get_top(),      C_CSTR)
        l_tc_xout = ln(tc_bg.get_bottom(), xout_bg.get_top(),    WHITE)
        l_so_xout = ln(so_bg.get_right(),  xout_bg.get_left(),   C_SIG)
        l_xout_br = ln(xout_bg.get_right(), YHAT_BR,             WHITE)
        l_br_at   = ln(YHAT_BR,             aout_node.get_left(), WHITE)
        l_br_yhat = ln(YHAT_BR,             yhat_node.get_top(),  C_YHAT)

        # Inputs — x_t line is now perfectly vertical
        l_ain = ln(ain_node.get_right(), CONC_P, C_A_FILL)
        l_xin = ln(xt_node.get_top(),   CONC_P, C_XT)

        # Bus routing
        l_conc_bus = ln(CONC_P, BUS_P_M, WHITE, sw=3.75)
        l_bus      = ln(BUS_P_L, BUS_P_R, WHITE, sw=3.75)
        l_vf = ln(np.array([-3.80 + SX, BUS_Y, 0]), sf_bg.get_bottom(), WHITE, sw=3.0)
        l_vi = ln(np.array([-1.20 + SX, BUS_Y, 0]), si_bg.get_bottom(), WHITE, sw=3.0)
        l_vg = ln(np.array([ 1.20 + SX, BUS_Y, 0]), tg_bg.get_bottom(), WHITE, sw=3.0)
        l_vo = ln(np.array([ 3.20 + SX, BUS_Y, 0]), so_bg.get_bottom(), WHITE, sw=3.0)

        # ══════════════════════════════════════════════════════════════════
        #  PHASE 1 — GrowFromCenter
        # ══════════════════════════════════════════════════════════════════
        self.play(GrowFromCenter(cell_box), run_time=0.55)
        self.play(
            GrowFromCenter(cin_node), GrowFromCenter(cout_node),
            GrowFromCenter(ain_node), GrowFromCenter(aout_node),
            GrowFromCenter(xt_node),  GrowFromCenter(yhat_node),
            run_time=0.50,
        )
        self.play(
            GrowFromCenter(xf_node), GrowFromCenter(add_node),
            GrowFromCenter(sf_node), GrowFromCenter(si_node),
            GrowFromCenter(tg_node), GrowFromCenter(so_node),
            GrowFromCenter(xinp_node),
            GrowFromCenter(tc_node), GrowFromCenter(xout_node),
            GrowFromCenter(conc_dot),
            run_time=0.60,
        )
        self.play(
            FadeIn(glbl_f), FadeIn(glbl_i),
            FadeIn(glbl_c), FadeIn(glbl_o),
            run_time=0.30,
        )
        self.wait(0.20)

        # ══════════════════════════════════════════════════════════════════
        #  PHASE 2 — ShowCreation lines
        # ══════════════════════════════════════════════════════════════════
        self.play(
            ShowCreation(l_c1), ShowCreation(l_c2),
            ShowCreation(l_c3), ShowCreation(l_c4),
            run_time=0.50,
        )
        self.play(
            ShowCreation(l_ain), ShowCreation(l_xin),
            run_time=0.45,
        )
        self.play(ShowCreation(l_conc_bus), run_time=0.25)
        self.play(ShowCreation(l_bus), run_time=0.40)
        self.play(
            ShowCreation(l_vf), ShowCreation(l_vi),
            ShowCreation(l_vg), ShowCreation(l_vo),
            run_time=0.45,
        )
        self.play(
            ShowCreation(l_sf_xf),
            ShowCreation(l_si_up), ShowCreation(l_si_corner), ShowCreation(l_si_h),
            ShowCreation(l_tg_up), ShowCreation(l_tg_corner), ShowCreation(l_tg_h),
            ShowCreation(l_xinp_add),
            run_time=0.50,
        )
        self.play(
            ShowCreation(l_br_tc), ShowCreation(l_tc_xout),
            ShowCreation(l_so_xout),
            ShowCreation(l_xout_br), ShowCreation(l_br_at),
            ShowCreation(l_br_yhat),
            run_time=0.50,
        )
        self.wait(0.30)

        # ══════════════════════════════════════════════════════════════════
        #  PHASE 3 — Pulse pass with math equations
        # ══════════════════════════════════════════════════════════════════

        # Inputs concatenated
        run_p(ain_node.get_center(), CONC_P, C_A_BRIGHT, rt=0.50)
        run_p(xt_node.get_center(),  CONC_P, C_XT_BRIGHT, rt=0.50)
        show_desc(r"[a_{t-1},\, x_t]")
        self.wait(2.0)

        run_p(CONC_P, BUS_P_M, WHITE, rt=0.25)

        # Forget gate
        run_p(BUS_P_L, sf_node.get_center(), WHITE, rt=0.35)
        self.play(Indicate(sf_node, color=WHITE, scale_factor=1.10), run_time=0.22)
        show_desc(r"f_t = \sigma(W_f \cdot [a_{t-1},\, x_t] + b_f)")
        self.wait(2.0)

        # Forget elementwise multiply (f_t ⊙ C_{t-1})
        run_p(cin_node.get_center(), xf_node.get_center(), C_CSTR_BRIGHT, rt=0.40)
        run_p(sf_node.get_center(),  xf_node.get_center(), C_SIG_BRIGHT,  rt=0.30)
        self.play(Indicate(xf_node, color=WHITE, scale_factor=1.12), run_time=0.22)
        show_desc(r"f_t \odot C_{t-1}")
        self.wait(2.0)

        # Input gate
        run_p(np.array([-1.20 + SX, BUS_Y, 0]), si_node.get_center(), WHITE, rt=0.35)
        self.play(Indicate(si_node, color=WHITE, scale_factor=1.10), run_time=0.22)
        show_desc(r"i_t = \sigma(W_i \cdot [a_{t-1},\, x_t] + b_i)")
        self.wait(2.0)

        # Candidate c̃
        run_p(np.array([1.20 + SX, BUS_Y, 0]), tg_node.get_center(), WHITE, rt=0.35)
        self.play(Indicate(tg_node, color=WHITE, scale_factor=1.10), run_time=0.22)
        show_desc(r"\tilde{c}_t = \tanh(W_c \cdot [a_{t-1},\, x_t] + b_c)")
        self.wait(2.0)

        # Input multiply (i_t ⊙ c̃_t) — L-shaped pulses
        # sigma_i -> elbow -> xinp
        run_p(si_node.get_center(), SI_ELBOW, C_SIG_BRIGHT, rt=0.18)
        run_p(SI_ELBOW, xinp_node.get_center(), C_SIG_BRIGHT, rt=0.18)
        # tanh_g -> elbow -> xinp
        run_p(tg_node.get_center(), TG_ELBOW, C_TANH_BRIGHT, rt=0.18)
        run_p(TG_ELBOW, xinp_node.get_center(), C_TANH_BRIGHT, rt=0.18)
        self.play(Indicate(xinp_node, color=WHITE, scale_factor=1.12), run_time=0.22)
        show_desc(r"i_t \odot \tilde{c}_t")
        self.wait(2.0)

        # C_t calculation: both paths feed into add node
        run_p(xf_node.get_center(), add_node.get_center(), C_CSTR_BRIGHT, rt=0.35)
        run_p(xinp_node.get_center(), add_node.get_center(), WHITE, rt=0.30)
        self.play(Indicate(add_node, color=WHITE, scale_factor=1.12), run_time=0.22)
        show_desc(r"C_t = f_t \odot C_{t-1} + i_t \odot \tilde{c}_t")
        self.wait(2.0)

        run_p(add_node.get_center(), cout_node.get_center(), C_CSTR_BRIGHT, rt=0.40)

        # Output gate
        run_p(BUS_P_R, so_node.get_center(), WHITE, rt=0.35)
        self.play(Indicate(so_node, color=WHITE, scale_factor=1.10), run_time=0.22)
        show_desc(r"o_t = \sigma(W_o \cdot [a_{t-1},\, x_t] + b_o)")
        self.wait(2.0)

        # tanh(C_t) from above
        run_p(BRANCH_P, tc_node.get_center(), C_CSTR_BRIGHT, rt=0.30)
        self.play(Indicate(tc_node, color=WHITE, scale_factor=1.10), run_time=0.22)
        show_desc(r"\tanh(C_t)")
        self.wait(2.0)

        # Output elementwise multiply: o_t ⊙ tanh(C_t)
        run_p(so_node.get_center(),  xout_node.get_center(), C_SIG_BRIGHT, rt=0.30)
        run_p(tc_node.get_center(),  xout_node.get_center(), WHITE, rt=0.30)
        self.play(Indicate(xout_node, color=WHITE, scale_factor=1.12), run_time=0.22)
        show_desc(r"a_t = o_t \odot \tanh(C_t)")
        self.wait(2.0)

        run_p(xout_node.get_center(), YHAT_BR, C_CSTR_BRIGHT, rt=0.30)
        run_p(YHAT_BR, aout_node.get_center(), C_CSTR_BRIGHT, rt=0.30)
        run_p(YHAT_BR, yhat_node.get_center(), C_YHAT_BRIGHT, rt=0.40)
        show_desc(r"\hat{y}_t")
        self.wait(2.0)

        clear_desc()
        self.wait(0.50)

        validate_layout(self, label="LSTMCell", camera_scale=1.50)

        # ================================================================
        # PHASE 4 -- Unrolled LSTM chain: "I grew up in France. I speak ____"
        # ================================================================
        # Fade all existing objects
        all_p3 = [
            cell_box,
            cin_node, cout_node, ain_node, aout_node, xt_node, yhat_node,
            xf_node, add_node, sf_node, si_node, tg_node, so_node,
            xinp_node, tc_node, xout_node, conc_dot,
            glbl_f, glbl_i, glbl_c, glbl_o,
            l_c1, l_c2, l_c3, l_c4,
            l_ain, l_xin, l_conc_bus, l_bus,
            l_vf, l_vi, l_vg, l_vo,
            l_sf_xf, l_si_up, l_si_corner, l_si_h, l_tg_up, l_tg_corner, l_tg_h, l_xinp_add,
            l_br_tc, l_tc_xout, l_so_xout, l_xout_br, l_br_at, l_br_yhat,
        ]
        self.play(
            *[FadeOut(m) for m in all_p3],
            self.camera.frame.animate.scale(1.80).move_to(RIGHT * 0.6),
            run_time=0.50,
        )
        self.wait(0.30)

        GOLD    = "#FFD700"
        CB      = "#3498DB"
        HT      = "#1ABC9C"
        WC      = "#A8DADC"
        CA      = "#F39C12"

        def arr5(a, b, col, sw=2.5, bf=0.08):
            ar = Arrow(a, b, buff=bf, stroke_width=sw,
                       max_tip_length_to_length_ratio=0.14)
            ar.set_color(col)
            return ar

        # -- Sentence at top --
        sentence5 = Text("I grew up in France.  I speak ____",
                         font_size=56)
        sentence5.set_color(WHITE)
        sentence5.scale(1.5)
        sentence5.move_to(np.array([0.0, 5.5, 0]))
        self.play(Write(sentence5), run_time=0.60)
        self.wait(2.0)

        # -- 7 simplified LSTM cells --
        words5 = ["I", "grew", "up", "in", "France", "I", "speak"]
        T5 = len(words5)
        SP5 = 4.2
        HX5 = [-(T5 - 1) * SP5 / 2 + i * SP5 for i in range(T5)]
        Y_CELL5 = 0.0
        Y_CSTATE5 = 2.5
        Y_WORD5 = -2.8

        cells5 = []
        for i in range(T5):
            r5 = RoundedRectangle(width=2.8, height=2.0, corner_radius=0.20)
            r5.set_fill(CB, opacity=0.15)
            r5.set_stroke(CB, width=2.5)
            r5.move_to(np.array([HX5[i], Y_CELL5, 0]))
            lb5 = Text("LSTM", font_size=48, weight="BOLD")
            lb5.set_color(CB)
            lb5.move_to(r5.get_center())
            cells5.append(VGroup(r5, lb5))

        # -- Cell state highway --
        cstate5 = Arrow(
            np.array([HX5[0] - 2.5, Y_CSTATE5, 0]),
            np.array([HX5[-1] + 2.5, Y_CSTATE5, 0]),
            buff=0, stroke_width=8.0, color=CB,
            max_tip_length_to_length_ratio=0.015,
        )

        # -- Hidden state arrows --
        h0_5c = Circle(radius=0.55)
        h0_5c.set_fill("#8E44AD", 0.40)
        h0_5c.set_stroke("#8E44AD", 2.0)
        h0_5c.move_to(np.array([HX5[0] - SP5 * 0.85, Y_CELL5, 0]))
        h0_5l = Tex(r"a_0", font_size=48)
        h0_5l.set_color(WHITE)
        h0_5l.move_to(h0_5c.get_center())
        h0_5g = VGroup(h0_5c, h0_5l)

        harr5_0 = arr5(h0_5g.get_right(), cells5[0][0].get_left(), HT, sw=3.0)
        harrs5 = [arr5(cells5[i][0].get_right(), cells5[i + 1][0].get_left(),
                       HT, sw=3.0)
                  for i in range(T5 - 1)]

        # -- Word labels + input arrows --
        wlbls5 = []
        xarrs5 = []
        for i in range(T5):
            wl5 = Text(words5[i], font_size=56, weight="BOLD")
            wl5.set_color(WC)
            wl5.move_to(np.array([HX5[i], Y_WORD5, 0]))
            wlbls5.append(wl5)
            xarrs5.append(arr5(wl5.get_top() + UP * 0.20,
                               cells5[i][0].get_bottom(),
                               WC, sw=2.5))

        # -- Vertical arrows: cell -> cell state --
        c_up5 = [arr5(cells5[i][0].get_top(),
                      np.array([HX5[i], Y_CSTATE5, 0]),
                      CB, sw=2.0, bf=0.10)
                 for i in range(T5)]

        # -- Prediction slot --
        pred5 = Text("?", font_size=56, weight="BOLD")
        pred5.set_color(CA)
        pred5.scale(1.4)
        pred5.move_to(np.array([HX5[-1] + SP5 * 0.55, Y_CELL5, 0]))
        pred5.shift(RIGHT * 0.7)
        pred_arr5 = arr5(cells5[-1][0].get_right(), pred5.get_left(),
                         CA, sw=3.0)

        # === Build diagram ===
        self.play(LaggedStart(*[FadeIn(c) for c in cells5],
                              lag_ratio=0.08, run_time=0.80))
        self.play(ShowCreation(cstate5), run_time=0.55)
        self.play(FadeIn(h0_5g), GrowArrow(harr5_0), run_time=0.35)
        self.play(LaggedStart(*[GrowArrow(ha) for ha in harrs5],
                              lag_ratio=0.06, run_time=0.65))
        self.play(
            LaggedStart(*[FadeIn(w) for w in wlbls5],
                        lag_ratio=0.06, run_time=0.60),
            LaggedStart(*[GrowArrow(xa) for xa in xarrs5],
                        lag_ratio=0.06, run_time=0.60),
        )
        self.play(LaggedStart(*[GrowArrow(ca) for ca in c_up5],
                              lag_ratio=0.06, run_time=0.55))
        self.play(FadeIn(pred5), GrowArrow(pred_arr5), run_time=0.35)
        self.wait(1.5)

        # === Sequential word processing ===
        def flash5(mob, tw=0.50, rt=0.55):
            return ShowPassingFlash(mob.copy().set_color(WHITE),
                                   time_width=tw, run_time=rt)

        gold_line5 = None
        for i in range(T5):
            self.play(Indicate(wlbls5[i], color=WHITE, scale_factor=1.15),
                      run_time=0.30)
            self.play(flash5(xarrs5[i], tw=0.50, rt=0.45), run_time=0.45)
            self.play(Indicate(cells5[i], color=WHITE, scale_factor=1.08),
                      run_time=0.30)
            self.play(flash5(c_up5[i], tw=0.50, rt=0.40), run_time=0.40)

            if i == 4:  # "France"
                gold_line5 = Line(
                    np.array([HX5[4], Y_CSTATE5, 0]),
                    np.array([HX5[-1] + 2.5, Y_CSTATE5, 0]),
                    stroke_width=10, color=GOLD,
                )
                gold_line5.set_opacity(0.70)
                france_msg = Text(
                    "France stored in cell state!",
                    font_size=48, weight="BOLD",
                )
                france_msg.set_color(GOLD)
                france_msg.move_to(np.array([0.0, 4.2, 0]))
                france_msg.shift(DOWN * 0.23)
                self.play(
                    Indicate(cells5[4], color=GOLD, scale_factor=1.25),
                    ShowCreation(gold_line5),
                    run_time=0.65,
                )
                self.play(FadeIn(france_msg, shift=UP * 0.15),
                          run_time=0.40)
                self.wait(2.0)
                self.play(FadeOut(france_msg), run_time=0.30)
                self.play(ShowPassingFlash(
                    gold_line5.copy().set_color(WHITE).set_opacity(0.80),
                    time_width=0.35, run_time=0.70))

            if i < T5 - 1:
                self.play(flash5(harrs5[i], tw=0.50, rt=0.40),
                          run_time=0.40)

            if i > 4 and gold_line5 is not None:
                self.play(ShowPassingFlash(
                    gold_line5.copy().set_color(WHITE).set_opacity(0.60),
                    time_width=0.30, run_time=0.55))

        # === Prediction reveal ===
        french5 = Text("French!", font_size=64, weight="BOLD")
        french5.set_color(GOLD)
        french5.next_to(pred_arr5, RIGHT, buff=0.25)
        self.play(FadeOut(pred5), Write(french5), run_time=0.55)
        self.play(
            Indicate(french5, color=WHITE, scale_factor=1.30),
            ShowPassingFlash(cstate5.copy().set_color(GOLD),
                            time_width=0.30, run_time=1.0),
            run_time=1.0,
        )
        self.wait(2.0)

        # === Takeaway message ===
        msg5a = Text("Cell state highway preserves long-term memory!",
                     font_size=76, weight="BOLD")
        msg5a.set_color(CB)
        msg5a.move_to(np.array([0.0, -4.95, 0]))
        self.play(Write(msg5a), run_time=0.65)
        self.wait(2.0)

        validate_layout(self, label="LSTMCell_P4_CHAIN", camera_scale=2.70)



class GRUCell(InteractiveScene):
    def construct(self):
        self.camera.frame.scale(1.50)

        # ── Colors ────────────────────────────────────────────────────────
        G_CELL_FILL = "#1F77B4"
        G_CELL_STK  = "#145A8A"
        G_SIG       = "#FF7F0E"    # orange sigma gates
        G_SIG_S     = "#CC6600"
        G_TANH_FILL = "#8B0000"    # red candidate tanh
        G_TANH_STK  = "#C0392B"
        G_ADD_BLU   = "#1F77B4"    # add node (blue)
        G_ASTR      = "#3498DB"    # activation stream blue
        G_A_FILL    = "#7D3C98"    # purple a nodes
        G_A_STK     = "#4A235A"
        G_XT        = "#5DADE2"    # cyan input
        G_YHAT      = "#F4D03F"    # yellow output
        G_PULSE     = "#FFA500"

        # Bright pulse colors
        G_A_BRIGHT    = "#C39BD3"
        G_XT_BRIGHT   = "#85C1E9"
        G_SIG_BRIGHT  = "#F5B041"
        G_TANH_BRIGHT = "#E74C3C"
        G_ASTR_BRIGHT = "#5DADE2"
        G_YHAT_BRIGHT = "#F9E154"
        G_AT_PURPLE     = "#9B59B6"    # purple a_{t-1} branch
        G_AT_PUR_BRIGHT = "#BB8FCE"    # bright purple pulse

        # ── Helpers ───────────────────────────────────────────────────────
        def ln(a, b, col, sw=4.5):
            l = Line(a, b, stroke_width=sw).set_color(col)
            l.z_index = -1
            return l

        def mk_pulse(col=G_PULSE, r=0.25):
            o = Dot(radius=r)
            o.set_fill(col, opacity=0.80)
            o.set_stroke(width=0)
            o.set_z_index(6)
            i = Dot(radius=r * 0.48)
            i.set_fill(WHITE, opacity=1.0)
            i.set_stroke(width=0)
            i.set_z_index(7)
            return VGroup(o, i)

        def run_p(start, end, col=G_PULSE, rt=0.40):
            p = mk_pulse(col)
            p.move_to(start)
            self.play(GrowFromCenter(p), run_time=0.08)
            self.play(p.animate.move_to(end), run_time=rt)
            self.play(FadeOut(p), run_time=0.08)

        def sigma_circ(pos, r=0.60, fs=44):
            bg = Circle(radius=r)
            bg.set_fill(G_SIG, opacity=0.97)
            bg.set_stroke(G_SIG_S, width=3.5)
            bg.move_to(pos)
            lbl = Tex(r"\sigma", font_size=fs)
            lbl.set_color(WHITE); lbl.scale(2.0); lbl.move_to(pos)
            return bg, lbl, VGroup(bg, lbl)

        def tanh_circ(pos, r=0.50, fs=44):
            bg = Circle(radius=r)
            bg.set_fill(G_TANH_FILL, opacity=0.97)
            bg.set_stroke(G_TANH_STK, width=3.5)
            bg.move_to(pos)
            lbl = Text("T", font_size=fs, weight="BOLD")
            lbl.set_color(WHITE); lbl.scale(1.25); lbl.move_to(pos)
            return bg, lbl, VGroup(bg, lbl)

        def op_node(pos, is_mult=True, r=0.45, fs=52):
            bg = Circle(radius=r)
            if is_mult:
                bg.set_fill(WHITE, opacity=0.97)
                bg.set_stroke("#999999", width=4.5)
                lbl = Tex(r"\times", font_size=fs)
                lbl.set_color(BLACK)
                lbl.set_stroke(BLACK, width=2.0)
            else:
                bg.set_fill(G_ADD_BLU, opacity=0.97)
                bg.set_stroke(WHITE, width=4.5)
                lbl = Text("+", font_size=fs, weight="BOLD")
                lbl.set_color(WHITE)
            bg.move_to(pos)
            lbl.scale(1.25); lbl.move_to(pos)
            return bg, lbl, VGroup(bg, lbl)

        # ── Description text (pure math, top) ───────────────────────────
        DESC_P = np.array([0.0, 4.70, 0])
        desc_ref = [None]

        def show_desc(txt):
            new_t = Tex(txt, font_size=92)
            new_t.set_color(WHITE)
            new_t.move_to(DESC_P)
            if desc_ref[0] is not None:
                self.play(FadeOut(desc_ref[0]), FadeIn(new_t), run_time=0.28)
            else:
                self.play(FadeIn(new_t), run_time=0.28)
            desc_ref[0] = new_t

        def clear_desc():
            if desc_ref[0] is not None:
                self.play(FadeOut(desc_ref[0]), run_time=0.25)
                desc_ref[0] = None

        # ── Symmetric GRU Layout ────────────────────────────────────────
        #
        #  Perfectly symmetric: center = ORIGIN, 3 columns
        #
        #           ×(1-z)  ────────  +  ────────  a_t (out)
        #  a_{t-1} ──┤               ↑
        #  (in)       │     ×(z)  ───┘
        #             │      ↑
        #          z(σ)    tanh(ã)    r(σ)
        #             │      ↑         │
        #             └── ×(r) ────────┘
        #                  ↑
        #             [a_{t-1}, x_t]
        #                  ↑
        #                 x_t

        # Activation stream Y (top row)
        A_Y = 2.50

        # Gate row Y (sigma gates sit on bus line)
        GATE_Y = -1.80

        # Tanh candidate Y (centered between rmul and top row)
        TANH_Y = 0.90

        # Bus Y (bottom inside)
        BUS_Y = -1.80

        # Symmetric X positions — 3-column grid
        X_LEFT  = -3.20    # z gate, ×(1-z)
        X_MID   =  0.00    # tanh, ×(z), ×(r), concat
        X_RIGHT =  3.20    # r gate

        # r⊙a multiply Y (also used for branch junction)
        RMUL_Y = -0.60

        # a_{t-1} branch-down X and merge Y
        BRANCH_X = -4.50
        MERGE_Y  = -2.80

        # Named points for branch/merge
        BRANCH_PT    = np.array([BRANCH_X, A_Y, 0])
        JUNC_RMUL_PT = np.array([BRANCH_X, RMUL_Y, 0])
        MERGE_PT     = np.array([X_MID, MERGE_Y, 0])

        # ══════════════════════════════════════════════════════════════════
        #  BUILD ALL SHAPES
        # ══════════════════════════════════════════════════════════════════

        cell_box = RoundedRectangle(width=12.0, height=7.0, corner_radius=0.50)
        cell_box.set_fill(G_CELL_FILL, opacity=0.16)
        cell_box.set_stroke(G_CELL_STK, width=4.5)
        cell_box.move_to(ORIGIN)
        cell_box.set_z_index(-4)

        # Top row: ×(1-z) left, + right (a-stream)
        keep_bg, keep_lbl, keep_node = op_node(
            np.array([X_LEFT, A_Y, 0]), is_mult=True)
        add_bg, add_lbl, add_node = op_node(
            np.array([X_RIGHT, A_Y, 0]), is_mult=False)
        add_bg.set_fill("#2ECC71", opacity=0.97)
        add_bg.set_stroke(WHITE, width=4.5)

        # Middle row: z gate (left), tanh candidate (center), r gate (right)
        sz_bg, sz_lbl, sz_node = sigma_circ(np.array([X_LEFT, GATE_Y, 0]))
        TANH_X = 2.20
        cand_bg, cand_lbl, cand_node = tanh_circ(
            np.array([TANH_X, TANH_Y - 0.30, 0]), r=0.55, fs=44)
        sr_bg, sr_lbl, sr_node = sigma_circ(np.array([X_RIGHT, GATE_Y, 0]))

        # z⊙ã multiply — below + node, off the main a-stream (parallel)
        ZMUL_Y = 1.50
        zmul_bg, zmul_lbl, zmul_node = op_node(
            np.array([X_MID, ZMUL_Y, 0]), is_mult=True, r=0.42, fs=48)

        # r⊙a multiply — below tanh (between gates and bus)
        rmul_bg, rmul_lbl, rmul_node = op_node(
            np.array([X_MID, RMUL_Y, 0]), is_mult=True, r=0.42, fs=48)

        # Gate labels
        glbl_z = Tex(r"z", font_size=38)
        glbl_z.scale(2.0); glbl_z.set_color(WHITE)
        glbl_z.next_to(sz_bg, RIGHT, buff=0.15).shift(DOWN * 0.60)

        glbl_r = Tex(r"r", font_size=38)
        glbl_r.scale(2.0); glbl_r.set_color(WHITE)
        glbl_r.next_to(sr_bg, LEFT, buff=0.15).shift(DOWN * 0.60)

        glbl_a = Tex(r"\tilde{a}", font_size=38)
        glbl_a.scale(2.0); glbl_a.set_color(WHITE)
        glbl_a.next_to(cand_bg, RIGHT, buff=0.15).shift(DOWN * 0.50)

        # Concat dot
        CONC_P = np.array([X_MID, BUS_Y, 0])
        conc_dot = Circle(radius=0.12)
        conc_dot.set_fill(WHITE, opacity=1.0)
        conc_dot.set_stroke(WHITE, width=2.0)
        conc_dot.move_to(CONC_P)

        # Branch dot on a-stream where a_{t-1} drops down (purple)
        a_branch_dot = Circle(radius=0.12)
        a_branch_dot.set_fill(G_AT_PURPLE, opacity=1.0)
        a_branch_dot.set_stroke(G_AT_PURPLE, width=2.0)
        a_branch_dot.move_to(BRANCH_PT)
        a_branch_dot.z_index = 1

        # Junction dot at rmul level where branch splits to × circle (purple)
        a_junc_dot = Circle(radius=0.10)
        a_junc_dot.set_fill(G_AT_PURPLE, opacity=1.0)
        a_junc_dot.set_stroke(G_AT_PURPLE, width=2.0)
        a_junc_dot.move_to(JUNC_RMUL_PT)
        a_junc_dot.z_index = 1

        # Merge dot where a_{t-1} meets x_t
        merge_dot = Circle(radius=0.12)
        merge_dot.set_fill(WHITE, opacity=1.0)
        merge_dot.set_stroke(WHITE, width=2.0)
        merge_dot.move_to(MERGE_PT)
        merge_dot.z_index = 1

        # Bus
        BUS_P_L = np.array([X_LEFT, BUS_Y, 0])
        BUS_P_R = np.array([X_RIGHT, BUS_Y, 0])

        # ── Outside elements ────────────────────────────────────────────
        def purp_rect(pos, w, tex_str):
            bx = RoundedRectangle(width=w, height=0.90, corner_radius=0.18)
            bx.set_fill(G_A_FILL, opacity=1.0)
            bx.set_stroke(G_A_STK, width=3.0)
            bx.move_to(pos)
            lb = Tex(tex_str, font_size=44)
            lb.set_color(WHITE); lb.scale(1.50); lb.move_to(pos)
            return VGroup(bx, lb)

        ain_node  = purp_rect(np.array([-8.00, A_Y, 0]), 2.10, r"a_{t-1}")
        aout_node = purp_rect(np.array([ 8.00, A_Y, 0]), 1.70, r"a_t")

        xt_circ = Circle(radius=0.55)
        xt_circ.set_fill(G_XT, opacity=0.97)
        xt_circ.set_stroke(WHITE, width=5.5)
        xt_circ.move_to(np.array([X_MID, -4.50, 0]))
        xt_lbl = Tex(r"x_t", font_size=50)
        xt_lbl.set_color(BLACK); xt_lbl.scale(1.50)
        xt_lbl.move_to(xt_circ.get_center())
        xt_node = VGroup(xt_circ, xt_lbl)

        YHAT_X = 5.50
        yhat_circ = Circle(radius=0.50)
        yhat_circ.set_fill(G_YHAT, opacity=0.97)
        yhat_circ.set_stroke(WHITE, width=5.0)
        yhat_circ.move_to(np.array([YHAT_X, -4.50, 0]))
        yhat_lbl = Tex(r"\hat{y}", font_size=44)
        yhat_lbl.set_color(BLACK); yhat_lbl.scale(1.30)
        yhat_lbl.move_to(yhat_circ.get_center())
        yhat_node = VGroup(yhat_circ, yhat_lbl)

        # Branch point on a-stream for ŷ output
        YHAT_BRANCH = np.array([YHAT_X, A_Y, 0])
        yhat_branch = Circle(radius=0.10)
        yhat_branch.set_fill(G_ASTR, opacity=1.0)
        yhat_branch.set_stroke(G_ASTR, width=2.0)
        yhat_branch.move_to(YHAT_BRANCH)
        yhat_branch.z_index = 1

        # ══════════════════════════════════════════════════════════════════
        #  LINES — all straight, center-to-center, z_index=-1
        # ══════════════════════════════════════════════════════════════════

        # a-stream top: a_{t-1} → ×(1-z) → + → a_t  (parallel, zmul feeds from below)
        l_a1 = ln(ain_node.get_center(), keep_bg.get_center(), G_AT_PURPLE)
        l_a2 = ln(keep_bg.get_center(), add_bg.get_center(), WHITE)
        l_a3 = ln(add_bg.get_center(), aout_node.get_center(), WHITE)

        # zmul → + (feeds into add from below — parallel path)
        l_zmul_add = ln(zmul_bg.get_center(), add_bg.get_center(), "#2ECC71")

        # Branch down from a-stream to ŷ
        l_branch_yhat = ln(YHAT_BRANCH, yhat_node.get_center(), G_YHAT)

        # z gate → ×(1-z) (straight up)
        l_z_keep = ln(sz_bg.get_center(), keep_bg.get_center(), G_SIG)

        # z gate → ×(z) (straight diagonal)
        l_z_zmul = ln(sz_bg.get_center(), zmul_bg.get_center(), G_SIG)

        # r gate → ×(r) (straight diagonal)
        l_r_rmul = ln(sr_bg.get_center(), rmul_bg.get_center(), G_SIG)

        # ×(r) → tanh candidate (straight up)
        l_rmul_cand = ln(rmul_bg.get_center(), cand_bg.get_center(), G_TANH_FILL)

        # tanh candidate → ×(z) (straight up)
        l_cand_zmul = ln(cand_bg.get_center(), zmul_bg.get_center(), G_TANH_FILL)

        # a_{t-1} branch seg1: down from a-stream to junction at rmul Y (PURPLE)
        l_at_down = ln(BRANCH_PT, JUNC_RMUL_PT, G_AT_PURPLE, sw=3.5)
        # a_{t-1} branch seg2: side branch right to rmul × circle (PURPLE)
        l_at_right_rmul = ln(JUNC_RMUL_PT, rmul_bg.get_center(), G_AT_PURPLE, sw=3.5)
        # a_{t-1} branch seg3: continue down from junction past z label to merge Y (PURPLE)
        l_at_down2 = ln(JUNC_RMUL_PT, np.array([BRANCH_X, MERGE_Y, 0]), G_AT_PURPLE, sw=3.5)
        # a_{t-1} branch seg4: right to meet x_t input line (PURPLE)
        l_at_right_merge = ln(np.array([BRANCH_X, MERGE_Y, 0]), MERGE_PT, G_AT_PURPLE, sw=3.5)

        # Input: x_t → merge point
        l_xin = ln(xt_node.get_center(), MERGE_PT, G_XT)

        # Input x_t direct to tanh candidate (blue, from merge point)
        l_xt_cand = ln(MERGE_PT, cand_bg.get_center(), G_ASTR, sw=3.5)

        # Merge → concat (white — combined [a_{t-1}, x_t])
        l_merge_conc = ln(MERGE_PT, CONC_P, WHITE)

        # Bus: horizontal
        l_bus = ln(BUS_P_L, BUS_P_R, WHITE, sw=3.75)

        # Bus center → ×(r)
        l_bus_rmul = ln(CONC_P, rmul_bg.get_center(), WHITE, sw=3.0)

        # ══════════════════════════════════════════════════════════════════
        #  PHASE 1 — Grow all shapes
        # ══════════════════════════════════════════════════════════════════
        self.play(GrowFromCenter(cell_box), run_time=0.55)
        self.play(
            GrowFromCenter(ain_node),
            GrowFromCenter(aout_node),
            GrowFromCenter(xt_node),
            GrowFromCenter(yhat_node),
            run_time=0.50,
        )
        self.play(
            GrowFromCenter(keep_node),
            GrowFromCenter(add_node),
            GrowFromCenter(zmul_node),
            GrowFromCenter(sz_node),
            GrowFromCenter(sr_node),
            GrowFromCenter(cand_node),
            GrowFromCenter(rmul_node),
            GrowFromCenter(conc_dot),
            GrowFromCenter(yhat_branch),
            GrowFromCenter(a_branch_dot),
            GrowFromCenter(a_junc_dot),
            GrowFromCenter(merge_dot),
            run_time=0.60,
        )
        self.play(
            FadeIn(glbl_z), FadeIn(glbl_r), FadeIn(glbl_a),
            run_time=0.30,
        )
        self.wait(0.20)

        # ══════════════════════════════════════════════════════════════════
        #  PHASE 2 — Draw all lines
        # ══════════════════════════════════════════════════════════════════
        self.play(
            ShowCreation(l_a1), ShowCreation(l_a2),
            ShowCreation(l_a3),
            run_time=0.50,
        )
        self.play(ShowCreation(l_xin), ShowCreation(l_merge_conc), run_time=0.35)
        self.play(
            ShowCreation(l_at_down), ShowCreation(l_at_down2),
            run_time=0.40,
        )
        self.play(
            ShowCreation(l_at_right_rmul), ShowCreation(l_at_right_merge),
            run_time=0.35,
        )
        self.play(ShowCreation(l_bus), run_time=0.40)
        self.play(
            ShowCreation(l_z_keep), ShowCreation(l_z_zmul),
            run_time=0.45,
        )
        self.play(
            ShowCreation(l_r_rmul), ShowCreation(l_bus_rmul),
            run_time=0.45,
        )
        self.play(
            ShowCreation(l_rmul_cand),
            ShowCreation(l_xt_cand),
            ShowCreation(l_cand_zmul),
            ShowCreation(l_zmul_add),
            run_time=0.50,
        )
        self.play(ShowCreation(l_branch_yhat), run_time=0.35)
        self.wait(0.30)

        # ══════════════════════════════════════════════════════════════════
        #  PHASE 3 — Pulse pass with math equations
        # ══════════════════════════════════════════════════════════════════

        # Input concat: a_{t-1} drops down left column, then right to merge (purple)
        run_p(BRANCH_PT, JUNC_RMUL_PT, G_AT_PUR_BRIGHT, rt=0.20)
        run_p(JUNC_RMUL_PT, np.array([BRANCH_X, MERGE_Y, 0]), G_AT_PUR_BRIGHT, rt=0.20)
        run_p(np.array([BRANCH_X, MERGE_Y, 0]), MERGE_PT, G_AT_PUR_BRIGHT, rt=0.15)
        run_p(xt_node.get_center(), MERGE_PT, G_XT_BRIGHT, rt=0.25)
        run_p(MERGE_PT, CONC_P, WHITE, rt=0.20)
        show_desc(r"[a_{t-1},\, x_t]")
        self.wait(2.0)

        # Update gate z (pulse along bus to z gate)
        run_p(CONC_P, sz_node.get_center(), WHITE, rt=0.35)
        self.play(Indicate(sz_node, color=WHITE, scale_factor=1.10), run_time=0.22)
        show_desc(r"z_t = \sigma(W_z \cdot [a_{t-1},\, x_t] + b_z)")
        self.wait(2.0)

        # Reset gate r (pulse along bus to r gate)
        run_p(CONC_P, sr_node.get_center(), WHITE, rt=0.35)
        self.play(Indicate(sr_node, color=WHITE, scale_factor=1.10), run_time=0.22)
        show_desc(r"r_t = \sigma(W_r \cdot [a_{t-1},\, x_t] + b_r)")
        self.wait(2.0)

        # r ⊙ a_{t-1} (a_{t-1} reaches rmul via purple junction branch)
        run_p(sr_node.get_center(), rmul_node.get_center(), G_SIG_BRIGHT, rt=0.25)
        run_p(BRANCH_PT, JUNC_RMUL_PT, G_AT_PUR_BRIGHT, rt=0.20)
        run_p(JUNC_RMUL_PT, rmul_node.get_center(), G_AT_PUR_BRIGHT, rt=0.20)
        self.play(Indicate(rmul_node, color=WHITE, scale_factor=1.12), run_time=0.22)
        show_desc(r"r_t \odot a_{t-1}")
        self.wait(2.0)

        # Candidate ã (r⊙a_{t-1} from rmul + x_t from merge both feed tanh)
        run_p(rmul_node.get_center(), cand_node.get_center(), G_TANH_BRIGHT, rt=0.30)
        run_p(MERGE_PT, cand_node.get_center(), G_ASTR_BRIGHT, rt=0.30)
        self.play(Indicate(cand_node, color=WHITE, scale_factor=1.10), run_time=0.22)
        show_desc(r"\tilde{a}_t = \tanh(W \cdot [r_t \odot a_{t-1},\, x_t] + b)")
        self.wait(2.0)

        # z ⊙ ã
        run_p(sz_node.get_center(), zmul_node.get_center(), G_SIG_BRIGHT, rt=0.25)
        run_p(cand_node.get_center(), zmul_node.get_center(), G_TANH_BRIGHT, rt=0.25)
        self.play(Indicate(zmul_node, color=WHITE, scale_factor=1.12), run_time=0.22)
        show_desc(r"z_t \odot \tilde{a}_t")
        self.wait(2.0)

        # (1-z) ⊙ a_{t-1}
        run_p(ain_node.get_center(), keep_node.get_center(), G_ASTR_BRIGHT, rt=0.40)
        run_p(sz_node.get_center(), keep_node.get_center(), G_SIG_BRIGHT, rt=0.25)
        self.play(Indicate(keep_node, color=WHITE, scale_factor=1.12), run_time=0.22)
        show_desc(r"(1 - z_t) \odot a_{t-1}")
        self.wait(2.0)

        # a_t = (1-z)a_{t-1} + z ã_t
        run_p(keep_node.get_center(), add_node.get_center(), G_ASTR_BRIGHT, rt=0.25)
        run_p(zmul_node.get_center(), add_node.get_center(), G_ASTR_BRIGHT, rt=0.25)
        self.play(Indicate(add_node, color=WHITE, scale_factor=1.12), run_time=0.22)
        show_desc(r"a_t = (1-z_t) \odot a_{t-1} + z_t \odot \tilde{a}_t")
        self.wait(2.0)

        # Output ŷ (branch from a-stream down)
        run_p(add_node.get_center(), YHAT_BRANCH, G_ASTR_BRIGHT, rt=0.25)
        run_p(YHAT_BRANCH, yhat_node.get_center(), G_YHAT_BRIGHT, rt=0.35)
        show_desc(r"\hat{y}_t")
        self.wait(2.0)

        clear_desc()
        self.wait(0.50)

        validate_layout(self, label="GRUCell", camera_scale=1.50)

        # ══════════════════════════════════════════════════════════════════
        # PHASE 4 -- Unrolled GRU chain: sentiment analysis
        # ══════════════════════════════════════════════════════════════════
        all_p3 = [
            cell_box,
            ain_node, aout_node, xt_node, yhat_node,
            keep_node, add_node, zmul_node,
            sz_node, sr_node, cand_node, rmul_node, conc_dot,
            glbl_z, glbl_r, glbl_a,
            l_a1, l_a2, l_a3,
            l_zmul_add,
            l_xin, l_xt_cand, l_merge_conc, l_bus,
            l_z_keep, l_z_zmul,
            l_r_rmul, l_bus_rmul,
            l_at_down, l_at_right_rmul, l_at_down2, l_at_right_merge,
            l_rmul_cand, l_cand_zmul,
            l_branch_yhat, yhat_branch,
            a_branch_dot, a_junc_dot, merge_dot,
        ]
        self.play(
            *[FadeOut(m) for m in all_p3],
            self.camera.frame.animate.scale(1.80).move_to(RIGHT * 0.6),
            run_time=0.50,
        )
        self.wait(0.30)

        GOLD = "#FFD700"
        CB   = "#1F77B4"
        HT   = "#1ABC9C"
        WC   = "#A8DADC"
        CA   = "#FF7F0E"

        def arr6(a, b, col, sw=2.5, bf=0.08):
            ar = Arrow(a, b, buff=bf, stroke_width=sw,
                       max_tip_length_to_length_ratio=0.14)
            ar.set_color(col)
            return ar

        # -- Sentence at top --
        sentence6 = Text("The movie was long but the ending was really great",
                         font_size=56)
        sentence6.set_color(WHITE)
        sentence6.scale(1.5)
        sentence6.move_to(np.array([0.0, 5.5, 0]))
        self.play(Write(sentence6), run_time=0.70)
        self.wait(2.0)

        # -- 10 simplified GRU cells --
        words6 = ["The", "movie", "was", "long", "but", "the",
                   "ending", "was", "really", "great"]
        T6 = len(words6)
        SP6 = 2.8
        HX6 = [-(T6 - 1) * SP6 / 2 + i * SP6 - 0.99 for i in range(T6)]
        Y_CELL6 = 0.0
        Y_WORD6 = -2.8

        cells6 = []
        for i in range(T6):
            r6 = RoundedRectangle(width=2.0, height=1.4, corner_radius=0.18)
            r6.set_fill(CB, opacity=0.15)
            r6.set_stroke(CB, width=2.5)
            r6.move_to(np.array([HX6[i], Y_CELL6, 0]))
            lb6 = Text("GRU", font_size=48, weight="BOLD")
            lb6.set_color(CB)
            lb6.move_to(r6.get_center())
            cells6.append(VGroup(r6, lb6))

        # -- Hidden state arrows (no cell state — key GRU difference) --
        h0_6c = Circle(radius=0.55)
        h0_6c.set_fill("#8E44AD", 0.40)
        h0_6c.set_stroke("#8E44AD", 2.0)
        h0_6c.move_to(np.array([HX6[0] - SP6 * 0.85, Y_CELL6, 0]))
        h0_6l = Tex(r"a_0", font_size=48)
        h0_6l.set_color(WHITE)
        h0_6l.move_to(h0_6c.get_center())
        h0_6g = VGroup(h0_6c, h0_6l)

        harr6_0 = arr6(h0_6g.get_right(), cells6[0][0].get_left(), HT, sw=3.0)
        harrs6 = [arr6(cells6[i][0].get_right(), cells6[i + 1][0].get_left(),
                       HT, sw=3.0)
                  for i in range(T6 - 1)]

        # -- Word labels + input arrows --
        wlbls6 = []
        xarrs6 = []
        for i in range(T6):
            wl6 = Text(words6[i], font_size=52, weight="BOLD")
            wl6.set_color(WC)
            wl6.move_to(np.array([HX6[i], Y_WORD6, 0]))
            wlbls6.append(wl6)
            xarrs6.append(arr6(wl6.get_top() + UP * 0.20,
                               cells6[i][0].get_bottom(),
                               WC, sw=2.5))

        # -- Prediction slot --
        pred6 = Text("?", font_size=56, weight="BOLD")
        pred6.set_color(CA)
        pred6.scale(1.4)
        pred6.move_to(np.array([HX6[-1] + SP6 * 0.55, Y_CELL6, 0]))
        pred6.shift(RIGHT * 0.96)
        pred_arr6 = arr6(cells6[-1][0].get_right(), pred6.get_left(),
                         CA, sw=3.0)

        # === Build entire diagram — left-to-right sweep in 2 seconds ===
        build_anims = [FadeIn(h0_6g), GrowArrow(harr6_0)]
        for i in range(T6):
            build_anims.append(FadeIn(cells6[i]))
            build_anims.append(FadeIn(wlbls6[i]))
            build_anims.append(GrowArrow(xarrs6[i]))
            if i < T6 - 1:
                build_anims.append(GrowArrow(harrs6[i]))
        build_anims.append(FadeIn(pred6))
        build_anims.append(GrowArrow(pred_arr6))
        self.play(LaggedStart(*build_anims, lag_ratio=0.04, run_time=2.0))
        self.wait(1.0)

        # === Left-to-right processing sweep ===
        process_anims = []
        for i in range(T6):
            process_anims.append(Indicate(cells6[i], color=WHITE, scale_factor=1.08))
        self.play(LaggedStart(*process_anims, lag_ratio=0.12, run_time=2.0))

        # Final word "great" — sentiment highlight
        great_msg = Text(
            "Hidden state captures full sentiment!",
            font_size=58, weight="BOLD",
        )
        great_msg.set_color("#2ECC71")
        great_msg.move_to(np.array([0.0, 3.8, 0]))
        self.play(
            Indicate(cells6[-1], color="#2ECC71", scale_factor=1.25),
            run_time=0.65,
        )
        self.play(FadeIn(great_msg, shift=UP * 0.15), run_time=0.40)
        self.wait(2.0)
        self.play(FadeOut(great_msg), run_time=0.30)

        # === Prediction reveal ===
        pos6 = Text("Positive!", font_size=64, weight="BOLD")
        pos6.set_color("#2ECC71")
        pos6.next_to(pred_arr6, RIGHT, buff=0.25)
        self.play(FadeOut(pred6), Write(pos6), run_time=0.55)
        self.play(
            Indicate(pos6, color=WHITE, scale_factor=1.30),
            run_time=0.80,
        )
        self.wait(2.0)

        # === Takeaway message ===
        msg6a = Text("GRU: Simpler than LSTM, often similar performance!",
                     font_size=76, weight="BOLD")
        msg6a.set_color(CB)
        msg6a.move_to(np.array([0.0, -5.8, 0]))
        self.play(Write(msg6a), run_time=0.65)
        self.wait(2.0)

        validate_layout(self, label="GRUCell_P4_CHAIN", camera_scale=2.70)


# ============================================================
# TopicOverview — curriculum table of contents
# ============================================================
class TopicOverview(InteractiveScene):
    def construct(self):

        self.camera.frame.scale(1.65)

        TOPICS = [
            "What is sequence data?",
            "Why ANNs fail?",
            "Recurrent neural networks",
            "RNN types",
            "Back propagation through time",
            "Vanishing gradients",
            "Long short-term memory",
            "Gated Recurrent Unit",
            "Bidirectional RNNs",
            "Deep RNNs",
        ]
        BULLET = "\u2022"
        FONT  = 52
        V_BUFF = 0.55

        # Build rows: each is a VGroup(bullet, label)
        rows = VGroup()
        for topic in TOPICS:
            bul = Text(BULLET, font_size=FONT, color=WHITE)
            lbl = Text(topic,  font_size=FONT, color=WHITE)
            row = VGroup(bul, lbl).arrange(RIGHT, buff=0.30)
            rows.add(row)

        rows.arrange(DOWN, buff=V_BUFF, aligned_edge=LEFT)
        rows.move_to(ORIGIN)

        # Fade in all rows at once
        self.play(LaggedStart(
            *[FadeIn(r, shift=RIGHT * 0.15) for r in rows],
            lag_ratio=0.12,
            run_time=2.0,
        ))
        self.wait(0.5)

        # Highlight rectangle — starts matching first row
        rect = RoundedRectangle(
            corner_radius=0.18,
            width=rows[0].get_width() * 1.10 + 0.55,
            height=rows[0].get_height() * 1.10 + 0.28,
        )
        rect.set_fill(YELLOW, opacity=0.12)
        rect.set_stroke(YELLOW, width=2.5, opacity=0.75)
        rect.move_to(rows[0])
        self.play(FadeIn(rect), run_time=0.40)
        self.wait(0.60)

        # Walk through each topic
        for row in rows[1:]:
            target_rect = RoundedRectangle(
                corner_radius=0.18,
                width=row.get_width() * 1.10 + 0.55,
                height=row.get_height() * 1.10 + 0.28,
            )
            target_rect.set_fill(YELLOW, opacity=0.12)
            target_rect.set_stroke(YELLOW, width=2.5, opacity=0.75)
            target_rect.move_to(row)
            self.play(Transform(rect, target_rect), run_time=0.50)
            self.wait(0.55)

        self.wait(1.5)



class InputNotation(InteractiveScene):
    """Show x^{<t>} notation and that words are converted to vectors."""

    def construct(self):
        self.camera.frame.scale(1.30).shift(DOWN * 0.80)

        C_Y  = "#F4D03F"
        C_C  = "#5DADE2"
        C_P  = "#7D3C98"
        C_G  = "#2ECC71"
        C_O  = "#FF7F0E"

        # ═══════════════════════════════════════════════════════════════
        #  PART 1 — Angle-bracket superscript notation (no arrows)
        # ═══════════════════════════════════════════════════════════════
        notations = [
            (r"x^{\langle t \rangle}",       "Input at time step  t",        C_C),
            (r"x^{\langle t-1 \rangle}",     "Input at previous time step",  C_C),
            (r"a^{\langle t \rangle}",       "Activation at time step  t",   C_P),
            (r"a^{\langle t-1 \rangle}",     "Activation at previous step",  C_P),
            (r"\hat{y}^{\langle t \rangle}", "Predicted output at time  t",  C_O),
        ]

        rows = []
        for idx, (tex_s, desc_s, col) in enumerate(notations):
            y = 2.40 - idx * 1.20

            sym = Tex(tex_s, font_size=64)
            sym.set_color(col)
            sym.move_to(np.array([-3.20 - 0.77, y, 0]))

            desc = Text(desc_s, font_size=38)
            desc.set_color(WHITE)
            desc.move_to(np.array([2.20 - 0.77, y, 0]))

            grp = VGroup(sym, desc)
            rows.append(grp)

        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15)
                                for r in rows],
                              lag_ratio=0.15, run_time=1.50))
        self.wait(3.0)

        note = Text("The angle bracket just means \"at time step t\"",
                     font_size=40, weight="BOLD")
        note.set_color(C_G)
        note.move_to(DOWN * 3.97)
        self.play(FadeIn(note, shift=UP * 0.10), run_time=0.40)
        self.wait(2.0)

        # ═══════════════════════════════════════════════════════════════
        #  PART 2 — Words are converted to vectors
        #  Keep sentence visible, show split words below it
        # ═══════════════════════════════════════════════════════════════
        self.play(*[FadeOut(m) for m in [note, *rows]], run_time=0.40)

        # Show a sentence
        sentence = Text("I love this movie", font_size=56)
        sentence.set_color(WHITE)
        sentence.move_to(UP * 3.20)
        self.play(Write(sentence), run_time=0.55)
        self.wait(1.5)

        # Split into words — shown BELOW sentence (sentence stays)
        words = ["I", "love", "this", "movie"]
        NW = len(words)
        SP = 3.80
        wx = [-(NW - 1) * SP / 2 + i * SP for i in range(NW)]
        Y_W = 1.40

        wlbls = []
        for i, w in enumerate(words):
            t = Text(w, font_size=52, weight="BOLD")
            t.set_color(C_C)
            t.move_to(np.array([wx[i], Y_W, 0]))
            wlbls.append(t)

        self.play(LaggedStart(*[FadeIn(w, shift=DOWN * 0.15)
                                for w in wlbls],
                              lag_ratio=0.12, run_time=0.80))
        self.wait(1.0)

        # Arrows down to vectors
        Y_VEC = -1.80
        arrows = []
        vecs = []
        for i in range(NW):
            ar = Arrow(
                np.array([wx[i], Y_W - 0.50, 0]),
                np.array([wx[i], Y_VEC + 1.60, 0]),
                buff=0.08, stroke_width=3.0,
                max_tip_length_to_length_ratio=0.18,
            )
            ar.set_color(C_O)
            arrows.append(ar)

            # Column vector with more vertical spacing
            vals = [
                [0.23, -0.81, 0.55, 0.12],
                [-0.42, 0.67, 0.03, -0.91],
                [0.78, -0.15, 0.44, 0.60],
                [0.31, 0.92, -0.56, 0.17],
            ]
            col_strs = [f"{v:.2f}" for v in vals[i]]
            vec_txt = Tex(
                r"\begin{bmatrix}"
                + r"\\[6pt]".join(col_strs)
                + r"\end{bmatrix}",
                font_size=38,
            )
            vec_txt.set_color(C_G)
            vec_txt.move_to(np.array([wx[i], Y_VEC, 0]))
            vecs.append(vec_txt)

        self.play(LaggedStart(*[GrowArrow(a) for a in arrows],
                              lag_ratio=0.10, run_time=0.70))
        self.play(LaggedStart(*[FadeIn(v, shift=DOWN * 0.10)
                                for v in vecs],
                              lag_ratio=0.10, run_time=0.80))
        self.wait(2.0)

        # Labels using x^{<t>} notation
        lbl_x = []
        for i in range(NW):
            xl = Tex(
                r"x^{\langle " + str(i + 1) + r" \rangle}",
                font_size=96,
            )
            xl.set_color(C_C)
            xl.next_to(vecs[i], DOWN, buff=0.55)
            lbl_x.append(xl)

        self.play(LaggedStart(*[FadeIn(l) for l in lbl_x],
                              lag_ratio=0.10, run_time=0.60))
        self.wait(3.0)

        validate_layout(self, label="InputNotation", camera_scale=1.30)


class ExpandNotation(InteractiveScene):
    """Show compact gate equation, then expand it — text only, no matrices."""

    def construct(self):
        self.camera.frame.scale(1.14)

        C_Y   = "#F4D03F"
        C_SIG = "#FF7F0E"
        C_W   = "#5DADE2"
        C_A   = "#7D3C98"
        C_X   = "#2ECC71"
        C_B   = "#E74C3C"

        # ═══════════════════════════════════════════════════════════════
        #  STEP 1 — Show compact form
        # ═══════════════════════════════════════════════════════════════
        compact = Tex(
            r"f_t = \sigma(W_f \cdot [a_{t-1},\, x_t] + b_f)",
            font_size=72,
        )
        compact.set_color(WHITE)
        compact.move_to(UP * 2.50)
        self.play(Write(compact), run_time=0.80)
        self.wait(2.5)

        # ═══════════════════════════════════════════════════════════════
        #  STEP 2 — Explain [ , ] in text
        # ═══════════════════════════════════════════════════════════════
        explain1 = Tex(r"[a_{t-1},\, x_t]", font_size=64)
        explain1.set_color(C_Y)
        explain1.move_to(np.array([-3.50, 0.60, 0])).shift(LEFT*1.96)

        means = Text("means concatenate the two vectors", font_size=40)
        means.set_color(GREY_B)
        means.next_to(explain1, RIGHT, buff=0.40)

        self.play(FadeIn(explain1), FadeIn(means), run_time=0.45)
        self.wait(2.0)

        # ═══════════════════════════════════════════════════════════════
        #  STEP 3 — Show expanded form
        # ═══════════════════════════════════════════════════════════════
        expand_label = Text("Expanded, this becomes:", font_size=42, weight="BOLD")
        expand_label.set_color(GREY_B)
        expand_label.move_to(DOWN * 0.60)
        self.play(FadeIn(expand_label), run_time=0.30)
        self.wait(0.8)

        expanded = Tex(
            r"f_t = \sigma("
            r"W_{fa} \cdot a_{t-1}"
            r" + "
            r"W_{fx} \cdot x_t"
            r" + b_f)",
            font_size=68,
        )
        expanded.set_color(WHITE)
        expanded.move_to(DOWN * 2.00)
        self.play(Write(expanded), run_time=0.80)
        self.wait(3.0)

        validate_layout(self, label="ExpandNotation", camera_scale=1.30)



