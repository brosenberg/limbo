"""!roll [diceroll] returns the result of a given dice roll"""

import random
import re

USAGE = """```Usage: !roll [diceroll]
ex: !roll 3d6
    !roll 2d4-2
    !roll 10d4+10```"""

def roll(input_dice):
    r = re.match('^([0-9]+)\s*d\s*([0-9]+)\s*([-+\/*x])?\s*([0-9]+)?\s*$', input_dice)
    result = 0
    rolls = []
    try:
        dice     = int(r.group(1))
        sides    = int(r.group(2))
    except AttributeError:
        return "Unknown dice input: %s\n%s" % (input_dice, USAGE)
    try:
        mod_type = r.group(3)
        mod      = int(r.group(4))
    except AttributeError:
        mod_type = ""
        mod = ""
    except TypeError:
        mod_type = ""
        mod = ""
    old_dice = dice

    while dice > 0:
        roll = random.randint(1, sides)
        rolls.append(roll)
        result += roll
        dice -= 1

    if mod_type == '+':
        result += mod
    if mod_type == '*' or mod_type == 'x':
        result *= mod
    if mod_type == '/':
        result /= mod

    result = "%dd%d%s%s: (%s)%s%s = %d" % (old_dice, sides, mod_type, mod, '+'.join(str(x) for x in rolls), mod_type, mod, result)

    return result


def on_message(msg, server):
    text = msg.get("text", "")

    r = re.match('!roll (.*?)$', text)
    try:
        return roll(r.group(1))
    except AttributeError:
        return
