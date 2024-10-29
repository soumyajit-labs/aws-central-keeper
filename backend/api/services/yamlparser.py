import re
from . import translate

def fmtr(s):
    try:
        f1 = s.replace('\\n','\n')
        f2 = f1.replace('\\"![','"![')
        f3 = f2.replace(']\\"',']"')
        return f3
    except:
        return s

def parser(text, ops, key):
    splt = fmtr(text).split('\n')
    accumulator = []
    response = {}
    for item in splt:
        k = item.split(":")[0]
        v = item.split(":")[1]
        if ((v).strip() != ''):
            if ops == 'encrypt':
                unpadded = re.search('"(.*)"', (v).strip())
            else:
                unpadded = re.search('"!\[(.*)\]"', (v).strip())
            result = translate.translate(key=key, operation=ops, text=unpadded.group(1))
            accumulator.append(k + ': \"' + result + '\"')
        else:
            accumulator.append(k + ':')
    response['value'] = '\n'.join(accumulator)
    return (response)