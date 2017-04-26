class TreeNode:
    def __init__(self): # конструктор
        self.data = ""
        self.left = ""
        self.right = ""

    def set_data(self, data, left, right): 
        self.data = data
        self.left = left
        self.right = right        
    
    def printNode(self): # даже не пытайся вникать в суть этой функции, я сама тут перестала что-то понимать
        
        global d
        
        d+=1
        deep = d
        
        print('\n','   '*deep+self.data)
        
        if (type(self.left) != (str)):
            print('   '*deep+'L:', end =' ')
            if ((self.left.left != '') or (self.left.right != '')):
                self.left.printNode()
            else:
                print(self.left.data)
        else:
            print('   '*deep+'L:', self.left, sep = ' ')
            
        if type(self.right) != (str): 
            print('   '*deep+'R:',end =' ')
            if ((self.right.left != '') or (self.right.right != '')):
                self.right.printNode()
            else:
                print(self.right.data)
        else:
            print('   '*deep+'R:', self.right, sep = ' ')
        d-=1
    
    def parse(self):
        s = self.data
                
        s = brackets(s)           # убираем внешние скобки
        
        p1, p2 = len(s)-1, len(s)+3
        i=len(s)-1
        
        
        while i>=0:               # сложение и вычитаение (бинарное), ищем с конца
            if s[i] == ')':     
                i = skip(s, i-1)+1 # пропускаем внутренности скобок
            elif s[i] == '+' or ((s[i] == '-') and (i != 0) and (s[i-1] != '(')):   # проверяем, что минус не унарный             
                p1 = p2-2                         
                p2 = i+1
                
                tempL = TreeNode()                  
                tempR = TreeNode()
                tempL.set_data(s[:p2-1], '', '')
                tempR.set_data(s[p2:p1+1], '', '')
                
                self.set_data(s[i], tempL, tempR)
                
                self.left.parse()   # рекурсивно вызываем эту функцию от ее новоиспеченных листов
                self.right.parse()
                return 0
            i-=1
        
        p1, p2 = len(s)-1, len(s)+3
        i=len(s)-1        
        
        while i>=0:                         # умножение и деление
            if s[i] == ')':        
                i = skip(s, i-1)+1
            elif s[i] == '*' or s[i] == '/':                      
                p1 = p2-2                         
                p2 = i+1
                
                tempL = TreeNode()
                tempR = TreeNode()
                tempL.set_data(s[:p2-1], '', '')
                tempR.set_data(s[p2:p1+1], '', '')
                
                self.set_data(s[i], tempL, tempR)
                
                self.left.parse()
                self.right.parse()
                return 0
            i-=1            
        
        if s[0] == '-':                #унаный минус
                tempL = TreeNode()
                tempL.set_data(s[1:], '', '')
                
                self.set_data('-', tempL, '')
                
                self.left.parse()
                return 0
        return 1
    
            


def skip(s, i):         # пропуск внутренних скобок
    ch = 1
    while (i >=0) and (ch!=0):
        if s[i] == ')':
            ch+=1
        elif s[i] == '(':
            ch-=1
        i-=1        
    return i

def brackets(s):        # отбрасывание внешних скобок
    if (s[0] == '(') and (s[len(s)-1] == ')'):
        ch=1
        i = 1
        while (i <len(s)) and (ch!=0):
            if s[i]=='(':
                ch+=1
            elif s[i]==')':
                ch-=1
            i+=1
        if ch==0 and i==len(s):
            return s[1:len(s)-1]
        else:
            return s
    else:
        return s

def isId(s): # провека на то, что идентификатор норм 
    lett = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    numb = '0123456789'
    if s[0] not in lett:
        return False
    for i in range(1,len(s)):
        if s[i] not in (lett+numb):
            return False
    return True
print('Enter a string: ')
S = input()
d = -1 # глубина листа (нужно для вывода)
S = ''.join(S.split()) # убираем все пробелы
parts = S.split('=') # разделяем строку по знаку "="
if len(parts)>2:    # если частей больше 2, то и "=" было не одно
    print('In this string more than one "="')
elif len(parts)<2:  # если меньше 2, то "=" не было
    print('This string has no "="')
elif not(isId(parts[0])):      # если справа от "=" неправильный идентификатор
    print('It is not ID on the left of "="')
else:
    node = TreeNode() # создаем корень
    tempL = TreeNode()
    tempR = TreeNode()
    tempL.set_data(parts[0], '', '') 
    tempR.set_data(parts[1], '', '')    
    node.set_data('=', tempL, tempR)
    node.right.parse()      # парсим правую часть (левая - идентификатор)
    node.printNode()    
    





