from MinHash_utils import *


def main():
    
    # Custumize csv field size limit
    csv.field_size_limit(100000000)
    
    # A dictionary conataining windows common software names
    common_windows_software_names = get_dic_of_common_windows_software_names()

    # Delete emtpy name from common_windows_software_names
    delete_key(common_windows_software_names, '')

    # Prepare a dictionary with all possible 3-grams
    three_grams_dic = get_all_3_grams_list()
    
    # For each tri gram in three_grams_dict -> add software names contains it
    init_three_grams_dic(three_grams_dic, common_windows_software_names)

    # Execute 100 random hash functions for each tri-gram
    three_gram_to_hash_values_dic = get_three_gram_to_hash_values_dic(three_grams_dic)

    # Initalize 100 X length(software_names) matrix
    signature_matrix = init_signature_matrix(common_windows_software_names)

    # For each row, col in signature_matrix -> put minimum value of relevant hash results
    eval_signature_matrix(signature_matrix, three_grams_dic, three_gram_to_hash_values_dic)
    
    # Plit each 100 length signature in signature_matrix into 25 pieces of size 4
    LSH_buckets = build_LSH_buckets(signature_matrix, common_windows_software_names)

    # Save results
    save(LSH_buckets, signature_matrix, three_gram_to_hash_values_dic)

    # Prepare a file with all relevant data regarding the bands
    prepaere_csv_files_per_band(LSH_buckets)


if __name__ == "__main__":
    main()




