"""
気象入力・予測データの日英併記リストアニメーション

天気予報AIに入力し、予測する気象データの種類を
日本語メイン、英語サブで表示します。

対応箇所: yt_script.md L309-311

使用方法:
    manim -pql weather_input_data_animation.py WeatherInputData
    manim -pqh weather_input_data_animation.py WeatherInputData  # 高画質
"""

from manim import *


class WeatherInputData(Scene):
    """気象入力・予測データの日英併記リストアニメーション"""

    def construct(self):
        # タイトル
        self.show_title()

        # 入力・予測データのリスト
        self.show_input_output_data()

        # まとめ
        self.show_summary()

    def show_title(self):
        """タイトルを表示"""
        title = Text("入力・予測データ", font_size=48)
        subtitle = Text("Input & Prediction Data", font_size=28, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.2)

        title_group = VGroup(title, subtitle)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)
        self.play(FadeOut(title_group))

    def create_bilingual_item(self, japanese, english, icon_color=BLUE):
        """日英併記のアイテムを作成"""
        # アイコン（丸いドット）
        icon = Dot(radius=0.15, color=icon_color, fill_opacity=0.8)

        # 日本語テキスト（メイン、大きめ）
        jp_text = Text(japanese, font_size=36)

        # 英語テキスト（サブ、小さめ、グレー）
        en_text = Text(english, font_size=22, color=GRAY)
        en_text.next_to(jp_text, DOWN, buff=0.1, aligned_edge=LEFT)

        # テキストグループ
        text_group = VGroup(jp_text, en_text)
        text_group.next_to(icon, RIGHT, buff=0.3)

        # 全体グループ
        item = VGroup(icon, text_group)

        return item

    def show_input_output_data(self):
        """入力・予測データを表示"""
        # セクションタイトル（入力して予測する）
        section_title = Text("入力して予測するデータ", font_size=40)
        section_subtitle = Text("Input & Predict", font_size=24, color=GRAY)
        section_subtitle.next_to(section_title, DOWN, buff=0.15)
        section_group = VGroup(section_title, section_subtitle)
        section_group.to_edge(UP, buff=0.6)

        self.play(Write(section_title))
        self.play(FadeIn(section_subtitle, shift=UP))

        # 気象データのリスト（日本語メイン、英語サブ）
        weather_data = [
            ("気温", "Temperature", RED_C),
            ("風速", "Wind Speed", TEAL_C),
            ("気圧", "Pressure", BLUE_C),
            ("降水量", "Precipitation", GREEN_C),
        ]

        # アイテムを作成
        items = VGroup()
        for japanese, english, color in weather_data:
            item = self.create_bilingual_item(japanese, english, color)
            items.add(item)

        # 縦に並べる
        items.arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        items.move_to(ORIGIN + DOWN * 0.3)

        # 各アイテムを順番にアニメーション表示
        for i, item in enumerate(items):
            icon = item[0]
            text_group = item[1]

            # アイコンをフェードイン、テキストをWrite
            self.play(
                FadeIn(icon, scale=0.5),
                Write(text_group[0]),  # 日本語
                run_time=0.6,
            )
            self.play(
                FadeIn(text_group[1], shift=UP * 0.1),  # 英語
                run_time=0.3,
            )

        self.wait(1.5)

        # 保存
        self.section_group = section_group
        self.items = items

    def show_summary(self):
        """まとめを表示"""
        # 既存要素をフェードアウト
        self.play(
            FadeOut(self.section_group),
            FadeOut(self.items),
        )

        # まとめテキスト（6時間後を予測、繰り返して60時間後）
        summary = VGroup(
            Text("6時間後を予測", font_size=40),
            Text("Predict 6 hours ahead", font_size=24, color=GRAY),
        ).arrange(DOWN, buff=0.15)

        arrow = Text("↓ 繰り返し", font_size=32, color=YELLOW)
        arrow_en = Text("Repeat", font_size=20, color=GRAY)
        arrow_group = VGroup(arrow, arrow_en).arrange(DOWN, buff=0.1)

        result = VGroup(
            Text("60時間後まで予測", font_size=40, color=BLUE),
            Text("Predict up to 60 hours", font_size=24, color=GRAY),
        ).arrange(DOWN, buff=0.15)

        full_summary = VGroup(summary, arrow_group, result).arrange(DOWN, buff=0.5)

        self.play(Write(summary[0]))
        self.play(FadeIn(summary[1], shift=UP))
        self.wait(0.5)

        self.play(FadeIn(arrow_group, shift=DOWN))
        self.wait(0.5)

        self.play(Write(result[0]))
        self.play(FadeIn(result[1], shift=UP))

        self.wait(2)
        self.play(FadeOut(full_summary))
