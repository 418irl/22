def adder(x,y):
    a=x+y
    return (a)

def subtractor(x,y):
    b=x-y
    return (b)

def multiplier(x,y):
    c=x*y
    return (c)

def divider(x,y):
    d=x/y
    return (d)

x= int(input("Enter x"))
y= int(input("Enter y"))
op=input("Enter which operation you want to try")
op=int(op)
print(type(op))
if op==1:
    print("x+y=",adder(x,y))
elif op==2:
    print("x-y=",subtractor(x,y))
elif op==3:
    print("x*y=",multiplier(x,y))
elif op==4:
    print("x/y=",divider(x,y))
else:
    print("operation not chosen correctly")
