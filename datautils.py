'''Data utility functions for use in data mapping'''

def dataframe_to_nested_dict(df):
	drec = dict()
	ncols = df.values.shape[1]
	for line in df.values:
		d = drec
		for j, col in enumerate(line[:-1]):
			if not col in d.keys():
				if j != ncols - 2:
					d[col] = {}
					d = d[col]
				else:
					d[col] = line[-1]
			else:
				if j != ncols - 2:
					d = d[col]
	return drec