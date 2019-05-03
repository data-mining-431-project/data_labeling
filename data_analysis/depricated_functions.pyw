"""
Depricated Functions to be used in data_analysis.py
"""

def plot_nutrients(python_database, x_code, color = None):
	x_val_list = []
	need_label = True
	x_label = ""
	normalize_to_kcal = True
	per_kcal = 1

	# Loops through the Product Database and prepares a list of the x and y values
	for id, product in python_database.iteritems():
		try:
			if product.nutrients[x_code] != None:
				if normalize_to_kcal:
													# Nutrient Value per x kcals
					x_val_list.append(product.nutrients[x_code].value * per_kcal / product.nutrients[208].value)
				else:
													 # Nutrient Value
					x_val_list.append(product.nutrients[x_code].value)
			if need_label:
					x_label = product.nutrients[x_code].nutrient_type
					need_label = False
		except:
			pass

	# Sorting Data...
	print "Sorting Data..."
	x_val_list.sort()
	print "Done\n"

	# Graphing Data...
	print "Graphing Data..."

	# Converts the list to a np.array for plotting
	x_val_array = np.array(x_val_list)
		
	x_mean = np.mean(x_val_array)
	x_std = np.std(x_val_array)
	x_pdf = stats.norm.pdf(x_val_array, x_mean, x_std)
	plt.plot(x_val_array, x_pdf, color = color, label = x_label)

	print "Done\n"

def plot_all_nutrients(python_database, nutrient_codes):
	plt.figure(1)
	i = 0
	while i < len(nutrient_codes):
		print ("Plot %d of %d" % (i + 1, (len(nutrient_codes))) )
		plt.subplot(8, 8, i+1)
		plot_nutrients(python_database, nutrient_codes[i], color = 'r')
		i+=1
	plt.tight_layout()

def get_X_2D(python_database, nutrient_code_1, nutrient_code_2):
	nutrient_1_values = []
	nutrient_2_values = []
	X = []

	for id, product in python_database.items():
		try:
			nutrient_1_values.append(product.nutrients[nutrient_code_1].value/product.nutrients[208].value)
			nutrient_2_values.append(product.nutrients[nutrient_code_2].value/product.nutrients[208].value)
		except:
			pass
	nutrient_1_values = preprocessing.scale(np.array(nutrient_1_values)).tolist()
	nutrient_2_values = preprocessing.scale(np.array(nutrient_2_values)).tolist()

	for nutrient_value_1, nutrient_value_2 in zip(nutrient_1_values, nutrient_2_values):
		# Cull Outliers, anything greater than 3 sigma
		if nutrient_value_1 <= 3.0 and nutrient_value_2 <= 3.0:
			X.append([nutrient_value_1, nutrient_value_2])
	X = np.array(X)

	return X

def cluster_nutrient_2D(python_database, num_clusters, nutrient_code_1, nutrient_code_2):
	X = get_X_2D(python_database, nutrient_code_1, nutrient_code_2)
	km = KMeans(n_clusters = num_clusters, n_init = 50)

	print "Clustering Data..."
	km.fit(X)
	print "Done\n"

	folder_name_1 = ""
	folder_name_2 = ""
	for id, product in python_database.items():
		try:
			folder_name_1 = dir_path + "\\Nutrient_Data\\" + product.nutrients[nutrient_code_1].nutrient_type + ' vs ' + product.nutrients[nutrient_code_2].nutrient_type
			folder_name_2 = dir_path + "\\Nutrient_Data\\" + product.nutrients[nutrient_code_1].nutrient_type + ' vs ' + product.nutrients[nutrient_code_2].nutrient_type + '\\' + "clusters_" + str(num_clusters)
			break
		except:
			pass


	if not os.path.isdir(folder_name_1):
		os.mkdir(folder_name_1)
		os.mkdir(folder_name_2)
	else:
		if not os.path.isdir(folder_name_2):
			os.mkdir(folder_name_2)
	items_processed = 0.0
	total_items = len(km.labels_)
	print "Saving Data..."
	cluster_list = []
	for idx, cls in enumerate(km.labels_):
		cluster_list.append([cls, [X[idx][0], X[idx][1]]])
	sorted(cluster_list, key=lambda cluster: cluster[0])
	f = []
	i = 0
	while i < num_clusters:
		f.append(open((folder_name_2 + "\\" + 'cluster-{0}.txt').format(i), 'a'))
		i+=1
	for cluster in cluster_list:
		f[cluster[0]].write(json.dumps([cluster[1][0], cluster[1][1]]) + '\n')
		# Progress Indicator
		items_processed = items_processed + 1
		progress_percent = (items_processed/total_items)*100.0
		if items_processed%5000 == 0:
			print ("%05.2f%%" % progress_percent)
	for file in f:
		file.close()
	print "Done\n"

