# -*- coding: utf-8 -*-
# 实验室扫描仪只能扫单面, 这个脚本可以将正反面PDF合并成一个双面PDF

import pypdf

front_pdf_path = "1.pdf"
back_pdf_path = "2.pdf"
output_pdf_path = "3.pdf"
reverse_flag = False # 是否需要将正面页旋转180度


if __name__ == "__main__":
    front_reader = pypdf.PdfReader(front_pdf_path)
    back_reader = pypdf.PdfReader(back_pdf_path)
    writer = pypdf.PdfWriter()

    front_pages = len(front_reader.pages)
    back_pages = len(back_reader.pages)

    if front_pages != back_pages:
        raise ValueError(f"正面和反面PDF页数不一致! {front_pages}, {back_pages}")
    print(f"PDF页数: {front_pages}")

    for i in range(front_pages):
        if reverse_flag:
            front_reader.pages[i].rotate(180)
        writer.add_page(front_reader.pages[i])
        writer.add_page(back_reader.pages[back_pages - 1 - i]) # 背面页一般是反的, 需要反向遍历

    # 保存合并后的PDF
    with open(output_pdf_path, 'wb') as output_file:
        writer.write(output_file)

    print(f"\n✅ 合并完成！")
    print(f"📄 输出文件: {output_pdf_path}")
    print(f"📊 总页数: {len(writer.pages)}")
