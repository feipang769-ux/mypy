import argparse,os,json
from datetime import datetime

data_file = 'ledger.json'

def initialize():
    if not os.path.exists(data_file):
        return {'entries':[],'next_id':1}
    try:
        with open(data_file,'r') as f:
            return json.load(f)
    except:
        return {'entries':[],'next_id':1}

def save_file(data):
    with open(data_file,'w',encoding='utf-8') as f:
        return json.dump(data,f,ensure_ascii=False,indent=2)

def add_entry(args):
    data = initialize()
    entry = {
            'id':data['next_id'],
            'type':args.type, 
            'date':args.date if args.date else datetime.now().strftime('%Y-%m-%d %H:%M'),
            'amount':args.amount,
            'category':args.category,
            'desc':args.desc
        }
    data['entries'].append(entry)
    data['next_id'] += 1
    save_file(data)
    print('数据保存成功')

def list_entries(args):
    data = initialize()
    entries = data['entries']
    if not entries:
        print('当前无记录')
        return 

    entries_sorted = sorted(entries,key=lambda x: x['date'],reverse=True)

    for e in entries_sorted:
        type_label = '收入' if e['type'] == 'income' else '支出'
        print(f'{e['id']},{type_label}, {e['amount']},{e['date']}')
    print('账目推送完成')

def summary(args):
    data = initialize()
    entries = data['entries']
    if not entries:
            print('当前无记录')
            return

    stats = {}
    for e in entries:
        month_key = e['date'][:7]
        if month_key not in stats:
            stats[month_key] = {'income':0,'expense':0}
        if e['type'] == 'income':
            stats[month_key]['income'] += e['amount']
        else:
            stats[month_key]['expense'] += e['amount']

    print('月度收支汇总')
    total_inc = 0
    total_exp = 0
    for month in stats.keys():
        inc = stats[month]['income']
        exp = stats[month]['expense']
        total_inc += inc 
        total_exp += exp
        print(f'{month} \n 收入:{inc} 支出:{exp} 结余:{inc - exp}')
    print(f'总计: \n 收入:{total_inc},支出:{total_exp},结余:{total_inc - total_exp}')


def delete_entry(args):
    data = initialize()
    target_id = args.id
    found = False
    for i,e in enumerate(data['entries']):
        if e['id'] == target_id:
            del data['entries'][i]
            found = True
            break

    if found:
        print('记录已删除')
        save_file(data)
    else:
        print('未找到记录')


def main():
    parser = argparse.ArgumentParser(description='命令行记账本')
    subparser = parser.add_subparsers(dest='command',required=True)

    parser_a = subparser.add_parser('add',help='添加一笔记录')
    parser_a.add_argument('-t','--type',choices=['income','expense'],required=True,help='income or expense')
    parser_a.add_argument('-c','--category',required=True,help='添加一个分类')
    parser_a.add_argument('-d','--desc',required=True,help='添加一个备注')
    parser_a.add_argument('-a','--amount',type=float,required=True,help='金额')
    parser_a.add_argument('--date',help='自定义日期')

    parser_list = subparser.add_parser('list',help='列出所有记录')

    parser_summary = subparser.add_parser('summary',help='月度统计')

    parser_delete = subparser.add_parser('delete',help='删除一笔记录')
    parser_delete.add_argument("id",type=int, required=True,help='要删除的ID')

    args = parser.parse_args()

    if args.command == 'add':
        add_entry(args)
    elif args.command == 'list':
        list_entries(args)
    elif args.command == 'summary':
        summary(args)
    elif args.command == 'delete':
        delete_entry(args)

if __name__ == '__main__':
    main()
    
        