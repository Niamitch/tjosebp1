# -*- coding: utf-8 -*-
import re

def get_ingredient(line):
    pattern = re.compile("((?:1 oz à 2 oz|\(|\)|\d à \d|\d/\d|\d+,?\d*|(?:Q|q)uelques|une?|Une ?|quinzaine|au goût|à volonté| ?demi)*(?: (?:petite)? ?tasses?| cuillères? à (?:soupe|café)| lb| ml| mL| g(?: |\))| c. à (?:soupe|thé)| oz| c. à (?:s|c).| c. à .s| cl| kg| Kg| c.à.(?:c|s)| pincée| pintes?| enveloppes?| (?:B|b)ouquet| gallons?| ?(?:F|f)euilles?| tranches| tronçons| verres?| (?:R|r)ondelles?| gousses?| morceau| botte| boîtes?(?: de conserve)?|. à soupe)?)? ?(?:de |d'|d’|du)?([ \w%'’]*)")
    match = re.match(pattern,line)
    return ('QUANTITE :'+match.group(1),'INGREDIENT :'+match.group(2))


def main():
    with open("./resources/ingredients.txt") as f:
        for line in f:
            tuple = get_ingredient(line)
            print(tuple)

if __name__ == "__main__":
   main()