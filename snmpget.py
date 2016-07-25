from time import sleep
from datetime import datetime
from pysnmp.entity.rfc3413.oneliner import cmdgen

commands=(
    # Identity
    ('upsBasicIdentModel',0),
    ('upsBasicOutputStatus',0),

    # Battery
    ('upsBasicBatteryStatus',0),           # str
    ('upsBasicBatteryTimeOnBattery',0),    # x10-2 (1/100) seconds
    ('upsHighPrecBatteryCapacity',0),      # % *10
    ('upsHighPrecBatteryTemperature',0),   # °C *10
    ('upsAdvBatteryRunTimeRemaining',0),   # x10-2 (1/100) seconds 
    ('upsHighPrecBatteryActualVoltage',0), # V *10

    # Input Voltage
    #('upsBasicInputPhase',0),             # 
    ('upsHighPrecInputLineVoltage',0),    # V *10
    ('upsHighPrecInputMaxLineVoltage',0), # V *10
    ('upsHighPrecInputMinLineVoltage',0), # V *10
    ('upsHighPrecInputFrequency',0),      # Hz *10
    ('upsAdvInputLineFailCause',0),       #

    # Output Voltage
    ('upsBasicOutputStatus',0),         #
    #('upsBasicOutputPhase',0),          # 
    ('upsHighPrecOutputVoltage',0),     # V *10
    ('upsHighPrecOutputFrequency',0),   # Hz *10
    ('upsHighPrecOutputLoad',0),        # % *10
    ('upsHighPrecOutputCurrent',0),     # A *10
    ('upsHighPrecOutputEfficiency',0),  # % *10
    ('upsHighPrecOutputEnergyUsage',0), # kWh *10
)

<<<<<<< HEAD
keys={
    "PowerNet-MIB::upsBasicIdentModel.0":"upsModel",
    "PowerNet-MIB::upsBasicOutputStatus.0":"upsStatus",
    "PowerNet-MIB::upsBasicBatteryStatus.0":"batteryStatus",
    "PowerNet-MIB::upsBasicBatteryTimeOnBattery.0":"batteryTime",
    "PowerNet-MIB::upsHighPrecBatteryCapacity.0":"batteryCapacity",
    "PowerNet-MIB::upsHighPrecBatteryTemperature.0":"batteryTemperature",
    "PowerNet-MIB::upsAdvBatteryRunTimeRemaining.0":"batteryTimeRemaining",
    "PowerNet-MIB::upsHighPrecBatteryActualVoltage.0":"batteryVoltage",
    #"PowerNet-MIB::upsBasicInputPhase.0":"",
    "PowerNet-MIB::upsHighPrecInputLineVoltage.0":"inputVoltage",
    "PowerNet-MIB::upsHighPrecInputMaxLineVoltage.0":"inputVoltageMax",
    "PowerNet-MIB::upsHighPrecInputMinLineVoltage.0":"inputVoltageMin",
    "PowerNet-MIB::upsHighPrecInputFrequency.0":"inputFrequency",
    "PowerNet-MIB::upsAdvInputLineFailCause.0":"inputFailCause",
    "PowerNet-MIB::upsBasicOutputStatus.0":"outputStatus",
    #"PowerNet-MIB::upsBasicOutputPhase.0":"",
    "PowerNet-MIB::upsHighPrecOutputVoltage.0":"outputVoltage",
    "PowerNet-MIB::upsHighPrecOutputFrequency.0":"outputFrequency",
    "PowerNet-MIB::upsHighPrecOutputLoad.0":"outputLoad",
    "PowerNet-MIB::upsHighPrecOutputCurrent.0":"outputCurrent",
    "PowerNet-MIB::upsHighPrecOutputEfficiency.0":"outputEfficiency",
    "PowerNet-MIB::upsHighPrecOutputEnergyUsage.0":"outputEnergyUsage",

    "SNMPv2-SMI::enterprises.318.1.1.1.1.1.1.0":"upsModel",
    "SNMPv2-SMI::enterprises.318.1.1.1.4.1.1.0":"upsStatus",
    "SNMPv2-SMI::enterprises.318.1.1.1.2.1.1.0":"batteryStatus",
    "SNMPv2-SMI::enterprises.318.1.1.1.2.1.2.0":"batteryTime",
    "SNMPv2-SMI::enterprises.318.1.1.1.2.3.1.0":"batteryCapacity",
    "SNMPv2-SMI::enterprises.318.1.1.1.2.3.2.0":"batteryTemperature",
    "SNMPv2-SMI::enterprises.318.1.1.1.2.2.3.0":"batteryTimeRemaining",
    "SNMPv2-SMI::enterprises.318.1.1.1.2.3.4.0":"batteryVoltage",
    #"SNMPv2-SMI::enterprises.318.1.1.1.3.1.1.0":"",
    "SNMPv2-SMI::enterprises.318.1.1.1.3.3.1.0":"inputVoltage",
    "SNMPv2-SMI::enterprises.318.1.1.1.3.3.2.0":"inputVoltageMax",
    "SNMPv2-SMI::enterprises.318.1.1.1.3.3.3.0":"inputVoltageMin",
    "SNMPv2-SMI::enterprises.318.1.1.1.3.3.4.0":"inputFrequency",
    "SNMPv2-SMI::enterprises.318.1.1.1.3.2.5.0":"inputFailCause",
    "SNMPv2-SMI::enterprises.318.1.1.1.4.1.1.0":"outputStatus",
    #"SNMPv2-SMI::enterprises.318.1.1.1.4.1.2.0":"",
    "SNMPv2-SMI::enterprises.318.1.1.1.4.3.1.0":"outputVoltage",
    "SNMPv2-SMI::enterprises.318.1.1.1.4.3.2.0":"outputFrequency",
    "SNMPv2-SMI::enterprises.318.1.1.1.4.3.3.0":"outputLoad",
    "SNMPv2-SMI::enterprises.318.1.1.1.4.3.4.0":"outputCurrent",
    "SNMPv2-SMI::enterprises.318.1.1.1.4.3.5.0":"outputEfficiency",
    "SNMPv2-SMI::enterprises.318.1.1.1.4.3.6.0":"outputEnergyUsage",
}

