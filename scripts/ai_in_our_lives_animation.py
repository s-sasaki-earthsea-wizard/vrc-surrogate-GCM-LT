"""
AIと私たちの生活の関わりを解説するアニメーション

科学研究へのAI技術の取り入れ方を考える必要性と、
天気予報AIが私たちの生活に密着した重要な例であることを視覚的に表現します。

使用方法:
    manim -pql ai_in_our_lives_animation.py AIInOurLives
    manim -pqh ai_in_our_lives_animation.py AIInOurLives  # 高画質
"""

from manim import *
import numpy as np


def bilingual_text(jp_text, en_text, jp_size=28, en_size=18, jp_color=WHITE, en_color=GRAY):
    """日英併記のテキストを作成（英語はサブで小さめ）"""
    jp = Text(jp_text, font_size=jp_size, color=jp_color)
    en = Text(en_text, font_size=en_size, color=en_color)
    en.next_to(jp, DOWN, buff=0.1)
    return VGroup(jp, en)


class AIInOurLives(Scene):
    """AIと私たちの生活の関わりを解説するアニメーション"""

    def construct(self):
        # タイトル
        self.show_title()

        # 関係者のつながり
        self.show_stakeholders()

        # 天気予報AIと日常生活
        self.show_weather_ai_in_daily_life()

        # まとめ
        self.show_conclusion()

    def show_title(self):
        """タイトルを表示"""
        title = bilingual_text(
            "AIと科学研究の未来",
            "The Future of AI in Science",
            jp_size=48,
            en_size=28,
        )
        subtitle = bilingual_text(
            "みんなで考える時代へ",
            "A Time for Collective Thinking",
            jp_size=32,
            en_size=20,
            jp_color=BLUE,
            en_color=BLUE_D,
        )
        subtitle.next_to(title, DOWN, buff=0.5)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle))

    def create_person_icon(self, label_jp, label_en, color, icon_char="👤"):
        """人物アイコンを作成"""
        circle = Circle(radius=0.5, color=color, fill_opacity=0.3)
        icon = Text(icon_char, font_size=32)
        icon.move_to(circle.get_center())
        label = bilingual_text(label_jp, label_en, jp_size=18, en_size=12, jp_color=color, en_color=color)
        label.next_to(circle, DOWN, buff=0.2)
        return VGroup(circle, icon, label)

    def show_stakeholders(self):
        """関係者のつながりを表示"""
        # セクションタイトル
        section_title = bilingual_text(
            "AIをどう取り入れるか",
            "How to Integrate AI",
            jp_size=36,
            en_size=22,
        )
        section_title.to_edge(UP)
        self.play(Write(section_title))

        # 中心のAI
        ai_box = VGroup(
            RoundedRectangle(
                width=2, height=1.5, corner_radius=0.2, color=YELLOW, fill_opacity=0.3
            ),
            bilingual_text("AI", "Artificial Intelligence", jp_size=28, en_size=12, jp_color=YELLOW, en_color=YELLOW_D),
        )
        ai_box.move_to(ORIGIN)

        self.play(FadeIn(ai_box))

        # 関係者を配置（三角形）
        # 研究者
        researcher = self.create_person_icon("研究者", "Researchers", BLUE, "🔬")
        researcher.move_to(UP * 2 + LEFT * 2.5)

        # 技術者
        engineer = self.create_person_icon("技術者", "Engineers", GREEN, "💻")
        engineer.move_to(UP * 2 + RIGHT * 2.5)

        # 利用者（私たち）
        user = self.create_person_icon("私たち", "Users (Us)", ORANGE, "👥")
        user.move_to(DOWN * 2)

        # 一人ずつ登場
        self.play(FadeIn(researcher, shift=DOWN))
        self.wait(0.3)
        self.play(FadeIn(engineer, shift=DOWN))
        self.wait(0.3)
        self.play(FadeIn(user, shift=UP))

        # つながりの矢印（双方向）
        arrows = VGroup()

        # 研究者 ↔ AI
        arrow1 = DoubleArrow(
            researcher[0].get_center() + DOWN * 0.5 + RIGHT * 0.3,
            ai_box.get_center() + UP * 0.5 + LEFT * 0.5,
            color=BLUE_C,
            buff=0.2,
            stroke_width=3,
        )
        arrows.add(arrow1)

        # 技術者 ↔ AI
        arrow2 = DoubleArrow(
            engineer[0].get_center() + DOWN * 0.5 + LEFT * 0.3,
            ai_box.get_center() + UP * 0.5 + RIGHT * 0.5,
            color=GREEN_C,
            buff=0.2,
            stroke_width=3,
        )
        arrows.add(arrow2)

        # 利用者 ↔ AI
        arrow3 = DoubleArrow(
            user[0].get_center() + UP * 0.5,
            ai_box.get_center() + DOWN * 0.5,
            color=ORANGE,
            buff=0.2,
            stroke_width=3,
        )
        arrows.add(arrow3)

        # 関係者同士のつながり（点線）
        line1 = DashedLine(
            researcher[0].get_center() + RIGHT * 0.5,
            engineer[0].get_center() + LEFT * 0.5,
            color=GRAY,
            stroke_width=2,
        )
        line2 = DashedLine(
            researcher[0].get_center() + DOWN * 0.5 + RIGHT * 0.3,
            user[0].get_center() + UP * 0.3 + LEFT * 0.5,
            color=GRAY,
            stroke_width=2,
        )
        line3 = DashedLine(
            engineer[0].get_center() + DOWN * 0.5 + LEFT * 0.3,
            user[0].get_center() + UP * 0.3 + RIGHT * 0.5,
            color=GRAY,
            stroke_width=2,
        )

        self.play(
            *[Create(arrow) for arrow in arrows],
            Create(line1),
            Create(line2),
            Create(line3),
        )

        # メッセージ
        message = bilingual_text(
            "みんなで考える必要がある",
            "We all need to think together",
            jp_size=26,
            en_size=16,
            jp_color=WHITE,
            en_color=GRAY,
        )
        message.to_edge(DOWN, buff=0.5)

        box = SurroundingRectangle(message, color=WHITE, buff=0.15)
        self.play(Write(message), Create(box))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def show_weather_ai_in_daily_life(self):
        """天気予報AIと日常生活の関わりを表示"""
        # セクションタイトル
        section_title = bilingual_text(
            "天気予報AIと私たちの生活",
            "Weather AI in Our Daily Lives",
            jp_size=36,
            en_size=22,
        )
        section_title.to_edge(UP)
        self.play(Write(section_title))

        # 中心に天気予報AI
        weather_ai = VGroup(
            Circle(radius=1, color=BLUE, fill_opacity=0.3),
            bilingual_text(
                "天気予報AI",
                "Weather AI",
                jp_size=22,
                en_size=14,
                jp_color=BLUE,
                en_color=BLUE_D,
            ),
        )
        weather_ai[1].move_to(weather_ai[0].get_center())
        weather_ai.move_to(ORIGIN)

        self.play(FadeIn(weather_ai))

        # 生活シーンを放射状に配置
        scenes = [
            ("☂️", "傘を持つ？", "Bring umbrella?", UP * 2.3, TEAL),
            ("👕", "服装は？", "What to wear?", UP * 1.5 + RIGHT * 2.2, PURPLE),
            ("🌾", "農作業", "Farming", RIGHT * 2.8, GREEN),
            ("✈️", "旅行計画", "Travel plans", DOWN * 1.5 + RIGHT * 2.2, ORANGE),
            ("⚠️", "災害対策", "Disaster prep", DOWN * 2.3, RED),
            ("🏃", "運動・外出", "Exercise", DOWN * 1.5 + LEFT * 2.2, YELLOW),
            ("🎪", "イベント", "Events", LEFT * 2.8, PINK),
            ("🏠", "洗濯物", "Laundry", UP * 1.5 + LEFT * 2.2, MAROON),
        ]

        scene_objects = VGroup()
        for icon, jp_label, en_label, position, color in scenes:
            scene_group = VGroup(
                Text(icon, font_size=36),
                bilingual_text(jp_label, en_label, jp_size=16, en_size=11, jp_color=color, en_color=color),
            )
            scene_group[1].next_to(scene_group[0], DOWN, buff=0.1)
            scene_group.move_to(position)
            scene_objects.add(scene_group)

        # 一つずつ登場
        for scene in scene_objects:
            self.play(FadeIn(scene, scale=0.8), run_time=0.3)

        # 天気予報AIから各シーンへの線
        lines = VGroup()
        for scene in scene_objects:
            line = Line(
                weather_ai[0].get_center(),
                scene.get_center(),
                color=BLUE_C,
                stroke_width=2,
                stroke_opacity=0.5,
            )
            lines.add(line)

        self.play(*[Create(line) for line in lines], run_time=0.8)

        # パルス効果（天気予報AIが情報を発信）
        for _ in range(2):
            pulse = Circle(radius=0.1, color=BLUE, fill_opacity=0.8)
            pulse.move_to(weather_ai[0].get_center())
            self.play(
                pulse.animate.scale(30).set_opacity(0),
                run_time=1,
            )

        # 強調メッセージ
        emphasis = bilingual_text(
            "生活に密着した重要な例",
            "A crucial example in our daily lives",
            jp_size=28,
            en_size=17,
            jp_color=YELLOW,
            en_color=YELLOW_D,
        )
        emphasis.to_edge(DOWN, buff=0.4)

        box = SurroundingRectangle(emphasis, color=YELLOW, buff=0.15)
        self.play(Write(emphasis), Create(box))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def show_conclusion(self):
        """まとめを表示"""
        # タイトル
        title = bilingual_text(
            "これからのAIと社会",
            "AI and Society Going Forward",
            jp_size=40,
            en_size=24,
            jp_color=WHITE,
            en_color=GRAY,
        )
        title.to_edge(UP, buff=0.8)
        self.play(Write(title))

        # ポイント
        points = VGroup(
            VGroup(
                Text("1", font_size=24, color=BLUE).set_opacity(0.8),
                bilingual_text(
                    "AIは科学研究を変えつつある",
                    "AI is transforming scientific research",
                    jp_size=24,
                    en_size=15,
                ),
            ).arrange(RIGHT, buff=0.4),
            VGroup(
                Text("2", font_size=24, color=GREEN).set_opacity(0.8),
                bilingual_text(
                    "天気予報AIは身近な例",
                    "Weather AI is a familiar example",
                    jp_size=24,
                    en_size=15,
                ),
            ).arrange(RIGHT, buff=0.4),
            VGroup(
                Text("3", font_size=24, color=ORANGE).set_opacity(0.8),
                bilingual_text(
                    "研究者も技術者も私たちも",
                    "Researchers, engineers, and us",
                    jp_size=24,
                    en_size=15,
                ),
            ).arrange(RIGHT, buff=0.4),
        ).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        points.move_to(ORIGIN + UP * 0.3)

        for point in points:
            self.play(FadeIn(point, shift=RIGHT * 0.3))
            self.wait(0.5)

        self.wait(0.5)

        # 最後のメッセージ
        final_message = bilingual_text(
            "一緒に考えていく時代",
            "An era of thinking together",
            jp_size=32,
            en_size=20,
            jp_color=YELLOW,
            en_color=YELLOW_D,
        )
        final_message.to_edge(DOWN, buff=0.8)

        box = SurroundingRectangle(final_message, color=YELLOW, buff=0.2)
        self.play(Write(final_message), Create(box))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])


