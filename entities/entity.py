class Entity:
    def __init__(self, hp, time, atk_rate, atk, speed, range, pos_player):
        self.hp = hp
        self.time = time
        self.atk_rate = atk_rate
        self.atk = atk
        self.speed = speed
        self.range = range
        self.pos = list(pos_player)  # Convertir le tuple en liste

    def death(self):
        print('JORDAN T MORT')

    def heal(self,  heal):
        target_hp = self.hp + heal
        if target_hp > 100:
            target_hp = 100
        self.hp = target_hp

    def decrease_hp(self, damage):
        print(f"[DEBUG] decrease_hp appelé - HP avant: {self.hp}, Dégâts reçus: {damage}")
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        print(f"[DEBUG] HP après: {self.hp}")

    def attack(self, target, damage):
        print(f"[DEBUG] Entity.attack appelé - Dégâts: {damage}, Cible HP avant: {target.hp}")
        target.decrease_hp(damage)
        print(f"[DEBUG] Cible HP après: {target.hp}")

    def tick(self):
        pass

    def freeze_time(self):
        pass