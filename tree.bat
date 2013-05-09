
python main.py -f tree -ap 1 -as 1 -n tree-attributes-p1s1
python main.py -f tree -ap 1 -as 2 -n tree-attributes-p1s2
python main.py -f tree -ap 1 -as 3 -n tree-attributes-p1s3
python main.py -f tree -ap 2 -as 1 -n tree-attributes-p2s1
python main.py -f tree -ap 2 -as 2 -n tree-attributes-p2s2
python main.py -f tree -ap 2 -as 3 -n tree-attributes-p2s3
python main.py -f vector -ap 1 -as 1 -n vector-attributes-p1s1
python main.py -f vector -ap 1 -as 2 -n vector-attributes-p1s2
python main.py -f vector -ap 1 -as 3 -n vector-attributes-p1s3
python main.py -f vector -ap 2 -as 1 -n vector-attributes-p2s1
python main.py -f vector -ap 2 -as 2 -n vector-attributes-p2s2
python main.py -f vector -ap 2 -as 3 -n vector-attributes-p2s3

for /l %%x in (0, 2, 8) do (
    for /l %%y in (0, 2, 8) do (
        python main.py -f vector -re .%%x -mu .%%y -n vector-gen-%%x-%%y
        python main.py -f tree -re .%%x -mu .%%y -n tree-gen-%%x-%%y
    )
)
