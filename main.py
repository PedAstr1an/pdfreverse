import PyPDF2
import os

def reverse_pdf_pages(input_pdf, output_pdf):
    # 检查输入文件是否存在
    if not os.path.exists(input_pdf):
        print(f"错误：输入文件'{input_pdf}'不存在。")
        return

    try:
        # 打开输入的PDF文件
        with open(input_pdf, 'rb') as infile:
            reader = PyPDF2.PdfReader(infile)
            total_pages = len(reader.pages)

            # 创建一个PDF写入器
            writer = PyPDF2.PdfWriter()

            # 处理页数顺序
            if total_pages % 2 == 0:
                # 偶数页数：前半部分为奇数页，后半部分为偶数页反转
                odd_pages = list(range(0, total_pages, 2))  # 奇数页
                even_pages = list(range(1, total_pages, 2))  # 偶数页
                even_pages.reverse()  # 反转偶数页
                new_order = odd_pages + even_pages
            else:
                # 奇数页数：先按偶数规则反转，再加一个空白页
                odd_pages = list(range(0, total_pages, 2))  # 奇数页
                even_pages = list(range(1, total_pages, 2))  # 偶数页
                even_pages.reverse()  # 反转偶数页
                odd_pages.append(None)  # None代表空白页
                new_order = odd_pages + even_pages

            # 将重新排序的页面写入新的PDF
            for i in new_order:
                if i is None:
                    # 如果是空白页，使用add_blank_page方法
                    writer.add_blank_page(width=reader.pages[0].mediabox.width, height=reader.pages[0].mediabox.height)
                else:
                    writer.add_page(reader.pages[i])

            # 写入输出的PDF文件
            with open(output_pdf, 'wb') as outfile:
                writer.write(outfile)
            print(f"PDF文档已处理并保存为: {output_pdf}")
    except Exception as e:
        print(f"处理PDF时发生错误: {e}")

def process_pdfs_in_directory(directory):
    # 获取目录中所有后缀为.pdf的文件
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]

    if not pdf_files:
        print("错误：当前目录没有PDF文件。")
        return

    # 处理每个PDF文件
    for pdf_file in pdf_files:
        input_file = os.path.join(directory, pdf_file)
        output_file = os.path.join(directory, "print.pdf")
        reverse_pdf_pages(input_file, output_file)

# 获取当前程序根目录
current_directory = os.path.dirname(os.path.abspath(__file__))

# 处理目录中的PDF文件
process_pdfs_in_directory(current_directory)
