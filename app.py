import flask
from flask import Flask
from flask_fontawesome import FontAwesome

import data_file

app = Flask(__name__)
fa = FontAwesome(app)


@app.route('/')
def main_page():
    if flask.request.remote_addr == '127.0.0.1':  # Check if it is being accessed by itself (for screensaver)
        from random import randint  # Moves the menu to a random part of the screen to act as a screen saver
        return flask.render_template("main.html", p_top=randint(0, 20), p_left=randint(-10, 15))
    else: return flask.render_template("main.html", p_top=None, p_left=None)  # Setting p_top or p_left to None disables the screen saver


@app.route('/resistors')
def resistor_page():
    if not flask.request.args: return flask.render_template("query.html", title='What Resistance?', buttons=['K', 'M'], unit='O', type='R')
    query = phrase_input(flask.request.args['value'], 'R')
    if query is None:  # phrase_input() checks if it has the needed characters to be a good query, otherwise it returns None
        return flask.render_template("error.html", title="Please enter a valid resistance", subtitle="Redirecting to the first page in 10 seconds..."), 400
    else:
        print("R: Got Query", query)
        #return create_data(query, layout.resistors)
        return create_data(query, data_file.Resistors.table)

@app.route('/capacitors_e')
def capacitor_e_page():
    if not flask.request.args: return flask.render_template("query.html", title="What Capacitance?", buttons=['U', 'N', 'P'], unit='F', type='C')
    if not 'volts' in flask.request.args: return flask.render_template("query.html", title="What Voltage?", unit='V', type='C', query=flask.request.query_string.decode())
    query = phrase_input(flask.request.args['value'], 'F')
    volts = flask.request.args['volts']
    if query is None:
        return flask.render_template("error.html", title="Please enter a valid capacitance", subtitle="Redirecting to the first page in 10 seconds..."), 400
    else:
        print("C: Got Query", query, volts + 'V')
        return create_data(query, data_file.CapacitorsE.table)

@app.route('/capacitors_o')
def capacitor_o_page():
    if not flask.request.args: return flask.render_template("query.html", title="What Capacitance?", buttons=['U', 'N', 'P'], unit='F', type='C')
    if not 'volts' in flask.request.args: return flask.render_template("query.html", title="What Voltage?", unit='V', type='C', query=flask.request.query_string.decode())
    query = phrase_input(flask.request.args['value'], 'F')
    volts = flask.request.args['volts']
    if query is None:
        return flask.render_template("error.html", title="Please enter a valid capacitance", subtitle="Redirecting to the first page in 10 seconds..."), 400
    else:
        print("C: Got Query", query, volts + 'v')
        return create_data(query, data_file.Capacitors.table)


@app.route('/pots')
def potentiometer_page():
    if not flask.request.args: return flask.render_template("query.html", title='What Resistance?', buttons=['K', 'M'], unit='O', type='P')
    query = phrase_input(flask.request.args['value'], 'R')
    if query is None:
        return flask.render_template("error.html", title="Please enter a valid resistance", subtitle="Redirecting to the first page in 10 seconds..."), 400
    else:
        print("P: Got Query", query)
        return create_data(query, data_file.Potentiometers.table)

@app.errorhandler(404)
def page_not_found(error):  # This will catch errors and redirect to the home screen so the Raspberry Pi does not get stuck on one page
    app.logger.error(error, flask.request.path)
    return flask.render_template("error.html", title="An Error Occured", subtitle="Page not found.", error=error), 404


@app.errorhandler(500)
def server_error(error):
    app.logger.error(error, flask.request.path)
    return flask.render_template("error.html", title="An Error Occured", subtitle="A server error occurred", error=error), 500


@app.errorhandler(Exception)
def unhandled_exception(e):
    app.logger.error(e, flask.request.path)
    return flask.render_template("error.html", title="An Error Occured", subtitle="An exception occurred", error=e), 500


def phrase_input(arg, type):
    query = arg
    queryup = query.upper()  # The query should already be uppercase, but if not this fixes that
    if not query.count('.') <= 1:  # The query should only contain 1 or no periods
        return None
    unit_to_decimal = queryup[:]
    unitcount = 0
    for i in ['K', 'M', 'U', 'N', 'P', type]:
        unit_to_decimal = unit_to_decimal.replace(i, '.')  # Turns the query value into a decimal
        unitcount += queryup.count(i)  # Counts the amount of a certain unit
    if unitcount >= 2: return None     # So if there is more than 1 it can return None
    if not unit_to_decimal.replace('.', '').isdigit(): return None  # Checks if the query does not contain any forign characters
    if unit_to_decimal[-1] == '.': unit_to_decimal = unit_to_decimal[:-1]  # Removes the decimal if it's unneeded

    for i in ['K', 'M', 'U', 'N', 'P', type]:
        if i == type or queryup.find(i) != -1:  # if i contains the same unit as the query
            print(queryup, i, queryup.find(i))
            if unit_to_decimal.count('.') == 1:
                return unit_to_decimal.replace('.', i)  # if i contains a decimal replace it with the unit
            elif unit_to_decimal.count('.') == 0:
                return (unit_to_decimal + i).replace('000R', 'K').replace('000K', 'M')  # if i does not contain a decimal concatanate the unit and simplify
            else: return None  # I know this should theoretically never happen, but if it contains negative decimals or similar return None


