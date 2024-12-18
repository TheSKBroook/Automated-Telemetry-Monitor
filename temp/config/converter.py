# Convert xlsx. file into yml format
import pandas as pd
import yaml, json, ast, math

data_dictionary = {
    "alert": "{Alert Name}_{Severity}",
    "expr": "{Expression}",
    "for": "{During}",
    "labels": {"severity": "{Severity}"},
    "annotations": {"summary": "{Summary}", "description": "{Description}"}
}

# 
def fill(rule_dict, expression, severity):
    temp_file = {}
    count = 0

    for kk, vv in data_dictionary.items():
        if isinstance(vv, str):
            rule_dict["Severity"] = severity
            rule_dict["Expression"] = expression
            temp_file[kk] = vv.format(**rule_dict)
        else:
            temp_file[kk] = {key: value.format(**rule_dict) for key, value in
                             vv.items()}
        count += 1

    return temp_file


def main():
    final_file = {'groups': []}
    df = pd.read_excel('/home/eason/demo/temp/metrics_excel.xlsx')
    temp_dict = {}
    # 把yml前面架構架好
    for ind in df.index:
        # 假設有多個groups:
        if (df.at[ind, 'Enabled']) == "Y":
            if not isinstance(df.at[ind, 'Second Cat.'], str):
                final_file['groups'].append({'name': df.at[ind, 'Main Cat.'], 'rules': []})
            # 整理每個rules轉成dict
            if isinstance(df.at[ind, 'Alert Name'], str):
                temp_dict[f"rule_{ind}"] = {col: df[col][ind] for col in df.columns}

    # 從整理好的dict把data_dictionary填好
    for group_ind in range(len(final_file['groups'])):
        for temp_dict_key, temp_dict_value in temp_dict.items():
            # 把對應的key, value放到相對的group
            if final_file['groups'][group_ind]['name'] == temp_dict_value["Main Cat."]:
                severity_list = temp_dict_value["Labels Severity"].split("\n")
                express_list = temp_dict_value["Express"].split("\n")
                for i in range(len(severity_list)):
                    temp = fill(temp_dict_value, express_list[i], severity_list[i])
                    final_file['groups'][group_ind]['rules'].append(temp)


    with open('/home/eason/demo/docker/prometheus/rules.yml', 'w') as file_yml:
        yaml.safe_dump(final_file, file_yml, default_flow_style=False)


if __name__ == '__main__':
    main()
