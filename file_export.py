# Header should be a string with the variables separated by a |
# data should be a list of lists : data[0] should be all time points of var0, etc...
# if not sure, execute the script as main file
def list_to_csv(header, data):
    valid_data = True
    error_message = ""
    if data is None:
        valid_data = False
        error_message = "No data to show"
    elif type(data) is not list:
        valid_data = False
        error_message = "Wrong data type"
    else:
        l0 = len(data[0])
        temp = True
        for e in data:
            temp = temp and (len(e) == l0)
        if not temp:
            valid_data = False
            error_message = "Different data lengths"

    if not valid_data:
        with open('export.csv', 'w') as fich:
            fich.write(error_message)
        return
    with open('export.csv', 'w') as fich:
        fich.write(header+"\n")
        for t in range(len(data[0])):
            for var in data[:-1]:
                fich.write(str(var[t])+"|")
            fich.write(str(data[-1][t])+"\n")

if __name__ == "__main__":
    test_data = []
    lon = 10
    nb_var = 5
    for i_var in range(nb_var):
        liste_temp = []
        for k in range(lon):
            liste_temp.append(i_var*10+k)
        test_data.append(liste_temp)

    test_data.append(["e"]*lon)

    print(test_data)
    list_to_csv("k0|k1|k2|k3|k4|l", test_data)