import re

def untaggedJuniperIntConfig(untaggedNpeConfigDetails):
  config = """
******************** Configuration For {interfaceDesc} ************************************

set interfaces ae{interfaceNumber} unit {subInterfaceNumber} description {interfaceDesc}
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} encapsulation vlan-ccc
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} vlan-id {interfaceVlan}
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} input-vlan-map pop
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} output-vlan-map push

set interfaces ae{interfaceNumber} unit {subInterfaceNumber} family ccc filter input l2-fwf-policer-{outbountDataRate}{outInterfaceRateUnit}
set class-of-service interfaces ae{interfaceNumber} unit {subInterfaceNumber} forwarding-class mission-critical
set class-of-service interfaces ae{interfaceNumber} unit {subInterfaceNumber} rewrite-rules ieee-802.1 l2vpn-rw-8p
set class-of-service interfaces ae{interfaceNumber} unit {subInterfaceNumber} output-traffic-control-profile l3-tcp-unpri-{outbountDataRate}{outInterfaceRateUnit}

set protocols l2circuit neighbor {vcIp} interface ae{interfaceNumber}.{subInterfaceNumber} virtual-circuit-id {vcNumber}
set protocols l2circuit neighbor {vcIp} interface ae{interfaceNumber}.{subInterfaceNumber} description {interfaceDesc}
set protocols l2circuit neighbor {vcIp} interface ae{interfaceNumber}.{subInterfaceNumber} no-control-word
set protocols l2circuit neighbor {vcIp} interface ae{interfaceNumber}.{subInterfaceNumber} mtu 2000
set protocols l2circuit neighbor {vcIp} interface ae{interfaceNumber}.{subInterfaceNumber} encapsulation-type ethernet
set protocols l2circuit neighbor {vcIp} interface ae{interfaceNumber}.{subInterfaceNumber} pseudowire-status-tlv

----------------------------------------------------------------------------
** Please configure the below line if NNI is NGE:****
set class-of-service interfaces xe-x/x/x  unit yyyy rewrite-rules ieee-802.1 l2vpn-rw-8p
set class-of-service interfaces xe-x/x/x  unit yyyy forwarding-class mission-critical

========================================================================================================================================================
""".format(
  interfaceNumber=untaggedNpeConfigDetails["interfaceNumber"],subInterfaceNumber=untaggedNpeConfigDetails["subInterfaceNumber"],interfaceVlan=untaggedNpeConfigDetails["vlanNumber"],
  interfaceDesc=untaggedNpeConfigDetails["interfaceDesc"],vcIp=untaggedNpeConfigDetails["vcIp"],
  vcNumber=untaggedNpeConfigDetails["vcNumber"],outbountDataRate=untaggedNpeConfigDetails["outbountDataRate"],
  inboundDataRate=untaggedNpeConfigDetails["inboundDataRate"],
  inInterfaceRateUnit=untaggedNpeConfigDetails["inInterfaceRateUnit"],
  outInterfaceRateUnit=untaggedNpeConfigDetails["outInterfaceRateUnit"]
  )
  return config

