import os # imported for Operating system functionality for terminal clear
import random
import json


#inventory weapon dictionary item (key) and gold cost (value) to implement
#shop and inventory functionality
store_inventory = { 
                   "health_potion": {"price": 10, "effect": "restores 50 health"},
                   "sword": {"price": 100, "effect": "increases attack power by 10"},
                   "great_sword": {"price": 200, "effect":" greatly increases attack power by 15"},
                   "shield": {"price": 75, "effect": "increases defense by 5"},
                   "iron_shield": {"price": 200, "effect":" greatly increases defense power by 10"},
}

# Save Functionality for the game
def save_game(player, wizard, filename='save_file.json'):
    #defining player data to be saved, will update as game evolves
    game_data = {
        "player": 
            { "name": player.name,
             "class": type(player).__name__,
             "health": player.health,
             "attack_power": player.base_attack,
             "defense": player.defense,
             "health_potions": player.health_potions,
             "evasion": player.evasion,
             "gold": player.gold},
            "wizard": wizard.__dict__ 
            }
    #declaring a file name and 'w' for write
    with open(filename, 'w') as file:
        json.dump(game_data, file) 
        print("Game saved!")
# Load functionality for the game
def load_game(filename="save_file.json"):
    try: 
        # declares file name and 'r' for read
        with open(filename, 'r') as file:
            game_data = json.load(file) 
            print("Loaded game!") 
            return game_data
        # Returns No file found if no saves detected
    except FileNotFoundError: 
        print("No file found") 
        return None
    
# Base Enemy class, elected to separate Enemy and Player Classes as I may
# want attributes assigned to enemies that dont belong to character
class Enemy:
    def __init__(self, name, health, attack_power, 
                 evasion = .2, gold_gain=25, defense = 15): 
        self.name = name
        self.health = health
        self.base_attack = attack_power
        self.max_health = health
        self.evasion = evasion
        self.gold_gain = gold_gain
        self.defense = defense
    
    #attack functionality with built in evasion and a modifier 
    # to base_attack with random increase from 1-10
    def attack(self, opponent):
        if random.random() < opponent.evasion:
            print(f"{opponent.name} dodges!")
        else:
            actual_attack = (self.base_attack + random.randint(1,10))
            opponent.health -= actual_attack
            print(f"{self.name} attacks {opponent.name} for {actual_attack} damage!")
            if opponent.health <= 0:
                print(f"{opponent.name} has been defeated!")
    #display stat functionality
    def display_stats(self):
        return (f"{self.name}'s Stats\n"
                f"Health: {self.health}/{self.max_health}\n"
                f"Attack Power: {self.base_attack}\n"
                f"Defense: {self.defense}\n"
                f"Evasion: {self.evasion}%\n"
                f"Gold Held: {self.gold_gain}\n")
                


# Base character. Any and all characters created shart these attributes        
class Character:
    def __init__(self, name, health, attack_power, health_potions=0, evasion = .2,
                 gold = 0, defense = 10):
        self.name = name
        self.health = health
        self.base_attack = attack_power
        self.max_health = health
        self.health_potions = health_potions    
        self.evasion = evasion
        self.gold = gold
        self.defense = defense
        self.weapons = ["Rusty Sword"]
        self.current_weapon = ["Rusty Sword"]
        self.armor = []
        self.current_armor = []
    #    
    @property
    def weapon_attack(self):
        attack = self.base_attack
        if self.current_weapon == "Rusty Sword":
            attack += 5
        elif self.current_weapon == "Great Sword":
            attack += 15
            
        return attack
# standard attack with built in dodge  
    def attack(self, opponent):
        if random.random() < opponent.evasion:
            print(f"{opponent.name} dodges!")
        else:
            actual_attack = (self.base_attack + random.randint(1,10) - opponent.defense)
            opponent.health -= actual_attack
            print(f"{self.name} attacks {opponent.name} for {actual_attack} damage!")
            if opponent.health <= 0:
                print(f"{opponent.name} has been defeated!")
