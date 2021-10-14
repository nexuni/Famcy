def updateList(list_to_update, content):
    for i in range(len(list_to_update)):
        list_to_update.pop()

    for temp in content:
        list_to_update.append(temp)