def strTime(s):
    def timeTickToTime(s):
        s//=100
        d=s//86400
        s-=(86400*d)
        h=s//3600
        s-=(h*3600)
        m=s//60
        s-=(60*m)
        return d,h,m,s
    _,_,m,s=timeTickToTime(int(s))
    return "{:02d}:{:02d}".format(m,s)


cmdLookup=dict(
    upsModel=lambda x: str(x),
    upsStatus=lambda x: str(x),
    batteryStatus=lambda x: str(x),
    batteryTime=lambda x: int(x),
    batteryCapacity=lambda x: float(x)/10.,
    batteryTemperature=lambda x: float(x)/10.,
    batteryTimeRemaining=strTime,
    batteryVoltage=lambda x: float(x)/10.,
    inputVoltage=lambda x: float(x)/10.,
    inputVoltageMax=lambda x: float(x)/10.,
    inputVoltageMin=lambda x: float(x)/10.,
    inputFrequency=lambda x: float(x)/10.,
    inputFailCause=lambda x: str(x),
    outputStatus=lambda x: str(x),
    outputVoltage=lambda x: float(x)/10.,
    outputFrequency=lambda x: float(x)/10.,
    outputLoad=lambda x: float(x)/10.,
    outputCurrent=lambda x: float(x)/10.,
    outputEfficiency=lambda x: float(x)/10.,
    outputEnergyUsage=lambda x: float(x)/100.,
)

print("{}: Create MIB Variables...".format(str(datetime.now())))

mibVariables=[]
for cmd in commands:
    mibVariables.append(
        cmdgen.MibVariable('PowerNet-MIB',*cmd).addMibSource('/home/pi/APC-SNMP/CompiledMIBs')
    )

def heartbeat():
    print("{}: Heartbeating...?".format(str(datetime.now())))
    cmdGen=cmdgen.CommandGenerator()
    indication,status,index,varBinds=cmdGen.getCmd(
        cmdgen.CommunityData('public', mpModel=0),
        cmdgen.UdpTransportTarget(('134.36.67.93',161)),
        *mibVariables
    )

    print("{}: Parsed:".format(str(datetime.now())))
    if indication: print(indication)
    else:
        if status:
            print("{} at {}".format(
                status.prettyPrint(),
                index and varBinds[int(errorIndex)-1] or '?'
            ))
        else:
            for name,val in varBinds:
                #print("{} = {}".format(name.prettyPrint(), val.prettyPrint()))
                name,val=name.prettyPrint(),val.prettyPrint()
                try: name=keys[name]
                except KeyError as e:
                    print("ERROR:",e)
                    continue
                val=cmdLookup[name](val)
                print(name,val,(type(name),type(val)))

print("{}: Starting...".format(str(datetime.now())))
while 1:
    try:
        heartbeat()
        sleep(30)
    except KeyboardInterrupt: break
