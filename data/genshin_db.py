# Aptitudes
lundi = ["Amber", "Barbara", "Klee", "Sucrose", "Childe", "Diona", "Aloy", "Keqing", "Ningguang", "Qiqi", "Xiao", "Shenhe", "Yoimiya", "Kokomi", "Thomas",  "Yelan", "Cyno", "Heizou", "Tighnari", "Candace"]
mardi = ["Bennett", "Diluc", "Jean", "Mona", "Noelle", "Razor", "Eula", "Chongyun", "Xiangling", "Ganyu", "Hu Tao", "Kazuha", "Yun Jin", "Ayaka", "Sara", "Itto", "Ayato", "Layla", "Nahida", "Shinobu", "Dori"]
mercredi = ["Fischl", "Kaeya", "Lisa", "Venti", "Albedo", "Rosalia", "Beidou", "Xingqiu", "Zhongli", "Xinyan", "Yanfei", "Sayu", "Raiden", "Gorou", "Yae", "Nilou", "Collei"]

twins = ["Aether", "Lumine"]

aptitudes_time = {
    0: lundi + twins,
    1: mardi + twins,
    2: mercredi + twins,
    3: lundi + twins,
    4: mardi + twins,
    5: mercredi + twins,
    6: lundi + mardi + mercredi + twins
}

# Armes
lundi_w = ["dull blade", "silver sword", "cool steel", "favonius sword", "royal longsword", "the alley flash", "cinnabar spindle", "aquila favonia", "ferrous shadow", "the bell", "snow-tombed starsilver", "song of broken pines", "raven bow", "stringless", "mitternachts waltz", "apprentice notes", "pocket grimoire", "magic guide", "favonius codex", "royal grimoire", "dark iron sword", "blackliff longsword", "lion roar", "summit shaper", "quartz", "lithic blade", "whiteblind", "white tassel", "crescent pike", "primordial jade winged-spear", "slingshot", "blackliff warbow", "rust", "emerald orb", "blackliff agate", "solar pearl", "amenoma kageuchi", "mistsplitter reforged", "akuoumaru", "hakushin ring", "oathsworn eye", "everlasting moonglow", "Aqua Simulacra", "Sapwood Blade", "Xiphos Moonlight", "Key of Khaj Nisut", "Forest Regalia"]
mardi_w = ["harbinger of dawn", "the black sword", "the flute", "sword of descension", "skyward blade", "waster greatsword", "old mercs pal", "bloodtainted greatsword", "sacrificial greatsword", "skyward pride", "deathmatch", "dragonspine spear", "hunters bow", "seasoned hunters bow", "sharpshooters oath", "sacrificial bow", "skyward harp", "elegy for the end", "thrilling tales of dragon slayers", "the widsith", "wine and song", "dodoco tales", "skyward atlas", "Fillet Blade", "Prototype Rancour", "Primordial Jade Cutter", "Debate Club", "Blackcliff Slasher", "Rainslasher", "The Unforged", "Halberd", "Blackcliff Pole", "Dragons Bane", "Royal Spear", "Calamity Queller", "Messenger", "Prototype Crescent", "Twin Nephrite", "Prototype Amber", "Eye of Perception", "Haran Geppaku Futsu", "Katsuragikiri Nagamasa", "Redhorn Stonethresher", "Hamayumi", "Predator", "Mouuns Moon", "Thundering Pulse", "Moonpiercer", "Staff of the Scarlet Sands", "Wandering Evenstar", "Fruit of Fulfillment", "A Thousand Floating Dreams"]
mercredi_w = ["Travelers Handy Sword", "Sacrificial Sword", "Festering Desire", "Freedom Sworn", "White Iron Greatsword", "Favonius Greatsword", "Royal Greatsword", "Wolfs Gravestone", "Beginners Protector", "Iron Point", "Favonius Lance", "Skyward Spine", "Recurve Bow", "Alley Hunter", "Favonius Warbow", "Royal Bow", "Windblume Ode", "Amos Bow", "Otherworldly Story", "Sacrificial Fragments", "Frostbearer", "Lost Prayer to the Sacred Winds", "Skyrider Sword", "Iron Sting", "Skyrider Greatsword", "Prototype Archaic", "Serpent Spine", "Luxurious Sea Lord", "Black Tassel", "Lithic Spear", "Prototype Starglitter", "Vortex Vanquisher", "Staff of Homa", "Compound Bow", "Fading Twilight", "Mappa Mare", "Memory of Dust", "Kitain Cross Spear", "The Catch", "Wavebreakers Fin", "Engulfing Lightning", "Polar Star", "Kaguras Verity", "Makhaira Aquamarine", "Kings Squire", "End of the Line", "Hunters Path"]

weapons_time = {
    0: lundi_w,
    1: mardi_w,
    2: mercredi_w,
    3: lundi_w,
    4: mardi_w,
    5: mercredi_w,
    6: lundi_w + mardi_w + mercredi_w
}
