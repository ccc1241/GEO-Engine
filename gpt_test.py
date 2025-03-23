import requests
import random
import re

def call_gpt4_api(messages, temperature=0.1):
    # API接口的URL
    url = "https://research-cm.openai.azure.com/openai/deployments/GPT432K/chat/completions?api-version=2023-05-15"
    api_key = "your api key"

    # 设置请求头
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }

    # 请求的数据
    data = {
        "messages": messages,
        "temperature": temperature
    }
    # 发送POST请求
    response = requests.post(url, headers=headers, json=data)

    # 检查响应状态
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# 把HYPOTHESES开始CONCLUSION结尾的字符串提取出来并做分割
def string_parse(gpt_string):
    hypotheses_start = gpt_string.find("HYPOTHESES:")
    conclusion_end = hypotheses_start + gpt_string[hypotheses_start:].find('|') - 1
    hypotheses = re.split(r'[；;：:,，]', gpt_string[hypotheses_start:conclusion_end])
    hypotheses[0] += ':'
    hypotheses = [hyp.strip() for hyp in hypotheses if hyp.strip() != ""]

    if hypotheses_start == -1:  # 如果没有解析到就直接返回值退出方法
        return -1
    else:
        return hypotheses

# 把用到的点排序，并最后赋值给POINT字符串后面
def point_sort(parsed_string):
    letter_counts = {}
    start_point = parsed_string[1].find("POINT")
    # 防止把point的第一个字母也作为一个约束来解析
    if start_point != -1:
        for statement in parsed_string[2:-1]:
            # 分出每个字母
            letters = statement.split()
            # 记录字母的使用次数
            for letter in letters[1:]:
                letter_counts[letter] = letter_counts.get(letter, 0) + 1
        points = "POINT "
        # 按值从大到小排序字典，并获取排序后的键
        sorted_letters = sorted(letter_counts, key=letter_counts.get, reverse=True)
        # 将排序后的键加到points后面
        points += ' '.join(sorted_letters)
        parsed_string[1] = points
        return parsed_string
    else:
        return parsed_string

def convert_to_example_thm(hypotheses):
    # 从数据结构生成第二种形式的字符串
    example_thm_str = "EXAMPLE THM\n"
    for i, hyp in enumerate(hypotheses):
        if i == len(hypotheses) - 1:
            # 最后一行把'CONCLUSION='替换为'SHOW:'
            hyp = hyp.replace('CONCLUSION=', 'SHOW:')
        example_thm_str += f"{hyp}\n"

    # 获取点的数量
    points = hypotheses[1].split(' ')[1:]

    # 生成随机坐标并添加到最后一行
    random_coordinates = generate_random_coordinates(points)
    example_thm_str += "  ".join(random_coordinates)

    return example_thm_str

def generate_random_coordinates(points):
    # 生成在100到500之间的随机坐标，保留 +5 和 -20 不变
    coordinates = []
    for point in points:
        x = random.randint(100, 500)
        y = random.randint(100, 500)
        coordinates.append(f"{point}({x}+5,{y}-20)")
    return coordinates



# 定义你的提示字符串
# INTERSECTION_LL A B C D M | 线段AB和线段CD相交于点M
system_prompt = r"""
    作为一名几何数学专家解析几何数学题目，你的任务首先是找出题目中包含的几何元素，如点、线段和多边形信息。
    在此基础上，归纳上述几何元素之间的几何关系,如正交、平行、垂直、共圆。
    请将按照题目在第一列，几何关系在第二列的格式输出至表格中，
    例子1: 
    输入题目：AB的中点是F，DE的中点是C，BE⊥EA，BD⊥DA，请证明：FC⊥DE.
    输出：| 题目 | 几何关系 |
    | :--- | :--- |
    | AB的中点是F，DE的中点是C，BE⊥EA，BD⊥DA，请证明：FC⊥DE.  | HYPOTHESES: POINT A B C D E F；VERTI E B A E；VERTI D B A D；MID F B A；MID C D E, CONCLUSION： VERTI F C D E |
    下面我将给你一组构造语句，每个构造语句后面都有相应的几何关系
    POINT A | 点A
    EQ_LINE A B C D | 线段AB等于线段CD
    RATIO_LINE A B C D n m | 线段AB和线段CD成比例且AB/CD=n/m
    ANGLE A B C α | 角ABC的角度为α°
    BI_ANGLE A B C D E | DE是角ABC的角平分线
    R_ANGLE A B C | 角ABC是直角，∠ABC=90°
    EQ_ANGLE A B C D E F | ∠ABC = ∠DEF
    COMP_ANGLE A B C D E F | ∠ABC与∠DEF互补
    COTER_ANGLE A B C D E F | ∠ABC与∠DEF互余
    RATIO_ANGLE A B C D E F n m | 角ABC和角DEF成比例且∠ABC/∠DEF=n/m
    MID O A B | 点O是线段AB的中点
    VERTI E B A E | 直线BE⊥EA
    PARALLEL A B C D | AB平行CD
    INTERSECTION_LL	A B C D E | 线段AB与线段CD的交点是E
    R_TRIANGLE A B C | A,B,C组成了一个直角三角形
    EQ_TRIANGLE A B C D E F | 三角形ABC全等于三角形DEF
    SIM_TRIANGLE A B C D E F | 三角形ABC相似于三角形DEF
    ISO_TRIANGLE A B C | A,B,C组成了一个等腰三角形且AB=AC
    REGU_TRIANGLE A B C | 等边三角形ABC
    IR_TRIANGLE A B C | A,B,C组成了一个等腰直角三角形且BC是直角边
    PARALLELOGRAM A B C D | 平行四边形ABCD
    RECTANGLE A B C D | 矩形ABCD
    SQUARE A B C D | 正方形ABCD
    CIRCLE A B C D | 圆内接四边形ABCD
    
    注意事项：
    1.POINT是在统计题目中出现过的所有点。
    2.请不要使用没有提到的构造语句。
    3.CO_LINE只能用于表示三个点，不能表示多个点。
    
    下面我将给出一组几何数学题，请你模仿上面给出的例子，使用表中提供的所有构造语句，注意事项，找出题目中包含的几何元素，如点、线段和多边形信息，并输出至表格中。
    """

