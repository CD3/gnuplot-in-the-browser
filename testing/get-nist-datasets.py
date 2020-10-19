import requests,pathlib
from pyparsing import *
import re

dataset_names = [
"Misra1a",
"Chwirut2",
"Chwirut1",
"Lanczos3",
"Gauss1",
"Gauss2",
"DanWood",
"Misra1b",
"Kirby2",
"Hahn1",
# "Nelson",
"MGH17",
"Lanczos1",
"Lanczos2",
"Gauss3",
"Misra1c",
"Misra1d",
"Roszman1",
"ENSO",
"MGH09",
"Thurber",
"BoxBOD",
"Rat42",
"MGH10",
"Eckerle4",
"Rat43",
"Bennett5",
]

class parsers:
  Float = Combine(Optional(Literal("+")|Literal("-")) + Word(nums+".") + Optional(Word("Ee") + Optional(Literal("+")|Literal("-")) + Word(nums)))
  Int = Combine(Optional(Literal("+")|Literal("-")) + Word(nums))
  data_line_counts = Suppress(Literal("Data")+Literal("(")+Literal("lines"))+Word(nums)("startline")+Suppress(Literal("to"))+Word(nums)("endline")
  parameter = alphas
  model_identifier = Suppress(Literal("Model:"))
  model_type = Word(alphas)("type") + Suppress(Literal("Class") + Optional(QuotedString("(",endQuoteChar=")")))
  model_parameters = Word(nums)("parameter count") + Suppress(Literal("Parameters") + Literal("(")) + Word(alphanums)("first parameter") + Suppress(Literal("and")|Literal("to")) + Word(alphanums)("last parameter") + Suppress(Literal(")"))
  model_constant = Suppress(Optional(Word(alphas) + Literal("=") + Float))
  model_function = Suppress(Literal("y")+Literal("=")) + SkipTo(LineEnd()+LineEnd())
  model_spec = model_identifier + model_type + model_parameters + model_constant + model_function("model function")

  

  model_parameter = Combine(Literal("b")+Word(nums)) + Suppress(Literal("=")) + Float("start value 1") + Float("start value 2") + Float("certified value") + Float("certified standard deviation")


for name in dataset_names:
  url = f"https://www.itl.nist.gov/div898/strd/nls/data/LINKS/DATA/{name}.dat"
  print("Downloading",name,"from",url)
  file = pathlib.Path(f"{name}.dat")
  if not file.exists():
    r = requests.get(url,allow_redirects=False)
    file.write_text(r.content.decode("utf-8"))
  else:
    print(f"{file} already exists, skipping")

for name in dataset_names:
  dfile = pathlib.Path(f"{name}.dat")
  gfile = pathlib.Path(f"{name}.gnuplot")
  print(f"Generating gnuplot file for {name}.")
  data = pathlib.Path(dfile).read_text()

  data_lines = data.split("\n")
  script_lines = []

  # get data
  matches = parsers.data_line_counts.searchString(data)
  if len(matches) > 1:
    print(f"ERROR: more than one set of data lines found in {dfile}. Skipping.")
    continue
  else:
    dbeg,dend = matches[0]
    script_lines.append("# data")
    script_lines.append("$data << EOD")
    script_lines += data_lines[int(dbeg)-1:int(dend)]
    script_lines.append("EOD")

  params = { m[0] : m[1:] for m in parsers.model_parameter.searchString(data) }

  script_lines.append("# parameters")
  for p in params:
    script_lines.append(f"{p}_s1  = {params[p][0]}")
    script_lines.append(f"{p}_s2  = {params[p][1]}")
    script_lines.append(f"{p}_exp = {params[p][2]}")
    script_lines.append(f"{p}_unc = {params[p][3]}")

  model = parsers.model_spec.searchString(data)
  # print(model)

  script_lines.append("# fit function")
  func = model[0]["model function"][0]
  func = func.replace("\n","").replace("[","(").replace("]",")")
  func = re.sub(r"\+\s*e$","# + e",func)
  script_lines.append(f"f(x) = {func}")
  script_lines.append("# a parameterized version of the fit function")
  script_lines.append(f"f2(x,{','.join(params.keys())}) = {func}")





  starting_points = {"s1":"first starting point", "s2": "second starting point", "exp": "certified value"}

  for k in starting_points:
    script_lines.append(f"# do fit from {starting_points[k]}")
    for p in params.keys():
      script_lines.append(f"{p} = {p}_{k}")
    script_lines.append("fit f(x) '$data' u 2:1 via "+",".join(params.keys()))
    for p in params.keys():
      script_lines.append(f"{p}_{k}_fit_val = {p}")
      script_lines.append(f"{p}_{k}_fit_unc = {p}_err")



  plot_cmd = "plot '$data' u 2:1 title 'data'"
  for k in starting_points:
    plot_cmd += ", f2(x,"+",".join([f"{p}_{k}_fit_val" for p in params])+f") title '{starting_points[k]}'"

  script_lines.append(plot_cmd)

  script_lines.append("# print summary")
  script_lines.append("pdiff(x,y) = 200*(x-y)/(x+y)")
  script_lines.append(f"print 'certified values'")
  for p in params:
    script_lines.append(f"print '{p} = ',{p}_exp,' +/- ',{p}_unc")
  for k in starting_points:
    script_lines.append(f"print '{starting_points[k]}'")
    for p in params:
      script_lines.append(f"print '{p} = ',{p}_{k}_fit_val,' +/- ',{p}_{k}_fit_unc,' (',pdiff({p}_{k}_fit_val,{p}_exp),'% +/- ',pdiff({p}_{k}_fit_unc,{p}_unc),'%)'")



  gfile.write_text("\n".join(script_lines))





