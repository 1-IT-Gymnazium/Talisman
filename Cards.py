import Classes

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

enemycards = [
    Classes.Enemy("Ape", "./EnemyCards/Ape.png", "yep", "0", "3"),
    Classes.Enemy("Bandit", "./EnemyCards/Bandit.png", "yep", "0", "4"),
    Classes.Enemy("Bear", "./EnemyCards/Bear.png", "yep", "0", "3"),
    Classes.Enemy("Demon", "./EnemyCards/Demon.png", "yep", "10", "0"),
    Classes.Enemy("Dopplergang", "./EnemyCards/Dopplergang.png", "yep", "0", "7"),
    Classes.Enemy("Dragon", "./EnemyCards/Dragon.png", "yep", "0", "7"),
    Classes.Enemy("Ghost", "./EnemyCards/Ghost.png", "yep", "4", "0"),
    Classes.Enemy("Giant", "./EnemyCards/Giant.png", "yep", "0", "6"),
    Classes.Enemy("Goblin", "./EnemyCards/Goblin.png", "yep", "0", "2"),
    Classes.Enemy("Hobgoblin", "./EnemyCards/Hobgoblin.png", "yep", "0", "3"),
    Classes.Enemy("Lemure", "./EnemyCards/Lemure.png", "yep", "1", "0"),
    Classes.Enemy("Lion", "./EnemyCards/Lion.png", "yep", "0", "3"),
    Classes.Enemy("Orge", "./EnemyCards/Orge.png", "yep", "0", "5"),
    Classes.Enemy("Serpent", "./EnemyCards/Serpent.png", "yep", "0", "4"),
    Classes.Enemy("Shadow", "./EnemyCards/Shadow.png", "yep", "2", "0"),
    Classes.Enemy("Spectre", "./EnemyCards/Spectre.png", "yep", "3", "0"),
    Classes.Enemy("WildBoar", "./EnemyCards/WildBoar.png", "yep", "0", "1"),
    Classes.Enemy("Wolf", "./EnemyCards/Wolf.png", "yep", "0", "2"),
    Classes.Enemy("Wraith", "./EnemyCards/Wraith.png", "yep", "5", "0"),
    Classes.Enemy("Farmer", "./EnemyCards/Farmer.png", "yep", "0", "3"),
]

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