def taggedJuniperIntConfig(taggedNpeConfigDetails):
  config = """
******************** Configuration For {interfaceDesc} ************************************
 
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} description {interfaceDesc}
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} encapsulation vlan-ccc
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} vlan-tags outer {peVlanId}
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} vlan-tags inner {ceVlanId}
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} input-vlan-map pop-swap
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} input-vlan-map inner-vlan-id {ceVlanId}
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} output-vlan-map swap-push
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} family ccc

set interfaces ae{interfaceNumber} unit {subInterfaceNumber} family ccc filter input l2-fwf-policer-{outbountDataRate}{outInterfaceRateUnit}
set class-of-service interfaces ae{interfaceNumber} unit {subInterfaceNumber} forwarding-class mission-critical
set class-of-service interfaces ae{interfaceNumber} unit {subInterfaceNumber} rewrite-rules ieee-802.1 l2vpn-rw-8p
set class-of-service interfaces ae{interfaceNumber} unit {subInterfaceNumber} output-traffic-control-profile l3-tcp-unpri-{outbountDataRate}{outInterfaceRateUnit}


set protocols l2circuit neighbor {vcIp} interface ae{interfaceNumber}.{subInterfaceNumber} virtual-circuit-id {vcNumber}
set protocols l2circuit neighbor {vcIp} interface ae{interfaceNumber}.{subInterfaceNumber} description {interfaceDesc}
set protocols l2circuit neighbor {vcIp} interface ae{interfaceNumber}.{subInterfaceNumber} no-control-word
set protocols l2circuit neighbor {vcIp} interface ae{interfaceNumber}.{subInterfaceNumber} mtu 2000
set protocols l2circuit neighbor {vcIp} interface ae{interfaceNumber}.{subInterfaceNumber} encapsulation-type ethernet-vlan
set protocols l2circuit neighbor {vcIp} interface ae{interfaceNumber}.{subInterfaceNumber} pseudowire-status-tlv

----------------------------------------------------------------------------

Please configure the below line on NNI device:
==============================================
config
l2vpn profile <MPS-SITECODE-1>:<MPS-SITECODE-2>_qnq
peer <MPS1 Loopback0 IP>
redundancy-mode independent
remote-encap dot1q
backup-peer <MPS2 Loopback0 IP>
end

xc <port> vlan-id <vlan> vc-id <NEW VC-ID 1> profile <MPS-SITECODE-1>:<MPS-SITECODE-2>_qnq  backup
vc-id <NEW VC-ID 2> peer <MPS2 Loopback0 IP>

========================================================================================================================================================
""".format(
  interfaceNumber=taggedNpeConfigDetails["interfaceNumber"],
  subInterfaceNumber=taggedNpeConfigDetails["subInterfaceNumber"],
  peVlanId=taggedNpeConfigDetails["peVlanId"],
  ceVlanId=taggedNpeConfigDetails["ceVlanId"],
  interfaceDesc=taggedNpeConfigDetails["interfaceDesc"],
  vcIp=taggedNpeConfigDetails["vcIp"],
  vcNumber=taggedNpeConfigDetails["vcNumber"],
  outbountDataRate=taggedNpeConfigDetails["outbountDataRate"],
  inboundDataRate=taggedNpeConfigDetails["inboundDataRate"],
  inInterfaceRateUnit=taggedNpeConfigDetails["inInterfaceRateUnit"],
  outInterfaceRateUnit=taggedNpeConfigDetails["outInterfaceRateUnit"]
  )
  return config

def taggedNGEJuniperIntConfig(taggedNGEConfigDetails):
  config = """
******************** Configuration For {interfaceDesc} ************************************
 
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} description {interfaceDesc}
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} encapsulation vlan-ccc
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} vlan-tags outer {peVlanId}
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} vlan-tags inner {ceVlanId}
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} input-vlan-map pop-swap
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} input-vlan-map inner-vlan-id {ceVlanId}
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} output-vlan-map swap-push
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} family ccc

set interfaces ae{interfaceNumber} unit {subInterfaceNumber} family ccc filter input l2-fwf-policer-{outbountDataRate}{outInterfaceRateUnit}
set class-of-service interfaces ae{interfaceNumber} unit {subInterfaceNumber} forwarding-class mission-critical
set class-of-service interfaces ae{interfaceNumber} unit {subInterfaceNumber} rewrite-rules ieee-802.1 l2vpn-rw-8p
set class-of-service interfaces ae{interfaceNumber} unit {subInterfaceNumber} output-traffic-control-profile l3-tcp-unpri-{outbountDataRate}{outInterfaceRateUnit}

set protocols l2circuit neighbor {vcIp} interface ae{interfaceNumber}.{subInterfaceNumber} virtual-circuit-id {vcNumber}
set protocols l2circuit neighbor {vcIp} interface ae{interfaceNumber}.{subInterfaceNumber} description {interfaceDesc}
set protocols l2circuit neighbor {vcIp} interface ae{interfaceNumber}.{subInterfaceNumber} no-control-word
set protocols l2circuit neighbor {vcIp} interface ae{interfaceNumber}.{subInterfaceNumber} mtu 2000
set protocols l2circuit neighbor {vcIp} interface ae{interfaceNumber}.{subInterfaceNumber} encapsulation-type ethernet
set protocols l2circuit neighbor {vcIp} interface ae{interfaceNumber}.{subInterfaceNumber} pseudowire-status-tlv

----------------------------------------------------------------------------
Please configure the below line on NNI(NGE)side:
================================================
set class-of-service interfaces xe-x/x/x  unit yyyy rewrite-rules ieee-802.1 l2vpn-rw-8p
set class-of-service interfaces xe-x/x/x  unit yyyy forwarding-class mission-critical

========================================================================================================================================================
""".format(
  interfaceNumber=taggedNGEConfigDetails["interfaceNumber"],
  subInterfaceNumber=taggedNGEConfigDetails["subInterfaceNumber"],
  peVlanId=taggedNGEConfigDetails["peVlanId"],
  ceVlanId=taggedNGEConfigDetails["ceVlanId"],
  interfaceDesc=taggedNGEConfigDetails["interfaceDesc"],
  vcIp=taggedNGEConfigDetails["vcIp"],
  vcNumber=taggedNGEConfigDetails["vcNumber"],
  outbountDataRate=taggedNGEConfigDetails["outbountDataRate"],
  inboundDataRate=taggedNGEConfigDetails["inboundDataRate"],
  inInterfaceRateUnit=taggedNGEConfigDetails["inInterfaceRateUnit"],
  outInterfaceRateUnit=taggedNGEConfigDetails["outInterfaceRateUnit"]
  )
  return config

