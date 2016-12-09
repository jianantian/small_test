#fr = open(filename)
stop_dict = ['的','到','因','于'] 

def modified(word):
	#去掉字符串中的\xa0, 以免报错
	word_x0 = word.replace('\xa0', '')
	word_x1 = word_x0.replace('\xe7', '')
	return word_x1


def trans(s):
	for char in s:
		if char in stop_dict:
			s = s.replace(char, ' ')
	return s

def cut(s):
	
	key_dict = {}
	start_pos = 0

	while ' ' in s[start_pos:]:
		end_pos = s[start_pos:].index(' ')
		tmp_str = s[start_pos: end_pos]
		tmp_pos = start_pos
		if len(tmp_str) >= 2:
		    while(tmp_pos < end_pos):
		        comp_str = tmp_str[tmp_pos:]
		        while(len(comp_str) >= 2):
		            if comp_str in s[start_pos+len(comp_str)-1:]:
		                key_dict[comp_str] = s.count(comp_str)
		                tmp_pos += len(comp_str)
		                #这里有问题
		            else:
		            	comp_str = comp_str[:-1]
		    start_pos = end_pos

	return key_dict

s1 = modified('患者王敦昂，男性，60岁，已婚，因“左上肺癌术后3年余，进食后梗噎感3周”入院。患者既往2012年3月30日于我科行左上肺支气管袖状切除、支气管成形术，术后恢复顺利。于3周前无明显诱因下出现进食后梗噎感，进硬食后明显，当时未予重视，未行特殊治疗。患者进食后梗噎感进行性加重，尚能进正常饮食，遂至滨海县中医院就诊，查胃镜及病理示：距门齿27-31cm处高级别上皮内瘤变，完善胸部CT平扫（检查号：103491）提示：左肺部分切除术后改变，肺气肿。现患者为求进一步治疗来我院门诊就诊，拟诊“肺癌术后”收住我科。病程中，患者无发热、咳嗽，无胸闷、胸痛，无腹痛、腹泻，无返酸、嗳气，无恶心、呕吐，尚能进正常饮食，睡眠可，二便正常，体重减轻2公斤。既往2012年3月30日于我科行左上肺支气管袖状切除、支气管成形术，术后恢复顺利')
s2 = trans(s1)
res = cut(s2)
print(res)
