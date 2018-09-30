# -*- coding: utf-8 -*-
import re

def get_ingredient(line):
    pattern = re.compile(r"((?:1 oz à 2 oz| ?g(?: |\))|\((?=\d|à|a)|\)|\d à \d|\d/\d|\d+,?\d*|(?:Q|q)uelques|une?|Une ?|quinzaine|au goût|à volonté| ?demi)*(?: (?:petite)? ?tasses?\)?| cuillères? à (?:soupe|café)| lb\)?| ml\)?| mL| c. à (?:soupe|thé)\)?| oz\)?| c. à (?:s|c).| c. à .s| cl| kg| Kg| c.à.(?:c|s)| pincée| pintes?| enveloppes?| (?:B|b)ouquet| gallons?| ?(?:F|f)euilles?| tranches| tronçons| verres?| (?:R|r)ondelles?| gousses?| morceau| botte| noix| boîtes?(?: de conserve)?|. à soupe)?)? ?(?:de |d'|d’|du)?([ \w%'’]+)")
    matches = re.findall(pattern,line)
    quantity = ''
    ingredient = ''

    for match in matches:
        quantity += match[0]+' '
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