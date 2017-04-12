def scroll(arr):
    result = []
    i = 0
    temp = []
    while i < len(arr):
        temp.append([arr[i], arr[i + 1]])
        i = i + 2
    snake_arr = []
    i = 0
    while i < len(temp):
        snake_arr.append(temp[i][1])
        i = i + 1
    i = len(temp) - 1
    while i > 0:
        snake_arr.append(temp[i][0])
        i = i-1
    new_snake_arr = []
    new_snake_arr.append(snake_arr[len(snake_arr)-1])
    i=0
    while i<len(snake_arr)-1:
        new_snake_arr.append(snake_arr[i])
        i=i+1
    result.append(arr[0])
    result.append(new_snake_arr[0])
    i=0
    new_arr=[]
    while i<len(new_snake_arr)/2:

        new_arr.append(new_snake_arr[len(new_snake_arr)-1-i])
        new_arr.append(new_snake_arr[i + 1])
        i=i+1
    i=0
    while i<len(new_arr):
        result.append(new_arr[i])
        i=i+1
    return result

print scroll([1, 3, 5, 2, 7, 4, 8, 6])