from datamapper import DataMapper
import json

config = {
	"input": {
		"datasets": [
			# Imports datasets, merges and flattens them to DataFrame format
			{
				"filepath": "./data/input.xlsx",
				# "multi_indices": ['t', 'x', 'rr'],
			}
		]
	},
	"map": {
		# Does the heavy lifting
		"column_apply": [
			("rr", lambda row: "RiverReach_{0}_{1}_{2}".format(int(row['x']), int(row['y']), int(row['rr']))),
			("x", lambda row: "GridCell_{0}_{1}".format(int(row['x']), int(row['y'])))
		],
		"drop_columns": ['y']
		# "use_column_as_dimension": {
		# 	"dimension_column": "t",
		# 	"array_column": "total_m_np"
		# 	"fill_value": 0
		# }
	},
	"output": {
		# Splits up the merged DataFrame (if required) and outputs
		"datasets": [
			{
				"filepath": "./data/output.json",
				"orient": "nested"
			}
		]
	}
}

dm = DataMapper(config)
dm.map()

with open('c:/code/datamapper/output.json', 'r') as json_file:
	print(json.dumps(json.load(json_file), indent=2))
