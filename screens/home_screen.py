from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.lang import Builder
from textwrap import dedent

Builder.load_string(
    """
<CustomSlider@Slider>:
    background_width: 0
    padding: sp(20)
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'assets/img/sliderisi.png'
    canvas.after:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: (self.value_pos[0] - sp(20), self.center_y - sp(20)) if self.orientation == 'horizontal' else (self.center_x - sp(20), self.value_pos[1] - sp(20))
            size: (sp(40), sp(40))
            source: 'assets/img/knob.png'
"""
)

class ClickableImage(ButtonBehavior, Image):
    pass


class SplashScreen(Screen):
    pass


class GameScreen(Screen):
    pass


class menuGame(Screen):
    pass


class homeScreen(Screen):
    def __init__(self, **kwargs):
        super(homeScreen, self).__init__(**kwargs)

        self.button_sound = SoundLoader.load('assets/music/soundButton/soundButton.MP3')
        if not self.button_sound:
            print("Error: Sound file not found or failed to load.")

        Clock.schedule_once(self.build_ui, 0.5)  

    def on_enter(self):
        """Dipanggil saat layar home_screen muncul. Mulai musik in-game di sini."""
        print("Home screen muncul, mulai musik in-game")
        app = App.get_running_app()
        app.start_background_music()

    def play_button_sound(self):
        """Memainkan suara tombol dengan volume yang mengikuti slider SFX"""
        app = App.get_running_app()
        if self.button_sound:
            self.button_sound.volume = app.sfx_volume  
            self.button_sound.play()

    def build_ui(self, dt):
        """Membangun layout UI setelah transisi splash screen selesai"""
        main_menu_layout = FloatLayout()

        bgAwal = Image(source='assets/img/background.JPG', allow_stretch=True, keep_ratio=False)
        main_menu_layout.add_widget(bgAwal)
        logoTebakGambar = Image(source='assets/img/logo.png', size_hint=(None, None), size=(150, 150),
                                pos_hint={'center_x': 0.5, 'center_y': 0.8})
        main_menu_layout.add_widget(logoTebakGambar)

        self.mulaiBTn = ClickableImage(size_hint=(None, None), size=(230, 230),
                                    pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                    source='assets/img/play.png')

        keluarBTn = ClickableImage(size_hint=(None, None), size=(70, 70),
                pos_hint={'right': 1, 'top': 1},
                source='assets/img/exit.png')

        self.mulaiBTn.bind(on_press=self.play_button_and_switch)
        keluarBTn.bind(on_press=self.play_button_and_exit_confirm)

        main_menu_layout.add_widget(self.mulaiBTn)
        main_menu_layout.add_widget(keluarBTn)

        print("Menambahkan tombol settings...")  
        try:
            self.settings_button = ClickableImage(source='assets/gif/setting.gif', size_hint=(None, None), size=(70, 70),
                    pos_hint={'x': 0.02, 'top': 1})  
            self.settings_button.bind(on_press=self.play_button_and_settings)
            main_menu_layout.add_widget(self.settings_button)
            print("Tombol settings ditambahkan.")
        except Exception as e:
            print(f"Error loading settings button: {e}")

        self.add_widget(main_menu_layout)

        self.animate_play_button()

    def animate_play_button(self):
        anim = Animation(size=(230, 230), duration=1) + Animation(size=(150, 150), duration=1)
        anim.repeat = True  
        anim.start(self.mulaiBTn)

    def play_button_and_switch(self, instance):
        """Memainkan suara tombol dan beralih ke layar game"""
        self.play_button_sound()
        Clock.schedule_once(self.switch_to_menu_game, 0.3)

    def switch_to_menu_game(self, dt):
        """Pindahkan ke layar game tanpa menghentikan musik"""
        self.manager.current = 'menu_game'

    def play_button_and_exit_confirm(self, instance):
        """Memainkan suara tombol sebelum menampilkan konfirmasi keluar"""
        self.play_button_sound()
        Clock.schedule_once(self.show_exit_popup, 0.3)

    def show_exit_popup(self, dt):
        """Menampilkan popup konfirmasi untuk keluar dari aplikasi dengan background khusus"""
        try:
            popup_layout = FloatLayout()

            ya_button = ClickableImage(source='assets/img/Keluar/iya.png', size_hint=(None, None), size=(300, 150),
                pos_hint={'center_x': 0.3, 'y': 0.4})
            ya_button.bind(on_press=self.exit_app)

            tidak_button = ClickableImage(source='assets/img/Keluar/tidak.png', size_hint=(None, None), size=(300, 150),
                pos_hint={'center_x': 0.7, 'y': 0.4})
            tidak_button.bind(on_press=lambda x: exit_popup.dismiss())

            popup_layout.add_widget(ya_button)
            popup_layout.add_widget(tidak_button)

            exit_popup = Popup(title="",  
                        title_size=0,
                        separator_height=0,  
                        content=popup_layout,
                        size_hint=(0.75, 0.5),
                        auto_dismiss=True,
                        background='assets/img/Keluar/bg.png')
            exit_popup.open()

        except Exception as e:
            print(f"Error showing exit popup: {e}")

    def play_button_and_settings(self, instance):
        """Memainkan suara tombol sebelum menampilkan settings"""
        self.play_button_sound()
        self.show_settings_popup(instance)

    def show_settings_popup(self, instance):
        """Tampilkan pop-up pengaturan suara"""
        try:
            app = App.get_running_app()

            popup_layout = FloatLayout()

            sfx_bg = Image(
                source="assets/img/options/sfx.png",
                size_hint=(None, None),
                size=(100, 100),
                pos_hint={"x": 0.1, "y": 0.5},
            )
            bgm_bg = Image(
                source="assets/img/options/bgm.png",
                size_hint=(None, None),
                size=(100, 100),
                pos_hint={"x": 0.1, "y": 0.4},
            )

            popup_layout.add_widget(sfx_bg)
            popup_layout.add_widget(bgm_bg)

            

            bgm_slider_code = dedent(
                f"""
CustomSlider:
    min: 0
    max: 1
    value: {app.bgm_volume}
    size_hint: (0.6, None)
    height: 200
    pos_hint: {{"center_x": .6, "center_y": .4}}
    cursor_size: (40, 40)
"""
            )
            bgm_slider = Builder.load_string(bgm_slider_code)
            bgm_slider.bind(value=lambda instance, value: app.update_bgm_volume(value))
            popup_layout.add_widget(bgm_slider)

            sfx_slider_code = dedent(
                f"""
CustomSlider:
    min: 0
    max: 1
    value: {app.sfx_volume}
    size_hint:(0.6, None)
    height: 200
    pos_hint: {{"center_x": 0.6, "center_y": 0.57}}
    cursor_size: (40, 40)
"""
            )
            sfx_slider = Builder.load_string(sfx_slider_code)
            sfx_slider.bind(value=lambda instance, value: app.update_sfx_volume(value))
            popup_layout.add_widget(sfx_slider)

            close_button = ClickableImage(
                source="assets/img/x.png",
                size_hint=(None, None),
                size=(100, 100),
                pos_hint={"right": 0.97, "top": 0.75},
            )
            close_button.bind(on_press=lambda x: self.play_close_button_and_dismiss(settings_popup))
            popup_layout.add_widget(close_button)

            settings_popup = Popup(
                title="",
                title_size=0,
                separator_height=0,
                content=popup_layout,
                size_hint=(1, 0.8),
                auto_dismiss=True,
                background="assets/img/options/bgOptions.png",
            )
            settings_popup.open()

        except Exception as e:
            print(f"Error showing settings popup: {e}")

    def play_close_button_and_dismiss(self, popup):
        """Memainkan suara tombol lalu menutup popup"""
        self.play_button_sound()  # Memainkan suara tombol
        popup.dismiss()

    def exit_app(self, instance):
        """Keluar dari aplikasi"""
        App.get_running_app().stop()

class GameApp(App):
    bgm_volume = 0.5
    sfx_volume = 0.5

    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(homeScreen(name='home'))
        sm.add_widget(menuGame(name='menu_game'))
        return sm

    def on_start(self):
        self.bgm_volume = float(self.config.get('volume', 'bgm_volume', fallback='0.5'))
        self.sfx_volume = float(self.config.get('volume', 'sfx_volume', fallback='0.5'))

    def start_background_music(self):
        self.background_music = SoundLoader.load('assets/music/background.mp3')
        if self.background_music:
            self.background_music.loop = True
            self.background_music.volume = self.bgm_volume
            self.background_music.play()

    def update_bgm_volume(self, value):
        self.bgm_volume = value
        if hasattr(self, 'background_music') and self.background_music:
            self.background_music.volume = self.bgm_volume

    def update_sfx_volume(self, value):
        self.sfx_volume = value

    def on_stop(self):
        self.config.set('volume', 'bgm_volume', str(self.bgm_volume))
        self.config.set('volume', 'sfx_volume', str(self.sfx_volume))
        self.config.write()

    def build_config(self, config):
        config.setdefaults('volume', {
            'bgm_volume': '0.5',
            'sfx_volume': '0.5'
        })