import pyparsing as pp
import sys
import re

def normalize_vietnamese_numbers(input_string):
    # Remove Vietnamse dot thousands separator
    result = input_string
    while True:
        s = re.sub(r"(\d+)\.(\d+)", r"\1\2", result)
        if s == result:
            break
        result = s

    # Replace floating point commas with temporary text
    result = re.sub(r"(\d+),(\d+)", r"\1.\2", result)

    return result


def normalize_three_dots(input_string, token_3_dots="..."):
    result = input_string.replace("…", "...")
    result = re.sub(r"\.[\. ]*\.+", token_3_dots, result)
    return result


def get_option_content(option, lower=False):
    option = option[2:].strip()
    return option.lower() if lower else option

def get_grammar():
    # Define the grammar for the expression
    """
        program::= (text + expression + equation)*
        text::= <string of characters and not numbers>
        expression::= literal_list | literal (op literal)*
        equation::= expression (BLANK | compare_op) expression
        literal::= (integer | float ) unit? | time | mixed_number | cloze
        literal_list::= literal (SEMI literal)*
        compare_op::= "=" | "<" | ">"
        op::= "+" | "-" | mul_op | div_op
        mul_op::= "x" | "\\times" | $\\times$
        div_op::= ":" | "\\div" | $\\div$
        unit::= weight | money | time | measure
        weight::= "kg" | "g" | "mg" | "t" | "lb" | "oz"
        SEMI::= ";"
        BLANK::= ("…" + ('.'+))+
    """
    ############################################
    #                                          #
    #                LEXICAL RULES             #
    #                                          #
    ############################################ 
    ############################################
    #                   Units                  #
    ############################################ 
    ton = pp.Literal('tấn').setParseAction(lambda t: 'ton')
    ta = pp.Literal('tạ').setParseAction(lambda t: 'quintal')
    kilogam = (pp.Literal('kg') | pp.Literal('ki lô gam') | pp.Literal('ki-lô-gam')).setParseAction(lambda t: 'kg')
    gam = (pp.Literal('g') | pp.Literal('gam')).setParseAction(lambda t: 'g')
    yen = pp.Literal('yến').setParseAction(lambda t: 'yen')
    weight_unit = kilogam | gam | ton | ta | yen
<<<<<<< HEAD
<<<<<<< HEAD

    money_unit = pp.Literal('đ') | pp.Literal('đồng') # careful with this one
=======
    money_unit = pp.Literal('đ') | pp.Literal('đồng')
>>>>>>> 89333f4d9d28df144e9976956821627747715b30
=======
    money_unit = pp.Literal('đ') | pp.Literal('đồng')
