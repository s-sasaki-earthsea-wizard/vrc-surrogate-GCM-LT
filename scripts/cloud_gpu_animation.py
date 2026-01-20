"""
クラウドGPU活用の概念図アニメーション

ローカルPCでは厳しい高性能GPU処理を、
クラウドGPUで時間課金で借りて実行する流れを可視化します。

対応箇所: yt_script.md L294-298

使用方法:
    manim -pql cloud_gpu_animation.py CloudGPU
    manim -pqh cloud_gpu_animation.py CloudGPU  # 高画質
"""

from manim import *


class CloudGPU(Scene):
    """クラウドGPU活用の概念図アニメーション"""

    def construct(self):
        # タイトル
        self.show_title()

        # ローカルPCの限界
        self.show_local_pc_limitation()

        # クラウドGPUへの接続
        self.show_cloud_connection()

        # 時間課金のメリット
        self.show_hourly_billing()

        # まとめ
        self.show_summary()

    def show_title(self):
        """タイトルを表示"""
        title = Text("クラウドGPUを借りる", font_size=48)
        subtitle = Text("高性能GPUを時間単位でレンタル", font_size=32, color=BLUE)
        subtitle.next_to(title, DOWN)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

    def create_pc_icon(self, label_text, scale=1.0):
        """PCアイコンを作成"""
        # モニター
        monitor = Rectangle(
            width=1.6 * scale,
            height=1.0 * scale,
            color=WHITE,
            fill_opacity=0.1,
        )
        # 画面（内側）
        screen = Rectangle(
            width=1.4 * scale,
            height=0.8 * scale,
            color=BLUE_D,
            fill_opacity=0.3,
        )
        # スタンド
        stand = Rectangle(
            width=0.2 * scale,
            height=0.3 * scale,
            color=WHITE,
            fill_opacity=0.1,
        )
        stand.next_to(monitor, DOWN, buff=0)
        # ベース
        base = Rectangle(
            width=0.6 * scale,
            height=0.08 * scale,
            color=WHITE,
            fill_opacity=0.1,
        )
        base.next_to(stand, DOWN, buff=0)

        pc = VGroup(monitor, screen, stand, base)

        # ラベル
        label = Text(label_text, font_size=20 * scale)
        label.next_to(pc, DOWN, buff=0.3 * scale)

        return VGroup(pc, label)

    def create_server_icon(self, label_text, scale=1.0, color=GREEN):
        """サーバー/GPUアイコンを作成"""
        # サーバーラック風の箱
        box = Rectangle(
            width=1.4 * scale,
            height=1.8 * scale,
            color=color,
            fill_opacity=0.2,
        )
        # インジケーターライト
        lights = VGroup()
        for i in range(3):
            light = Dot(
                radius=0.06 * scale,
                color=GREEN_A,
            )
            light.move_to(box.get_left() + RIGHT * 0.2 * scale + DOWN * (0.4 - 0.4 * i) * scale)
            lights.add(light)

        # スロット線
        slots = VGroup()
        for i in range(3):
            slot = Line(
                LEFT * 0.4 * scale,
                RIGHT * 0.4 * scale,
                color=color,
                stroke_width=2,
            )
            slot.move_to(box.get_center() + DOWN * (0.4 - 0.4 * i) * scale)
            slots.add(slot)

        server = VGroup(box, lights, slots)

        # ラベル
        label = Text(label_text, font_size=20 * scale)
        label.next_to(server, DOWN, buff=0.3 * scale)

        return VGroup(server, label)

    def create_cloud_shape(self, scale=1.0, color=BLUE):
        """雲の形を作成"""
        # 複数の円を組み合わせて雲を作る
        circles = VGroup(
            Circle(radius=0.5 * scale, color=color, fill_opacity=0.2),
            Circle(radius=0.4 * scale, color=color, fill_opacity=0.2).shift(
                LEFT * 0.4 * scale + DOWN * 0.1 * scale
            ),
            Circle(radius=0.35 * scale, color=color, fill_opacity=0.2).shift(
                RIGHT * 0.45 * scale + DOWN * 0.05 * scale
            ),
            Circle(radius=0.3 * scale, color=color, fill_opacity=0.2).shift(
                LEFT * 0.7 * scale + DOWN * 0.15 * scale
            ),
            Circle(radius=0.25 * scale, color=color, fill_opacity=0.2).shift(
                RIGHT * 0.7 * scale + DOWN * 0.1 * scale
            ),
        )
        return circles

    def show_local_pc_limitation(self):
        """ローカルPCの限界を表示"""
        title = Text("自分のパソコンだと...", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # PCアイコン
        pc = self.create_pc_icon("普通のGPU", scale=1.2)
        pc.move_to(ORIGIN)

        self.play(FadeIn(pc, shift=UP))
        self.wait(0.5)

        # 困った顔（？マーク）
        question = Text("？", font_size=60, color=YELLOW)
        question.next_to(pc, UP, buff=0.3)
        self.play(Write(question))

        # 問題点を表示
        problem_text = Text(
            "最先端のAIモデルを動かすには\nちょっと厳しい...",
            font_size=28,
            color=RED_C,
        )
        problem_text.next_to(pc, RIGHT, buff=1.0)

        self.play(Write(problem_text))
        self.wait(1.5)

        # 保存して次のシーンへ
        self.local_pc = pc
        self.question = question
        self.play(
            FadeOut(problem_text),
            FadeOut(title),
        )

    def show_cloud_connection(self):
        """クラウドGPUへの接続を表示"""
        title = Text("クラウドGPUという選択肢", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # ローカルPCを左に移動
        self.play(
            self.local_pc.animate.shift(LEFT * 4),
            self.question.animate.shift(LEFT * 4),
        )

        # 雲を作成
        cloud = self.create_cloud_shape(scale=1.5, color=BLUE)
        cloud.move_to(ORIGIN + UP * 0.5)
        cloud_label = Text("クラウド", font_size=24, color=BLUE)
        cloud_label.next_to(cloud, UP, buff=0.2)

        self.play(FadeIn(cloud, shift=DOWN), Write(cloud_label))

        # クラウドGPU（右側）
        gpu_server = self.create_server_icon("高性能GPU\n(A100)", scale=1.2, color=GREEN)
        gpu_server.move_to(RIGHT * 4)

        self.play(FadeIn(gpu_server, shift=UP))

        # 接続矢印（PC → クラウド）
        arrow1 = Arrow(
            self.local_pc.get_right() + RIGHT * 0.2,
            cloud.get_left() + LEFT * 0.1,
            color=YELLOW,
            buff=0.1,
        )
        # 接続矢印（クラウド → GPU）
        arrow2 = Arrow(
            cloud.get_right() + RIGHT * 0.1,
            gpu_server.get_left() + LEFT * 0.2,
            color=YELLOW,
            buff=0.1,
        )

        self.play(Create(arrow1), Create(arrow2))

        # 「インターネット」ラベル
        internet_label = Text("インターネット", font_size=20, color=GRAY)
        internet_label.next_to(arrow1, UP, buff=0.1)

        self.play(Write(internet_label))

        # ？を笑顔（チェックマーク）に変更
        checkmark = Text("✓", font_size=50, color=GREEN)
        checkmark.move_to(self.question.get_center())

        self.play(
            Transform(self.question, checkmark),
        )

        self.wait(1)

        # 保存
        self.cloud = cloud
        self.cloud_label = cloud_label
        self.gpu_server = gpu_server
        self.arrow1 = arrow1
        self.arrow2 = arrow2
        self.internet_label = internet_label
        self.title = title

    def show_hourly_billing(self):
        """時間課金のメリットを表示"""
        self.play(FadeOut(self.title))

        title = Text("必要なときだけ、必要な分だけ", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # 時計アイコン（円）
        clock_circle = Circle(radius=0.4, color=WHITE, stroke_width=2)
        clock_hand_h = Line(ORIGIN, UP * 0.2, color=WHITE, stroke_width=3)
        clock_hand_m = Line(ORIGIN, UP * 0.35 + RIGHT * 0.1, color=WHITE, stroke_width=2)
        clock = VGroup(clock_circle, clock_hand_h, clock_hand_m)
        clock.move_to(DOWN * 2 + LEFT * 2)

        # コインアイコン
        coin = Circle(radius=0.35, color=YELLOW, fill_opacity=0.3, stroke_width=2)
        coin_text = Text("$", font_size=28, color=YELLOW)
        coin_icon = VGroup(coin, coin_text)
        coin_icon.move_to(DOWN * 2 + RIGHT * 2)

        self.play(Create(clock), FadeIn(coin_icon))

        # 説明テキスト
        billing_text = VGroup(
            Text("時間単位で課金", font_size=28),
            Text("使った分だけ支払い", font_size=24, color=GRAY),
        ).arrange(DOWN, buff=0.2)
        billing_text.move_to(DOWN * 2)

        self.play(Write(billing_text))
        self.wait(1.5)

        self.clock = clock
        self.coin_icon = coin_icon
        self.billing_text = billing_text
        self.section_title = title

    def show_summary(self):
        """まとめを表示"""
        # 既存要素をフェードアウト
        self.play(
            FadeOut(self.local_pc),
            FadeOut(self.question),
            FadeOut(self.cloud),
            FadeOut(self.cloud_label),
            FadeOut(self.gpu_server),
            FadeOut(self.arrow1),
            FadeOut(self.arrow2),
            FadeOut(self.internet_label),
            FadeOut(self.clock),
            FadeOut(self.coin_icon),
            FadeOut(self.billing_text),
            FadeOut(self.section_title),
        )

        # まとめテキスト
        summary = VGroup(
            Text("クラウドGPUなら", font_size=40),
            Text("高価な機材を買わなくても", font_size=32, color=BLUE),
            Text("最先端のAIを試せる", font_size=32, color=GREEN),
        ).arrange(DOWN, buff=0.4)

        self.play(Write(summary[0]))
        self.play(FadeIn(summary[1], shift=UP))
        self.play(FadeIn(summary[2], shift=UP))

        self.wait(2)
        self.play(FadeOut(summary))