def efmmgmtIntConfig(efmmgmtNpeConfigDetails):
  config = """
******************** Configuration For {interfaceDesc} ************************************
 
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} vlan-id {interfaceVlan}
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} description {interfaceDesc}
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} encapsulation vlan-bridge

set interfaces irb unit {subInterfaceNumber} description {interfaceDesc}
set interfaces irb unit {subInterfaceNumber} arp-resp unrestricted
set interfaces irb unit {subInterfaceNumber} family inet address {IPaddress}/{cidr}

set interfaces irb unit {subInterfaceNumber} mac 00:01:02:03:04:05

set vlans vlan-{interfaceVlan} l3-interface irb.{subInterfaceNumber}
set vlans vlan-{interfaceVlan} interface ae{interfaceNumber}.{subInterfaceNumber}
set vlans vlan-{interfaceVlan} vlan-id {interfaceVlan}

set routing-instances efm_mgmt interface irb.{subInterfaceNumber}

========================================================================================================================================================
""".format(
  interfaceNumber=efmmgmtNpeConfigDetails["interfaceNumber"],subInterfaceNumber=efmmgmtNpeConfigDetails["subInterfaceNumber"],interfaceVlan=efmmgmtNpeConfigDetails["vlanNumber"],
  interfaceDesc=efmmgmtNpeConfigDetails["interfaceDesc"],IPaddress = efmmgmtNpeConfigDetails["IPaddress"],
  cidr=efmmgmtNpeConfigDetails["SubnetMask"]
  )
  return config

def ttbinternetIntConfig(ttbinternetNpeConfigDetails):
  config = """
******************** Configuration For {interfaceDesc} ************************************
 
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} vlan-id {interfaceVlan}
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} description {interfaceDesc}
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} encapsulation vlan-bridge

set interfaces irb unit {subInterfaceNumber} description {interfaceDesc}
set interfaces irb unit {subInterfaceNumber} arp-resp unrestricted
set interfaces irb unit {subInterfaceNumber} family inet address {IPaddress}/{cidr}

set interfaces irb unit {subInterfaceNumber} mac 00:01:02:03:04:05

set vlans vlan-{interfaceVlan} l3-interface irb.{subInterfaceNumber}
set vlans vlan-{interfaceVlan} interface ae{interfaceNumber}.{subInterfaceNumber}
set vlans vlan-{interfaceVlan} vlan-id {interfaceVlan}

set routing-instances ttb_internet  interface irb.{subInterfaceNumber}

set interfaces ae{interfaceNumber} unit {subInterfaceNumber} family ccc filter input l2-fwf-policer-{outbountDataRate}{outInterfaceRateUnit}
set class-of-service interfaces ae{interfaceNumber} unit {subInterfaceNumber} rewrite-rules ieee-802.1 dia-rw    
set class-of-service interfaces aae{interfaceNumber} unit {subInterfaceNumber} output-traffic-control-profile dia-tcp-{outbountDataRate}{outInterfaceRateUnit}


========================================================================================================================================================
""".format(
  interfaceNumber=ttbinternetNpeConfigDetails["interfaceNumber"],
  subInterfaceNumber=ttbinternetNpeConfigDetails["subInterfaceNumber"],
  interfaceVlan=ttbinternetNpeConfigDetails["vlanNumber"],
  interfaceDesc=ttbinternetNpeConfigDetails["interfaceDesc"],
  IPaddress = ttbinternetNpeConfigDetails["IPaddress"],
  cidr=ttbinternetNpeConfigDetails["SubnetMask"],
  outbountDataRate=ttbinternetNpeConfigDetails["outbountDataRate"],
  inboundDataRate=ttbinternetNpeConfigDetails["inboundDataRate"],
  inInterfaceRateUnit=ttbinternetNpeConfigDetails["inInterfaceRateUnit"],
  outInterfaceRateUnit=ttbinternetNpeConfigDetails["outInterfaceRateUnit"]
  )
  return config

