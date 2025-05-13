input_str = input("nhập X , Y")
dimension = [int(x) for x in input_str.split(',')]
rowNum = dimension[0]
colNum = dimension[1]

multilist = [[0 for col in range(colNum)] for now in range (rowNum)]
for row in range(rowNum):
    for col in range(rowNum):
        multilist[row][col] = row*col   
print(multilist)