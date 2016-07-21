from pysnmp.carrier.asyncore.dispatch import AsyncoreDispatcher
from pysnmp.carrier.asyncore.dgram import udp, udp6, unix
from pyasn1.codec.ber import decoder
from pysnmp.proto import api
from pysnmp.smi import builder, view, rfc1902
import os, logging
from logging.handlers import RotatingFileHandler
import netifaces as ni

#TRAP_IP_ADDRESS=ni.ifaddresses('eth0')[2][0]['addr']
TRAP_IP_ADDRESS=ni.ifaddresses('en0')[2][0]['addr']
TRAP_PORT=162
TEN_MEGABYTES=10485760
LOG_FILE="./ups.log" #"/var/log/ups.log"

LOGGING_FORMAT="%{asctime}s %{levelname} %{message}s"
loggingHandler=RotatingFileHandler(LOG_FILE, maxBytes=TEN_MEGABYTES, backupCount=5)
logging.basicConfig(format=LOGGING_FORMAT, handlers=(loggingHandler,))

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
            logger.error("Unsupported SNMP version {}".format(version))
            return

        req,msg=decoder.decode(msg, asn1Spec=module.Message())
        logger.info("Notification message from {}:{}".format(domain, address))

        pdu=module.apiMessage.getPDU(req)
        if not pdu.isSameTypeWith(module.TrapPDU()): continue

        if version==api.protoVersion1:
            print(module,req)

        else: pass
    return msg

dispatcher=AsyncoreDispatcher()
dispatcher.registerRecvCbFun(snmpRecvCallback)
dispatcher.registerTransport(
    udp.domainName, udp.UdpSocketTransport().openServerMode((TRAP_IP_ADDRESS, TRAP_PORT))
)
dispatcher.jobStarted(1)
try: dispatcher.runDispatcher()
except:
    dispatcher.closeDispatcher()
    raise