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
