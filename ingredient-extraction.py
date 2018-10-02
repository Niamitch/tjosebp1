# -*- coding: utf-8 -*-
import re

def get_ingredient(line):
    pattern = re.compile(r"((?:1 oz à 2 oz|\((?=\d|à|a)|\)| ?½| ?¾| ?¼|\d à \d|\d/\d|\d+,?\d*|(?:Q|q)uelques|une?|Une ?|quinzaine|au goût|à volonté| ?demi)*(?: (?:petite)? ?tasses?\)?|trait| sommités| cuillères? à (?:soupe|café)| lb\)?| ml\)?| mL| ?g(?:\b|\))| c. à (?:soupe|thé)\)?| oz\)?| c. à (?:s|c).| c. à .s| cl| kg| Kg| c.à.(?:c|s)| pincée| pintes?| enveloppes?| (?:B|b)ouquet| gallons?| ?(?:F|f)euilles?| tranches| tronçons| verres?| (?:R|r)ondelles?| gousses?| lamelles?| morceau| botte| noix| boîtes?(?: de conserve)?|. à soupe| à volonté)?)? ?(?:des? |d'|d’|du|à)?([ \w%'’]+)(?:,[ \w%'’/\(¼\)éç]+)?")
    matches = re.findall(pattern,line)
    quantity = ''
    ingredient = ''

    for match in matches:
        if(match[0] != ' '):
            quantity += match[0]+' '
        if (match[1] != ' '):
            ingredient += match[1]+' '
    quantity = quantity[:-1]
    ingredient = ingredient[:-1]
    return (quantity,ingredient)


def main():
    with open("./resources/ingredients.txt") as f:
        for line in f:
            tuple = get_ingredient(line.rstrip())
            print(tuple)

if __name__ == "__main__":
   main()