from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from datetime import datetime, timedelta
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.audio import SoundLoader
import json
import os
import random

class ClickableImage(ButtonBehavior, Image):
    pass

class MatchIndukAnakGame(Screen):
    def on_enter(self):
        """Mematikan backsound saat masuk ke screen ini."""
        app = App.get_running_app()
        app.stop_music()  

    def play_sound_popup(self, stars):
        """Memutar suara berdasarkan jumlah bintang."""
        sounds = {
            3: 'assets/music/soundPopup/perfect.mp3',
            2: 'assets/music/soundPopup/Good.mp3',
            1: 'assets/music/soundPopup/Okeay.mp3',
            0: 'assets/music/soundPopup/Give_the_best.mp3'
        }
        
        sound_file = sounds.get(stars)
        if sound_file:
            sound = SoundLoader.load(sound_file)
            if sound:
                sound.play()

    def on_leave(self):
        """Memulai kembali backsound saat meninggalkan screen ini.""" 
        app = App.get_running_app()
        app.start_background_music()

    def __init__(self, **kwargs):
        super(MatchIndukAnakGame, self).__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 1)  
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)
        self.layout = FloatLayout()

        background_image = Image(source="assets/img/background_level.jpg", allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background_image)

        self.button_sound = SoundLoader.load('assets/music/soundButton/soundButton.MP3')
        if not self.button_sound:
            print("Error: Sound file not found or failed to load.")

        back_button = ClickableImage(size_hint=(None, None), size=(140, 100),
                            pos_hint={'center_x': 0.5, 'top': 1.02},
                            source='assets/img/back.png',  
                            ) 
        back_button.bind(on_press=self.go_back)
        self.layout.add_widget(back_button)


        self.max_lives = 3
        self.lives = self.max_lives
        self.questions_answered = 0
        self.max_hints = 3  
        self.hints_left = self.max_hints  
        self.hint_cooldown_time = 180  
        self.hint_last_used = None  

        self.used_hint = False  
        self.wrong_attempts = 0  

        self.lives_label = Image(source=f"assets/img/nyawa-bantuan/nyawa_{self.lives}.png", 
                         size_hint=(None, None), size=(200, 200), 
                         pos_hint={'center_x': 0.15, 'top': 1.05}
                         )
        self.layout.add_widget(self.lives_label)


        self.fruit_box = BoxLayout(orientation='horizontal', size_hint=(0.8, None), height=100,
                                   pos_hint={'center_x': 0.5, 'center_y': 0.4})
        self.layout.add_widget(self.fruit_box)

        self.hint_button = ClickableImage(source=f"assets/img/nyawa-bantuan/bantuan_{self.hints_left}.png", size_hint=(None, None), size=(200, 250),
                                  pos_hint={'center_x': 0.85, 'top': 1.08})
        self.hint_button.bind(on_press=self.use_hint)
        self.layout.add_widget(self.hint_button)

        self.add_widget(self.layout)

        self.tree_image = Image(size_hint=(0.4, 0.4), pos_hint={'center_x': 0.5, 'center_y': 0.7})
        self.layout.add_widget(self.tree_image)


        self.level = 1 
        self.completed_levels = [False] * 9

    def play_button_sound(self):
        """Memainkan suara tombol dengan volume yang mengikuti slider SFX"""
        app = App.get_running_app()
        if self.button_sound:
            self.button_sound.volume = app.sfx_volume  
            self.button_sound.play()

    def start_game(self, level):
        """Memulai permainan dengan level yang dipilih."""
        self.current_level = level
        self.level = level
        self.lives = self.max_lives
        self.lives_label.source = f"assets/img/nyawa-bantuan/nyawa_{self.lives}.png"  
        self.lives_label.reload()  
        self.load_level_data(level)
        self.load_new_question()


    def load_level_data(self, level):
        """Memuat data pertanyaan tetap berdasarkan level dari file JSON."""
        with open('assets/json/level_anak_induk.json', 'r') as f:
            level_data = json.load(f)

        if str(level) in level_data['levels']:
            level_info = level_data['levels'][str(level)]
            
            image = level_info['image']
            answer = level_info['answer']
            
            self.tree_fruit_pairs = [(image, answer)]
            self.correct_fruit = answer
        else:
            print(f"Level {level} tidak ditemukan dalam file JSON.")

    def load_new_question(self):
        self.tree_image.source = self.tree_fruit_pairs[0][0] 

        all_fruits = ["ayam", "buaya", "harimau", "jerapah", "kucing", "kuda", "rusa", "sapi", "tupai"]

        other_fruits = [fruit for fruit in all_fruits if fruit != self.correct_fruit]

        random_fruits = random.sample(other_fruits, 2)

        random_fruits.append(self.correct_fruit)

        random.shuffle(random_fruits)

        self.fruit_box.clear_widgets()
        for fruit in random_fruits:
            fruit_button = Button(size_hint=(None, 1), width=100, background_normal=f"assets/img/hewan/{fruit}.png")
            fruit_button.bind(on_press=lambda instance, fruit=fruit: self.check_match(fruit))
            self.fruit_box.add_widget(fruit_button)

    def load_stars_data(self):
        if os.path.exists('assets/json/level_anak_induk.json'):
            with open('assets/json/level_anak_induk.json', 'r') as file:
                return json.load(file)
        return {"levels": {}}  

    def save_stars_data(self, level, stars):
        stars_data = self.load_stars_data()  

        if str(level) in stars_data["levels"]:
            current_stars = int(stars_data["levels"][str(level)].get("stars", 0))

            if stars > current_stars:
                stars_data["levels"][str(level)]["stars"] = str(stars)
                print(f"Bintang baru ({stars}) disimpan untuk level {level}.")
            else:
                print(f"Bintang saat ini ({current_stars}) lebih tinggi atau sama dengan bintang baru ({stars}). Mengambil bintang lama.")
                stars_data["levels"][str(level)]["stars"] = str(current_stars)

            if stars > 0:  
                next_level = str(level + 1)
                if next_level in stars_data["levels"]:
                    if stars_data["levels"][next_level]["stars"] == "terkunci":
                        stars_data["levels"][next_level]["stars"] = "0"
                        print(f"Level {next_level} telah diatur bintangnya menjadi 0 setelah menyelesaikan level {level}.")
                        self.mark_level_completed() 
                    self.update_level_selection(self.level, True, int(stars_data["levels"][str(level)]["stars"]))
                else: 
                    self.update_level_selection(self.level, True, int(stars_data["levels"][str(level)]["stars"]))
            self.show_complete_answer_popup(int(stars_data["levels"][str(level)]["stars"]), correct_answer=True)
        else:
            print(f"Level {level} tidak ditemukan dalam data JSON.")

        with open('assets/json/level_anak_induk.json', 'w') as file:
            json.dump(stars_data, file, indent=4)


 

    def check_match(self, fruit):
        """Memeriksa apakah buah yang dipilih cocok dengan pohon."""
        self.play_button_sound()
        if self.lives > 0:
            if fruit == self.correct_fruit:
                stars = self.calculate_stars()
                self.save_stars_data(self.level, stars) 
                self.load_new_question()    
                

                self.used_hint = False
                self.wrong_attempts = 0
            else:
                self.wrong_attempts += 1  
                self.lives -= 1
                self.lives_label.source = f"assets/img/nyawa-bantuan/nyawa_{self.lives}.png"  
                self.lives_label.reload()  

                if self.lives > 0:
                    self.show_complete_answer_popup(correct_answer=False)
                else:
                    self.show_game_over_popup()  


    def show_game_over_popup(self):
        """Menampilkan popup Game Over dengan tombol Kembali dan Home."""

        game_over_popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10)

        button_layout = BoxLayout(orientation='horizontal', size_hint=(0.5, 0.4), spacing=10, padding=[10, 10, 10, 70], pos_hint={'center_x': 0.5})

        home_button = ClickableImage(size_hint=(0.05, 0.4), source='assets/img/popup/home.png')  
        home_button.bind(on_press=self.go_back_from_game_over) 
        button_layout.add_widget(home_button)

        game_over_popup_content.add_widget(button_layout)

        self.game_over_popup = Popup(
            title="",  
            title_size=0,
            separator_height=0,  
            content=game_over_popup_content,
            size_hint=(1, 0.8),
            auto_dismiss=True,
            background='assets/img/popup/gameOver.png'  
        )
        
        self.game_over_popup.open()



    def go_back_from_game_over(self, instance):
        """Fungsi untuk kembali ke menu pemilihan level dan menutup popup."""
        self.play_button_sound()
        self.manager.current = 'level_screen_anak_induk'  
        if self.game_over_popup:
            self.game_over_popup.dismiss()  
            self.reset_game()  

    def reset_game(self):
        """Mengatur ulang status permainan untuk memulai kembali."""
        self.lives = self.max_lives
        self.questions_answered = 0
        self.hints_left = self.max_hints
        self.lives_label.source = f"assets/img/nyawa-bantuan/nyawa_{self.lives}.png"
        self.hint_button.background_normal = f"assets/img/nyawa-bantuan/bantuan_{self.hints_left}.png"
        self.load_new_question() 

    def go_back(self, instance):
        """Kembali ke layar sebelumnya."""
        self.play_button_sound()
        self.manager.current = 'level_screen_anak_induk'

    def mark_level_completed(self):
        """Tandai level sebagai selesai dan perbarui status di LevelSelectionScreen."""
        level_screen_anak_induk = self.manager.get_screen('level_screen_anak_induk')
        level_screen_anak_induk.completed_levels[self.level - 1] = True  

        if self.level < len(level_screen_anak_induk.completed_levels):
            level_screen_anak_induk.completed_levels[self.level] = True


    def update_level_selection(self, level, is_correct, stars):
        """Memperbarui status level pada pemilihan level."""
        level_screen_anak_induk = self.manager.get_screen('level_screen_anak_induk')
        level_screen_anak_induk.on_answer_valid(level-1, is_correct, stars)  

    def show_complete_answer_popup(self, stars=0, correct_answer=False):
        """Menampilkan popup untuk hasil permainan berdasarkan jumlah bintang yang diperoleh.
        Jika jawaban benar dan bintang > 0, ada tombol Next Level dan Kembali.
        Jika jawaban salah atau bintang 0, hanya ada tombol Kembali.
        Jika level terakhir, langsung tampilkan pop-up game selesai."""

        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        overlay_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        button_layout = FloatLayout(size_hint=(1, 0.4))

        if correct_answer:
            if stars == 3:
                background_image = 'assets/img/popup/popup_bintang_3.png'
            elif stars == 2:
                background_image = 'assets/img/popup/popup_bintang_2.png'
            elif stars == 1:
                background_image = 'assets/img/popup/popup_bintang_1.png'
            else:
                background_image = 'assets/img/popup/popup_bintang_0.png'

            self.play_sound_popup(stars)

            back_button = ClickableImage(size_hint=(None, None), size=(200, 200), source='assets/img/popup/home.png')
            back_button.bind(on_press=self.go_back_and_close_popup)
            back_button.pos_hint = {'x': 0.12, 'center_y': 0.3}  
            button_layout.add_widget(back_button)

            if stars > 0:
                next_button = ClickableImage(size_hint=(None, None), size=(200, 200), source='assets/img/popup/next.png')
                next_button.bind(on_press=self.go_to_next_level)
                next_button.pos_hint = {'right': 0.88, 'center_y': 0.3}  
                button_layout.add_widget(next_button)
            else : 
                close_button = ClickableImage(size_hint=(None, None), size=(200, 200), source='assets/img/popup/ulang.png')
                close_button.bind(on_press=self.close_popup_and_reload)
                close_button.pos_hint = {'right': 0.88, 'center_y': 0.3}
                button_layout.add_widget(close_button)

        else:
            background_image = 'assets/img/popup/POPUP_SALAH.png'
            
            close_button = ClickableImage(size_hint=(None, None), size=(200, 200), source='assets/img/popup/ulang.png')
            close_button.bind(on_press=self.close_popup)
            
            close_button.pos_hint = {'center_x': 0.5, 'center_y': 0.3}
            button_layout.add_widget(close_button)

        overlay_layout.add_widget(button_layout)

        popup_layout.add_widget(overlay_layout)

        self.result_popup = Popup(
            title="",
            title_size=0,
            separator_height=0,
            content=popup_layout,
            size_hint=(1, 0.8),
            auto_dismiss=True,
            background=background_image,
        )
        self.result_popup.open()

    def calculate_stars(self):
        """Menghitung jumlah bintang berdasarkan kriteria yang diberikan."""
        if self.used_hint:
            if self.wrong_attempts == 0:
                return 2  
            elif self.wrong_attempts == 1:
                return 1  
            else:
                return 0  
        else:
            if self.wrong_attempts == 0:
                return 3 
            elif self.wrong_attempts == 1:
                return 2  
            else:
                return 1  


    def go_back_and_close_popup(self, instance):
        """Fungsi untuk kembali ke level selection dan menutup popup."""
        self.go_back(instance)  
        self.result_popup.dismiss()  

    def close_popup(self, instance):
        """Menutup popup hasil permainan."""
        self.play_button_sound()
        self.result_popup.dismiss()  
    
    def close_popup_and_reload(self, instance):
        """Menutup popup hasil permainan."""
        self.play_button_sound()
        self.lives = self.max_lives
        self.lives_label.source = f"assets/img/nyawa-bantuan/nyawa_{self.lives}.png" 
        self.result_popup.dismiss()  
        self.lives_label.reload()


    def go_to_next_level(self, instance):
        self.play_button_sound()
        """Memulai level berikutnya setelah menyelesaikan level saat ini atau tampilkan pop-up jika game selesai."""
        self.result_popup.dismiss()  
        if self.level == len(self.completed_levels):
            self.show_complete_popup()
        else:
            self.level += 1  
            self.start_game(self.level)  

    def close_popup_and_return(self, instance):
        """Fungsi untuk menutup pop-up dan kembali ke halaman level."""
        self.result_popup.dismiss()  
        self.manager.current = 'level_screen_anak_induk'  

    def show_complete_popup(self):
        """Menampilkan pop-up ketika semua level sudah diselesaikan."""
        
        popup_layout = FloatLayout()

        home_button = ClickableImage(
            size_hint=(None, None), 
            size=(200, 210), 
            source='assets/img/popup/home.png', 
            pos_hint={'center_x': 0.5, 'top': 0.36}  
        )
        home_button.bind(on_press=self.go_back_and_close_popup)
        popup_layout.add_widget(home_button)

        self.result_popup = Popup(
            title="",  
            title_size=0,  
            separator_height=0,  
            content=popup_layout,
            size_hint=(1, 0.8),
            auto_dismiss=True,
            background='assets/img/popup/congrast.png',  
        )
        self.result_popup.open()

    def show_bantuan_popup(self, show_image=False):
        """Menampilkan popup untuk memberi tahu hasil permainan dengan background dan tombol custom."""
        
        popup_layout = FloatLayout()
        
        overlay_layout = BoxLayout(orientation='vertical', padding=[10, 50, 10, 10], spacing=10, size_hint=(0.9, 0.9), pos_hint={'center_x': 0.5, 'center_y': 0.8})

        self.float_container = FloatLayout(size_hint=(1, None), height=200)  
        
        if show_image:
            hewan_image = Image(source=f"assets/img/siluet/{self.correct_fruit}_siluet.png", size_hint=(None, None), size=(150, 150),
                                pos_hint={'center_x': 0.5, 'center_y': 0.4})  
            self.float_container.add_widget(hewan_image)
        else:
            remaining_time = self.hint_cooldown_time - (datetime.now() - self.hint_last_used).seconds
            self.time_label = Label(
                text=f"{remaining_time // 60} : {remaining_time % 60}",
                font_size='35sp',         
                bold=True,                
                pos_hint={'center_x': 0.5, 'center_y': 0.55}  
            )
            self.hint_event = Clock.schedule_interval(self.update_hint_cooldown, 1)
            popup_layout.add_widget(self.time_label)

        overlay_layout.add_widget(self.float_container)
        
        popup_layout.add_widget(overlay_layout)
        
        close_button = ClickableImage(size_hint=(None, None), size=(200, 200), 
                            source='assets/img/x.png', pos_hint={'right': 0.98, 'top': 0.88})
        close_button.bind(on_press=lambda *args: self.close_bantuan_popup(popup))
        popup_layout.add_widget(close_button)
        
        popup = Popup(
            title="",  
            title_size=0,  
            separator_height=0,  
            content=popup_layout,
            size_hint=(1, 0.8),
            auto_dismiss=True,
            background='assets/img/popup/popup_polos.png',  
        )
        popup.open()

    def update_hint_cooldown(self, dt):
        """Memperbarui waktu cooldown di dalam pop-up setiap detik."""
        remaining_time = self.hint_cooldown_time - (datetime.now() - self.hint_last_used).seconds
        
        if remaining_time <= 0:
            Clock.unschedule(self.hint_event)

            self.float_container.clear_widgets()
            self.time_label.text = ""

            hewan_image = Image(
                source=f"assets/img/siluet/{self.correct_fruit}_siluet.png",
                size_hint=(None, None),
                size=(150, 150),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            self.float_container.add_widget(hewan_image)
        else:
            minutes = remaining_time // 60
            seconds = remaining_time % 60
            self.time_label.text = f"{minutes} : {str(seconds).zfill(2)}"

    def show_bantuan_habis(self):
        """Menampilkan popup untuk memberi tahu hasil permainan dengan background dan tombol custom."""
    
        popup_layout = FloatLayout()
        
        overlay_layout = BoxLayout(orientation='vertical', padding=[10, 50, 10, 10], spacing=10, size_hint=(0.9, 0.9), pos_hint={'center_x': 0.5, 'center_y': 0.8})

        self.float_bantuan = FloatLayout(size_hint=(1, None), height=200)  
        

        overlay_layout.add_widget(self.float_bantuan)
        
        popup_layout.add_widget(overlay_layout)
        
        close_button = ClickableImage(size_hint=(None, None), size=(200, 200), 
                            source='assets/img/x.png', pos_hint={'right': 0.98, 'top': 0.88})
        close_button.bind(on_press=lambda *args: self.close_bantuan_popup(popup))
        popup_layout.add_widget(close_button)
        
        popup = Popup(
            title="",  
            title_size=0,  
            separator_height=0,  
            content=popup_layout,
            size_hint=(1, 0.8),
            auto_dismiss=True,
            background='assets/img/popup/bantuan_habis.png',  
        )
        popup.open()


    def close_bantuan_popup(self, popup):
        """Menutup popup bantuan."""
        self.play_button_sound()
        popup.dismiss()


    def use_hint(self, instance):
        """Gunakan hint untuk membantu pemain, jika tidak dalam cooldown."""
        self.play_button_sound()
        if self.hints_left > 0 and (self.hint_last_used is None or
                                    (datetime.now() - self.hint_last_used) > timedelta(seconds=self.hint_cooldown_time)):
            self.hints_left -= 1
            self.hint_button.background_normal = f"assets/img/nyawa-bantuan/bantuan_{self.hints_left}.png"
            self.hint_last_used = datetime.now()
            self.show_bantuan_popup(show_image=True) 
            self.used_hint = True 
        elif self.hints_left == 0:
            self.show_bantuan_habis()
        else:
            self.show_bantuan_popup()

                
    def reset_hint(self, dt):
        """Mengaktifkan kembali bantuan dan memperbarui teks tombol."""
        self.hints_left = self.max_hints  
        self.hint_button.background_normal = f"assets/img/nyawa-bantuan/bantuan_{self.hints_left}.png"
        self.hint_button.disabled = False  

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size