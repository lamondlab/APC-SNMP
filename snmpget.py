from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen=cmdgen.CommandGenerator()

indication,status,index,varBinds=cmdGen.getCmd(
	cmdgen.CommunityData('public'),
	cmdgen.UdpTransportTarget(('134.36.67.93',161)),
	'1.3.6.1.4.1.318.1.2.1.1.1.0'
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