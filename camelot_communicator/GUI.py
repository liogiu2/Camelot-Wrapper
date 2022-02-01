import PySimpleGUI as sg
import multiprocessing


def GUI(queueIn : multiprocessing.Queue, queueOut : multiprocessing.Queue):
    entity_list_column = []
    
    other_list_column = []

    #starting_message = queue.get()
    starting_state = queueIn.get()

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
        [sg.Text('Camelot instruction'), sg.Input(key='-INCI-', size = (100, 1)),sg.Button('Send', key='_SEND_CI_')],
        #[sg.Text('PDDL relation'), sg.Input(key='-INPR-', size = (100, 1)),sg.Button('Send', key='_SEND_PR_')],
        [sg.Text('PDDL action'), sg.Input(key='-INPA-', size = (100, 1)),sg.Button('Send', key='_SEND_PA_')],
        [sg.Button('Exit'), 
        sg.Button('Update')
        ],
    ]

    window = sg.Window('Window Title', layout)
    #sg.show_debugger_window(location=(0, 0))
    while True:             # Event Loop
        event, values = window.read(timeout=100)
        if event == '_SEND_CI_':
            if values['-INCI-'] != '':
                send = {"CI": values['-INCI-']}
                queueOut.put(send)
        # if event == '_SEND_PR_':
        #     if values['-INPR-'] != '':
        #         send = {"PR": values['-INPR-']}
        #         queueOut.put(send)
        if event == '_SEND_PA_':
            if values['-INPA-'] != '':
                send = {"PA": values['-INPA-']}
                queueOut.put(send)
        if event == "Update" or event == sg.TIMEOUT_KEY:
            new_state = None
            try:
                new_state = queueIn.get_nowait()
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
                            window.extend_layout(window['-COL2-'], [[sg.T(str(relation), key="-RELATION-"+str(j_n), text_color='black')]])
                            window['-COL2-'].contents_changed() 
                        else:
                            if window["-RELATION-"+str(j_n)].get() == str(relation):
                                #window["-RELATION-"+str(j_n)].update(value = str(relation), text_color = "black")
                                pass
                            else:
                                window["-RELATION-"+str(j_n)].update(value = str(relation), text_color = "black")
                        j_n += 1
                    j = j_n
                    window['-COL2-'].contents_changed() 

                    window.refresh()
            else:
                continue
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
    window.close()