def ttbinternetIntEADConfig(ttbinternetEADConfigDetails):
  config = """
******************** Configuration For {interfaceDesc} ************************************
 
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} vlan-id {interfaceVlan}
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} description {interfaceDesc}
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} family inet address {IPaddress}/{cidr}

set routing-instances ttb_internet  interface ae{interfaceNumber}.{subInterfaceNumber}

set interfaces ae{interfaceNumber} unit {subInterfaceNumber} family ccc filter input l2-fwf-policer-{outbountDataRate}{outInterfaceRateUnit}
set class-of-service interfaces ae{interfaceNumber} unit {subInterfaceNumber} rewrite-rules ieee-802.1 dia-rw    
set class-of-service interfaces aae{interfaceNumber} unit {subInterfaceNumber} output-traffic-control-profile dia-tcp-{outbountDataRate}{outInterfaceRateUnit}


========================================================================================================================================================
""".format(
  interfaceNumber=ttbinternetEADConfigDetails["interfaceNumber"],
  subInterfaceNumber=ttbinternetEADConfigDetails["subInterfaceNumber"],
  interfaceVlan=ttbinternetEADConfigDetails["vlanNumber"],
  interfaceDesc=ttbinternetEADConfigDetails["interfaceDesc"],
  IPaddress = ttbinternetEADConfigDetails["IPaddress"],
  cidr=ttbinternetEADConfigDetails["SubnetMask"],
  outbountDataRate=ttbinternetEADConfigDetails["outbountDataRate"],
  inboundDataRate=ttbinternetEADConfigDetails["inboundDataRate"],
  inInterfaceRateUnit=ttbinternetEADConfigDetails["inInterfaceRateUnit"],
  outInterfaceRateUnit=ttbinternetEADConfigDetails["outInterfaceRateUnit"]
  )
  return config

def ttbinternetIntEoFTTCConfig(ttbinternetEoFTTCConfigDetails):
  config = """
******************** Configuration For {interfaceDesc} ************************************
 
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} vlan-id {interfaceVlan}
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} description {interfaceDesc}
set interfaces ae{interfaceNumber} unit {subInterfaceNumber} family inet address {IPaddress}/{cidr}

set routing-instances ttb_internet  interface ae{interfaceNumber}.{subInterfaceNumber}

set interfaces ae{interfaceNumber} unit {subInterfaceNumber} family ccc filter input l2-fwf-policer-{outbountDataRate}{outInterfaceRateUnit}
set class-of-service interfaces ae{interfaceNumber} unit {subInterfaceNumber} rewrite-rules ieee-802.1 dia-rw    
set class-of-service interfaces aae{interfaceNumber} unit {subInterfaceNumber} output-traffic-control-profile dia-tcp-{outbountDataRate}{outInterfaceRateUnit}


========================================================================================================================================================
""".format(
  interfaceNumber=ttbinternetEoFTTCConfigDetails["interfaceNumber"],
  subInterfaceNumber=ttbinternetEoFTTCConfigDetails["subInterfaceNumber"],
  interfaceVlan=ttbinternetEoFTTCConfigDetails["vlanNumber"],
  interfaceDesc=ttbinternetEoFTTCConfigDetails["interfaceDesc"],
  IPaddress = ttbinternetEoFTTCConfigDetails["IPaddress"],
  cidr=ttbinternetEoFTTCConfigDetails["SubnetMask"],
  outbountDataRate=ttbinternetEoFTTCConfigDetails["outbountDataRate"],
  inboundDataRate=ttbinternetEoFTTCConfigDetails["inboundDataRate"],
  inInterfaceRateUnit=ttbinternetEoFTTCConfigDetails["inInterfaceRateUnit"],
  outInterfaceRateUnit=ttbinternetEoFTTCConfigDetails["outInterfaceRateUnit"]
  )
  return config
  
def validateIsInteger(strinput):
  if strinput.isdigit():
    return True
  else:
    return False

def getInterfaceDetails(line):
  interface = line.split()[1].split(".", 1)
  interfaceNumber = re.search('Eth-Trunk(.*)$', interface[0]).group(1)
  return  interfaceNumber if validateIsInteger(interfaceNumber) else None, interface[1] if validateIsInteger(interface[1]) else None

def getVcNumber(line):
  vcDetails = line.split()
  return vcDetails[2], vcDetails[3] if validateIsInteger(vcDetails[3]) else None
 
