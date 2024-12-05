import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import pygame
import threading
from PIL import Image, ImageTk

# Инициализация pygame для звуков
pygame.mixer.init()

# Загрузка звуков
sound_create = pygame.mixer.Sound('Connecting to satelite li - Converted Vocals.mp3')
sound_manual = pygame.mixer.Sound('Manual mode. Activated. - Converted Vocals.mp3')
sound_auto = pygame.mixer.Sound('Automatic control mode on - Converted Vocals.mp3')
sound_nuke = pygame.mixer.Sound('Nuclear missle. Launch. - Converted Vocals.mp3')
sound_target = pygame.mixer.Sound('Target destroyed. - Converted Vocals.mp3')
sound_fatal = pygame.mixer.Sound('Forced disconnection from - Converted Vocals.mp3')
sound_colonylost = pygame.mixer.Sound('Colony. Lost - Converted Vocals.mp3')
sound_economy = pygame.mixer.Sound('New Tiberium fabrics. Eng - Converted Vocals.mp3')
sound_transport = pygame.mixer.Sound('New transportions ships.  - Converted Vocals.mp3')
sound_enem = pygame.mixer.Sound('New enemies battleships.  - Converted Vocals.mp3')
sound_signal = pygame.mixer.Sound('Mission acomplished. Sign - Converted Vocals.mp3')
sound_victory = pygame.mixer.Sound('Commander. You have compl - Converted Vocals.mp3')

# Загрузка фоновой музыки
pygame.mixer.music.load('musi.mp3')
pygame.mixer.music.play(-1)  # Воспроизведение в цикле

# Классы для планет и корпораций
class CelestialBody:
    def __init__(self, name):
        self.name = name

class Planet(CelestialBody):
    def __init__(self, name, production, demand, technology):
        super().__init__(name)
        self.production = production
        self.demand = demand
        self.technology = technology
        self.health = 100  # Здоровье планеты

class Asteroid(CelestialBody):
    def __init__(self, name, resource_type, mining_cost):
        super().__init__(name)
        self.resource_type = resource_type
        self.mining_cost = mining_cost

class Corporation:
    def __init__(self, name):
        self.name = name

class LogisticsCompany(Corporation):
    def __init__(self, name):
        super().__init__(name)

class TechTrader(Corporation):
    def __init__(self, name):
        super().__init__(name)

class MinerCompany(Corporation):
    def __init__(self, name):
        super().__init__(name)

