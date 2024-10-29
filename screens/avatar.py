from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock

class AnimatedImage(ButtonBehavior, BoxLayout):
    def __init__(self, base_path, fps=10, **kwargs):
        super().__init__(**kwargs)

        self.base_path = base_path
        self.fps = fps

        self.current_image = 0

        self.images = [f"{self.base_path}{i}.png" for i in range(4)]  

        self.img = Image(source=self.images[self.current_image], size_hint=(None, None), size=(200, 200))
        self.add_widget(self.img)

        Clock.schedule_interval(self.update_image, 1 / self.fps)

    def update_image(self, dt):
        """Fungsi untuk mengubah gambar setiap frame berdasarkan fps."""
        self.current_image = (self.current_image + 1) % len(self.images)  
        self.img.source = self.images[self.current_image]
