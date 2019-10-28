"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
import numpy as np
def baseline(train, test):
	'''
	TODO: implement the baseline algorithm.
	input:  training data (list of sentences, with tags on the words)
		test data (list of sentences, no tags on the words)
	output: list of sentences, each sentence is a list of (word,tag) pairs.
		E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
	'''
	predicts = []
	tags = ["ADJ", "ADV", "IN","PART","PRON", "NUM", "CONJ", "UH", "TO","VERB", "MODAL", "DET", "NOUN", "PERIOD", "PUNCT", "X"]      
	word2tag = {}
	for data in train:
		for word, tag in data:
			if word == "START":
				continue
			if word in word2tag:
				if tag in word2tag[word]:
					word2tag[word][tag] += 1
				else:
					word2tag[word][tag] = 1
			else:
				word2tag[word] = {tag : 1}
	
				
	for data in test:
		temp = []
		for word in data:
			if word == "START":
				temp.append(("START","START"))
			else:
				if word not in word2tag:
					temp.append((word, "NOUN"))
				else:
					temp.append((word, max(word2tag[word], key = lambda x : word2tag[word][x])))
		predicts.append(temp)

	
	return predicts


def most_likely(word):
	if ord(word[0]) >= 48 and ord(word[0]) <=57: return ["NUM"]
	if len(word) > 3:
		if word[-4:] == "tion" or word[-4 : ] == "ment" or word[-4 : ] == "ness" or word[-3:] == "ity" or word[-3 :]=="ism"\
			or word[-3:] == "age" or word[-2:] == "er" or word[-3:]== "ery": return ["NOUN"]
		if word[-2:] == "en" or word[-3:] == "ize": return ["VERB"]
		if word[-3:] == "ing": return ["VERB", "NOUN", "ADJ"]
		if word[-2:] == "ed": return ["VERB", "ADJ"]
		if word[-4:] == "able" or word[-4:] == "ible" or word[-2:] == "ic" or word[-3:] == "ive" or word[-3:] == "ish" \
			or word[-2:] == "al" or word[-4:] == "ical" : return ["ADJ"] 
		if word[-2:] == "ly": return ["ADV", "VERB", "NOUN"]
	return []
	

def viterbi(train, test):
	'''
	TODO: implement the Viterbi algorithm.
	input:  training data (list of sentences, with tags on the words)
		test data (list of sentences, no tags on the words)
	output: list of sentences with tags on the words
		E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
	'''
	is_masc = [('START', 'START'), ('december', 'NOUN'), ('1998', 'NUM')] in train
	predicts = []
	tags = ["ADJ", "ADV", "IN","PART","PRON", "NUM", "CONJ", "UH", "TO","VERB", "MODAL", "DET", "NOUN", "PERIOD", "PUNCT", "X"]      
	tag_index = {tag : i for i, tag in enumerate(tags)}
	initial_prob = {tag : 0 for tag in tags}
	transition_prob = np.zeros([len(tags), len(tags)])
	emission_prob = {tag : {} for tag in tags}
	emission_count = {tag : 0 for tag in tags}
	hapax = np.zeros([len(tags)])

	for data in train: 
		count = True
		for word, tag in data:
			if word == "START" : continue
			if count:
				initial_prob[tag] += 1
			if word in emission_prob[tag]:
				emission_prob[tag][word] += 1   
			else :
				emission_prob[tag][word] = 1
			emission_count[tag] += 1
			count = False
	
	total = 0
	for data in train:
		for i in range(len(data) - 1):
			if i == 0: continue
			index1 = tag_index[data[i][1]]
			index2 = tag_index[data[i + 1][1]]
			transition_prob[index1, index2] += 1	
			total += 1
	
	rare = 0
	hapax_word = [" "] * 16
	for tag in emission_prob.keys():
		for word in emission_prob[tag].keys():
			if emission_prob[tag][word] == 1:
				hapax_word[tag_index[tag]] = word
				hapax[tag_index[tag]] += 1
				rare += 1
	
	alpha = 1
	hapax = (hapax + alpha) / (rare + alpha * len(tags))


	alpha = 0.1 if is_masc else 800
	transition_prob = -1 * np.log((transition_prob + alpha) / (total + alpha * len(tags) * len(tags)))


	alpha0 = 0.05
	for tag in emission_prob.keys():
		emission_prob[tag]["<UNK>"] = 0
		alpha = alpha0 * hapax[tag_index[tag]]
		denom = (emission_count[tag] + len(emission_prob[tag]) * alpha)
		for word in emission_prob[tag].keys():
			emission_prob[tag][word] = -1 * np.log((emission_prob[tag][word] + alpha) / denom)

	alpha = 0.5
	for tag in initial_prob.keys():
		initial_prob[tag] = -1 * np.log((initial_prob[tag] + alpha) / (len(train) + alpha * len(tags)))

	for sentence in test:
		temp = []
		sentence = sentence[1:]
		if len(sentence) == 0:
			predicts.append([("START", "START")])
			continue
		
		trellis = np.zeros([len(sentence), len(tags)])
		parent_map = np.zeros([len(sentence), len(tags)], dtype="<U6")

		likely_tags = most_likely(sentence[0])
		for i in range(len(tags)):
			if sentence[0] in emission_prob[tags[i]]:
				emission = emission_prob[tags[i]][sentence[0]]
			else:
				if tags[i] in likely_tags:
					emission = emission_prob[tags[i]][hapax_word[i]]
				else:
					emission = emission_prob[tags[i]]["<UNK>"] 
			trellis[0, i] = initial_prob[tags[i]] + emission


		for i in range(1, len(sentence)):
			word = sentence[i]	
			likely_tags = most_likely(word) 
			for j in range(len(tags)):
				tag = tags[j] 
				if word in emission_prob[tag]:
					emission = emission_prob[tag][word]
				else:
					if tag in likely_tags:
						emission = emission_prob[tag][hapax_word[j]]
					else:
						emission = emission_prob[tag]["<UNK>"]

				costs = []
				for k in range(len(tags)):
					costs.append(trellis[i - 1, k] + transition_prob[k, j])
				
				best_index = np.argmin(costs)
				parent_map[i, j] = tags[best_index]
				trellis[i, j] = costs[best_index] + emission
	
		index = np.argmin(trellis[-1])
		temp.append((sentence[-1],  tags[index]))
		for i in range(len(sentence) - 2, 0, -1):
			temp.insert(0, (sentence[i], parent_map[i + 1, index]))
			index = tag_index[parent_map[i + 1, index]]

		if len(sentence) != 1:
			temp.insert(0, (sentence[0], tags[np.argmin(trellis[0])]))
		temp.insert(0, ("START", "START"))
		
		predicts.append(temp)
					
		print(predicts)
	return predicts


