#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 标签提取工具 - GUI版本
从 HTML 文件或直接粘贴的 HTML 代码中提取 <span class="name"> 标签内容
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from bs4 import BeautifulSoup
import os


class HTMLTagExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HTML 标签提取工具")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        self.html_files = []
        self.extracted_tags = []
        
        self.create_widgets()
    
    def create_widgets(self):
        """创建GUI组件"""
        
        # 创建 Notebook（标签页）
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 标签页1：从文件读取
        file_tab = ttk.Frame(notebook)
        notebook.add(file_tab, text="📁 从文件读取")
        
        # 标签页2：从文本读取
        text_tab = ttk.Frame(notebook)
        notebook.add(text_tab, text="📝 粘贴 HTML 代码")
        
        # ========== 文件读取标签页 ==========
        self.create_file_tab(file_tab)
        
        # ========== HTML 代码标签页 ==========
        self.create_text_tab(text_tab)
        
        # ========== 底部公共区域 ==========
        # 配置框架
        config_frame = ttk.LabelFrame(self.root, text="提取配置", padding=10)
        config_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(config_frame, text="目标元素:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(config_frame, text='<a><span class="name"></span><span class="count"></span></a>').grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(config_frame, text="分隔符:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.separator_entry = ttk.Entry(config_frame, width=10)
        self.separator_entry.insert(0, ", ")
        self.separator_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # 结果框架
        result_frame = ttk.LabelFrame(self.root, text="📊 提取结果", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 操作按钮
        btn_frame = ttk.Frame(result_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(btn_frame, text="💾 保存为 tags.txt", command=self.save_to_file, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="📋 复制结果", command=self.copy_result, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🗑️ 清空结果", command=self.clear_result, width=15).pack(side=tk.LEFT, padx=5)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, height=8, font=("Consolas", 10), wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # 状态栏
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="等待操作...", foreground="gray")
        self.status_label.pack(side=tk.LEFT)
        
        self.count_label = ttk.Label(status_frame, text="", foreground="blue")
        self.count_label.pack(side=tk.RIGHT)
    
    def create_file_tab(self, parent):
        """创建文件读取标签页"""
        # 文件选择框架
        file_frame = ttk.Frame(parent, padding=10)
        file_frame.pack(fill=tk.X)
        
        ttk.Button(file_frame, text="📁 选择单个文件", command=self.select_single_file, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text="📂 选择多个文件", command=self.select_multiple_files, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text="🗑️ 清空列表", command=self.clear_files, width=15).pack(side=tk.LEFT, padx=5)
        
        # 文件列表框架
        list_frame = ttk.LabelFrame(parent, text="已选择的文件", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        list_scroll = ttk.Scrollbar(list_frame)
        list_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.file_listbox = tk.Listbox(list_frame, yscrollcommand=list_scroll.set)
        self.file_listbox.pack(fill=tk.BOTH, expand=True)
        list_scroll.config(command=self.file_listbox.yview)
        
        # 提取按钮
        action_frame = ttk.Frame(parent, padding=10)
        action_frame.pack(fill=tk.X)
        
        ttk.Button(action_frame, text="🚀 从文件提取标签", command=self.extract_from_files, width=30).pack()
    
    def create_text_tab(self, parent):
        """创建HTML代码输入标签页"""
        # 说明标签
        info_frame = ttk.Frame(parent, padding=10)
        info_frame.pack(fill=tk.X)
        
        info_label = ttk.Label(info_frame, text="💡 提示：将 HTML 代码粘贴到下方文本框，然后点击「提取标签」按钮", 
                              foreground="blue")
        info_label.pack()
        
        # HTML 输入框架
        input_frame = ttk.LabelFrame(parent, text="HTML 代码输入区", padding=10)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.html_input = scrolledtext.ScrolledText(input_frame, height=15, font=("Consolas", 9), wrap=tk.WORD)
        self.html_input.pack(fill=tk.BOTH, expand=True)
        
        # 插入提示文本
        placeholder = """<!-- 在这里粘贴 HTML 代码 -->
<!-- 例如：-->
<a href="/tag/example">
  <span class="name">tag1</span>
  <span class="count">1234</span>
</a>
<a href="/tag/example2">
  <span class="name">tag2</span>
  <span class="count">567</span>
</a>"""
        self.html_input.insert(1.0, placeholder)
        self.html_input.config(foreground="gray")
        
        # 绑定焦点事件（实现 placeholder 效果）
        self.html_input.bind("<FocusIn>", self.on_html_input_focus_in)
        self.html_input.bind("<FocusOut>", self.on_html_input_focus_out)
        
        # 操作按钮
        action_frame = ttk.Frame(parent, padding=10)
        action_frame.pack(fill=tk.X)
        
        ttk.Button(action_frame, text="🚀 从代码提取标签", command=self.extract_from_text, width=30).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="🗑️ 清空输入", command=self.clear_html_input, width=20).pack(side=tk.LEFT, padx=5)
    
    def on_html_input_focus_in(self, event):
        """输入框获得焦点时"""
        if self.html_input.get(1.0, tk.END).strip().startswith("<!-- 在这里粘贴"):
            self.html_input.delete(1.0, tk.END)
            self.html_input.config(foreground="black")
    
    def on_html_input_focus_out(self, event):
        """输入框失去焦点时"""
        if not self.html_input.get(1.0, tk.END).strip():
            placeholder = """<!-- 在这里粘贴 HTML 代码 -->
<!-- 例如：-->
<a href="/tag/example">
  <span class="name">tag1</span>
  <span class="count">1234</span>
</a>
<a href="/tag/example2">
  <span class="name">tag2</span>
  <span class="count">567</span>
</a>"""
            self.html_input.insert(1.0, placeholder)
            self.html_input.config(foreground="gray")
    
    def select_single_file(self):
        """选择单个文件"""
        filename = filedialog.askopenfilename(
            title="选择 HTML 文件",
            filetypes=[("HTML 文件", "*.html *.htm"), ("所有文件", "*.*")]
        )
        if filename:
            self.html_files.append(filename)
            self.update_file_list()
    
    def select_multiple_files(self):
        """选择多个文件"""
        filenames = filedialog.askopenfilenames(
            title="选择多个 HTML 文件",
            filetypes=[("HTML 文件", "*.html *.htm"), ("所有文件", "*.*")]
        )
        if filenames:
            self.html_files.extend(filenames)
            self.update_file_list()
    
    def clear_files(self):
        """清空文件列表"""
        self.html_files = []
        self.update_file_list()
        self.status_label.config(text="文件列表已清空", foreground="gray")
    
    def update_file_list(self):
        """更新文件列表显示"""
        self.file_listbox.delete(0, tk.END)
        for filepath in self.html_files:
            filename = os.path.basename(filepath)
            self.file_listbox.insert(tk.END, filename)
        
        self.status_label.config(text=f"已选择 {len(self.html_files)} 个文件", foreground="blue")
    
    def clear_html_input(self):
        """清空HTML输入框"""
        self.html_input.delete(1.0, tk.END)
        self.html_input.config(foreground="black")
    
    def extract_from_files(self):
        """从文件提取标签"""
        if not self.html_files:
            messagebox.showwarning("警告", "请先选择 HTML 文件！")
            return
        
        all_tags = []
        separator = self.separator_entry.get()
        
        self.status_label.config(text="正在从文件提取标签...", foreground="orange")
        self.root.update()
        
        try:
            for filepath in self.html_files:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    
                    tags = self.extract_tags_from_html(html_content)
                    all_tags.extend(tags)
                
                except Exception as e:
                    messagebox.showerror("错误", f"处理文件 {os.path.basename(filepath)} 时出错:\n{str(e)}")
            
            # 去重
            all_tags = list(dict.fromkeys(all_tags))
            
            self.display_results(all_tags, separator)
        
        except Exception as e:
            self.status_label.config(text=f"❌ 提取失败", foreground="red")
            messagebox.showerror("错误", f"提取过程出错:\n{str(e)}")
    
    def extract_from_text(self):
        """从文本框提取标签"""
        html_content = self.html_input.get(1.0, tk.END).strip()
        
        if not html_content or html_content.startswith("<!-- 在这里粘贴"):
            messagebox.showwarning("警告", "请先粘贴 HTML 代码！")
            return
        
        separator = self.separator_entry.get()
        
        self.status_label.config(text="正在从代码提取标签...", foreground="orange")
        self.root.update()
        
        try:
            all_tags = self.extract_tags_from_html(html_content)
            self.display_results(all_tags, separator)
        
        except Exception as e:
            self.status_label.config(text=f"❌ 提取失败", foreground="red")
            messagebox.showerror("错误", f"提取过程出错:\n{str(e)}")
    
    def extract_tags_from_html(self, html_content):
        """从HTML内容中提取标签（包含计数）"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 查找所有包含 <span class="name"> 的 <a> 标签
        a_tags = soup.find_all('a', href=True)
        
        tags = []
        for a_tag in a_tags:
            # 在 <a> 标签内查找 name 和 count
            name_span = a_tag.find('span', class_='name')
            count_span = a_tag.find('span', class_='count')
            
            if name_span:
                tag_text = name_span.get_text().strip()
                
                # 如果有计数，添加括号标注
                if count_span:
                    count_text = count_span.get_text().strip()
                    full_tag = f"{tag_text} ({count_text})"
                else:
                    full_tag = tag_text
                
                # 去重（基于完整文本）
                if full_tag and full_tag not in tags:
                    tags.append(full_tag)
        
        return tags
    
    def display_results(self, tags, separator):
        """显示提取结果"""
        if tags:
            result = separator.join(tags)
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)
            
            self.extracted_tags = tags
            
            self.status_label.config(text=f"✓ 提取完成！共 {len(tags)} 个唯一标签", foreground="green")
            self.count_label.config(text=f"📊 {len(tags)} 个标签")
            
            messagebox.showinfo("成功", f"成功提取 {len(tags)} 个唯一标签！")
        else:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "未找到任何 <span class=\"name\"> 标签（需在 <a> 标签内）")
            self.status_label.config(text="⚠ 未找到任何标签", foreground="orange")
            messagebox.showwarning("警告", "未找到任何 <span class=\"name\"> 标签！")
    
    def save_to_file(self):
        """保存为文件"""
        if not self.extracted_tags:
            messagebox.showwarning("警告", "没有可保存的内容！请先提取标签。")
            return
        
        filename = filedialog.asksaveasfilename(
            title="保存标签文件",
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
            initialfile="tags.txt"
        )
        
        if filename:
            try:
                separator = self.separator_entry.get()
                content = separator.join(self.extracted_tags)
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                messagebox.showinfo("成功", f"已保存到:\n{filename}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败:\n{str(e)}")
    
    def copy_result(self):
        """复制结果到剪贴板"""
        result = self.result_text.get(1.0, tk.END).strip()
        if result and not result.startswith('未找到'):
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            messagebox.showinfo("成功", "结果已复制到剪贴板！")
        else:
            messagebox.showwarning("警告", "没有可复制的内容！")
    
    def clear_result(self):
        """清空结果"""
        self.result_text.delete(1.0, tk.END)
        self.extracted_tags = []
        self.status_label.config(text="结果已清空", foreground="gray")
        self.count_label.config(text="")


def main():
    root = tk.Tk()
    app = HTMLTagExtractorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
