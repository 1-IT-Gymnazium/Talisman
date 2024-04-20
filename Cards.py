import Classes

# Initializing a list of Character objects with specified attributes.
characters = [
    Classes.Character("Assassin", "./Characters/Assassin.png", 3, 3, 4, 3, 1, "Evil", "City"),
    Classes.Character("Druid", "./Characters/Druid.png", 2, 4, 4, 4, 1, "Neutral", "Chapel"),
    Classes.Character("Dwarf", "./Characters/Dwarf.png", 3, 3, 5, 5, 1, "Neutral", "Cracks"),
    Classes.Character("Elf", "./Characters/Elf.png", 3, 4, 4, 3, 1, "Good", "ElvForest"),
    Classes.Character("Ghoul", "./Characters/Ghoul.png", 2, 4, 4, 4, 1, "Evil", "Village"),
    Classes.Character("Minstrel", "./Characters/Minstrel.png", 2, 4, 4, 5, 1, "Good", "Tavern"),
    Classes.Character("Monk", "./Characters/Monk.png", 2, 3, 4, 5, 1, "Good", "Village"),
    Classes.Character("Priest", "./Characters/Priest.png", 2, 4, 4, 5, 1, "Good", "Chapel"),
    Classes.Character("Prophetess", "./Characters/Prophetess.png", 2, 4, 4, 2, 1, "Good", "Chapel"),
    Classes.Character("Sorceress", "./Characters/Sorceress.png", 2, 4, 4, 3, 1, "Evil", "City"),
    Classes.Character("Thief", "./Characters/Thief.png", 3, 3, 4, 2, 1, "Neutral", "City"),
    Classes.Character("Troll", "./Characters/Troll.png", 6, 1, 6, 1, 1, "Neutral", "Cracks"),
    Classes.Character("Wizard", "./Characters/Wizard.png", 2, 5, 4, 3, 1, "Evil", "Chapel"),
    Classes.Character("Warrior", "./Characters/Warrior.png", 4, 2, 5, 1, 1, "Neutral", "Tavern")
]
"""
Each Character object is initialized with various attributes:
- name (str): The character's name.
- image (str): Path to the character's image file.
- strength (int): The character's strength attribute.
- craft (int): The character's craft attribute.
- life (int): The character's life points.
- fate (int): The character's fate points.
- gold (int): The amount of gold the character starts with.
- alignment (str): The character's alignment (e.g., "Evil", "Neutral", "Good").
- start (str): The starting location on the game board.
"""

# Initializing a list of Enemy cards for the game.
enemycards = [
    Classes.Enemy("Ape", "./EnemyCards/Ape.png", "yep", 0, 3),
    Classes.Enemy("Bandit", "./EnemyCards/Bandit.png", "yep", 0, 4),
    Classes.Enemy("Bear", "./EnemyCards/Bear.png", "yep", 0, 3),
    Classes.Enemy("Demon", "./EnemyCards/Demon.png", "yep", 10, 0),
    Classes.Enemy("Dopplergang", "./EnemyCards/Dopplergang.png", "yep", 0, 7),
    Classes.Enemy("Dragon", "./EnemyCards/Dragon.png", "yep", 0, 7),
    Classes.Enemy("Ghost", "./EnemyCards/Ghost.png", "yep", 4, 0),
    Classes.Enemy("Giant", "./EnemyCards/Giant.png", "yep", 0, 6),
    Classes.Enemy("Goblin", "./EnemyCards/Goblin.png", "yep", 0, 2),
    Classes.Enemy("Hobgoblin", "./EnemyCards/Hobgoblin.png", "yep", 0, 3),
    Classes.Enemy("Lemure", "./EnemyCards/Lemure.png", "yep", 1, 0),
    Classes.Enemy("Lion", "./EnemyCards/Lion.png", "yep", 0, 3),
    Classes.Enemy("Orge", "./EnemyCards/Orge.png", "yep", 0, 5),
    Classes.Enemy("Serpent", "./EnemyCards/Serpent.png", "yep", 0, 4),
    Classes.Enemy("Shadow", "./EnemyCards/Shadow.png", "yep", 2, 0),
    Classes.Enemy("Spectre", "./EnemyCards/Spectre.png", "yep", 3, 0),
    Classes.Enemy("WildBoar", "./EnemyCards/WildBoar.png", "yep", 0, 1),
    Classes.Enemy("Wolf", "./EnemyCards/Wolf.png", "yep", 0, 2),
    Classes.Enemy("Wraith", "./EnemyCards/Wraith.png", "yep", 5, 0),
    Classes.Enemy("Farmer", "./EnemyCards/Farmer.png", "yep", 0, 3)
]
"""
Each Enemy object represents an antagonist in the game:
- name (str): The name of the enemy.
- image (str): Path to the enemy's image file.
- effect (str): Description of the effect (currently placeholder "yep").
- craft (str): The enemy's craft value, important for craft battles.
- strength (str): The enemy's strength value, used in strength battles.
"""

