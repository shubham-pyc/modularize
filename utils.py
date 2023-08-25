def make_import_statement(alias):
	value = None
	if alias.asname is not None:
		value = f"{alias.name} as {alias.asname}"
	else:
		value = alias.name
	return value

def make_from_import_statement(node):
	module = node.module
	full_import = f"{module} import ("
	buffer = set()
	for alias in node.names:
		value = make_import_statement(alias)
		buffer.add(value)
	
	full_import += ",".join(buffer) +")"
	return full_import

