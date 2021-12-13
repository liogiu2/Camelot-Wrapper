import PySimpleGUI as sg
import multiprocessing


def GUI(queue : multiprocessing.Queue):
    entity_list_column = []
    
    other_list_column = []

    #starting_message = queue.get()
    starting_state = queue.get()

    i = 0
    for entity in starting_state.entities:
        entity_list_column.append([sg.T(str(entity), key="-ENTITY-"+str(i))])
        i += 1
    
    j = 0
    for relation in starting_state.relations:
        other_list_column.append([sg.T(str(relation), key="-RELATION-"+str(j))])
        j += 1

    layout = [
        [
            sg.Column(entity_list_column, scrollable=True ,vertical_scroll_only=True, size=(300,400), key='-COL1-'),
            sg.VSeperator(),
            sg.Column(other_list_column, scrollable=True ,vertical_scroll_only=True, size=(400,400), key='-COL2-'),
        ],
        [sg.Button('Exit'), 
        sg.Button('Update')
        ],
    ]

    window = sg.Window('Window Title', layout)
    #sg.show_debugger_window(location=(0, 0))
    while True:             # Event Loop
        event, values = window.read(timeout=100)
        if event == "Update" or event == sg.TIMEOUT_KEY:
            new_state = None
            try:
                new_state = queue.get_nowait()
            except Exception:
                continue
            if new_state is not None:
                if type(new_state) is str:
                    window['-Message-'].update(value = str(new_state))
                    window.refresh()
                else:
                    i_n = 0
                    for entity in new_state.entities:
                        if i_n >= i:
                            window.extend_layout(window['-COL1-'], [[sg.T(str(entity), key="-ENTITY-"+str(i_n), text_color='red')]])
                            window['-COL1-'].contents_changed()
                        else:
                            if window["-ENTITY-"+str(i_n)].get() == str(entity):
                                window["-ENTITY-"+str(i_n)].update(value = str(entity), text_color = "black")
                            else:
                                window["-ENTITY-"+str(i_n)].update(value = str(entity), text_color = "red")   
                        i_n += 1
                    i = i_n
                    window['-COL1-'].contents_changed() 

                    j_n = 0
                    for relation in new_state.relations:
                        if j_n >= j:
                            window.extend_layout(window['-COL2-'], [[sg.T(str(relation), key="-RELATION-"+str(j_n), text_color='red')]])
                            window['-COL2-'].contents_changed() 
                        else:
                            if window["-RELATION-"+str(j_n)].get() == str(relation):
                                #window["-RELATION-"+str(j_n)].update(value = str(relation), text_color = "black")
                                pass
                            else:
                                window["-RELATION-"+str(j_n)].update(value = str(relation), text_color = "red")
                        j_n += 1
                    j = j_n
                    window['-COL2-'].contents_changed() 

                    window.refresh()
            else:
                continue
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
    window.close()

