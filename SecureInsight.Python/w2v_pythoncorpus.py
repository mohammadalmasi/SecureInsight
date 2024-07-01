from pydriller import Repository

#collect all python code for building a corpus to train the word2vec model


repos = ["https://github.com/mohammadalmasi/PythonApplication1"]

pythontraining = ""

for r in repos:
  print(r)
  files = []
  for commit in Repository(r).traverse_commits():
      for m in commit.modified_files:
        filename = m.new_path
        
        if filename is not None:
          if ".py" in filename:
            if not filename in files:
              code = m.source_code
              if code is not None:
                pythontraining = pythontraining + "\n\n" + code
                files.append(filename)
        
          
  with open('pythontraining.txt', 'w') as outfile:
    outfile.write(pythontraining)