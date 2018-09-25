from binaryninja import *

def get_address_from_sig(bv, sigList):
	br = BinaryReader(bv)

	result = 0

	for search_func in bv.functions:
		br.seek(search_func.start)

		while bv.get_functions_containing(br.offset) != None and search_func in bv.get_functions_containing(br.offset):
			found = True
			for entry in sigList:
				byte = br.read8()
				if entry != byte and entry != '?':
					found = False
					break
			if found:
				result = br.offset
				break
		if result != 0:
			break

	return result

def get_amount_of_hits(bv, sigList):
	br = BinaryReader(bv)

	result = 0

	if len(sigList) == 0:
		return result

	for search_func in bv.functions:
		br.seek(search_func.start)

		while bv.get_functions_containing(br.offset) != None and search_func in bv.get_functions_containing(br.offset):
			found = True
			for entry in sigList:
				byte = br.read8()
				if entry != byte and entry != '?':
					found = False
					break
			if found:
				result += 1

	return result

def SigMakerFind(bv):
	user_input = get_text_line_input("Find Signature...\t\t\t\t\t", "SigMaker")

	if user_input == None:
		return

	sig = user_input.split(" ")

	sigList = []

	for value in sig:
		if value == '?':
			sigList.append(value)
		elif value != '?' and value != '':
			sigList.append(int(value,16))

	result = get_address_from_sig(bv, sigList)

	if result != 0:
		new_result = result - len(sigList)
		print 'Found:\t' + format(new_result, '16x') + '\nInside:\t' + format(bv.get_functions_containing(new_result)[0].start, '16x') + '\nSignature:\t' + user_input + '\nHits:\t' + format(get_amount_of_hits(bv,sigList), '10x')
		show_message_box("Search result",'Address:\t' + format(new_result, '16x') + '\n' + 'Function:\t' + format(bv.get_functions_containing(new_result)[0].start, '16x') + '\n', MessageBoxButtonSet.OKButtonSet, MessageBoxIcon.InformationIcon)
	else:
		print 'Found:\t' + 'None' + '\nInside:\t' + 'None' + '\nSignature:\t' + user_input
		show_message_box("Search result",'Address:\t' + 'NONE' + '\n' + 'Function:\t' + 'NONE' + '\n', MessageBoxButtonSet.OKButtonSet, MessageBoxIcon.InformationIcon)

	return

def get_sig_from_address(bv, addr, first_try = True):
	
	if addr == None:
		return

	br = BinaryReader(bv)

	sigList = []

	br.seek(addr)

	org_func = bv.get_functions_containing(br.offset)

	if org_func == None:
		return sigList

	while get_amount_of_hits(bv,sigList) != 1:
		
		if len(sigList) > 24 and first_try:
			return get_sig_from_address(bv, org_func[0].start, False)
		elif not first_try:
			return sigList
		
		containing = bv.get_functions_containing(br.offset)

		if (containing == None or containing[0] != org_func[0]) and first_try:
			return get_sig_from_address(bv, org_func[0].start, False)
		elif not first_try:
			return sigList

		target_func = containing[0]
		constants = target_func.get_constants_referenced_by(br.offset)

		if len(constants) != 0 and constants[0].pointer:
			length = bv.get_instruction_length(br.offset) - 4
			for x in range(length):
				sigList.append(br.read8())
			for x in range(4):
				sigList.append('?')
				br.offset += 1
		else:
			length = bv.get_instruction_length(br.offset)
			for x in range(length):
				sigList.append(br.read8())

	return sigList		
	
def convert_to_hex_string(value):
	str_value = (hex(value).rstrip("L").lstrip("0x").upper() or "0")
	if len(str_value) == 1:
		return '0' + str_value
	else:
		return str_value

def convert_to_string(sigList):
	
	if len(sigList) == 0:
		return "NONE"

	str_sig = ""
	count = 0
	for entry in sigList:
		if entry != '?':
			str_sig += convert_to_hex_string(entry)
		else:
			str_sig += entry
		count += 1
		if count != len(sigList):
			str_sig += ' '

	return str_sig

def SigMakerCreate(bv, addr):

	show_message_box("Create Signature","It can take a while for the plugin to finish.\nPress 'OK' if you want to start.", MessageBoxButtonSet.OKButtonSet, MessageBoxIcon.InformationIcon)

	sigList = get_sig_from_address(bv, addr)

	str_sig = convert_to_string(sigList)
	print 'Created Signature:\t' + str_sig
	show_message_box("Created Signature",'Address:\t' + format(get_address_from_sig(bv, sigList) - len(sigList), '16x') + '\n' + 'Signature:\t' + str_sig + '\n', MessageBoxButtonSet.OKButtonSet, MessageBoxIcon.InformationIcon)



PluginCommand.register("[SigMaker] Find Signature", "", SigMakerFind)
PluginCommand.register_for_address("[SigMaker] Create Signature", "", SigMakerCreate)

