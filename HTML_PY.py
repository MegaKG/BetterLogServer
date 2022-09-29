#!/usr/bin/env python3


#Handles the extra value
def _procExtra(extra):
    EXTRA = ''
    for key in extra:
        EXTRA += str(key) + '=\"' + str(extra[key]) + '\" '
    if EXTRA != '':
        EXTRA = EXTRA[:-1]
        EXTRA = ' ' + EXTRA
    return EXTRA

#This is the parent class that contains all the methods
class _major:
    def __init__(self):
        pass

    def append(self,*CONTENT):
        for i in CONTENT:
            self.content.append(i)

    def __str__(self):
        INNER = ''
        for C in self.content:
            INNER += str(C)

        return '<' + self.TAG + _procExtra(self.extra) + '>\n' + INNER + '\n</' + self.TAG + '>\n'

    def __repr__(self):
        return self.__str__()

    def standardinit(self,CONTENT,EXTRA):
        self.content = []
        for i in CONTENT:
            self.content.append(i)
        self.extra = EXTRA



#These are adaptations of the major (parent) class that are specific to HTML tags
class html(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'html'
        self.standardinit(CONTENT,EXTRA)
        
class body(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'body'
        self.standardinit(CONTENT,EXTRA)

class header(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'header'
        self.standardinit(CONTENT,EXTRA)

class head(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'head'
        self.standardinit(CONTENT,EXTRA)

class footer(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'footer'
        self.standardinit(CONTENT,EXTRA)

class div(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'div'
        self.standardinit(CONTENT,EXTRA)

class form(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'form'
        self.standardinit(CONTENT,EXTRA)

class span(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'span'
        self.standardinit(CONTENT,EXTRA)

class p(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'p'
        self.standardinit(CONTENT,EXTRA)

class a(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'a'
        self.standardinit(CONTENT,EXTRA)

class b(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'b'
        self.standardinit(CONTENT,EXTRA)

class pre(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'pre'
        self.standardinit(CONTENT,EXTRA)

class button(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'button'
        self.standardinit(CONTENT,EXTRA)

class script(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'script'
        self.standardinit(CONTENT,EXTRA)

class meta(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'meta'
        self.standardinit(CONTENT,EXTRA)

class h(_major):
    def __init__(self,*CONTENT,Layer=1,EXTRA={}):
        self.TAG = 'h' + str(Layer)
        self.standardinit(CONTENT,EXTRA)

class ul(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'ul'
        self.standardinit(CONTENT,EXTRA)

class li(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'li'
        self.standardinit(CONTENT,EXTRA)

class style(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'style'
        self.standardinit(CONTENT,EXTRA)

class main(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'main'
        self.standardinit(CONTENT,EXTRA)

class frame(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'frame'
        self.standardinit(CONTENT,EXTRA)

class dl(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'dl'
        self.standardinit(CONTENT,EXTRA)

class dt(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'dt'
        self.standardinit(CONTENT,EXTRA)

class dd(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'dd'
        self.standardinit(CONTENT,EXTRA)

class table(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'table'
        self.standardinit(CONTENT,EXTRA)

class tr(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'tr'
        self.standardinit(CONTENT,EXTRA)

class th(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'th'
        self.standardinit(CONTENT,EXTRA)

class td(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'td'
        self.standardinit(CONTENT,EXTRA)

class hinput:
    def __init__(self,Type,Name=None,Value=None,EXTRA={}):
        self.extra = EXTRA
        self.Type = Type
        self.Value = Value
        self.Name = Name

    def __repr__(self):
        return self.__str__()

    def __str__(self):

        Name = ''
        if self.Name != None:
            Name = ' name=\"' + str(self.Name) + '\"' + ' id=\"' + str(self.Name) + '\"'
        
        Value = ''
        if self.Value != None:
            Value = ' value=\"' + str(self.Value) + '\"'
        
        return '<input type=\"' + str(self.Type) + '\"' + Name + Value + _procExtra(self.extra) + '>\n'

class label(_major):
    def __init__(self,*CONTENT,FOR=None,EXTRA={}):
        self.TAG = 'label'
        self.standardinit(CONTENT,EXTRA)
        self.FOR = FOR

    def __str__(self):
        INNER = ''
        for i in self.content:
            INNER += str(i)

        FOR = ''
        if self.FOR != None:
            FOR = ' for=\"' + str(self.FOR) + '\"'

        return '<' + self.TAG + FOR + _procExtra(self.extra) + '>\n' + INNER + '\n</' + self.TAG + '>\n'



class link:
    def __init__(self,Rel,Resource,EXTRA={}):
        self.extra = EXTRA
        self.Rel = Rel
        self.Resource = Resource

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '<input rel=\"' + str(self.Rel) + '\" href=\"' + str(self.Rel) + '\" ' + _procExtra(self.extra) + '>\n'


class hr:
    def __init__(self,EXTRA={}):
        self.extra = EXTRA

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '<hr' + _procExtra(self.extra) + '>\n'


class br:
    def __init__(self,EXTRA={}):
        self.extra = EXTRA

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '<br' + _procExtra(self.extra) + '>\n'


class base:
    def __init__(self,URL,EXTRA={}):
        self.extra = EXTRA
        self.URL = URL

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '<base href=\"' + str(self.URL) + '\" ' + _procExtra(self.extra) + '>\n'


class em(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'em'
        self.standardinit(CONTENT,EXTRA)


class s(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 's'
        self.standardinit(CONTENT,EXTRA)

class q(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'q'
        self.standardinit(CONTENT,EXTRA)

class i(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'i'
        self.standardinit(CONTENT,EXTRA)

class img(_major):
    def __init__(self,Source,*CONTENT,EXTRA={}):
        self.TAG = 'img'
        self.standardinit(CONTENT,EXTRA)
        self.Source = Source

    def __str__(self):
        INNER = ''
        for i in self.content:
            INNER += str(i)

        return '<' + self.TAG + ' src=\"' + str(self.Source) + '\" ' + _procExtra(self.extra) + '>\n' + INNER + '\n</' + self.TAG + '>\n'


class video(_major):
    def __init__(self,Source,*CONTENT,EXTRA={}):
        self.TAG = 'video'
        self.standardinit(CONTENT,EXTRA)
        self.Source = Source

    def __str__(self):
        INNER = ''
        for i in self.content:
            INNER += str(i)

        return '<' + self.TAG + ' src=\"' + str(self.Source) + '\" ' + _procExtra(self.extra) + '>\n' + INNER + '\n</' + self.TAG + '>\n'


class u(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'u'
        self.standardinit(CONTENT,EXTRA)

class svg(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'svg'
        self.standardinit(CONTENT,EXTRA)

class custom(_major):
    def __init__(self,TAG,*CONTENT,EXTRA={}):
        self.TAG = TAG
        self.standardinit(CONTENT,EXTRA)

class samp(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'samp'
        self.standardinit(CONTENT,EXTRA)

class ol(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'ol'
        self.standardinit(CONTENT,EXTRA)

class strong(_major):
    def __init__(self,*CONTENT,EXTRA={}):
        self.TAG = 'strong'
        self.standardinit(CONTENT,EXTRA)

class textarea(_major):
    def __init__(self,Name=None,*Value,EXTRA={}):
        self.TAG = 'textarea'
        self.standardinit(Value,EXTRA)
        self.Name = Name
    
    def __str__(self):
        Name = ''
        if self.Name != None:
            Name = ' name=\"' + str(self.Name) + '\"' + ' id=\"' + str(self.Name) + '\"'

        INNER = ''
        for C in self.content:
            INNER += str(C)

        return '<' + self.TAG + Name + _procExtra(self.extra) + '>\n' + INNER + '\n</' + self.TAG + '>\n'


class option(_major):
    def __init__(self,Value='',*Content,EXTRA={}):
        self.TAG = 'option'
        if len(Content) == 0:
            Content = [Value]
        self.standardinit(Content,EXTRA)
        self.Value = Value
    
    def __str__(self):
        Value = ' value=\"' + str(self.Value) + '\"'
        INNER = ''
        for C in self.content:
            INNER += str(C)

        return '<' + self.TAG + Value + _procExtra(self.extra) + '>\n' + INNER + '\n</' + self.TAG + '>\n'


class datalist(_major):
    def __init__(self,ID,*CONTENT,EXTRA={}):
        self.TAG = 'datalist'
        self.standardinit(CONTENT,EXTRA)
        self.ID = ID

    def __str__(self):
        INNER = ''
        for C in self.content:
            INNER += str(C)

        return '<' + self.TAG + ' id=\"' + str(self.ID) + '\"' +  _procExtra(self.extra) + '>\n' + INNER + '\n</' + self.TAG + '>\n'

class select(_major):
    def __init__(self,Name,*CONTENT,EXTRA={}):
        self.TAG = 'datalist'
        self.standardinit(CONTENT,EXTRA)
        self.ID = Name

    def __str__(self):
        INNER = ''
        for C in self.content:
            INNER += str(C)

        return '<' + self.TAG + ' id=\"' + str(self.ID) + '\"' + ' name=\"' + str(self.ID) + '\"' +  _procExtra(self.extra) + '>\n' + INNER + '\n</' + self.TAG + '>\n'

#The Mapping for those who have trouble 
orderedList = ol
image = img
underline = u
heading = h
bold = b
hyperlink = a
preformatted = pre
unorderedList = ul
listItem = li
inputLabel = label
descriptionList = dl
descriptionTerm = dt
descriptionValue = dd
tableRow = tr
tableHeaderCell = th
tableCell = td
emphasised = em
verticalBreak = br
horizontalRule = hr
strikethrough = s
quotation = q
italic = i


#Here is some simple text stuff
class t_bold:
    pass

class t_underline:
    pass

class t_italic:
    pass

class t_emphasise:
    pass

class t_strikethrough:
    pass

class text:
    def __init__(self,Content,*FORMAT):
        self.cont = Content
        for i in FORMAT:
            if i is t_bold:
                self.cont = bold(self.cont)
            elif i is t_underline:
                self.cont = underline(self.cont)
            elif i is t_italic:
                self.cont = italic(self.cont)
            elif i is t_emphasise:
                self.cont = emphasised(self.cont)
            elif i is t_strikethrough:
                self.cont = strikethrough(self.cont)

    def __str__(self):
        return self.cont

    def __repr__(self):
        return self.cont


#Create Table from 2d ARR
class table2dArr:
    def __init__(self,Array):
        self.array = Array

    def __str__(self):
        OUT = table()
        H = self.array[0]
        HR = tr()
        for cell in H:
            HR.append(th(cell))
        OUT.append(HR)

        for datarow in self.array[1:]:
            TR = tr()
            for datacell in datarow:
                TR.append(td(datacell))
            OUT.append(TR)
        return OUT
            
    def __repr__(self):
        return self.__str__()

#Create Table from Dict Array
class tableDictArr:
    def __init__(self,Array):
        self.array = Array

    def __str__(self):
        OUT = table()
        H = self.array.keys()
        HR = tr()
        for cell in H:
            HR.append(th(cell))
        OUT.append(HR)

        for i in range(len(self.array[H[0]])):
            TR = tr()
            for key in H:
                TR.append(td(self.array[key][i]))
            OUT.append(TR)

        return OUT
            
    def __repr__(self):
        return self.__str__()

if __name__ == '__main__':
    print(html(body("HELLO")))