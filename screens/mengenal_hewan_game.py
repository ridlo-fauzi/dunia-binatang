from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
from kivy.graphics import Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import ButtonBehavior

class ClickableImage(ButtonBehavior, Image):
    pass

class MengenalHewanGame(Screen):
    def on_enter(self):
        """Mematikan backsound saat masuk ke screen ini."""
        app = App.get_running_app()
        app.stop_music()  


    def on_leave(self):
        """Memulai kembali backsound saat meninggalkan screen ini.""" 
        app = App.get_running_app()
        app.start_background_music()  
    
    def __init__(self, **kwargs):
        super(MengenalHewanGame, self).__init__(**kwargs)

        with self.canvas.before:
                self.bg_image = Image(source='./assets/img/game1/mengenalHewan.png', allow_stretch=True, keep_ratio=False)
                self.rect = Rectangle(texture=self.bg_image.texture, size=self.size, pos=self.pos)
                self.bind(size=self._update_rect, pos=self._update_rect)


        layout = FloatLayout()

        back_button = ClickableImage(size_hint=(None, None), size=(100, 80),
                        pos_hint={'x': 0, 'top': 1},
                        source='assets/img/back.png')
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        scroll_view = ScrollView(size_hint=(0.9, 0.75), pos_hint={'center_x': 0.5, 'center_y': 0.55})

        image_grid = GridLayout(cols=2, padding=20, spacing=20, size_hint_y=None)
        image_grid.bind(minimum_height=image_grid.setter('height'))

        self.sounds = {}
        gambar_dan_suara = [
            ('assets/img/hewan/jerapah.png', 'assets/music/soundNamaHewan/jerapah.mp3'),
            ('assets/img/hewan/lumba-lumba.png', 'assets/music/soundNamaHewan/lumba-lumba.mp3'),
            ('assets/img/hewan/kucing.png', 'assets/music/soundNamaHewan/kucing.mp3'),
            ('assets/img/hewan/sapi.png', 'assets/music/soundNamaHewan/sapi.mp3'),
            ('assets/img/hewan/semut.png', 'assets/music/soundNamaHewan/laba-laba.mp3'),
            ('assets/img/hewan/tupai.png', 'assets/music/soundNamaHewan/tupai.mp3'),
            ('assets/img/hewan/harimau.png', 'assets/music/soundNamaHewan/harimau.mp3'),
            ('assets/img/hewan/kelinci.png', 'assets/music/soundNamaHewan/kelinci.mp3'),
            ('assets/img/hewan/ayam.png', 'assets/music/soundNamaHewan/ayam.mp3'),
            ('assets/img/hewan/buaya.png', 'assets/music/soundNamaHewan/buaya.mp3'),
            ('assets/img/hewan/rusa.png', 'assets/music/soundNamaHewan/rusa.mp3'),
            ('assets/img/hewan/kuda.png', 'assets/music/soundNamaHewan/kuda.mp3')
        ]

        for gambar, suara in gambar_dan_suara:
            img_button = ClickableImage(size_hint=(None, None), size=(200, 200),  
                                source=gambar)
            img_button.bind(on_press=self.create_sound_callback(suara))
            image_grid.add_widget(img_button)

            self.sounds[suara] = SoundLoader.load(suara)

        scroll_view.add_widget(image_grid)

        layout.add_widget(scroll_view)

        self.add_widget(layout)

    def go_back(self, instance):
        """Fungsi untuk kembali ke menu game."""
        app = App.get_running_app()
        self.manager.current = 'menu_game'

    def create_sound_callback(self, sound_file):
        """Membuat callback khusus untuk setiap suara hewan."""
        def play_sound_callback(instance):
            """Memutar suara ketika gambar hewan ditekan."""
            sound = self.sounds.get(sound_file)
            if sound:
                print(f"Memainkan suara: {sound_file}")
                sound.play()
            else:
                print(f"Error: File {sound_file} tidak ditemukan atau tidak bisa dimuat.")
        return play_sound_callback

    def _update_rect(self, instance, value):
        """Memperbarui ukuran dan posisi latar belakang gambar."""
        self.rect.pos = instance.pos
        self.rect.size = instance.size
