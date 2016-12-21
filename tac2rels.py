import json
from os import listdir
from sys import stderr
from collections import Counter


relations={}

with open("rel2etyps.txt") as f:
    for line in f:
        fields=line.split("\t")
        #print(fields)
        rel=fields[0]
        etyp1=fields[1].split()
        etyp2=fields[2].split()
        relations[rel]=[etyp1,etyp2]


patterns={}

with open ("patterns.txt") as f:
    for line in f:
        fields=line.split()
        if line[0]!="#" and len(fields) > 3:
            relation=fields[0]
            if relation in relations:
                pdict=patterns
                for w in fields[1:]:
                    if w in ["$ARG1","$ARG2"]:
                        typ="ent"
                    else:
                        typ="txt"
                    subdict=pdict.get(typ,{})
                    pdict[typ]=subdict
                    subsubdict=subdict.get(w,{})
                    subdict[w]=subsubdict
                    pdict=subsubdict
                pdict["rel"]=relation

#print(patterns)
                


basedir="../"
querydata="LDC2016E39_TAC_KBP_English_Cold_Start_Comprehensive_Evaluation_Data_Sets_2012-2015/data/2015/eval/cold_start/"
#querydata=""
corpus="LDC2016E39_TAC_KBP_English_Cold_Start_Comprehensive_Evaluation_Data_Sets_2012-2015/data/2015/eval/source_documents/"

ldir=corpus

#etyps=Counter()
#ents={}

def next(current,typ,token,etyp):
    global patterns
    new=[]
    current.append((patterns,"_","","_","",""))
    for pdict,ent1,etyp1,ent2,etyp2,string in current:
        if typ in pdict:
            if typ=="ent":
                if "$ARG1" in pdict[typ]:
                    ent1=token
                    etyp1=etyp
                    string=string+" "+ent1
                    new.append((pdict[typ]["$ARG1"],ent1,etyp1,ent2,etyp2,string))
                    if "rel" in pdict[typ]["$ARG1"] and relations[rel]==(etyp1,etyp2):
                        print(pdict[typ]["$ARG1"]["rel"],ent1,ent2,string)
                if "$ARG2" in pdict[typ]:
                    ent2=token
                    etyp2=etyp
                    string=string+" "+ent2
                    new.append((pdict[typ]["$ARG2"],ent1,etyp1,ent2,etyp2,string))
                    if "rel" in pdict[typ]["$ARG2"] and etyp1 in relations[rel][0] and etyp2 in relations[rel][1]:
                        print(pdict[typ]["$ARG2"]["rel"],ent1,ent2,string)
            elif token in pdict[typ]:
                string=string+" "+token
                new.append((pdict[typ][token],ent1,etyp1,ent2,etyp2,string))
                if "rel" in pdict[typ][token] and relations[rel]==(etyp1,etyp2):
                    print(pdict[typ][token]["rel"],ent1,ent2,string)
            elif "*" in pdict[typ]:
                string=string+" "+token
                newdict={"txt":{"*":pdict[typ]["*"]}}
                new.append((newdict,ent1,etyp1,ent2,etyp2,string))
                if "rel" in pdict[typ]["*"] and relations[rel]==(etyp1,etyp2):
                    print(pdict[typ]["*"]["rel"],ent1,ent2,string)
    return new

for source in ["mpdf_TurboParser/","nw_TurboParser/"]:
    for fname in listdir(basedir+ldir+source):#[:2000]:
        if fname.endswith(".xml"):
            #stderr.write(basedir+ldir+source+fname+"\n")
            with open(basedir+ldir+source+fname) as f:
                current=[]
                eflag=False
                ent=""
                for line in f:
                    fields=line.split("\t")
                    if len(fields) >= 10 and line[0] != "<" and fields[0]!="":
                        start=  int(fields[0])
                        end=    int(fields[1])
                        if end >= start:
                            token=      fields[3].lower()
                            lemma=      fields[4]
                            postag=     fields[5]
                            netag=      fields[6]
                            coref=      fields[7]
                            head=   int(fields[8])
                            dep=        fields[9]
                            if netag[0]=="B":
                                eflag=True
                                ent=token
                                etyp=netag
                                #etyps[etyp]+=1
                            elif netag[0]=="I":
                                eflag=True
                                ent=ent+" "+token
                            else:
                                if eflag:
                                    current=next(current,"ent",ent,etyp)
                                    #ents[etyp]=ents.get(etyp,Counter())
                                    #ents[etyp][ent]+=1
                                    eflag=False
                                    ent=""
                                    etyp=""
                                current=next(current,"txt",token,"")
                    else:
                        current=[]
                        eflag=False
                        ent=""
                        etyp=""
                            

#for etyp,c in etyps.most_common():
#    print(etyp,c)
#    for ent,c2 in ents[etyp].most_common()[:10]:
#        print("",ent,c2)