# Класс для игры
class GalacticEmpireGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Империя Звезд")
        self.root.configure(bg='black')  # Установка черного фона
        self.graph = nx.Graph()
        self.planets = []
        self.asteroids = []
        self.corporations = []
        self.current_turn = 0
        self.profit = 0
        self.auto_turn_active = False
        self.resource_prices = {}
        self.attack_threshold = 500
        self.nuke_cost = 500  # Стоимость ядерной ракеты
        self.planet_destruction_penalty = 250  # Штраф за уничтожение планеты
        self.economy_development_cost = 350  # Стоимость развития экономики
        self.transport_development_cost = 600  # Стоимость развития транспортных путей
        self.victory_threshold = 1000 # Порог победы

        self.create_ui()

    def create_ui(self):
        self.frame = tk.Frame(self.root, bg='black')  # Установка черного фона для фрейма
        self.frame.pack()

        # Загрузка изображения
        self.image = Image.open("AI.jpg")
        self.photo = ImageTk.PhotoImage(self.image)

        # Создание метки для изображения
        self.image_label = tk.Label(self.frame, image=self.photo, bg='black')
        self.image_label.pack(side=tk.TOP, anchor=tk.NW)

        # Добавление надписи рядом с изображением
        self.text_label = tk.Label(self.frame, text="...To punish and enslave.", bg='black', fg='white')
        self.text_label.pack(side=tk.TOP, anchor=tk.NW)

        self.create_button = tk.Button(self.frame, text="Подключится к сети спутников", command=self.create_galaxy, bg='black', fg='white')
        self.create_button.pack()

        self.turn_button = tk.Button(self.frame, text="Следующий Ход", command=self.next_turn, bg='black', fg='white')
        self.turn_button.pack()

        self.auto_turn_button = tk.Button(self.frame, text="Автоматический контроль экономики", command=self.toggle_auto_turn, bg='black', fg='white')
        self.auto_turn_button.pack()

        self.nuke_button = tk.Button(self.frame, text="Ядерная ракета", command=self.launch_nuke, bg='yellow', fg='black')
        self.nuke_button.pack()

        self.economy_button = tk.Button(self.frame, text="Строительство новых заводов", command=self.develop_economy, bg='green', fg='white')
        self.economy_button.pack()

        self.transport_button = tk.Button(self.frame, text="Покупка новых транспортных кораблей", command=self.develop_transport, bg='blue', fg='white')
        self.transport_button.pack()

        self.profit_label = tk.Label(self.frame, text="Тиберий: 0", bg='black', fg='white')
        self.profit_label.pack()

        self.figure = plt.figure(figsize=(10, 8))  # Увеличение размера поля игры
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame)
        self.canvas.get_tk_widget().pack()

    def create_galaxy(self):
        sound_create.play()
        self.planets = [
            Planet("Colony Alpha", {"Food": 10}, {"Energy": 5}, 5),
            Planet("Colony Beta", {"Minerals": 15}, {"Food": 10}, 3),
            Planet("Colony Charlie", {"Energy": 20}, {"Minerals": 15}, 4),
            Planet("Colony Gamma", {"Minerals": 25}, {"Energy": 10}, 6),
            Planet("Colony Theta", {"Energy": 30}, {"Food": 20}, 5),
            Planet("Colony Delta", {"Food": 15}, {"Minerals": 10}, 4),
            Planet("Colony Epsilon", {"Energy": 25}, {"Food": 15}, 5),
            Planet("Colony Zeta", {"Minerals": 20}, {"Energy": 15}, 6)
        ]

        self.asteroids = [
            Asteroid("Neo-Erzatz", "Minerals", 5),
            Asteroid("Monika De Kreuzez", "Energy", 3),
            Asteroid("Armada", "Minerals", 4),
            Asteroid("ScreamStar", "Energy", 2),
            Asteroid("EagleWipe", "Minerals", 6),
            Asteroid("Azure", "Energy", 4)
        ]

        self.corporations = [
            LogisticsCompany("LogisticsCorp"),
            TechTrader("TechTraderCorp"),
            MinerCompany("MinerCorp")
        ]

        self.graph.add_nodes_from([(p.name, {"type": "planet"}) for p in self.planets])
        self.graph.add_nodes_from([(a.name, {"type": "asteroid"}) for a in self.asteroids])

        self.graph.add_edge("Colony Alpha", "Colony Beta", weight=10, safety=0.9)
        self.graph.add_edge("Colony Beta", "Colony Charlie", weight=15, safety=0.8)
        self.graph.add_edge("Colony Charlie", "Colony Alpha", weight=20, safety=0.7)
        self.graph.add_edge("Colony Gamma", "Colony Theta", weight=25, safety=0.8)
        self.graph.add_edge("Colony Theta", "Colony Alpha", weight=30, safety=0.7)
        self.graph.add_edge("Colony Delta", "Colony Epsilon", weight=20, safety=0.8)
        self.graph.add_edge("Colony Epsilon", "Colony Zeta", weight=25, safety=0.7)
        self.graph.add_edge("Colony Zeta", "Colony Delta", weight=30, safety=0.8)

        self.draw_graph()

    def draw_graph(self):
        pos = nx.spring_layout(self.graph)
        plt.clf()
        planet_nodes = [n for n, d in self.graph.nodes(data=True) if d['type'] == 'planet']
        asteroid_nodes = [n for n, d in self.graph.nodes(data=True) if d['type'] == 'asteroid']
        nx.draw_networkx_nodes(self.graph, pos, nodelist=planet_nodes, node_color='green', node_size=2000)
        nx.draw_networkx_nodes(self.graph, pos, nodelist=asteroid_nodes, node_color='red', node_size=2000)
        nx.draw_networkx_edges(self.graph, pos)
        nx.draw_networkx_labels(self.graph, pos)
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
        self.canvas.draw()

    def next_turn(self):
        self.current_turn += 1
        self.profit += self.calculate_profit()  # Улучшенная логика прибыли
        self.profit_label.config(text=f"Тиберий: {self.profit}")
        self.update_resource_prices()
        self.handle_asteroid_attacks()
        self.add_new_asteroids()
        self.draw_graph()

        if not self.planets:
            self.end_game("Все колонии уничтожены. Игра окончена.")
        elif self.profit >= self.victory_threshold:
            sound_signal.play()
            self.end_game("Победа! Вы развили сеть колоний и выполнили поставленную вам задачу!")

    def calculate_profit(self):
        profit = 0
        for planet in self.planets:
            for resource, amount in planet.production.items():
                profit += amount * self.resource_prices.get(resource, 1)
            for resource, amount in planet.demand.items():
                profit -= amount * self.resource_prices.get(resource, 1)

        for asteroid in self.asteroids:
            profit -= asteroid.mining_cost
            profit += random.randint(1, 5) * self.resource_prices.get(asteroid.resource_type, 1)

        return profit

    def update_resource_prices(self):
        for resource in ["Food", "Energy", "Minerals"]:
            self.resource_prices[resource] = random.randint(1, 10)

    def handle_asteroid_attacks(self):
        if not self.planets:
            sound_fatal.play()
            return

        if self.profit > self.attack_threshold:
            for asteroid in self.asteroids:
                if random.random() < 0.5:  # 50% шанс атаки астероида
                    target_planet = random.choice(self.planets)
                    target_planet.health -= 10
                    if target_planet.health <= 0:
                        self.planets.remove(target_planet)
                        self.graph.remove_node(target_planet.name)
                        self.profit -= self.planet_destruction_penalty  # Списание 250 тиберия
                        self.profit_label.config(text=f"Тиберий: {self.profit}")
                        messagebox.showinfo("Атака вражеского линкора", f"Линкор {asteroid.name} уничтожил колонию {target_planet.name}! Пропало 250 тиберия.")
                        sound_colonylost.play()

    def add_new_asteroids(self):
        if self.current_turn % 5 == 0:
            new_asteroids = [
                Asteroid(f"Schl.Sc.Kr.-X{len(self.asteroids) + 1}", "Minerals", 5),
                Asteroid(f"Schl.Sc.Lt.-X{len(self.asteroids) + 2}", "Energy", 3)
            ]
            self.asteroids.extend(new_asteroids)
            self.graph.add_nodes_from([(a.name, {"type": "asteroid"}) for a in new_asteroids])
            sound_enem.play()
            messagebox.showinfo("Прибытие новых сил противника", f"Прибыли новые вражеские линкоры! {new_asteroids[0].name} и {new_asteroids[1].name}!")

    def launch_nuke(self):
        if not self.asteroids:
            messagebox.showinfo("Ядерная ракета", "Целей для ядерной ракеты нет!")
            return

        if self.profit >= self.nuke_cost:
            sound_nuke.play()
            self.profit -= self.nuke_cost  # Вычитаем стоимость ракеты
            self.profit_label.config(text=f"Тиберий: {self.profit}")
            selected_asteroid = random.choice(self.asteroids)
            if random.random() < 0.75:  # 75% шанс уничтожения астероида
                self.asteroids.remove(selected_asteroid)
                self.graph.remove_node(selected_asteroid.name)
                messagebox.showinfo("Ядерная ракета", f"Ядерная ракета уничтожила вражеский линкор {selected_asteroid.name}!")
                sound_target.play()
            else:
                messagebox.showinfo("Ядерная ракета", "Ядерная ракета промахнулась!")
        else:
            messagebox.showinfo("Ядерная ракета", "Недостаточно Тиберия для запуска ядерной ракеты!")

    def develop_economy(self):
        if self.profit >= self.economy_development_cost:
            sound_economy.play()
            self.profit -= self.economy_development_cost
            self.profit_label.config(text=f"Тиберий: {self.profit}")
            for planet in self.planets:
                for resource, amount in planet.production.items():
                    planet.production[resource] *= 1.2  # Увеличение выработки на 20%
            messagebox.showinfo("Развитие экономики", "Экономика колоний улучшена! Выработка тиберия увеличена на 20%.")
        else:
            messagebox.showinfo("Развитие экономики", "Недостаточно Тиберия для развития экономики!")

    def develop_transport(self):
        if self.profit >= self.transport_development_cost:
            sound_transport.play()
            self.profit -= self.transport_development_cost
            self.profit_label.config(text=f"Тиберий: {self.profit}")
            for u, v, d in self.graph.edges(data=True):
                d['weight'] *= 0.8  # Снижение затрат топлива на 20%
            messagebox.showinfo("Запрос новых кораблей", "Новые транспортники прибыли! Затраты топлива снижены на 20%.")
        else:
            messagebox.showinfo("Запрос новых кораблей", "Недостаточно Тиберия для покупки новых транспортников!")

    def toggle_auto_turn(self):
        if self.auto_turn_active:
            sound_manual.play()
            self.auto_turn_active = False
            self.auto_turn_button.config(text="Автоматический контроль экономики")
        else:
            self.auto_turn_active = True
            self.auto_turn_button.config(text="Ручной контроль экономики")
            self.start_auto_turn()
            sound_auto.play()

    def start_auto_turn(self):
        if self.auto_turn_active:
            self.next_turn()
            threading.Timer(5.0, self.start_auto_turn).start()

    def end_game(self, message):
        messagebox.showinfo("Конец игры", message)
        if "Победа" in message:
            self.show_victory_menu()
        else:
            sound_fatal.play()

    def show_victory_menu(self):
        sound_victory.play()
        victory_window = tk.Toplevel(self.root)
        victory_window.title("Конец игры.")
        victory_window.configure(bg='black')

        # Загрузка изображения
        victory_image = Image.open("Kane.jpg")
        victory_photo = ImageTk.PhotoImage(victory_image)

        # Создание метки для изображения
        victory_image_label = tk.Label(victory_window, image=victory_photo, bg='black')
        victory_image_label.image = victory_photo  # Сохранение ссылки на изображение
        victory_image_label.pack(side=tk.TOP, anchor=tk.NW)

        # Добавление надписи рядом с изображением
        victory_text_label = tk.Label(victory_window, text="Commander. You have completed the task assigned to you, ", bg='black', fg='red', font=("Helvetica", 12))
        victory_text_label.pack(side=tk.TOP, anchor=tk.NW)

        victory_text_label = tk.Label(victory_window, text="you have ensured the development of the economy on the colonies allocated to you.", bg='black', fg='red', font=("Helvetica", 12))
        victory_text_label.pack(side=tk.TOP, anchor=tk.NW)

        victory_text_label = tk.Label(victory_window, text="Troops of the NOD brotherhood have been sent to this region, so you can proceed to the next tasks. Thank you for your service to the brotherhood.", bg='black', fg='red', font=("Helvetica", 12))
        victory_text_label.pack(side=tk.TOP, anchor=tk.NW)

if __name__ == "__main__":
    root = tk.Tk()
    game = GalacticEmpireGame(root)
    root.mainloop()