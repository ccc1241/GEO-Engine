# 简介
本项目聚焦于初等几何教育领域，旨在设计并搭建一个面向中小学学生和教师的自动几何证明平台，目前已上传源代码及测试用数据集。<br>（开发手册待完善后上传）
# 模块介绍
data文件夹存放的GEO_data数据集<br>
Engine.py为推理引擎源代码<br>
Informations.py为推理引擎的几何实体库<br>
Lemmas.py为推理引擎的几何规则库<br>
api_test.py为外部接口调用模块<br>
# 依赖
Python 3.6+ <br>
torch 1.7.1<br>
transformers 4.8.2<br>
python3-pip<br>
Flask==2.0.1<br>
JPype1==1.4.1<br>
numpy==1.22.3<br>
opencv_python==4.7.0.72<br>
oss2==2.4.0<br>
pandas==1.4.2<br>
Requests==2.31.0<br>
sympy==1.10.1<br>
wolframclient==1.1.7<br>
Werkzeug==2.2.2<br>
# 运行GEO-engine
1、申请OpenAI的接口密钥、百度OCR的接口密钥，实现外部接口的调用<br>
2、下载Geometry3K数据集，https://drive.google.com/drive/folders/1d05WYXtlgKIoaPpK1v94LYph_heiXM7Z?usp=sharing<br>
3、安装必要的依赖<br>
4、使用Geometry3K数据集训练RetinaNet模型<br>
5、修改各文件的绝对路径<br>
6、运行Engine.py<br>
# Q&A
如果您遇到任何安装部署或者代码运行问题，请直接联系作者。:)
