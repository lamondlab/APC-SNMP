from pysnmp.smi import builder, view, rfc1902
import os

mb=builder.MibBuilder()
mibSrcs=mb.getMibSources()+(builder.DirMibSource(os.path.join(os.getcwd(), "CompiledMIBs")),)
mb.setMibSources(*mibSrcs)
print(mibSrcs)
mb.loadModules('SNMPv2-MIB', 'SNMP-COMMUNITY-MIB', 'PowerNet-MIB', 'UPS-MIB')
vc=view.MibViewController(mb)

varBinds=[
    ('1.3.6.1.2.1.1.3.0',9041620),
    ('1.3.6.1.6.3.1.1.4.1.0','1.3.6.1.4.1.318.0.636'),
    ('1.3.6.1.4.1.318.2.3.3.0',b'UPS: On battery power in response to distorted input.'),
    ('1.3.6.1.2.1.33.1.2.3.0' ,20),
    ('1.3.6.1.2.1.33.1.2.2.0', 0),
    ('1.3.6.1.2.1.33.1.9.7.0', 2),

]

for k,v in varBinds:
    q=tuple(int(kk) for kk in k.split('.'))
    print(k,q)
    try:print(vc.getNodeName(q))
    except: print("Fail 1!")
    try: 
        vb=rfc1902.ObjectType(rfc1902.ObjectIdentity(k), v).resolveWithMib(vc)
        print(vb.prettyPrint())
    except: print("Fail 2!")
