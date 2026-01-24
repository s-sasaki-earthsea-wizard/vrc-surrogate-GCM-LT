"""
実行結果（時間とコスト）のアニメーション

天気予報AI実行にかかった時間とコストを表示します。

対応箇所: yt_script.md L315-316, L324

使用方法:
    manim -pql execution_result_animation.py ExecutionResult
    manim -pqh execution_result_animation.py ExecutionResult  # 高画質
"""

from manim import *


class ExecutionResult(Scene):
    """実行結果（時間とコスト）のアニメーション"""

    def construct(self):
        # タイトル
        self.show_title()

        # 実行時間
        self.show_execution_time()

        # コスト
        self.show_cost()

        # まとめ
        self.show_summary()

    def show_title(self):
        """タイトルを表示"""
        title = Text("実行結果", font_size=48)
        subtitle = Text("Execution Result", font_size=28, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.2)

        title_group = VGroup(title, subtitle)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)
        self.play(FadeOut(title_group))

    def create_clock_icon(self, scale=1.0):
        """時計アイコンを作成"""
        circle = Circle(radius=0.5 * scale, color=WHITE, stroke_width=3)
        # 時針
        hour_hand = Line(
            ORIGIN,
            UP * 0.25 * scale + RIGHT * 0.1 * scale,
            color=WHITE,
            stroke_width=4,
        )
        # 分針
        minute_hand = Line(
            ORIGIN,
            UP * 0.35 * scale,
            color=WHITE,
            stroke_width=3,
        )
        # 中心点
        center_dot = Dot(radius=0.04 * scale, color=WHITE)

        clock = VGroup(circle, hour_hand, minute_hand, center_dot)
        return clock

    def create_coin_icon(self, scale=1.0, text="$"):
        """コインアイコンを作成"""
        circle = Circle(
            radius=0.5 * scale,
            color=YELLOW,
            fill_opacity=0.3,
            stroke_width=3,
        )
        symbol = Text(text, font_size=36 * scale, color=YELLOW)
        coin = VGroup(circle, symbol)
        return coin

    def show_execution_time(self):
        """実行時間を表示"""
        # セクションタイトル
        section_title = Text("推論にかかった時間", font_size=36)
        section_title.to_edge(UP, buff=0.8)
        self.play(Write(section_title))

        # 時計アイコン
        clock = self.create_clock_icon(scale=1.5)
        clock.move_to(LEFT * 3)

        self.play(Create(clock))

        # 3日間の予報
        duration_label = Text("3日間の天気予報", font_size=32)
        duration_label_en = Text("3-day weather forecast", font_size=20, color=GRAY)
        duration_group = VGroup(duration_label, duration_label_en).arrange(DOWN, buff=0.1)
        duration_group.move_to(RIGHT * 1.5 + UP * 1)

        self.play(Write(duration_label))
        self.play(FadeIn(duration_label_en, shift=UP))

        # 矢印
        arrow = Arrow(
            duration_group.get_bottom() + DOWN * 0.2,
            duration_group.get_bottom() + DOWN * 1.2,
            color=YELLOW,
            buff=0.1,
        )
        self.play(Create(arrow))

        # 約35分（大きく表示）
        time_text = Text("約35分", font_size=56, color=GREEN)
        time_text_en = Text("About 35 minutes", font_size=28, color=GRAY)
        time_group = VGroup(time_text, time_text_en).arrange(DOWN, buff=0.15)
        time_group.next_to(arrow, DOWN, buff=0.3)

        self.play(Write(time_text))
        self.play(FadeIn(time_text_en, shift=UP))

        self.wait(1.5)

        # 保存して次へ
        self.play(
            FadeOut(section_title),
            FadeOut(clock),
            FadeOut(duration_group),
            FadeOut(arrow),
            FadeOut(time_group),
        )

    def show_cost(self):
        """コストを表示"""
        # セクションタイトル
        section_title = Text("かかったコスト", font_size=36)
        section_title.to_edge(UP, buff=0.8)
        self.play(Write(section_title))

        # コインアイコン（ドル）
        coin_dollar = self.create_coin_icon(scale=1.2, text="$")
        coin_dollar.move_to(LEFT * 4 + UP * 0.5)

        # コインアイコン（円）
        coin_yen = self.create_coin_icon(scale=1.2, text="¥")
        coin_yen[0].set_color(ORANGE)
        coin_yen[1].set_color(ORANGE)
        coin_yen.move_to(LEFT * 4 + DOWN * 1.5)

        self.play(FadeIn(coin_dollar, scale=0.5))

        # 約3ドル
        dollar_text = Text("約3ドル", font_size=48, color=GREEN)
        dollar_text_en = Text("About $3", font_size=28, color=GRAY)
        dollar_group = VGroup(dollar_text, dollar_text_en).arrange(DOWN, buff=0.1)
        dollar_group.move_to(RIGHT * 1 + UP * 0.5)

        self.play(Write(dollar_text))
        self.play(FadeIn(dollar_text_en, shift=UP))

        self.wait(0.5)

        # 円に変換
        self.play(FadeIn(coin_yen, scale=0.5))

        yen_text = Text("500円弱", font_size=48, color=ORANGE)
        yen_text_en = Text("Less than 500 yen", font_size=28, color=GRAY)
        yen_group = VGroup(yen_text, yen_text_en).arrange(DOWN, buff=0.1)
        yen_group.move_to(RIGHT * 1 + DOWN * 1.5)

        self.play(Write(yen_text))
        self.play(FadeIn(yen_text_en, shift=UP))

        self.wait(1.5)

        # 保存
        self.section_title = section_title
        self.coin_dollar = coin_dollar
        self.coin_yen = coin_yen
        self.dollar_group = dollar_group
        self.yen_group = yen_group

    def show_summary(self):
        """まとめを表示"""
        # 既存要素をフェードアウト
        self.play(
            FadeOut(self.section_title),
            FadeOut(self.coin_dollar),
            FadeOut(self.coin_yen),
            FadeOut(self.dollar_group),
            FadeOut(self.yen_group),
        )

        # ワンコインで天気予報
        summary_main = Text("ワンコインで天気予報", font_size=48, color=YELLOW)
        summary_en = Text("Weather forecast for just one coin", font_size=28, color=GRAY)
        summary_group = VGroup(summary_main, summary_en).arrange(DOWN, buff=0.2)

        # コインアイコンを追加
        coin = self.create_coin_icon(scale=0.8, text="¥")
        coin[0].set_color(ORANGE)
        coin[1].set_color(ORANGE)
        coin.next_to(summary_group, LEFT, buff=0.5)

        full_summary = VGroup(coin, summary_group)
        full_summary.move_to(ORIGIN)

        self.play(FadeIn(coin, scale=0.5))
        self.play(Write(summary_main))
        self.play(FadeIn(summary_en, shift=UP))

        self.wait(2)
        self.play(FadeOut(full_summary))