#Healing function. Each character starts with 0 potions. Will define amount in
# sub class. When store is added potion count can be increased            
    def drink_health_potion(self):
        os.system('cls')
        if self.health_potions == 0:
            print("You don't have any potions!")
        else:
            self.health += 100 #value of potion
            self.health_potions -=1 #decrease the number of health potions
        if self.health > self.max_health:
            self.health = self.max_health
            print(f"You drank a potion and are now at {self.health} health!")
            print(self.display_stats())
    # displays stats, as more attributes are added this will need updated               
    def display_stats(self):
        return (f"{self.name}'s Stats\n" 
                f"Health: {self.health}/{self.max_health}\n"
                f"Attack Power: {self.base_attack}\n"
                f"Health Potions: {self.health_potions}\n"
                f"Evasion: {self.evasion}%\n"
                f"Defense: {self.defense}\n"
                f"Gold: {self.gold}\n"
                f"Current Weapon: {self.current_weapon}")
        
    
   # Store functionality 
    def display_store(self):
        os.system('cls') 
        print("\n--- Welcome to the Shop Adventurer ---") 
        for item, effect in store_inventory.items():
            print(f"{item.capitalize()}:{effect['price']} gold - {effect['effect']}") 
            print("-----------------------------")
        
    def purchase_item(self):  
        choice = input("Enter the item you want to buy or 'exit' to leave the store: ").lower() 
        if choice == 'exit':
            print("Leaving the store.")
            return
        if choice in store_inventory:
            item = store_inventory[choice] 
            if self.gold >= item['price']: 
                self.gold -= item['price']
                if choice == "health_potion":
                    self.health_potions += 1 
                elif choice == "sword":
                    self.base_attack += 5 
                elif choice == "shield":
                    self.defense += 5
                elif choice == "iron_shield":
                    self.defense += 10
                elif choice == "great_sword":
                    self.base_attack = 15
                    
                
                print(f"You bought a {choice}!") 
            else: print("You don't have enough gold to buy this item.") 
            
        else: print("Invalid choice. Please select a valid item.") 
        

# Hero class (inherits from Character) 
class Hero(Character):
    def __init__(self, name,):
        super().__init__(name, health=140, attack_power=25, health_potions=2,
                         defense=10) 
# Special attack menu. Each sub class will have one that differs based on 
# Moves within their character      
    def special_attack_menu(self, opponent):
        os.system('cls')
        print("1. Heavy Swing")
        print("2. Heroic Strike")
        print("3. Return to menu")
        option = input("--> ")
        os.system('cls') #utilized to clear terminal for readability and user
                        #quality of life
        # calls ability functions designed in instances of Character Class
        if option == '1':
            self.heavy_swing(opponent) # calls heavy swing from hero class
        elif option == '2':
            self.heroic_strike(opponent) # calls heroic strike from hero class
        elif option == '3':
            pass
        else:
            print("Invalid Choice, no special attack performed. ")
            
    # Special attack for the hero class
    # Standard power attack with defense 
    def heavy_swing(self, opponent):
        damage = (self.base_attack * 1.5) - opponent.defense
        opponent.health -= damage 
        print(f"{self.name} uses Heavy Swing on {opponent.name} for {damage} damage!") 
        input(" ")
        if opponent.health <= 0: 
            print(f"{opponent.name} has been defeated!")
            
    def heroic_strike(self, opponent):
        damage = (self.base_attack * 1.5) - opponent.defense 
        opponent.health -= damage 
        opponent.evasion -= .2 # removes ability for enemy to evade this attack
        print(f"{self.name} uses Heroic Strike on {opponent.name} for {damage} damage!") 
        input(" ")
        if opponent.health <= 0: 
            print(f"{opponent.name} has been defeated!")

# Bandit class (inherits from Character)
class Bandit(Character):
    def __init__(self, name,):
        super().__init__(name, health=100, attack_power=25, health_potions=2)

    def special_attack_menu(self, opponent):
        os.system('cls')
        print("1. Life Steal")
        print("2. Evade")
        print("3. Return to menu")
        option = input("\nChoose a special attack:")
        os.system('cls')
        
        if option == '1':
            self.life_steal(opponent) 
        elif option == '2':
            self.evade(opponent)
        elif option == '3':
            pass
        else:
            print("Invalid Choice, no special attack performed. ")
        
    def life_steal(self, opponent): # weaker attack that drains health from opponent
        acutal_damage = (self.base_attack + random.randint(1,10)) * .75 
        opponent.health -= acutal_damage 
        print(f"{self.name} uses Life Steal on {opponent.name} for {acutal_damage} damage!")
        self.health += acutal_damage * .2
        print(f"{self.name} heals for " + str(round(acutal_damage * .2)))
        input(" ")
        if opponent.health <= 0: 
            print(f"{opponent.name} has been defeated!") 
            
    def evade(self, opponent):
        self.evasion += .30 # increases evasion to %50
        print(f"{self.name} casts evade om {self.name} and increased evasion to %50!")
        input(" ")