def getIPadderss(line):
  IPDetails = line.split()
  cidr=''.join(list(map(lambda x: bin(x)[2:].zfill(8), list(map(int, IPDetails[3].split(".")))))).count("1")
  return IPDetails[2], cidr

def getInterfaceDataRate(line):
  #!disclaimer
  interfaceDataRate = re.search('qos-profile.*?(\d+)(mb|gb)', line).group(1)
  interfaceRateUnit = re.search('qos-profile.*?(mb|gb)', line).group(1)
  if interfaceRateUnit == "mb":
    interfaceRateUnit = "m"
  elif interfaceRateUnit == "gb":
    interfaceRateUnit = "g"
  else:
    interfaceRateUnit = None
  return interfaceDataRate if validateIsInteger(interfaceDataRate) else None, interfaceRateUnit

def handleUntaggedNPE(num, line, untaggedNpeConfigDetails):
  if num == 1:
    interfaceNumber, subInterfaceNumber = getInterfaceDetails(line)
    untaggedNpeConfigDetails.update({"interfaceNumber": interfaceNumber, "subInterfaceNumber":subInterfaceNumber})
  if num == 2:
    vlan = line.split()[2]
    if validateIsInteger(vlan):
      untaggedNpeConfigDetails["vlanNumber"] = vlan
    else:
      untaggedNpeConfigDetails["vlanNumber"] = None
  if num == 4:
    interfaceDesc = line.split("description ", 1)[1]
    untaggedNpeConfigDetails["interfaceDesc"] = interfaceDesc
  if "mpls l2vc" in line:
    vcIp, vcNumber = getVcNumber(line)
    untaggedNpeConfigDetails.update({"vcIp": vcIp, "vcNumber":vcNumber})
  if "qos"  in line:
    outbountDataRate, outInterfaceRateUnit = getInterfaceDataRate(line)
    untaggedNpeConfigDetails.update({"outbountDataRate": outbountDataRate, "outInterfaceRateUnit":outInterfaceRateUnit})
  if "qos"  in line:
    inboundDataRate, inInterfaceRateUnit = getInterfaceDataRate(line)
    untaggedNpeConfigDetails["inboundDataRate"] = getInterfaceDataRate(line)
    untaggedNpeConfigDetails.update({"inboundDataRate": inboundDataRate, "inInterfaceRateUnit":inInterfaceRateUnit})
  return untaggedNpeConfigDetails

def handleTaggedNPE(num,line, taggedNpeConfigDetails):
  if num == 1:
    interfaceNumber, subInterfaceNumber = getInterfaceDetails(line)
    taggedNpeConfigDetails.update({"interfaceNumber": interfaceNumber, "subInterfaceNumber":subInterfaceNumber})
  if num == 3:
    interfaceDesc = line.split("description ", 1)[1]
    taggedNpeConfigDetails["interfaceDesc"] = interfaceDesc
  if num == 6:
    lineSplit = line.split()
    peVlanId = lineSplit[3]
    ceVlanId = lineSplit[5]
    if validateIsInteger(peVlanId) and validateIsInteger(ceVlanId):
      taggedNpeConfigDetails.update({"peVlanId": peVlanId, "ceVlanId":ceVlanId})
    else:
      taggedNpeConfigDetails.update({"peVlanId": None, "ceVlanId":None})
  if "mpls l2vc" in line:
    vcIp, vcNumber = getVcNumber(line)
    taggedNpeConfigDetails.update({"vcIp": vcIp, "vcNumber":vcNumber})
  if "qos"  in line:
    outbountDataRate, outInterfaceRateUnit = getInterfaceDataRate(line)
    taggedNpeConfigDetails.update({"outbountDataRate": outbountDataRate, "outInterfaceRateUnit":outInterfaceRateUnit})
  if "qos"  in line:
    inboundDataRate, inInterfaceRateUnit = getInterfaceDataRate(line)
    taggedNpeConfigDetails["inboundDataRate"] = getInterfaceDataRate(line)
    taggedNpeConfigDetails.update({"inboundDataRate": inboundDataRate, "inInterfaceRateUnit":inInterfaceRateUnit})
  return taggedNpeConfigDetails