def plot_cluster(python_database, num_clusters, nutrient_code_1, nutrient_code_2):
	folder_name = ""
	x_label = ""
	y_label = ""
	for id, product in python_database.items():
		try:
			x_label = product.nutrients[nutrient_code_1].nutrient_type
			y_label = product.nutrients[nutrient_code_2].nutrient_type
			folder_name = dir_path + "\\Nutrient_Data\\" + product.nutrients[nutrient_code_1].nutrient_type + ' vs ' + product.nutrients[nutrient_code_2].nutrient_type + '\\' + "clusters_" + str(num_clusters)
			break
		except:
			try:
				x_label = product.nutrients[nutrient_code_2].nutrient_type
				y_label = product.nutrients[nutrient_code_1].nutrient_type
				folder_name = dir_path + "\\Nutrient_Data\\" + product.nutrients[nutrient_code_2].nutrient_type + ' vs ' + product.nutrients[nutrient_code_1].nutrient_type + '\\' + "clusters_" + str(num_clusters)
				break
			except:
				pass
	file_clusters = []
	for i in range(num_clusters):
		file_clusters.append(readJSON((folder_name + "\\" + 'cluster-{0}.txt').format(i)))

	clusters = []
	for file_cluster in file_clusters:
		i_cluster = []
		value_list_1 = []
		value_list_2 = []
		for entry in file_cluster:
			value_list_1.append(entry[0])
			value_list_2.append(entry[1])
		i_cluster.append(value_list_1)
		i_cluster.append(value_list_2)
		clusters.append(i_cluster)

	colors = cm.rainbow(np.linspace(0, 1, len(clusters)))
	for cluster, c in zip(clusters, colors):
		plt.scatter(cluster[0], cluster[1], color = c)
	plt.xlabel(x_label)
	plt.ylabel(y_label)

def cluster_all_nutrients(python_database, low_cluster_limit, high_cluster_limit, nutrient_code_1, nutrient_code_2):
	for i in range(low_cluster_limit, high_cluster_limit + 1):
		cluster_nutrient_2D(python_database, i, nutrient_code_1, nutrient_code_2)

def plot_all_clusters(python_database, low_cluster_limit, high_cluster_limit, nutrient_code_1, nutrient_code_2, figure_number):
	plt.figure(figure_number)
	j = 1
	for i in range(low_cluster_limit,high_cluster_limit + 1):
		plt.subplot(int(math.ceil(math.sqrt(high_cluster_limit-low_cluster_limit))), int(math.ceil(math.sqrt(high_cluster_limit-low_cluster_limit))), j)
		plot_cluster(python_database, i, nutrient_code_1, nutrient_code_2)
		j+=1

def cluster_all_data(python_database, nutrient_codes, low_cluster_limit, high_cluster_limit):
	i = 0
	j = 1
	while i < len(nutrient_codes) - 1:
		while j < len(nutrient_codes):
			cluster_all_nutrients(python_database, low_cluster_limit, high_cluster_limit, nutrient_codes[i], nutrient_codes[j])
			j+=1
		i+=1
		j=i+1
