import json
import os
import pandas as pd

def load_rules():
    # 自动适配本地或云端路径
    config_path = os.path.join(os.path.dirname(__file__), "config", "rules.json")
    with open(config_path, encoding='utf-8') as f:
        return json.load(f)

def calculate_performance(df):
    rules = load_rules()
    weights = rules.get("科室权重", {})
    
    # 清洗科室名称
    df['科室'] = df['科室'].astype(str).str.strip()
    
    # 检查匹配
    unmatched = ~df['科室'].isin(weights.keys())
    if unmatched.any():
        missing = df[unmatched]['科室'].unique()
        raise ValueError(f"❌ 配置中缺少科室权重: {list(missing)}")
    
    # 计算总绩效
    df['总绩效'] = df['科室'].map(weights) * df['工资总和']
    df['总绩效'] = df['总绩效'].round(2)
    
    return df[['科室', '工资总和', '占比', '总绩效']]