def handleTaggedNGE(num,line, taggedNGEConfigDetails):
  if num == 1:
    interfaceNumber, subInterfaceNumber = getInterfaceDetails(line)
    taggedNGEConfigDetails.update({"interfaceNumber": interfaceNumber, "subInterfaceNumber":subInterfaceNumber})
  if num == 3:
    interfaceDesc = line.split("description ", 1)[1]
    taggedNGEConfigDetails["interfaceDesc"] = interfaceDesc
  if num == 6:
    lineSplit = line.split()
    peVlanId = lineSplit[3]
    ceVlanId = lineSplit[5]
    if validateIsInteger(peVlanId) and validateIsInteger(ceVlanId):
      taggedNGEConfigDetails.update({"peVlanId": peVlanId, "ceVlanId":ceVlanId})
    else:
      taggedNGEConfigDetails.update({"peVlanId": None, "ceVlanId":None})
  if "mpls l2vc" in line:
    vcIp, vcNumber = getVcNumber(line)
    taggedNGEConfigDetails.update({"vcIp": vcIp, "vcNumber":vcNumber})
  if "qos"  in line:
    outbountDataRate, outInterfaceRateUnit = getInterfaceDataRate(line)
    taggedNGEConfigDetails.update({"outbountDataRate": outbountDataRate, "outInterfaceRateUnit":outInterfaceRateUnit})
  if "qos"  in line:
    inboundDataRate, inInterfaceRateUnit = getInterfaceDataRate(line)
    taggedNGEConfigDetails["inboundDataRate"] = getInterfaceDataRate(line)
    taggedNGEConfigDetails.update({"inboundDataRate": inboundDataRate, "inInterfaceRateUnit":inInterfaceRateUnit})
  return taggedNGEConfigDetails

def handleefmmgmtNPE(num, line, efmmgmtNpeConfigDetails):
  if num == 1:
    interfaceNumber, subInterfaceNumber = getInterfaceDetails(line)
    efmmgmtNpeConfigDetails.update({"interfaceNumber": interfaceNumber, "subInterfaceNumber":subInterfaceNumber})
  if num == 2:
    vlan = line.split()[2]
    if validateIsInteger(vlan):
      efmmgmtNpeConfigDetails["vlanNumber"] = vlan
    else:
      efmmgmtNpeConfigDetails["vlanNumber"] = None
  if num == 4:
    interfaceDesc = line.split("description ", 1)[1]
    efmmgmtNpeConfigDetails["interfaceDesc"] = interfaceDesc
  if num == 6:
    IPaddress, subnetmask = getIPadderss(line)
    efmmgmtNpeConfigDetails.update({"IPaddress": IPaddress, "SubnetMask":subnetmask})
  return efmmgmtNpeConfigDetails

def handlettbinternetNPE(num,line, ttbinternetNpeConfigDetails):
  if num == 1:
    interfaceNumber, subInterfaceNumber = getInterfaceDetails(line)
    ttbinternetNpeConfigDetails.update({"interfaceNumber": interfaceNumber, "subInterfaceNumber":subInterfaceNumber})
  if num == 2:
    vlan = line.split()[2]
    if validateIsInteger(vlan):
      ttbinternetNpeConfigDetails["vlanNumber"] = vlan
    else:
      ttbinternetNpeConfigDetails["vlanNumber"] = None
  if num == 4:
    interfaceDesc = line.split("description ", 1)[1]
    ttbinternetNpeConfigDetails["interfaceDesc"] = interfaceDesc
  if num == 6:
      IPaddress, subnetmask = getIPadderss(line)
      ttbinternetNpeConfigDetails.update({"IPaddress": IPaddress, "SubnetMask":subnetmask})
  if "qos"  in line: 
    outbountDataRate, outInterfaceRateUnit = getInterfaceDataRate(line)
    ttbinternetNpeConfigDetails.update({"outbountDataRate": outbountDataRate, "outInterfaceRateUnit":outInterfaceRateUnit})
  if "qos"  in line:
    inboundDataRate, inInterfaceRateUnit = getInterfaceDataRate(line)
    ttbinternetNpeConfigDetails["inboundDataRate"] = getInterfaceDataRate(line)
    ttbinternetNpeConfigDetails.update({"inboundDataRate": inboundDataRate, "inInterfaceRateUnit":inInterfaceRateUnit})
  return ttbinternetNpeConfigDetails

