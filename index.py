def reindex_file(input_file_path, output_file_path):
    mapping = {}
    new_index = 1
    output = []

    with open(input_file_path, 'r') as file:
        for line in file:
            if line.strip():  # vérifie si la ligne n'est pas vide
                index1, index2 = map(int, line.split('\t'))

                if index1 not in mapping:
                    mapping[index1] = new_index
                    new_index += 1

                if index2 not in mapping:
                    mapping[index2] = new_index
                    new_index += 1

                output.append(f"{mapping[index1]}\t{mapping[index2]}")

    with open(output_file_path, 'w') as file:
        file.write('\n'.join(output))

input_file = 'C:\\Users\\winona\\Documents\\M1\\S1\\SystemeComplexe\\Projet\\ca-GrQc.txt\\data1.txt'
output_file = 'C:\\Users\\winona\\Documents\\M1\\S1\\SystemeComplexe\\Projet\\ca-GrQc.txt\\data.txt'

reindex_file(input_file, output_file)