# Initializing a list of Object cards that players can collect during the game.
objectcards = [
    Classes.ObjectCard("Armour", "./ObjectCards/Armour.png", "yep"),
    Classes.ObjectCard("Axe", "./ObjectCards/Axe.png", "add_strength", 1),
    Classes.ObjectCard("BagOfGold", "./ObjectCards/BagOfGold.png", "give_gold", 1),
    Classes.ObjectCard("Helmet", "./ObjectCards/Helmet.png", "yep"),
    Classes.ObjectCard("Shield", "./ObjectCards/Shield.png", "yep"),
    Classes.ObjectCard("Sword", "./ObjectCards/Sword.png", "add_strength", 1),
    Classes.ObjectCard("TwoBagsOfGold", "./ObjectCards/TwoBagsOfGold.png", "give_gold", 2),
    Classes.ObjectCard("WaterBottle", "./ObjectCards/WaterBottle.png", "yep"),
]
"""
ObjectCard is used for items that players can use:
- name (str): The name of the object.
- image (str): Path to the object's image file.
- effect (str): The effect of the object (e.g., "add_strength" to increase player strength).
- effect_value (int, optional): The value by which the effect modifies the player's attribute.
"""

# Initializing a list of Follower cards that can accompany characters.
followercards = [
    Classes.Follower("Alchemist", "./FollowerCards/Alchemist.png", "yep"),
    Classes.Follower("Gnome", "./FollowerCards/Gnome.png", "yep"),
    Classes.Follower("Guide", "./FollowerCards/Guide.png", "yep"),
    Classes.Follower("Hag", "./FollowerCards/Hag.png", "yep"),
    Classes.Follower("Maiden", "./FollowerCards/Maiden.png", "add_craft", 2),
    Classes.Follower("Mercenary", "./FollowerCards/Mercenary.png", "yep"),
    Classes.Follower("Mule", "./FollowerCards/Mule.png", "yep"),
    Classes.Follower("Pixie", "./FollowerCards/Pixie.png", "yep"),
    Classes.Follower("Poltergeist", "./FollowerCards/Poltergeist.png", "yep"),
    Classes.Follower("Prince", "./FollowerCards/Prince.png", "yep"),
    Classes.Follower("Princess", "./FollowerCards/Princess.png", "yep"),
    Classes.Follower("Unicorn", "./FollowerCards/Unicorn.png", "add_both", 1)
]
"""
Follower cards represent allies or companions:
- name (str): The name of the follower.
- image (str): Path to the follower's image file.
- effect (str): The specific assistance or boost provided by the follower.
- effect_value (int, optional): The numerical enhancement to character attributes.
"""

# Initializing a list of Magic Object cards that impart special abilities or bonuses.
magicobjectcards = [
    Classes.MagicObject("Amulet", "./MagicObjects/Amulet.png", "yep"),
    Classes.MagicObject("Cross", "./MagicObjects/Cross.png", "yep"),
    Classes.MagicObject("HolyGrail", "./MagicObjects/HolyGrail.png", "add_craft", 1),
    Classes.MagicObject("HolyLance", "./MagicObjects/HolyLance.png", "add_strength", 1),
    Classes.MagicObject("MagicBelt", "./MagicObjects/MagicBelt.png", "add_strength", 1),
    Classes.MagicObject("OrbOfKnowledge", "./MagicObjects/OrbOfKnowledge.png", "yep"),
    Classes.MagicObject("PotionOfStrength", "./MagicObjects/PotionOfStrength.png", "yep"),
    Classes.MagicObject("Ring", "./MagicObjects/Ring.png", "give_both", 1),
    Classes.MagicObject("RuneSword", "./MagicObjects/RuneSword.png", "add_strength", 1),
    Classes.MagicObject("SolomonCrown", "./MagicObjects/SolomonCrown.png", "add_craft", 2),
    Classes.MagicObject("Talisman", "./MagicObjects/Talisman.png", "yep"),
    Classes.MagicObject("Wand", "./MagicObjects/Wand.png", "yep"),
]
"""
MagicObject cards provide magical enhancements or abilities:
- name (str): The name of the magic object.
- image (str): Path to the magic object's image file.
- effect (str): The type of magic effect provided by the object.
- effect_value (int, optional): The value of the magical effect, modifying character stats or abilities.
"""

