"""
AIが万能ではないことを解説するアニメーション

LLMのハルシネーション（もっともらしい嘘）や
画像生成AIの失敗例（手の描写など）を視覚的に表現します。

使用方法:
    manim -pql ai_limitations_animation.py AILimitations
    manim -pqh ai_limitations_animation.py AILimitations  # 高画質
"""

from manim import *


def bilingual_text(jp_text, en_text, jp_size=28, en_size=18, jp_color=WHITE, en_color=GRAY):
    """日英併記のテキストを作成（英語はサブで小さめ）"""
    jp = Text(jp_text, font_size=jp_size, color=jp_color)
    en = Text(en_text, font_size=en_size, color=en_color)
    en.next_to(jp, DOWN, buff=0.1)
    return VGroup(jp, en)


class AILimitations(Scene):
    """AIが万能ではないことを解説するアニメーション"""

    def construct(self):
        # タイトル
        self.show_title()

        # AIの得意・苦手を比較
        self.show_strengths_weaknesses()

        # LLMのハルシネーション例
        self.show_llm_hallucination()

        # 画像生成AIの失敗例
        self.show_image_ai_failure()

        # まとめ
        self.show_conclusion()

    def show_title(self):
        """タイトルを表示"""
        title = bilingual_text(
            "AIは万能ではない",
            "AI is Not Omnipotent",
            jp_size=48,
            en_size=28,
        )
        subtitle = bilingual_text(
            "賢いけど、限界もある",
            "Smart, but has limitations",
            jp_size=32,
            en_size=20,
            jp_color=YELLOW,
            en_color=YELLOW_D,
        )
        subtitle.next_to(title, DOWN, buff=0.5)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle))

    def show_strengths_weaknesses(self):
        """AIの得意・苦手を表示"""
        # セクションタイトル
        section_title = bilingual_text(
            "AIの得意・苦手",
            "Strengths & Weaknesses",
            jp_size=36,
            en_size=22,
        )
        section_title.to_edge(UP)
        self.play(Write(section_title))

        # 得意なこと（左側）
        strengths_title = bilingual_text(
            "得意",
            "Strengths",
            jp_size=28,
            en_size=18,
            jp_color=GREEN,
            en_color=GREEN_D,
        )
        strengths_items = VGroup(
            bilingual_text("• パターン認識", "Pattern recognition", jp_size=20, en_size=14),
            bilingual_text("• 大量データ処理", "Processing big data", jp_size=20, en_size=14),
            bilingual_text("• 高速な推論", "Fast inference", jp_size=20, en_size=14),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)

        strengths_box = VGroup(
            RoundedRectangle(
                width=5.5, height=4.5, corner_radius=0.2, color=GREEN, fill_opacity=0.1
            ),
        )
        strengths_title.move_to(strengths_box.get_top() + DOWN * 0.5)
        strengths_items.next_to(strengths_title, DOWN, buff=0.3)
        strengths_group = VGroup(strengths_box, strengths_title, strengths_items)
        strengths_group.move_to(LEFT * 3.2 + DOWN * 0.4)

        # 苦手なこと（右側）
        weaknesses_title = bilingual_text(
            "苦手",
            "Weaknesses",
            jp_size=28,
            en_size=18,
            jp_color=RED,
            en_color=RED_D,
        )
        weaknesses_items = VGroup(
            bilingual_text("• 未知の状況", "Novel situations", jp_size=20, en_size=14),
            bilingual_text("• 論理的な推論", "Logical reasoning", jp_size=20, en_size=14),
            bilingual_text("• 常識的判断", "Common sense", jp_size=20, en_size=14),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)

        weaknesses_box = VGroup(
            RoundedRectangle(
                width=5.5, height=4.5, corner_radius=0.2, color=RED, fill_opacity=0.1
            ),
        )
        weaknesses_title.move_to(weaknesses_box.get_top() + DOWN * 0.5)
        weaknesses_items.next_to(weaknesses_title, DOWN, buff=0.3)
        weaknesses_group = VGroup(weaknesses_box, weaknesses_title, weaknesses_items)
        weaknesses_group.move_to(RIGHT * 3.2 + DOWN * 0.4)

        # アニメーション
        self.play(FadeIn(strengths_group))
        self.wait(0.5)
        self.play(FadeIn(weaknesses_group))
        self.wait(1.5)

        # 注釈
        note = bilingual_text(
            "学習したパターンの外は苦手",
            "Struggles outside learned patterns",
            jp_size=24,
            en_size=16,
            jp_color=GRAY,
            en_color=GRAY_D,
        )
        note.to_edge(DOWN, buff=0.6)
        self.play(Write(note))
        self.wait(1)

        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def show_llm_hallucination(self):
        """LLMのハルシネーション（もっともらしい嘘）を表示"""
        # セクションタイトル
        section_title = bilingual_text(
            "例1: LLMのハルシネーション",
            "Example 1: LLM Hallucination",
            jp_size=32,
            en_size=20,
            jp_color=BLUE,
            en_color=BLUE_D,
        )
        section_title.to_edge(UP)
        self.play(Write(section_title))

        # ユーザーの質問
        user_bubble = VGroup(
            RoundedRectangle(
                width=6, height=1.2, corner_radius=0.2, color=BLUE, fill_opacity=0.2
            ),
            bilingual_text(
                "東京タワーは何メートル？",
                "How tall is Tokyo Tower?",
                jp_size=22,
                en_size=14,
            ),
        )
        user_bubble.move_to(UP * 1.2 + LEFT * 1)

        user_icon = VGroup(
            Circle(radius=0.3, color=BLUE, fill_opacity=0.5),
            Text("U", font_size=20, color=WHITE),
        )
        user_icon.next_to(user_bubble, LEFT, buff=0.3)

        self.play(FadeIn(user_icon), FadeIn(user_bubble))
        self.wait(0.5)

        # AIの回答（正しい）
        ai_answer = bilingual_text(
            "333メートルです",
            "It's 333 meters",
            jp_size=22,
            en_size=14,
            jp_color=GREEN,
            en_color=GREEN_D,
        )
        ai_bubble_correct = VGroup(
            RoundedRectangle(
                width=5, height=1.2, corner_radius=0.2, color=GREEN, fill_opacity=0.2
            ),
            ai_answer,
        )
        ai_bubble_correct.move_to(DOWN * 0.5 + RIGHT * 1.5)

        ai_icon = VGroup(
            Circle(radius=0.3, color=GREEN, fill_opacity=0.5),
            Text("AI", font_size=16, color=WHITE),
        )
        ai_icon.next_to(ai_bubble_correct, RIGHT, buff=0.3)

        self.play(FadeIn(ai_icon), FadeIn(ai_bubble_correct))

        # チェックマーク
        check = bilingual_text(
            "✓ 正解！",
            "Correct!",
            jp_size=20,
            en_size=14,
            jp_color=GREEN,
            en_color=GREEN_D,
        )
        check.next_to(ai_bubble_correct, DOWN, buff=0.2)
        self.play(FadeIn(check))
        self.wait(1)

        # クリーンアップして次へ
        self.play(
            FadeOut(user_bubble),
            FadeOut(user_icon),
            FadeOut(ai_bubble_correct),
            FadeOut(ai_icon),
            FadeOut(check),
        )

        # 新しい質問（架空の情報）
        user_q2 = bilingual_text(
            "「虹色の塔」という本の著者は？",
            'Who wrote "Rainbow Tower"?',
            jp_size=20,
            en_size=13,
        )
        user_bubble2 = VGroup(
            RoundedRectangle(
                width=6.5, height=1.3, corner_radius=0.2, color=BLUE, fill_opacity=0.2
            ),
            user_q2,
        )
        user_bubble2.move_to(UP * 1.2 + LEFT * 0.8)

        user_icon2 = VGroup(
            Circle(radius=0.3, color=BLUE, fill_opacity=0.5),
            Text("U", font_size=20, color=WHITE),
        )
        user_icon2.next_to(user_bubble2, LEFT, buff=0.3)

        self.play(FadeIn(user_icon2), FadeIn(user_bubble2))
        self.wait(0.5)

        # AIの回答（ハルシネーション）
        ai_wrong = VGroup(
            bilingual_text(
                "山田太郎氏の代表作です",
                "A masterpiece by Taro Yamada",
                jp_size=20,
                en_size=13,
            ),
            bilingual_text(
                "1985年に出版されました",
                "Published in 1985",
                jp_size=18,
                en_size=12,
                jp_color=GRAY,
                en_color=GRAY_D,
            ),
        ).arrange(DOWN, buff=0.15)

        ai_bubble_wrong = VGroup(
            RoundedRectangle(
                width=6.5, height=1.8, corner_radius=0.2, color=RED, fill_opacity=0.2
            ),
            ai_wrong,
        )
        ai_bubble_wrong.move_to(DOWN * 0.8 + RIGHT * 1)

        ai_icon2 = VGroup(
            Circle(radius=0.3, color=GREEN, fill_opacity=0.5),
            Text("AI", font_size=16, color=WHITE),
        )
        ai_icon2.next_to(ai_bubble_wrong, RIGHT, buff=0.3)

        self.play(FadeIn(ai_icon2), FadeIn(ai_bubble_wrong))

        # 警告マーク
        warning = VGroup(
            bilingual_text(
                "⚠️ 実在しない本！",
                "This book doesn't exist!",
                jp_size=22,
                en_size=14,
                jp_color=RED,
                en_color=RED_D,
            ),
            bilingual_text(
                "もっともらしく嘘をつく",
                "Confidently makes things up",
                jp_size=18,
                en_size=12,
                jp_color=YELLOW,
                en_color=YELLOW_D,
            ),
        ).arrange(DOWN, buff=0.15)
        warning.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(warning, scale=1.2))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def show_image_ai_failure(self):
        """画像生成AIの失敗例を表示"""
        # セクションタイトル
        section_title = bilingual_text(
            "例2: 画像生成AIの失敗",
            "Example 2: Image AI Failure",
            jp_size=32,
            en_size=20,
            jp_color=PURPLE,
            en_color=PURPLE_D,
        )
        section_title.to_edge(UP)
        self.play(Write(section_title))

        # プロンプト
        prompt_text = bilingual_text(
            "プロンプト: 「ラーメンを食べる人」",
            'Prompt: "A person eating ramen"',
            jp_size=22,
            en_size=14,
        )
        prompt_box = VGroup(
            RoundedRectangle(
                width=8, height=1.3, corner_radius=0.2, color=WHITE, fill_opacity=0.1
            ),
            prompt_text,
        )
        prompt_box.shift(UP * 1.3)
        self.play(FadeIn(prompt_box))

        # 生成中のアニメーション
        generating = bilingual_text(
            "生成中...",
            "Generating...",
            jp_size=24,
            en_size=16,
            jp_color=GRAY,
            en_color=GRAY_D,
        )
        generating.shift(DOWN * 0.2)
        self.play(Write(generating))

        # ドットアニメーション
        for _ in range(2):
            for i in range(3):
                dots = "." * (i + 1)
                new_jp = Text(f"生成中{dots}", font_size=24, color=GRAY)
                new_en = Text(f"Generating{dots}", font_size=16, color=GRAY_D)
                new_en.next_to(new_jp, DOWN, buff=0.1)
                new_text = VGroup(new_jp, new_en)
                new_text.shift(DOWN * 0.2)
                self.remove(generating)
                generating = new_text
                self.add(generating)
                self.wait(0.3)

        self.play(FadeOut(generating))

        # 結果フレーム
        result_frame = Rectangle(width=5, height=3.5, color=GRAY, fill_opacity=0.05)
        result_frame.shift(DOWN * 0.8)

        # 人物のシルエット（簡略化）
        person = VGroup(
            Circle(radius=0.4, color=WHITE, fill_opacity=0.3).shift(UP * 0.8),  # 頭
            Ellipse(width=1.5, height=1.8, color=WHITE, fill_opacity=0.3).shift(
                DOWN * 0.5
            ),  # 体
        )
        person.move_to(result_frame.get_center())

        # ラーメン丼
        bowl = VGroup(
            Arc(radius=0.8, angle=PI, color=ORANGE, fill_opacity=0.3).shift(DOWN * 1.2),
            Line(LEFT * 0.8, RIGHT * 0.8, color=ORANGE).shift(DOWN * 1.2),
        )
        bowl.move_to(result_frame.get_center() + DOWN * 0.5)

        # 問題の手（6本指風）
        hand = VGroup()
        for i in range(6):  # 6本の指
            finger = Line(ORIGIN, UP * 0.3, color=WHITE, stroke_width=3)
            finger.rotate(PI / 6 * (i - 2.5))
            finger.shift(LEFT * 0.3 + DOWN * 0.3)
            hand.add(finger)
        hand.move_to(result_frame.get_center() + LEFT * 0.8)

        self.play(FadeIn(result_frame), FadeIn(person), FadeIn(bowl))
        self.play(FadeIn(hand))

        # 問題箇所を強調
        problem_circle = Circle(radius=0.6, color=RED, stroke_width=3)
        problem_circle.move_to(hand.get_center())

        problem_label = VGroup(
            bilingual_text(
                "指が6本!?",
                "6 fingers!?",
                jp_size=22,
                en_size=14,
                jp_color=RED,
                en_color=RED_D,
            ),
            bilingual_text(
                "手掴みでラーメン!?",
                "Eating with bare hands!?",
                jp_size=20,
                en_size=13,
                jp_color=YELLOW,
                en_color=YELLOW_D,
            ),
        ).arrange(DOWN, buff=0.15)
        problem_label.next_to(problem_circle, RIGHT, buff=0.5)

        self.play(Create(problem_circle), FadeIn(problem_label))
        self.wait(1)

        # 説明
        explanation = VGroup(
            bilingual_text(
                "画像AIは「見た目」を学習",
                "Image AI learns appearances",
                jp_size=22,
                en_size=14,
            ),
            bilingual_text(
                "物理的な正しさは理解していない",
                "Doesn't understand physical correctness",
                jp_size=20,
                en_size=13,
                jp_color=GRAY,
                en_color=GRAY_D,
            ),
        ).arrange(DOWN, buff=0.2)
        explanation.to_edge(DOWN, buff=0.4)

        self.play(Write(explanation))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def show_conclusion(self):
        """まとめを表示"""
        # タイトル
        title = bilingual_text(
            "AIとの付き合い方",
            "How to Work with AI",
            jp_size=40,
            en_size=24,
            jp_color=YELLOW,
            en_color=YELLOW_D,
        )
        title.to_edge(UP, buff=0.7)
        self.play(Write(title))

        # ポイント
        points = VGroup(
            VGroup(
                Text("✓", font_size=28, color=GREEN),
                bilingual_text(
                    "AIは賢くて便利",
                    "AI is smart and useful",
                    jp_size=26,
                    en_size=16,
                ),
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("✓", font_size=28, color=GREEN),
                bilingual_text(
                    "でも万能ではない",
                    "But not omnipotent",
                    jp_size=26,
                    en_size=16,
                ),
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("✓", font_size=28, color=GREEN),
                bilingual_text(
                    "限界を理解して使う",
                    "Understand its limitations",
                    jp_size=26,
                    en_size=16,
                ),
            ).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        points.move_to(ORIGIN)

        for point in points:
            self.play(FadeIn(point, shift=RIGHT * 0.3))
            self.wait(0.5)

        self.wait(1)

        # 最後のメッセージ
        final_message = bilingual_text(
            "天気予報AIも同じ",
            "Weather AI is the same",
            jp_size=32,
            en_size=20,
            jp_color=BLUE,
            en_color=BLUE_D,
        )
        final_message.to_edge(DOWN, buff=0.8)

        box = SurroundingRectangle(final_message, color=BLUE, buff=0.2)

        self.play(Write(final_message), Create(box))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])


