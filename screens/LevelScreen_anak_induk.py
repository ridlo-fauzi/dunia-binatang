import json
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.audio import SoundLoader

class ClickableImage(ButtonBehavior, Image):
    pass

class LevelScreenAnakInduk(Screen):
    def __init__(self, **kwargs):
        super(LevelScreenAnakInduk, self).__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)
        
        self.completed_levels = [False] * 9
        self.completed_levels[0] = True 
        self.stars_per_level = [0] * 9
        self.load_levels_data()

        layout = FloatLayout()

        background_image = Image(source="assets/img/background_level.jpg", allow_stretch=True, keep_ratio=False)
        layout.add_widget(background_image)

        self.button_sound = SoundLoader.load('assets/music/soundButton/soundButton.MP3')
        if not self.button_sound:
            print("Error: Sound file not found or failed to load.")

        back_button = ClickableImage(size_hint=(None, None), size=(250, 200),
                             pos_hint={'center_x': 0.5, 'top': 1.02},
                             source='assets/img/back.png')
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        title = Image(source="assets/img/level.png", size_hint=(None, None), size=(1000, 250), pos_hint={'center_x': 0.5, 'top': 0.9})
        layout.add_widget(title) 

        button_positions = [
            (0.25, 0.60), (0.55, 0.60), (0.85, 0.60),
            (0.15, 0.45), (0.45, 0.45), (0.75, 0.45),
            (0.25, 0.30), (0.55, 0.30), (0.85, 0.30)
        ]

        self.level_buttons = []  

        for i in range(len(button_positions)):
            pos_hint = {'center_x': button_positions[i][0], 'center_y': button_positions[i][1]}
            button_layout = RelativeLayout(size_hint=(None, None), size=(200, 112.5), pos_hint=pos_hint)

            if self.completed_levels[i]:
                level_image_source = f"assets/img/level/level_{i+1}_bintang_{self.stars_per_level[i]}.png"  
            else:
                level_image_source = f"assets/img/level/level_{i+1}_terkunci.png" 

            level_image = Image(source=level_image_source, size_hint=(None, None), size=(200, 200), pos_hint={'center_x': 0.5, 'top': 0.90})

            self.level_buttons.append(level_image)

            def on_level_image_touch(instance, touch, level=i):
                if instance.collide_point(*touch.pos):
                    if self.completed_levels[level]: 
                        self.start_game_for_level(level)
                    return True
                return False

            level_image.bind(on_touch_down=on_level_image_touch)

            if not self.completed_levels[i]:
                level_image.color = (0.5, 0.5, 0.5, 1)  

                level_image.bind(on_touch_down=lambda instance, touch: touch.ungrab(instance))

            button_layout.add_widget(level_image)
            layout.add_widget(button_layout)

        self.add_widget(layout)

    def play_button_sound(self):
        """Memainkan suara tombol dengan volume yang mengikuti slider SFX"""
        app = App.get_running_app()
        if self.button_sound:
            self.button_sound.volume = app.sfx_volume  
            self.button_sound.play()

    def load_levels_data(self):
        """Muat data level dari file JSON dan inisialisasi stars_per_level."""
        try:
            with open("assets/json/level_anak_induk.json", "r") as json_file:
                data = json.load(json_file)
                for level in range(1, 10):  
                    stars = data["levels"][str(level)]["stars"]  

                    if stars == "terkunci":
                        self.completed_levels[level - 1] = False  
                        self.stars_per_level[level - 1] = 0  
                    else:
                        self.completed_levels[level - 1] = True  
                        self.stars_per_level[level - 1] = int(stars)  
                
                last_completed_level = next((i for i in range(len(self.completed_levels) - 1, -1, -1) if self.completed_levels[i]), None)
                if last_completed_level is not None and self.stars_per_level[last_completed_level] == 3:
                    if last_completed_level + 1 < len(self.completed_levels):
                        self.completed_levels[last_completed_level + 1] = True  
        except Exception as e:
            print(f"Error loading level data: {e}")



    def start_game_for_level(self, level):
        """Mulai permainan dengan level yang dipilih."""    
        self.play_button_sound()
        match_anak_induk_game = self.manager.get_screen('match_anak_induk_game')
        match_anak_induk_game.start_game(level + 1)  
        self.manager.current = 'match_anak_induk_game'  

    def on_answer_valid(self, level, is_correct, stars_earned):
        """Handler ketika jawaban benar untuk level tertentu.""" 
        if is_correct:
            print(f"Level {level + 1} selesai dengan {stars_earned} bintang")
            self.completed_levels[level] = True  
            self.stars_per_level[level] = stars_earned  

            if level + 1 < len(self.completed_levels):
                self.completed_levels[level + 1] = True  

            self.update_level_buttons()

    def update_level_buttons(self):
        """Update tampilan tombol level berdasarkan level yang sudah dibuka dan jumlah bintang.""" 
        for i, level_image in enumerate(self.level_buttons):
            if i < 9:  
                if self.completed_levels[i]:
                    stars = self.stars_per_level[i]
                    new_source = f"assets/img/level/level_{i+1}_bintang_{stars}.png"
                    print(f"Update gambar level {i + 1} ke {new_source}") 
                    if level_image.source != new_source:  
                        level_image.source = new_source
                        level_image.reload()  
                    level_image.color = (1, 1, 1, 1)  
                    level_image.disabled = False  
                else:
                    new_source = f"assets/img/level/level_{i+1}_terkunci.png"
                    print(f"Level {i + 1} terkunci, menggunakan gambar {new_source}")  
                    if level_image.source != new_source: 
                        level_image.source = new_source
                        level_image.reload()  
                    level_image.color = (0.5, 0.5, 0.5, 1) 
                    level_image.disabled = True  

    def go_back(self, instance):
        """Kembali ke layar sebelumnya.""" 
        self.play_button_sound()
        self.manager.current = 'menu_game'

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size
