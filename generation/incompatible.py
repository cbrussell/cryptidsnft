incompatible_list = [ 

    # avoid black wings with dark background
    # black2, superdark, purp2, forest, varsity, skyish, sky, egg, black444

    {"4_back": "back_featherwings_black","background": "black2"},
    {"4_back": "back_dragonwings_black", "background": "black2"},
    {"4_back": "back_spike_black",       "background": "black2"},

    {"4_back": "back_featherwings_black","background": "black444"},
    {"4_back": "back_dragonwings_black", "background": "black444"},
    {"4_back": "back_spike_black",       "background": "black444"},

    {"4_back": "back_featherwings_black","background": "superdark"},
    {"4_back": "back_dragonwings_black", "background": "superdark"},
    {"4_back": "back_spike_black",       "background": "superdark"},

    {"4_back": "back_featherwings_black","background": "purp2"},
    {"4_back": "back_dragonwings_black", "background": "purp2"},
    {"4_back": "back_spike_black",       "background": "purp2"},

    {"4_back": "back_featherwings_black","background": "forest"},
    {"4_back": "back_dragonwings_black", "background": "forest"},
    {"4_back": "back_spike_black",       "background": "forest"},

    {"4_back": "back_featherwings_black","background": "varsity"},
    {"4_back": "back_dragonwings_black", "background": "varsity"},
    {"4_back": "back_spike_black",       "background": "varsity"},

    {"4_back": "back_featherwings_black","background": "skyish"},
    {"4_back": "back_dragonwings_black", "background": "skyish"},
    {"4_back": "back_spike_black",       "background": "skyish"},

    {"4_back": "back_featherwings_black","background": "sky"},
    {"4_back": "back_dragonwings_black", "background": "sky"},
    {"4_back": "back_spike_black",       "background": "sky"},

    # purple spike clashes with purple bacjground
    { "4_back": "back_spike_purple", "background": "purp2" },          

    # white wing clashes with egg/tan background
    { "4_back": "back_spike_white", "background": "tan_egg_light" },           
    { "4_back": "back_dragonwings_white", "background": "tan_egg_light" },
    { "4_back": "back_featherwings_white", "background": "tan_egg_light" },
    { "4_back": "back_spike_white", "background": "tan_egg_light" },

    { "4_back": "back_spike_white", "background": "tan_egg_dark" },           
    { "4_back": "back_dragonwings_white", "background": "tan_egg_dark" },
    { "4_back": "back_featherwings_white", "background": "tan_egg_dark" },
    { "4_back": "back_spike_white", "background": "tan_egg_dark" },                  
    
    # orange featherwing clashes
    { "4_back": "back_featherwings_orange", "background": "sand2"},
    { "4_back": "back_featherwings_yellow","background": "tan_egg_light"},
    { "4_back": "back_featherwings_yellow","background": "tan_egg_dark"},

    # yellow dragonwing clashes
    { "4_back": "back_dragonwings_yellow","background": "tan_egg_light"},
    { "4_back": "back_dragonwings_yellow","background": "tan_egg_dark"},
                     
    # orange featherwing clashes
    { "4_back": "back_featherwings_orange", "background": "tan_egg_light"},
    { "4_back": "back_featherwings_orange", "background": "tan_egg_dark"},

    # blue wing clashes
    { "4_back": "back_dragonwings_blue", "background": "skyish"},
    { "4_back": "back_featherwings_blue", "background": "skyish"},

    # purple spike clash with varsity
    { "4_back": "back_spike_purple",   "background": "varsity"},

    # avoid red background clashes
    { "base_color": "red", "background": "apricot"},
    { "base_color": "red", "background": "varsity"},
    { "base_color": "red", "background": "superdark"},
    { "base_color": "red", "background": "purp2"},

    # tail and background clashes with black tips (scorpion, kitsune, lion)
    { "1_tail": "tail_kitsune_orange","background": "superdark"},
    { "1_tail": "tail_lion_red", "background": "superdark"},
    { "1_tail": "tail_kitsune_red","background": "superdark"},
    { "1_tail": "tail_lion_orange", "background": "superdark"},
    { "1_tail": "tail_scorpion_orange", "background":    "superdark"},
    { "1_tail": "tail_scorpion_red", "background":       "superdark"},

    { "1_tail": "tail_kitsune_orange","background":     "black444"},
    { "1_tail": "tail_lion_red", "background":          "black444"},
    { "1_tail": "tail_kitsune_red","background":        "black444"},
    { "1_tail": "tail_lion_orange", "background":       "black444"},
    { "1_tail": "tail_scorpion_orange", "background":    "black444"},
    { "1_tail": "tail_scorpion_red", "background":       "black444"},

    { "1_tail": "tail_kitsune_orange","background":     "black2"},
    { "1_tail": "tail_lion_red", "background":          "black2"},
    { "1_tail": "tail_kitsune_red","background":        "black2"},
    { "1_tail": "tail_lion_orange", "background":       "black2"},
    { "1_tail": "tail_scorpion_orange", "background":   "black2"},
    { "1_tail": "tail_scorpion_red", "background":      "black2"},

    # avoid orange base and apricot background
    { "base_color": "orange", "background": "apricot"},

    # avoid dark backround and medium/dark horns 
    { "background": "black2", "13_horns": "horns_ram_medium"},
    { "background": "black2", "13_horns": "horns_ram_dark"},
    { "background": "black2", "13_horns": "horns_unicorn_medium"},
    { "background": "black2", "13_horns": "horns_unicorn_dark"},
    { "background": "black2", "13_horns": "horns_goat_medium"},
    { "background": "black2", "13_horns": "horns_goat_dark"},
    { "background": "black2", "13_horns": "horns_bull_medium"},
    { "background": "black2", "13_horns": "horns_bull_dark"},
    { "background": "black2", "13_horns": "horns_antlers_medium"},
    { "background": "black2", "13_horns": "horns_antlers_dark"},

    { "background": "black444", "13_horns": "horns_ram_medium"},
    { "background": "black444", "13_horns": "horns_ram_dark"},
    { "background": "black444", "13_horns": "horns_unicorn_medium"},
    { "background": "black444", "13_horns": "horns_unicorn_dark"},
    { "background": "black444", "13_horns": "horns_goat_medium"},
    { "background": "black444", "13_horns": "horns_goat_dark"},
    { "background": "black444", "13_horns": "horns_bull_medium"},
    { "background": "black444", "13_horns": "horns_bull_dark"},
    { "background": "black444", "13_horns": "horns_antlers_medium"},
    { "background": "black444", "13_horns": "horns_antlers_dark"},

    { "background": "superdark", "13_horns": "horns_ram_medium"},
    { "background": "superdark", "13_horns": "horns_ram_dark"},
    { "background": "superdark", "13_horns": "horns_unicorn_medium"},
    { "background": "superdark", "13_horns": "horns_unicorn_dark"},
    { "background": "superdark", "13_horns": "horns_goat_medium"},
    { "background": "superdark", "13_horns": "horns_goat_dark"},
    { "background": "superdark", "13_horns": "horns_bull_medium"},
    { "background": "superdark", "13_horns": "horns_bull_dark"},
    { "background": "superdark", "13_horns": "horns_antlers_medium"},
    { "background": "superdark", "13_horns": "horns_antlers_dark"},

    { "background": "purp2", "13_horns": "horns_ram_medium"},
    { "background": "purp2", "13_horns": "horns_ram_dark"},
    { "background": "purp2", "13_horns": "horns_unicorn_medium"},
    { "background": "purp2", "13_horns": "horns_unicorn_dark"},
    { "background": "purp2", "13_horns": "horns_goat_medium"},
    { "background": "purp2", "13_horns": "horns_goat_dark"},
    { "background": "purp2", "13_horns": "horns_bull_medium"},
    { "background": "purp2", "13_horns": "horns_bull_dark"},
    { "background": "purp2", "13_horns": "horns_antlers_medium"},
    { "background": "purp2", "13_horns": "horns_antlers_dark"},

 
    { "background": "varsity", "13_horns": "horns_ram_medium"},
    { "background": "varsity", "13_horns": "horns_ram_dark"},
    { "background": "varsity", "13_horns": "horns_unicorn_medium"},
    { "background": "varsity", "13_horns": "horns_unicorn_dark"},
    { "background": "varsity", "13_horns": "horns_goat_medium"},
    { "background": "varsity", "13_horns": "horns_goat_dark"},
    { "background": "varsity", "13_horns": "horns_bull_medium"},
    { "background": "varsity", "13_horns": "horns_bull_dark"},
    { "background": "varsity", "13_horns": "horns_antlers_medium"},
    { "background": "varsity", "13_horns": "horns_antlers_dark"},
 
    { "background": "skyish", "13_horns": "horns_ram_medium"},
    { "background": "skyish", "13_horns": "horns_ram_dark"},
    { "background": "skyish", "13_horns": "horns_unicorn_medium"},
    { "background": "skyish", "13_horns": "horns_unicorn_dark"},
    { "background": "skyish", "13_horns": "horns_goat_medium"},
    { "background": "skyish", "13_horns": "horns_goat_dark"},
    { "background": "skyish", "13_horns": "horns_bull_medium"},
    { "background": "skyish", "13_horns": "horns_bull_dark"},
    { "background": "skyish", "13_horns": "horns_antlers_medium"},
    { "background": "skyish", "13_horns": "horns_antlers_dark"},
 
    { "background": "sky", "13_horns": "horns_ram_medium"},
    { "background": "sky", "13_horns": "horns_ram_dark"},
    { "background": "sky", "13_horns": "horns_unicorn_medium"},
    { "background": "sky", "13_horns": "horns_unicorn_dark"},
    { "background": "sky", "13_horns": "horns_goat_medium"},
    { "background": "sky", "13_horns": "horns_goat_dark"},
    { "background": "sky", "13_horns": "horns_bull_medium"},
    { "background": "sky", "13_horns": "horns_bull_dark"},
    { "background": "sky", "13_horns": "horns_antlers_medium"},
    { "background": "sky", "13_horns": "horns_antlers_dark"},

    { "11b_headaccent": "headaccent_bear_points_white", "background": "sand2" },


    { "background": "forest", "base_color": "red" },
    {  "background": "sky", "4_back": "back_featherwings_purple" }
     
]  