>>>>>>> 89333f4d9d28df144e9976956821627747715b30

    hour = pp.Literal('giờ').setParseAction(lambda t: 'hour')
    minute = pp.Literal('phút').setParseAction(lambda t: 'minute')
    second = pp.Literal('giây').setParseAction(lambda t: 'second')
    day = pp.Literal('ngày').setParseAction(lambda t: 'day')
    time_unit = hour | minute | second | day

    km = pp.oneOf(['kilômét', 'km', 'ki-lô-mét', 'ki lô mét']).setParseAction(lambda t: 'km')
    hm = pp.oneOf(['hectômét', 'hm', 'héc-tô-mét', 'héc tô mét']).setParseAction(lambda t: 'hm')
    dam = pp.oneOf(['dam', 'đề ca mét', 'đề-ca-mét']).setParseAction(lambda t: 'dam')
    m = (pp.Literal('mét') | pp.Literal('m')).setParseAction(lambda t: 'm')
    dm = pp.oneOf(['decimet', 'dm', 'đề xi mét', 'đề-xi-mét']).setParseAction(lambda t: 'dm')
    cm = pp.oneOf(['centimet', 'cm', 'xăng-ti-mét', 'xăng ti mét']).setParseAction(lambda t: 'cm')
    mm = pp.oneOf(['milimet', 'mm', 'mi-li-mét', 'mi li mét']).setParseAction(lambda t: 'mm')
    km2 = pp.oneOf(['kilômét vuông', 'km2', 'ki-lô-mét vuông', 'ki lô mét vuông', 'km^2', 'km^{2}']).setParseAction(lambda t: 'km2')
    hm2 = pp.oneOf(['ha', 'héc-ta', 'héc ta', 'héc-tô-mét vuông', 'héc tô mét vuông', 'hm^2', 'hm^{2}', 'hm2']).setParseAction(lambda t: 'hm2')
    dam2 = pp.oneOf(['dam2', 'đề ca mét vuông', 'đề-ca-mét vuông', 'dam^2', 'dam^{2}']).setParseAction(lambda t: 'dam2')
    m2 = pp.oneOf(['mét vuông', 'm2', 'mét-vuông', 'm^2', 'm^{2}', 'm $2$']).setParseAction(lambda t: 'm2')
    dm2 = pp.oneOf(['dm2', 'đề xi mét vuông', 'đề-xi-mét vuông', 'dm^2', 'dm^{2}', 'dm $2$']).setParseAction(lambda t: 'dm2')
    cm2 = pp.oneOf(['xăng ti mét vuông', 'cm2', 'xăng-ti-mét vuông', 'cm^2', 'cm^{2}', 'cm $2$']).setParseAction(lambda t: 'cm2')
    mm2 = pp.oneOf(['mi-li-mét vuông', 'mm2', 'mi li mét vuông', 'mm^2', 'mm^{2}', 'mm $2$']).setParseAction(lambda t: 'mm2')
    km3 = pp.oneOf(['kilômét khối', 'km3', 'ki-lô-mét khối', 'ki lô mét khối']).setParseAction(lambda t: 'km3')
    m3 = pp.oneOf(['mét khối', 'm3', 'mét-khối', 'm^3', 'm^{3}', 'm $3$']).setParseAction(lambda t: 'm3')
    dm3 = pp.oneOf(['đề xi mét khối', 'đề-xi-mét khối', 'dm3', 'dm^3', 'dm^{3}', 'dm $3$', 'lít']).setParseAction(lambda t: 'dm3')
    cm3 = pp.oneOf(['xăng ti mét khối', 'xăng-ti-mét khối', 'cm3', 'cm^3', 'cm^{3}', 'cm $3$', 'ml']).setParseAction(lambda t: 'cm3')
    mm3 = pp.oneOf(['mi-li-mét khối', 'mi li mét khối', 'mm3', 'mm^3', 'mm^{3}', 'mm $3$']).setParseAction(lambda t: 'mm3')

    measure_unit = km3 | m3 | dm3 | cm3 | mm3 | km2 | hm2 | dam2 | m2 | dm2 | cm2 | mm2 | km | hm | dam | m | dm | cm | mm
    speed_unit = pp.oneOf("m km") + pp.Literal('/') + time_unit

    celsius = pp.oneOf(['độ C', 'độ-C', 'oC', '°C']).setParseAction(lambda t: 'oC')
    farhenheit = pp.oneOf(['độ F', 'độ-F', 'oF', '°F']).setParseAction(lambda t: 'oF')
    kelvin = pp.oneOf(['độ K', 'độ-K', 'oK', '°K']).setParseAction(lambda t: 'oK')
    temperature_unit = celsius | farhenheit | kelvin

<<<<<<< HEAD
<<<<<<< HEAD
    percent = pp.oneOf(['%', 'phần trăm']).setParseAction(lambda t: '0.01')

    unit = (time_unit | weight_unit  | speed_unit | measure_unit  | temperature_unit | percent).setParseAction(lambda t: ['*', *t])
=======
    unit = (time_unit | weight_unit | money_unit  | speed_unit | measure_unit  | temperature_unit).setParseAction(lambda t: ['*', *t])
>>>>>>> 89333f4d9d28df144e9976956821627747715b30
=======
    unit = (time_unit | weight_unit | money_unit  | speed_unit | measure_unit  | temperature_unit).setParseAction(lambda t: ['*', *t])
>>>>>>> 89333f4d9d28df144e9976956821627747715b30
    ############################################
    #         Extra symbols and variables      #
    ############################################ 
    constants = pp.oneOf(["\\pi", "π", "e"])

    ############################################
    #          Operators and delimiters        #
    ############################################ 
    compare_op = pp.oneOf("= < >").setParseAction(lambda t: '==' if t[0] == '=' else t[0])
    mul_op = pp.oneOf(["x", "\\times", "${\\times}$", "×"]).setParseAction(lambda t: '*')
    div_op = pp.oneOf([":", "\\div", "$\\div$", "/"]).setParseAction(lambda t: '/')
    add_op = pp.oneOf("- – ­").setParseAction(lambda t: '-') | pp.Literal("+")
    bin_op = add_op | mul_op | div_op
    left_par = pp.oneOf(["(", "\\left("]).setParseAction(lambda t: '(')
    right_par = pp.oneOf([")", "\\right)"]).setParseAction(lambda t: ')')

    ############################################
    #                                          #
    #                PARSER RULES              #
    #                                          #
    ############################################ 
    ############################################
    #                   Text                   #
    ############################################ 
    exclude_chars = pp.nums + '\\-('
    word = pp.Word(pp.pyparsing_unicode.printables, excludeChars=exclude_chars)
    texts = pp.OneOrMore(word + pp.Optional(pp.oneOf('- (') + word))
    cloze = pp.Word(pp.nums + "*")

    ############################################
    #                    Data                  #
    ############################################ 
    integer = pp.Combine(pp.Optional(pp.Literal('-')) + pp.Word(pp.nums + ' ')).setParseAction(lambda t: t[0].replace(' ', ''))
    float_number = pp.Combine(integer + "." + integer)