# Astrologer class (inherits from Character)
class Astrologer(Character):
    def __init__(self, name):
        super().__init__(name, health=150, attack_power=20, health_potions=2)
    
    def special_attack_menu(self, opponent):
        os.system('cls')
        print("1. Look to the Stars")
        print("2. Astrologer's Healing")
        print("3. Return to menu")
        option = input("\nChoose a special attack:")
        os.system('cls')
        
        if option == '1':
            self.look_to_the_stars(opponent)
        elif option == '2':
            self.astrologers_healing(opponent)
        elif option == '3':
            pass
        else:
            print("Invalid Choice, no special attack performed. ")
        
    def look_to_the_stars(self, opponent):
        self.base_attack += 10 # buff for player
        print(f"{self.name} uses Look to the Stars on {self.name} and increases Attack Power by 10!")
        input(" ")
        
    def astrologers_healing(self, opponent):
        self.health += 30 #casts a heal
        input(" ")
        print(f"{self.name} regenerates 30 health. ! Current health: {self.health}")
        
# Warrior class (inherits from Character)
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health=100, attack_power=35, health_potions=2)
        
    def special_attack_menu(self, opponent):
        os.system('cls')
        print("1. Roar")
        print("2. Berserk")
        print("3. Return to menu")
        option = input("\nChoose a special attack:")
        os.system('cls')
        
        if option == '1':
            self.roar(opponent)
        elif option == '2':
            self.beserk(opponent)
        elif option == '3':
            pass
        else:
            print("Invalid Choice, no special attack performed. ")
             
    def roar (self, opponent):
        opponent.base_attack -= opponent.base_attack *.75 # debuff for opponent
        print(f"{self.name} uses Roar on {opponent.name} and decrease their attack by 25%!")
        input(" ")
        
    def beserk(self,opponent):
        self.base_attack += 10 # buff for player
        print(f"{self.name} uses Berserk on {self.name} and increases their attack by 10!")
        input(" ")
        

# THESE CLASSES ARE UNDER DEVELOPMENT

# # Prisoner class (inherits from Character)
# class Prisoner(Character):
#     def __init__(self, name):
#         super().__init__(name, health=100, attack_power=35)

# # Confessor class (inherits from Character)
# class Confessor(Character):
#     def __init__(self, name):
#         super().__init__(name, health=100, attack_power=35)  

# # Wretch class (inherits from Character)
# class Wretch(Character):
#     def __init__(self, name):
#         super().__init__(name, health=100, attack_power=35)  # Boost attack power

# # Vagabond class (inherits from Character)
# class Vagabond(Character):
#     def __init__(self, name):
#         super().__init__(name, health=100, attack_power=35)  # Boost attack power

# # Prophet class (inherits from Character)
# class Prophet(Character):
#     def __init__(self, name):
#         super().__init__(name, health=100, attack_power=35)  # Boost attack power

# # Samurai class (inherits from Character)
# class Samurai(Character):
#     def __init__(self, name):
#         super().__init__(name, health=100, attack_power=35)  # Boost attack power


# EvilWizard class (inherits from Character)
class EvilWizard(Enemy):
    def __init__(self, name):
        super().__init__(name, health=150, attack_power=15)  # Lower attack power
    
    # Evil Wizard's special ability: it can regenerate health
    def regenerate(self):
        self.health += 5 
        print(f"{self.name} regenerates 5 health! Current health: {self.health}")
     # evil wizards fireball attack that does fixed damage   
    def fireball(self, opponent):
        damage = 40
        opponent.health -= damage
        print(f"{self.name} casts Fireball on {opponent.name} for {damage} damage!")
        
class Goblin(Enemy):
    def __init__(self, name):
        super().__init__(name, health=150, attack_power=15, gold_gain = 30)  # Lower attack power

