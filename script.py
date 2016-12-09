import re
import os
import jieba
import csv
from bs4 import BeautifulSoup as bs


path_train = 'c:/users/yingying.zhu/documents/dataset/train'
#class get_info(s):
def list_to_str(l):
	res = ''
	for s in l:
		res += str(s)
		res += ' '
	return res

def get_age(s):
	'''从字符串s中提取年龄'''
	age_re = r'(\d+)(\s?岁)'
	return re.search(age_re, s).group(1)


def modified(word):
	#去掉字符串中的\xa0, 以免报错
	word_xa0 = word.replace('\xa0', '')
	word_xa1 = word_xa0.replace('？', '')

	#把字符串中的中文冒号替换成英文冒号
	word_res = word_xa1.replace('：', ':')
	return word_res


def get_patinet_info(patient_num):
	
	txt_dict_tmp = []
	user_dict_tmp = []
	user_dic = []

	patient_id = int(patient_num)

	csvfile = open(str(patient_num)+'.csv', 'w')

	writer = csv.writer(csvfile)

	path_patient = path_train + '/' + patient_num

	head_dict = {}
	head_list = [] 

	for file_type in os.listdir(path_patient):
		filename = path_patient + '/' + file_type
		soup = bs(open(filename), 'html.parser')


		if ('病程记录' in modified(soup.get_text()) and '查房' not in modified(soup.get_text())):
			tag_list = []
			res_list = []
			item = soup.p
			name_hospital = item.text
			

			# csvfile = open('result.csv', 'w')
			# writer = csv.writer(csvfile)

			#把文件中的信息整理成一个list
			#list的第一个元素是医院名称
			tag_list.append(item)
			res_list.append(name_hospital)
			for sibling in item.next_siblings:
			    try:
			        if len(sibling.text.strip()) != 0:
			            name = sibling.text.strip()
			            tag_list.append(sibling)
			            res_list.append(name)
			    except AttributeError:
			        pass  


			#处理第一行数据, 即病人的相关信息, 这是一个列表
			patient_info = [word for word in res_list[1].split('\n') if word != '']

			head_dict['医院名称'] = name_hospital
			if '医院名称' not in head_list:
				head_list.append('医院名称')

			i = 0
			while i in range(len(patient_info)):
				head_dict[patient_info[i]] = patient_info[i+1]
				if patient_info[i] not in head_list:
					head_list.append(patient_info[i])
				i += 2

			#check ID, 检查病人ID是否正确
			def check_patient_num():
				if int(head_dict['ID号']) != patient_id:
					pass

			#处理第二行信息, 即就诊时间, 这是一个列表
			time_info = res_list[2].split()
			head_dict['病历时间'] = time_info.pop(0)
			if '病历时间' not in head_list:
				head_list.append('病历时间')
			if len(time_info) > 0 :
				head_dict['报告名称'] = time_info
				if '报告名称' not in head_list:
					head_list.append('报告名称')

			#入院时间
			add_info = modified(res_list[3])
			writer.writerow([add_info])

			# #主要内容
			# case_char = modified(res_list[4])
			# writer.writerow([case_char])

			#后面的部分整理为字典格式, key为报告中的黑体字, 键值为对应的内容
			dic = {}
			key_list = []
			j = -1
			for i in range(4, len(tag_list)):
			    try:
			        if 'bold' in tag_list[i].next_element['style']:
			            sent_tmp = modified(res_list[i]).split(':')
			            key_list.append(sent_tmp[0])
			            j += 1
			            dic[key_list[j]] = sent_tmp[1:]
			        else:
			            try:
			                value = modified(res_list[i])
			                if len(value) > 0:
			                    dic[key_list[j]].append(value)
			            except IndexError:
			                writer.writerrow(modified(res_list[i]))
			    except AttributeError:
			    	#print (patient_num + '	' + file_type + '	' + str(i))
			    	pass



			for key in key_list:
			    writer.writerow([key, dic[key]])
			    if '初步诊断' in key:
			    	user_dict_tmp.extend(dic[key])
			    elif '病例特点' in key:
			    	txt_dict_tmp.append(list_to_str(dic[key]))



			    
			#医生信息
			doc_info = modified(res_list[-2])
			writer.writerow([doc_info])


		else:
			continue


	for ley in head_list:
		writer.writerow([ley, [head_dict[ley]]])

	csvfile.close()

	#把初步诊断结果中的词语做成一个列表, 这里的句子结构简单, 可以提取关键词添加到词典中去
	match_treat = r'(\d.\d?)?(\S*)(？$)?'
	user_dic = [word for word in user_dict_tmp if len(word) > 0]
	final_dic = [re.search(match_treat, word).group(2) for word in user_dic]
	# print(head_dict['姓名'], patient_num)
	# print(final_dic)

	# print('\n')
	#print(txt_dict_tmp)

	return final_dic, txt_dict_tmp


patient = []
my_dic = []
fr = open('jilu.txt', 'w')
for num in os.listdir(path_train):

	final_dict, txt_dict = get_patinet_info(str(num))
	my_dic.extend(final_dict)
	print(txt_dict)
	[fr.write(s + '\n') for s in txt_dict] 
	fr.write('\n\n\n\n')
	patient.extend(txt_dict)


fr.close()
#print(set(my_dic))
print(patient)