<<<<<<< HEAD
<<<<<<< HEAD
    fraction = (pp.Suppress("\\frac{") + integer + pp.Suppress("}{") + integer + pp.Suppress("}")).setParseAction(lambda t: '(' + t[0] + '/' + t[1] + ')' )
=======
    fraction = (pp.Suppress("\\frac{") + integer + pp.Suppress("}{") + integer + pp.Suppress("}")).setParseAction(lambda t: t[0] + '/' + t[1] )
>>>>>>> 89333f4d9d28df144e9976956821627747715b30
=======
    fraction = (pp.Suppress("\\frac{") + integer + pp.Suppress("}{") + integer + pp.Suppress("}")).setParseAction(lambda t: t[0] + '/' + t[1] )
>>>>>>> 89333f4d9d28df144e9976956821627747715b30
    mixed_fraction = (integer + fraction).setParseAction(lambda t: '( ' + t[0] + ' + ' + t[1] + ' )')
    sqrt_number = (pp.oneOf(["\\sqrt", "√"]) + integer | pp.Literal("\\sqrt{") + integer + pp.Literal("}")).setParseAction(lambda t: 'math.sqrt(' + t[1] + ')')
    time = pp.Combine(integer + ":" + integer)
    number = (float_number | integer)("literal")
    def get_mixed_unit(t):
        return ['(', *t[:3], '+', *t[3:], ')']
    mixed_unit = (number + unit("unit") + number + unit("unit")).setParseAction(get_mixed_unit) # double unit
    literal = mixed_unit | mixed_fraction | fraction | number + pp.Optional(unit)("unit") | time  | cloze | constants | sqrt_number
    literal_list = pp.delimitedList(literal, delim=";")

    ############################################
    #                  Expression              #
    ############################################ 
    expression, expression_1 = pp.Forward(), pp.Forward()
    power_expr = pp.Literal("^").setParseAction(lambda t: "**") + (pp.Suppress("{") + integer + pp.Suppress("}") | integer)
    expression_1 << (literal_list | literal   | left_par + expression + right_par) + pp.Optional(power_expr)
    expression << (expression_1 + bin_op + expression | expression_1)
    blank_op = pp.OneOrMore(pp.oneOf(["…", ".", " ", ",", "?"])).setParseAction(lambda t: '...')("blank")
    equation = expression + (compare_op + blank_op | blank_op | compare_op ) + pp.Optional(expression | unit("unit"))

    ############################################
    #                   Program                #
    ############################################
    def markType(marker):
        global types, locs
        def parse_action_impl(l, t):
            types.append(marker)
            locs.append(l)
            return t
        return parse_action_impl
    
    program = pp.ZeroOrMore(  \
        pp.Group(equation).setParseAction(markType("Equation")) | 
        pp.Group(expression).setParseAction(markType("Expression"))  |  
        pp.Group(texts).setParseAction(markType("Text")) 
    )
    return program 

def get_var_dict():
    return {
        "mm": 1, "cm": 10, "dm": 100, "m": 1000, "dam": 1e4, "hm": 1e5, "km": 1e6,
        "second": 1, "minute": 60, "hour": 3600, "day": 86400, 
        "g": 1, "kg": 1000, "ton": 1e6, "quintal": 1e5, "yen": 1e4,
        "mm3": 1, "cm3": 1e3, "dm3": 1e6, "m3": 1e9, "km3": 1e18, "dam3": 1e12, "hm3": 1e15,
        "mm2": 1, "cm2": 1e2, "dm2": 1e4, "m2": 1e6, "km2": 1e12, "dam2": 1e8, "hm2": 1e10,
    }

def get_number_grammar(  ):
    """ Special cases:
    "Hai mươi lăm", "Mười một", "Một trăm linh năm", "Ba mươi tư", "Bốn mươi tư", "Bốn trăm"
    """
    head_rule = pp.oneOf(["một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín", "mười"])
    tail_rule = pp.oneOf([])

def parse_expression(text, grammar):
    global types, locs
    types, locs = [], []
    # Parse the text
    result = grammar.parseString(text)
    # process locs
    locs.append(len(text))
    for i in range(len(locs) - 1):
        locs[i] = (locs[i], locs[i+1])
    locs.pop() # remove the last element
    return result, types, locs
