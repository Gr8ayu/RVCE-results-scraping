
# 1RV18IS009 > 1RV18 + IS + 009

def generateUSN(USNbegin):
    branches = ['IS','CV','AS','BT','CH','CS','EC','EE','EI','IM','ME','TE']
    branches = [USNbegin+x for x in branches]
    USN = {}
    for branch in branches:
        USN[branch]=[]
        for i in range(1,210):
            if i in range(10):
                USN[branch].append(branch + "00" + str(i))
            elif i in range(10,100):
                USN[branch].append( branch + "0" + str(i))
            else:
                USN[branch].append( branch + str(i))
    # with open("USNlist"+USNbegin+".txt","w") as file:
    #     for branch,item in USN.items():
    #         file.write("\n".join(item))
    #         file.write("\n")

    #for key in USN.keys():
        # print("generated", len(USN[key]),"keys for", key)

    return USN