class AILimitationsShort(Scene):
    """AIの限界（短縮版）"""

    def construct(self):
        title = bilingual_text(
            "AIは万能ではない",
            "AI is Not Omnipotent",
            jp_size=44,
            en_size=26,
        )
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.scale(0.7).to_edge(UP))

        # 2つの例を並べて表示
        # LLMの例
        llm_example = VGroup(
            bilingual_text("LLM", "Large Language Model", jp_size=24, en_size=14, jp_color=BLUE, en_color=BLUE_D),
            bilingual_text("もっともらしい嘘", "Plausible lies", jp_size=20, en_size=13, jp_color=RED, en_color=RED_D),
        ).arrange(DOWN, buff=0.3)
        llm_example.move_to(LEFT * 3 + UP * 0.3)

        # 画像AIの例
        image_example = VGroup(
            bilingual_text("画像生成AI", "Image Gen AI", jp_size=24, en_size=14, jp_color=PURPLE, en_color=PURPLE_D),
            bilingual_text("手掴みでラーメン", "Eating ramen by hand", jp_size=20, en_size=13, jp_color=RED, en_color=RED_D),
        ).arrange(DOWN, buff=0.3)
        image_example.move_to(RIGHT * 3 + UP * 0.3)

        self.play(FadeIn(llm_example), FadeIn(image_example))
        self.wait(1)

        # 共通点
        common = bilingual_text(
            "学習したパターンの外は苦手",
            "Struggles outside learned patterns",
            jp_size=24,
            en_size=15,
            jp_color=YELLOW,
            en_color=YELLOW_D,
        )
        common.shift(DOWN * 1.2)
        self.play(Write(common))
        self.wait(0.5)

        # 結論
        conclusion = VGroup(
            bilingual_text(
                "賢いけど限界もある",
                "Smart, but has limits",
                jp_size=28,
                en_size=17,
            ),
            bilingual_text(
                "→ だから人間の判断が大切",
                "→ Human judgment matters",
                jp_size=24,
                en_size=15,
                jp_color=GREEN,
                en_color=GREEN_D,
            ),
        ).arrange(DOWN, buff=0.35)
        conclusion.to_edge(DOWN, buff=0.6)

        self.play(Write(conclusion))
        self.wait(2)


if __name__ == "__main__":
    # コマンドラインから実行する場合の例
    # manim -pql ai_limitations_animation.py AILimitations
    # manim -pql ai_limitations_animation.py AILimitationsShort
    pass