def get_system_prompt():
    return system_prompt

if __name__ == "__main__":

    print(123)
    exit()
    print(3)
    # 初始化对话历史并添加提示字符串
    messages = [{"role": "system", "content": get_system_prompt()}]

    while True:
        prompt_text = input("\n请输入提示文本（或输入'exit'退出）：")

        # 检查是否为退出命令
        if prompt_text.lower() == 'exit':
            print("程序已退出。")
            break

        # 添加用户的消息到对话历史
        messages.append({"role": "user", "content": prompt_text})

        # 获取GPT-4的响应
        assistant_reply = call_gpt4_api(messages)
        if assistant_reply:
            print("\nGPT-4的回复:", assistant_reply)
            # 添加GPT-4的响应到对话历史
            messages.append({"role": "assistant", "content": assistant_reply})

        # 输出解析到的条件和结论
        parsed_string = string_parse(assistant_reply)
        if parsed_string != -1:
            output_chat = convert_to_example_thm(parsed_string)
            with open("gpt_output.txt", "w", encoding="utf-8") as file:
                file.write(output_chat)
            java_use()



"""作为一名几何数学专家解析几何数学题目，你的任务是找出题目中包含的几何元素，如点、线段和多边形信息。
    在此基础上，归纳上述几何元素之间的几何关系,如正交、平行、垂直、共圆。
    请将按照题目在第一列，几何关系在第二列的格式输出至表格中，
    例子: 
    输入题目：在矩形ABCD中,点E是AD的中点,过A,E,C三点的圆交直线CD于另一点F.求证:AF⊥BE.
    输出：| 题目 | 几何关系 |
    | :--- | :--- |
    | 在矩形ABCD中,点E是AD的中点,过A,E,C三点的圆交直线CD于另一点F.求证:AF⊥BE.  | HYPOTHESES: POINT A B C D E F；RECTANGLE A B C D；MIDPOINT E A D；CIRCUMCENTER O A E C；ON_LINE F C D；ON_CIRCLE F O A, CONCLUSION= PERPENDICULAR A F B E |
    接下来我会给你一组题目和几何关系供你学习参考
    | 在△ABC中，AB=AC，延长AB到E，使得BE=AB，D是AB中点，求证：CE=2*CD.   |  HYPOTHESES: POINT A B C D E； ISO_TRIANGLE A B C；MIDPOINT D A B；MIDPOINT B A E, CONCLUSION= RATIO C D C E 1 2 |
    | 在△ABC中，D是BC上的点，若AB⊥AC，AD⊥BC，求证:BA^2=BC*BD.   | HYPOTHESES: TRIANGLE A B C；ON_LINE D B C；ON_TLINE D A B C；ON_TLINE A B A C, CONCLUSION= EQ_PRODUCT A B A B B C B D |
    | 在△ABC中,BC=AC,点D为AB的中点,连结CD,点E为CD的中点,作DG⊥AE于点G,点F为BC的中点,连结GF,DF,求证：GF=DF. | HYPOTHESES: POINT A B C D E F G；ISO_TRIANGLE C A B；MIDPOINT D B A；MIDPOINT E D C；MIDPOINT F B C；FOOT G D A E, CONCLUSION= EQDISTANCE G F D F |
    | 在三角形ABC中，中线AD、BE交于G，延长BA至F，使得AB=AF，DA⊥BE求证：GF=CA. | HYPOTHESES: POINT A B C D E F G；TRIANGLE A B C；MIDPOINT D B C；MIDPOINT E A C；INTERSECTION_LL G A D B E；MIDPOINT A B F；ON_TLINE D A B E, CONCLUSION= EQDISTANCE F G A C |
    | 在梯形ABCD中,AB∥CD. 在较长的底边CD上取一点G,使DG等于梯形的中位线长.求证:AC⊥BD的充要条件是BG也等于其中位线长. | HYPOTHESES: POINT A B C D E F G；TRAPEZOID A B C D；ON_TLINE A C B D；MIDPOINT E D A；MIDPOINT F C B；PRATIO G D E F 1 1, CONCLUSION= EQDISTANCE B G E F |
    | 在梯形ABCD中，AB∥DC，CD=3*BA，点E位于BD上,且BE=2/3*DE，AD⊥CE，证明: AC=CD | HYPOTHESES: POINT A B C D E；ON_TLINE A D C E；PRATIO D C A B 3 1；LRATIO E B E D 2 3, CONCLUSION= EQDISTANCE C A C D |
    | 在△ABE中,AB=3BE,C、D为边AB上两点,且满足CD=AC=BD,点F是AE的中点，证明:∠CDF=90°. | HYPOTHESES: POINT A B C D E F；LRATIO C A C B 1 2；LRATIO D B D A 1 2；CIRCLE B D；ON_CIRCLE E B D；MIDPOINT F E A, CONCLUSION= PERPENDICULAR C F D F |
    | 在△GAB中，D、C是GA、GB上的点，且B、C、D、A四点共圆，O1是△GDC的外心，求证：GO1⊥AB. | HYPOTHESES: POINT A B C O D G O1；CIRCUMCENTER O A B C；ON_CIRCLE D O A；ON_PLINE G D D A；ON_PLINE G C C B；CIRCUMCENTER O1 D C G, CONCLUSION= PERPENDICULAR G O1 A B |
    | 在△ABC中，D是AC的中点，E是BC上的点，且2BE=EC，求证：AB⊥AC AE=2/3*BD. | HYPOTHESES: POINT A B C D E；R_TRIANGLE A B C；MIDPOINT D C A；LRATIO E B E C A B, CONCLUSION= RATIO A E B D 3 2 |
    | 在△ABC中，AC=BC，D是AB中点，E是BD中点，点F将边BC分为3:1（由顶点C算起）,证明：AE=DF. | HYPOTHESES: POINT A B C D E F；ISO_TRIANGLE C A B；MIDPOINT D A C；MIDPOINT E B D；LRATIO F B F C 1 3, CONCLUSION= EQDISTANCE A E D F |
    | 在△ABC中，CB=AC，CB⊥DB，E在AB上，且DB=DE，求证：AC⊥DE. | HYPOTHESES: POINT A B C D E；ISO_TRIANGLE C A B；ON_TLINE D B C B；CIRCLE D B；INTERSECTION_LC E A B D B, CONCLUSION= PERPENDICULAR D E A C |
    | 在△ABC中，BA⊥CB，BC=2AC，D为BC中点，E为AD上一点，且AE:ED=1:2. 求证BE⊥AC. | HYPOTHESES: POINT A B C D E；TRATIO C B A B 2 1；MIDPOINT D C B；LRATIO E A E D 1 2, CONCLUSION= PERPENDICULAR B E A C |
    | 线段AE上有点B,在线段AE的同侧作正方形ABCD、BEFG，求证：AG⊥CE. | HYPOTHESES: POINT A B C D E F G；SQUARE A B C D；SQUARE B E F G, CONCLUSION= PERPENDICULAR A G C E |
    | 由三角形ABC的两边向外做正方形ABED、正方形BCGF，P是平面内一点，如果PD⊥CB、PG⊥AB，求证PB⊥AC. | HYPOTHESES: POINT A B C D E F G P；TRIANGLE A B C；SQUARE A B D E；SQUARE B C F G；ON_TLINE B C P E；ON_TLINE B A P F, CONCLUSION= PERPENDICULAR P B A C |
    | 在梯形ABCD中,AC//BD，∠ABD=90°,对角线BC⊥DC，求证: BC^2=AC*BD.  | HYPOTHESES: POINT A B C D；ON_TLINE D B B A；ON_TLINE C A B A；ON_TLINE D C C B, CONCLUSION= EQ_PRODUCT B C B C A C B D |
    | 圆内接平行四边形BCDE, CE交BD于A. 求证：DE⊥BE.  | HYPOTHESES: POINT A B C D E；CIRCLE A B；ON_CIRCLE C A B；ON_CIRCLE D A B；PRATIO E D C B 1 1, CONCLUSION= PERPENDICULAR D E B E |
    | 已知:正方形 ABCD 及等边三角形EDC 如图位置放置，连接 AE，BE。求证:AE=BE  | HYPOTHESES: POINT A B C D E；SQUARE A B C D；EQ_TRIANGLE E A B, CONCLUSION= EQDISTANCE D E C E |
    | 设E为正方形ABCD边AB的中点，EF⊥CE,交AD于F.求证:∠BCE=∠ECF  | HYPOTHESES: POINT A B C D E F；SQUARE A B C D；MIDPOINT E B A；ON_TLINE F E E C；ON_LINE F A D, CONCLUSION= EQANGLE B C C E E C C F |
    | 在⊙ B中，点 E是直径 AC 延长线上一点，过点 E 作⊙ B 的切线，切点为 D ，连接 CD .求证： ∠A = ∠EDC  | HYPOTHESES: POINT A B C D E；CIRCLE B A；INTERSECTION_LC C A B B A；ON_CIRCLE D B A；ON_TLINE E D D B；ON_LINE E A B, CONCLUSION= EQANGLE B A A D C D D E |
    | AD 是△ ABC 的中线， E 是 AD 的中点， F 是 BE 延长线与 AC 的交点，求证AF：FC=1：2  | HYPOTHESES: POINT A B C D E F；TRIANGLE A B C；MIDPOINT D C B；MIDPOINT E D A；INTERSECTION_LL F A C B E, CONCLUSION= RATIO A F C F 1 2 |
    | EA 和 ED 分别与⊙ B 相切于 A、D两点，作直径 AC 并延长，交 ED 的延长线于点 F ，连接 BE , CD .求证： BE //CD  | HYPOTHESES: POINT A B C D E F；CIRCLE B A；INTERSECTION_LC C A B B A；ON_TLINE E A B A；ON_CIRCLE D B A；ON_TLINE E D D B；INTERSECTION_LL F A B D E, CONCLUSION= PARALLEL C D B E |
    | 从圆D外一定点D两切线DB. DC,设切点弦BC交DA于E,过E任引一弦FG,求证DA平分∠GDF.  | HYPOTHESES: POINT A B C D E F G；CIRCLE A B；ON_CIRCLE C A B；ON_TLINE D B B A；ON_TLINE D C C A；INTERSECTION_LL E A D B C；ON_CIRCLE F A B；INTERSECTION_LC G E F A B, CONCLUSION= EQANGLE F D D A A D D G |
    | 在 Rt △ ABC 中， ∠ACB =90°, D 为边 AC 上一点， DE⊥AB 于点 E,F 为 BD 的中点，CF的延长线交 AB 于点 G 求证： CF = EF  | HYPOTHESES: POINT A B C D E F G；R_TRIANGLE C A B；ON_LINE D A C；FOOT E D A B；MIDPOINT F B D；INTERSECTION_LL G A B C F, CONCLUSION= EQDISTANCE C F E F |
    | 三角形ABC的边BC的中点为D，过A的任意一条直线AF⊥BF于点F，CG⊥AF于点G，求证：DG=DF  | HYPOTHESES: POINT A B C E D F G；MIDPOINT D C B；FOOT F B A E；FOOT G C A E, CONCLUSION= EQDISTANCE D G D F |
    | 从Rt△ABC两边AB,AC各向外作正方形ABDE、ACFG,连CD、BF各交AB、AC于X、Y,则AX=AY.  | HYPOTHESES: POINT A B C D E F G H I；R_TRIANGLE C A B；SQUARE C B D E；SQUARE C A F G；INTERSECTION_LL H A D B C；INTERSECTION_LL I A C B F, CONCLUSION= EQDISTANCE C H C I |
    | AB 是⊙ C的直径， DE 是⊙ C的弦，过点 A 作 AF⊥ED 于点 F ，过点 B 作 BG⊥ED 于点 G ．求证： DF = GE  | HYPOTHESES: POINT A B C D E F G；ON_LINE C A B；CIRCLE C A；ON_CIRCLE D C A；ON_CIRCLE E C A；FOOT F A D E；FOOT G B D E, CONCLUSION= EQDISTANCE D F G E |
    | 在△ ABC 中， D 为 BC 的中点， E 为 AB 上一点， AE : BE =1:2, AD 与 CE 交于点 F，则 AD : DF =2:1  | HYPOTHESES: POINT A B C D E F；TRIANGLE A B C；MIDPOINT D C B；LRATIO E A E B 1 2；INTERSECTION_LL F A D C E, CONCLUSION= RATIO A D F D 2 1 |
    | 在等边三角形 ABC 中， D 是 AC 的中点， EF是 BC 延长线上的一点，且 CF = CD , DE⊥BC ，垂足为 E 求证： E 是 BF 的中点  | HYPOTHESES: POINT A B C D E F；EQ_TRIANGLE C A B；MIDPOINT D C A；FOOT E D B C；ON_ALINE F C B B C B；EQDISTANCE D C C F, CONCLUSION= EQDISTANCE B E E F |
    | BD 是△ ABC 的中线，点 E 在 BD 上，延长 AE交 BC 于点 F ．若 BE =3DE，则求证BF：FC=3:2  | HYPOTHESES: POINT A B C D E F；TRIANGLE A B C；MIDPOINT D C A；LRATIO E D E B 1 3；INTERSECTION_LL F A E B C, CONCLUSION= RATIO B F F C 3 2 |
    | 已知：在正方形 ABCD 的边 BC 上任取一点 E ，连接 AE ，一条与 AE 垂直的直线l（垂足为点 F）沿 AFE方向，从点 A 开始向下平移，当直线l经过 AE的中点时，设l与对角线 BD 交于点 G ，连接 GE ，如图所示，求∠ FEG的度数是否为45°。 | HYPOTHESES: POINT A B C D E F G；SQUARE A B C D；ON_LINE E B C；MIDPOINT F E A；ON_TLINE G F E A；ON_LINE G B D, CONCLUSION= S_ANGLE A E E G 45 |
    | AC是⊙ B 的直径，过⊙ B外一点 F 作⊙ B的两条切线 FD , FE ，切点分别为 E , D ，连接 BF , ED .求证： DE⊥BF | HYPOTHESES: POINT A B C D E F；CIRCLE B A；INTERSECTION_LC C A B B A；ON_CIRCLE D B A；ON_CIRCLE E B A；ON_TLINE F D D B；ON_TLINE F E E B, CONCLUSION= PERPENDICULAR D E B F |
    | 用Rt△ABC一腰AC为直径作圆;交斜边BC于D，则过D的切线平分AB. | HYPOTHESES: POINT A B C D E F；R_TRIANGLE C A B；ON_LINE D B C；CIRCLE D C；INTERSECTION_LC E A B D C；ON_LINE F A C；ON_TLINE F E E D, CONCLUSION= EQDISTANCE A F F C |
    | 在矩形ABCD中，E是AD的中点，延长CE，BA相交于点F，连接AC，DF。求证：三角形AFC全等于三角形DCF。 | HYPOTHESES: POINT A B C D E F G；SQUARE A B C D；ON_LINE E B C；FOOT F B A E；ON_PLINE G F F B；ON_LINE G D C, CONCLUSION= CON_TRIANGLE A F C D C F |
    | 已知，D为BC上一点，E 、 F分别为圆ABD 、 圆ACD的圆心，求证: 三角形ABC与三角形DEF相似 | HYPOTHESES: POINT A B C D O O1；ON_LINE D B C；CIRCUMCENTER O A D B；CIRCUMCENTER O1 A D C, CONCLUSION= SIM_TRIANGLE D O1 O A C B |
    | C为线段AB 上一点,分别以AC,CB 为一边在AB 的同侧作正三角形ACD与正三角形ECB.求证:AE =DB. | HYPOTHESES: POINT A B C D E；ON_LINE C A B；EQ_TRIANGLE D C B；EQ_TRIANGLE E A C, CONCLUSION= EQDISTANCE E B A D |
    | 已知:三角形ABC中,AB=AC，BAC=90°，AD为BC 边上的高线,E为BC边上一点,EF 垂直AC,F为垂足,EG 垂直AB,G为垂足求证;DG=DF | HYPOTHESES: POINT A B C D E F G；ON_TLINE C A C B；ON_BLINE C A B；FOOT D C A B；ON_LINE E A B；FOOT F E B C；FOOT G E A C, CONCLUSION= EQDISTANCE D G D F |
    | 已知三角形ABC中，AE=EC,AF =FB,BE,CF 相交于G，求证:BG=2GE | HYPOTHESES: POINT A B C D E F；TRIANGLE A B C；MIDPOINT D C A；MIDPOINT E B A；INTERSECTION_LL F B D C E, CONCLUSION= RATIO B F F D 2 1 |
    | 正方形ABCD中,E为AB 上一点,F为BC上一点,且BE=BF,自B作BG⊥EC,G为垂足求证:DG⊥FG | HYPOTHESES: POINT A B C D E F G；SQUARE A B C D；ON_LINE E A B；TRATIO F B E B 1 1；FOOT G B C E, CONCLUSION=  PERPENDICULAR F G G D |
    | AB,AC为圆A的半径,D,E分别为 AC,AB 的中点求证:BD = CE. | HYPOTHESES: POINT A B C D E；CIRCLE A B；ON_CIRCLE C A B；MIDPOINT D C A；MIDPOINT E B A, CONCLUSION= EQDISTANCE D B C E |
    | △ABC的高AE和BD相交于 G, AE的延长线交外接圆O于点F求证:E为FG的中点. | HYPOTHESES: POINT A B C D E O F G；TRIANGLE A B C；FOOT D B A C；FOOT E A B C；CIRCUMCENTER O A B C；INTERSECTION_LC F A E O A；INTERSECTION_LL G A E B D, CONCLUSION= EQDISTANCE G E E F |
    | 已知ACBD 是圆内接四边形，∠ACB =90°,过点D作AB,CB的垂线，垂足分别为点 E,F，EF与DC交点为G求证:EF平分DC | HYPOTHESES: POINT A B C O D E F G；R_TRIANGLE C A B；CIRCUMCENTER O A C B；ON_CIRCLE D O A；FOOT E D A B；FOOT F D B C；INTERSECTION_LL G C D E F, CONCLUSION= EQDISTANCE D G C G |
    | DC , DB 分别与⊙ A 相切于点 C , B ，点 E在 DC 上，且 AE // BD 、 EF⊥BD ，垂足为点 F .求证： AE = BF | HYPOTHESES: POINT A B C D E F；CIRCLE A B；ON_CIRCLE C A B；ON_TLINE D C C A；ON_TLINE D B B A；ON_PLINE E A D B；ON_LINE E C D；FOOT F E B D, CONCLUSION= EQDISTANCE A E B F |
    | 设D、F、E顺序为△ABC三边中点，求证圆ABC在A点的切线AG与圆DFE在F点的切线FH平行。 | HYPOTHESES:；POINT A B C D E F O O1 G H；TRIANGLE A B C；MIDPOINT D B A；MIDPOINT E C A；MIDPOINT F B C；CIRCUMCENTER O B A C；CIRCUMCENTER O1 F D E；ON_TLINE G A O A；ON_TLINE H F O1 F, CONCLUSION= PARALLEL A G F H |
    | BC 是⊙ C 的直径， DB 为⊙ A 的弦， AE⊥BC , AE 与 BD 的延长线交于点 E ，过点 D的切线交 AE 于点 F .求证：∠FED =∠ACD | HYPOTHESES: POINT A B C D E F；CIRCLE A B；INTERSECTION_LC C A B A B；ON_CIRCLE D A B；ON_TLINE E A B A；ON_LINE E B D；ON_TLINE F D D A；ON_LINE F A E, CONCLUSION= EQANGLE B C C D B E E A |
    | 圆C和圆A相交于点E和点B,AC的延长线交 C于点D,DE,DB 的延长线分别和A相交于点 F,G.求证:EF =BG | HYPOTHESES: POINT A B C D E F G；CIRCLE A B；CIRCLE C B；INTERSECTION_LC D A C C B；INTERSECTION_CC E A B C B；INTERSECTION_LC F D E A B；INTERSECTION_LC G B D A B, CONCLUSION= EQDISTANCE F E B G |
    | D是△ABC的垂心,F、E分别在AC、AB上，且B、𝐶、𝐸、F共圆，BF、CE交于点G，BF、CE的中点分别为H、I，求证：HI⊥DG. | HYPOTHESES: POINT A B C D E O F G H I；TRIANGLE A B C；ORTHOCENTER D A B C；ON_LINE E A B；CIRCUMCENTER O B E C；INTERSECTION_LC F A C O B；INTERSECTION_LL G B F C E；MIDPOINT H F B；MIDPOINT I C E, CONCLUSION= PERPENDICULAR G D H I |
    | F是BA的中点，C是DE的中点，BD⊥DA，BE⊥EA. 求证：FC⊥DE. | HYPOTHESES: POINT A B C D E F；MIDPOINT F B A；R_TRIANGLE D A B；R_TRIANGLE E A B；MIDPOINT C E D, CONCLUSION= PERPENDICULAR F C D E |
    下面我将给出一组几何数学题，请你模仿上面给出的例子，找出题目中包含的几何元素，如点、线段和多边形信息，并输出至表格中。
    
    
    
        5.PERPENDICULAR只能用于待证结论CONCLUSION中，不能作为构造语句使用，请使用ON_TLINE。
"""



