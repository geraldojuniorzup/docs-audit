import os
import re

from templateframework.metadata import Metadata
def run(metadata: Metadata = None):
    print("Hello from lgpd_script.py!")
    # vocabulary
    personal_datas_pt = ['nome', 'nascimento', 'rg', 'cpf',
                        'endereco', 'cep', 'cartao', 'renda', 'telefone', 'e-mail']
    sensitive_datas_pt = ['etnia', 'raca', 'religiao',
                        'partido', 'sindicato', 'diabetico', 'católico', 'evangélico', 'protestante', 'masculino', 'feminino']

    personal_datas_en = ['name', 'birth', 'nin', 'address',
                        'post code', 'zip code', 'card', 'income', 'telephone', 'email']
    sensitive_datas_en = ['ethnicity', 'race', 'religion', 'party', 'union', 'diabetic',
                        'catholic', 'evangelical', 'protestant', 'male', 'masculine', 'feminine', 'female']

    personal_datas = personal_datas_pt + personal_datas_en
    sensitive_datas = sensitive_datas_pt + sensitive_datas_en

    phoneNumRegex = re.compile(r'(^[0-9]{2})?(\s|-)?(9?[0-9]{4})-?([0-9]{4}$)')
    cpfSimpleRegex = re.compile(r'\b\d{11}\b')
    cpfRegex = re.compile(r'\d{3}\.\d{3}\.\d{3}\-\d{2}')
    rgRegex = re.compile(r'(^\d{1,2}).?(\d{3}).?(\d{3})-?(\d{1}|X|x$)')
    cepRegex = re.compile(r'\d{5}\-\d{3}')
    emailRegex = re.compile(
        r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    path = str(metadata.target_path)

    print("\n 🔎 -- Critical Data Analysis Tool -- 🔎 \n")


    def searchData(path):

        print("\n 📖 Detailed Data Analysis 📖 \n")

        count_personal_total = 0
        count_sensitive_total = 0
        count_file_total = 0

        for path, subdirs, files in os.walk(path):
            for file_name in files:
                with open(os.path.join(path, file_name), 'r', encoding='utf-8', errors='ignore') as f:
                    file = f.read()

                final_path = os.path.abspath(file_name)
                count_personal = 0
                count_sensitive = 0

                searchCpf = cpfRegex.search(file, re.MULTILINE)
                if(searchCpf):
                    count_personal += 1
                    print("The personal data CPF found in this path: " +
                        searchCpf.group())

                searchCpfSimple = cpfSimpleRegex.search(file, re.MULTILINE)
                if(searchCpfSimple):
                    count_personal += 1
                    print("The personal data CPF found in this path: " +
                        searchCpfSimple.group())

                searchPhone = phoneNumRegex.search(file, re.MULTILINE)
                if(searchPhone):
                    count_personal += 1
                    print("The personal data phone found in this path: " +
                        searchPhone.group())

                searchRg = rgRegex.search(file, re.MULTILINE)
                if(searchRg):
                    count_personal += 1
                    print("The personal data RG found in this path: " +
                        searchRg.group())

                searchCep = cepRegex.search(file, re.MULTILINE)
                if(searchCep):
                    count_personal += 1
                    print("The personal data CEP found in this path: " +
                        searchCep.group())

                searchEmail = emailRegex.search(file, re.MULTILINE)
                if(searchEmail):
                    count_personal += 1
                    print("The personal data Email found in this path: " +
                        searchEmail.group())

                for personal_data in personal_datas:
                    personal_data = personal_data.strip()
                    if (re.search(r'\b' + re.escape(personal_data) + r'\b', file, re.MULTILINE)):
                        count_personal += 1
                        print("The personal data " +
                            personal_data + " found in this path ")

                for sensitive_data in sensitive_datas:
                    sensitive_data = sensitive_data.strip()
                    if (re.search(r'\b' + re.escape(sensitive_data) + r'\b', file, re.MULTILINE)):
                        count_sensitive += 1
                        print("The sensitive data " +
                            sensitive_data + " found in this path ")

                if (count_personal and count_sensitive >= 1):
                    print("\n 🚨 Pay close attention to this file: " +
                        final_path + " 🚨 \n")
                    count_file_total = count_file_total + 1
                elif (count_personal >= 1):
                    print("\n 🚧 Attention to this file: " + final_path + " 👀 \n")
                    count_file_total = count_file_total + 1
                elif (count_sensitive >= 1):
                    print("\n 🚧 Attention to this file: " + final_path + " 👀 \n")
                    count_file_total = count_file_total + 1
                count_personal_total = count_personal + count_personal_total
                count_sensitive_total = count_sensitive + count_sensitive_total
        return count_personal_total, count_sensitive_total, count_file_total


    count_personal_total, count_sensitive_total, count_file_total = searchData(
        path)

    print("\n 📈 Data Analysis Summary 📈\n")
    print("😱 Possible personal data violation: " + str(count_personal_total))
    print("💔 Possible sensitive data violation: " + str(count_sensitive_total))
    print("📃 Total files with possible violations: " + str(count_file_total))



    return metadata