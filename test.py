import PySimpleGUI as sg

layout = [
    [sg.Frame("I'm a frame",[[sg.Button(button_text='Change size')]],key='body')]
]

window = sg.Window('Window',layout)
window.finalize()


while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    if event == 'Change size':
        window['Change size'].set_size(size=(200, 200))
        window.refresh()