# 2023/9/24版本，倒数第二题可以通过测试
r"""
    作为一名几何数学专家解析几何数学题目，你的任务是找出题目中包含的几何元素，如点、线段和多边形信息。
    在此基础上，归纳上述几何元素之间的几何关系,如正交、平行、垂直、共圆。
    请将按照题目在第一列，几何关系在第二列的格式输出至表格中，
    例子: 
    输入题目：AB的中点是F，DE的中点C，BE⊥EA，BD⊥DA，请证明：FC⊥DE.
    输出：| 题目 | 几何关系 |
    | :--- | :--- |
    | AB的中点是F，DE的中点C，BE⊥EA，BD⊥DA，请证明：FC⊥DE.  | HYPOTHESES: POINT A B；FOOT D B A D；FOOT E B A E；MIDPOINT F B A；MIDPOINT C D E, CONCLUSION= PERPENDICULAR F C D E |
    下面我将给你一组只能在HYPOTHESES使用的构造语句，每一个构造语句后面都有相应的中文解释，请按照这些构造语句的规则来解析题目：
    POINT A	构造自由点A
    ON_LINE C A B	约束点C在直线AB上
    ON_CIRCLE C A B	约束点C在圆AB上
    ON_PLINE D C A B	约束点D在过C点平行于AB的直线上
    ON_TLINE D C A B	约束点D在过C点垂直于AB的直线上
    FOOT E B A E	直线BE垂直于直线EA，垂足E为约束点
    ON_BLINE C A B	约束点C在AB的垂直平分线上
    ON_ALINE D1 C1 A1 B1 A B C D	约束点D1是过C1点且和直线A1B1成角度α的直线上的一点，且α=∠[AB,CD]
    ON_RCIRCLE D C A B	约束点D在以C为圆心，以AB为半径的圆上
    MIDPOINT O A B	约束点O是线段AB的中点
    LRATIO P A B n m	约束点P在直线AB上且AP/PB=n/m, n和m为整数
    PRATIO P C A B n m	CP∥AB且CP/AB = n/m,P为约束点，n和m为整数
    TRATIO P C A B n m	CP⊥AB且CP/AB = n/m,P为约束点， n和m为整数
    CENTROID O A B C	约束点O是三角形ABC的重心
    ORTHOCENTER O A B C	   约束点O是三角形ABC的垂心
    CIRCUMCENTER O A B C	约束点O是三角形ABC的外心
    INCENTER O A B C	约束点O是三角形ABC的内心
    INTERSECTION_LP F A B C D E	   约束点F是直线AB和过C点平行于CD直线的交点
    INTERSECTION_LT F A B C D E	   约束点F是直线AB和过C点垂直于CD直线的交点
    INTERSECTION_LC E A B C D	约束点E是直线AB和圆CD的交点
    INTERSECTION_CC E A B C D	约束点E是圆AB和圆CD的交点
    R_TRIANGLE A B C	直线AB与AC交于约束点A，角CAB为直角的直角三角形

    下面我将给你一组待证结论CONCLUSION中使用的语句，请不要在HYPOTHESES中使用：
    PERPENDICULAR D E B F   求证DE⊥BF
    RATIO A F C F 1 2   求证AF：FC=1：2
    EQDISTANCE A B C D	AB与CD长度相等

    需要注意的是：
    1.POINT语句会构造自由点（不受任何约束），而其他构造语句的第一个字母都代表约束点（受到构造语句定义的规则约束）。
    2.除了POINT语句，每个构造语句的第一个点都代表着要构造的新点，后面的所有点都代表着已有的点。
    3.请不要对一个点进行两次构造。
    4.请不要用POINT构造约束点。
    5.请不要使用上面没有提到的构造语句。

    下面我将给出一组几何数学题，请你模仿上面给出的例子，使用提供的所有构造语句，找出题目中包含的几何元素，如点、线段和多边形信息，并输出至表格中。
    """


