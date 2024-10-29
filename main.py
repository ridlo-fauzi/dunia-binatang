from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from screens.home_screen import homeScreen
from screens.menu_game import menuGame
from screens.SplashScreen import SplashScreen
from screens.mengenal_hewan_game import MengenalHewanGame
from screens.tebak_gambar_game import TebakGambarGame
from screens.match_induk_anak_game import MatchIndukAnakGame
from screens.LevelScreen_tebak_gambar import LevelScreenTebakGambar
from screens.LevelScreen_anak_induk import LevelScreenAnakInduk

class TebakGambarApp(App):

    def build(self):
        Window.size = (360, 640)
        self.sm = ScreenManager(transition=FadeTransition())

        splash_screen = SplashScreen(name='splash')
        main_menu = homeScreen(name='main_menu')
        menu_game_screen = menuGame(name='menu_game')
        mengenal_hewan_game = MengenalHewanGame(name='mengenal_hewan_game')
        level_screen_anak_induk = LevelScreenAnakInduk(name='level_screen_anak_induk')
        level_screen_tebak_gambar = LevelScreenTebakGambar(name='level_screen_tebak_gambar')
        match_anak_induk_game = MatchIndukAnakGame(name='match_anak_induk_game')
        tebak_gambar_game = TebakGambarGame(name='tebak_gambar_game')

        self.sm.add_widget(splash_screen)
        self.sm.add_widget(main_menu)
        self.sm.add_widget(menu_game_screen)
        self.sm.add_widget(mengenal_hewan_game)
        self.sm.add_widget(level_screen_anak_induk)
        self.sm.add_widget(level_screen_tebak_gambar)
        self.sm.add_widget(match_anak_induk_game)
        self.sm.add_widget(tebak_gambar_game)

        self.sm.current = 'splash'

        self.button_sound = SoundLoader.load('assets/music/soundButton/soundButton.MP3')
        self.sfx_sound = SoundLoader.load('assets/music/sfx.mp3')  
        if not self.button_sound:
            print("Error: Sound button file not found.")
        if not self.sfx_sound:
            print("Error: SFX sound file not found.")

        self.music_playing = False  
        self.music = None  
        self.sfx_volume = 1.0 
        self.bgm_volume = 1.0  
        
        return self.sm

    def start_background_music(self):
        """Memulai musik latar."""
        if not self.music_playing:
            self.music = SoundLoader.load('assets/music/kids.mp3')
            if self.music:
                self.music.loop = True
                self.music.volume = self.bgm_volume  
                self.music.play()
                self.music_playing = True
                print("Background music playing.")
            else:
                print("Error: Background music file not found.")

    def stop_music(self):
        """Menghentikan musik latar."""
        if self.music and self.music.state == 'play':
            self.music.stop()
            self.music_playing = False
            print("Background music stopped.")

    def play_button_sound(self):
        """Memainkan suara tombol ketika tombol ditekan."""
        if self.button_sound:
            self.button_sound.volume = self.sfx_volume  
            self.button_sound.play()
        else:
            print("Error: Button sound not available.")

    def update_bgm_volume(self, volume):
        """Memperbarui volume BGM."""
        self.bgm_volume = volume
        if self.music:
            self.music.volume = volume

    def update_sfx_volume(self, volume):
        """Memperbarui volume SFX."""
        self.sfx_volume = volume
        if self.sfx_sound:  
            self.sfx_sound.volume = volume

if __name__ == '__main__':
    TebakGambarApp().run()