class AIInOurLivesShort(Scene):
    """AIと生活の関わり（短縮版）"""

    def construct(self):
        title = bilingual_text(
            "天気予報AIと私たちの生活",
            "Weather AI in Our Daily Lives",
            jp_size=40,
            en_size=24,
        )
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.scale(0.7).to_edge(UP))

        # 中心に天気予報AI
        weather_ai = VGroup(
            Circle(radius=0.8, color=BLUE, fill_opacity=0.3),
            bilingual_text("天気予報AI", "Weather AI", jp_size=20, en_size=13, jp_color=BLUE, en_color=BLUE_D),
        )
        weather_ai[1].move_to(weather_ai[0].get_center())

        self.play(FadeIn(weather_ai))

        # 周囲に生活シーン
        icons = ["☂️", "👕", "🌾", "✈️", "⚠️", "🏃"]
        icon_objects = VGroup()
        for i, icon in enumerate(icons):
            angle = i * TAU / len(icons) - PI / 2
            pos = np.array([np.cos(angle) * 2.2, np.sin(angle) * 2.2, 0])
            icon_text = Text(icon, font_size=32)
            icon_text.move_to(pos)
            icon_objects.add(icon_text)

        self.play(*[FadeIn(icon, scale=0.8) for icon in icon_objects])

        # 線でつなぐ
        lines = VGroup()
        for icon in icon_objects:
            line = Line(
                weather_ai[0].get_center(),
                icon.get_center(),
                color=BLUE_C,
                stroke_width=2,
                stroke_opacity=0.5,
            )
            lines.add(line)

        self.play(*[Create(line) for line in lines], run_time=0.5)
        self.wait(0.5)

        # メッセージ
        message = bilingual_text(
            "生活に密着した重要な例",
            "A crucial example in our daily lives",
            jp_size=26,
            en_size=16,
            jp_color=YELLOW,
            en_color=YELLOW_D,
        )
        message.to_edge(DOWN, buff=0.8)

        self.play(Write(message))
        self.wait(0.5)

        # 結論
        conclusion = bilingual_text(
            "みんなで考える時代へ",
            "An era of thinking together",
            jp_size=28,
            en_size=17,
            jp_color=GREEN,
            en_color=GREEN_D,
        )
        conclusion.next_to(message, DOWN, buff=0.3)

        self.play(Write(conclusion))
        self.wait(2)


if __name__ == "__main__":
    # コマンドラインから実行する場合の例
    # manim -pql ai_in_our_lives_animation.py AIInOurLives
    # manim -pql ai_in_our_lives_animation.py AIInOurLivesShort
    pass