"""2023/9/26 还是分不清白约束点和自由点，下面尝试把每一条规则写上约束点
    作为一名几何数学专家解析几何数学题目，你的任务是找出题目中包含的几何元素，如点、线段和多边形信息。
    在此基础上，归纳上述几何元素之间的几何关系,如正交、平行、垂直、共圆。
    请将按照题目在第一列，几何关系在第二列的格式输出至表格中，
    例子1: 
    输入题目：AB的中点是F，DE的中点是C，BE⊥EA，BD⊥DA，请证明：FC⊥DE.
    输出：| 题目 | 几何关系 |
    | :--- | :--- |
    | AB的中点是F，DE的中点是C，BE⊥EA，BD⊥DA，请证明：FC⊥DE.  | HYPOTHESES: POINT A B；FOOT D B A D；FOOT E B A E；MIDPOINT F B A；MIDPOINT C D E, CONCLUSION= PERPENDICULAR F C D E |
    注意：例子1中，因为A、B没有出现在其他构造语句的第一位字母中，所以A、B为自由点，因为D、E、F、C都是构造语句的第一个字母，所以D、E、F、C为约束点。
    例子2:
    输入题目：圆内接平行四边形BCDE, CE交BD于A. 求证：DE⊥BE.
    输出：| 题目 | 几何关系 |
    | :--- | :--- |
    | 圆内接平行四边形BCDE, CE交BD于A. 求证：DE⊥BE.  | HYPOTHESES: POINT A B C D E；CIRCLE A B；ON_CIRCLE C A B；ON_CIRCLE D A B；PRATIO E D C B 1 1, CONCLUSION= PERPENDICULAR D E B E |

    下面我将给你一组只能在HYPOTHESES使用的构造语句，每个构造语句后面都有相应的几何关系
    构造语句 | 几何关系
    POINT A	| 构造一个自由点A
    ON_LINE C A B | C在直线AB上
    ON_CIRCLE C A B	| C在圆AB上
    ON_PLINE D C A B | D在过C点平行于AB的直线上
    ON_TLINE D C A B | D在过C点垂直于AB的直线上
    ON_BLINE C A B | C在AB的垂直平分线上
    ON_ALINE D1 C1 A1 B1 A B C D | D1是过C1点且和直线A1B1成角度α的直线上的一点，且α=∠[AB,CD]
    ON_RCIRCLE D C A B | D在以C为圆心，以AB为半径的圆上
    MIDPOINT O A B | O是线段AB的中点
    LRATIO P A B n m | P在直线AB上且AP/PB=n/m, n和m为整数
    PRATIO P C A B n m | CP∥AB且CP/AB = n/m, n和m为整数
    TRATIO P C A B n m | CP⊥AB且CP/AB = n/m, n和m为整数
    CENTROID O A B C | O是三角形ABC的重心
    ORTHOCENTER O A B C | O是三角形ABC的垂心
    CIRCUMCENTER O A B C | O是三角形ABC的外心，A、B、C三点在圆O上
    INCENTER O A B C | O是三角形ABC的内心
    INTERSECTION_LP F A B C D E	| F是直线AB和过C点平行于CD直线的交点
    INTERSECTION_LT F A B C D E	| F是直线AB和过C点垂直于CD直线的交点
    INTERSECTION_LC E A B C D | E是直线AB和圆CD的交点
    INTERSECTION_CC E A B C D | E是圆AB和圆CD的交点

    CIRCUMCENTER D A B C | A、B、C在以D为圆心的圆上
    CIRCLE A B | 以A为圆心，B为圆上一点做一个圆
    TRIANGLE A B C | A,B,C组成了一个三角形
    R_TRIANGLE A B C | 直线AB与AC交于点A，角CAB为直角的直角三角形
    ISO_TRIANGLE C A B | CA=CB，且A，B，C不共线;
    FOOT E B A E | BE⊥EA，E为垂足
    EQ_TRIANGLE A B C | AB=BC=CA,∠ABC=∠CAB=∠BCA=60°,A,B,C不共线且是逆时钟排序的:
    TRAPEZOID A B C D | AB∥CD且AB和CD有同样的方向，这等价于AB和CD是平行的;
    PARALLELOGRAM A B C D | AB∥CD，BC∥AD，A，B，C不共线
    RECTANGLE A B C D | A，B，C，D是平行四边形且DA⊥BA
    SQUARE A B C D | A，B，C，D是矩形并且AB= AD:

    下一条语句为复合构造语句
    CIRCLE O1 D；ON_CIRCLE C O1 D；ON_CIRCLE B O1 D；ON_CIRCLE A O1 D | 圆内接四边形BCAD

    下面我将给你一组待证结论CONCLUSION中使用的构造语句，请不要在HYPOTHESES中使用：
    PERPENDICULAR D E B F | 求证DE⊥BF
    RATIO A F C F 1 2 | 求证AF：FC=1：2
    EQDISTANCE A B C D | AB与CD长度相等

    注意事项：
    1.构造语句的第一个字母都代表受到构造规则约束的点，无须加在POINT语句中。
    2.构造语句后面的第一个字母也代表即将构造的点，其余字母都代表已经构造的点。
    3.请不要对一个点进行两次约束。
    4.请不要使用没有提到的构造语句。
    5.不在构造语句的第一个字母的都是自由点，需要使用POINT语句构造

    下面我将给出一组几何数学题，请你模仿上面给出的例子，使用表中提供的所有构造语句，注意事项，找出题目中包含的几何元素，如点、线段和多边形信息，并输出至表格中。
    """

