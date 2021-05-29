import PySimpleGUI as sg

sg.ChangeLookAndFeel('Dark')
sg.SetOptions(element_padding=(0,0))

layout = [
          [sg.ReadFormButton('Numbers', button_color=('white', 'black'), key='start'),
           sg.ReadFormButton('Letters', button_color=('white', 'firebrick4'), key='stop')],
          [sg.Combo(('Numbers', 'Letters'), key='combo1', change_submits=True), sg.Combo(('a', 'b', 'c', 'd'), key='combo2')]
          ]

form = sg.FlexForm("Change Combo Values", default_element_size=(12,1), text_justification='r', auto_size_text=False, auto_size_buttons=False,
                   default_button_element_size=(12,1))
form.Layout(layout)
while True:
    button, values = form.Read()
    if button is None:
        exit(69)
    if button is 'Numbers':
        form.FindElement('combo1').Update(values=(7,8,9,0))
        form.FindElement('combo2').Update(values=(1,2,3,4))
    elif button is 'Letters':
        form.FindElement('combo1').Update(values=('a','b','c','d'))
        form.FindElement('combo2').Update(values=('e','f','g','h'))

    if values['combo1'] == 'Numbers':
        form.FindElement('combo2').Update(values=(1,2,3,4))
    elif values['combo1'] == 'Letters':
        form.FindElement('combo2').Update(values=('e','f','g','h'))