def handlettbinternetEAD(num,line, ttbinternetEADConfigDetails):
  if num == 1:
    interfaceNumber, subInterfaceNumber = getInterfaceDetails(line)
    ttbinternetEADConfigDetails.update({"interfaceNumber": interfaceNumber, "subInterfaceNumber":subInterfaceNumber})
  if num == 2:
    vlan = line.split()[2]
    if validateIsInteger(vlan):
      ttbinternetEADConfigDetails["vlanNumber"] = vlan
    else:
      ttbinternetEADConfigDetails["vlanNumber"] = None
  if num == 4:
    interfaceDesc = line.split("description ", 1)[1]
    ttbinternetEADConfigDetails["interfaceDesc"] = interfaceDesc
  if num == 6:
      IPaddress, subnetmask = getIPadderss(line)
      ttbinternetEADConfigDetails.update({"IPaddress": IPaddress, "SubnetMask":subnetmask})
  if "qos"  in line: 
    outbountDataRate, outInterfaceRateUnit = getInterfaceDataRate(line)
    ttbinternetEADConfigDetails.update({"outbountDataRate": outbountDataRate, "outInterfaceRateUnit":outInterfaceRateUnit})
  if "qos"  in line:
    inboundDataRate, inInterfaceRateUnit = getInterfaceDataRate(line)
    ttbinternetEADConfigDetails["inboundDataRate"] = getInterfaceDataRate(line)
    ttbinternetEADConfigDetails.update({"inboundDataRate": inboundDataRate, "inInterfaceRateUnit":inInterfaceRateUnit})
  return ttbinternetEADConfigDetails

def handlettbinternetEoFTTC(num,line, ttbinternetEoFTTCConfigDetails):
  if num == 1:
    interfaceNumber, subInterfaceNumber = getInterfaceDetails(line)
    ttbinternetEoFTTCConfigDetails.update({"interfaceNumber": interfaceNumber, "subInterfaceNumber":subInterfaceNumber})
  if num == 2:
    vlan = line.split()[2]
    if validateIsInteger(vlan):
      ttbinternetEoFTTCConfigDetails["vlanNumber"] = vlan
    else:
      ttbinternetEoFTTCConfigDetails["vlanNumber"] = None
  if num == 4:
    interfaceDesc = line.split("description ", 1)[1]
    ttbinternetEoFTTCConfigDetails["interfaceDesc"] = interfaceDesc
  if num == 6:
      IPaddress, subnetmask = getIPadderss(line)
      ttbinternetEoFTTCConfigDetails.update({"IPaddress": IPaddress, "SubnetMask":subnetmask})
  if "qos"  in line: 
    outbountDataRate, outInterfaceRateUnit = getInterfaceDataRate(line)
    ttbinternetEoFTTCConfigDetails.update({"outbountDataRate": outbountDataRate, "outInterfaceRateUnit":outInterfaceRateUnit})
  if "qos"  in line:
    inboundDataRate, inInterfaceRateUnit = getInterfaceDataRate(line)
    ttbinternetEoFTTCConfigDetails["inboundDataRate"] = getInterfaceDataRate(line)
    ttbinternetEoFTTCConfigDetails.update({"inboundDataRate": inboundDataRate, "inInterfaceRateUnit":inInterfaceRateUnit})
  return ttbinternetEoFTTCConfigDetails
  
#Clear the Outputfile before proceeding
raw = open('C:\Blended Migration\outputFile.txt', "w")

with open('C:\Blended Migration\Sourceconfig.txt') as myfile:
      content=myfile.read()
eachInterfaceIntoList = re.findall(r'(?:interface Eth-Trunk).*?(?=interface Eth-Trunk|$)', content, re.DOTALL)