# # 2024/01/20修改之前用的提示，保留旧版本
# system_prompt = r"""
#     作为一名几何数学专家解析几何数学题目，你的任务首先是找出题目中包含的LaTeX格式的语句，并转为普通语句，然后找出题目中包含的几何元素，如点、线段和多边形信息。
#     在此基础上，归纳上述几何元素之间的几何关系,如正交、平行、垂直、共圆。
#     请将按照题目在第一列，几何关系在第二列的格式输出至表格中，
#     例子1:
#     输入题目：AB的中点是F，DE的中点是C，BE⊥EA，BD⊥DA，请证明：FC⊥DE.
#     输出：| 题目 | 几何关系 |
#     | :--- | :--- |
#     | AB的中点是F，DE的中点是C，BE⊥EA，BD⊥DA，请证明：FC⊥DE.  | HYPOTHESES: POINT A B；FOOT E B A E；FOOT D B A D；MIDPOINT F B A；MIDPOINT C D E, CONCLUSION= PERPENDICULAR F C D E |
#     注意：例子1中，因为E点在BE⊥EA出现两次，D点在BD⊥DA出现两次，所以要使用FOOT E B A E和FOOT D B A D
#     例子2：
#     输入题目：AB的中点是F，DE的中点是C，\\(BE \perp EA\\)，BD⊥DA，请证明：FC⊥DE.
#     输出：| 题目 | 几何关系 |
#     | :--- | :--- |
#     | AB的中点是F，DE的中点是C，BE⊥EA，BD⊥DA，请证明：FC⊥DE.  | HYPOTHESES: POINT A B；FOOT E B A E；FOOT D B A D；MIDPOINT F B A；MIDPOINT C D E, CONCLUSION= PERPENDICULAR F C D E |
#     注意：例子2中，题目中包含有LaTeX格式的语句\\(BE \perp EA\\)，请先将LaTeX语句转为普通格式BE⊥EA，再输入到表格中
#     下面我将给你一组只能在HYPOTHESES使用的构造语句，每个构造语句后面都有相应的几何关系
#     POINT A	构造自由点A
#     ON_LINE C A B	约束点C在直线AB上
#     ON_CIRCLE C A B	约束点C在圆AB上
#     ON_PLINE D C A B	约束点D在过C点平行于AB的直线上
#     ON_TLINE D C A B	约束点D在过C点垂直于AB的直线上
#     FOOT E B A E	直线BE⊥EA
#     ON_BLINE C A B	约束点C在AB的垂直平分线上
#     ON_ALINE D1 C1 A1 B1 A B C D	约束点D1是过C1点且和直线A1B1成角度α的直线上的一点，且α=∠[AB,CD]
#     ON_RCIRCLE D C A B	约束点D在以C为圆心，以AB为半径的圆上
#     MIDPOINT O A B	约束点O是线段AB的中点
#     LRATIO P A B n m	约束点P在直线AB上且AP/PB=n/m, n和m为整数
#     PRATIO P C A B n m	CP∥AB且CP/AB = n/m,P为约束点，n和m为整数
#     TRATIO P C A B n m	CP⊥AB且CP/AB = n/m,P为约束点， n和m为整数
#     CENTROID O A B C	约束点O是三角形ABC的重心
#     ORTHOCENTER O A B C	   约束点O是三角形ABC的垂心
#     CIRCUMCENTER O A B C	约束点O是三角形ABC的外心
#     INCENTER O A B C	约束点O是三角形ABC的内心
#     INTERSECTION_LP F A B C D E	   约束点F是直线AB和过C点平行于CD直线的交点
#     INTERSECTION_LT F A B C D E	   约束点F是直线AB和过C点垂直于CD直线的交点
#     INTERSECTION_LC E A B C D	约束点E是直线AB和圆CD的交点
#     INTERSECTION_CC E A B C D	约束点E是圆AB和圆CD的交点
#
#     R_TRIANGLE A B C	直线AB与AC交于约束点A，角CAB为直角的直角三角形
#     CIRCUMCENTER D A B C | A、B、C在以约束点D为圆心的圆上
#     CIRCLE A B | 以约束点A为圆心，B为圆上一点做一个圆
#     TRIANGLE A B C | A,B,C组成了一个三角形
#     R_TRIANGLE A B C | 直线AB与AC交于点约束点A，角CAB为直角的直角三角形
#     ISO_TRIANGLE C A B | CA=CB，且A，B，C不共线，A为约束点
#     FOOT E B A E | BE⊥EA，约束点E为垂足
#     EQ_TRIANGLE A B C | AB=BC=CA,∠ABC=∠CAB=∠BCA=60°,A,B,C不共线且是逆时钟排序的，C为约束点
#     TRAPEZOID A B C D | AB∥CD且AB和CD有同样的方向，这等价于AB和CD是平行的;
#     PARALLELOGRAM A B C D | AB∥CD，BC∥AD，A，B，C不共线，A、B、C为自由点，D为约束点
#     RECTANGLE A B C D | A，B，C，D是平行四边形且DA⊥BA，D为约束点
#     SQUARE A B C D | A，B，C，D是矩形并且AB= AD，C为约束点，D为约束点
#
#     下一条语句为复合构造语句
#     CIRCLE O1 D；ON_CIRCLE C O1 D；ON_CIRCLE B O1 D；ON_CIRCLE A O1 D | 圆内接四边形BCAD
#
#     下面我将给你一组待证结论CONCLUSION中使用的构造语句，请不要在HYPOTHESES中使用：
#     PERPENDICULAR D E B F | 求证DE⊥BF
#     RATIO A F C F 1 2 | 求证AF：FC=1：2
#     EQDISTANCE A B C D | AB与CD长度相等
#
#     注意事项：
#     1.构造语句的第一个字母都代表受到构造规则约束的点，无须加在POINT语句中。
#     2.构造语句后面的第一个字母也代表即将构造的点，其余字母都代表已经构造的点。
#     3.请不要对一个点进行两次约束。
#     4.请不要使用没有提到的构造语句。
#     5.不在构造语句的第一个字母的都是自由点，需要使用POINT语句构造
#
#     下面我将给出一组几何数学题，请你模仿上面给出的例子，使用表中提供的所有构造语句，注意事项，找出题目中包含的几何元素，如点、线段和多边形信息，并输出至表格中。
#     """
