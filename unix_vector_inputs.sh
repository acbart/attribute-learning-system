python main.py -function_type vector -retain_percent .1 -mutation_rate .9 -name vector-gen-high-mutation
python main.py -function_type vector -retain_percent .2 -mutation_rate .6 -name vector-gen-high-mutation-equal-others
python main.py -function_type vector -retain_percent .1 -mutation_rate .45 -name vector-gen-equal-mutation-crossover
python main.py -function_type vector -retain_percent .1 -mutation_rate 0 -name vector-gen-high-crossover
python main.py -function_type vector -retain_percent .6 -mutation_rate .2 -name vector-gen-high-retention-equal-others
python main.py -function_type vector -retain_percent .9 -mutation_rate .1 -name vector-gen-high-retention-no-crossover
python main.py -function_type vector -retain_percent .33 -mutation_rate .34 -name vector-gen-equal

python main.py -function_type vector -primary_attributes 1 -secondary_attributes 1 -name vector-attributes-p1s1
python main.py -function_type vector -primary_attributes 1 -secondary_attributes 2 -name vector-attributes-p1s2
python main.py -function_type vector -primary_attributes 1 -secondary_attributes 3 -name vector-attributes-p1s3
python main.py -function_type vector -primary_attributes 2 -secondary_attributes 1 -name vector-attributes-p2s1
python main.py -function_type vector -primary_attributes 2 -secondary_attributes 2 -name vector-attributes-p2s2
python main.py -function_type vector -primary_attributes 2 -secondary_attributes 3 -name vector-attributes-p2s3

python main.py -function_type vector -player1 greedy -player2 greedy -name vector-players-greedy-greedy
python main.py -function_type vector -player1 greedy -player2 random -name vector-players-greedy-random
python main.py -function_type vector -player1 random -player2 greedy -name vector-players-random-greedy
python main.py -function_type vector -player1 random -player2 random -name vector-players-random-random
python main.py -function_type vector -player1 greedy -name vector-players-greedy-minimax
python main.py -function_type vector -player1 random -name vector-players-random-minimax
python main.py -function_type vector -player2 greedy -name vector-players-minimax-greedy
python main.py -function_type vector -player2 random -name vector-players-minimax-random
python main.py -function_type vector -name vector-players-minimax-minimax