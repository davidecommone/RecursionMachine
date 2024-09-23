# Python 3.11.6   https://www.python.org/downloads/release/python-3116/


import recursion_machine

# II. "Seagulls Backroom" 

header_riro_graph = r""" #(set-global-staff-size 14)
\header {
composer = \markup {Davide Commone}
title = \markup {OUTPUT RIRO MACHINE}
subtitle = \markup {II.}
}
"""
header_riro_comb_score = r""" #(set-global-staff-size 14)
\header {
composer = \markup {Davide Commone}
title = \markup {OUTPUT COMBINAORE, ciclo RIRO}
subtitle = \markup {II.}
}
"""
header_riro_graduation_score = r""" #(set-global-staff-size 14)
\header {
composer = \markup {Davide Commone}
title = \markup {OUTPUT GRIO MACHINE, ciclo RIRO}
subtitle = \markup {II.}
}
"""


header_irio_graph = r""" #(set-global-staff-size 14)
\header {
composer = \markup {Davide Commone}
title = \markup {OUTPUT IRIO MACHINE}
subtitle = \markup {II.}
}
"""
header_irio_comb_score = r""" #(set-global-staff-size 14)
\header {
composer = \markup {Davide Commone}
title = \markup {OUTPUT COMBINATORE, ciclo IRIO}
subtitle = \markup {II.}
}
"""
header_irio_graduation_score = r""" #(set-global-staff-size 14)
\header {
composer = \markup {Davide Commone}
title = \markup {OUTPUT GRIO MACHINE, ciclo IRIO}
subtitle = \markup {II.}
}
"""


# Ciclo RIRO
buffer_riro_elem3 = recursion_machine.riro("e' d' bf a f d g,",50) 
recursion_machine.makegraph_recursion(buffer_riro_elem3,header_riro_graph)
combinazione_riro = recursion_machine.combinatore(buffer_riro_elem3,"gabbiani","onsetfeat", 40,header_riro_comb_score)
grad_list_riro = recursion_machine.grio(combinazione_riro,"gabbiani","noveltyfeat",1009,1,3,header_riro_graduation_score)
recursion_machine.grito(12,3,grad_list_riro,"gabbiani","deltatime",500,7)


# Ciclo IRIO
buffer_irio_elem3 = recursion_machine.irio("e' d' bf a f d g,",50) 
recursion_machine.makegraph_recursion(buffer_irio_elem3,header_irio_graph)
combinazione_irio = recursion_machine.combinatore(buffer_irio_elem3,"gabbiani","onsetfeat", 73,header_irio_comb_score)
grad_list_irio = recursion_machine.grio(combinazione_irio,"gabbiani","noveltyfeat",1117,1,3,header_irio_graduation_score)
recursion_machine.grito(12,3,grad_list_irio,"gabbiani","deltatime",521,7)