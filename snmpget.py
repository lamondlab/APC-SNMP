from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen=cmdgen.CommandGenerator()

c1=cmdgen.MibVariable('PowerNet-MIB','upsBasicIdentModel',0).addMibSource('/home/pi/APC-SNMP/CompiledMIBs')
c2=cmdgen.MibVariable('PowerNet-MIB','upsBasicOutputStatus',0).addMibSource('/home/pi/APC-SNMP/CompiledMIBs')

indication,status,index,varBinds=cmdGen.getCmd(
	cmdgen.CommunityData('public', mpModel=0),
	cmdgen.UdpTransportTarget(('134.36.67.93',161)),
        cmdgen.MibVariable('iso.org.dod.internet.mgmt.mib-2.system.sysDescr.0'),
        cmdgen.MibVariable('SNMPv2-MIB', 'sysDescr', 0),
        c1,c2
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
