import PySimpleGUI as sg

layout = [[sg.Checkbox("Reject defaults", default=False, enable_events=True, key="reject")],
          [sg.Text("Enter three values", visible=False, key="instruct")],
          [sg.Multiline(enter_submits=False, autoscroll=True, visible=False, do_not_clear=True, key="override")]]
layout += [[sg.Button('Read'), sg.Exit()]]

window = sg.Window("Select inputs", layout)
while True:
    event, values = window.Read()
    print(values)
    if values["reject"]:
        window.Element('instruct').Update(visible=True)
        window.Element('override').Update(visible=True)
        if event is None or event == 'Exit':
                break