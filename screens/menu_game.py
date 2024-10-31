from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from screens.avatar import AnimatedImage
from kivy.core.audio import SoundLoader

class ClickableImage(ButtonBehavior, Image):
    def __init__(self, with_animation=True, **kwargs):
        super(ClickableImage, self).__init__(**kwargs)
        if with_animation:
            self.animate_button()

    def animate_button(self):
        """Animasi berulang zoom in dan zoom out"""
        anim = Animation(size=(450, 450), duration=2) + Animation(size=(400, 400), duration=1)
        anim.repeat = True 
        anim.start(self)

class menuGame(Screen):
    def __init__(self, **kwargs):
        super(menuGame, self).__init__(**kwargs)

        menu_game_layout = FloatLayout()

        self.button_sound = SoundLoader.load('assets/music/soundButton/soundButton.MP3')
        if not self.button_sound:
            print("Error: Sound file not found or failed to load.")

        bgMenu = Image(source='assets/img/Screen.png', allow_stretch=True, keep_ratio=False)
        menu_game_layout.add_widget(bgMenu)

        back_button = ClickableImage(size_hint=(None, None), size=(400, 400),
            pos_hint={'x': 0.02, 'top': 0.98},
            source='assets/img/back.png', with_animation=False)  
        back_button.bind(on_press=self.go_back_to_main_menu)
        menu_game_layout.add_widget(back_button)

        button_size = (500, 450)

        button_mengenalHewan = ClickableImage(size_hint=(None, None), size=button_size, source='assets/img/menuGame/mengenalHewann.png')
        button_mengenalHewan.pos_hint = {'x': 0.05, 'y': 0.5}
        button_mengenalHewan.bind(on_press=self.go_to_mengenal_hewan) 
        menu_game_layout.add_widget(button_mengenalHewan)

        button_tebakGambar = ClickableImage(size_hint=(None, None), size=button_size, source='assets/img/menuGame/menebakSuara.png')
        button_tebakGambar.pos_hint = {'x': 0.4, 'y': 0.3}
        button_tebakGambar.bind(on_press=self.go_to_tebak_suara)  
        menu_game_layout.add_widget(button_tebakGambar)

        button_anakInduk = ClickableImage(size_hint=(None, None), size=button_size, source='assets/img/menuGame/mengenalnduk.png')
        button_anakInduk.pos_hint = {'x': 0.02, 'y': 0.1}
        button_anakInduk.bind(on_press=self.go_to_mengenal_induk)  
        menu_game_layout.add_widget(button_anakInduk)

        self.add_widget(menu_game_layout)

    def play_button_sound(self):
        """Memainkan suara tombol dengan volume yang mengikuti slider SFX"""
        app = App.get_running_app()
        if self.button_sound:
            self.button_sound.volume = app.sfx_volume  
            self.button_sound.play()

    def on_enter(self):
        """Dipanggil saat layar menu game muncul. Tidak hentikan musik."""
        print("Memasuki menu game, musik tetap diputar.")

    def on_leave(self):
        """Tidak menghentikan musik saat keluar dari menu game."""
        print("Meninggalkan menu game, musik tetap diputar.")

    def go_to_mengenal_hewan(self, instance):
        """Pindah ke layar mengenal hewan"""
        self.play_button_sound()
        self.manager.current = 'mengenal_hewan_game'
    
    def go_to_tebak_suara(self, instance):
        """Pindah ke layar mengenal hewan"""
        self.play_button_sound()
        self.manager.current = 'level_screen_tebak_gambar'

    def go_to_mengenal_induk(self, instance):
        """Pindah ke layar game"""
        self.play_button_sound()
        self.manager.current = 'level_screen_anak_induk'

    def go_back_to_main_menu(self, instance):
        """Kembali ke menu utama"""
        self.play_button_sound()
        self.manager.current = 'main_menu'