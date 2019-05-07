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

def make_nutrient_frequency_file(python_database, nutrient_codes):
	nutrient_frequency = dict()
	for nutrient_code in nutrient_codes:
		nutrient_frequency[nutrient_code] = 0

	for id, product in python_database.items():
		for nutrient_code in nutrient_codes:
			try:
				throw = product.nutrients[nutrient_code].value
				nutrient_frequency[nutrient_code] += 1
			except:
				pass
	
	nutrient_frequency_list = []
	for key, value in zip(nutrient_frequency.keys(), nutrient_frequency.values()):
		nutrient_frequency_list.append([key, value])

	nutrient_frequency_list = sorted(nutrient_frequency_list, key = lambda nutrient_frequency_list: nutrient_frequency_list[1], reverse = True)
	writeJSON(nutrient_frequency_list, "nutrient_frequency_list.JSON")

def make_adjusted_nutrient_code_file():
	nutrient_frequency_list = sorted(readJSON("nutrient_frequency_list.JSON"), key = lambda nutrient_frequency_list: nutrient_frequency_list[0])
	nutrient_code_list = []
	for nutrient_code in nutrient_frequency_list:
		nutrient_code_list.append(nutrient_code[0])

	f = open(nutrient_codes_filename, 'w+')
	g = open("all_nutrient_codes.txt", 'r+')
	for line in g.readlines():
		if int(line[0:3]) in nutrient_code_list:
			f.write(line)
	g.close()
	f.close()

def get_X(python_database, nutrient_codes):
	X = []
	for id, product in python_database.items():
		x = []
		for nutrient_code in nutrient_codes:
			try:
				x.append(product.nutrients[nutrient_code].value)
			except:
				x.append(0.0)
		X.append(x)
	return X

def find_k(X, low_cluster_limit, high_cluster_limit):
	x = range(low_cluster_limit, high_cluster_limit+1)
	y = []
	items_processed = 0.0
	total_items = len(x)

	print "Calculating k-values..."
	for k in x:
		km = KMeans(n_clusters = k, n_init = 100, n_jobs = -2)
		km.fit(X)
		y.append(km.inertia_)
		# Progress Indicator
		items_processed = items_processed + 1
		progress_percent = (items_processed/total_items)*100.0
		if items_processed%1 == 0:
			print ("%05.2f%%" % progress_percent)
	print "Done\n"

	plt.xlabel("k-Clusters")
	plt.ylabel("SSE")
	plt.title("Nutrients K-Means")
	plt.plot(x,y)
	plt.grid(b=True, which='both')
	plt.show()

def run_kmeans(python_database, nutrient_codes, low_cluster_limit, high_cluster_limit):
	X = get_X(python_database, nutrient_codes)
	find_k(X, low_cluster_limit, high_cluster_limit)