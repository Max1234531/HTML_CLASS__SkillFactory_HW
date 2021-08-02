class Tag:
    '''основной класс для html-тегов от которого будем наследовать другие (TopLevelTag, HTML).'''

    def __init__(self, tag, is_single=False, klass=None, **kwargs ):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        self.children = []
        self.is_single = is_single
        self.is_child = False #моя разработка для правильных отступов, (спойлер: это работает)

        if klass:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            self.attributes[attr] = value
        
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return  str(self)

    #перегрузка оператора '+=' для добавления вложенных тегов
    def __iadd__(self, other):
        other.is_child = True   #опять-таки для отступов
        self.children.append(str(other))
        return self

    def __str__(self):

        att = []
        att_string = ""
        out = ""

        for attribute, value in self.attributes.items():
            att.append(' %s="%s"' % (attribute, value))
        att_string += "".join(att)

        if self.is_single:
            out = "<{tag}{attrs}/>".format(tag=self.tag, attrs=att_string)
        else:
            out = "<{tag}{attrs}>".format(tag=self.tag, attrs=att_string)
            if len(self.children) != 0:
                for child in self.children: out += '\n' + child
                out += '\n'
            else: out += "{text}".format(text = self.text)
            out += "</{tag}>".format(tag=self.tag)

        #реализация отступов (просто если тэг является потомком, он приписывает себе табуляцию перед началом строки)
        if self.is_child:
            out = out.replace("\n", "\n    ")
            return "    " + out
        else:
            return out


class TopLevelTag(Tag):
    '''Этот класс почти в точности повторяет Tag, поэтому применим наследование'''

    #т.к. эти теги всегда парные и не содержат текста поправим конструктор
    def __init__(self, tag, klass=None, **kwargs ):
        self.tag = tag
        self.attributes = {}
        self.children = []
        self.is_single = False
        self.is_child = False
    #кстати, благодаря умной реализации класса Tag ничего другого в этом классе менять не надо)


class HTML(Tag):
    '''опять наследовние... и пара дополнений'''

    #нам нужно лишь немного поправить некоторые методы для полноценной работы класса
    def __init__(self, output=None, klass=None, **kwargs ):
        self.tag = "html"
        self.attributes = {}
        self.children = []
        self.is_single = False
        self.output = output
        self.is_child = False

    #реализация сохранения (print или в файл)
    def __exit__(self, *args):
        if self.output:
            with open(self.output, 'w') as out_file:
                out_file.write(str(self))
        else:
            print(self)