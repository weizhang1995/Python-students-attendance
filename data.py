import io
import os.path
import re

## The list2csv function is used to save the list to a csv file.
## list2csv函数用来把列表存储为csv文件
def list2csv(list,file):
	str1=','
	str2='\n'
	with io.open(file, 'w+', encoding='utf8') as f:
		for line in list:
			f.write(str1.join(line) + str2)

## The csv2list function is used to read the csv file line by line, 
# and we selected id and names which we would use next time.
## csv2list函数用来一行一行读取csv文件，存储为列表
# 我们在这里把需要用到的学号（id）和学生姓名（names）读取出来，存到列表
def csv2list(file_path):
	lst = []
	with io.open(file_path, 'r', encoding='gb18030') as f:
		for line in f:
			try:
				data = line.replace('\n','').replace(' ','').split(',')[2]
				id = data[0:8]
				name = data[8:]
				lst.append([id,name])
			except:
				print('End of file')
	# 对每个文件重复的学号剔除，使得每个文件仅保留一次签到记录
	return list(dict((x[0], x) for x in lst).values())

## The read_dir function is used to read txt files by directory path.
## read_dir函数用来通过传递文件路径来读取整个文件夹里面的txt文件
def read_dir(dir_path):
	files = [f for f in os.listdir(dir_path) if f.endswith(".txt")]
	data = []
	for file in files:
		data = data + csv2list('./kaoqin/' + file)
	return data

## Now we begain to use functions above to deal with datas.
# First we can get a total data list.
## 现在开始运用上面的函数处理数据
# 首先我们的到一个汇总的data列表，包含id和names
data = read_dir('./kaoqin')

## Then we use the id to count the times of each student attended classes.
# We use {dict} in Python to ensure the id is unique for each student.
## 接下来，我们通过唯一id来统计每个学生签到次数
# 我们创建Python字典来保证每个学生id是唯一确定的
db = {}
result = []
for i in data:
	id = i[0]
	name = i[1]
	# 保证id都是数字，剔除学号少输一位的同学
	if id.isdigit():
		try:
			# and if one's id is in the dictionary, the 'times' plus 1;
			# 如果一个学生的id出现在字典里，就把他签到次数加1
			db[id] = [name, db[id][1] + 1]
		except KeyError:
			# else we add the id in our dictionary and initiallize it's 'times' as 1.
			# 如果id不在字典里，就把他的id加入到字典中，并且初始化他的签到次数为1
			db[id] = [name, 1]
for j in db:
	result.append([j,db[j][0],str(db[j][1])])

list2csv(result,'qiandao.csv')

