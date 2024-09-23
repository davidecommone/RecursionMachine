# Python 3.11.6   https://www.python.org/downloads/release/python-3116/


import recursion_machine

# I. "Cricket Backroom"

header_riro_graph = r""" #(set-global-staff-size 14)
\header {
composer = \markup {Davide Commone}
title = \markup {OUTPUT RIRO MACHINE}
subtitle = \markup {I.}
}
"""
header_riro_comb_score = r""" #(set-global-staff-size 14)
\header {
composer = \markup {Davide Commone}
title = \markup {OUTPUT COMBINAORE, ciclo RIRO}
subtitle = \markup {I.}
}
"""
header_riro_graduation_score = r""" #(set-global-staff-size 14)
\header {
composer = \markup {Davide Commone}
title = \markup {OUTPUT GRIO MACHINE, ciclo RIRO}
subtitle = \markup {I.}
}
"""


header_irio_graph = r""" #(set-global-staff-size 14)
\header {
composer = \markup {Davide Commone}
title = \markup {OUTPUT IRIO MACHINE}
subtitle = \markup {I.}
}
"""
header_irio_comb_score = r""" #(set-global-staff-size 14)
\header {
composer = \markup {Davide Commone}
title = \markup {OUTPUT COMBINATORE, ciclo IRIO}
subtitle = \markup {I.}
}
"""
header_irio_graduation_score = r""" #(set-global-staff-size 14)
\header {
composer = \markup {Davide Commone}
title = \markup {OUTPUT GRIO MACHINE, ciclo IRIO}
subtitle = \markup {I.}
}
"""


# Ciclo RIRO
buffer_riro_mov1 = recursion_machine.riro("c f bf ef' af'",50,False) 
recursion_machine.makegraph_recursion(buffer_riro_mov1,header_riro_graph)
combinazione_riro = recursion_machine.combinatore(buffer_riro_mov1,"notte","onsetfeat", 29,header_riro_comb_score)
grad_list_riro = recursion_machine.grio(combinazione_riro,"notte","noveltyfeat",541,1,3,header_riro_graduation_score)
recursion_machine.grito(9,3,grad_list_riro,"notte","deltatime",439,5)

# Ciclo IRIO
buffer_irio_mov1 = recursion_machine.irio("c f bf ef' af'",50,False) 
recursion_machine.makegraph_recursion(buffer_irio_mov1,header_irio_graph)
combinazione_irio = recursion_machine.combinatore(buffer_irio_mov1,"notte","onsetfeat", 67,header_irio_comb_score)
grad_list_irio = recursion_machine.grio(combinazione_irio,"notte","noveltyfeat",1873,1,3,header_irio_graduation_score)
recursion_machine.grito(9,3,grad_list_irio,"notte","deltatime",643,5)