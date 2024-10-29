from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.progressbar import ProgressBar

class SplashScreen(Screen):
    def __init__(self, logo_size=(0.5, 0.5), **kwargs):
        super(SplashScreen, self).__init__(**kwargs)

        self.layout = FloatLayout()
        self.add_widget(self.layout)

        self.background_image = Image(
            source="./assets/img/bgSplash/splash.png",  
            allow_stretch=True, 
            keep_ratio=False,  
            size_hint=(1, 1),  
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        self.layout.add_widget(self.background_image)

        self.background = Image(
            source="./assets/img/logo.png",
            allow_stretch=True, 
            keep_ratio=True,  
            size_hint=logo_size,  
            pos_hint={"center_x": 0.5, "center_y": 0.75}  
        )
        self.layout.add_widget(self.background)

        self.progress_bar = ProgressBar(
            max=100,
            value=0,
            size_hint=(0.5, None),  
            height=20,
            pos_hint={"center_x": 0.5, "y": 0.1},  
        )
        self.layout.add_widget(self.progress_bar)

        self.bind(size=self.update_layout)

        Clock.schedule_interval(self.update_progress_bar, 1 / 30)

    def update_layout(self, *args):
        """Fungsi untuk menyesuaikan elemen berdasarkan ukuran layar yang baru"""
        pass

    def update_progress_bar(self, dt):
        """Fungsi untuk meng-update progress bar"""
        self.progress_bar.value += dt * 20
        if self.progress_bar.value >= 100:
            self.progress_bar.value = 100

    def on_enter(self):
        """Dipanggil saat layar splash dimasukkan ke dalam ScreenManager"""
        print("Splash screen on_enter dipanggil")  
        Clock.schedule_once(self.play_splash_sound, 0.5)  
        Clock.schedule_once(self.switch_to_main, 6)  

    def play_splash_sound(self, dt):
        """Memutar suara splash"""
        print("Memulai pemutaran suara splash")  
        self.sound = SoundLoader.load('assets/music/soundSplash/SplashTebakGambar.MP3')
        if self.sound:
            self.sound.play()
            print("Suara splash diputar")  
        else:
            print("Error: Suara splash tidak ditemukan!")

    def on_leave(self):
        """Hentikan suara splash sebelum berpindah ke layar utama"""
        if self.sound:
            self.sound.stop()

    def switch_to_main(self, dt):
        """Berpindah ke layar utama setelah splash selesai"""
        print("Beralih ke layar utama")  
        self.manager.current = 'main_menu'  
