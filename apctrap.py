print("Import...")

from pysnmp.carrier.asyncore.dispatch import AsyncoreDispatcher
from pysnmp.carrier.asyncore.dgram import udp, udp6, unix
from pyasn1.codec.ber import decoder
from pysnmp.proto import api
from pysnmp.smi import builder, view
from pysnmp.smi.rfc1902 import ObjectType, ObjectIdentity
import os, logging
from logging.handlers import RotatingFileHandler
import netifaces as ni

print("Setup...")

TRAP_IP_ADDRESS=ni.ifaddresses('eth0')[2][0]['addr']
#TRAP_IP_ADDRESS=ni.ifaddresses('en0')[2][0]['addr']
TRAP_PORT=162
TEN_MEGABYTES=10485760
#LOG_FILE="./ups.log"
LOG_FILE="/var/log/ups.log"

COMPILED_MIB_PATH=os.path.join(os.getcwd(), "CompiledMIBs")
MIB_MODULES=('SNMPv2-MIB', 'SNMP-COMMUNITY-MIB', 'PowerNet-MIB', 'UPS-MIB')


LOGGING_FORMAT="%(asctime)s %(levelname)s - %(message)s"
loggingHandler=RotatingFileHandler(LOG_FILE, maxBytes=TEN_MEGABYTES, backupCount=5)
logging.basicConfig(format=LOGGING_FORMAT, handlers=(loggingHandler,))
logging.getLogger('apctrap').setLevel(logging.INFO)

mibBuilder=builder.MibBuilder()
mibSources=mibBuilder.getMibSources()+(builder.DirMibSource(COMPILED_MIB_PATH),)
mibBuilder.setMibSources(*mibSources)
mibBuilder.loadModules(*MIB_MODULES)
viewController=view.MibViewController(mibBuilder)

def secsToTime(s):
    d=s/86400
    s-=(86400*d)
    h=s/3600
    s-=(h*3600)
    m=s/60
    s-=(60*m)
    return d,h,m,s

def snmpRecvCallback(dispatcher, domain, address, msg):
    logger=logging.getLogger("apctrap")
    while msg:
        version=int(api.decodeMessageVersion(msg))
        if version in api.protoModules: module=api.protoModules[version]
        else:
            logger.error("Unsupported SNMP version {0}".format(version))
            return

        req,msg=decoder.decode(msg, asn1Spec=module.Message())
        logger.info("Notification from {0}:{1}".format(domain, address))

        pdu=module.apiMessage.getPDU(req)
        if not pdu.isSameTypeWith(module.TrapPDU()): continue

        if version==api.protoVersion1:
            varBinds=module.apiTrapPDU.getVarBindList(pdu)
        else: varBinds=module.apiPDU.getVarBindList(pdu)

        for v,b in varBinds:
            key='.'.join([str(i) for i in v._value])
            value=b.getComponent('simple')._value

            print(viewController.getNodeName(v._value))
            parsed=ObjectType(ObjectIdentity(key), value)
            try: parsed.resolveWithMib(viewController)
            except Exception as e: 
                print("Failed to resolve symbol: {}={} ({})", key, value,e)
                continue
            print(parsed[0].getMibSymbol(), end="")
            try: print(parsed[1]._value)
            except AttributeError: print(parsed[1].getMibSymbol())

    return msg

dispatcher=AsyncoreDispatcher()
dispatcher.registerRecvCbFun(snmpRecvCallback)
dispatcher.registerTransport(
    udp.domainName, udp.UdpSocketTransport().openServerMode((TRAP_IP_ADDRESS, TRAP_PORT))
)
dispatcher.jobStarted(1)
print("Starting...")
try: dispatcher.runDispatcher()
except:
    dispatcher.closeDispatcher()
    raise