strangercards = [
    Classes.Stranger("Enchanter", "./StrangerCards/Enchanter.png", "yep"),
    Classes.Stranger("Fairy", "./StrangerCards/Fairy.png", "yep"),
    Classes.Stranger("Healer", "./StrangerCards/Healer.png", "yep"),
    Classes.Stranger("Hermit", "./StrangerCards/Hermit.png", "yep"),
    Classes.Stranger("Instructor", "./StrangerCards/Instructor.png", "yep"),
    Classes.Stranger("Mage", "./StrangerCards/Mage.png", "yep"),
    Classes.Stranger("Phantom", "./StrangerCards/Phantom.png", "yep"),
    Classes.Stranger("Sorcerer", "./StrangerCards/Sorcerer.png", "yep"),
    Classes.Stranger("Witch", "./StrangerCards/Witch.png", "yep")
]

# List of Place cards representing various locations in the game that players can visit.
placecards = [
    Classes.Place("Cave", "./Place/Cave.png", "Yep"),
    Classes.Place("FountainOfW", "./Place/FountainOfW.png", "Yep"),
    Classes.Place("MagicPortal", "./Place/MagicPortal.png", "Yep"),
    Classes.Place("MagicStream", "./Place/MagicStream.png", "Yep"),
    Classes.Place("Market", "./Place/Market.png", "Yep"),
    Classes.Place("Marsh", "./Place/Marsh.png", "Yep"),
    Classes.Place("Maze", "./Place/Maze.png", "Yep"),
    Classes.Place("PoolOfLife", "./Place/PoolOfLife.png", "Yep"),
    Classes.Place("Shrine", "./Place/Shrine.png", "Yep"),
]
"""
Place cards represent locations with specific interactions:
- name (str): The name of the place.
- image (str): Path to the place's image file.
- effect (str): Description of what happens when a character visits this place.
"""

# Initializing a list of Spell cards, which are magical effects that players can cast.
spellcards = [
    Classes.Spell("Acqusition", "./Spell/Acqusition.png", "yep"),
    Classes.Spell("Alchemy", "./Spell/Alchemy.png", "yep"),
    Classes.Spell("CounterSpell", "./Spell/CounterSpell.png", "yep"),
    Classes.Spell("DestroyMagic", "./Spell/DestroyMagic.png", "yep"),
    Classes.Spell("Destruction", "./Spell/Destruction.png", "yep"),
    Classes.Spell("Divination", "./Spell/Divination.png", "yep"),
    Classes.Spell("Healing", "./Spell/Healing.png", "yep"),
    Classes.Spell("Hex", "./Spell/Hex.png", "yep"),
    Classes.Spell("Immobility", "./Spell/Immobility.png", "yep"),
    Classes.Spell("Invisibility", "./Spell/Invisibility.png", "yep"),
    Classes.Spell("Mesmerism", "./Spell/Mesmerism.png", "yep"),
    Classes.Spell("Nullify", "./Spell/Nullify.png", "yep"),
    Classes.Spell("Preservation", "./Spell/Preservation.png", "yep"),
    Classes.Spell("PsionicBlast", "./Spell/PsionicBlast.png", "yep"),
    Classes.Spell("Random", "./Spell/Random.png", "yep"),
    Classes.Spell("Teleport", "./Spell/Teleport.png", "yep"),
    Classes.Spell("TemporalWarp", "./Spell/TemporalWarp.png", "yep")
]
"""
Spell cards allow characters to perform magical actions:
- name (str): The name of the spell.
- image (str): Path to the spell's image file.
- effect (str): The magical effect of the spell, impacting the game or other players.
"""
