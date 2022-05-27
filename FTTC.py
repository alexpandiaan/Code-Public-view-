import xlrd   
loc = ("C:/Blended Migration/Migration_Fillsheet_v1.xlsx") 
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(1) 
rows = input("how many rows of data available in excel sheet\n")
var = int (rows)
i = 1
dum='.0'
dot='.'
dash='-'
MPS1_name=sheet.cell_value(49,0)
MPS1_IP=sheet.cell_value(49,1)
MPS2_name=sheet.cell_value(50,0)
MPS2_IP=sheet.cell_value(50,1)

NGE1_name=sheet.cell_value(49,2)
NGE1_IP=sheet.cell_value(49,3)
NGE2_name=sheet.cell_value(50,2)
NGE2_IP=sheet.cell_value(50,3)

x2=sheet.cell_value(49,4)
NGE1_PS = int(x2)
x3=sheet.cell_value(50,4)
NGE2_PS = int(x3)

lt_1=sheet.cell_value(49,5)
lt_2=sheet.cell_value(50,5)

a1 = sheet.cell_value(49,6)	  
ae_1 = int(a1)
a2 =  sheet.cell_value(50,6)
ae_2 = int(a2)
f=open("FTTC-Config.txt",'w')
while ( i <= var ) : 
		x4 = sheet.cell_value(i,6)
		MPS_Number = int(x4)
		if ( MPS_Number == 1 ) :
			x = sheet.cell_value(i,2)
			VSI_ID=int(x)      
			OGHP_ID = sheet.cell_value(i,0)
			GE_Port = sheet.cell_value(i,1)
			x1= sheet.cell_value(i,3)
			Mul_VLAN = str(x1)
			Multicast_IP = sheet.cell_value(i,4)
			Multicast_IP_subnet=Multicast_IP.split("/")
			Multicast_IPClass=Multicast_IP_subnet[0].split(".")
			Mul_IP ='.'.join(Multicast_IPClass[0:3]+[str(int(Multicast_IPClass[-1])+1)])
			desc = sheet.cell_value(i,5)
			f.write("\n")
			f.write (" Please find the below Configurations for "+OGHP_ID+'\n')
			f.write("**********************************MPS Configurations*********************************** \n")
			f.write("# \n")
			f.write( "vsi vsi_"+str(VSI_ID)+'\n')
			f.write(" pwsignal ldp \n ")
			f.write("  vsi-id "+str(VSI_ID)+'\n')
			f.write("  control-word enable \n")
			f.write("  peer "+str(NGE1_IP)+'\n')
			f.write("  peer "+str(NGE2_IP )+'\n')
			f.write("  protect-group vpls_"+str(VSI_ID)+'\n')
			f.write("   protect-mode pw-redundancy master \n")  
			f.write("	reroute never \n")      
			f.write("   peer "+str(NGE1_IP)+" preference 1 \n")
			f.write("   peer "+str(NGE2_IP)+" preference 2 \n")
			f.write("   traffic-statistics enable \n")
			f.write(" mtu 2000 \n")
			f.write(" ignore-ac-state \n")
			f.write(" mac-learning disable \n")
			f.write("# \n")      
			f.write("interface "+GE_Port+'\n')
			f.write("negotiation auto  \n")
			f.write("description "+desc+'\n')
			f.write("mtu 2000 \n")
			f.write("undo shutdown \n")
			f.write("undo dcn \n")
			f.write("# \n")
			MPS_Version = sheet.cell_value(49,7)
			if ( MPS_Version == 7 ) :
					f.write("interface "+GE_Port+dot+str(VSI_ID)+'\n')
					f.write("description "+desc+'\n')
					f.write("vlan-type dot1q "+str(VSI_ID)+'\n')
					f.write("statistic enable \n")
					f.write("l2 binding vsi vsi_"+str(VSI_ID)+'\n')
					f.write("trust upstream ttt-default inbound \n")
					f.write("trust upstream ttt-default outbound \n")
					f.write("trust 8021p outbound \n")
					if GE_Port == 'Gi0/2/0' or  GE_Port == 'Gi0/2/1' or GE_Port == 'Gi0/2/2' or  GE_Port == 'Gi0/2/3' or GE_Port == 'Gi0/3/0' or  GE_Port == 'Gi0/3/1' or GE_Port == 'Gi0/3/2' or  GE_Port == 'Gi0/3/3':
						f.write("qos-profile ttt-default-10gb outbound identifier none \n")
					else :
						f.write("qos-profile ttt-default-1gb outbound identifier none \n")
					f.write("# \n")
					if (len(Mul_VLAN) == 9 ):
						x1_class = x1.split("-")
						mv = x1_class[0:3]
						Mul_vlan1= mv[0]
						Mul_vlan2= mv[1]				
						Multicast_IP_subnet=Multicast_IP.split("-")
						Multicast_IPClass=Multicast_IP_subnet[0].split("/")
						M1 = Multicast_IPClass[0]
						M2 = Multicast_IPClass[1]				
						def hostip(Multicast_IP):
							Multicast_IP_subnet=Multicast_IP.split("/")
							Multicast_IPClass=Multicast_IP_subnet[0].split(".")
							Mul_IP ='.'.join(Multicast_IPClass[0:3]+[str(int(Multicast_IPClass[-1])+1)])
							return(Mul_IP)				
						Multicast_IP1 = hostip(M1)
						Multicast_IP2 = hostip(M2)
						f.write("interface "+GE_Port+dot+str(Mul_vlan1)+'\n')
						f.write("vlan-type dot1q "+str(Mul_vlan1)+'\n')
						f.write("mtu 2000 \n")
						f.write("description :r="+OGHP_ID+"/"+str(VSI_ID)+":sev=5:p=ttt:t=iptv: \n")
						f.write("ip binding vpn-instance iptv \n")
						f.write("ip address "+Multicast_IP1+" 255.255.255.252 \n") 
						f.write("statistic enable \n")
						f.write("pim sm \n")
						f.write("igmp enable \n")
						f.write("igmp version 3 \n")
						f.write("igmp timer query 10 \n")
						f.write("igmp group-policy acl-name non-glop-filter \n")				
						f.write("\n")
						f.write("interface "+GE_Port+dot+str(Mul_vlan2)+'\n')
						f.write("vlan-type dot1q "+str(Mul_vlan2)+'\n')
						f.write("mtu 2000 \n")
						f.write("description :r="+OGHP_ID+"/"+str(VSI_ID)+":sev=5:p=ttt:t=iptv: \n")
						f.write("ip binding vpn-instance iptv \n")
						f.write("ip address "+Multicast_IP2+" 255.255.255.252 \n") 
						f.write("statistic enable \n")
						f.write("pim sm \n")
						f.write("igmp enable \n")
						f.write("igmp version 3 \n")
						f.write("igmp timer query 10 \n")
						f.write("igmp group-policy acl-name non-glop-filter \n")
				
					else:
						Multicast_IP_subnet=Multicast_IP.split("/")
						Multicast_IPClass=Multicast_IP_subnet[0].split(".")
						Mul_IP ='.'.join(Multicast_IPClass[0:3]+[str(int(Multicast_IPClass[-1])+1)])
						Mul_VLAN_x1= int(x1)
						f.write("interface "+GE_Port+dot+str(Mul_VLAN_x1)+'\n')
						f.write("vlan-type dot1q "+str(Mul_VLAN_x1)+'\n')
						f.write("mtu 2000 \n")
						f.write("description :r="+OGHP_ID+"/"+str(VSI_ID)+":sev=5:p=ttt:t=iptv: \n")
						f.write("ip binding vpn-instance iptv \n")
						f.write("ip address "+Mul_IP+" 255.255.255.252 \n") 
						f.write("statistic enable \n")
						f.write("pim sm \n")
						f.write("igmp enable \n")
						f.write("igmp version 3 \n")
						f.write("igmp timer query 10 \n")
						f.write("igmp group-policy acl-name non-glop-filter \n")
					
			elif ( MPS_Version == 9 ) :
					f.write("interface "+GE_Port+dot+str(VSI_ID)+'\n')
					f.write("description "+desc+'\n')
					f.write("statistic enable \n")
					f.write("encapsulation dot1q-termination\n")
					f.write("dot1q termination vid "+str(VSI_ID)+'\n')				
					f.write("l2 binding vsi vsi_"+str(VSI_ID)+'\n')
					f.write("trust upstream ttt-default inbound \n")
					f.write("trust upstream ttt-default outbound \n")
					f.write("trust 8021p outbound \n")
					if GE_Port == 'Gi0/2/0' or  GE_Port == 'Gi0/2/1' or GE_Port == 'Gi0/2/2' or  GE_Port == 'Gi0/2/3' or GE_Port == 'Gi0/3/0' or  GE_Port == 'Gi0/3/1' or GE_Port == 'Gi0/3/2' or  GE_Port == 'Gi0/3/3':
						f.write("qos-profile ttt-default-10gb outbound identifier none \n")
					else :
						f.write("qos-profile ttt-default-1gb outbound identifier none \n")					
					f.write("# \n")
					if (len(Mul_VLAN) == 9 ):
						x1_class = x1.split("-")
						mv = x1_class[0:3]
						Mul_vlan1= mv[0]
						Mul_vlan2= mv[1]				
						Multicast_IP_subnet=Multicast_IP.split("-")
						Multicast_IPClass=Multicast_IP_subnet[0].split("/")
						M1 = Multicast_IPClass[0]
						M2 = Multicast_IPClass[1]				
						def hostip(Multicast_IP):
							Multicast_IP_subnet=Multicast_IP.split("/")
							Multicast_IPClass=Multicast_IP_subnet[0].split(".")
							Mul_IP ='.'.join(Multicast_IPClass[0:3]+[str(int(Multicast_IPClass[-1])+1)])
							return(Mul_IP)				
						Multicast_IP1 = hostip(M1)
						Multicast_IP2 = hostip(M2)
						f.write("interface "+GE_Port+dot+str(Mul_vlan1)+'\n')
						f.write("encapsulation dot1q-termination\n")
						f.write("dot1q termination vid "+str(Mul_vlan1)+'\n')
						f.write("mtu 2000 \n")
						f.write("description :r="+OGHP_ID+"/"+str(VSI_ID)+":sev=5:p=ttt:t=iptv: \n")
						f.write("ip binding vpn-instance iptv \n")
						f.write("ip address "+Multicast_IP1+" 255.255.255.252 \n") 
						f.write("statistic enable \n")
						f.write("pim sm \n")
						f.write("igmp enable \n")
						f.write("igmp version 3 \n")
						f.write("igmp timer query 10 \n")
						f.write("igmp group-policy acl-name non-glop-filter \n")				
						f.write("\n")
						f.write("interface "+GE_Port+dot+str(Mul_vlan2)+'\n')
						f.write("vlan-type dot1q "+str(Mul_vlan2)+'\n')
						f.write("mtu 2000 \n")
						f.write("description :r="+OGHP_ID+"/"+str(VSI_ID)+":sev=5:p=ttt:t=iptv: \n")
						f.write("ip binding vpn-instance iptv \n")
						f.write("ip address "+Multicast_IP2+" 255.255.255.252 \n") 
						f.write("statistic enable \n")
						f.write("pim sm \n")
						f.write("igmp enable \n")
						f.write("igmp version 3 \n")
						f.write("igmp timer query 10 \n")
						f.write("igmp group-policy acl-name non-glop-filter \n")
					
					else:
						Multicast_IP_subnet=Multicast_IP.split("/")
						Multicast_IPClass=Multicast_IP_subnet[0].split(".")
						Mul_IP ='.'.join(Multicast_IPClass[0:3]+[str(int(Multicast_IPClass[-1])+1)])
						Mul_VLAN_x1= int(x1)
						f.write("interface "+GE_Port+dot+str(Mul_VLAN_x1)+'\n')
						f.write("encapsulation dot1q-termination\n")
						f.write("dot1q termination vid "+str(Mul_VLAN_x1)+'\n')
						f.write("mtu 2000 \n")
						f.write("description :r="+OGHP_ID+"/"+str(VSI_ID)+":sev=5:p=ttt:t=iptv: \n")
						f.write("ip binding vpn-instance iptv \n")
						f.write("ip address "+Mul_IP+" 255.255.255.252 \n") 
						f.write("statistic enable \n")
						f.write("pim sm \n")
						f.write("igmp enable \n")
						f.write("igmp version 3 \n")
						f.write("igmp timer query 10 \n")
						f.write("igmp group-policy acl-name non-glop-filter \n")
			f.write("**********************************NGE 1 Configurations******************************************* \n")
			f.write("set interfaces ps"+str(NGE1_PS)+" description :r="+MPS1_name+":q="+GE_Port+dot+str(VSI_ID)+":v=ae"+str(ae_1)+":sev=5:t=pw: \n")
			f.write("set interfaces ps"+str(NGE1_PS)+" anchor-point "+str(lt_1)+'\n')
			f.write("set interfaces ps"+str(NGE1_PS)+" flexible-vlan-tagging \n")
			f.write("set interfaces ps"+str(NGE1_PS)+" auto-configure stacked-vlan-ranges dynamic-profile auto-stacked-pwht accept dhcp-v4 \n")
			f.write("set interfaces ps"+str(NGE1_PS)+" auto-configure stacked-vlan-ranges dynamic-profile auto-stacked-pwht accept pppoe \n")
			f.write("set interfaces ps"+str(NGE1_PS)+" auto-configure stacked-vlan-ranges dynamic-profile auto-stacked-pwht ranges "+str(VSI_ID)+'-'+str(VSI_ID)+",any \n")	
			f.write("set interfaces ps"+str(NGE1_PS)+" auto-configure stacked-vlan-ranges authentication packet-types dhcp-v4 \n")	
			f.write("set interfaces ps"+str(NGE1_PS)+" auto-configure stacked-vlan-ranges authentication packet-types pppoe \n")	
			f.write("set interfaces ps"+str(NGE1_PS)+" auto-configure stacked-vlan-ranges authentication username-include delimiter" ' ' '"@" \n')	
			f.write("set interfaces ps"+str(NGE1_PS)+" auto-configure stacked-vlan-ranges authentication username-include user-prefix pwht \n")	
			f.write("set interfaces ps"+str(NGE1_PS)+" auto-configure stacked-vlan-ranges authentication username-include interface-name \n")	
			f.write("set interfaces ps"+str(NGE1_PS)+" auto-configure stacked-vlan-ranges access-profile vlan-auth-access \n")	
			f.write("set interfaces ps"+str(NGE1_PS)+" auto-configure remove-when-no-subscribers \n")	
			f.write("set interfaces ps"+str(NGE1_PS)+" mtu 2022 \n")	
			f.write("set interfaces ps"+str(NGE1_PS)+" no-gratuitous-arp-request \n")	
			f.write("set interfaces ps"+str(NGE1_PS)+" unit 0 encapsulation ethernet-ccc \n")	
			f.write ('\n')	
			f.write("set protocols l2circuit neighbor "+MPS1_IP+" interface ps"+str(NGE1_PS)+dum+" virtual-circuit-id "+str(VSI_ID)+'\n')	
			f.write("set protocols l2circuit neighbor "+MPS1_IP+" interface ps"+str(NGE1_PS)+dum+" description :r="+MPS1_name+":q=vsi_"+str(VSI_ID)+":v=ae"+str(ae_1)+":sev=5:t=pw: \n")	
			f.write("set protocols l2circuit neighbor "+MPS1_IP+" interface ps"+str(NGE1_PS)+dum+" control-word \n")	
			f.write("set protocols l2circuit neighbor "+MPS1_IP+" interface ps"+str(NGE1_PS)+dum+" mtu 2000 \n")	
			f.write("set protocols l2circuit neighbor "+MPS1_IP+" interface ps"+str(NGE1_PS)+dum+" encapsulation-type ethernet-vlan \n")	
			f.write("set protocols l2circuit neighbor "+MPS1_IP+" interface ps"+str(NGE1_PS)+dum+" pseudowire-status-tlv hot-standby-vc-on \n")	
			f.write ('\n') 	
			f.write("set interfaces "+str(lt_1)+" hierarchical-scheduler implicit-hierarchy \n")	
			f.write("set routing-instances ttt_fttx_res system services dhcp-local-server group dhcp-ls interface ps"+str(NGE1_PS)+dum+'\n')	
			f.write("set class-of-service interfaces interface-set ps"+str(NGE1_PS)+" output-traffic-control-profile 10g-tcp \n")	
			f.write('\n')	  	
			f.write("**********************************NGE 2 Configurations******************************************* \n")	
			f.write("set interfaces ps"+str(NGE2_PS)+" description :r="+MPS1_name+":q="+GE_Port+dot+str(VSI_ID)+":v=ae"+str(ae_2)+":sev=5:t=pw: \n")	
			f.write("set interfaces ps"+str(NGE2_PS)+" anchor-point "+str(lt_2)+'\n')
			f.write("set interfaces ps"+str(NGE2_PS)+" flexible-vlan-tagging \n")	
			f.write("set interfaces ps"+str(NGE2_PS)+" auto-configure stacked-vlan-ranges dynamic-profile auto-stacked-pwht accept dhcp-v4 \n")	
			f.write("set interfaces ps"+str(NGE2_PS)+" auto-configure stacked-vlan-ranges dynamic-profile auto-stacked-pwht accept pppoe \n")	
			f.write("set interfaces ps"+str(NGE2_PS)+" auto-configure stacked-vlan-ranges dynamic-profile auto-stacked-pwht ranges "+str(VSI_ID)+'-'+str(VSI_ID)+",any \n")	
			f.write("set interfaces ps"+str(NGE2_PS)+" auto-configure stacked-vlan-ranges authentication packet-types dhcp-v4 \n")	
			f.write("set interfaces ps"+str(NGE2_PS)+" auto-configure stacked-vlan-ranges authentication packet-types pppoe \n")	
			f.write("set interfaces ps"+str(NGE2_PS)+" auto-configure stacked-vlan-ranges authentication username-include delimiter" ' ' '"@" \n')	
			f.write("set interfaces ps"+str(NGE2_PS)+" auto-configure stacked-vlan-ranges authentication username-include user-prefix pwht \n")	
			f.write("set interfaces ps"+str(NGE2_PS)+" auto-configure stacked-vlan-ranges authentication username-include interface-name \n")	
			f.write("set interfaces ps"+str(NGE2_PS)+" auto-configure stacked-vlan-ranges access-profile vlan-auth-access \n")	
			f.write("set interfaces ps"+str(NGE2_PS)+" auto-configure remove-when-no-subscribers \n")	
			f.write("set interfaces ps"+str(NGE2_PS)+" mtu 2022 \n")	
			f.write("set interfaces ps"+str(NGE2_PS)+" no-gratuitous-arp-request \n")	
			f.write("set interfaces ps"+str(NGE2_PS)+" unit 0 encapsulation ethernet-ccc \n")	
			f.write ('\n') 	
			f.write("set protocols l2circuit neighbor "+MPS1_IP+" interface ps"+str(NGE2_PS)+dum+" virtual-circuit-id "+str(VSI_ID)+'\n')	
			f.write("set protocols l2circuit neighbor "+MPS1_IP+" interface ps"+str(NGE2_PS)+dum+" description :r="+MPS1_name+":q=vsi_"+str(VSI_ID)+":v=ae"+str(ae_2)+":sev=5:t=pw: \n")	
			f.write("set protocols l2circuit neighbor "+MPS1_IP+" interface ps"+str(NGE2_PS)+dum+" control-word \n")	
			f.write("set protocols l2circuit neighbor "+MPS1_IP+" interface ps"+str(NGE2_PS)+dum+" mtu 2000 \n")	
			f.write("set protocols l2circuit neighbor "+MPS1_IP+" interface ps"+str(NGE2_PS)+dum+" encapsulation-type ethernet-vlan \n")	
			f.write("set protocols l2circuit neighbor "+MPS1_IP+" interface ps"+str(NGE2_PS)+dum+" pseudowire-status-tlv hot-standby-vc-on \n")	
			f.write ('\n')	
			f.write("set interfaces "+str(lt_2)+" hierarchical-scheduler implicit-hierarchy \n")	
			f.write("set routing-instances ttt_fttx_res system services dhcp-local-server group dhcp-ls interface ps"+str(NGE2_PS)+dum+'\n')	
			f.write("set class-of-service interfaces interface-set ps"+str(NGE2_PS)+" output-traffic-control-profile 10g-tcp \n")
			NGE1_PS += 1
			NGE2_PS += 1
			i += 1
					
		else:
			x = sheet.cell_value(i,2)
			VSI_ID=int(x)      
			OGHP_ID = sheet.cell_value(i,0)
			GE_Port = sheet.cell_value(i,1)
			x1= sheet.cell_value(i,3)
			Mul_VLAN = str(x1)
			Multicast_IP = sheet.cell_value(i,4)
			Multicast_IP_subnet=Multicast_IP.split("/")
			Multicast_IPClass=Multicast_IP_subnet[0].split(".")
			Mul_IP ='.'.join(Multicast_IPClass[0:3]+[str(int(Multicast_IPClass[-1])+1)])
			desc = sheet.cell_value(i,5)			
			f.write("\n")
			f.write (" Please find the below Configurations for "+OGHP_ID+'\n')
			f.write("**********************************MPS Configurations*********************************** \n")
			f.write("# \n")
			f.write( "vsi vsi_"+str(VSI_ID)+'\n')
			f.write(" pwsignal ldp  \n")
			f.write("  vsi-id "+str(VSI_ID)+'\n')
			f.write("  control-word enable \n")
			f.write("  peer "+str(NGE2_IP)+'\n')
			f.write("  peer "+str(NGE1_IP )+'\n')
			f.write("  protect-group vpls_"+str(VSI_ID)+'\n')
			f.write("   protect-mode pw-redundancy master \n ")  
			f.write("	reroute never  \n")      
			f.write("   peer "+str(NGE2_IP)+" preference 1  \n")
			f.write("   peer "+str(NGE1_IP)+" preference 2  \n")
			f.write("   traffic-statistics enable  \n")
			f.write(" mtu 2000  \n")
			f.write(" ignore-ac-state \n")
			f.write(" mac-learning disable  \n")
			f.write("#  \n")      
			f.write("interface "+GE_Port+'\n')
			f.write("negotiation auto \n")
			f.write("description "+desc+'\n')
			f.write("mtu 2000 \n")
			f.write("undo shutdown \n")
			f.write("undo dcn \n")
			f.write("# \n")
			MPS_Version = sheet.cell_value(50,7)
			if ( MPS_Version == 7 ) :
					f.write("interface "+GE_Port+dot+str(VSI_ID)+'\n')
					f.write("description "+desc+'\n')
					f.write("vlan-type dot1q "+str(VSI_ID)+'\n')
					f.write("statistic enable \n")
					f.write("l2 binding vsi vsi_"+str(VSI_ID)+'\n')
					f.write("trust upstream ttt-default inbound \n")
					f.write("trust upstream ttt-default outbound \n")
					f.write("trust 8021p outbound \n")
					if GE_Port == 'Gi0/2/0' or  GE_Port == 'Gi0/2/1' or GE_Port == 'Gi0/2/2' or  GE_Port == 'Gi0/2/3' or GE_Port == 'Gi0/3/0' or  GE_Port == 'Gi0/3/1' or GE_Port == 'Gi0/3/2' or  GE_Port == 'Gi0/3/3':
						f.write("qos-profile ttt-default-10gb outbound identifier none \n")
					else :
						f.write("qos-profile ttt-default-1gb outbound identifier none \n")
					f.write("# \n")
					if (len(Mul_VLAN) == 9 ):
						x1_class = x1.split("-")
						mv = x1_class[0:3]
						Mul_vlan1= mv[0]
						Mul_vlan2= mv[1]				
						Multicast_IP_subnet=Multicast_IP.split("-")
						Multicast_IPClass=Multicast_IP_subnet[0].split("/")
						M1 = Multicast_IPClass[0]
						M2 = Multicast_IPClass[1]				
						def hostip(Multicast_IP):
							Multicast_IP_subnet=Multicast_IP.split("/")
							Multicast_IPClass=Multicast_IP_subnet[0].split(".")
							Mul_IP ='.'.join(Multicast_IPClass[0:3]+[str(int(Multicast_IPClass[-1])+1)])
							return(Mul_IP)				
						Multicast_IP1 = hostip(M1)
						Multicast_IP2 = hostip(M2)
						f.write("interface "+GE_Port+dot+str(Mul_vlan1)+'\n')
						f.write("vlan-type dot1q "+str(Mul_vlan1)+'\n')
						f.write("mtu 2000 \n")
						f.write("description :r="+OGHP_ID+"/"+str(VSI_ID)+":sev=5:p=ttt:t=iptv: \n")
						f.write("ip binding vpn-instance iptv \n")
						f.write("ip address "+Multicast_IP1+" 255.255.255.252 \n") 
						f.write("statistic enable \n")
						f.write("pim sm \n")
						f.write("igmp enable \n")
						f.write("igmp version 3 \n")
						f.write("igmp timer query 10 \n")
						f.write("igmp group-policy acl-name non-glop-filter \n")				
						f.write("\n")
						f.write("interface "+GE_Port+dot+str(Mul_vlan2)+'\n')
						f.write("vlan-type dot1q "+str(Mul_vlan2)+'\n')
						f.write("mtu 2000 \n")
						f.write("description :r="+OGHP_ID+"/"+str(VSI_ID)+":sev=5:p=ttt:t=iptv: \n")
						f.write("ip binding vpn-instance iptv \n")
						f.write("ip address "+Multicast_IP2+" 255.255.255.252 \n") 
						f.write("statistic enable \n")
						f.write("pim sm \n")
						f.write("igmp enable \n")
						f.write("igmp version 3 \n")
						f.write("igmp timer query 10 \n")
						f.write("igmp group-policy acl-name non-glop-filter \n")
				
					else:
						Multicast_IP_subnet=Multicast_IP.split("/")
						Multicast_IPClass=Multicast_IP_subnet[0].split(".")
						Mul_IP ='.'.join(Multicast_IPClass[0:3]+[str(int(Multicast_IPClass[-1])+1)])
						Mul_VLAN_x1= int(x1)
						f.write("interface "+GE_Port+dot+str(Mul_VLAN_x1)+'\n')
						f.write("vlan-type dot1q "+str(Mul_VLAN_x1)+'\n')
						f.write("mtu 2000 \n")
						f.write("description :r="+OGHP_ID+"/"+str(VSI_ID)+":sev=5:p=ttt:t=iptv: \n")
						f.write("ip binding vpn-instance iptv \n")
						f.write("ip address "+Mul_IP+" 255.255.255.252 \n") 
						f.write("statistic enable \n")
						f.write("pim sm \n")
						f.write("igmp enable \n")
						f.write("igmp version 3 \n")
						f.write("igmp timer query 10 \n")
						f.write("igmp group-policy acl-name non-glop-filter \n")
					
			elif ( MPS_Version == 9 ) :
					f.write("interface "+GE_Port+dot+str(VSI_ID)+'\n')
					f.write("description "+desc+'\n')
					f.write("statistic enable \n")
					f.write("encapsulation dot1q-termination\n")
					f.write("dot1q termination vid "+str(VSI_ID)+'\n')				
					f.write("l2 binding vsi vsi_"+str(VSI_ID)+'\n')
					f.write("trust upstream ttt-default inbound \n")
					f.write("trust upstream ttt-default outbound \n")
					f.write("trust 8021p outbound \n")
					if GE_Port == 'Gi0/2/0' or  GE_Port == 'Gi0/2/1' or GE_Port == 'Gi0/2/2' or  GE_Port == 'Gi0/2/3' or GE_Port == 'Gi0/3/0' or  GE_Port == 'Gi0/3/1' or GE_Port == 'Gi0/3/2' or  GE_Port == 'Gi0/3/3':
						f.write("qos-profile ttt-default-10gb outbound identifier none \n")
					else :
						f.write("qos-profile ttt-default-1gb outbound identifier none \n")
					f.write("# \n")
					if (len(Mul_VLAN) == 9 ):
						x1_class = x1.split("-")
						mv = x1_class[0:3]
						Mul_vlan1= mv[0]
						Mul_vlan2= mv[1]				
						Multicast_IP_subnet=Multicast_IP.split("-")
						Multicast_IPClass=Multicast_IP_subnet[0].split("/")
						M1 = Multicast_IPClass[0]
						M2 = Multicast_IPClass[1]				
						def hostip(Multicast_IP):
							Multicast_IP_subnet=Multicast_IP.split("/")
							Multicast_IPClass=Multicast_IP_subnet[0].split(".")
							Mul_IP ='.'.join(Multicast_IPClass[0:3]+[str(int(Multicast_IPClass[-1])+1)])
							return(Mul_IP)				
						Multicast_IP1 = hostip(M1)
						Multicast_IP2 = hostip(M2)
						f.write("interface "+GE_Port+dot+str(Mul_vlan1)+'\n')
						f.write("encapsulation dot1q-termination\n")
						f.write("dot1q termination vid "+str(Mul_vlan1)+'\n')
						f.write("mtu 2000 \n")
						f.write("description :r="+OGHP_ID+"/"+str(VSI_ID)+":sev=5:p=ttt:t=iptv: \n")
						f.write("ip binding vpn-instance iptv \n")
						f.write("ip address "+Multicast_IP1+" 255.255.255.252 \n") 
						f.write("statistic enable \n")
						f.write("pim sm \n")
						f.write("igmp enable \n")
						f.write("igmp version 3 \n")
						f.write("igmp timer query 10 \n")
						f.write("igmp group-policy acl-name non-glop-filter \n")				
						f.write("\n")
						f.write("interface "+GE_Port+dot+str(Mul_vlan2)+'\n')
						f.write("vlan-type dot1q "+str(Mul_vlan2)+'\n')
						f.write("mtu 2000 \n")
						f.write("description :r="+OGHP_ID+"/"+str(VSI_ID)+":sev=5:p=ttt:t=iptv: \n")
						f.write("ip binding vpn-instance iptv \n")
						f.write("ip address "+Multicast_IP2+" 255.255.255.252 \n") 
						f.write("statistic enable \n")
						f.write("pim sm \n")
						f.write("igmp enable \n")
						f.write("igmp version 3 \n")
						f.write("igmp timer query 10 \n")
						f.write("igmp group-policy acl-name non-glop-filter \n")
					
					else:
						Multicast_IP_subnet=Multicast_IP.split("/")
						Multicast_IPClass=Multicast_IP_subnet[0].split(".")
						Mul_IP ='.'.join(Multicast_IPClass[0:3]+[str(int(Multicast_IPClass[-1])+1)])
						Mul_VLAN_x1= int(x1)
						f.write("interface "+GE_Port+dot+str(Mul_VLAN_x1)+'\n')
						f.write("encapsulation dot1q-termination\n")
						f.write("dot1q termination vid "+str(Mul_VLAN_x1)+'\n')
						f.write("mtu 2000 \n")
						f.write("description :r="+OGHP_ID+"/"+str(VSI_ID)+":sev=5:p=ttt:t=iptv: \n")
						f.write("ip binding vpn-instance iptv \n")
						f.write("ip address "+Mul_IP+" 255.255.255.252 \n") 
						f.write("statistic enable \n")
						f.write("pim sm \n")
						f.write("igmp enable \n")
						f.write("igmp version 3 \n")
						f.write("igmp timer query 10 \n")
						f.write("igmp group-policy acl-name non-glop-filter \n")
			
			f.write('\n')	  
			f.write("**********************************NGE 1 Configurations******************************************* \n")
			f.write("set interfaces ps"+str(NGE1_PS)+" description :r="+MPS2_name+":q="+GE_Port+dot+str(VSI_ID)+":v=ae"+str(ae_1)+":sev=5:t=pw: \n")
			f.write("set interfaces ps"+str(NGE1_PS)+" anchor-point "+str(lt_1)+'\n')
			f.write("set interfaces ps"+str(NGE1_PS)+" flexible-vlan-tagging \n")
			f.write("set interfaces ps"+str(NGE1_PS)+" auto-configure stacked-vlan-ranges dynamic-profile auto-stacked-pwht accept dhcp-v4 \n")
			f.write("set interfaces ps"+str(NGE1_PS)+" auto-configure stacked-vlan-ranges dynamic-profile auto-stacked-pwht accept pppoe \n")
			f.write("set interfaces ps"+str(NGE1_PS)+" auto-configure stacked-vlan-ranges dynamic-profile auto-stacked-pwht ranges "+str(VSI_ID)+'-'+str(VSI_ID)+",any \n")	
			f.write("set interfaces ps"+str(NGE1_PS)+" auto-configure stacked-vlan-ranges authentication packet-types dhcp-v4 \n")	
			f.write("set interfaces ps"+str(NGE1_PS)+" auto-configure stacked-vlan-ranges authentication packet-types pppoe \n")	
			f.write("set interfaces ps"+str(NGE1_PS)+" auto-configure stacked-vlan-ranges authentication username-include delimiter" ' ' '"@" \n')	
			f.write("set interfaces ps"+str(NGE1_PS)+" auto-configure stacked-vlan-ranges authentication username-include user-prefix pwht \n")	
			f.write("set interfaces ps"+str(NGE1_PS)+" auto-configure stacked-vlan-ranges authentication username-include interface-name \n")	
			f.write("set interfaces ps"+str(NGE1_PS)+" auto-configure stacked-vlan-ranges access-profile vlan-auth-access \n")	
			f.write("set interfaces ps"+str(NGE1_PS)+" auto-configure remove-when-no-subscribers \n")	
			f.write("set interfaces ps"+str(NGE1_PS)+" mtu 2022 \n")	
			f.write("set interfaces ps"+str(NGE1_PS)+" no-gratuitous-arp-request \n")	
			f.write("set interfaces ps"+str(NGE1_PS)+" unit 0 encapsulation ethernet-ccc \n")	
			f.write ('\n')	
			f.write("set protocols l2circuit neighbor "+MPS2_IP+" interface ps"+str(NGE1_PS)+dum+" virtual-circuit-id "+str(VSI_ID)+'\n')	
			f.write("set protocols l2circuit neighbor "+MPS2_IP+" interface ps"+str(NGE1_PS)+dum+" description :r="+MPS1_name+":q=vsi_"+str(VSI_ID)+":v=ae"+str(ae_1)+":sev=5:t=pw: \n")	
			f.write("set protocols l2circuit neighbor "+MPS2_IP+" interface ps"+str(NGE1_PS)+dum+" control-word \n")	
			f.write("set protocols l2circuit neighbor "+MPS2_IP+" interface ps"+str(NGE1_PS)+dum+" mtu 2000 \n")	
			f.write("set protocols l2circuit neighbor "+MPS2_IP+" interface ps"+str(NGE1_PS)+dum+" encapsulation-type ethernet-vlan \n")	
			f.write("set protocols l2circuit neighbor "+MPS2_IP+" interface ps"+str(NGE1_PS)+dum+" pseudowire-status-tlv hot-standby-vc-on \n")	
			f.write ('\n') 	
			f.write("set interfaces "+str(lt_1)+" hierarchical-scheduler implicit-hierarchy \n")	
			f.write("set routing-instances ttt_fttx_res system services dhcp-local-server group dhcp-ls interface ps"+str(NGE1_PS)+dum+'\n')	
			f.write("set class-of-service interfaces interface-set ps"+str(NGE1_PS)+" output-traffic-control-profile 10g-tcp \n")	
			f.write('\n')	  	
			f.write("**********************************NGE 2 Configurations******************************************* \n")	
			f.write("set interfaces ps"+str(NGE2_PS)+" description :r="+MPS2_name+":q="+GE_Port+dot+str(VSI_ID)+":v=ae"+str(ae_2)+":sev=5:t=pw: \n")	
			f.write("set interfaces ps"+str(NGE2_PS)+" anchor-point "+str(lt_2)+"\n")
			f.write("set interfaces ps"+str(NGE2_PS)+" flexible-vlan-tagging \n")	
			f.write("set interfaces ps"+str(NGE2_PS)+" auto-configure stacked-vlan-ranges dynamic-profile auto-stacked-pwht accept dhcp-v4 \n")	
			f.write("set interfaces ps"+str(NGE2_PS)+" auto-configure stacked-vlan-ranges dynamic-profile auto-stacked-pwht accept pppoe \n")	
			f.write("set interfaces ps"+str(NGE2_PS)+" auto-configure stacked-vlan-ranges dynamic-profile auto-stacked-pwht ranges "+str(VSI_ID)+'-'+str(VSI_ID)+",any \n")	
			f.write("set interfaces ps"+str(NGE2_PS)+" auto-configure stacked-vlan-ranges authentication packet-types dhcp-v4 \n")	
			f.write("set interfaces ps"+str(NGE2_PS)+" auto-configure stacked-vlan-ranges authentication packet-types pppoe \n")	
			f.write("set interfaces ps"+str(NGE2_PS)+" auto-configure stacked-vlan-ranges authentication username-include delimiter" ' ' '"@" \n')	
			f.write("set interfaces ps"+str(NGE2_PS)+" auto-configure stacked-vlan-ranges authentication username-include user-prefix pwht \n")	
			f.write("set interfaces ps"+str(NGE2_PS)+" auto-configure stacked-vlan-ranges authentication username-include interface-name \n")	
			f.write("set interfaces ps"+str(NGE2_PS)+" auto-configure stacked-vlan-ranges access-profile vlan-auth-access \n")	
			f.write("set interfaces ps"+str(NGE2_PS)+" auto-configure remove-when-no-subscribers \n")	
			f.write("set interfaces ps"+str(NGE2_PS)+" mtu 2022 \n")	
			f.write("set interfaces ps"+str(NGE2_PS)+" no-gratuitous-arp-request \n")	
			f.write("set interfaces ps"+str(NGE2_PS)+" unit 0 encapsulation ethernet-ccc \n")	
			f.write ('\n') 	
			f.write("set protocols l2circuit neighbor "+MPS2_IP+" interface ps"+str(NGE2_PS)+dum+" virtual-circuit-id "+str(VSI_ID)+'\n')	
			f.write("set protocols l2circuit neighbor "+MPS2_IP+" interface ps"+str(NGE2_PS)+dum+" description :r="+MPS1_name+":q=vsi_"+str(VSI_ID)+":v=ae"+str(ae_2)+":sev=5:t=pw: \n")	
			f.write("set protocols l2circuit neighbor "+MPS2_IP+" interface ps"+str(NGE2_PS)+dum+" control-word \n")	
			f.write("set protocols l2circuit neighbor "+MPS2_IP+" interface ps"+str(NGE2_PS)+dum+" mtu 2000 \n")	
			f.write("set protocols l2circuit neighbor "+MPS2_IP+" interface ps"+str(NGE2_PS)+dum+" encapsulation-type ethernet-vlan \n")	
			f.write("set protocols l2circuit neighbor "+MPS2_IP+" interface ps"+str(NGE2_PS)+dum+" pseudowire-status-tlv hot-standby-vc-on \n")	
			f.write ('\n')	
			f.write("set interfaces "+str(lt_2)+" hierarchical-scheduler implicit-hierarchy \n")	
			f.write("set routing-instances ttt_fttx_res system services dhcp-local-server group dhcp-ls interface ps"+str(NGE2_PS)+dum+'\n')	
			f.write("set class-of-service interfaces interface-set ps"+str(NGE2_PS)+" output-traffic-control-profile 10g-tcp \n")
			NGE1_PS += 1
			NGE2_PS += 1
			i += 1
			

f.write("\n")
f.write("Please find the below Command line for verification \n")
f.write("screen-length 0 temporary \n")
f.write("display interface description | no-more \n")
f.write("display interface brief | no-more \n")
f.write("display vsi services all\n")
f.write("display vsi peer-info \n ")
f.write("\n")
f.write("\n")
j = 1
while ( j <= var ) :
	x = sheet.cell_value(j,2)
	V_ID=int(x)      
	Gi_Port = sheet.cell_value(j,1)
	f.write("display interface "+str(Gi_Port)+" | no-more\n")
	f.write("display optical-module extend information interface " +str(Gi_Port)+ "\n")
	f.write("display ip routing-table vpn-instance iptv | include " +str(Gi_Port)+ "\n")
	f.write("display traffic-statistics vsi vsi_" +str(V_ID)+ "\n")
	f.write("display vsi name vsi_"+str(V_ID)+" peer-info\n")
	f.write("\n")
	f.write("\n")
	j += 1
	