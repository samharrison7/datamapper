import os
import sys
import json
import pandas as pd
import datautils as du
import pprint


class DataMapper:

	def __init__(self, config):
		self.config = config
		self.input_dataframes = []
		self.merged_dataframe = None
		self.output_dataframes = []

	def map(self):
		"""Map input dataset(s) to output dataset(s), based on config"""
		self.parse_input_datasets()                 # Convert input datasets to one DataFrame
		self.parse_merged_dataset()                 # Perform any specified actions on the merged DataFrame
		self.parse_output_datasets()                # Split the merged DataFrame and output

	def parse_input_datasets(self):
		"""Convert input datasets to one DataFrame"""

		# Loop through input datasets in config
		for key, input_dataset in enumerate(self.config['input']['datasets']):
			# Try and figure out file type by extension
			extension = os.path.splitext(input_dataset['filepath'])[1].lower()
			# Use the correct Pandas read method based on extension
			if extension in ['.xls', '.xlsx', '.xlsm']:
				self.input_dataframes.append(pd.read_excel(input_dataset['filepath']))
			elif extension in ['.csv', '.sv']:
				self.input_dataframes.append(pd.read_csv(input_dataset['filepath']))
			else:
				# We currently don't support this type
				print("File type of input file {0} could not be determined. "
					  "File type may not be supported. Ignoring this file.".format(input_dataset['filepath']))

		# Merge the datasets
		# TODO Provide more config options from this, based on https://pandas.pydata.org/pandas-docs/stable/merging.html
		self.merged_dataframe = pd.concat(self.input_dataframes)

	def parse_merged_dataset(self):
		"""Perform any specified actions on merged DataFrame"""

		# Loop through input datasets in config
		# TODO Allow any Pandas function to be specified in config such that it is called on the DataFrame here
		# Altering columns based on applied functions
		if 'column_apply' in self.config['map']:
			for column, apply_func in self.config['map']['column_apply']:
				self.merged_dataframe[column] = self.merged_dataframe.apply(apply_func, axis=1)

		# Columns to drop
		if 'drop_columns' in self.config['map']:
			self.merged_dataframe = self.merged_dataframe.drop(columns=self.config['map']['drop_columns'])

		# Columns to convert to dimensions of another column
		# TODO Think about how to get this working
		# if 'use_column_as_dimension' in self.config['map']:
		# 	dimension_column = self.config['map']['use_column_as_dimension']['dimension_column']
		# 	array_column = self.config['map']['use_column_as_dimension']['array_column']
		# 	other_columns = [column for column in self.merged_dataframe.columns.tolist()
		# 					 if column not in [dimension_column, array_column]]
		# 	dimension_length = len(self.merged_dataframe[dimension_column].drop_duplicates())
		# 	# Create new dataframe which should have the correct number of rows after removing
		# 	# dimension column and using it as the dimension of array column
		# 	new_dataframe = self.merged_dataframe.loc[self.merged_dataframe[dimension_column] == 1]
		# 	# Convert scalar to array
		# 	# new_dataframe[array_column] = new_dataframe.apply(lambda r: [r[array_column]], axis=1)
		#
		# 	for i in range(2, dimension_length + 1):
		# 		rows_to_merge = self.merged_dataframe.loc[self.merged_dataframe[dimension_column] == i]
		#
		# 		for dim, row in rows_to_merge.iterrows():
		# 			new_dataframe[array_column] = new_dataframe.apply(lambda r: r[array_column].append(row[array_column]), axis=1)
		# 	print(new_dataframe)
		# 	sys.exit()

	def parse_output_datasets(self):
		"""Split the merged DataFrame into desired datasets and output based on config"""

		if len(self.config['output']['datasets']) > 1:
			print("More than one output dataset not currently supported. Sorry!")
		else:
			# Try and figure out file type by extension
			for key, output_dataset in enumerate(self.config['output']['datasets']):
				extension = os.path.splitext(output_dataset['filepath'])[1].lower()
				if extension == '.json':
					# If it's JSON, what orientation should dataset by output in? In addition to
					# Pandas options, "nested" converts to hierarchical JSON structure
					if output_dataset['orient'] == 'nested':
						nested_dict = du.dataframe_to_nested_dict(self.merged_dataframe)
						with open(output_dataset['filepath'], 'w') as json_file:
							json.dump(nested_dict, json_file)
					else:
						print("JSON output file 'orient' option {0} not supported.".format(dataset) )
				else:
					# We currently don't support this type
					print("File type of output file {0} could not be determined. "
						  "File type may not be supported.".format(self.config['output']['datasets'][0]['filepath']))
