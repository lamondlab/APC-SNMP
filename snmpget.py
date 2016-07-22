from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen=cmdgen.CommandGenerator()

#c1=cmdgen.MibVariable('PowerNet-MIB','upsBasicIdentModel',0).addMibSource('/home/pi/APC-SNMP/CompiledMIBs')
#c2=cmdgen.MibVariable('PowerNet-MIB','upsBasicOutputStatus',0).addMibSource('/home/pi/APC-SNMP/CompiledMIBs')

commands=(
    # Identity
    ('upsBasicIdentModel',0),
    ('upsBasicOutputStatus',0),

    # Battery
    ('upsBasicBatteryStatus',0),         # str
    ('upsAdvBatteryCapacity',0),         # str
    ('upsAdvBatteryTemperature',0),      # °C
    ('upsAdvBatteryRunTimeRemaining',0), # x10-2 (1/100) seconds 

    # Input Voltage
    ('upsBasicInputPhase',0),
    ('upsAdvInputLineVoltage',0),
    ('upsAdvInputMaxLineVoltage',0),
    ('upsAdvInputMinLineVoltage',0),
    ('upsAdvInputFrequency',0),
    ('upsAdvLineFailCaus',0),

    # Output Voltage
    ('upsBasicOutputStatus',0),
    ('upsAdvOutputVoltage',0),
    ('upsAdvOutputFrequency',0),
    ('upsAdvOutputLoad',0),
    ('upsAdvOutputCurrent',0), 
)
mibVariables=[]
for cmd in commands:
    mibVariables.append(
        cmdgen.MibVariable('PowerNet-MIB',*cmd).addMibSource('/home/pi/APC-SNMP/CompiledMIBs')
    )

indication,status,index,varBinds=cmdGen.getCmd(
    cmdgen.CommunityData('public', mpModel=0),
    cmdgen.UdpTransportTarget(('134.36.67.93',161)),
    *mibVariables
)

if indication: print(indication)
else:
    if status:
        print("{} at {}".format(
            status.prettyPrint(),
            index and varBinds[int(errorIndex)-1] or '?'
        ))
    else:
        for name,val in varBinds:
            print("{} = {}".format(name.prettyPrint(), val.prettyPrint()))
