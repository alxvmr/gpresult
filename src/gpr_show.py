'''
Модуль для отображения результата вычитывания
'''
import gettext

'''
TODO: Добавить определение языка системы
'''
gettext.bindtextdomain("gpr_show", "/locales")
gettext.textdomain("gpr_show")
t = gettext.translation("gpr_show", localedir="locales", languages=['ru_RU'])
t.install()
_ = t.gettext


'''
TODO: Добавить в заголовок тип вывода (без пустых ключей, ...)
'''
def header_gen(type, name):
    s = _("\nA list of applied policies for the ")
    if type == 'user':
        s += _("user {}:\n\n").format(name)
    elif type == 'machine':
        s += _("machine {}:\n\n").format(name)
    return s

def formatted_show(policies, type, name):
    keys = policies['keys']
    values = policies['values']
    output = header_gen(type, name)

    max_n = -1
    max_v = -1
    for n, v in zip(keys, values):
        if n:
          l = len(n)
          if l > max_n:
              max_n = l
        if v:
            l = len(str(v))
            if l > max_v:
                max_v = l
    max_n += 3

    for n, v in zip(keys, values):
        output += "{:{max_n}s} {:{max_v}s}\n".format(str(n), str(v), max_n=max_n, max_v=max_v)
    
    print(output)