def create_data(query, layout_item):
    table_data = []
    count = 0
    item_count = 0

    for i in layout_item:  # for the line list i the full list
        data2 = []
        for j in i:  # for the box list in the line list
            data = ['']
            for k in j:  # for the item list in the box list
                count += 1
                if layout_item is data_file.Resistors.table:
                    if k == query or k == query + '0':  # if the item is the query
                        data[0] += "<span class='bg-danger d-block mb-n4'>" + k + "</span>" + '<br>'  # highlight it in red
                        item_count += 1
                    else:
                        if k != "": data[0] += "<span class='" + data_file.Resistors.get_colour(count) + " d-block mb-n4'>" + k + "</span>" + '<br>'  # otherwise give it its corresponding colour
                        else: data[0] += k + '<br>'  # or if it's empty just give it a break (ha ha, that was terrible I know)

                elif layout_item is data_file.Potentiometers.table:
                    ptype = flask.request.args['type']
                    if k == ptype + query or k == ptype + query + '0' or k == ptype + query.replace('K', '000R'):  # if item is the query but this time Jaycar's naming is dumb
                        data[0] += "<span class='bg-danger d-block mb-n4'>" + k + "</span>" + '<br>'
                        item_count += 1
                    else:
                        if k != "": data[0] += "<span class='" + data_file.Potentiometers.get_colour(count) + " d-block mb-n4'>" + k + "</span>" + '<br>'
                        else: data[0] += k + '<br>'

                elif layout_item is data_file.Capacitors.table:
                    ks = k.split('|')
                    if ks[0] == query and ks[1] != '' and ks[1] == flask.request.args['volts']:
                        data[0] += "<span class='bg-danger d-block mb-n4'>" + ks[0] + "</span>" + '<br>'
                        item_count += 1
                    else:
                        if k == 'nbsp': data[0] += '&nbsp;' * 8; count += 4
                        elif ks[0] != "": data[0] += "<span class='" + data_file.Capacitors.get_colour(count) + " d-block mb-n4'>" + ks[0] + "</span>" + '<br>'
                        else: data[0] += ks[0] + '<br>'

                elif layout_item is data_file.CapacitorsE.table:
                    ks = k.split('|')
                    if ks[0] == query and ks[1] != '' and ks[1] == flask.request.args['volts']:
                        data[0] += "<span class='bg-danger d-block mb-n4'>" + ks[0] + "</span>" + '<br>'
                        item_count += 1
                    else:
                        if k == 'nbsp': data[0] += '&nbsp;' * 8; count += 4
                        elif ks[0] != "": data[0] += "<span class='" + data_file.CapacitorsE.get_colour(count) + " d-block mb-n4'>" + ks[0] + "</span>" + '<br>'
                        else: data[0] += ks[0] + '<br>'

            data2.append(data)
        table_data.append(data2)

    message = ""
    message2 = ""

    if item_count == 0: stock_header = "We may not have this item in stock"
    else: stock_header = "Items that match this description are <span class='bg-danger'>highlighed in red</span>"

    if layout_item is data_file.Resistors.table:
        item_pricing = data_file.Resistors.pricing
        message = data_file.Resistors.message
    elif layout_item is data_file.Potentiometers.table:
        item_pricing = data_file.Potentiometers.pricing
        message = data_file.Potentiometers.message
    elif layout_item is data_file.CapacitorsE.table:
        item_pricing = data_file.CapacitorsE.pricing
        message = data_file.CapacitorsE.message
    elif layout_item is data_file.Capacitors.table:
        item_pricing = data_file.Capacitors.pricing
        message = data_file.Capacitors.message
        message2 = data_file.Capacitors.message2
    # There is no else SO it errors if layout_item is not above, because if it's made it this far then somethings clearly wrong

    return flask.render_template("table.html", table_data=table_data, header=stock_header, message=message, message2=message2, pricing=item_pricing)


if __name__ == '__main__':
    app.run()
