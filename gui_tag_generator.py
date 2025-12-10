#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
随机标签组合生成器 - GUI版本
从 tags.txt 文件中随机选择3个标签并生成搜索URL
"""

import random
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import webbrowser

# ==================== 配置区域 ====================
CONFIG = {
    'tags_file': 'tags.txt',
    'base_url': 'https://nhentai.net/search/',
    'tag_count': 3,
    'sort_param': 'popular-week',
}
# ================================================


class TagGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("随机标签生成器")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        self.tags = []
        self.current_url = ""
        
        self.create_widgets()
        self.load_tags_auto()
    
    def create_widgets(self):
        """创建GUI组件"""
        
        # 顶部框架 - 配置区域
        config_frame = ttk.LabelFrame(self.root, text="配置", padding=10)
        config_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 标签文件
        ttk.Label(config_frame, text="标签文件:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.file_entry = ttk.Entry(config_frame, width=40)
        self.file_entry.insert(0, CONFIG['tags_file'])
        self.file_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(config_frame, text="浏览", command=self.browse_file).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(config_frame, text="加载", command=self.load_tags).grid(row=0, column=3, padx=5, pady=5)
        
        # 基础URL
        ttk.Label(config_frame, text="基础URL:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(config_frame, width=40)
        self.url_entry.insert(0, CONFIG['base_url'])
        self.url_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # 标签数量
        ttk.Label(config_frame, text="标签数量:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.count_spinbox = ttk.Spinbox(config_frame, from_=1, to=10, width=10)
        self.count_spinbox.set(CONFIG['tag_count'])
        self.count_spinbox.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # 排序参数（下拉选择）
        ttk.Label(config_frame, text="排序方式:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.sort_combobox = ttk.Combobox(config_frame, width=18, state="readonly")
        self.sort_combobox['values'] = ('popular-today', 'popular-week', 'popular')
        self.sort_combobox.set(CONFIG['sort_param'])
        self.sort_combobox.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        # 状态标签
        self.status_label = ttk.Label(config_frame, text="等待加载标签文件...", foreground="gray")
        self.status_label.grid(row=4, column=0, columnspan=4, sticky=tk.W, pady=5)
        
        # 中间框架 - 生成按钮
        button_frame = ttk.Frame(self.root, padding=10)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.generate_btn = ttk.Button(button_frame, text="🎲 生成随机标签", command=self.generate_tags, state=tk.DISABLED)
        self.generate_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="🔗 在浏览器中打开", command=self.open_in_browser).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📋 复制URL", command=self.copy_url).pack(side=tk.LEFT, padx=5)
        
        # 结果框架 - 显示选中的标签
        result_frame = ttk.LabelFrame(self.root, text="随机选择的标签", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.tags_text = tk.Text(result_frame, height=5, font=("Arial", 11), wrap=tk.WORD)
        self.tags_text.pack(fill=tk.BOTH, expand=True)
        
        # URL框架
        url_frame = ttk.LabelFrame(self.root, text="生成的搜索URL", padding=10)
        url_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.url_text = tk.Text(url_frame, height=4, font=("Arial", 10), wrap=tk.WORD)
        self.url_text.pack(fill=tk.BOTH, expand=True)
        
        # 底部框架 - 统计信息
        stats_frame = ttk.Frame(self.root, padding=5)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.stats_label = ttk.Label(stats_frame, text="", foreground="blue")
        self.stats_label.pack(side=tk.LEFT)
    
    def browse_file(self):
        """浏览文件"""
        filename = filedialog.askopenfilename(
            title="选择标签文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if filename:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, filename)
            self.load_tags()
    
    def load_tags_auto(self):
        """自动加载默认标签文件"""
        try:
            filename = self.file_entry.get()
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                self.tags = [tag.strip() for tag in content.split(',') if tag.strip()]
            
            if self.tags:
                self.status_label.config(text=f"✓ 成功加载 {len(self.tags)} 个标签", foreground="green")
                self.generate_btn.config(state=tk.NORMAL)
                self.update_stats()
            else:
                self.status_label.config(text="⚠ 文件为空", foreground="orange")
        except FileNotFoundError:
            self.status_label.config(text=f"⚠ 找不到文件: {filename}", foreground="orange")
        except Exception as e:
            self.status_label.config(text=f"❌ 加载失败: {str(e)}", foreground="red")
    
    def load_tags(self):
        """加载标签文件"""
        filename = self.file_entry.get()
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                self.tags = [tag.strip() for tag in content.split(',') if tag.strip()]
            
            if self.tags:
                self.status_label.config(text=f"✓ 成功加载 {len(self.tags)} 个标签", foreground="green")
                self.generate_btn.config(state=tk.NORMAL)
                self.update_stats()
                messagebox.showinfo("成功", f"成功加载 {len(self.tags)} 个标签！")
            else:
                self.status_label.config(text="⚠ 文件为空", foreground="orange")
                messagebox.showwarning("警告", "标签文件为空！")
        except FileNotFoundError:
            self.status_label.config(text=f"❌ 找不到文件: {filename}", foreground="red")
            messagebox.showerror("错误", f"找不到文件: {filename}")
        except Exception as e:
            self.status_label.config(text=f"❌ 加载失败: {str(e)}", foreground="red")
            messagebox.showerror("错误", f"加载失败: {str(e)}")
    
    def generate_tags(self):
        """生成随机标签"""
        if not self.tags:
            messagebox.showwarning("警告", "请先加载标签文件！")
            return
        
        try:
            count = int(self.count_spinbox.get())
            if count > len(self.tags):
                messagebox.showwarning("警告", f"标签数量不足！只有 {len(self.tags)} 个标签")
                count = len(self.tags)
            
            # 随机选择标签（保留完整的标签包括计数）
            selected_tags_with_count = random.sample(self.tags, count)
            
            # 显示标签（包含计数）
            self.tags_text.delete(1.0, tk.END)
            for i, tag in enumerate(selected_tags_with_count, 1):
                self.tags_text.insert(tk.END, f"Tag {i}: {tag}\n")
            
            # 生成URL（只使用标签名称，不包含计数）
            base_url = self.url_entry.get()
            sort_param = self.sort_combobox.get()
            
            # 提取纯标签名（去除括号中的计数）
            selected_tags_clean = [self.extract_tag_name(tag) for tag in selected_tags_with_count]
            
            processed_tags = [tag.replace(' ', '+') for tag in selected_tags_clean]
            tag_query = ', '.join(processed_tags)
            query_string = f"tag:{tag_query}"
            encoded_query = query_string.replace(' ', '+').replace(',', '%2C').replace(':', '%3A')
            
            self.current_url = f"{base_url}?q={encoded_query}&sort={sort_param}"
            
            # 显示URL
            self.url_text.delete(1.0, tk.END)
            self.url_text.insert(tk.END, self.current_url)
            
        except Exception as e:
            messagebox.showerror("错误", f"生成失败: {str(e)}")
    
    def open_in_browser(self):
        """在浏览器中打开URL"""
        if self.current_url:
            webbrowser.open(self.current_url)
        else:
            messagebox.showwarning("警告", "请先生成URL！")
    
    def copy_url(self):
        """复制URL到剪贴板"""
        if self.current_url:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.current_url)
            messagebox.showinfo("成功", "URL已复制到剪贴板！")
        else:
            messagebox.showwarning("警告", "请先生成URL！")
    
    def update_stats(self):
        """更新统计信息"""
        self.stats_label.config(text=f"📊 标签库: {len(self.tags)} 个标签")
    
    def extract_tag_name(self, tag_with_count):
        """提取标签名称（去除括号中的计数）"""
        # 如果包含括号，提取括号前的内容
        if '(' in tag_with_count:
            return tag_with_count.split('(')[0].strip()
        return tag_with_count.strip()


def main():
    root = tk.Tk()
    app = TagGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
