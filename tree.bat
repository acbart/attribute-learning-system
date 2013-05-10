for /l %%x in (2, 2, 8) do (
    for /l %%y in (0, 2, 8) do (
        python main.py -f tree -re .%%x -mu .%%y -n tree-gen-%%x-%%y
    )
)
