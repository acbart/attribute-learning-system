python main.py -function_type tree -retain_percent .1 -mutation_rate .9 -name tree-gen-high-mutation
python main.py -function_type tree -retain_percent .2 -mutation_rate .6 -name tree-gen-high-mutation-equal-others
python main.py -function_type tree -retain_percent .1 -mutation_rate .45 -name tree-gen-equal-mutation-crossover
python main.py -function_type tree -retain_percent .1 -mutation_rate 0 -name tree-gen-high-crossover
python main.py -function_type tree -retain_percent .6 -mutation_rate .2 -name tree-gen-high-retention-equal-others
python main.py -function_type tree -retain_percent .9 -mutation_rate .1 -name tree-gen-high-retention-no-crossover
python main.py -function_type tree -retain_percent .33 -mutation_rate .34 -name tree-gen-equal

python main.py -function_type tree -primary_attributes 1 -secondary_attributes 1 -name tree-attributes-p1s1
python main.py -function_type tree -primary_attributes 1 -secondary_attributes 2 -name tree-attributes-p1s2
python main.py -function_type tree -primary_attributes 1 -secondary_attributes 3 -name tree-attributes-p1s3
python main.py -function_type tree -primary_attributes 2 -secondary_attributes 1 -name tree-attributes-p2s1
python main.py -function_type tree -primary_attributes 2 -secondary_attributes 2 -name tree-attributes-p2s2
python main.py -function_type tree -primary_attributes 2 -secondary_attributes 3 -name tree-attributes-p2s3

python main.py -function_type tree -player1 greedy -player2 greedy -name tree-players-greedy-greedy
python main.py -function_type tree -player1 greedy -player2 random -name tree-players-greedy-random
python main.py -function_type tree -player1 random -player2 greedy -name tree-players-random-greedy
python main.py -function_type tree -player1 random -player2 random -name tree-players-random-random
python main.py -function_type tree -player1 greedy -name tree-players-greedy-minimax
python main.py -function_type tree -player1 random -name tree-players-random-minimax
python main.py -function_type tree -player2 greedy -name tree-players-minimax-greedy
python main.py -function_type tree -player2 random -name tree-players-minimax-random
python main.py -function_type tree -name tree-players-minimax-minimax