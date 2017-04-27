class TreeNode:
    def __init__(self): 
        self.data = ""
        self.left = -1
        self.right = -1

    def set_data(self, data, left, right): 
        self.data = data
        self.left = left
        self.right = right        
    
    def printNode(self): 
        
        global d
        
        d+=1
        deep = d
        
        print('\n','   '*deep+self.data)
        
        if  (self.left != -1):
            if (type(self.left) != (str)):
                print('   '*deep+'L:', end =' ')
                if ((self.left.left != '') or (self.left.right != '')):
                    self.left.printNode()
                else:
                    print(self.left.data)
            else:
                print('   '*deep+'L:', self.left, sep = ' ')
        if (self.right != -1):
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
                
        s = brackets(s)           
        
        p1, p2 = len(s)-1, len(s)+3
        i=len(s)-1
        
        
        while i>=0:               
            if s[i] == ')':     
                i = skip(s, i-1)+1 
            elif s[i] == '+' or ((s[i] == '-') and (i != 0) and (s[i-1] != '(')):   
                p1 = p2-2                         
                p2 = i+1
                
                tempL = TreeNode()                  
                tempR = TreeNode()
                tempL.set_data(s[:p2-1], -1,-1)
                tempR.set_data(s[p2:p1+1], -1,-1)
                
                self.set_data(s[i], tempL, tempR)
                
                self.left.parse()   
                self.right.parse()
                return 0
            i-=1
        
        p1, p2 = len(s)-1, len(s)+3
        i=len(s)-1        
        
        while i>=0:                         
            if s[i] == ')':        
                i = skip(s, i-1)+1
            elif s[i] == '*' or s[i] == '/':                      
                p1 = p2-2                         
                p2 = i+1
                
                tempL = TreeNode()
                tempR = TreeNode()
                tempL.set_data(s[:p2-1], -1, -1)
                tempR.set_data(s[p2:p1+1], -1, -1)
                
                self.set_data(s[i], tempL, tempR)
                
                self.left.parse()
                self.right.parse()
                return 0
            i-=1            
        
        if s[0] == '-':                
                tempL = TreeNode()
                tempL.set_data(brackets(s[1:]), -1, -1)
                
                self.set_data('-', tempL, -1)
                
                self.left.parse()
                return 0
        return 1
    
    def generateCode(self):
        global result
        
        if (not isOperator(self.data)) or (self.left == -1 and self.right == -1):
            if isId(self.data) or isConst(self.data):
                result.append('move eax, ' + self.data)
            return
        
        if (self.data == '='):
            self.right.generateCode()
            result.append('mov '+ self.left.data + ', eax')
        elif (self.data == '-') and (self.right == -1): # unary operator -
            self.left.generateCode()
            result.append('neg eax')
        elif (isId(self.left.data) or isConst(self.left.data)) and (isId(self.right.data) or isConst(self.right.data)): # ID or CONST on left and right both
            result.append('mov eax, ' + self.left.data)
            result.append(oper(self.data) + ' eax, '+ self.right.data)
        elif ((isOperator(self.left.data)) and (isId(self.right.data) or isConst(self.right.data))): # binaty operator on left and ID or CONST on right
            self.left.generateCode()
            result.append(oper(self.data) + ' eax, '+ self.right.data)
        elif (self.data in '+*') and (isOperator(self.right.data)) and (isId(self.left.data) or isConst(self.left.data)): #commutative binary operator with ID or CONST on left and binary operator on right
            self.right.generateCode()
            result.append(oper(self.data) + ' eax, '+ self.left.data)
        elif (self.data in '-/') and (isOperator(self.right.data)) and (isId(self.left.data) or isConst(self.left.data)): #uncommutative binary operator with ID or CONST on left and binary operator on right  
            self.right.generateCode()
            result.append('mov edx, ' + self.left.data)
            result.append('xchg eax, edx')
            result.append(oper(self.data) + ' eax, edx')
        elif (isOperator(self.left.data)) and (isOperator(self.right.data)):   #both brunches are binary operators             
            self.right.generateCode()                  
            result.append('push eax') 
            self.left.generateCode()
            result.append('pop edx')
            result.append(oper(self.data) + ' eax, edx')              
        else:
            return 0

def skip(s, i):         
    ch = 1
    while (i >=0) and (ch!=0):
        if s[i] == ')':
            ch+=1
        elif s[i] == '(':
            ch-=1
        i-=1        
    return i

def brackets(s):        
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

def isId(s): 
    lett = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    numb = '0123456789_'
    if s[0] not in lett:
        return False
    for i in range(1,len(s)):
        if s[i] not in (lett+numb):
            return False
    return True

def isConst(s):
    numb = '0123456789.'
    if s.count('.')>1:
        return False
    for i in range (len(s)):
        if s[i] not in numb:
            return False
    return True

def isOperator(s):
    if s in '+-*/=':
        return True
    else:
        return False

def oper(s):
    if s=='+':
        return("add")
    elif s== '-':
        return ("sub")
    elif s == '*':
        return("imul")
    elif s == '/':
        return("idiv") 
print('Enter a string: ')
S = input()
d = -1 
result = []
S = ''.join(S.split()) 
parts = S.split('=') 
if len(parts)>2:    
    print('In this string more than one "="')
elif len(parts)<2:  
    print('This string has no "="')
elif not(isId(parts[0])):      
    print('It is not ID on the left of "="')
else:
    node = TreeNode() 
    tempL = TreeNode()
    tempR = TreeNode()
    tempL.set_data(parts[0], -1, -1) 
    tempR.set_data(parts[1], -1, -1)    
    node.set_data('=', tempL, tempR)
    node.right.parse()      
#    node.printNode()  
    node.generateCode()
    print("\nOptimal code:")
    for i in range (len(result)):
        print(result[i])


"""tests:
   
1. A=-B+(C-D)*2+(E+100)*3 
2. À1=D1*Ñ1+(Ñ2+02)*5-7
3. X=Y*Z*(B-C)*2+7
4. Y=(F1+F22)*10+7*(F13-F333)
5. À100=5*(À+D+C)*10-D
6. TABLE=(A+B)*R-F*(S-Y-Z)
7. Ò11=(-A)*B+C*D-E10*E11
8. Z100=Z1*(Z2+Z3)-Z4*(Z5-Z6)
9. RES=(C10-C20)*10+5*X*(Y-100)
"""