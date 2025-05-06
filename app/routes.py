from flask import Blueprint, render_template, request
import pandas as pd

# 创建蓝图对象
bp = Blueprint('main', __name__)

# 在应用启动时一次性读取并预处理数据
df = pd.read_excel('app/data/characters.xlsx', engine='openpyxl')

# 清理数据框中的字符串列，去除两端的空格
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].str.strip()

# 添加缺失的身份地位字段（用于前端筛选）
for col in ['身份地位', '身份地位详细', '身份地位细分']:
    if col not in df.columns:
        df[col] = ''

# 路由：首页，显示所有人物
@bp.route('/')
def index():
    persons = df.to_dict(orient='records')
    return render_template('index.html', persons=persons)

# 路由：处理搜索请求
@bp.route('/search', methods=['POST'])
def search():
    name = request.form.get('name', '').strip()
    if name:
        result = df[df['姓名'].str.contains(name, case=False, na=False)]
    else:
        result = df
    return render_template('result.html', result=result.to_dict(orient='records'))

# 路由：处理分面筛选请求（含身份地位筛选）
@bp.route('/filter', methods=['GET'])
def filter():
    # 获取筛选参数
    dynasty = request.args.get('dynasty')
    gender = request.args.get('gender')
    birthplace = request.args.get('birthplace')
    thoughts = request.args.get('thoughts')
    field = request.args.get('field')
    category1 = request.args.get('category1')
    category2 = request.args.get('category2')
    category3 = request.args.get('category3')

    result = df.copy()

    if dynasty:
        result = result[result['朝代'] == dynasty]
    if gender:
        result = result[result['性别'] == gender]
    if birthplace:
        result = result[result['地理背景'] == birthplace]
    if thoughts:
        result = result[result['思想流派'] == thoughts]
    if field:
        result = result[result['主要领域'] == field]
    if category1:
        result = result[result['身份地位'] == category1]
    if category2:
        result = result[result['身份地位详细'] == category2]
    if category3:
        result = result[result['身份地位细分'] == category3]

    return render_template('result.html', result=result.to_dict(orient='records'))