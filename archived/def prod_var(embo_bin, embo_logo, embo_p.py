def prod_var(embo_bin, embo_logo, embo_plastic_id, embo_gender_code_acc):
    embo_product = "New Product"
    embo_varient = "New Varient"

    with open('config/product_varient_list.txt', 'r', encoding='utf-8') as data_file:
        next(data_file)  # skip header

        for line in data_file:
            line_data = [col.strip() for col in line.split(',')]

            if len(line_data) < 6:
                continue

            file_embo, file_logo, file_plastic_id, file_gender, file_product, file_varient = line_data
            file_plastic_id = file_plastic_id.upper()
            file_gender = file_gender.upper()

            if embo_bin == file_embo and embo_logo == file_logo:

                # 1. Exact plastic + gender
                if embo_plastic_id.strip() == file_plastic_id and embo_gender_code_acc == file_gender:
                    return [file_product, file_varient]

                # 2. Exact plastic, gender blank
                elif embo_plastic_id.strip() == file_plastic_id and file_gender == "":
                    return [file_product, file_varient]

                # 3. Plastic NO + gender match
                elif file_plastic_id == "NO" and embo_gender_code_acc == file_gender:
                    return [file_product, file_varient]

                # 4. Plastic NO + gender blank
                elif file_plastic_id == "NO" and file_gender == "":
                    return [file_product, file_varient]

    return [embo_product, embo_varient]



print(prod_var("466505","102","NO","2"))