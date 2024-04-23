# Python 3.11.6   https://www.python.org/downloads/release/python-3116/
# Abjad 3.19      https://abjad.github.io/index.html# 
# Lilypond 2.24.3 (in esecuzione Guile 3.0)  https://lilypond.org/doc/v2.24/Documentation/web/download
#
# Davide Commone 2024


import abjad
import re
import field_dataset
from collections import deque


def octave_normalizer_UP(to_normalize, reference_th):
    if any(p > reference_th for p in to_normalize):
        threshold_offset = max(p for p in to_normalize if p > reference_th) - reference_th                                 
        class_to_string_conv = re.findall(r'-?\d+', str(threshold_offset))               
        octave_transpose = (int(class_to_string_conv[0]) // 12)                                                                                                            
        transpose_n = -(octave_transpose + 1) * 12                                                             
        to_normalize = to_normalize.transpose(transpose_n)  
    else:
        pass
    return to_normalize


def octave_normalizer_DOWN(to_normalize, reference_th):
    if any(p < reference_th for p in to_normalize):
        threshold_offset = min(p for p in to_normalize if p < reference_th) - reference_th                              
        class_to_string_conv = re.findall(r'-?\d+', str(threshold_offset))                 
        octave_transpose = -(-int(class_to_string_conv[0]) // 12)                                                              
        transpose_n = abs(octave_transpose - 1) * 12
        to_normalize = to_normalize.transpose(transpose_n)  
    else:
        pass
    return to_normalize


def makegraph_recursion(buffer, header):
    container = abjad.Container()
    score = abjad.Score()
    preamble = r"""
    
    \layout {
        \context {
            \Staff
            \override VerticalAxisGroup.staff-staff-spacing.minimum-distance = 11
        }       
        \context {
            \Score
            \override SpacingSpanner.strict-spacing = ##t
            \override SystemStartBar.stencil = ##f
            \override Stem.stencil = ##f
            \override TextScript.staff-padding = 5
            \override TimeSignature.transparent = ##t
            proportionalNotationDuration = #(ly:make-moment 1 16)
        }
    }
"""

    for pitch_segment in buffer:
        notes = abjad.makers.make_notes(pitch_segment, durations=(1,4))
        container.extend(notes)
       
        abjad.attach(abjad.BarLine("||"), container[-1])
        score.append(container)
    
    item_in_element = len(buffer[0])
    abjad.attach(abjad.Clef("bass"), container[0])
    abjad.attach(abjad.TimeSignature((item_in_element, 4)), container[0]) 

    lilypond_file = abjad.LilyPondFile([header,preamble,score])
    abjad.show(lilypond_file)



def riro(original="", max_items=5,normalize_mode = True): 
    buffer = []
    buffer_check = []
    limiter_index = 1
    if normalize_mode is True:
        threshold = -29  # Sol 0
    else:
        threshold = 10 # Sib 3
    
    # Elemento originale (o): 
    conversione_pitch = [abjad.NamedPitch(_) for _ in original.split()]
    pitch_original = abjad.PitchSegment(conversione_pitch)
    buffer.append(pitch_original)  
    
    original_for_check = pitch_original.__str__()
    original_for_check = re.findall(r'-?\d+', original_for_check)
    original_for_check = [int(item) for item in original_for_check]  
    buffer_check.append(original_for_check)
    
    # Retrogrado dell'originale R(0):
    pushing = pitch_original.retrograde()
    if normalize_mode is True:
        pushing = octave_normalizer_DOWN(pushing, threshold)
    else:
        pushing = octave_normalizer_UP(pushing, threshold)
    buffer.append(pushing)  

    pushing_check = pushing.__str__()
    pushing_check = re.findall(r'-?\d+', pushing_check)
    pushing_check = [int(item) for item in pushing_check]
    buffer_check.append(pushing_check)
    
    
    while True:
        axis = pushing[0]                                                                              

        #Inverso ricorsivo I...(R(0)) :                                                                  
        pushing = pushing.invert(axis)                                             
        if normalize_mode is True:
            pushing = octave_normalizer_DOWN(pushing, threshold)
        else:
            pushing = octave_normalizer_UP(pushing, threshold)                                         
        buffer.append(pushing)

        pushing_check = pushing.__str__()
        pushing_check = re.findall(r'-?\d+', pushing_check)
        pushing_check = [int(item) for item in pushing_check]
        buffer_check.append(pushing_check)
                                                                                
        #Retrogrado ricorsivo R...(I(R(o))):
        pushing = pushing.retrograde()                                           
        if normalize_mode is True:
            pushing = octave_normalizer_DOWN(pushing, threshold)
        else:
            pushing = octave_normalizer_UP(pushing, threshold)                             
        buffer.append(pushing)

        pushing_check = pushing.__str__()
        pushing_check = re.findall(r'-?\d+', pushing_check)
        pushing_check = [int(item) for item in pushing_check]
        buffer_check.append(pushing_check)
                                                                               
            
        limiter_index += 1
        
        # Controllo della ridondanza:
        if any(pushing_check == item for item in buffer_check[:-2]) or limiter_index > max_items: 
            print("triggered_codition_1")          
            break
        elif any(pushing_check == [item + 12 for item in items] for items in buffer_check) or any(pushing_check == [item + 24 for item in items] for items in buffer_check) or any(pushing_check == [item + 36 for item in items] for items in buffer_check):
            print("triggered_codition_2")
            break
        elif any(pushing_check == [item - 12 for item in items] for items in buffer_check) or any(pushing_check == [item - 24 for item in items] for items in buffer_check) or any(pushing_check == [item - 36 for item in items] for items in buffer_check):
            print("triggered_codition_3")
            break
        else:
            pass

    return buffer



def irio(original="", max_items= int(),normalize_mode = True):
    buffer = []
    buffer_check = []
    limiter_index = 1
    if normalize_mode is True:
        threshold = 10 #  Sib 3
    else:
        threshold = -29  # Sol 0

    
    conversione_pitch = [abjad.NamedPitch(_) for _ in original.split()]
    pitch_original = abjad.PitchSegment(conversione_pitch)
    buffer.append(pitch_original)

    #Elemento originale (o):
    original_for_check = pitch_original.__str__()
    original_for_check = re.findall(r'-?\d+', original_for_check)
    original_for_check = [int(item) for item in original_for_check]  
    buffer_check.append(original_for_check)
    
    # Inversione dell'originale I(o):
    pushing = pitch_original.invert(pitch_original[0])
    if normalize_mode is True:
        pushing = octave_normalizer_UP(pushing, threshold)
    else:
        pushing = octave_normalizer_DOWN(pushing, threshold)
    buffer.append(pushing)
    
    pushing_check = pushing.__str__()
    pushing_check = re.findall(r'-?\d+', pushing_check)
    pushing_check = [int(item) for item in pushing_check]
    buffer_check.append(pushing_check)
   
    while True:  

        #Retrogrado ricorsivo R...(I(o)):                                                                          
        pushing = pushing.retrograde()                               
        if normalize_mode is True:
            pushing = octave_normalizer_UP(pushing, threshold)
        else:
            pushing = octave_normalizer_DOWN(pushing, threshold)                            
        buffer.append(pushing)

        pushing_check = pushing.__str__()
        pushing_check = re.findall(r'-?\d+', pushing_check)
        pushing_check = [int(item) for item in pushing_check]
        buffer_check.append(pushing_check)
        
        axis = pushing[0]

        #Inverso ricorsivo I...(R(I(o))):                                                              
        pushing = pushing.invert(axis)                                      
        if normalize_mode is True:
            pushing = octave_normalizer_UP(pushing, threshold)
        else:
            pushing = octave_normalizer_DOWN(pushing, threshold)                                          
        buffer.append(pushing)

        pushing_check = pushing.__str__()
        pushing_check = re.findall(r'-?\d+', pushing_check)
        pushing_check = [int(item) for item in pushing_check]
        buffer_check.append(pushing_check)
                                                                             
        limiter_index += 1

        #Controllo della ridondanza:
        if any(pushing_check == item for item in buffer_check[:-2]) or limiter_index > max_items: 
            print("triggered_codition_1")          
            break
        elif any(pushing_check == [item + 12 for item in items] for items in buffer_check) or any(pushing_check == [item + 24 for item in items] for items in buffer_check) or any(pushing_check == [item + 36 for item in items] for items in buffer_check):
            print("triggered_codition_2")
            break
        elif any(pushing_check == [item - 12 for item in items] for items in buffer_check) or any(pushing_check == [item - 24 for item in items] for items in buffer_check) or any(pushing_check == [item - 36 for item in items] for items in buffer_check):
            print("triggered_codition_3")
            break
        else:
            pass
    
    return buffer



def combinatore(elements_buffer, field_main_key, field_secondary_key,renorm_max,header_literal): 
    combinazione = []
    elements_buffer_converted = []
    filtered_combinazione = []

    elements_buffer.pop(0)
    removing_index = len(elements_buffer)
    elements_buffer.pop(removing_index -1)
    elements_buffer.pop(removing_index -2)
    
    if field_secondary_key == "noveltyfeat":
        data = field_dataset.dataset[field_main_key][field_secondary_key]
    elif field_secondary_key == "deltatime" or "onsetfeat":
        data = field_dataset.normdata[field_main_key][field_secondary_key]
    else:
        print("Error, key" + field_secondary_key + " not found")
    
    data = [int(item * renorm_max) for item in data]
    
    # Conversione da PitchSegment(list) a list
    for pitch_segment in elements_buffer:  
        pitch_segment = pitch_segment.__str__()
        pitch_segment = re.findall(r'-?\d+', pitch_segment)
        pitch_segment = [int(item) for item in pitch_segment]
        elements_buffer_converted.append(pitch_segment)

    # Costruisce le combinazioni cambiando l'ordine degli item di elements_buffer
    for item in data:  
        index = int(item) % len(elements_buffer_converted)
        to_combinazione = elements_buffer_converted[index]
        combinazione.append(to_combinazione)

    # Filtra la combinazione eliminando gli elementi ripetuti
    for item in combinazione:  
        if item not in filtered_combinazione:
            filtered_combinazione.append(item)
        

    # Genera il file .pdf
    container = abjad.Container()
    score = abjad.Score()
    preamble = r"""
    \layout {
        \context {
            \Staff
            \override VerticalAxisGroup.staff-staff-spacing.minimum-distance = 11
        }
        \context {
            \Score
            \override SpacingSpanner.strict-spacing = ##t
            \override SystemStartBar.stencil = ##f
            \override Stem.stencil = ##f
            \override TextScript.staff-padding = 5
            \override TimeSignature.transparent = ##t
            proportionalNotationDuration = #(ly:make-moment 1 16)
        }
    }
    """

    for pitch_segment in filtered_combinazione:
        notes = abjad.makers.make_notes(pitch_segment, durations=(1,4))
        container.extend(notes)
       
        abjad.attach(abjad.BarLine("||"), container[-1])
        score.append(container)
    
    item_in_element = len(filtered_combinazione[0])
    abjad.attach(abjad.Clef("bass"), container[0])
    abjad.attach(abjad.TimeSignature((item_in_element, 4)), container[0]) 

    lilypond_file = abjad.LilyPondFile([header_literal,preamble,score])
    abjad.show(lilypond_file)  

    return filtered_combinazione    #collezione di liste



def grio(combination_list, field_main_key, field_secondary_key, renorm_max, step_min, step_max, header_literal): 
    
    if field_secondary_key == "noveltyfeat":
        data = field_dataset.dataset[field_main_key][field_secondary_key]
    elif field_secondary_key == "deltatime" or "onsetfeat":
        data = field_dataset.normdata[field_main_key][field_secondary_key]
    else:
        print("Error, key " + field_secondary_key + " not found!")

    data = [int(item * renorm_max) for item in data]
    grad_notes_list = []
    grad_step_list = []

    i = 0
    j = 0

    for items in combination_list:

        for item in items:

            data_index = j % len(data)
            to_graduate = int(data[int(data_index)]) % 2      
            grad_notes_list.append(to_graduate)

            if to_graduate == 1:

                note_number = (j % len(items)) + 1

                step_leng_list = list(range(step_min,(step_max+1)))
                step_leng_index = int(data[int(data_index)]) % len(step_leng_list)      
                step_leng = step_leng_list[step_leng_index]
                grad_step_list.append(step_leng)       
                #print("la nota" + str(note_number) + " dell' elemento" + str(i+1) + " : to graduate")
                #print("ripetere l'elemento " + str(step_leng) + " volte")

            elif to_graduate == 0:
                note_number = (j % len(items)) + 1
                #print("la nota" + str(note_number) + " dell' elemento" + str(i+1) + " : to NOT graduate")

            else:
                pass

            j += 1

        i += 1

    
    # Genera il file .pdf
    container = abjad.Container()
    score = abjad.Score()
    preamble = r"""
    \layout {
        \context {
            \Staff
            \override VerticalAxisGroup.staff-staff-spacing.minimum-distance = 20
        }
        \context {
            \Score
            \override SpacingSpanner.strict-spacing = ##t
            \override SystemStartBar.stencil = ##f
            \override Stem.stencil = ##f
            \override TextScript.staff-padding = 1
            \override TimeSignature.transparent = ##t
            proportionalNotationDuration = #(ly:make-moment 1 16)
        }
    }
    """
    j = 0
    index_gsl = 0

    for pitch_segment in combination_list:
        notes = abjad.makers.make_notes(pitch_segment, durations=(1,4))

        for item in notes:
            notes_index = j % len(notes)

            if grad_notes_list[j] == 1:
                item = item.note_head
                abjad.tweak(item, r"\tweak color #red")
                item.tweaks
                grad_value = grad_step_list[index_gsl]
                mark = r"\markup \with-color #red"
                mark = mark + r" { i \sub" + str(grad_value) + "}" #\hspace #-0.75
                iteration_mark = abjad.Markup(mark)
                abjad.attach(iteration_mark, notes[notes_index] , direction=abjad.UP)
                index_gsl += 1
            else:
                pass
        
            j += 1
            
        container.extend(notes)
        abjad.attach(abjad.BarLine("||"), container[-1])
        score.append(container)
               
    item_in_element = len(combination_list[0])
    abjad.attach(abjad.Clef("bass"), container[0])
    abjad.attach(abjad.TimeSignature((item_in_element, 4)), container[0]) 

    lilypond_file = abjad.LilyPondFile([header_literal,preamble,score])
    abjad.show(lilypond_file)

    print(grad_notes_list)
    print(grad_step_list)
    print(str(len(grad_step_list)) + " steps")
    print(str(sum(grad_step_list)) + "graduation bars")

    grio_out = [grad_notes_list,grad_step_list]
    return grio_out



def grito(bars_total_duration, voicesnumber, grio_out_istance, field_main_key, field_secondary_key, renorm_max, max_items, allow_singlevoice = False): 
    
    if field_secondary_key == "noveltyfeat":
        data = field_dataset.dataset[field_main_key][field_secondary_key]
    elif field_secondary_key == "deltatime" or field_secondary_key == "onsetfeat":
        data = field_dataset.normdata[field_main_key][field_secondary_key]
    else:
        print("Error, key " + field_secondary_key + " not found!")
        return None

    data = [int(item * renorm_max) for item in data]
    
    # Passi per l'offset (in valori da 0 a 8 quarti) uno per ogni elemento in uscita da GRIO (in questo caso sono 5):
    offsetvalue_list = set()  
    i = 0
    while len(offsetvalue_list) < max_items+1:  
        dataindex = i % len(data)
        offset = int(data[dataindex] % bars_total_duration)
        offsetvalue_list.add(offset)
        i += 1
    offsetvalue_list = list(offsetvalue_list)  
    
    # Lista con i valori, da 1 a 9 quarti, relativi alla posizione dalla quale viene ripercorso il pattern nell'interpolazione:
    i = 0
    graduation_lenght_list = []
    for item in grio_out_istance[1]:    
        dataindex = i % len(data)
        bars = int(data[dataindex] % bars_total_duration)+1
        graduation_lenght_list.append(bars)
        i += 1

    voicemute_coll = []
    if allow_singlevoice is True:
        voicestate_set = [[1,1,1],[1,0,1],[0,1,1],[1,1,0],[0,1,0],[0,0,1],[1,0,0]]
    else:
        voicestate_set =  [[1,1,1],[1,0,1],[0,1,1],[1,1,0]] 

    # Voci attive in ciascuna battuta di ciascuno dei passaggi di interpolazione:
    for i in range(0,int(sum(grio_out_istance[1]))):    
        dataindex = i % len(data) 
        index_choice = int(data[dataindex] % len(voicestate_set))
        state_voice = voicestate_set[index_choice]
        voicemute_coll.append(state_voice)
        i += 1
    
    print("lenght graduation_lenght_list: " + str(len(graduation_lenght_list)))
    print("lenght voicemute_coll: " + str(len(voicemute_coll)))

    print(offsetvalue_list)
    print(graduation_lenght_list)
    print(voicemute_coll)
    gritoOut = [offsetvalue_list, graduation_lenght_list, voicemute_coll]

    return gritoOut