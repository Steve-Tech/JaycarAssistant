def openCSV(filename):
    file = open("CSVs\\" + filename, 'r')
    split1 = []
    for line in file:
        split1.append(line.replace(',\n', '').split(','))
    file.close()

    split2 = []
    for i in split1:
        i1 = []
        for j in i:
            i1.append(j.split('&'))
        split2.append(i1)
    return split2


class Resistors:
    table = openCSV('Resistors.csv')

    pricing = [['', ['Watts', 'Qty 1+', 'Qty 25+', 'Qty 100+']], ['bg-warning text-dark', ['0.25W', '$0.48', '$0.34', '$0.29']], ['bg-light text-dark', ['0.5W', '$0.55', '$0.39', '$0.33']], ['bg-success', ['1W', '$0.48', '$0.34', '$0.29']], ['bg-primary', ['5W', '$0.48', '$0.34', '$0.29']], ['bg-purple', ['10W', '$1.80', '$1.25', '$1.05']]]

    message = ""

    def get_colour(countIn):
        count = (countIn - 11) / 4
        if count <= 31: return "bg-light text-dark"
        elif count <= 38: return "bg-warning text-dark"
        elif count <= 59: return "bg-success"
        elif count <= 70: return "bg-primary"
        elif count <= 75: return "bg-purple"
        else: return ""


class Potentiometers:
    table = openCSV('Potentiometers.csv')

    pricing = None

    message = "Starts from row 5"

    def get_colour(countIn):
        count = (countIn - 2) / 4
        if count <= 5: return "bg-light text-dark"
        elif count <= 7: return "bg-primary"
        elif count <= 8: return "bg-light text-dark"
        elif count <= 11: return "bg-warning text-dark"
        elif count <= 14: return "bg-success"
        elif count <= 20: return "bg-purple"
        elif count <= 23: return "bg-light text-dark"
        elif count <= 29: return "bg-primary"
        else: return ""


class Capacitors:
    table = openCSV('Capacitors.csv')

    pricing = None

    message = "Starts from row 6 on the Left"
    message2 = "Right side"

    def get_colour(countIn):
        count1 = (countIn - 10) / 4
        count2 = (countIn - 139) / 4
        if count1 <= 9: return "bg-light text-dark"
        elif count1 <= 11: return "bg-purple"
        elif count1 <= 13: return "bg-purple"
        elif count1 <= 26: return "bg-success"
        elif count1 <= 27: return "bg-light text-dark"
        elif count1 <= 29: return "bg-warning text-dark"
        #elif count1 <= 31: return "bg-light text-dark"
        elif count1 <= 32: return "bg-light text-dark"

        elif count2 <= 4: return "bg-purple"
        elif count2 <= 9: return "bg-success"
        elif count2 <= 13: return "bg-warning text-dark"
        elif count2 <= 17: return "bg-light text-dark"
        elif count2 <= 19: return "bg-success"
        elif count2 <= 21: return ""
        elif count2 <= 27: return "bg-purple"
        elif count2 <= 36: return "bg-warning text-dark"
        elif count2 <= 39: return "bg-primary"
        elif count2 <= 42: return "bg-purple"
        else: return ""


class CapacitorsE:
    table = openCSV('CapacitorsE.csv')

    pricing = None

    message = "Starts from row 8"

    def get_colour(countIn):
        return "bg-light text-dark"


if __name__ == '__main__':
    print('Resistors', Resistors.table)
    print('Potentiometers', Potentiometers.table)
    print('Capacitors', Capacitors.table)
    print('CapacitorsE', CapacitorsE.table)