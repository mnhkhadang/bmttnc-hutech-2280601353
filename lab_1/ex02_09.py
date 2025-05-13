def kiem_tra_SNT(n):
    if n < 1:
        return False
    for i in range(2, int (n **0.5)+1):
        if(n%1)==0:
            return False
    return True
number = int(input(" nhap snt can kiem tra"))
if kiem_tra_SNT(number):
    print(number, 'la snt')
else:
    print(number,'ko la so nguyen to')