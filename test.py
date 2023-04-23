def get_true_var(var: str):
    with open('vars_from_bd.py', 'r') as f:
        old_data = f.readlines()
    with open('vars_from_bd.py', 'w') as f:
        fm = []
        for r in old_data:
            if r.split()[0] == var and r.split()[2] == 'False':
                fm.append(f'{var}=True\n')
                continue
            fm.append(r)
        f.writelines(fm)
    print('Сделал True')

def get_false_var(var: str):
    with open('vars_from_bd.py', 'r') as f:
        old_data = f.readlines()
    with open('vars_from_bd.py', 'w') as f:
        fm = []
        for r in old_data:
            if r.split()[0] == var and r.split()[2] == 'True':
                fm.append(f'{var}=False\n')
                continue
            fm.append(r)
        f.writelines(fm)
    print('сделал false')

# for r in f:
#     if r[0] == 'READER' and r.split()[2] == 'False':
#         fm.append(f'READER=True')
#         # print(r.split()[2])
#         continue
#     fm.append(r)
# f.writelines(fm)
