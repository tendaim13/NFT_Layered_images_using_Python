import os
from random import random
from PIL import Image
from layer import Layer
from typing import List


class AvatarGenerator:
    def __init__(self, images_path: str):
        self.layers = self.load_image_layers(images_path)
        self.background_color = (120,150,180)
        self.rare_background = (255,255,150)
        self.rare_background_chance = 0.05
        self.output_path: str = "./output"
        os.makedirs(self.output_path, exist_ok=True)

    def load_image_layers(self, images_path: str):
        sub_paths = sorted(os.listdir(images_path))
        #print (sub_paths)
        layers = []
        for sub_path in sub_paths:
            layer_path = os.path.join(images_path, sub_path)
            layer = Layer(layer_path)
            layers.append(layer)
        
        layers[2].rarity = 0.80
        layers[3].rarity = 0.15
        return layers

    def generate_image_sequence(self):
        image_path_sequence = []
        for layer in self.layers:
            image_path = layer.get_random_image_path()
            image_path_sequence.append(image_path)
        
        return image_path_sequence

    def render_avatar_image(self, image_path_sequence: List[str]):
        #print(image_path_sequence)
        if random() < self.rare_background_chance:
            bg_color = self.rare_background
        else:
            bg_color = self.background_color
        image = Image.new("RGBA",(24,24), bg_color)
        for image_path in image_path_sequence:
            layer_image= Image.open(image_path)
            image = Image.alpha_composite(image, layer_image)
        return image

    def save_image(self, image: Image.Image, i: int=0):
        image_index = str(i).zfill(4)
        image_filename = f"avatar_{image_index}.png"
        image_save_path = os.path.join(self.output_path, image_filename)
        image.save(image_save_path)

    def generate_avatar(self, n:int = 1):
        #print("yeett")
        for i in range(n):
            image_path_sequence = self.generate_image_sequence()
            #print("almost")
            #print(image_path_sequence )

            image = self.render_avatar_image(image_path_sequence= image_path_sequence)
            self.save_image(image, i)
            
            