# 列表框行序调整
# 导入库
import PySimpleGUI as sg
text = ['第一行', '第二行', '第三行', '第四行']

layout = [
    [sg.T('列表内容：')],
    [
     sg.Listbox(text, key='-TEXT-', select_mode='single', enable_events=True,
                background_color='white', text_color='red', size=(80, 6))
     ],
    [sg.B('刷新显示'), sg.B('上调'), sg.B('下调'), sg.B('置首'), sg.B('置尾')]

]

# 创建主窗口，设置窗口名，给窗口传入layout指明的组件
window = sg.Window('文本行序调整', layout, size=(600, 200))

while True:
    # 读取事件和输入型组件的返回值,values返回值是一个字典
    event, values = window.read()
    # 控制台输出，便于调试
    print(event, values)
    # 点击x退出
    if event == sg.WIN_CLOSED:
        break
    if event == '刷新显示':
        window['-TEXT-'].update(text)

    if event == '置首':
        sss = window['-TEXT-'].get_indexes()[0]
        if sss == 0:
            sg.popup('已到达最顶部')
        else:
            temp = text[sss]
            del text[sss]
            text.insert(0, temp)
            window['-TEXT-'].update(text, set_to_index=0)

    if event == '置尾':
        sss = window['-TEXT-'].get_indexes()[0]
        if sss == len(text)-1:
            sg.popup('已到达最底部')
        else:
            temp = text[sss]
            del text[sss]
            text.append(temp)
            window['-TEXT-'].update(text, set_to_index=len(text)-1)
    if event == '上调':
        sss = window['-TEXT-'].get_indexes()[0]
        if sss == 0:
            sg.popup('已经到达最顶部')
        else:
            temp = text[sss]
            del text[sss]
            text.insert(sss-1, temp)
            window['-TEXT-'].update(text, set_to_index=sss-1)
    if event == '下调':
        sss = window['-TEXT-'].get_indexes()[0]
        if sss == len(text)-1:
            sg.popup('已经到达最底部')
        else:
            temp = text[sss]
            del text[sss]
            text.insert(sss+1, temp)
            window['-TEXT-'].update(text, set_to_index=sss+1)

# 最后关闭窗口，防止循环中的退出事件失效
window.close()
