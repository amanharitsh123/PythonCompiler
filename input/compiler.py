import subprocess, os, time, signal

def subprocess_cmd(command,inputfile,outputfile,time_limit,mem_limit):
	# ulimit -Sv 500000
	#augmenting command for memory usage restriction 
	command="ulimit -Sv " + mem_limit+";"+command
	process = subprocess.Popen(command,stdout=outputfile,stdin=inputfile,shell=True, preexec_fn=os.setsid)
	is_timeout=wait_timeout(process,time_limit)
	if is_timeout:
		return True
		# print("Time Limit Exceeded!!")

def compute_score(f1,f2,is_TLE):
	file1=open(f1,"r")
	file2=open(f2,"r")
	score=0
	for x,y in zip(file1.readlines(),file2.readlines()):
		if x==y:
			score+=1
	file1=open(f1,"w")
	file1.write(str(score))
	# print(score)
	if is_TLE:
		file1.write(" Time Limit Exceeded")

def wait_timeout(proc, seconds):
	start = time.time()
	end = start + seconds
	interval = min(seconds / 1000.0, .25)

	while True:
		result = proc.poll()
		if result is not None:
			return result
		if time.time() >= end:
			os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
			return True
		time.sleep(interval)


dic_languages={1:"python3 test.py", 2:"gcc test.c;./a.out",3:"g++ test.cpp;./a.out"}
command_to_compile = ""
inputfile = open("/input/inp.txt")
sanitized_input = open("sanitized_input","w")
outputfile = open("/output/output.txt","w")

# Fetch Parameters [language,time_limit,mem_limit]

parameters = inputfile.readline()
parameters = parameters.split()
language = int(parameters[0])
time_limit = int(parameters[1])
mem_limit = parameters[2]

command_to_compile = dic_languages[language]
# print("compiling ",command_to_compile)

# Stripfile for the first line
subprocess.Popen("sed '1d'  inp.txt",stdout=sanitized_input,stdin=inputfile,shell=True, preexec_fn=os.setsid)

# Changing input file to read mode and starting compilation
sanitized_input=open("sanitized_input","r")
is_TLE=subprocess_cmd(command_to_compile,sanitized_input,outputfile,time_limit,mem_limit)
compute_score("/output/output.txt","/output/target.txt",is_TLE)

