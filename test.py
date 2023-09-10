with open('source/id_list.txt', 'r', encoding='utf-8') as idlist:
    idlist = idlist.read()
    idlist = idlist.split('\n')
    result = list(map(int, idlist))

print(result)
print(type(result[0]))
print(type(result))