for interfaceBlock in eachInterfaceIntoList:
    untaggedNPE = taggedNPE = taggedNGE = efmmgmtNPE = ttbinternetNPE = ttbinternetEAD = ttbinternetEoFTTC = False
    taggedNpeConfigDetails = {}
    taggedNGEConfigDetails = {}
    untaggedNpeConfigDetails = {}
    efmmgmtNpeConfigDetails = {}
    ttbinternetNpeConfigDetails = {}
    ttbinternetEADConfigDetails = {}
    ttbinternetEoFTTCConfigDetails = {}
    InterfaceBlockReadLine = interfaceBlock.splitlines()
    if "dot1q" in InterfaceBlockReadLine[1]:
      if "efm-mgmt" in InterfaceBlockReadLine[4]:
        print("efm-mgmt")
        efmmgmtNPE = True
      elif "ttb_internet" in InterfaceBlockReadLine[4]:
       print("ttb_internet")
       if "description" in InterfaceBlockReadLine[3]:
           TTBFindList = re.findall(r'(?::).*?(?= ""|$)',InterfaceBlockReadLine[3], re.DOTALL)
           print(TTBFindList)
           TTBFindList_1 = TTBFindList[0]
           print(TTBFindList_1[:4])
           if TTBFindList_1[:4] == ":EAD":
               print("EAD TTB Internet")
               ttbinternetEAD = True
           elif TTBFindList_1[:4] == ":EFM":
               print("EFM TTB Internet")
               ttbinternetNPE = True
           elif TTBFindList_1[:4] == ":EoF":
               print("EoFTTC TTB Internet")
               ttbinternetEoFTTC = True
      elif "mpls" in InterfaceBlockReadLine[6]:
          print("L2 MPLS circuit")
          untaggedNPE =  True
    elif "qinq termination" in InterfaceBlockReadLine[5]:
      print("Tagged L2 MPLS Circuit")
      if "mpls" in InterfaceBlockReadLine[6]:
          NNIIPFindList = re.findall(r'(?:mpls l2vc 10.).*?(?= |$)', InterfaceBlockReadLine[6], re.DOTALL)
          print(NNIIPFindList)
          NNIIPFindList_1 =NNIIPFindList[0]
          print(NNIIPFindList_1[17])
          if NNIIPFindList_1[17] == '0':
              print("its Tagged NGE circuit")
              taggedNGE =  True
          else:
              print("its Tagged NPE Circuit")
              taggedNPE = True
    for num, line in enumerate(InterfaceBlockReadLine, start=1):
      if untaggedNPE:
        untaggedNpeConfigDetails = handleUntaggedNPE(num,line, untaggedNpeConfigDetails)
      elif taggedNPE:
        taggedNpeConfigDetails = handleTaggedNPE(num,line, taggedNpeConfigDetails)
      elif taggedNGE:
          taggedNGEConfigDetails = handleTaggedNPE(num,line, taggedNGEConfigDetails)
      elif efmmgmtNPE:
          efmmgmtNpeConfigDetails = handleefmmgmtNPE(num,line, efmmgmtNpeConfigDetails)
      elif ttbinternetNPE:
        ttbinternetNpeConfigDetails = handlettbinternetNPE(num,line, ttbinternetNpeConfigDetails)
      elif ttbinternetEAD:
          ttbinternetEADConfigDetails = handlettbinternetEAD(num,line, ttbinternetEADConfigDetails)
      elif ttbinternetEoFTTC:
          ttbinternetEoFTTCConfigDetails = handlettbinternetEoFTTC(num,line, ttbinternetEoFTTCConfigDetails)
    print(untaggedNpeConfigDetails)
    print(taggedNpeConfigDetails)
    print(taggedNGEConfigDetails)
    print(efmmgmtNpeConfigDetails)
    print(ttbinternetNpeConfigDetails)
    print(ttbinternetEADConfigDetails)
    print(ttbinternetEoFTTCConfigDetails)
    #validation
    def validation_interface(configDetail):
      for k,v in configDetail.items():
        if v is None:
          error_message="Please check the missing details on this below interface {}".format(configDetail)
          with open('C:\Blended Migration\outputFile.txt', '+a') as myoutputfile:
            myoutputfile.write(error_message)
          raise Exception(error_message)
    if untaggedNPE:
      validation_interface(untaggedNpeConfigDetails)
      singleInterfaceConfig = untaggedJuniperIntConfig(untaggedNpeConfigDetails)
    elif taggedNPE:
      validation_interface(taggedNpeConfigDetails)
      singleInterfaceConfig = taggedJuniperIntConfig(taggedNpeConfigDetails)
    elif taggedNGE:
        validation_interface(taggedNGEConfigDetails)
        singleInterfaceConfig = taggedNGEJuniperIntConfig(taggedNGEConfigDetails)
    elif efmmgmtNPE:
        validation_interface(efmmgmtNpeConfigDetails)
        singleInterfaceConfig = efmmgmtIntConfig(efmmgmtNpeConfigDetails)
    elif ttbinternetNPE:
        validation_interface(ttbinternetNpeConfigDetails)
        singleInterfaceConfig = ttbinternetIntConfig(ttbinternetNpeConfigDetails)
    elif ttbinternetEAD:
        validation_interface(ttbinternetEADConfigDetails)
        singleInterfaceConfig = ttbinternetIntEADConfig(ttbinternetEADConfigDetails)
    elif ttbinternetEoFTTC:
        validation_interface(ttbinternetEoFTTCConfigDetails)
        singleInterfaceConfig = ttbinternetIntEoFTTCConfig(ttbinternetEoFTTCConfigDetails)
    with open('outputFile.txt', '+a') as myoutputfile:
      myoutputfile.write(singleInterfaceConfig)
#closing the input and output file
myfile.close()
myoutputfile.close()
#closing the input and output file
myfile.close()
myoutputfile.close()