# Function to create player character based on user input and load if character
# created previously
def create_character():
    print("Please choose an option: ")
    print("1. New Game")
    print("2. Load Game")
    option = input("--> ")
    os.system('cls')
    if option == "1":
        print("Choose your character class:")
        print("1. Hero")
        print("2. Bandit")
        print("3. Astrologer") 
        print("4. Warrior") 
        # print("5. Prisoner")  These classes are still under development
        # print("6. Confessor")  
        # print("7. Wretch")  
        # print("8. Vagabond")  
        # print("9. Prophet")  
        # print("0. Samurai")  
        
        # User input for character class choice and name
        class_choice = input("--> ")
        os.system('cls')
        name = input("Enter your character's name: ")
        os.system('cls')

        if class_choice == '1':
            return Hero(name)
        elif class_choice == '2':
            return Bandit(name)
        elif class_choice == '3':
            return Astrologer(name)
        elif class_choice == '4':
            return Warrior(name)
        # elif class_choice == '5': # Under Development
        #     return Prisoner(name)
        # elif class_choice == '6':
        #     return Confessor(name)
        # elif class_choice == '7':
        #     return Wretch(name)
        # elif class_choice == '8':
        #     return Vagabond(name)
        # elif class_choice == '9':
        #     return Prophet(name)
        # elif class_choice == '0':
        #     return Samurai(name)
        else:
            print("Invalid choice. Defaulting to Hero.")
            return Hero(name)
    elif option == '2':
        #load functiuonality defined below. as more attributes are added this
        #will need to be updated
        data = load_game() 
        if data:
            class_name = data["player"]["class"] 
            name = data["player"]["name"] 
            health = data["player"]["health"] 
            attack_power = data["player"]["attack_power"] 
            health_potions = data["player"]["health_potions"] 
            evasion = data["player"]["evasion"] 
            defense = data["player"]["defense"]
            gold = data["player"]["gold"]
            
            if class_name == "Hero": 
                player = Hero(name) 
            elif class_name == "Bandit":
                player = Bandit(name) 
            elif class_name == "Astrologer": 
                player = Astrologer(name) 
            elif class_name == "Warrior": 
                player = Warrior(name) 
                
            player.health = health 
            player.base_attack = attack_power 
            player.health_potions = health_potions 
            player.evasion = evasion 
            player.defense = defense
            player.gold = gold
            return player 
        else: return create_character() 
    else: 
        print("Please enter a valid option") 
        return create_character()

# Battle function with user menu for actions
def battle(player, wizard):
    while wizard.health > 0 and player.health > 0:
        print("\n--- Your Turn ---")
        print("1. Attack")
        print("2. Use Special Ability")
        print("3. Drink Potion")
        print("4. View Stats")
        print("5. Visit Shop")
        print("5. Save\n")
        # Gets stats as formatted strings
        player_stats = player.display_stats().split('\n') 
        wizard_stats = wizard.display_stats().split('\n')
        # Print stats side by side in columns
        for p_stat, w_stat in zip(player_stats, wizard_stats): 
            print(f"{p_stat:<40} {w_stat}")

        choice = input("\n-->")

        if choice == '1':
            os.system('cls')
            player.attack(wizard)
            input(" ")
        elif choice == '2':
            player.special_attack_menu(wizard or player) 
        elif choice == '3':
            player.drink_health_potion()
        elif choice == '4':
            # print stats side by side when viewing stats
            # zip takes two or more iterables and combines them into pairs.
            for p_stat, w_stat in zip(player.display_stats().split('\n'), 
                                      wizard.display_stats().split('\n')): 
                print(f"{p_stat:<40} {w_stat}")
        elif choice == '5':
            player.display_store()
            player.purchase_item()
        elif choice == '6':
            save_game(player, wizard)
        else:
            print("Invalid choice, try again.")
            continue

        # Evil Wizard's turn to attack, randomly cast fireball, and regen each
        #turn 
        if wizard.health > 0:
            if random.random() < .35: #percentage of time for fireball to exec.
                wizard.fireball(player)
            else:
                wizard.attack(player)     
            wizard.regenerate() 
            input(" ")
            os.system('cls')
            
        if player.health <= 0:
            print(f"{player.name} has been defeated!")
            break

    if wizard.health <= 0:
        print(f"The {wizard.name} has been defeated by {player.name}!")

# Main function to handle the flow of the game
def main():
    os.system('cls')
    # Character creation phase
    player = create_character()

    # Evil Wizard is created
    wizard = EvilWizard("The Dark Wizard")

    # Start the battle
    battle(player, wizard)

if __name__ == "__main__":
    main()
    
    
