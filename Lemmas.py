import Engine
import Informations
from fractions import Fraction
import math

# 定理公理的父类
class Lemma(object):
    # 要求给出定理名字、所需输入信息的个数
    def __init__(self):
        self.name = None
        self.inputNum = None

    @staticmethod
    def Infer():
        return None

    def print(self):
        print(self.name)


def PrintReasonlingTree(node, level=0):
    if node is not None:
        print("第", level, "层", "---|" * level, '(', node.source, ')', end="")
        node.printSelf_CN()
        for condition in node.conditions:
            PrintReasonlingTree(condition, level + 1)


# from collections import deque
#
#
# def PrintReasonlingTree(root):
#     if root is None:
#         return
#
#     # 第一步：使用 BFS 来确定所有节点的层级
#     queue = deque([(root, 0)])
#     nodes_by_level = {}  # 用于存储每个层级的节点列表
#
#     while queue:
#         node, level = queue.popleft()
#         if level not in nodes_by_level:
#             nodes_by_level[level] = []
#         nodes_by_level[level].append(node)
#
#         for condition in node.conditions:
#             queue.append((condition, level + 1))
#
#     # 第二步：从最深层级的叶子节点开始逆向打印
#     for level in sorted(nodes_by_level.keys(), reverse=True):
#         for node in nodes_by_level[level]:
#             print("第", level, "层", "---|" * level, '(', node.source, ')', end="")
#             node.printSelf_CN()

# # 是否存在复合角
# class LmdDoubleAngleEqual(Lemma):
#     def __init__(self):
#         self.name = "两个相邻角相加得到一个大角"
#         self.inputNum = 2
#
#     @staticmethod
#     def Infer(info1, info2):
#         if info1.p2 == info2.p2:
#             newInfo = None
#             if info1.p1 == info2.p1:
#                 newInfo = Informations.Angle(info1.p3, info1.p2, info2.p3)
#             elif info1.p1 == info2.p3:
#                 newInfo = Informations.Angle(info1.p3, info1.p2, info2.p1)
#             elif info1.p3 == info2.p1:
#                 newInfo = Informations.Angle(info1.p1, info1.p2, info2.p3)
#             elif info1.p3 == info2.p3:
#                 newInfo = Informations.Angle(info1.p1, info1.p2, info2.p1)
#             if newInfo is not None:
#                 # newInfo.source = "以上两个相邻角相加得到一个大角"
#                 # newInfo.conditions.append(info1)
#                 newInfo.conditions.append(["以上两个相邻角相加得到一个大角", info1, info2])
#             return newInfo


# 两个角相等的三角形推出第三个角也相等
class LmDoubleangle_ThirdAngle(Lemma):
    def __init__(self):
        self.name = "两个角相等的三角形，第三个角也相等"
        self.inputNum = 2

    @staticmethod
    def Infer(info1, info2):
        set1 = set()
        set1.add(info1.p1)
        set1.add(info1.p2)
        set1.add(info1.p3)
        # print("角1")
        # print(info1.p1)
        # print(info1.p2)
        # print(info1.p3)
        set2 = set()
        set2.add(info1.p4)
        set2.add(info1.p5)
        set2.add(info1.p6)
        # print("角2")
        # print(info1.p4)
        # print(info1.p5)
        # print(info1.p6)
        set3 = set()
        set3.add(info2.p1)
        set3.add(info2.p2)
        set3.add(info2.p3)
        # print("角3")
        # print(info2.p1)
        # print(info2.p2)
        # print(info2.p3)
        set4 = set()
        set4.add(info2.p4)
        set4.add(info2.p5)
        set4.add(info2.p6)
        # print("角4")
        # print(info2.p4)
        # print(info2.p5)
        # print(info2.p6)
        newInfo = None
        if set1 == set3 and set2 == set4 and info1.p2 != info2.p2 and info1.p5 != info2.p5:
            if info1.p1 != info2.p2 and info1.p4 != info2.p5:
                newInfo = Informations.EqualAngle(info1.p2, info1.p1, info2.p2, info1.p5, info1.p4, info2.p5)

            elif info1.p1 != info2.p2 and info1.p6 != info2.p5:
                newInfo = Informations.EqualAngle(info1.p2, info1.p1, info2.p2, info1.p5, info1.p6, info2.p5)

            elif info1.p3 != info2.p2 and info1.p4 != info2.p5:
                newInfo = Informations.EqualAngle(info1.p2, info1.p3, info2.p2, info1.p5, info1.p4, info2.p5)

            elif info1.p3 != info2.p2 and info1.p6 != info2.p5:
                newInfo = Informations.EqualAngle(info1.p2, info1.p3, info2.p2, info1.p5, info1.p6, info2.p5)

        elif set1 == set4 and set2 == set3 and info1.p2 != info2.p5 and info1.p5 != info2.p2:
            if info1.p1 != info2.p5 and info1.p4 != info2.p2:
                newInfo = Informations.EqualAngle(info1.p2, info1.p1, info2.p5, info1.p5, info1.p4, info2.p2)

            elif info1.p1 != info2.p5 and info1.p6 != info2.p2:
                newInfo = Informations.EqualAngle(info1.p2, info1.p1, info2.p5, info1.p5, info1.p6, info2.p2)

            elif info1.p3 != info2.p5 and info1.p4 != info2.p2:
                newInfo = Informations.EqualAngle(info1.p2, info1.p3, info2.p5, info1.p5, info1.p4, info2.p2)

            elif info1.p3 != info2.p5 and info1.p6 != info2.p2:
                newInfo = Informations.EqualAngle(info1.p2, info1.p3, info2.p5, info1.p5, info1.p6, info2.p2)

        if newInfo is not None:
            # newInfo.source = "两个角相等的三角形，第三个角也相等"
            # newInfo.conditions.append(info1)
            newInfo.conditions.append(["两个角相等的三角形，第三个角也相等", info1, info2])
            # newInfo.printSelf()
        return newInfo


# 全等三角形的证明（边角边）
class LmEqualTriangleLAL(Lemma):
    def __init__(self):
        self.name = "边角边得出一对全等三角形"
        self.inputNum = 3

    @staticmethod
    def Infer(info1, info2, info3):
        set_angle1 = set()
        set_angle2 = set()
        set_angle3 = set()
        set_angle4 = set()
        # 角1的第一条边
        set_angle1.update(info1.p1, info1.p2)
        # 角1的第二条边
        set_angle2.update(info1.p2, info1.p3)
        # 角2的第一条边
        set_angle3.update(info1.p4, info1.p5)
        # 角2的第二条边
        set_angle4.update(info1.p5, info1.p6)

        set_line1_1 = set()
        set_line1_2 = set()
        set_line2_1 = set()
        set_line2_2 = set()
        # 第一对边中的第一条边
        set_line1_1.update(info2.p1, info2.p2)
        # 第一对边中的第二条边
        set_line1_2.update(info2.p3, info2.p4)
        # 第二对边中的第一条边
        set_line2_1.update(info3.p1, info3.p2)
        # 第二对边中的第二条边
        set_line2_2.update(info3.p3, info3.p4)

        newInfo1 = newInfo2 = None
        flag1 = flag2 = False
        # set_angle1和set_angle3搭配
        if (
                set_angle1 == set_line1_1 and set_angle3 == set_line1_2) or set_angle1 == set_line1_2 and set_angle3 == set_line1_1:
            if set_angle2 == set_line2_1 and set_angle4 == set_line2_2 or (
                    set_angle2 == set_line2_2 and set_angle4 == set_line2_1):
                newInfo1 = Informations.EqualTriangle(info1.p1, info1.p2, info1.p3, info1.p4, info1.p5, info1.p6)
                newInfo2 = Informations.EqualTriangle(info1.p3, info1.p2, info1.p1, info1.p4, info1.p5, info1.p6)
        # set_angle1和set_angle3搭配
        elif (
                set_angle1 == set_line2_1 and set_angle3 == set_line2_2) or set_angle1 == set_line2_2 and set_angle3 == set_line2_1:
            if set_angle2 == set_line1_1 and set_angle4 == set_line1_2 or (
                    set_angle2 == set_line1_2 and set_angle4 == set_line1_1):
                newInfo1 = Informations.EqualTriangle(info1.p1, info1.p2, info1.p3, info1.p4, info1.p5, info1.p6)
                newInfo2 = Informations.EqualTriangle(info1.p3, info1.p2, info1.p1, info1.p4, info1.p5, info1.p6)
        # set_angle1和set_angle4搭配
        elif (
                set_angle1 == set_line2_1 and set_angle4 == set_line2_2) or set_angle1 == set_line2_2 and set_angle4 == set_line2_1:
            if set_angle2 == set_line1_1 and set_angle3 == set_line1_2 or (
                    set_angle2 == set_line1_2 and set_angle3 == set_line1_1):
                newInfo1 = Informations.EqualTriangle(info1.p1, info1.p2, info1.p3, info1.p4, info1.p5, info1.p6)
                newInfo2 = Informations.EqualTriangle(info1.p3, info1.p2, info1.p1, info1.p4, info1.p5, info1.p6)
        # set_angle1和set_angle4搭配
        elif (
                set_angle1 == set_line2_1 and set_angle4 == set_line2_2) or set_angle1 == set_line2_2 and set_angle4 == set_line2_1:
            if set_angle2 == set_line1_1 and set_angle3 == set_line1_2 or (
                    set_angle2 == set_line1_2 and set_angle3 == set_line1_1):
                newInfo1 = Informations.EqualTriangle(info1.p1, info1.p2, info1.p3, info1.p4, info1.p5, info1.p6)
                newInfo2 = Informations.EqualTriangle(info1.p3, info1.p2, info1.p1, info1.p4, info1.p5, info1.p6)

        # # 找bug用
        # if info2.p1 == "C" and info2.p2 == "E" and info3.p1 == "B" and info3.p2 == "C" and info3.p3 == "C" and info3.p4 == "D" and \
        #         info1.p1 == "B" and info1.p2 == "C" and info1.p3 == "E" and info1.p4 == "F" and info1.p5 == "C" and info1.p6 == "D":
        #     info1.printSelf()
        #     info2.printSelf()
        #     info3.printSelf()
        #     if newInfo1 is not None:
        #         newInfo1.printSelf()
        #     else:
        #         print("空")
        #     if newInfo2 is not None:
        #         newInfo2.printSelf()
        #     else:
        #         print("空")
        #     print("####")
        if newInfo1 is not None:
            flag1 = check_EQTiangle(newInfo1, info2, info3)
        if newInfo2 is not None:
            flag2 = check_EQTiangle(newInfo2, info2, info3)
        if flag1 == True and newInfo1 is not None:
            # newInfo1.source = "边角边得出一对全等三角形"
            # newInfo1.conditions.append(info2)
            # newInfo1.conditions.append(info1)
            newInfo1.conditions.append(["边角边得出一对全等三角形", info2, info1, info3])
            return newInfo1
        elif flag2 == True and newInfo2 is not None:
            # newInfo2.source = "边角边得出一对全等三角形"
            # newInfo2.conditions.append(info2)
            # newInfo2.conditions.append(info1)
            newInfo2.conditions.append(["边角边得出一对全等三角形", info2, info1, info3])
            return newInfo2
        else:
            return None


# 判断全等三角形的字母顺序是否符合题意
def check_EQTiangle(checkTriangle, checkLine, checkLine_2):
    set1_1 = set()
    set1_2 = set()
    set2_1 = set()
    set2_2 = set()
    set3_1 = set()
    set3_2 = set()
    set_line_1 = set()
    set_line_2 = set()
    set_line_3 = set()
    set_line_4 = set()
    flag1 = flag2 = False
    set1_1.update(checkTriangle.p1, checkTriangle.p2)
    set1_2.update(checkTriangle.p4, checkTriangle.p5)

    set2_1.update(checkTriangle.p2, checkTriangle.p3)
    set2_2.update(checkTriangle.p5, checkTriangle.p6)

    set3_1.update(checkTriangle.p1, checkTriangle.p3)
    set3_2.update(checkTriangle.p4, checkTriangle.p6)

    set_line_1.update(checkLine.p1, checkLine.p2)
    set_line_2.update(checkLine.p3, checkLine.p4)
    set_line_3.update(checkLine_2.p1, checkLine_2.p2)
    set_line_4.update(checkLine_2.p3, checkLine_2.p4)
    if (set1_1 == set_line_1 and set1_2 == set_line_2) or (set1_1 == set_line_2 and set1_2 == set_line_1):
        flag1 = True
    elif (set2_1 == set_line_1 and set2_2 == set_line_2) or (set2_1 == set_line_2 and set2_2 == set_line_1):
        flag1 = True
    elif (set3_1 == set_line_1 and set3_2 == set_line_2) or (set3_1 == set_line_2 and set3_2 == set_line_1):
        flag1 = True
    else:
        flag1 = False
    if (set1_1 == set_line_3 and set1_2 == set_line_4) or (set1_1 == set_line_4 and set1_2 == set_line_3):
        flag2 = True
    elif (set2_1 == set_line_3 and set2_2 == set_line_4) or (set2_1 == set_line_4 and set2_2 == set_line_3):
        flag2 = True
    elif (set3_1 == set_line_3 and set3_2 == set_line_4) or (set3_1 == set_line_4 and set3_2 == set_line_3):
        flag2 = True
    else:
        flag2 = False
    flag = flag1 and flag2
    return flag


# 判断全等三角形的字母顺序是否符合题意
def check_EQTiangle_withoneline(checkTriangle, checkLine):
    set1_1 = set()
    set1_2 = set()
    set2_1 = set()
    set2_2 = set()
    set3_1 = set()
    set3_2 = set()
    set_line_1 = set()
    set_line_2 = set()
    flag1 = False
    set1_1.update(checkTriangle.p1, checkTriangle.p2)
    set1_2.update(checkTriangle.p4, checkTriangle.p5)

    set2_1.update(checkTriangle.p2, checkTriangle.p3)
    set2_2.update(checkTriangle.p5, checkTriangle.p6)

    set3_1.update(checkTriangle.p1, checkTriangle.p3)
    set3_2.update(checkTriangle.p4, checkTriangle.p6)

    set_line_1.update(checkLine.p1, checkLine.p2)
    set_line_2.update(checkLine.p3, checkLine.p4)
    if (set1_1 == set_line_1 and set1_2 == set_line_2) or (set1_1 == set_line_2 and set1_2 == set_line_1):
        flag1 = True
    elif (set2_1 == set_line_1 and set2_2 == set_line_2) or (set2_1 == set_line_2 and set2_2 == set_line_1):
        flag1 = True
    elif (set3_1 == set_line_1 and set3_2 == set_line_2) or (set3_1 == set_line_2 and set3_2 == set_line_1):
        flag1 = True
    else:
        flag1 = False
    return flag1


# 主要分为三种情况
# 1.一对有邻边的全等三角形              len(set_test) == 4
# 2.一对有共同点的全等三角形            len(set_test) == 5
# 3.一对即无邻边也无共同点的全等三角形    len(set_test) == 6
# 全等三角形的证明（有邻边）（边边边） 本函数处理上述第一种情况
class LmEqualTriangleLLL_1(Lemma):
    def __init__(self):
        self.name = "边边边得出一对全等三角形"
        self.inputNum = 3

    @staticmethod
    def Infer(info1, info2, equalTriangleList, coLineList):
        set_test = set()
        set_test.update(info1.p1, info1.p2, info1.p3, info1.p4, info2.p1, info2.p2, info2.p3, info2.p4)
        list_test = [info1.p1, info1.p2, info1.p3, info1.p4, info2.p1, info2.p2, info2.p3, info2.p4]
        set_info1 = set()
        set_info1.update(info1.p1, info1.p2, info1.p3, info1.p4)
        set_info2 = set()
        set_info2.update(info2.p1, info2.p2, info2.p3, info2.p4)
        if len(set_test) != 4:
            return False
        if not all(list_test.count(value) == 2 for value in set_test):  # 判断每个点是否都出现了两次
            return False
        temp = list(set_test)
        a1 = temp[0]
        a2 = temp[1]
        a3 = temp[2]
        a4 = temp[3]  # 提取不同的字母
        # 已知的四种两两组合
        known_combinations = [info1.p1 + info1.p2, info1.p3 + info1.p4, info2.p1 + info2.p2, info2.p3 + info2.p4,
                              info1.p2 + info1.p1, info1.p4 + info1.p3, info2.p2 + info2.p1, info2.p4 + info2.p3]
        # 生成所有可能的六种两两组合
        all_combinations = [a1 + a2, a1 + a3, a1 + a4, a2 + a3, a2 + a4, a3 + a4]
        # 寻找剩余的两种两两组合
        remaining_combinations = [comb for comb in all_combinations if comb not in known_combinations]
        result = [char for word in remaining_combinations for char in word]
        a1 = result[0]
        a2 = result[1]
        a3 = result[2]
        a4 = result[3]
        set1 = set()
        set2 = set()
        set3 = set()
        set4 = set()
        set1.update(a1, a3)
        set2.update(a2, a3)
        set3.update(a1, a4)
        set4.update(a2, a4)
        setinfo1 = set()
        setinfo2 = set()
        setinfo3 = set()
        setinfo4 = set()
        setinfo1.update(info1.p1, info1.p2)
        setinfo2.update(info1.p3, info1.p4)
        setinfo3.update(info2.p1, info2.p2)
        setinfo4.update(info2.p3, info2.p4)
        newInfo1 = newInfo2 = None
        flag1 = flag2 = flag = False
        # 当a1a2是共同边时
        if not (((set1 == setinfo1 and set2 == setinfo2) or (set1 == setinfo2 and set2 == setinfo1)) and (
                (set3 == setinfo3 and set4 == setinfo4) or (set3 == setinfo4 and set4 == setinfo3))):
            if not (((set1 == setinfo3 and set2 == setinfo4) or (set1 == setinfo4 and set2 == setinfo3)) and (
                    (set3 == setinfo1 and set4 == setinfo2) or (set3 == setinfo2 and set4 == setinfo1))):
                if len(set_info1) == len(set_info2) == 4:
                    newInfo1 = Informations.EqualTriangle(a1, a2, a3, a2, a1, a4)
                elif len(set_info1) == len(set_info2) == 3:
                    newInfo1 = Informations.EqualTriangle(a1, a2, a3, a1, a2, a4)
                else:
                    print("逻辑出错1")
        # 当a3a4是共同边时
        if not (((set1 == setinfo1 and set3 == setinfo2) or (set1 == setinfo2 and set3 == setinfo1)) and (
                (set2 == setinfo3 and set4 == setinfo4) or (set2 == setinfo4 and set4 == setinfo3))):
            if not (((set1 == setinfo3 and set3 == setinfo4) or (set1 == setinfo4 and set3 == setinfo3)) and (
                    (set2 == setinfo1 and set4 == setinfo2) or (set2 == setinfo2 and set4 == setinfo1))):
                if len(set_info1) == len(set_info2) == 4:
                    newInfo2 = Informations.EqualTriangle(a3, a4, a1, a4, a3, a2)
                elif len(set_info1) == len(set_info2) == 3:
                    newInfo2 = Informations.EqualTriangle(a3, a4, a1, a3, a4, a2)
                else:
                    print("逻辑出错2")
        if newInfo1 is not None:
            # 用一个res来存IsInList返回的值
            newInfo1.conditions.append(["三边相等推出全等三角形（包括一对邻边）", info1, info2])
            res = newInfo1.IsInList(equalTriangleList, coLineList)
            newInfo1.weight = max(info1.weight, info2.weight) + 1
            if check_EQTiangle(newInfo1, info1, info2) and res is False:
                equalTriangleList.append(newInfo1)
                flag1 = True
            elif res is True:
                pass
            else:
                nums = len(equalTriangleList[res].conditions)
                for item in equalTriangleList[res].conditions:
                    if len(item) != len(newInfo1.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo1.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalTriangleList[res].conditions.append(newInfo1.conditions[-1])
                equalTriangleList[res].weight = min(newInfo1.weight, equalTriangleList[res].weight)
        if newInfo2 is not None:
            # 用一个res来存IsInList返回的值
            newInfo2.conditions.append(["三边相等推出全等三角形（包括一对邻边）", info1, info2])
            res = newInfo2.IsInList(equalTriangleList, coLineList)
            newInfo2.weight = max(info1.weight, info2.weight) + 1
            if check_EQTiangle(newInfo2, info1, info2) and res is False:
                equalTriangleList.append(newInfo2)
                flag2 = True
            elif res is True:
                pass
            else:
                nums = len(equalTriangleList[res].conditions)
                for item in equalTriangleList[res].conditions:
                    if len(item) != len(newInfo2.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo2.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalTriangleList[res].conditions.append(newInfo2.conditions[-1])
                equalTriangleList[res].weight = min(newInfo2.weight, equalTriangleList[res].weight)
        flag = flag1 or flag2
        return flag


# 主要分为三种情况
# 1.一对有邻边的全等三角形              len(set_test) == 4
# 2.一对有共同点的全等三角形            len(set_test) == 5
# 3.一对即无邻边也无共同点的全等三角形    len(set_test) == 6
# 全等三角形的证明（无邻边）（边边边） 本函数处理上述第二、三种情况
class LmEqualTriangleLLL_2(Lemma):
    def __init__(self):
        self.name = "边边边得出一对全等三角形"
        self.inputNum = 3

    @staticmethod
    def Infer(info1, info2, info3, equalTriangleList, coLineList):

        flag = False
        newInfo = None
        set1_1 = set()  # 第一对 边 1_1
        set1_1.add(info1.p1)
        set1_1.add(info1.p2)

        set1_2 = set()  # 第一对 边 1_2
        set1_2.add(info1.p3)
        set1_2.add(info1.p4)

        set2_1 = set()  # 第一对 边 2_1
        set2_1.add(info2.p1)
        set2_1.add(info2.p2)

        set2_2 = set()  # 第一对 边 2_2
        set2_2.add(info2.p3)
        set2_2.add(info2.p4)

        set3_1 = set()  # 第一对 边 3_1
        set3_1.add(info3.p1)
        set3_1.add(info3.p2)

        set3_2 = set()  # 第一对 边 3_2
        set3_2.add(info3.p3)
        set3_2.add(info3.p4)
        set_test = set()
        set_temp = set()
        set_temp2 = set()
        set_test.update(info1.p1, info1.p2, info1.p3, info1.p4, info2.p1, info2.p2, info2.p3, info2.p4, info3.p1,
                        info3.p2, info3.p3, info3.p4)
        list_test = [info1.p1, info1.p2, info1.p3, info1.p4, info2.p1, info2.p2, info2.p3, info2.p4, info3.p1,
                     info3.p2, info3.p3, info3.p4]
        if len(set_test) > 6 or len(set_test) < 5:
            return False
        newInfo1 = newInfo2 = newInfo3 = newInfo4 = newInfo5 = newInfo6 = None
        if len(set_test) == 6:

            if not all(list_test.count(value) == 2 for value in set_test):  # 判断每个点是否都出现了两次
                return False
            if len(set_temp.union(set1_1, set2_1, set3_1)) == 3:
                set_temp = set_temp.union(set1_1, set2_2, set3_1)

                list_temp = list(set_temp)
                list_temp2 = list(set_temp2.union(set1_2, set2_2, set3_2))

                newInfo1 = Informations.EqualTriangle(list_temp[0], list_temp[1], list_temp[2], list_temp2[0],
                                                      list_temp2[1], list_temp2[2])
                newInfo2 = Informations.EqualTriangle(list_temp[0], list_temp[1], list_temp[2], list_temp2[0],
                                                      list_temp2[2], list_temp2[1])
                newInfo3 = Informations.EqualTriangle(list_temp[0], list_temp[1], list_temp[2], list_temp2[1],
                                                      list_temp2[0], list_temp2[2])
                newInfo4 = Informations.EqualTriangle(list_temp[0], list_temp[1], list_temp[2], list_temp2[1],
                                                      list_temp2[2], list_temp2[0])
                newInfo5 = Informations.EqualTriangle(list_temp[0], list_temp[1], list_temp[2], list_temp2[2],
                                                      list_temp2[0], list_temp2[1])
                newInfo6 = Informations.EqualTriangle(list_temp[0], list_temp[1], list_temp[2], list_temp2[2],
                                                      list_temp2[1], list_temp2[0])
            elif len(set_temp.union(set1_1, set2_1, set3_2)) == 3:
                set_temp = set_temp.union(set1_1, set2_2, set3_1)
                list_temp = list(set_temp)
                list_temp2 = list(set_temp2.union(set1_2, set2_2, set3_1))
                newInfo1 = Informations.EqualTriangle(list_temp[0], list_temp[1], list_temp[2], list_temp2[0],
                                                      list_temp2[1], list_temp2[2])
                newInfo2 = Informations.EqualTriangle(list_temp[0], list_temp[1], list_temp[2], list_temp2[0],
                                                      list_temp2[2], list_temp2[1])
                newInfo3 = Informations.EqualTriangle(list_temp[0], list_temp[1], list_temp[2], list_temp2[1],
                                                      list_temp2[0], list_temp2[2])
                newInfo4 = Informations.EqualTriangle(list_temp[0], list_temp[1], list_temp[2], list_temp2[1],
                                                      list_temp2[2], list_temp2[0])
                newInfo5 = Informations.EqualTriangle(list_temp[0], list_temp[1], list_temp[2], list_temp2[2],
                                                      list_temp2[0], list_temp2[1])
                newInfo6 = Informations.EqualTriangle(list_temp[0], list_temp[1], list_temp[2], list_temp2[2],
                                                      list_temp2[1], list_temp2[0])
            elif len(set_temp.union(set1_1, set2_2, set3_1)) == 3:
                set_temp = set_temp.union(set1_1, set2_2, set3_1)
                list_temp = list(set_temp)
                list_temp2 = list(set_temp2.union(set1_2, set2_1, set3_2))
                newInfo1 = Informations.EqualTriangle(list_temp[0], list_temp[1], list_temp[2], list_temp2[0],
                                                      list_temp2[1], list_temp2[2])
                newInfo2 = Informations.EqualTriangle(list_temp[0], list_temp[1], list_temp[2], list_temp2[0],
                                                      list_temp2[2], list_temp2[1])
                newInfo3 = Informations.EqualTriangle(list_temp[0], list_temp[1], list_temp[2], list_temp2[1],
                                                      list_temp2[0], list_temp2[2])
                newInfo4 = Informations.EqualTriangle(list_temp[0], list_temp[1], list_temp[2], list_temp2[1],
                                                      list_temp2[2], list_temp2[0])
                newInfo5 = Informations.EqualTriangle(list_temp[0], list_temp[1], list_temp[2], list_temp2[2],
                                                      list_temp2[0], list_temp2[1])
                newInfo6 = Informations.EqualTriangle(list_temp[0], list_temp[1], list_temp[2], list_temp2[2],
                                                      list_temp2[1], list_temp2[0])
            elif len(set_temp.union(set1_1, set2_2, set3_2)) == 3:
                set_temp = set_temp.union(set1_1, set2_2, set3_1)
                list_temp = list(set_temp)
                list_temp2 = list(set_temp2.union(set1_2, set2_1, set3_1))
                newInfo1 = Informations.EqualTriangle(list_temp[0], list_temp[1], list_temp[2], list_temp2[0],
                                                      list_temp2[1], list_temp2[2])
                newInfo2 = Informations.EqualTriangle(list_temp[0], list_temp[1], list_temp[2], list_temp2[0],
                                                      list_temp2[2], list_temp2[1])
                newInfo3 = Informations.EqualTriangle(list_temp[0], list_temp[1], list_temp[2], list_temp2[1],
                                                      list_temp2[0], list_temp2[2])
                newInfo4 = Informations.EqualTriangle(list_temp[0], list_temp[1], list_temp[2], list_temp2[1],
                                                      list_temp2[2], list_temp2[0])
                newInfo5 = Informations.EqualTriangle(list_temp[0], list_temp[1], list_temp[2], list_temp2[2],
                                                      list_temp2[0], list_temp2[1])
                newInfo6 = Informations.EqualTriangle(list_temp[0], list_temp[1], list_temp[2], list_temp2[2],
                                                      list_temp2[1], list_temp2[0])

            else:
                return False
            if newInfo1 is not None and check_EQTiangle(newInfo1, info1, info2):
                newInfo = newInfo1
            if newInfo2 is not None and check_EQTiangle(newInfo2, info1, info2):
                newInfo = newInfo2
            if newInfo3 is not None and check_EQTiangle(newInfo3, info1, info2):
                newInfo = newInfo3
            if newInfo4 is not None and check_EQTiangle(newInfo4, info1, info2):
                newInfo = newInfo4
            if newInfo5 is not None and check_EQTiangle(newInfo5, info1, info2):
                newInfo = newInfo5
            if newInfo6 is not None and check_EQTiangle(newInfo6, info1, info2):
                newInfo = newInfo6
            # if len(set_temp.union(set1_1, set2_1, set3_1)) == 3 or len(set_temp.union(set1_1, set2_1, set3_2)) == 3:
            #     set_top_point_first = set1_1 & set2_1  # 第一个三角形的顶点
            #     set_top_point_last = set1_2 & set2_2  # 第二个三角形的顶点
            #     set_left_point_first = set1_1.difference(set_top_point_first)  # 第一个三角形的左点
            #     set_right_point_first = set2_1.difference(set_top_point_first)  # 第一个三角形的右点
            #     set_left_point_second = set1_2.difference(set_top_point_last)  # 第二个三角形的左点
            #     set_right_point_second = set2_2.difference(set_top_point_last)  # 第二个三角形的右点
            #     tri_1_left = set_left_point_first.pop()
            #     tri_1_top = set_top_point_first.pop()
            #     tri_1_right = set_right_point_first.pop()
            #     tri_2_left = set_left_point_second.pop()
            #     tri_2_top = set_top_point_last.pop()
            #     tri_2_right = set_right_point_second.pop()
            #     newInfo = Informations.EqualTriangle(tri_1_left, tri_1_top, tri_1_right, tri_2_left, tri_2_top,
            #                                          tri_2_right)
            # elif len(set_temp.union(set1_1, set2_2, set3_1)) == 3 or len(set_temp.union(set1_1, set2_2, set3_2)) == 3:
            #     set_top_point_first = set1_1 & set2_2  # 第一个三角形的顶点
            #     set_top_point_last = set1_2 & set2_1  # 第二个三角形的顶点
            #     set_left_point_first = set1_1.difference(set_top_point_first)  # 第一个三角形的左点
            #     set_right_point_first = set2_2.difference(set_top_point_first)  # 第一个三角形的右点
            #     set_left_point_second = set1_2.difference(set_top_point_last)  # 第二个三角形的左点
            #     set_right_point_second = set2_1.difference(set_top_point_last)  # 第二个三角形的右点
            #     tri_1_left = set_left_point_first.pop()
            #     tri_1_top = set_top_point_first.pop()
            #     tri_1_right = set_right_point_first.pop()
            #     tri_2_left = set_left_point_second.pop()
            #     tri_2_top = set_top_point_last.pop()
            #     tri_2_right = set_right_point_second.pop()
            #     newInfo = Informations.EqualTriangle(tri_1_left, tri_1_top, tri_1_right, tri_2_left, tri_2_top,
            #                                          tri_2_right)
            # else:
            #     newInfo = None

        if len(set_test) == 5:

            num_2 = 0
            num_4 = 0
            co_point = ''  # 找到共同顶点
            for value in set_test:
                if list_test.count(value) == 2:
                    num_2 += 1
                elif list_test.count(value) == 4:
                    num_4 += 1
                    co_point = value
                else:
                    return False
            if num_4 != 1 and num_2 != 4:
                return False
            set_co_point = set()
            set_co_point.add(co_point)  # 把共同顶点放到set（）中，方便后续计算
            a1 = len(set1_1 & set_co_point)
            a2 = len(set1_2 & set_co_point)
            a3 = len(set2_1 & set_co_point)
            a4 = len(set2_2 & set_co_point)
            a5 = len(set3_1 & set_co_point)
            a6 = len(set3_2 & set_co_point)
            a = a1 + a2 + a3 + a4 + a5 + a6
            # 找出a1-a6中谁的值为0，对应的边就是对边，再结合草稿纸上的规则书写1到6种情况。
            if a != 4:
                return False
            opposide_point1 = opposide_point2 = opposide_point3 = opposide_point4 = None
            if a1 == 0:
                opposide_point1 = info1.p1
                opposide_point2 = info1.p2
            if a2 == 0:
                if opposide_point1 == None:
                    opposide_point1 = info1.p3
                    opposide_point2 = info1.p4
                opposide_point3 = info1.p3
                opposide_point4 = info1.p4
            if a3 == 0:
                if opposide_point1 == None:
                    opposide_point1 = info2.p1
                    opposide_point2 = info2.p2
                opposide_point3 = info2.p1
                opposide_point4 = info2.p2
            if a4 == 0:
                if opposide_point1 == None:
                    opposide_point1 = info2.p3
                    opposide_point2 = info2.p4
                opposide_point3 = info2.p3
                opposide_point4 = info2.p4
            if a5 == 0:
                if opposide_point1 == None:
                    opposide_point1 = info3.p1
                    opposide_point2 = info3.p2
                opposide_point3 = info3.p1
                opposide_point4 = info3.p2
            if a6 == 0:
                if opposide_point1 == None:
                    opposide_point1 = info3.p3
                    opposide_point2 = info3.p4
                opposide_point3 = info3.p3
                opposide_point4 = info3.p4
            newInfo1 = Informations.EqualTriangle(opposide_point1, co_point, opposide_point2, opposide_point3, co_point,
                                                  opposide_point4)
            newInfo2 = Informations.EqualTriangle(opposide_point1, co_point, opposide_point2, opposide_point4, co_point,
                                                  opposide_point3)
            newInfo3 = Informations.EqualTriangle(co_point, opposide_point1, opposide_point2, opposide_point3, co_point,
                                                  opposide_point4)
            newInfo4 = Informations.EqualTriangle(co_point, opposide_point1, opposide_point2, opposide_point4, co_point,
                                                  opposide_point3)
            newInfo5 = Informations.EqualTriangle(co_point, opposide_point1, opposide_point2, opposide_point3,
                                                  opposide_point4, co_point)
            newInfo6 = Informations.EqualTriangle(co_point, opposide_point1, opposide_point2, opposide_point4,
                                                  opposide_point3, co_point)
            if newInfo1 is not None and check_EQTiangle(newInfo1, info1, info2):
                newInfo = newInfo1
            if newInfo2 is not None and check_EQTiangle(newInfo2, info1, info2):
                newInfo = newInfo2
            if newInfo3 is not None and check_EQTiangle(newInfo3, info1, info2):
                newInfo = newInfo3
            if newInfo4 is not None and check_EQTiangle(newInfo4, info1, info2):
                newInfo = newInfo4
            if newInfo5 is not None and check_EQTiangle(newInfo5, info1, info2):
                newInfo = newInfo5
            if newInfo6 is not None and check_EQTiangle(newInfo6, info1, info2):
                newInfo = newInfo6
            # 在加入链表之前，要判断链表中是否已有相同信息；若相同则不添加
        if newInfo is not None:
            # 用一个res来存IsInList返回的值
            newInfo.conditions.append(["三边相等推出全等三角形", info1, info2, info3])
            res = newInfo.IsInList(equalTriangleList, coLineList)
            newInfo.weight = max(info1.weight, info2.weight, info3.weight) + 1
            if res is False:
                equalTriangleList.append(newInfo)
                flag = True
            elif res is True:
                pass
            else:
                nums = len(equalTriangleList[res].conditions)
                for item in equalTriangleList[res].conditions:
                    if len(item) != len(newInfo.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalTriangleList[res].conditions.append(newInfo.conditions[-1])
                equalTriangleList[res].weight = min(newInfo.weight, equalTriangleList[res].weight)
        return flag
        # num_2 = 0
        # num_4 = 0
        # co_point = 'X'  # 找到共同顶点
        # if len(set_test & set(co_point)) == 1:
        #     return None
        # for value in set_test:
        #     if list_test.count(value) == 2:
        #         num_2 += 1
        #     elif list_test.count(value) == 4:
        #         num_4 += 1
        #         co_point = value
        #     else:
        #         return None
        # if num_4 != 1 and num_2 != 4:
        #     return None
        #     set_co_point = set()
        #     set_co_point.add(co_point)  # 把共同顶点放到set（）中，方便后续计算
        #     for i in range(len(list_test)):
        #         print(list_test[i])
        #     # 将共同点分开，把某个三角形的共同点替换成X
        #     if len((set1_1 & set_co_point)) == 0:  # set1_1是对边的情况
        #         if info2.p1 == info1.p1 or info2.p1 == info1.p2:  # 替换共同点为X
        #             info2.p2 = 'X'
        #         if info2.p2 == info1.p1 or info2.p2 == info1.p2:
        #             info2.p1 = 'X'
        #         if info2.p3 == info1.p1 or info2.p3 == info1.p2:
        #             info2.p4 = 'X'
        #         if info2.p4 == info1.p1 or info2.p4 == info1.p2:
        #             info2.p3 = 'X'
        #         if info3.p1 == info1.p1 or info3.p1 == info1.p2:
        #             info3.p2 = 'X'
        #         if info3.p2 == info1.p1 or info3.p2 == info1.p2:
        #             info3.p1 = 'X'
        #         if info3.p3 == info1.p1 or info3.p3 == info1.p2:
        #             info3.p4 = 'X'
        #         if info3.p4 == info1.p1 or info3.p4 == info1.p2:
        #             info3.p3 = 'X'
        #     elif len((set1_2 & set_co_point)) == 0:  # set1_2是对边的情况 ，以下依次类推
        #         if info2.p1 == info1.p3 or info2.p1 == info1.p4:
        #             info2.p2 = 'X'
        #         if info2.p2 == info1.p3 or info2.p2 == info1.p4:
        #             info2.p1 = 'X'
        #         if info2.p3 == info1.p3 or info2.p3 == info1.p4:
        #             info2.p4 = 'X'
        #         if info2.p4 == info1.p3 or info2.p4 == info1.p4:
        #             info2.p3 = 'X'
        #         if info3.p1 == info1.p3 or info3.p1 == info1.p4:
        #             info3.p2 = 'X'
        #         if info3.p2 == info1.p3 or info3.p2 == info1.p4:
        #             info3.p1 = 'X'
        #         if info3.p3 == info1.p3 or info3.p3 == info1.p4:
        #             info3.p4 = 'X'
        #         if info3.p4 == info1.p3 or info3.p4 == info1.p4:
        #             info3.p3 = 'X'
        #     elif len((set2_1 & set_co_point)) == 0:
        #         if info1.p1 == info2.p1 or info1.p1 == info2.p2:
        #             info1.p2 = 'X'
        #         if info1.p2 == info2.p1 or info1.p2 == info2.p2:
        #             info1.p1 = 'X'
        #         if info1.p3 == info2.p1 or info1.p3 == info2.p2:
        #             info1.p4 = 'X'
        #         if info1.p4 == info2.p1 or info1.p4 == info2.p2:
        #             info1.p3 = 'X'
        #         if info3.p1 == info2.p1 or info3.p1 == info2.p2:
        #             info3.p2 = 'X'
        #         if info3.p2 == info2.p1 or info3.p2 == info2.p2:
        #             info3.p1 = 'X'
        #         if info3.p3 == info2.p1 or info3.p3 == info2.p2:
        #             info3.p4 = 'X'
        #         if info3.p4 == info2.p1 or info3.p4 == info2.p2:
        #             info3.p3 = 'X'
        #     elif len((set2_2 & set_co_point)) == 0:
        #         if info1.p1 == info2.p3 or info1.p1 == info2.p4:
        #             info1.p2 = 'X'
        #         if info1.p2 == info2.p3 or info1.p2 == info2.p4:
        #             info1.p1 = 'X'
        #         if info1.p3 == info2.p3 or info1.p3 == info2.p4:
        #             info1.p4 = 'X'
        #         if info1.p4 == info2.p3 or info1.p4 == info2.p4:
        #             info1.p3 = 'X'
        #         if info3.p1 == info2.p3 or info3.p1 == info2.p4:
        #             info3.p2 = 'X'
        #         if info3.p2 == info2.p3 or info3.p2 == info2.p4:
        #             info3.p1 = 'X'
        #         if info3.p3 == info2.p3 or info3.p3 == info2.p4:
        #             info3.p4 = 'X'
        #         if info3.p4 == info2.p3 or info3.p4 == info2.p4:
        #             info3.p3 = 'X'
        #     elif len((set3_1 & set_co_point)) == 0:
        #         if info1.p1 == info3.p1 or info1.p1 == info3.p2:
        #             info1.p2 = 'X'
        #         if info1.p2 == info3.p1 or info1.p2 == info3.p2:
        #             info1.p1 = 'X'
        #         if info1.p3 == info3.p1 or info1.p3 == info3.p2:
        #             info1.p4 = 'X'
        #         if info1.p4 == info3.p1 or info1.p4 == info3.p2:
        #             info1.p3 = 'X'
        #         if info2.p1 == info3.p1 or info2.p1 == info3.p2:
        #             info2.p2 = 'X'
        #         if info2.p2 == info3.p1 or info2.p2 == info3.p2:
        #             info2.p1 = 'X'
        #         if info2.p3 == info3.p1 or info2.p3 == info3.p2:
        #             info2.p4 = 'X'
        #         if info2.p4 == info3.p1 or info2.p4 == info3.p2:
        #             info2.p3 = 'X'
        #     elif len((set3_2 & set_co_point)) == 0:
        #         if info1.p1 == info3.p3 or info1.p1 == info3.p4:
        #             info1.p2 = 'X'
        #         if info1.p2 == info3.p3 or info1.p2 == info3.p4:
        #             info1.p1 = 'X'
        #         if info1.p3 == info3.p3 or info1.p3 == info3.p4:
        #             info1.p4 = 'X'
        #         if info1.p4 == info3.p3 or info1.p4 == info3.p4:
        #             info1.p3 = 'X'
        #         if info2.p1 == info3.p3 or info2.p1 == info3.p4:
        #             info2.p2 = 'X'
        #         if info2.p2 == info3.p3 or info2.p2 == info3.p4:
        #             info2.p1 = 'X'
        #         if info2.p3 == info3.p3 or info2.p3 == info3.p4:
        #             info2.p4 = 'X'
        #         if info2.p4 == info3.p3 or info2.p4 == info3.p4:
        #             info2.p3 = 'X'
        #     # 递归调用本函数，处理X替换过后的数据
        #     newInfo = LmEqualTriangleLLL_2.Infer(info1, info2, info3)
        #     if newInfo is not None:
        #         # newInfo.printSelf()
        #         # 恢复原状，把X换回原始共同点
        #         if newInfo.p1 == 'X': newInfo.p1 = co_point
        #         if newInfo.p2 == 'X': newInfo.p2 = co_point
        #         if newInfo.p3 == 'X': newInfo.p3 = co_point
        #         if newInfo.p4 == 'X': newInfo.p4 = co_point
        #         if newInfo.p5 == 'X': newInfo.p5 = co_point
        #         if newInfo.p6 == 'X': newInfo.p6 = co_point
        #     else:
        #         print("None")
        #     if info1.p1 == 'X': info1.p1 = co_point
        #     if info1.p2 == 'X': info1.p2 = co_point
        #     if info1.p3 == 'X': info1.p3 = co_point
        #     if info1.p4 == 'X': info1.p4 = co_point
        #     if info2.p1 == 'X': info2.p1 = co_point
        #     if info2.p2 == 'X': info2.p2 = co_point
        #     if info2.p3 == 'X': info2.p3 = co_point
        #     if info2.p4 == 'X': info2.p4 = co_point
        #     if info3.p1 == 'X': info3.p1 = co_point
        #     if info3.p2 == 'X': info3.p2 = co_point
        #     if info3.p3 == 'X': info3.p3 = co_point
        #     if info3.p4 == 'X': info3.p4 = co_point

        # return newInfo


# 全等三角形的证明（角边角）
class LmEqualTriangleALA(Lemma):
    def __init__(self):
        self.name = "角边角得出一对全等三角形"
        self.inputNum = 3

    @staticmethod
    def Infer(info1, info2, info3):
        set1 = set()  # 第一对 角1 a
        set1.add(info1.p1)
        set1.add(info1.p2)
        set1.add(info1.p3)

        set2 = set()  # 第一对 角2 b
        set2.add(info1.p4)
        set2.add(info1.p5)
        set2.add(info1.p6)

        set3 = set()  # 第二对 角1 c
        set3.add(info2.p1)
        set3.add(info2.p2)
        set3.add(info2.p3)

        set4 = set()  # 第二对 角2 d
        set4.add(info2.p4)
        set4.add(info2.p5)
        set4.add(info2.p6)
        if set1 == set2 or set3 == set4:
            return None

        set5 = set()  # a与c的夹边
        set5.add(info1.p2)
        set5.add(info2.p2)

        set6 = set()  # b与d的夹边
        set6.add(info1.p5)
        set6.add(info2.p5)

        set7 = set()  # a与d的夹边
        set7.add(info1.p2)
        set7.add(info2.p5)

        set8 = set()  # b与c的夹边
        set8.add(info1.p5)
        set8.add(info2.p2)

        set9 = set()  # 边1
        set9.add(info3.p1)
        set9.add(info3.p2)

        set10 = set()  # 边2
        set10.add(info3.p3)
        set10.add(info3.p4)

        newInfo = newInfo1 = newInfo2 = None
        if set1 == set3 and set2 == set4:
            if set5 == set9 and set6 == set10:
                newInfo1 = Informations.EqualTriangle(info1.p1, info1.p2, info1.p3, info1.p4, info1.p5, info1.p6)
                newInfo2 = Informations.EqualTriangle(info1.p1, info1.p2, info1.p3, info1.p6, info1.p5, info1.p4)
            elif set5 == set10 and set6 == set9:
                newInfo1 = Informations.EqualTriangle(info1.p1, info1.p2, info1.p3, info1.p4, info1.p5, info1.p6)
                newInfo2 = Informations.EqualTriangle(info1.p1, info1.p2, info1.p3, info1.p6, info1.p5, info1.p4)
        elif set1 == set4 and set2 == set3:
            if set7 == set9 and set8 == set10:
                newInfo1 = Informations.EqualTriangle(info1.p1, info1.p2, info1.p3, info1.p4, info1.p5, info1.p6)
                newInfo2 = Informations.EqualTriangle(info1.p1, info1.p2, info1.p3, info1.p6, info1.p5, info1.p4)
            elif set7 == set10 and set8 == set9:
                newInfo1 = Informations.EqualTriangle(info1.p1, info1.p2, info1.p3, info1.p4, info1.p5, info1.p6)
                newInfo2 = Informations.EqualTriangle(info1.p1, info1.p2, info1.p3, info1.p6, info1.p5, info1.p4)
        if newInfo1 is not None and check_EQTiangle_withoneline(newInfo1, info3):
            newInfo = newInfo1
        elif newInfo2 is not None and check_EQTiangle_withoneline(newInfo2, info3):
            newInfo = newInfo2
        if newInfo is not None:
            newInfo.conditions.append(["角边角得出一对全等三角形", info1, info3, info2])

        return newInfo


# 全等三角形对边相等推出对角相等
# class LmEqualTriangle_reverseAngle(Lemma):
#     def __init__(self):
#         self.name = "全等三角形对边相等推出对角相等"
#         self.inputNum = 2
#
#     @staticmethod
#     def Infer(info1, info2):
#         set1 = set()
#         set2 = set()
#         set3 = set()
#         set4 = set()
#         set5 = set()
#         set6 = set()
#         set7 = set()
#         set8 = set()
#         set1.add(info1.p1)
#         set1.add(info1.p2)
#
#         set2.add(info1.p1)
#         set2.add(info1.p3)
#
#         set3.add(info1.p2)
#         set3.add(info1.p3)
#
#         set4.add(info1.p4)
#         set4.add(info1.p5)
#
#         set5.add(info1.p4)
#         set5.add(info1.p6)
#
#         set6.add(info1.p5)
#         set6.add(info1.p6)
#
#         set7.add(info2.p1)
#         set7.add(info2.p2)
#
#         set8.add(info2.p3)
#         set8.add(info2.p4)
#         newInfo = None
#         if (set1 == set7 and set4 == set8) and (set1 == set8 and set4 == set7):
#             newInfo = Informations.EqualAngle(info1.p1, info1.p3, info1.p2, info1.p4, info1.p6, info1.p5)
#
#         elif (set1 == set7 and set5 == set8) and (set1 == set8 and set5 == set7):
#             newInfo = Informations.EqualAngle(info1.p1, info1.p3, info1.p2, info1.p4, info1.p5, info1.p6)
#
#         elif (set1 == set7 and set6 == set8) and (set1 == set8 and set6 == set7):
#             newInfo = Informations.EqualAngle(info1.p1, info1.p3, info1.p2, info1.p5, info1.p4, info1.p6)
#
#         elif (set2 == set7 and set4 == set8) and (set2 == set8 and set4 == set7):
#             newInfo = Informations.EqualAngle(info1.p1, info1.p2, info1.p3, info1.p4, info1.p6, info1.p5)
#
#         elif (set2 == set7 and set5 == set8) and (set2 == set8 and set5 == set7):
#             newInfo = Informations.EqualAngle(info1.p1, info1.p2, info1.p3, info1.p4, info1.p5, info1.p6)
#
#         elif (set2 == set7 and set6 == set8) and (set2 == set8 and set6 == set7):
#             newInfo = Informations.EqualAngle(info1.p1, info1.p2, info1.p3, info1.p5, info1.p4, info1.p6)
#
#         elif (set3 == set7 and set4 == set8) and (set3 == set8 and set4 == set7):
#             newInfo = Informations.EqualAngle(info1.p3, info1.p1, info1.p2, info1.p4, info1.p6, info1.p5)
#
#         elif (set3 == set7 and set5 == set8) and (set3 == set8 and set5 == set7):
#             newInfo = Informations.EqualAngle(info1.p3, info1.p1, info1.p2, info1.p4, info1.p5, info1.p6)
#
#         elif (set3 == set7 and set6 == set8) and (set3 == set8 and set6 == set7):
#             newInfo = Informations.EqualAngle(info1.p3, info1.p1, info1.p2, info1.p5, info1.p4, info1.p6)
#         if newInfo != None:
#             newInfo.source = "全等三角形对边相等推出对角相等"
#             newInfo.conditions.append(info1)
#             newInfo.conditions.append(info2)
#         return newInfo


class LmEqualTriangleGetAngle(Lemma):
    def __init__(self):
        self.name = "全等三角形对角相等"
        self.inputNum = 2

    @staticmethod
    def Infer(info1, equalAngleList, coLineList):  # 输入平行四边形，相等线集合，平行线集合
        newInfo1 = Informations.EqualAngle(info1.p1, info1.p2, info1.p3, info1.p4, info1.p5, info1.p6)
        newInfo2 = Informations.EqualAngle(info1.p2, info1.p1, info1.p3, info1.p5, info1.p4, info1.p6)
        newInfo3 = Informations.EqualAngle(info1.p1, info1.p3, info1.p2, info1.p4, info1.p6, info1.p5)
        flag = False
        flag1 = flag2 = flag3 = flag
        if newInfo1 is not None:
            newInfo1.conditions.append(["全等三角形对角相等", info1])
            res = newInfo1.IsInList(equalAngleList, coLineList)
            newInfo1.weight = info1.weight + 1
            if res is False:
                equalAngleList.append(newInfo1)
                flag1 = True
            elif res is True:
                pass
            else:
                nums = len(equalAngleList[res].conditions)
                for item in equalAngleList[res].conditions:
                    if len(item) != len(newInfo1.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo1.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalAngleList[res].conditions.append(newInfo1.conditions[-1])
                equalAngleList[res].weight = min(newInfo1.weight, equalAngleList[res].weight)

        if newInfo2 is not None:
            newInfo2.conditions.append(["全等三角形对角相等", info1])
            res = newInfo2.IsInList(equalAngleList, coLineList)
            newInfo2.weight = info1.weight + 1
            if res is False:
                equalAngleList.append(newInfo2)
                flag2 = True
            elif res is True:
                pass
            else:
                nums = len(equalAngleList[res].conditions)
                for item in equalAngleList[res].conditions:
                    if len(item) != len(newInfo2.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo2.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalAngleList[res].conditions.append(newInfo2.conditions[-1])
                equalAngleList[res].weight = min(newInfo2.weight, equalAngleList[res].weight)

        if newInfo3 is not None:
            newInfo3.conditions.append(["全等三角形对角相等", info1])
            res = newInfo3.IsInList(equalAngleList, coLineList)
            newInfo3.weight = info1.weight + 1
            if res is False:
                equalAngleList.append(newInfo3)
                flag3 = True
            elif res is True:
                pass
            else:
                nums = len(equalAngleList[res].conditions)
                for item in equalAngleList[res].conditions:
                    if len(item) != len(newInfo3.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo3.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalAngleList[res].conditions.append(newInfo3.conditions[-1])
                equalAngleList[res].weight = min(newInfo3.weight, equalAngleList[res].weight)
        flag = flag1 or flag2 or flag3  # 判断是否存在新的信息
        return flag




class LmEqualTriangleGetLine(Lemma):
    def __init__(self):
        self.name = "全等三角形对边相等"
        self.inputNum = 2

    @staticmethod
    def Infer(info1, equalLineList):  # 输入平行四边形，相等线集合，平行线集合
        newInfo1 = Informations.EqualLine(info1.p1, info1.p2, info1.p4, info1.p5)
        newInfo2 = Informations.EqualLine(info1.p2, info1.p3, info1.p5, info1.p6)
        newInfo3 = Informations.EqualLine(info1.p1, info1.p3, info1.p4, info1.p6)
        flag = False
        flag1 = flag2 = flag3 = flag

        if newInfo1 is not None:
            newInfo1.conditions.append(["全等三角形对边相等", info1])
            res = newInfo1.IsInList(equalLineList)
            newInfo1.weight = info1.weight + 1
            if res is False:
                equalLineList.append(newInfo1)
                flag1 = True
            elif res is True:
                pass
            else:
                nums = len(equalLineList[res].conditions)
                for item in equalLineList[res].conditions:
                    if len(item) != len(newInfo1.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo1.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    if newInfo1.info_name == "相等线EBFD":
                        print(1)
                    equalLineList[res].conditions.append(newInfo1.conditions[-1])
                equalLineList[res].weight = min(newInfo1.weight, equalLineList[res].weight)

        if newInfo2 is not None:
            newInfo2.conditions.append(["全等三角形对边相等", info1])
            res = newInfo2.IsInList(equalLineList)
            newInfo2.weight = info1.weight + 1
            if res is False:
                equalLineList.append(newInfo2)
                flag2 = True
            elif res is True:
                pass
            else:
                nums = len(equalLineList[res].conditions)
                for item in equalLineList[res].conditions:
                    if len(item) != len(newInfo2.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo2.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    if newInfo2.info_name == "相等线EBFD":
                        print(1)
                    equalLineList[res].conditions.append(newInfo2.conditions[-1])
                equalLineList[res].weight = min(newInfo2.weight, equalLineList[res].weight)

        if newInfo3 is not None:
            newInfo3.conditions.append(["全等三角形对边相等", info1])
            res = newInfo3.IsInList(equalLineList)
            newInfo3.weight = info1.weight + 1
            if res is False:
                equalLineList.append(newInfo3)
                flag3 = True
            elif res is True:
                pass
            else:
                nums = len(equalLineList[res].conditions)
                for item in equalLineList[res].conditions:
                    if len(item) != len(newInfo3.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo3.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    if newInfo3.info_name == "相等线EBFD":
                        print(1)
                    equalLineList[res].conditions.append(newInfo3.conditions[-1])
                equalLineList[res].weight = min(newInfo3.weight, equalLineList[res].weight)
        flag = flag1 or flag2 or flag3  # 判断是否存在新的信息
        return flag


# 全等三角形对角相等推出对边相等
# class LmEqualTriangle_reverseLine(Lemma):
#     def __init__(self):
#         self.name = "全等三角形对角相等推出对边相等"
#         self.inputNum = 2
#
#     @staticmethod
#     def Infer(info1, info2):
#         set1 = set()
#         set2 = set()
#         set3 = set()
#         set4 = set()
#
#         set1.add(info1.p1)
#         set1.add(info1.p2)
#         set1.add(info1.p3)
#
#         set2.add(info1.p4)
#         set2.add(info1.p5)
#         set2.add(info1.p6)
#
#         set3.add(info2.p1)
#         set3.add(info2.p2)
#         set3.add(info2.p3)
#
#         set4.add(info2.p4)
#         set4.add(info2.p5)
#         set4.add(info2.p6)
#
#         newInfo = None
#         if (set1 == set3 and set2 == set4) or (set1 == set4 and set2 == set3):
#             newInfo = Informations.EqualLine(info2.p1, info2.p3, info2.p4, info2.p6)
#         if newInfo != None:
#             newInfo.source = "全等三角形对角相等推出对边相等"
#             newInfo.conditions.append(info1)
#             newInfo.conditions.append(info2)
#         return newInfo

# newInfo = None
# if (set1 == set7 and set4 == set8) and (set1 == set8 and set4 == set7):
#     newInfo = Informations.EqualAngle(info1.p1, info1.p3, info1.p2, info1.p4, info1.p6, info1.p5)
#
# elif (set1 == set7 and set5 == set8) and (set1 == set8 and set5 == set7):
#     newInfo = Informations.EqualAngle(info1.p1, info1.p3, info1.p2, info1.p4, info1.p5, info1.p6)
#
# elif (set1 == set7 and set6 == set8) and (set1 == set8 and set6 == set7):
#     newInfo = Informations.EqualAngle(info1.p1, info1.p3, info1.p2, info1.p5, info1.p4, info1.p6)
#
# elif (set2 == set7 and set4 == set8) and (set2 == set8 and set4 == set7):
#     newInfo = Informations.EqualAngle(info1.p1, info1.p2, info1.p3, info1.p4, info1.p6, info1.p5)
#
# elif (set2 == set7 and set5 == set8) and (set2 == set8 and set5 == set7):
#     newInfo = Informations.EqualAngle(info1.p1, info1.p2, info1.p3, info1.p4, info1.p5, info1.p6)
#
# elif (set2 == set7 and set6 == set8) and (set2 == set8 and set6 == set7):
#     newInfo = Informations.EqualAngle(info1.p1, info1.p2, info1.p3, info1.p5, info1.p4, info1.p6)
#
# elif (set3 == set7 and set4 == set8) and (set3 == set8 and set4 == set7):
#     newInfo = Informations.EqualAngle(info1.p3, info1.p1, info1.p2, info1.p4, info1.p6, info1.p5)
#
# elif (set3 == set7 and set5 == set8) and (set3 == set8 and set5 == set7):
#     newInfo = Informations.EqualAngle(info1.p3, info1.p1, info1.p2, info1.p4, info1.p5, info1.p6)
#
# elif (set3 == set7 and set6 == set8) and (set3 == set8 and set6 == set7):
#     newInfo = Informations.EqualAngle(info1.p3, info1.p1, info1.p2, info1.p5, info1.p4, info1.p6)
# if newInfo != None:
#     newInfo.source = "全等三角形对角相等推出对边相等"
#     newInfo.conditions.append(info1)
#     newInfo.conditions.append(info2)
# return newInfo


# 平行传递性
# 输入2组平行信息，1-2与3-4点平行，3-4点与5-6点平行，推理出1-2点平行于5-6点
class LmParallalTransitivity(Lemma):
    def __init__(self):
        self.name = "平行传递性"
        self.inputNum = 2

    @staticmethod
    def Infer(info1, info2):
        set1 = set()
        set1.add(info1.p1)
        set1.add(info1.p2)
        set2 = set()
        set2.add(info1.p3)
        set2.add(info1.p4)
        set3 = set()
        set3.add(info2.p1)
        set3.add(info2.p2)
        set4 = set()
        set4.add(info2.p3)
        set4.add(info2.p4)

        if set1 == set3:
            newInfo = Informations.Parallel(info1.p3, info1.p4, info2.p3, info2.p4)
        elif set1 == set4:
            newInfo = Informations.Parallel(info1.p3, info1.p4, info2.p1, info2.p2)
        elif set2 == set3:
            newInfo = Informations.Parallel(info1.p1, info1.p2, info2.p3, info2.p4)
        elif set2 == set4:
            newInfo = Informations.Parallel(info1.p1, info1.p2, info2.p1, info2.p2)
        else:
            newInfo = None

        if newInfo is not None:
            # newInfo.source = "平行传递性"
            # newInfo.conditions.append(info1)
            newInfo.conditions.append(["平行传递性", info1, info2])
        return newInfo


# 相等线传递性
# 输入2组相等信息，1-2与3-4相等，3-4点与5-6点相等，推理出1-2与5-6相等
class LmEqualLineTransitivity(Lemma):
    def __init__(self):
        self.name = "相等线传递性"
        self.inputNum = 2

    @staticmethod
    def Infer(info1, info2):
        set1 = set()
        set1.add(info1.p1)
        set1.add(info1.p2)
        set2 = set()
        set2.add(info1.p3)
        set2.add(info1.p4)
        set3 = set()
        set3.add(info2.p1)
        set3.add(info2.p2)
        set4 = set()
        set4.add(info2.p3)
        set4.add(info2.p4)

        if set1 == set3:
            newInfo = Informations.EqualLine(info1.p3, info1.p4, info2.p3, info2.p4)
        elif set1 == set4:
            newInfo = Informations.EqualLine(info1.p3, info1.p4, info2.p1, info2.p2)
        elif set2 == set3:
            newInfo = Informations.EqualLine(info1.p1, info1.p2, info2.p3, info2.p4)
        elif set2 == set4:
            newInfo = Informations.EqualLine(info1.p1, info1.p2, info2.p1, info2.p2)
        else:
            newInfo = None

        if newInfo is not None:
            # newInfo.source = "相等线传递性"
            # newInfo.conditions.append(info1)
            newInfo.conditions.append(["相等线传递性", info1, info2])
        return newInfo


# 相等角传递性
# bug
class LmEqualAngleTransitivity(Lemma):
    def __init__(self):
        self.name = "相等角传递性"
        self.inputNum = 3

    @staticmethod
    def Infer(info1, info2, equalAngleList, coLineList):
        newInfo1 = newInfo2 = newInfo3 = None
        flag = flag1 = flag2 = flag3 = False
        # 第一对角里面的第一个角
        set1 = set()
        set1.add(info1.p1)
        set1.add(info1.p3)
        # 第一对角里面的第二个角
        set2 = set()
        set2.add(info1.p4)
        set2.add(info1.p6)
        # 第二对角里面的第一个角
        set3 = set()
        set3.add(info2.p1)
        set3.add(info2.p3)
        # 第二对角里面的第二个角
        set4 = set()
        set4.add(info2.p4)
        set4.add(info2.p6)
        if set1 == set3 and info1.p2 == info2.p2:
            newInfo1 = Informations.EqualAngle(info1.p1, info1.p2, info1.p3, info2.p4, info2.p5, info2.p6)  # 1 4
            newInfo2 = Informations.EqualAngle(info2.p1, info2.p2, info2.p3, info1.p4, info1.p5, info1.p6)  # 3 2
            newInfo3 = Informations.EqualAngle(info1.p4, info1.p5, info1.p6, info2.p4, info2.p5, info2.p6)  # 2 4
        elif set1 == set4 and info1.p2 == info2.p5:
            newInfo1 = Informations.EqualAngle(info1.p1, info1.p2, info1.p3, info2.p1, info2.p2, info2.p3)  # 1 3
            newInfo2 = Informations.EqualAngle(info1.p4, info1.p5, info1.p6, info2.p4, info2.p5, info2.p6)  # 2 4
            newInfo3 = Informations.EqualAngle(info2.p1, info2.p2, info2.p3, info1.p1, info1.p2, info1.p3)  # 3 1
        elif set2 == set3 and info1.p5 == info2.p2:
            newInfo1 = Informations.EqualAngle(info1.p1, info1.p2, info1.p3, info2.p1, info2.p2, info2.p3)  # 1 3
            newInfo2 = Informations.EqualAngle(info1.p1, info1.p2, info1.p3, info2.p4, info2.p5, info2.p6)  # 1 4
            newInfo3 = Informations.EqualAngle(info1.p4, info1.p5, info1.p6, info2.p4, info2.p5, info2.p6)  # 2 4
        elif set2 == set4 and info1.p5 == info2.p5:
            newInfo1 = Informations.EqualAngle(info1.p1, info1.p2, info1.p3, info2.p1, info2.p2, info2.p3)  # 1 3
            newInfo2 = Informations.EqualAngle(info1.p1, info1.p2, info1.p3, info2.p4, info2.p5, info2.p6)  # 1 4
            newInfo3 = Informations.EqualAngle(info1.p4, info1.p5, info1.p6, info2.p1, info2.p2, info2.p3)  # 2 3
        else:
            return False
            # if set5 == set7 and info1.p2 == info2.p2:
        #     newInfo = Informations.EqualAngle(info1.p4, info1.p5, info1.p6, info2.p1, info2.p2, info2.p3)
        # if set5 == set8 and info1.p2 == info2.p5:
        #     newInfo = Informations.EqualAngle(info1.p4, info1.p5, info1.p6, info2.p4, info2.p5, info2.p6)
        # if set6 == set7 and info1.p5 == info2.p2:
        #     newInfo = Informations.EqualAngle(info1.p1, info1.p2, info1.p3, info2.p1, info2.p2, info2.p3)
        # if set6 == set8 and info1.p5 == info2.p5:
        #     newInfo = Informations.EqualAngle(info1.p1, info1.p2, info1.p3, info2.p4, info2.p5, info2.p6)
        # if set5 != set6:
        #     if info1.p2 == info2.p2 and set1 == set3:
        #         newInfo = Informations.EqualAngle(info1.p4, info1.p5, info1.p6, info2.p4, info2.p5, info2.p6)
        #     elif info1.p2 == info2.p5 and set1 == set4:
        #         newInfo = Informations.EqualAngle(info1.p4, info1.p5, info1.p6, info2.p1, info2.p2, info2.p3)
        #     elif info1.p5 == info2.p2 and set2 == set3:
        #         newInfo = Informations.EqualAngle(info1.p1, info1.p2, info1.p3, info2.p4, info2.p5, info2.p6)
        #     elif info1.p5 == info2.p5 and set2 == set4:
        #         newInfo = Informations.EqualAngle(info1.p1, info1.p2, info1.p3, info2.p1, info2.p2, info2.p3)
        #     else:
        #         newInfo = None
        # else:
        #     newInfo = None
        if newInfo1 is not None:
            # 用一个res来存IsInList返回的值
            newInfo1.conditions.append(["相等角传递性", info1, info2])
            res = newInfo1.IsInList(equalAngleList, coLineList)
            newInfo1.weight = max(info1.weight, info2.weight) + 1
            if res is False:
                equalAngleList.append(newInfo1)
                flag1 = True
            elif res is True:
                pass
            else:
                nums = len(equalAngleList[res].conditions)
                for item in equalAngleList[res].conditions:
                    if len(item) != len(newInfo1.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo1.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalAngleList[res].conditions.append(newInfo1.conditions[-1])
                equalAngleList[res].weight = min(newInfo1.weight, equalAngleList[res].weight)
        if newInfo2 is not None:
            # 用一个res来存IsInList返回的值
            newInfo2.conditions.append(["相等角传递性", info1, info2])
            res = newInfo2.IsInList(equalAngleList, coLineList)
            newInfo2.weight = max(info1.weight, info2.weight) + 1
            if res is False:
                equalAngleList.append(newInfo2)
                flag2 = True
            elif res is True:
                pass
            else:
                nums = len(equalAngleList[res].conditions)
                for item in equalAngleList[res].conditions:
                    if len(item) != len(newInfo2.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo2.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalAngleList[res].conditions.append(newInfo2.conditions[-1])
                equalAngleList[res].weight = min(newInfo2.weight, equalAngleList[res].weight)
        if newInfo3 is not None:
            # 用一个res来存IsInList返回的值
            newInfo3.conditions.append(["相等角传递性", info1, info2])
            res = newInfo3.IsInList(equalAngleList, coLineList)
            newInfo3.weight = max(info1.weight, info2.weight) + 1
            if res is False:
                equalAngleList.append(newInfo3)
                flag3 = True
            elif res is True:
                pass
            else:
                nums = len(equalAngleList[res].conditions)
                for item in equalAngleList[res].conditions:
                    if len(item) != len(newInfo3.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo3.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalAngleList[res].conditions.append(newInfo3.conditions[-1])
                equalAngleList[res].weight = min(newInfo3.weight, equalAngleList[res].weight)
        flag = flag1 or flag2 or flag3

        return flag


# 两对边平行的四边形是平行四边形
# 输入2组平行信息，1-2与3-4点平行，5-6点与7-8点平行，若这四点对应重合，推理出1-2-3-4是平行四边形
class LmParallelogramaDetermination1(Lemma):
    def __init__(self):
        self.name = "两对边平行的四边形是平行四边形"
        self.inputNum = 2

    @staticmethod
    def Infer(info1, info2):
        newInfo = None
        set1 = set()
        set1.add(info1.p1)
        set1.add(info1.p2)
        set1.add(info1.p3)
        set1.add(info1.p4)

        set2 = set()
        set2.add(info2.p1)
        set2.add(info2.p2)
        set2.add(info2.p3)
        set2.add(info2.p4)

        check1 = set()
        check2 = set()
        check3 = set()
        check4 = set()
        check1.update(info1.p1, info1.p3)
        check2.update(info1.p2, info1.p4)
        check3.update(info1.p1, info1.p4)
        check4.update(info1.p2, info1.p3)
        check_a = set()
        check_b = set()
        check_a.update(info2.p1, info2.p2)
        check_b.update(info2.p3, info2.p4)
        if set1 == set2:  # 两个集合相等
            # 判断一下平行四边形的四点顺序
            if (check3 == check_a and check4 == check_b) or (check3 == check_b and check4 == check_a):
                newInfo = Informations.Parallogram(info1.p1, info1.p2, info1.p3, info1.p4)
            elif (check1 == check_a and check2 == check_b) or (check1 == check_b and check2 == check_a):
                newInfo = Informations.Parallogram(info1.p1, info1.p2, info1.p4, info1.p3)
        else:
            newInfo = None

        if newInfo is not None:
            # newInfo.source = "两对边平行的四边形是平行四边形"
            # newInfo.conditions.append(info1)
            newInfo.conditions.append(["两对边平行的四边形是平行四边形", info1, info2])

        return newInfo


# 一对边平行且相等的四边形是平行四边形
# 输入4个点，1-2点与3-4点平行，且 1-2点线段与3-4点线段相等，推理出1-2-3-4点构成平行四边形
class LmParallelogramaDetermination2(Lemma):
    def __init__(self):
        self.name = "一对边平行且相等的四边形是平行四边形"
        self.inputNum = 2

    @staticmethod
    def Infer(info1, info2, pointList):
        set1 = set()
        set2 = set()
        set1.add(info1.p1)
        set1.add(info1.p2)
        set2.add(info1.p3)
        set2.add(info1.p4)

        set3 = set()
        set4 = set()
        set3.add(info2.p1)
        set3.add(info2.p2)
        set4.add(info2.p3)
        set4.add(info2.p4)

        if (set1 == set3 and set2 == set4) or (set1 == set4 and set2 == set3):  # 两个集合相等
            p1 = p2 = p3 = p4 = ()
            for position in pointList:
                if position.p1 == info2.p1:
                    p1 = position.position
                elif position.p1 == info2.p2:
                    p2 = position.position
                elif position.p1 == info2.p3:
                    p3 = position.position
                elif position.p1 == info2.p4:
                    p4 = position.position
            if p1 is None or p1 is None or p1 is None or p1 is None:
                return None
            check = Engine.check_parallelogram(p1, p2, p3, p4)
            if check:
                newInfo = Informations.Parallogram(info2.p1, info2.p2, info2.p3, info2.p4)
            else:
                newInfo = Informations.Parallogram(info2.p1, info2.p2, info2.p4, info2.p3)
        else:
            newInfo = None

        if newInfo is not None:
            # newInfo.source = "一对边平行且相等的四边形是平行四边形"
            # newInfo.conditions.append(info1)
            newInfo.conditions.append(["一对边平行且相等的四边形是平行四边形", info1, info2])

        return newInfo


# 平行四边形得到线线相等和线线平行
class LmParallogramGetLineParall(Lemma):
    def __init__(self):
        self.name = "平行四边形对边平行且相等"
        self.inputNum = 2

    @staticmethod
    def Infer(parallogra, equalLineList, parallelLineList):  # 输入平行四边形，相等线集合，平行线集合
        # 第一对平行相等线
        a_line_eqaul = Informations.EqualLine(parallogra.p1, parallogra.p2, parallogra.p3, parallogra.p4)
        a_line_parallogra = Informations.Parallel(parallogra.p1, parallogra.p2, parallogra.p3, parallogra.p4)
        # 第二对平行相等线
        b_line_equal = Informations.EqualLine(parallogra.p1, parallogra.p4, parallogra.p2, parallogra.p3)
        b_line_parallogra = Informations.Parallel(parallogra.p1, parallogra.p4, parallogra.p2, parallogra.p3)
        flag = False
        flag1 = flag2 = flag3 = flag4 = flag
        if a_line_eqaul is not None:
            a_line_eqaul.conditions.append(["平行四边形对边相等1", parallogra])
            res = a_line_eqaul.IsInList(equalLineList)
            a_line_eqaul.weight = parallogra.weight + 1
            if res is False:
                equalLineList.append(a_line_eqaul)
                flag1 = True
            elif res is True:
                pass
            else:
                nums = len(equalLineList[res].conditions)
                for item in equalLineList[res].conditions:
                    if len(item) != len(a_line_eqaul.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != a_line_eqaul.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalLineList[res].conditions.append(a_line_eqaul.conditions[-1])
                equalLineList[res].weight = min(a_line_eqaul.weight, equalLineList[res].weight)

        # if a_line_parallogra.IsInList(parallelLineList) is False:
        #     # a_line_parallogra.source = "平行四边形对边平行"
        #     a_line_parallogra.conditions.append(["平行四边形对边平行", parallogra])
        #     parallelLineList.append(a_line_parallogra)
        #     flag2 = True
        if a_line_parallogra is not None:
            a_line_parallogra.conditions.append(["平行四边形对边平行", parallogra])
            res = a_line_parallogra.IsInList(parallelLineList)
            a_line_parallogra.weight = parallogra.weight + 1
            if res is False:
                parallelLineList.append(a_line_parallogra)
                flag2 = True
            elif res is True:
                pass
            else:
                nums = len(parallelLineList[res].conditions)
                for item in parallelLineList[res].conditions:
                    if len(item) != len(a_line_parallogra.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != a_line_parallogra.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    parallelLineList[res].conditions.append(a_line_parallogra.conditions[-1])
                parallelLineList[res].weight = min(a_line_parallogra.weight, parallelLineList[res].weight)


        # if b_line_equal.IsInList(equalLineList) is False:
        #     b_line_equal.conditions.append(["平行四边形对边相等", parallogra])
        #     equalLineList.append(b_line_equal)
        #     flag3 = True
        if b_line_equal is not None:
            b_line_equal.conditions.append(["平行四边形对边相等2", parallogra])
            res = b_line_equal.IsInList(equalLineList)
            b_line_equal.weight = parallogra.weight + 1
            if res is False:
                equalLineList.append(b_line_equal)
                flag1 = True
            elif res is True:
                pass
            else:
                nums = len(equalLineList[res].conditions)
                for item in equalLineList[res].conditions:
                    if len(item) != len(b_line_equal.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != b_line_equal.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalLineList[res].conditions.append(b_line_equal.conditions[-1])
                equalLineList[res].weight = min(b_line_equal.weight, equalLineList[res].weight)


        # if b_line_parallogra.IsInList(parallelLineList) is False:
        #     # b_line_parallogra.source = "平行四边形对边平行"
        #     b_line_parallogra.conditions.append(["平行四边形对边平行", parallogra])
        #     parallelLineList.append(b_line_parallogra)
        #     flag4 = True
        if b_line_parallogra is not None:
            b_line_parallogra.conditions.append(["平行四边形对边平行", parallogra])
            res = b_line_parallogra.IsInList(parallelLineList)
            b_line_parallogra.weight = parallogra.weight + 1
            if res is False:
                parallelLineList.append(b_line_parallogra)
                flag2 = True
            elif res is True:
                pass
            else:
                nums = len(parallelLineList[res].conditions)
                for item in parallelLineList[res].conditions:
                    if len(item) != len(b_line_parallogra.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != b_line_parallogra.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    parallelLineList[res].conditions.append(a_line_eqaul.conditions[-1])
                parallelLineList[res].weight = min(a_line_eqaul.weight, parallelLineList[res].weight)


        flag = flag1 or flag2 or flag3 or flag4  # 判断是否存在新的信息
        # print(flag,flag2,flag3,flag4)
        return flag






class LmParallogramGetneiangle(Lemma):
    def __init__(self):
        self.name = "平行四边形内错角相等"
        self.inputNum = 2

    @staticmethod
    def Infer(parallogra, equalAngleList, coLineList):  # 输入平行四边形，相等角集合
        # 第一对内错角
        a_angle_eqaul = Informations.EqualAngle(parallogra.p1, parallogra.p2, parallogra.p4, parallogra.p3,
                                                parallogra.p4, parallogra.p2)
        # 第二对内错角
        b_angle_eqaul = Informations.EqualAngle(parallogra.p3, parallogra.p2, parallogra.p4, parallogra.p1,
                                                parallogra.p4, parallogra.p2)
        # 第三对内错角
        c_angle_eqaul = Informations.EqualAngle(parallogra.p2, parallogra.p1, parallogra.p3, parallogra.p4,
                                                parallogra.p3, parallogra.p1)
        # 第四对内错角
        d_angle_eqaul = Informations.EqualAngle(parallogra.p4, parallogra.p1, parallogra.p3, parallogra.p2,
                                                parallogra.p3, parallogra.p1)

        flag = False
        flag1 = flag2 = flag3 = flag4 = flag
        if a_angle_eqaul is not None:
            # 用一个res来存IsInList返回的值
            a_angle_eqaul.conditions.append(["平行四边形内错角相等", parallogra])
            res = a_angle_eqaul.IsInList(equalAngleList, coLineList)
            a_angle_eqaul.weight = parallogra.weight + 1
            if res is False:
                equalAngleList.append(a_angle_eqaul)
                flag1 = True
            elif res is True:
                pass
            else:
                nums = len(equalAngleList[res].conditions)
                for item in equalAngleList[res].conditions:
                    if len(item) != len(a_angle_eqaul.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != a_angle_eqaul.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalAngleList[res].conditions.append(a_angle_eqaul.conditions[-1])
                equalAngleList[res].weight = min(a_angle_eqaul.weight, equalAngleList[res].weight)
        if b_angle_eqaul is not None:
            # 用一个res来存IsInList返回的值
            b_angle_eqaul.conditions.append(["平行四边形内错角相等", parallogra])
            res = b_angle_eqaul.IsInList(equalAngleList, coLineList)
            b_angle_eqaul.weight = parallogra.weight + 1
            if res is False:
                equalAngleList.append(b_angle_eqaul)
                flag2 = True
            elif res is True:
                pass
            else:
                nums = len(equalAngleList[res].conditions)
                for item in equalAngleList[res].conditions:
                    if len(item) != len(b_angle_eqaul.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != b_angle_eqaul.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalAngleList[res].conditions.append(b_angle_eqaul.conditions[-1])
                equalAngleList[res].weight = min(b_angle_eqaul.weight, equalAngleList[res].weight)
        if c_angle_eqaul is not None:
            # 用一个res来存IsInList返回的值
            c_angle_eqaul.conditions.append(["平行四边形内错角相等", parallogra])
            res = c_angle_eqaul.IsInList(equalAngleList, coLineList)
            c_angle_eqaul.weight = parallogra.weight + 1
            if res is False:
                equalAngleList.append(c_angle_eqaul)
                flag3 = True
            elif res is True:
                pass
            else:
                nums = len(equalAngleList[res].conditions)
                for item in equalAngleList[res].conditions:
                    if len(item) != len(c_angle_eqaul.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != c_angle_eqaul.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalAngleList[res].conditions.append(c_angle_eqaul.conditions[-1])
                equalAngleList[res].weight = min(c_angle_eqaul.weight, equalAngleList[res].weight)
        if d_angle_eqaul is not None:
            # 用一个res来存IsInList返回的值
            d_angle_eqaul.conditions.append(["平行四边形内错角相等", parallogra])
            res = d_angle_eqaul.IsInList(equalAngleList, coLineList)
            d_angle_eqaul.weight = parallogra.weight + 1
            if res is False:
                equalAngleList.append(d_angle_eqaul)
                flag4 = True
            elif res is True:
                pass
            else:
                nums = len(equalAngleList[res].conditions)
                for item in equalAngleList[res].conditions:
                    if len(item) != len(d_angle_eqaul.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != d_angle_eqaul.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalAngleList[res].conditions.append(d_angle_eqaul.conditions[-1])
                equalAngleList[res].weight = min(d_angle_eqaul.weight, equalAngleList[res].weight)

        flag = flag1 or flag2 or flag3 or flag4  # 判断是否存在新的信息
        # print(flag,flag2,flag3,flag4)
        return flag


class LmParallogramGetduiangle(Lemma):
    def __init__(self):
        self.name = "平行四边形对角相等"
        self.inputNum = 2

    @staticmethod
    def Infer(parallogra, equalAngleList, coLineList):  # 输入平行四边形，相等角集合
        # 第一对 对角
        a_angle_eqaul = Informations.EqualAngle(parallogra.p1, parallogra.p2, parallogra.p3, parallogra.p3,
                                                parallogra.p4, parallogra.p1)
        # 第二对 对角
        b_angle_eqaul = Informations.EqualAngle(parallogra.p4, parallogra.p1, parallogra.p2, parallogra.p2,
                                                parallogra.p3, parallogra.p4)

        flag = False
        flag1 = flag2 = flag
        if a_angle_eqaul is not None:
            # 用一个res来存IsInList返回的值
            a_angle_eqaul.conditions.append(["平行四边形对角相等", parallogra])
            res = a_angle_eqaul.IsInList(equalAngleList, coLineList)
            a_angle_eqaul.weight = parallogra.weight + 1
            if res is False:
                equalAngleList.append(a_angle_eqaul)
                flag1 = True
            elif res is True:
                pass
            else:
                nums = len(equalAngleList[res].conditions)
                for item in equalAngleList[res].conditions:
                    if len(item) != len(a_angle_eqaul.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != a_angle_eqaul.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalAngleList[res].conditions.append(a_angle_eqaul.conditions[-1])
                equalAngleList[res].weight = min(a_angle_eqaul.weight, equalAngleList[res].weight)
        if b_angle_eqaul is not None:
            # 用一个res来存IsInList返回的值
            b_angle_eqaul.conditions.append(["平行四边形对角相等", parallogra])
            res = b_angle_eqaul.IsInList(equalAngleList, coLineList)
            b_angle_eqaul.weight = parallogra.weight + 1
            if res is False:
                equalAngleList.append(b_angle_eqaul)
                flag2 = True
            elif res is True:
                pass
            else:
                nums = len(equalAngleList[res].conditions)
                for item in equalAngleList[res].conditions:
                    if len(item) != len(b_angle_eqaul.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != b_angle_eqaul.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalAngleList[res].conditions.append(b_angle_eqaul.conditions[-1])
                equalAngleList[res].weight = min(b_angle_eqaul.weight, equalAngleList[res].weight)

        flag = flag1 or flag2  # 判断是否存在新的信息
        return flag


class LmParallogramGetduiLine(Lemma):
    def __init__(self):
        self.name = "平行四边形对边互相平分"
        self.inputNum = 3

    @staticmethod
    def Infer(info1, info2, midPointList, parallogra):  # 输入平行四边形，相等角集合
        # 第一个中点
        newInfo1 = Informations.MidPoint(info1.p1, info1.p2, info1.p3)
        # 第二个中点
        newInfo2 = Informations.MidPoint(info2.p1, info2.p2, info2.p3)
        flag = False
        flag1 = flag2 = flag
        if newInfo1 is not None:
            # 用一个res来存IsInList返回的值
            newInfo1.conditions.append(["平行四边形对边互相平分", parallogra, info1])
            res = newInfo1.IsInList(midPointList)
            newInfo1.weight = max(parallogra.weight, info1.weight) + 1
            if res is False:
                midPointList.append(newInfo1)
                flag1 = True
            elif res is True:
                pass
            else:
                nums = len(midPointList[res].conditions)
                for item in midPointList[res].conditions:
                    if len(item) != len(newInfo1.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo1.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    midPointList[res].conditions.append(newInfo1.conditions[-1])
                midPointList[res].weight = min(newInfo1.weight, midPointList[res].weight)
        if newInfo2 is not None:
            # 用一个res来存IsInList返回的值
            newInfo2.conditions.append(["平行四边形对边互相平分", parallogra, info2])
            res = newInfo2.IsInList(midPointList)
            newInfo2.weight = max(parallogra.weight, info2.weight) + 1
            if res is False:
                midPointList.append(newInfo2)
                flag2 = True
            elif res is True:
                pass
            else:
                nums = len(midPointList[res].conditions)
                for item in midPointList[res].conditions:
                    if len(item) != len(newInfo2.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo2.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    midPointList[res].conditions.append(newInfo2.conditions[-1])
                midPointList[res].weight = min(newInfo2.weight, midPointList[res].weight)

        flag = flag1 or flag2  # 判断是否存在新的信息
        return flag


#   中点平分
class LmMidPoint_EqualLine:
    def __init__(self):
        self.name = "中点平分线段"
        self.inputNum = 1

    @staticmethod
    def Infer(info1):
        newInfo = Informations.EqualLine(info1.p2, info1.p1, info1.p3, info1.p1)
        # newInfo.source = "中点平分线段"
        newInfo.conditions.append(["中点平分线段", info1])
        return newInfo


# 中位线定理
# 输入两个中点信息，推理两中点构成线平行于底边（前提是中点信息中要有一个点重合）
class LmMedianLine(Lemma):
    def __init__(self):
        self.name = "中位线定理"
        self.inputNum = 4

    @staticmethod
    def Infer(info1, info2, parallelLineList, ratioLineList):
        flag1 = flag2 = False
        newInfo1 = newInfo2 = None
        if info1.p2 == info2.p2:
            newInfo1 = Informations.Parallel(info1.p1, info2.p1, info1.p3, info2.p3)
            newInfo2 = Informations.RatioLine(info1.p1, info2.p1, info1.p3, info2.p3, 1, 2)
        elif info1.p2 == info2.p3:
            newInfo1 = Informations.Parallel(info1.p1, info2.p1, info1.p3, info2.p2)
            newInfo2 = Informations.RatioLine(info1.p1, info2.p1, info1.p3, info2.p2, 1, 2)
        elif info1.p3 == info2.p2:
            newInfo1 = Informations.Parallel(info1.p1, info2.p1, info1.p2, info2.p3)
            newInfo2 = Informations.RatioLine(info1.p1, info2.p1, info1.p2, info2.p3, 1, 2)
        elif info1.p3 == info2.p3:
            newInfo1 = Informations.Parallel(info1.p1, info2.p1, info1.p2, info2.p2)
            newInfo2 = Informations.RatioLine(info1.p1, info2.p1, info1.p2, info2.p2, 1, 2)
        if newInfo1 is not None:
            # 用一个res来存IsInList返回的值
            newInfo1.conditions.append(["中位线定理", info1, info2])
            res = newInfo1.IsInList(parallelLineList)
            newInfo1.weight = max(info1.weight, info2.weight) + 1
            if res is False:
                parallelLineList.append(newInfo1)
                flag1 = True
            elif res is True:
                pass
            else:
                nums = len(parallelLineList[res].conditions)
                for item in parallelLineList[res].conditions:
                    if len(item) != len(newInfo1.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo1.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    parallelLineList[res].conditions.append(newInfo1.conditions[-1])
                parallelLineList[res].weight = min(newInfo1.weight, parallelLineList[res].weight)
        if newInfo2 is not None:
            # 用一个res来存IsInList返回的值
            newInfo2.conditions.append(["中位线定理_2", info1, info2])
            res = newInfo2.IsInList(ratioLineList)
            newInfo2.weight = max(info1.weight, info2.weight) + 1
            if res is False:
                ratioLineList.append(newInfo2)
                flag2 = True
            elif res is True:
                pass
            else:
                nums = len(ratioLineList[res].conditions)
                for item in ratioLineList[res].conditions:
                    if len(item) != len(newInfo2.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo2.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    ratioLineList[res].conditions.append(newInfo2.conditions[-1])
                ratioLineList[res].weight = min(newInfo2.weight, ratioLineList[res].weight)
        flag = flag1 or flag2
        return flag


# 成比例线段的传递性
class LmRatioLineGetMore(Lemma):
    def __init__(self):
        self.name = "成比例线段的传递性"
        self.inputNum = 4

    @staticmethod
    def Infer(info1, info2, ratioLineList, equalLineList):
        flag1 = flag2 = False
        newInfo1 = newInfo2 = None
        set1 = set()
        set2 = set()
        set3 = set()
        set4 = set()
        set1.update(info1.p1, info1.p2)
        set2.update(info1.p3, info1.p4)
        set3.update(info2.p1, info2.p2)
        set4.update(info2.p3, info2.p4)
        if set1 == set3:
            fraction_temp = Fraction(Fraction(info2.num1, info2.num2), Fraction(info1.num1, info1.num2))
            newInfo1 = Informations.RatioLine(info1.p3, info1.p4, info2.p3, info2.p4, fraction_temp.numerator,
                                              fraction_temp.denominator)
            if fraction_temp.numerator == fraction_temp.denominator:
                newInfo2 = Informations.EqualLine(info1.p3, info1.p4, info2.p3, info2.p4)
        elif set1 == set4:
            fraction_temp = Fraction(Fraction(info2.num2, info2.num1), Fraction(info1.num1, info1.num2))
            newInfo1 = Informations.RatioLine(info1.p3, info1.p4, info2.p1, info2.p2, fraction_temp.numerator,
                                              fraction_temp.denominator)
            if fraction_temp.numerator == fraction_temp.denominator:
                newInfo2 = Informations.EqualLine(info1.p3, info1.p4, info2.p1, info2.p2)
        elif set2 == set3:
            fraction_temp = Fraction(Fraction(info2.num1, info2.num2), Fraction(info1.num2, info1.num1))
            newInfo1 = Informations.RatioLine(info1.p1, info1.p2, info2.p3, info2.p4, fraction_temp.numerator,
                                              fraction_temp.denominator)
            if fraction_temp.numerator == fraction_temp.denominator:
                newInfo2 = Informations.EqualLine(info1.p1, info1.p2, info2.p3, info2.p4)
        elif set2 == set4:
            fraction_temp = Fraction(Fraction(info2.num2, info2.num1), Fraction(info1.num2, info1.num1))
            newInfo1 = Informations.RatioLine(info1.p1, info1.p2, info2.p1, info2.p2, fraction_temp.numerator,
                                              fraction_temp.denominator)
            if fraction_temp.numerator == fraction_temp.denominator:
                newInfo2 = Informations.EqualLine(info1.p1, info1.p2, info2.p1, info2.p2)
        if newInfo1 is not None:
            # 用一个res来存IsInList返回的值
            newInfo1.conditions.append(["线段成比例", info1, info2])
            res = newInfo1.IsInList(ratioLineList)
            newInfo1.weight = max(info1.weight, info2.weight) + 1
            if res is False:
                ratioLineList.append(newInfo1)
                flag1 = True
            elif res is True:
                pass
            else:
                nums = len(ratioLineList[res].conditions)
                for item in ratioLineList[res].conditions:
                    if len(item) != len(newInfo1.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo1.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    ratioLineList[res].conditions.append(newInfo1.conditions[-1])
                ratioLineList[res].weight = min(newInfo1.weight, ratioLineList[res].weight)
        if newInfo2 is not None:
            # 用一个res来存IsInList返回的值
            newInfo2.conditions.append(["线段成比例", info1, info2])
            res = newInfo2.IsInList(equalLineList)
            newInfo2.weight = max(info1.weight, info2.weight) + 1
            if res is False:
                equalLineList.append(newInfo2)
                flag2 = True
            elif res is True:
                pass
            else:
                nums = len(equalLineList[res].conditions)
                for item in equalLineList[res].conditions:
                    if len(item) != len(newInfo2.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo2.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalLineList[res].conditions.append(newInfo2.conditions[-1])
                equalLineList[res].weight = min(newInfo2.weight, equalLineList[res].weight)

        flag = flag1 or flag2
        return flag


# 成比例角的传递性
class LmRatioAngleGetMore(Lemma):
    def __init__(self):
        self.name = "成比例角的传递性"
        self.inputNum = 4

    @staticmethod
    def Infer(info1, info2, ratioAngleList, equalAngleList, coLineList):
        flag1 = flag2 = False
        newInfo1 = newInfo2 = None
        set1 = set()
        set2 = set()
        set3 = set()
        set4 = set()
        set1.update(info1.p1, info1.p3)
        set2.update(info1.p4, info1.p6)
        set3.update(info2.p1, info2.p3)
        set4.update(info2.p4, info2.p6)
        if set1 == set3 and info1.p2 == info2.p2:
            fraction_temp = Fraction(Fraction(info2.num1, info2.num2), Fraction(info1.num1, info1.num2))
            newInfo1 = Informations.RatioAngle(info1.p4, info1.p5, info1.p6, info2.p4, info2.p5, info2.p6,
                                               fraction_temp.numerator,
                                               fraction_temp.denominator)
            if fraction_temp.numerator == fraction_temp.denominator:
                newInfo2 = Informations.EqualAngle(info1.p4, info1.p5, info1.p6, info2.p4, info2.p5, info2.p6)

        elif set1 == set4 and info1.p2 == info2.p5:
            fraction_temp = Fraction(Fraction(info2.num2, info2.num1), Fraction(info1.num1, info1.num2))
            newInfo1 = Informations.RatioAngle(info1.p4, info1.p5, info1.p6, info2.p1, info2.p2, info2.p3,
                                               fraction_temp.numerator,
                                               fraction_temp.denominator)
            if fraction_temp.numerator == fraction_temp.denominator:
                newInfo2 = Informations.EqualAngle(info1.p4, info1.p5, info1.p6, info2.p1, info2.p2, info2.p3)

        elif set2 == set3 and info1.p5 == info2.p2:
            fraction_temp = Fraction(Fraction(info2.num1, info2.num2), Fraction(info1.num2, info1.num1))
            newInfo1 = Informations.RatioAngle(info1.p1, info1.p2, info1.p3, info2.p4, info2.p5, info2.p6,
                                               fraction_temp.numerator,
                                               fraction_temp.denominator)
            if fraction_temp.numerator == fraction_temp.denominator:
                newInfo2 = Informations.EqualAngle(info1.p1, info1.p2, info1.p3, info2.p4, info2.p5, info2.p6)

        elif set2 == set4 and info1.p5 == info2.p5:
            fraction_temp = Fraction(Fraction(info2.num2, info2.num1), Fraction(info1.num2, info1.num1))
            newInfo1 = Informations.RatioAngle(info1.p1, info1.p2, info1.p3, info2.p1, info2.p2, info2.p3,
                                               fraction_temp.numerator,
                                               fraction_temp.denominator)
            if fraction_temp.numerator == fraction_temp.denominator:
                newInfo2 = Informations.EqualAngle(info1.p1, info1.p2, info1.p3, info2.p1, info2.p2, info2.p3)
        if newInfo1 is not None:
            # 用一个res来存IsInList返回的值
            newInfo1.conditions.append(["角成比例", info1, info2])
            res = newInfo1.IsInList(ratioAngleList, coLineList)
            newInfo1.weight = max(info1.weight, info2.weight) + 1
            if res is False:
                ratioAngleList.append(newInfo1)
                flag1 = True
            elif res is True:
                pass
            else:
                nums = len(ratioAngleList[res].conditions)
                for item in ratioAngleList[res].conditions:
                    if len(item) != len(newInfo1.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo1.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    ratioAngleList[res].conditions.append(newInfo1.conditions[-1])
                ratioAngleList[res].weight = min(newInfo1.weight, ratioAngleList[res].weight)
        if newInfo2 is not None:
            # 用一个res来存IsInList返回的值
            newInfo2.conditions.append(["角成比例", info1, info2])
            res = newInfo2.IsInList(equalAngleList, coLineList)
            newInfo2.weight = max(info1.weight, info2.weight) + 1
            if res is False:
                equalAngleList.append(newInfo2)
                flag2 = True
            elif res is True:
                pass
            else:
                nums = len(equalAngleList[res].conditions)
                for item in equalAngleList[res].conditions:
                    if len(item) != len(newInfo2.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo2.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalAngleList[res].conditions.append(newInfo2.conditions[-1])
                equalAngleList[res].weight = min(newInfo2.weight, equalAngleList[res].weight)
        flag = flag1 or flag2
        return flag


# # 平行四边形对边有中点，推出四条小边平行且相等
# class Lmparallogram_Oppo_Midpoint(Lemma):
#     def __init__(self):
#         self.name = "平行四边形对边有中点，被两个中点分割出的四条边相等"
#         self.inputNum = 5
#
#     @staticmethod
#     def Infer(info1, info2, info3, equalLineList, parallelLineList):
#         set1 = set()
#         set2 = set()
#         set3 = set()
#         set4 = set()
#         set1.add(info3.p1)
#         set1.add(info3.p2)
#         set2.add(info3.p3)
#         set2.add(info3.p4)
#         set3.add(info3.p2)
#         set3.add(info3.p3)
#         set4.add(info3.p4)
#         set4.add(info3.p1)
#
#         set5 = set()
#         set6 = set()
#         set5.add(info1.p2)
#         set5.add(info1.p3)
#         set6.add(info2.p2)
#         set6.add(info2.p3)
#
#         flag = False
#         a = b = c = d = flag
#         a1 = a2 = b1 = b2 = c1 = c2 = d1 = d2 = flag
#
#         if (set1 == set5 and set2 == set6):
#             a_line_parallogra = Informations.Parallel(info3.p1, info1.p1, info3.p3, info2.p1)
#
#             a_line_eqaul = Informations.EqualLine(info3.p1, info1.p1, info3.p3, info2.p1)
#             if a_line_eqaul.IsInList(equalLineList) is False:
#                 # a_line_eqaul.source = "平行四边形对边有中点，被两个中点分割出的四条边相等"
#                 # a_line_eqaul.conditions.append(info3)
#                 # a_line_eqaul.conditions.append(info1)
#                 a_line_eqaul.conditions.append(["平行四边形对边有中点，被两个中点分割出的四条边相等", info3, info1, info2])
#                 equalLineList.append(a_line_eqaul)
#                 a1 = True
#             if a_line_parallogra.IsInList(parallelLineList) is False:
#                 # a_line_parallogra.source = "平行四边形对边有中点，被两个中点分割出的四条边平行"
#                 # a_line_parallogra.conditions.append(info3)
#                 # a_line_parallogra.conditions.append(info1)
#                 a_line_parallogra.conditions.append(["平行四边形对边有中点，被两个中点分割出的四条边平行", info3, info1, info2])
#                 parallelLineList.append(a_line_parallogra)
#                 a2 = True
#             a = a1 or a2
#         elif (set1 == set6 and set2 == set5):
#             b_line_parallogra = Informations.Parallel(info3.p1, info2.p1, info3.p3, info1.p1)
#             b_line_eqaul = Informations.EqualLine(info3.p1, info2.p1, info3.p3, info1.p1)
#             if b_line_eqaul.IsInList(equalLineList) is False:
#                 # b_line_eqaul.source = "平行四边形对边有中点，被两个中点分割出的四条边相等"
#                 # b_line_eqaul.conditions.append(info3)
#                 # b_line_eqaul.conditions.append(info1)
#                 b_line_eqaul.conditions.append(["平行四边形对边有中点，被两个中点分割出的四条边相等", info3, info1, info2])
#                 equalLineList.append(b_line_eqaul)
#                 b1 = True
#             if b_line_parallogra.IsInList(parallelLineList) is False:
#                 # b_line_parallogra.source = "平行四边形对边有中点，被两个中点分割出的四条边平行"
#                 # b_line_parallogra.conditions.append(info3)
#                 # b_line_parallogra.conditions.append(info1)
#                 b_line_parallogra.conditions.append(["平行四边形对边有中点，被两个中点分割出的四条边平行", info3, info1, info2])
#                 parallelLineList.append(b_line_parallogra)
#                 b2 = True
#             b = b1 or b2
#         elif (set3 == set5 and set4 == set6):
#             c_line_parallogra = Informations.Parallel(info3.p2, info1.p1, info3.p4, info2.p1)
#             c_line_eqaul = Informations.EqualLine(info3.p2, info1.p1, info3.p4, info2.p1)
#             # print("mymain检查点811165165146516516")
#             if c_line_eqaul.IsInList(equalLineList) is False:
#                 # c_line_eqaul.source = "平行四边形对边有中点，被两个中点分割出的四条边相等"
#                 # c_line_eqaul.conditions.append(info3)
#                 # c_line_eqaul.conditions.append(info1)
#                 c_line_eqaul.conditions.append(["平行四边形对边有中点，被两个中点分割出的四条边相等", info3, info1, info2])
#                 equalLineList.append(c_line_eqaul)
#                 c1 = True
#             if c_line_parallogra.IsInList(parallelLineList) is False:
#                 # c_line_parallogra.source = "平行四边形对边有中点，被两个中点分割出的四条边平行"
#                 # c_line_parallogra.conditions.append(info3)
#                 # c_line_parallogra.conditions.append(info1)
#                 c_line_parallogra.conditions.append(["平行四边形对边有中点，被两个中点分割出的四条边平行", info3, info1, info2])
#                 parallelLineList.append(c_line_parallogra)
#                 c2 = True
#             c = c1 or c2
#         elif (set3 == set6 and set4 == set5):
#             d_line_parallogra = Informations.Parallel(info3.p2, info2.p1, info3.p4, info1.p1)
#             d_line_eqaul = Informations.EqualLine(info3.p2, info2.p1, info3.p4, info1.p1)
#             # print("mymain检查点811")
#             # d_line_eqaul.Print()
#             # for i in equalLineList:
#             #     i.Print()
#
#             if d_line_eqaul.IsInList(equalLineList) is False:
#                 # print("mymain检查点812")
#                 # d_line_eqaul.source = "平行四边形对边有中点，被两个中点分割出的四条边相等"
#                 # d_line_eqaul.conditions.append(info3)
#                 # d_line_eqaul.conditions.append(info1)
#                 d_line_eqaul.conditions.append(["平行四边形对边有中点，被两个中点分割出的四条边相等", info3, info1, info2])
#                 equalLineList.append(d_line_eqaul)
#                 d1 = True
#             if d_line_parallogra.IsInList(parallelLineList) is False:
#                 # print("mymain检查点813")
#                 # d_line_parallogra.source = "平行四边形对边有中点，被两个中点分割出的四条边平行"
#                 # d_line_parallogra.conditions.append(info3)
#                 # d_line_parallogra.conditions.append(info1)
#                 d_line_parallogra.conditions.append(["平行四边形对边有中点，被两个中点分割出的四条边平行", info3, info1, info2])
#                 parallelLineList.append(d_line_parallogra)
#                 d2 = True
#             d = d1 or d2
#
#         flag = a or b or c or d  # 判断是否存在新的信息
#         # print(flag)
#         return flag


# 垂直推直角
class LmVertiGetRiangle(Lemma):
    def __init__(self):
        self.name = "垂直推直角"
        self.inputNum = 2

    @staticmethod
    def Infer(info1, rightAngleList):
        flag = False
        if info1.p5 != info1.p1 and info1.p5 != info1.p2 and info1.p5 != info1.p3 and info1.p5 != info1.p4:
            newInfo1 = Informations.RightAngle(info1.p1, info1.p5, info1.p3)
            newInfo2 = Informations.RightAngle(info1.p2, info1.p5, info1.p4)
            newInfo3 = Informations.RightAngle(info1.p3, info1.p5, info1.p2)
            newInfo4 = Informations.RightAngle(info1.p4, info1.p5, info1.p1)
        elif info1.p5 == info1.p1:
            newInfo1 = Informations.RightAngle(info1.p2, info1.p5, info1.p3)
            newInfo2 = Informations.RightAngle(info1.p2, info1.p5, info1.p4)
            newInfo3 = None
            newInfo4 = None
        elif info1.p5 == info1.p2:
            newInfo1 = Informations.RightAngle(info1.p1, info1.p5, info1.p3)
            newInfo2 = Informations.RightAngle(info1.p1, info1.p5, info1.p4)
            newInfo3 = None
            newInfo4 = None
        elif info1.p5 == info1.p3:
            newInfo1 = Informations.RightAngle(info1.p4, info1.p5, info1.p1)
            newInfo2 = Informations.RightAngle(info1.p4, info1.p5, info1.p2)
            newInfo3 = None
            newInfo4 = None
        elif info1.p5 == info1.p4:
            newInfo1 = Informations.RightAngle(info1.p3, info1.p5, info1.p1)
            newInfo2 = Informations.RightAngle(info1.p3, info1.p5, info1.p2)
            newInfo3 = None
            newInfo4 = None
        else:
            newInfo1 = newInfo2 = newInfo3 = newInfo4 = None
        if newInfo1 is not None:
            # 用一个res来存IsInList返回的值
            newInfo1.conditions.append(["两线互相垂直推出直角", info1])
            res = newInfo1.IsInList(rightAngleList)
            newInfo1.weight = info1.weight + 1
            if res is False:
                rightAngleList.append(newInfo1)
                flag = True
            elif res is True:
                pass
            else:
                nums = len(rightAngleList[res].conditions)
                for item in rightAngleList[res].conditions:
                    if len(item) != len(newInfo1.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo1.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    rightAngleList[res].conditions.append(newInfo1.conditions[-1])
                rightAngleList[res].weight = min(newInfo1.weight, rightAngleList[res].weight)
        if newInfo2 is not None:
            # 用一个res来存IsInList返回的值
            newInfo2.conditions.append(["两线互相垂直推出直角", info1])
            res = newInfo2.IsInList(rightAngleList)
            newInfo2.weight = info1.weight + 1
            if res is False:
                rightAngleList.append(newInfo2)
                flag = True
            elif res is True:
                pass
            else:
                nums = len(rightAngleList[res].conditions)
                for item in rightAngleList[res].conditions:
                    if len(item) != len(newInfo2.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo2.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    rightAngleList[res].conditions.append(newInfo2.conditions[-1])
                rightAngleList[res].weight = min(newInfo2.weight, rightAngleList[res].weight)
        if newInfo3 is not None:
            # 用一个res来存IsInList返回的值
            newInfo3.conditions.append(["两线互相垂直推出直角", info1])
            res = newInfo3.IsInList(rightAngleList)
            newInfo3.weight = info1.weight + 1
            if res is False:
                rightAngleList.append(newInfo3)
                flag = True
            elif res is True:
                pass
            else:
                nums = len(rightAngleList[res].conditions)
                for item in rightAngleList[res].conditions:
                    if len(item) != len(newInfo3.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo3.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    rightAngleList[res].conditions.append(newInfo3.conditions[-1])
                rightAngleList[res].weight = min(newInfo3.weight, rightAngleList[res].weight)
        if newInfo4 is not None:
            # 用一个res来存IsInList返回的值
            newInfo4.conditions.append(["两线互相垂直推出直角", info1])
            res = newInfo4.IsInList(rightAngleList)
            newInfo4.weight = info1.weight + 1
            if res is False:
                rightAngleList.append(newInfo4)
                flag = True
            elif res is True:
                pass
            else:
                nums = len(rightAngleList[res].conditions)
                for item in rightAngleList[res].conditions:
                    if len(item) != len(newInfo4.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo4.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    rightAngleList[res].conditions.append(newInfo4.conditions[-1])
                rightAngleList[res].weight = min(newInfo4.weight, rightAngleList[res].weight)
        return flag


# 垂直推三点共线
class LmVertiGetCoLine(Lemma):
    def __init__(self):
        self.name = "垂直推三点共线"
        self.inputNum = 2

    @staticmethod
    def Infer(info1, coLineList):
        if info1.p5 == "#":
            return False
        flag = False
        if info1.p5 != info1.p1 and info1.p5 != info1.p2 and info1.p5 != info1.p3 and info1.p5 != info1.p4:
            newInfo1 = Informations.CoLine(info1.p1, info1.p5, info1.p2)
            newInfo2 = Informations.CoLine(info1.p3, info1.p5, info1.p4)
        elif info1.p5 == info1.p1:
            newInfo1 = Informations.CoLine(info1.p3, info1.p5, info1.p4)
            newInfo2 = None
        elif info1.p5 == info1.p2:
            newInfo1 = Informations.CoLine(info1.p3, info1.p5, info1.p4)
            newInfo2 = None
        elif info1.p5 == info1.p3:
            newInfo1 = Informations.CoLine(info1.p1, info1.p5, info1.p2)
            newInfo2 = None
        elif info1.p5 == info1.p4:
            newInfo1 = Informations.CoLine(info1.p1, info1.p5, info1.p2)
            newInfo2 = None
        else:
            newInfo1 = newInfo2 = None
        if newInfo1 is not None:
            # 用一个res来存IsInList返回的值
            newInfo1.conditions.append(["垂直推出三点共线", info1])
            res = newInfo1.IsInList(coLineList)
            newInfo1.weight = info1.weight + 1
            if res is False:
                coLineList.append(newInfo1)
                flag = True
            elif res is True:
                pass
            else:
                nums = len(coLineList[res].conditions)
                for item in coLineList[res].conditions:
                    if len(item) != len(newInfo1.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo1.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    coLineList[res].conditions.append(newInfo1.conditions[-1])
                coLineList[res].weight = min(newInfo1.weight, coLineList[res].weight)
        if newInfo2 is not None:
            # 用一个res来存IsInList返回的值
            newInfo2.conditions.append(["垂直推出三点共线", info1])
            res = newInfo2.IsInList(coLineList)
            newInfo2.weight = info1.weight + 1
            if res is False:
                coLineList.append(newInfo2)
                flag = True
            elif res is True:
                pass
            else:
                nums = len(coLineList[res].conditions)
                for item in coLineList[res].conditions:
                    if len(item) != len(newInfo2.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo2.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    coLineList[res].conditions.append(newInfo2.conditions[-1])
                coLineList[res].weight = min(newInfo2.weight, coLineList[res].weight)
        return flag


# 共线传递
class LmCoLineGetCoLine(Lemma):
    def __init__(self):
        self.name = "共线传递"
        self.inputNum = 2

    @staticmethod
    def Infer(info1, info2, coLineList):
        flag = False
        set1 = set()
        set2 = set()
        set1.add(info1.p1)
        set1.add(info1.p2)
        set1.add(info1.p3)
        set2.add(info2.p1)
        set2.add(info2.p2)
        set2.add(info2.p3)
        intersection = set1 & set2
        if len(intersection) == 2:
            difference_set1 = set1 - set2
            difference_list1 = list(difference_set1)
            difference_set2 = set2 - set1
            difference_list2 = list(difference_set2)
            intersection_list = list(intersection)
            newInfo1 = Informations.CoLine(difference_list1[0], difference_list2[0], intersection_list[0])
            newInfo2 = Informations.CoLine(difference_list1[0], difference_list2[0], intersection_list[1])
        else:
            newInfo1 = newInfo2 = None
        if newInfo1 is not None:
            # 用一个res来存IsInList返回的值
            newInfo1.conditions.append(["共线传递", info1, info2])
            res = newInfo1.IsInList(coLineList)
            newInfo1.weight = max(info1.weight, info2.weight) + 1
            if res is False:
                coLineList.append(newInfo1)
                flag = True
            elif res is True:
                pass
            else:
                nums = len(coLineList[res].conditions)
                for item in coLineList[res].conditions:
                    if len(item) != len(newInfo1.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo1.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    coLineList[res].conditions.append(newInfo1.conditions[-1])
                coLineList[res].weight = min(newInfo1.weight, coLineList[res].weight)
        if newInfo2 is not None:
            # 用一个res来存IsInList返回的值
            newInfo2.conditions.append(["共线传递", info1, info2])
            res = newInfo2.IsInList(coLineList)
            newInfo2.weight = max(info1.weight, info2.weight) + 1
            if res is False:
                coLineList.append(newInfo2)
                flag = True
            elif res is True:
                pass
            else:
                nums = len(coLineList[res].conditions)
                for item in coLineList[res].conditions:
                    if len(item) != len(newInfo2.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo2.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    coLineList[res].conditions.append(newInfo2.conditions[-1])
                coLineList[res].weight = min(newInfo2.weight, coLineList[res].weight)
        return flag


# 共线传递垂直
class LmCoLineGetVertical(Lemma):
    def __init__(self):
        self.name = "共线传递垂直"
        self.inputNum = 2

    @staticmethod
    def Infer(info1, verticalLineList, pointList):
        flag = False
        for i in range(len(verticalLineList)):
            flag = False
            set1 = set()
            set2 = set()
            set3 = set()
            set1.add(info1.p1)
            set1.add(info1.p2)
            set2.add(info1.p1)
            set2.add(info1.p3)
            set3.add(info1.p2)
            set3.add(info1.p3)
            set4 = set()
            set5 = set()
            set4.add(verticalLineList[i].p1)
            set4.add(verticalLineList[i].p2)
            set5.add(verticalLineList[i].p3)
            set5.add(verticalLineList[i].p4)
            if set1 == set4:
                newInfo1 = Informations.VerticalLine(info1.p1, info1.p3, verticalLineList[i].p3, verticalLineList[i].p4, pointList,
                                                     verticalLineList[i].p5)
                newInfo2 = Informations.VerticalLine(info1.p2, info1.p3, verticalLineList[i].p3, verticalLineList[i].p4, pointList,
                                                     verticalLineList[i].p5)
            elif set1 == set5:
                newInfo1 = Informations.VerticalLine(info1.p1, info1.p3, verticalLineList[i].p1, verticalLineList[i].p2, pointList,
                                                     verticalLineList[i].p5)
                newInfo2 = Informations.VerticalLine(info1.p2, info1.p3, verticalLineList[i].p1, verticalLineList[i].p2, pointList,
                                                     verticalLineList[i].p5)

            elif set2 == set4:
                newInfo1 = Informations.VerticalLine(info1.p1, info1.p2, verticalLineList[i].p3, verticalLineList[i].p4, pointList,
                                                     verticalLineList[i].p5)
                newInfo2 = Informations.VerticalLine(info1.p2, info1.p3, verticalLineList[i].p3, verticalLineList[i].p4, pointList,
                                                     verticalLineList[i].p5)
            elif set2 == set5:
                newInfo1 = Informations.VerticalLine(info1.p1, info1.p2, verticalLineList[i].p1, verticalLineList[i].p2, pointList,
                                                     verticalLineList[i].p5)
                newInfo2 = Informations.VerticalLine(info1.p2, info1.p3, verticalLineList[i].p1, verticalLineList[i].p2, pointList,
                                                     verticalLineList[i].p5)
            elif set3 == set4:
                newInfo1 = Informations.VerticalLine(info1.p1, info1.p3, verticalLineList[i].p3, verticalLineList[i].p4, pointList,
                                                     verticalLineList[i].p5)
                newInfo2 = Informations.VerticalLine(info1.p2, info1.p1, verticalLineList[i].p3, verticalLineList[i].p4, pointList,
                                                     verticalLineList[i].p5)
            elif set3 == set5:
                newInfo1 = Informations.VerticalLine(info1.p1, info1.p3, verticalLineList[i].p1, verticalLineList[i].p2, pointList,
                                                     verticalLineList[i].p5)
                newInfo2 = Informations.VerticalLine(info1.p2, info1.p1, verticalLineList[i].p1, verticalLineList[i].p2, pointList,
                                                     verticalLineList[i].p5)
            else:
                newInfo1 = None
                newInfo2 = None
            if newInfo1 is not None:
                # 用一个res来存IsInList返回的值
                newInfo1.conditions.append(["共线传递垂直", info1, verticalLineList[i]])
                res = newInfo1.IsInList(verticalLineList)
                newInfo1.weight = max(info1.weight, verticalLineList[i].weight) + 1
                if res is False:
                    verticalLineList.append(newInfo1)
                    flag = True
                elif res is True:
                    pass
                else:
                    nums = len(verticalLineList[res].conditions)
                    for item in verticalLineList[res].conditions:
                        if len(item) != len(newInfo1.conditions[-1]):
                            nums -= 1
                            continue
                        else:
                            for list_no in range(len(item)):
                                if item[list_no] != newInfo1.conditions[-1][list_no]:
                                    nums -= 1
                                    break
                    if nums == 0:
                        verticalLineList[res].conditions.append(newInfo1.conditions[-1])
                    verticalLineList[res].weight = min(newInfo1.weight, verticalLineList[res].weight)
            if newInfo2 is not None:
                # 用一个res来存IsInList返回的值
                newInfo2.conditions.append(["共线传递垂直", info1, verticalLineList[i]])
                res = newInfo2.IsInList(verticalLineList)
                newInfo2.weight = max(info1.weight, verticalLineList[i].weight) + 1
                if res is False:
                    verticalLineList.append(newInfo2)
                    flag = True
                elif res is True:
                    pass
                else:
                    nums = len(verticalLineList[res].conditions)
                    for item in verticalLineList[res].conditions:
                        if len(item) != len(newInfo2.conditions[-1]):
                            nums -= 1
                            continue
                        else:
                            for list_no in range(len(item)):
                                if item[list_no] != newInfo2.conditions[-1][list_no]:
                                    nums -= 1
                                    break
                    if nums == 0:
                        verticalLineList[res].conditions.append(newInfo2.conditions[-1])
                    verticalLineList[res].weight = min(newInfo2.weight, verticalLineList[res].weight)
        return flag


# 共线传递平行
class LmCoLineGetParallel(Lemma):
    def __init__(self):
        self.name = "共线传递平行"
        self.inputNum = 2

    @staticmethod
    def Infer(info1, parallelLineList):
        flag = False
        for i in range(len(parallelLineList)):
            flag = False
            set1 = set()
            set2 = set()
            set3 = set()
            set1.add(info1.p1)
            set1.add(info1.p2)
            set2.add(info1.p1)
            set2.add(info1.p3)
            set3.add(info1.p2)
            set3.add(info1.p3)
            set4 = set()
            set5 = set()
            set4.add(parallelLineList[i].p1)
            set4.add(parallelLineList[i].p2)
            set5.add(parallelLineList[i].p3)
            set5.add(parallelLineList[i].p4)
            if set1 == set4:
                newInfo1 = Informations.Parallel(info1.p1, info1.p3, parallelLineList[i].p3, parallelLineList[i].p4)
                newInfo2 = Informations.Parallel(info1.p2, info1.p3, parallelLineList[i].p3, parallelLineList[i].p4)
            elif set1 == set5:
                newInfo1 = Informations.Parallel(info1.p1, info1.p3, parallelLineList[i].p1, parallelLineList[i].p2)
                newInfo2 = Informations.Parallel(info1.p2, info1.p3, parallelLineList[i].p1, parallelLineList[i].p2)
            elif set2 == set4:
                newInfo1 = Informations.Parallel(info1.p1, info1.p2, parallelLineList[i].p3, parallelLineList[i].p4)
                newInfo2 = Informations.Parallel(info1.p2, info1.p3, parallelLineList[i].p3, parallelLineList[i].p4)
            elif set2 == set5:
                newInfo1 = Informations.Parallel(info1.p1, info1.p2, parallelLineList[i].p1, parallelLineList[i].p2)
                newInfo2 = Informations.Parallel(info1.p2, info1.p3, parallelLineList[i].p1, parallelLineList[i].p2)
            elif set3 == set4:
                newInfo1 = Informations.Parallel(info1.p1, info1.p2, parallelLineList[i].p3, parallelLineList[i].p4)
                newInfo2 = Informations.Parallel(info1.p1, info1.p3, parallelLineList[i].p3, parallelLineList[i].p4)
            elif set3 == set5:
                newInfo1 = Informations.Parallel(info1.p1, info1.p2, parallelLineList[i].p1, parallelLineList[i].p2)
                newInfo2 = Informations.Parallel(info1.p1, info1.p3, parallelLineList[i].p1, parallelLineList[i].p2)
            else:
                newInfo1 = None
                newInfo2 = None
            if newInfo1 is not None:
                # 用一个res来存IsInList返回的值
                newInfo1.conditions.append(["共线传递平行", info1, parallelLineList[i]])
                res = newInfo1.IsInList(parallelLineList)
                newInfo1.weight = max(info1.weight, parallelLineList[i].weight) + 1
                if res is False:
                    parallelLineList.append(newInfo1)
                    flag = True
                elif res is True:
                    pass
                else:
                    nums = len(parallelLineList[res].conditions)
                    for item in parallelLineList[res].conditions:
                        if len(item) != len(newInfo1.conditions[-1]):
                            nums -= 1
                            continue
                        else:
                            for list_no in range(len(item)):
                                if item[list_no] != newInfo1.conditions[-1][list_no]:
                                    nums -= 1
                                    break
                    if nums == 0:
                        parallelLineList[res].conditions.append(newInfo1.conditions[-1])
                    parallelLineList[res].weight = min(newInfo1.weight, parallelLineList[res].weight)
            if newInfo2 is not None:
                # 用一个res来存IsInList返回的值
                newInfo2.conditions.append(["共线传递平行", info1, parallelLineList[i]])
                res = newInfo2.IsInList(parallelLineList)
                newInfo2.weight = max(info1.weight, parallelLineList[i].weight) + 1
                if res is False:
                    parallelLineList.append(newInfo2)
                    flag = True
                elif res is True:
                    pass
                else:
                    nums = len(parallelLineList[res].conditions)
                    for item in parallelLineList[res].conditions:
                        if len(item) != len(newInfo2.conditions[-1]):
                            nums -= 1
                            continue
                        else:
                            for list_no in range(len(item)):
                                if item[list_no] != newInfo2.conditions[-1][list_no]:
                                    nums -= 1
                                    break
                    if nums == 0:
                        parallelLineList[res].conditions.append(newInfo2.conditions[-1])
                    parallelLineList[res].weight = min(newInfo2.weight, parallelLineList[res].weight)
        return flag


# 共线传递相等角
class LmCoLineGetAngle(Lemma):
    def __init__(self):
        self.name = "共线传递相等角"
        self.inputNum = 2

    @staticmethod
    def Infer(info1, equalAngleList, complementaryAngleList, coLineList):
        flag = False
        newInfo1_CAngle = newInfo2_CAngle = newInfo3_CAngle = newInfo4_CAngle = newInfo1 = newInfo2 = newInfo3 = newInfo4 = newInfo5 = newInfo6 = None
        for i in range(len(equalAngleList)):
            flag = False
            # set123分别是共线的三条线段
            set1 = set()
            set2 = set()
            set3 = set()
            # set1和2是一个中间点和一个边点构成的线段
            set1.add(info1.p1)
            set1.add(info1.p2)
            set2.add(info1.p1)
            set2.add(info1.p3)
            # set3是两个边点构成的线段
            set3.add(info1.p2)
            set3.add(info1.p3)
            # set4567分别是两对相等角的四条边
            set4 = set()
            set5 = set()
            set6 = set()
            set7 = set()
            set4.add(equalAngleList[i].p1)
            set4.add(equalAngleList[i].p2)
            set5.add(equalAngleList[i].p2)
            set5.add(equalAngleList[i].p3)
            set6.add(equalAngleList[i].p4)
            set6.add(equalAngleList[i].p5)
            set7.add(equalAngleList[i].p5)
            set7.add(equalAngleList[i].p6)
            # set1
            if set1 == set4:
                if info1.p1 != equalAngleList[i].p2:
                    newInfo1 = Informations.EqualAngle(equalAngleList[i].p3, equalAngleList[i].p2, info1.p3,
                                                       equalAngleList[i].p1, equalAngleList[i].p2, equalAngleList[i].p3)
                else:
                    newInfo1_CAngle = Informations.ComplementaryAngle(equalAngleList[i].p3, equalAngleList[i].p2,
                                                                      info1.p3,
                                                                      equalAngleList[i].p1, equalAngleList[i].p2,
                                                                      equalAngleList[i].p3)
            if set1 == set5:
                if info1.p1 != equalAngleList[i].p2:
                    newInfo1 = Informations.EqualAngle(info1.p3, equalAngleList[i].p2, equalAngleList[i].p1,
                                                       equalAngleList[i].p1, equalAngleList[i].p2, equalAngleList[i].p3)
                else:
                    newInfo1_CAngle = Informations.ComplementaryAngle(info1.p3, equalAngleList[i].p2,
                                                                      equalAngleList[i].p1,
                                                                      equalAngleList[i].p1, equalAngleList[i].p2,
                                                                      equalAngleList[i].p3)
            if set1 == set6:
                if info1.p1 != equalAngleList[i].p5:
                    newInfo2 = Informations.EqualAngle(equalAngleList[i].p4, equalAngleList[i].p5, equalAngleList[i].p6,
                                                       equalAngleList[i].p6, equalAngleList[i].p5, info1.p3)
                else:
                    newInfo2_CAngle = Informations.ComplementaryAngle(equalAngleList[i].p4, equalAngleList[i].p5,
                                                                      equalAngleList[i].p6,
                                                                      equalAngleList[i].p6, equalAngleList[i].p5,
                                                                      info1.p3)
            if set1 == set7:
                if info1.p1 != equalAngleList[i].p5:
                    newInfo2 = Informations.EqualAngle(equalAngleList[i].p4, equalAngleList[i].p5, equalAngleList[i].p6,
                                                       info1.p3, equalAngleList[i].p5, equalAngleList[i].p4)
                else:
                    newInfo2_CAngle = Informations.ComplementaryAngle(equalAngleList[i].p4, equalAngleList[i].p5,
                                                                      equalAngleList[i].p6,
                                                                      info1.p3, equalAngleList[i].p5,
                                                                      equalAngleList[i].p4)

            # set2
            if set2 == set4:
                if info1.p1 != equalAngleList[i].p2:
                    newInfo3 = Informations.EqualAngle(equalAngleList[i].p3, equalAngleList[i].p2, info1.p2,
                                                       equalAngleList[i].p1, equalAngleList[i].p2, equalAngleList[i].p3)
                else:
                    newInfo3_CAngle = Informations.ComplementaryAngle(equalAngleList[i].p3, equalAngleList[i].p2,
                                                                      info1.p2,
                                                                      equalAngleList[i].p1, equalAngleList[i].p2,
                                                                      equalAngleList[i].p3)
            if set2 == set5:
                if info1.p1 != equalAngleList[i].p2:
                    newInfo3 = Informations.EqualAngle(info1.p2, equalAngleList[i].p2, equalAngleList[i].p1,
                                                       equalAngleList[i].p1, equalAngleList[i].p2, equalAngleList[i].p3)
                else:
                    newInfo3_CAngle = Informations.ComplementaryAngle(info1.p2, equalAngleList[i].p2,
                                                                      equalAngleList[i].p1,
                                                                      equalAngleList[i].p1, equalAngleList[i].p2,
                                                                      equalAngleList[i].p3)
            if set2 == set6:
                if info1.p1 != equalAngleList[i].p5:
                    newInfo4 = Informations.EqualAngle(equalAngleList[i].p4, equalAngleList[i].p5, equalAngleList[i].p6,
                                                       equalAngleList[i].p6, equalAngleList[i].p5, info1.p2)
                else:
                    newInfo4_CAngle = Informations.ComplementaryAngle(equalAngleList[i].p4, equalAngleList[i].p5,
                                                                      equalAngleList[i].p6,
                                                                      equalAngleList[i].p6, equalAngleList[i].p5,
                                                                      info1.p2)
            if set2 == set7:
                if info1.p1 != equalAngleList[i].p5:
                    newInfo4 = Informations.EqualAngle(equalAngleList[i].p4, equalAngleList[i].p5, equalAngleList[i].p6,
                                                       info1.p2, equalAngleList[i].p5, equalAngleList[i].p4)
                else:
                    newInfo4_CAngle = Informations.ComplementaryAngle(equalAngleList[i].p4, equalAngleList[i].p5,
                                                                      equalAngleList[i].p6,
                                                                      info1.p2, equalAngleList[i].p5,
                                                                      equalAngleList[i].p4)
            # set3
            if set3 == set4:
                newInfo5 = Informations.EqualAngle(equalAngleList[i].p3, equalAngleList[i].p2, info1.p1,
                                                   equalAngleList[i].p1, equalAngleList[i].p2, equalAngleList[i].p3)
            if set3 == set5:
                newInfo5 = Informations.EqualAngle(info1.p1, equalAngleList[i].p2, equalAngleList[i].p1,
                                                   equalAngleList[i].p1, equalAngleList[i].p2, equalAngleList[i].p3)
            if set3 == set6:
                newInfo6 = Informations.EqualAngle(equalAngleList[i].p4, equalAngleList[i].p5, equalAngleList[i].p6,
                                                   equalAngleList[i].p6, equalAngleList[i].p5, info1.p1)
            if set3 == set7:
                newInfo6 = Informations.EqualAngle(equalAngleList[i].p4, equalAngleList[i].p5, equalAngleList[i].p6,
                                                   info1.p1, equalAngleList[i].p5, equalAngleList[i].p4)
            if newInfo1 is not None:
                # 用一个res来存IsInList返回的值
                newInfo1.conditions.append(["共线传递相等角", info1, equalAngleList[i]])
                res = newInfo1.IsInList(equalAngleList, coLineList)
                newInfo1.weight = max(info1.weight, equalAngleList[i].weight) + 1
                newInfo1.source = "已知"
                if res is False:
                    equalAngleList.append(newInfo1)
                    flag = True
                elif res is True:
                    pass
                else:
                    nums = len(equalAngleList[res].conditions)
                    for item in equalAngleList[res].conditions:
                        if len(item) != len(newInfo1.conditions[-1]):
                            nums -= 1
                            continue
                        else:
                            for list_no in range(len(item)):
                                if item[list_no] != newInfo1.conditions[-1][list_no]:
                                    nums -= 1
                                    break
                    if nums == 0:
                        equalAngleList[res].conditions.append(newInfo1.conditions[-1])
                    equalAngleList[res].weight = min(newInfo1.weight, equalAngleList[res].weight)
            if newInfo1_CAngle is not None:
                # 用一个res来存IsInList返回的值
                newInfo1_CAngle.conditions.append(["共线传递互补角", info1, equalAngleList[i]])
                res = newInfo1_CAngle.IsInList(complementaryAngleList, coLineList)
                newInfo1_CAngle.weight = max(info1.weight, equalAngleList[i].weight) + 1
                newInfo1_CAngle.source = "已知"
                if res is False:
                    complementaryAngleList.append(newInfo1_CAngle)
                    flag = True
                elif res is True:
                    pass
                else:
                    nums = len(complementaryAngleList[res].conditions)
                    for item in complementaryAngleList[res].conditions:
                        if len(item) != len(newInfo1_CAngle.conditions[-1]):
                            nums -= 1
                            continue
                        else:
                            for list_no in range(len(item)):
                                if item[list_no] != newInfo1_CAngle.conditions[-1][list_no]:
                                    nums -= 1
                                    break
                    if nums == 0:
                        complementaryAngleList[res].conditions.append(newInfo1_CAngle.conditions[-1])
                    complementaryAngleList[res].weight = min(newInfo1_CAngle.weight, complementaryAngleList[res].weight)
            if newInfo2 is not None:
                # 用一个res来存IsInList返回的值
                newInfo2.conditions.append(["共线传递相等角", info1, equalAngleList[i]])
                res = newInfo2.IsInList(equalAngleList, coLineList)
                newInfo2.weight = max(info1.weight, equalAngleList[i].weight) + 1
                newInfo2.source = "已知"
                if res is False:
                    equalAngleList.append(newInfo2)
                    flag = True
                elif res is True:
                    pass
                else:
                    nums = len(equalAngleList[res].conditions)
                    for item in equalAngleList[res].conditions:
                        if len(item) != len(newInfo2.conditions[-1]):
                            nums -= 1
                            continue
                        else:
                            for list_no in range(len(item)):
                                if item[list_no] != newInfo2.conditions[-1][list_no]:
                                    nums -= 1
                                    break
                    if nums == 0:
                        equalAngleList[res].conditions.append(newInfo2.conditions[-1])
                    equalAngleList[res].weight = min(newInfo2.weight, equalAngleList[res].weight)
            if newInfo2_CAngle is not None:
                # 用一个res来存IsInList返回的值
                newInfo2_CAngle.conditions.append(["共线传递互补角", info1, equalAngleList[i]])
                res = newInfo2_CAngle.IsInList(complementaryAngleList, coLineList)
                newInfo2_CAngle.weight = max(info1.weight, equalAngleList[i].weight) + 1
                newInfo2_CAngle.source = "已知"
                if res is False:
                    complementaryAngleList.append(newInfo2_CAngle)
                    flag = True
                elif res is True:
                    pass
                else:
                    nums = len(complementaryAngleList[res].conditions)
                    for item in complementaryAngleList[res].conditions:
                        if len(item) != len(newInfo2_CAngle.conditions[-1]):
                            nums -= 1
                            continue
                        else:
                            for list_no in range(len(item)):
                                if item[list_no] != newInfo2_CAngle.conditions[-1][list_no]:
                                    nums -= 1
                                    break
                    if nums == 0:
                        complementaryAngleList[res].conditions.append(newInfo2_CAngle.conditions[-1])
                    complementaryAngleList[res].weight = min(newInfo2_CAngle.weight, complementaryAngleList[res].weight)
            if newInfo3 is not None:
                # 用一个res来存IsInList返回的值
                newInfo3.conditions.append(["共线传递相等角", info1, equalAngleList[i]])
                res = newInfo3.IsInList(equalAngleList, coLineList)
                newInfo3.weight = max(info1.weight, equalAngleList[i].weight) + 1
                newInfo3.source = "已知"
                if res is False:
                    equalAngleList.append(newInfo3)
                    flag = True
                elif res is True:
                    pass
                else:
                    nums = len(equalAngleList[res].conditions)
                    for item in equalAngleList[res].conditions:
                        if len(item) != len(newInfo3.conditions[-1]):
                            nums -= 1
                            continue
                        else:
                            for list_no in range(len(item)):
                                if item[list_no] != newInfo3.conditions[-1][list_no]:
                                    nums -= 1
                                    break
                    if nums == 0:
                        equalAngleList[res].conditions.append(newInfo3.conditions[-1])
                    equalAngleList[res].weight = min(newInfo3.weight, equalAngleList[res].weight)
            if newInfo3_CAngle is not None:
                # 用一个res来存IsInList返回的值
                newInfo3_CAngle.conditions.append(["共线传递互补角", info1, equalAngleList[i]])
                res = newInfo3_CAngle.IsInList(complementaryAngleList, coLineList)
                newInfo3_CAngle.weight = max(info1.weight, equalAngleList[i].weight) + 1
                newInfo3_CAngle.source = "已知"
                if res is False:
                    complementaryAngleList.append(newInfo3_CAngle)
                    flag = True
                elif res is True:
                    pass
                else:
                    nums = len(complementaryAngleList[res].conditions)
                    for item in complementaryAngleList[res].conditions:
                        if len(item) != len(newInfo3_CAngle.conditions[-1]):
                            nums -= 1
                            continue
                        else:
                            for list_no in range(len(item)):
                                if item[list_no] != newInfo3_CAngle.conditions[-1][list_no]:
                                    nums -= 1
                                    break
                    if nums == 0:
                        complementaryAngleList[res].conditions.append(newInfo3_CAngle.conditions[-1])
                    complementaryAngleList[res].weight = min(newInfo3_CAngle.weight, complementaryAngleList[res].weight)
            if newInfo4 is not None:
                # 用一个res来存IsInList返回的值
                newInfo4.conditions.append(["共线传递相等角", info1, equalAngleList[i]])
                res = newInfo4.IsInList(equalAngleList, coLineList)
                newInfo4.weight = max(info1.weight, equalAngleList[i].weight) + 1
                newInfo4.source = "已知"
                if res is False:
                    equalAngleList.append(newInfo4)
                    flag = True
                elif res is True:
                    pass
                else:
                    nums = len(equalAngleList[res].conditions)
                    for item in equalAngleList[res].conditions:
                        if len(item) != len(newInfo4.conditions[-1]):
                            nums -= 1
                            continue
                        else:
                            for list_no in range(len(item)):
                                if item[list_no] != newInfo4.conditions[-1][list_no]:
                                    nums -= 1
                                    break
                    if nums == 0:
                        equalAngleList[res].conditions.append(newInfo4.conditions[-1])
                    equalAngleList[res].weight = min(newInfo4.weight, equalAngleList[res].weight)
            if newInfo4_CAngle is not None:
                # 用一个res来存IsInList返回的值
                newInfo4_CAngle.conditions.append(["共线传递互补角", info1, equalAngleList[i]])
                res = newInfo4_CAngle.IsInList(complementaryAngleList, coLineList)
                newInfo4_CAngle.weight = max(info1.weight, equalAngleList[i].weight) + 1
                newInfo4_CAngle.source = "已知"
                if res is False:
                    complementaryAngleList.append(newInfo4_CAngle)
                    flag = True
                elif res is True:
                    pass
                else:
                    nums = len(complementaryAngleList[res].conditions)
                    for item in complementaryAngleList[res].conditions:
                        if len(item) != len(newInfo4_CAngle.conditions[-1]):
                            nums -= 1
                            continue
                        else:
                            for list_no in range(len(item)):
                                if item[list_no] != newInfo4_CAngle.conditions[-1][list_no]:
                                    nums -= 1
                                    break
                    if nums == 0:
                        complementaryAngleList[res].conditions.append(newInfo4_CAngle.conditions[-1])
                    complementaryAngleList[res].weight = min(newInfo4_CAngle.weight, complementaryAngleList[res].weight)
            if newInfo5 is not None:
                # 用一个res来存IsInList返回的值
                newInfo5.conditions.append(["共线传递相等角", info1, equalAngleList[i]])
                res = newInfo5.IsInList(equalAngleList, coLineList)
                newInfo5.weight = max(info1.weight, equalAngleList[i].weight) + 1
                newInfo5.source = "已知"
                if res is False:
                    equalAngleList.append(newInfo5)
                    flag = True
                elif res is True:
                    pass
                else:
                    nums = len(equalAngleList[res].conditions)
                    for item in equalAngleList[res].conditions:
                        if len(item) != len(newInfo5.conditions[-1]):
                            nums -= 1
                            continue
                        else:
                            for list_no in range(len(item)):
                                if item[list_no] != newInfo5.conditions[-1][list_no]:
                                    nums -= 1
                                    break
                    if nums == 0:
                        equalAngleList[res].conditions.append(newInfo5.conditions[-1])
                    equalAngleList[res].weight = min(newInfo5.weight, equalAngleList[res].weight)
            if newInfo6 is not None:
                # 用一个res来存IsInList返回的值
                newInfo6.conditions.append(["共线传递相等角", info1, equalAngleList[i]])
                res = newInfo6.IsInList(equalAngleList, coLineList)
                newInfo6.weight = max(info1.weight, equalAngleList[i].weight) + 1
                newInfo6.source = "已知"
                if res is False:
                    equalAngleList.append(newInfo6)
                    flag = True
                elif res is True:
                    pass
                else:
                    nums = len(equalAngleList[res].conditions)
                    for item in equalAngleList[res].conditions:
                        if len(item) != len(newInfo6.conditions[-1]):
                            nums -= 1
                            continue
                        else:
                            for list_no in range(len(item)):
                                if item[list_no] != newInfo6.conditions[-1][list_no]:
                                    nums -= 1
                                    break
                    if nums == 0:
                        equalAngleList[res].conditions.append(newInfo6.conditions[-1])
                    equalAngleList[res].weight = min(newInfo6.weight, equalAngleList[res].weight)

        return flag


# 两直线相交产生互补角、对顶角1
class LmCoLineGetComplementaryAngle_1(Lemma):
    def __init__(self):
        self.name = "两直线相交产生互补角、对顶角1"
        self.inputNum = 5

    @staticmethod
    def Infer(info1, info2, complementaryAngleList, equalAngleList, coLineList):
        flag1 = flag2 = flag3 = flag4 = flag5 = flag6 = False
        newInfo1 = newInfo2 = newInfo3 = newInfo4 = newInfo5 = newInfo6 = None
        newInfo1 = Informations.ComplementaryAngle(info1.p2, info1.p1, info2.p2, info1.p2, info1.p1, info2.p3)
        newInfo2 = Informations.ComplementaryAngle(info1.p3, info1.p1, info2.p2, info1.p3, info1.p1, info2.p3)
        newInfo3 = Informations.ComplementaryAngle(info2.p2, info1.p1, info1.p2, info2.p2, info1.p1, info1.p3)
        newInfo4 = Informations.ComplementaryAngle(info2.p3, info1.p1, info1.p2, info2.p3, info1.p1, info1.p3)
        newInfo5 = Informations.EqualAngle(info1.p2, info1.p1, info2.p2, info1.p3, info1.p1, info2.p3)
        newInfo6 = Informations.EqualAngle(info1.p3, info1.p1, info2.p2, info1.p2, info1.p1, info2.p3)
        newInfo1.source = "已知"
        newInfo2.source = "已知"
        newInfo3.source = "已知"
        newInfo4.source = "已知"
        newInfo5.source = "已知"
        newInfo6.source = "已知"
        if newInfo1 is not None:
            # 用一个res来存IsInList返回的值
            newInfo1.conditions.append(["两直线相交产生互补角", info1, info2])
            res = newInfo1.IsInList(complementaryAngleList, coLineList)
            newInfo1.weight = max(info1.weight, info2.weight) + 1
            if res is False:
                complementaryAngleList.append(newInfo1)
                flag1 = True
            elif res is True:
                pass
            else:
                nums = len(complementaryAngleList[res].conditions)
                for item in complementaryAngleList[res].conditions:
                    if len(item) != len(newInfo1.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo1.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    complementaryAngleList[res].conditions.append(newInfo1.conditions[-1])
                complementaryAngleList[res].weight = min(newInfo1.weight, complementaryAngleList[res].weight)
        if newInfo2 is not None:
            # 用一个res来存IsInList返回的值
            newInfo2.conditions.append(["两直线相交产生互补角", info1, info2])
            res = newInfo2.IsInList(complementaryAngleList, coLineList)
            newInfo2.weight = max(info1.weight, info2.weight) + 1
            if res is False:
                complementaryAngleList.append(newInfo2)
                flag2 = True
            elif res is True:
                pass
            else:
                nums = len(complementaryAngleList[res].conditions)
                for item in complementaryAngleList[res].conditions:
                    if len(item) != len(newInfo2.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo2.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    complementaryAngleList[res].conditions.append(newInfo2.conditions[-1])
                complementaryAngleList[res].weight = min(newInfo2.weight, complementaryAngleList[res].weight)
        if newInfo3 is not None:
            # 用一个res来存IsInList返回的值
            newInfo3.conditions.append(["两直线相交产生互补角", info1, info2])
            res = newInfo3.IsInList(complementaryAngleList, coLineList)
            newInfo3.weight = max(info1.weight, info2.weight) + 1
            if res is False:
                complementaryAngleList.append(newInfo3)
                flag3 = True
            elif res is True:
                pass
            else:
                nums = len(complementaryAngleList[res].conditions)
                for item in complementaryAngleList[res].conditions:
                    if len(item) != len(newInfo3.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo3.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    complementaryAngleList[res].conditions.append(newInfo3.conditions[-1])
                complementaryAngleList[res].weight = min(newInfo3.weight, complementaryAngleList[res].weight)
        if newInfo4 is not None:
            # 用一个res来存IsInList返回的值
            newInfo4.conditions.append(["两直线相交产生互补角", info1, info2])
            res = newInfo4.IsInList(complementaryAngleList, coLineList)
            newInfo4.weight = max(info1.weight, info2.weight) + 1
            if res is False:
                complementaryAngleList.append(newInfo4)
                flag4 = True
            elif res is True:
                pass
            else:
                nums = len(complementaryAngleList[res].conditions)
                for item in complementaryAngleList[res].conditions:
                    if len(item) != len(newInfo4.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo4.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    complementaryAngleList[res].conditions.append(newInfo4.conditions[-1])
                complementaryAngleList[res].weight = min(newInfo4.weight, complementaryAngleList[res].weight)
        if newInfo5 is not None:
            # 用一个res来存IsInList返回的值
            newInfo5.conditions.append(["对顶角相等", info1, info2])
            res = newInfo5.IsInList(equalAngleList, coLineList)
            newInfo5.weight = max(info1.weight, info2.weight) + 1
            if res is False:
                equalAngleList.append(newInfo5)
                flag5 = True
            elif res is True:
                pass
            else:
                nums = len(equalAngleList[res].conditions)
                for item in equalAngleList[res].conditions:
                    if len(item) != len(newInfo5.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo5.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalAngleList[res].conditions.append(newInfo5.conditions[-1])
                equalAngleList[res].weight = min(newInfo5.weight, equalAngleList[res].weight)
        if newInfo6 is not None:
            # 用一个res来存IsInList返回的值
            newInfo6.conditions.append(["对顶角相等", info1, info2])
            res = newInfo6.IsInList(equalAngleList, coLineList)
            newInfo6.weight = max(info1.weight, info2.weight) + 1
            if res is False:
                equalAngleList.append(newInfo6)
                flag6 = True
            elif res is True:
                pass
            else:
                nums = len(equalAngleList[res].conditions)
                for item in equalAngleList[res].conditions:
                    if len(item) != len(newInfo6.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo6.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalAngleList[res].conditions.append(newInfo6.conditions[-1])
                equalAngleList[res].weight = min(newInfo6.weight, equalAngleList[res].weight)

        flag = flag1 or flag2 or flag3 or flag4 or flag5 or flag6
        return flag


# 两直线相交产生互补角、对顶角2
class LmCoLineGetComplementaryAngle_2(Lemma):
    def __init__(self):
        self.name = "两直线相交产生互补角、对顶角2"
        self.inputNum = 5

    @staticmethod
    def Infer(info1, info2, complementaryAngleList, equalAngleList, coLineList):
        flag1 = flag2 = flag3 = flag4 = flag5 = flag6 = False
        newInfo1 = newInfo2 = newInfo3 = newInfo4 = newInfo5 = newInfo6 = None
        if info1.p1 == info2.p2:
            newInfo1 = Informations.ComplementaryAngle(info2.p1, info2.p2, info1.p2, info2.p1, info2.p2, info1.p3)
            newInfo2 = Informations.ComplementaryAngle(info2.p1, info2.p2, info1.p2, info2.p3, info2.p2, info1.p3)
            newInfo3 = Informations.ComplementaryAngle(info2.p3, info2.p2, info1.p2, info2.p1, info2.p2, info1.p3)
            newInfo4 = Informations.ComplementaryAngle(info2.p3, info2.p2, info1.p2, info2.p3, info2.p2, info1.p3)

            newInfo5 = Informations.EqualAngle(info1.p2, info2.p2, info2.p1, info1.p2, info2.p2, info2.p3)
            newInfo6 = Informations.EqualAngle(info1.p3, info2.p2, info2.p1, info1.p3, info2.p2, info2.p3)

        elif info1.p1 == info2.p3:
            newInfo1 = Informations.ComplementaryAngle(info2.p1, info1.p1, info1.p2, info2.p1, info1.p1, info1.p3)
            newInfo2 = Informations.ComplementaryAngle(info2.p1, info1.p1, info1.p2, info2.p2, info1.p1, info1.p3)
            newInfo3 = Informations.ComplementaryAngle(info2.p2, info1.p1, info1.p2, info2.p1, info1.p1, info1.p3)
            newInfo4 = Informations.ComplementaryAngle(info2.p2, info1.p1, info1.p2, info2.p2, info1.p1, info1.p3)

            newInfo5 = Informations.EqualAngle(info1.p2, info1.p1, info2.p1, info1.p2, info1.p1, info2.p2)
            newInfo6 = Informations.EqualAngle(info1.p3, info1.p1, info2.p1, info1.p3, info1.p1, info2.p2)

        elif info2.p1 == info1.p2:
            newInfo1 = Informations.ComplementaryAngle(info1.p1, info2.p1, info2.p2, info2.p3, info2.p1, info1.p1)
            newInfo2 = Informations.ComplementaryAngle(info1.p1, info2.p1, info2.p2, info2.p3, info2.p1, info1.p3)
            newInfo3 = Informations.ComplementaryAngle(info1.p3, info2.p1, info2.p2, info2.p3, info2.p1, info1.p1)
            newInfo4 = Informations.ComplementaryAngle(info1.p3, info2.p1, info2.p2, info2.p3, info2.p1, info1.p3)

            newInfo5 = Informations.EqualAngle(info2.p2, info2.p1, info1.p1, info2.p2, info2.p1, info1.p3)
            newInfo6 = Informations.EqualAngle(info2.p3, info2.p1, info1.p1, info2.p3, info2.p1, info1.p3)

        elif info2.p1 == info1.p3:
            newInfo1 = Informations.ComplementaryAngle(info1.p1, info2.p1, info2.p2, info2.p3, info2.p1, info1.p1)
            newInfo2 = Informations.ComplementaryAngle(info1.p1, info2.p1, info2.p2, info2.p3, info2.p1, info1.p2)
            newInfo3 = Informations.ComplementaryAngle(info1.p2, info2.p1, info2.p2, info2.p3, info2.p1, info1.p1)
            newInfo4 = Informations.ComplementaryAngle(info1.p2, info2.p1, info2.p2, info2.p3, info2.p1, info1.p2)

            newInfo5 = Informations.EqualAngle(info2.p2, info2.p1, info1.p1, info2.p2, info2.p1, info1.p2)
            newInfo6 = Informations.EqualAngle(info2.p3, info2.p1, info1.p1, info2.p3, info2.p1, info1.p2)
        newInfo1.source = "已知"
        newInfo2.source = "已知"
        newInfo3.source = "已知"
        newInfo4.source = "已知"
        newInfo5.source = "已知"
        newInfo6.source = "已知"
        if newInfo1 is not None:
            # 用一个res来存IsInList返回的值
            newInfo1.conditions.append(["两直线相交产生互补角", info1, info2])
            res = newInfo1.IsInList(complementaryAngleList, coLineList)
            newInfo1.weight = max(info1.weight, info2.weight) + 1
            if res is False:
                complementaryAngleList.append(newInfo1)
                flag1 = True
            elif res is True:
                pass
            else:
                nums = len(complementaryAngleList[res].conditions)
                for item in complementaryAngleList[res].conditions:
                    if len(item) != len(newInfo1.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo1.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    complementaryAngleList[res].conditions.append(newInfo1.conditions[-1])
                complementaryAngleList[res].weight = min(newInfo1.weight, complementaryAngleList[res].weight)
        if newInfo2 is not None:
            # 用一个res来存IsInList返回的值
            newInfo2.conditions.append(["两直线相交产生互补角", info1, info2])
            res = newInfo2.IsInList(complementaryAngleList, coLineList)
            newInfo2.weight = max(info1.weight, info2.weight) + 1
            if res is False:
                complementaryAngleList.append(newInfo2)
                flag2 = True
            elif res is True:
                pass
            else:
                nums = len(complementaryAngleList[res].conditions)
                for item in complementaryAngleList[res].conditions:
                    if len(item) != len(newInfo2.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo2.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    complementaryAngleList[res].conditions.append(newInfo2.conditions[-1])
        if newInfo3 is not None:
            # 用一个res来存IsInList返回的值
            newInfo3.conditions.append(["两直线相交产生互补角", info1, info2])
            res = newInfo3.IsInList(complementaryAngleList, coLineList)
            newInfo3.weight = max(info1.weight, info2.weight) + 1
            if res is False:
                complementaryAngleList.append(newInfo3)
                flag3 = True
            elif res is True:
                pass
            else:
                nums = len(complementaryAngleList[res].conditions)
                for item in complementaryAngleList[res].conditions:
                    if len(item) != len(newInfo3.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo3.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    complementaryAngleList[res].conditions.append(newInfo3.conditions[-1])
                complementaryAngleList[res].weight = min(newInfo3.weight, complementaryAngleList[res].weight)
        if newInfo4 is not None:
            # 用一个res来存IsInList返回的值
            newInfo4.conditions.append(["两直线相交产生互补角", info1, info2])
            res = newInfo4.IsInList(complementaryAngleList, coLineList)
            newInfo4.weight = max(info1.weight, info2.weight) + 1
            if res is False:
                complementaryAngleList.append(newInfo4)
                flag4 = True
            elif res is True:
                pass
            else:
                nums = len(complementaryAngleList[res].conditions)
                for item in complementaryAngleList[res].conditions:
                    if len(item) != len(newInfo4.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo4.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    complementaryAngleList[res].conditions.append(newInfo4.conditions[-1])
                complementaryAngleList[res].weight = min(newInfo4.weight, complementaryAngleList[res].weight)
        if newInfo5 is not None:
            # 用一个res来存IsInList返回的值
            newInfo5.conditions.append(["两直线相交产生相等角", info1, info2])
            res = newInfo5.IsInList(equalAngleList, coLineList)
            newInfo5.weight = max(info1.weight, info2.weight) + 1
            if res is False:
                equalAngleList.append(newInfo5)
                flag5 = True
            elif res is True:
                pass
            else:
                nums = len(equalAngleList[res].conditions)
                for item in equalAngleList[res].conditions:
                    if len(item) != len(newInfo5.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo5.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalAngleList[res].conditions.append(newInfo5.conditions[-1])
                equalAngleList[res].weight = min(newInfo5.weight, equalAngleList[res].weight)
        if newInfo6 is not None:
            # 用一个res来存IsInList返回的值
            newInfo6.conditions.append(["两直线相交产生相等角", info1, info2])
            res = newInfo6.IsInList(equalAngleList, coLineList)
            newInfo6.weight = max(info1.weight, info2.weight) + 1
            if res is False:
                equalAngleList.append(newInfo6)
                flag6 = True
            elif res is True:
                pass
            else:
                nums = len(equalAngleList[res].conditions)
                for item in equalAngleList[res].conditions:
                    if len(item) != len(newInfo6.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo6.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalAngleList[res].conditions.append(newInfo6.conditions[-1])
                equalAngleList[res].weight = min(newInfo6.weight, equalAngleList[res].weight)

        flag = flag1 or flag2 or flag3 or flag4 or flag5 or flag6
        return flag


# 两直线相交产生互补角、对顶角3
class LmCoLineGetComplementaryAngle_3(Lemma):
    def __init__(self):
        self.name = "两直线相交产生互补角、对顶角3"
        self.inputNum = 4

    @staticmethod
    def Infer(info1, info2, equalAngleList, coLineList):
        flag1 = flag2 = flag3 = flag4 = flag5 = flag6 = False
        newInfo1 = newInfo2 = newInfo3 = newInfo4 = newInfo5 = newInfo6 = None
        if info1.p3 == info2.p3:
            newInfo1 = Informations.EqualAngle(info1.p1, info1.p3, info2.p1, info1.p2, info1.p3, info2.p1)
            newInfo2 = Informations.EqualAngle(info1.p1, info1.p3, info2.p1, info1.p1, info1.p3, info2.p2)
            newInfo3 = Informations.EqualAngle(info1.p1, info1.p3, info2.p1, info1.p2, info1.p3, info2.p2)

            newInfo4 = Informations.EqualAngle(info1.p2, info1.p3, info2.p1, info1.p1, info1.p3, info2.p2)
            newInfo5 = Informations.EqualAngle(info1.p2, info1.p3, info2.p1, info1.p2, info1.p3, info2.p2)

            newInfo6 = Informations.EqualAngle(info1.p1, info1.p3, info2.p2, info1.p2, info1.p3, info2.p2)

        elif info1.p3 == info2.p2:
            newInfo1 = Informations.EqualAngle(info1.p1, info1.p3, info2.p1, info1.p2, info1.p3, info2.p1)
            newInfo2 = Informations.EqualAngle(info1.p1, info1.p3, info2.p1, info1.p1, info1.p3, info2.p3)
            newInfo3 = Informations.EqualAngle(info1.p1, info1.p3, info2.p1, info1.p2, info1.p3, info2.p3)

            newInfo4 = Informations.EqualAngle(info1.p2, info1.p3, info2.p1, info1.p1, info1.p3, info2.p3)
            newInfo5 = Informations.EqualAngle(info1.p2, info1.p3, info2.p1, info1.p2, info1.p3, info2.p3)

            newInfo6 = Informations.EqualAngle(info1.p1, info1.p3, info2.p3, info1.p2, info1.p3, info2.p3)

        elif info1.p2 == info2.p3:
            newInfo1 = Informations.EqualAngle(info1.p1, info1.p2, info2.p1, info1.p3, info1.p2, info2.p1)
            newInfo2 = Informations.EqualAngle(info1.p1, info1.p2, info2.p1, info1.p1, info1.p2, info2.p2)
            newInfo3 = Informations.EqualAngle(info1.p1, info1.p2, info2.p1, info1.p3, info1.p2, info2.p2)

            newInfo4 = Informations.EqualAngle(info1.p3, info1.p2, info2.p1, info1.p1, info1.p2, info2.p2)
            newInfo5 = Informations.EqualAngle(info1.p3, info1.p2, info2.p1, info1.p3, info1.p2, info2.p2)

            newInfo6 = Informations.EqualAngle(info1.p1, info1.p2, info2.p2, info1.p3, info1.p2, info2.p2)

        elif info1.p2 == info2.p2:
            newInfo1 = Informations.EqualAngle(info1.p1, info1.p2, info2.p1, info1.p3, info1.p2, info2.p1)
            newInfo2 = Informations.EqualAngle(info1.p1, info1.p2, info2.p1, info1.p1, info1.p2, info2.p3)
            newInfo3 = Informations.EqualAngle(info1.p1, info1.p2, info2.p1, info1.p3, info1.p2, info2.p3)

            newInfo4 = Informations.EqualAngle(info1.p3, info1.p2, info2.p1, info1.p1, info1.p2, info2.p3)
            newInfo5 = Informations.EqualAngle(info1.p3, info1.p2, info2.p1, info1.p3, info1.p2, info2.p3)

            newInfo6 = Informations.EqualAngle(info1.p1, info1.p2, info2.p3, info1.p3, info1.p2, info2.p3)
        newInfo1.source = "已知"
        newInfo2.source = "已知"
        newInfo3.source = "已知"
        newInfo4.source = "已知"
        newInfo5.source = "已知"
        newInfo6.source = "已知"
        if newInfo1 is not None:
            # 用一个res来存IsInList返回的值
            newInfo1.conditions.append(["对顶角相等", info1, info2])
            res = newInfo1.IsInList(equalAngleList, coLineList)
            newInfo1.weight = max(info1.weight, info2.weight) + 1
            if res is False:
                equalAngleList.append(newInfo1)
                flag1 = True
            elif res is True:
                pass
            else:
                nums = len(equalAngleList[res].conditions)
                for item in equalAngleList[res].conditions:
                    if len(item) != len(newInfo1.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo1.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalAngleList[res].conditions.append(newInfo1.conditions[-1])
                equalAngleList[res].weight = min(newInfo1.weight, equalAngleList[res].weight)
        if newInfo2 is not None:
            # 用一个res来存IsInList返回的值
            newInfo2.conditions.append(["对顶角相等", info1, info2])
            res = newInfo2.IsInList(equalAngleList, coLineList)
            newInfo2.weight = max(info1.weight, info2.weight) + 1
            if res is False:
                equalAngleList.append(newInfo2)
                flag2 = True
            elif res is True:
                pass
            else:
                nums = len(equalAngleList[res].conditions)
                for item in equalAngleList[res].conditions:
                    if len(item) != len(newInfo2.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo2.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalAngleList[res].conditions.append(newInfo2.conditions[-1])
                equalAngleList[res].weight = min(newInfo2.weight, equalAngleList[res].weight)
        if newInfo3 is not None:
            # 用一个res来存IsInList返回的值
            newInfo3.conditions.append(["对顶角相等", info1, info2])
            res = newInfo3.IsInList(equalAngleList, coLineList)
            newInfo3.weight = max(info1.weight, info2.weight) + 1
            if res is False:
                equalAngleList.append(newInfo3)
                flag3 = True
            elif res is True:
                pass
            else:
                nums = len(equalAngleList[res].conditions)
                for item in equalAngleList[res].conditions:
                    if len(item) != len(newInfo3.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo3.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalAngleList[res].conditions.append(newInfo3.conditions[-1])
                equalAngleList[res].weight = min(newInfo3.weight, equalAngleList[res].weight)
        if newInfo4 is not None:
            # 用一个res来存IsInList返回的值
            newInfo4.conditions.append(["对顶角相等", info1, info2])
            res = newInfo4.IsInList(equalAngleList, coLineList)
            newInfo4.weight = max(info1.weight, info2.weight) + 1
            if res is False:
                equalAngleList.append(newInfo4)
                flag4 = True
            elif res is True:
                pass
            else:
                nums = len(equalAngleList[res].conditions)
                for item in equalAngleList[res].conditions:
                    if len(item) != len(newInfo4.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo4.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalAngleList[res].conditions.append(newInfo4.conditions[-1])
                equalAngleList[res].weight = min(newInfo4.weight, equalAngleList[res].weight)
        if newInfo5 is not None:
            # 用一个res来存IsInList返回的值
            newInfo5.conditions.append(["对顶角相等", info1, info2])
            res = newInfo5.IsInList(equalAngleList, coLineList)
            newInfo5.weight = max(info1.weight, info2.weight) + 1
            if res is False:
                equalAngleList.append(newInfo5)
                flag5 = True
            elif res is True:
                pass
            else:
                nums = len(equalAngleList[res].conditions)
                for item in equalAngleList[res].conditions:
                    if len(item) != len(newInfo5.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo5.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalAngleList[res].conditions.append(newInfo5.conditions[-1])
                equalAngleList[res].weight = min(newInfo5.weight, equalAngleList[res].weight)
        if newInfo6 is not None:
            # 用一个res来存IsInList返回的值
            newInfo6.conditions.append(["对顶角相等", info1, info2])
            res = newInfo6.IsInList(equalAngleList, coLineList)
            newInfo6.weight = max(info1.weight, info2.weight) + 1
            if res is False:
                equalAngleList.append(newInfo6)
                flag6 = True
            elif res is True:
                pass
            else:
                nums = len(equalAngleList[res].conditions)
                for item in equalAngleList[res].conditions:
                    if len(item) != len(newInfo6.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo6.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalAngleList[res].conditions.append(newInfo6.conditions[-1])
                equalAngleList[res].weight = min(newInfo6.weight, equalAngleList[res].weight)

        flag = flag1 or flag2 or flag3 or flag4 or flag5 or flag6
        return flag


# 直角推出90°
class LmRiangleGet90(Lemma):
    def __init__(self):
        self.name = "直角等于90°"
        self.inputNum = 3

    @staticmethod
    def Infer(info1, angleList):
        flag = False
        newInfo = Informations.Angle(info1.p1, info1.p2, info1.p3, 90)
        if newInfo is not None:
            # 用一个res来存IsInList返回的值
            newInfo.conditions.append(["直角等于90°", info1])
            res = newInfo.IsInList(angleList)
            newInfo.weight = info1.weight + 1
            if res is False:
                angleList.append(newInfo)
                flag = True
            elif res is True:
                pass
            else:
                nums = len(angleList[res].conditions)
                for item in angleList[res].conditions:
                    if len(item) != len(newInfo.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    angleList[res].conditions.append(newInfo.conditions[-1])
                angleList[res].weight = min(newInfo.weight, angleList[res].weight)

        return flag


# 正方形得四对邻边垂直、一对对角线垂直
class LmSquareGetVertical(Lemma):
    def __init__(self):
        self.name = "正方形的邻边相互垂直"
        self.inputNum = 2

    @staticmethod
    def Infer(info1, verticalLineList, Aux, midPointList, pointList):
        flag = flag1 = flag2 = flag3 = flag4 = flag5 = flag6 = flag7 = False
        # 四对邻边垂直
        newInfo1 = newInfo2 = newInfo3 = newInfo4 = newInfo5 = newInfo6 = newInfo7 = None
        newInfo1 = Informations.VerticalLine(info1.p1, info1.p2, info1.p2, info1.p3,  pointList, info1.p2)
        newInfo2 = Informations.VerticalLine(info1.p2, info1.p3, info1.p3, info1.p4,  pointList, info1.p3)
        newInfo3 = Informations.VerticalLine(info1.p3, info1.p4, info1.p4, info1.p1,  pointList, info1.p4)
        newInfo4 = Informations.VerticalLine(info1.p4, info1.p1, info1.p1, info1.p2,  pointList, info1.p1)
        # 一对对角线垂直
        newInfo5 = Informations.VerticalLine(info1.p1, info1.p3, info1.p2, info1.p4, pointList, Aux)
        # 一对对角线互相平分
        newInfo6 = Informations.MidPoint(Aux, info1.p1, info1.p3)
        newInfo7 = Informations.MidPoint(Aux, info1.p2, info1.p4)
        if newInfo1 is not None:
            # 用一个res来存IsInList返回的值
            newInfo1.conditions.append(["正方形的邻边相互垂直", info1])
            res = newInfo1.IsInList(verticalLineList)
            newInfo1.weight = info1.weight + 1
            if res is False:
                verticalLineList.append(newInfo1)
                flag1 = True
            elif res is True:
                pass
            else:
                nums = len(verticalLineList[res].conditions)
                for item in verticalLineList[res].conditions:
                    if len(item) != len(newInfo1.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo1.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    verticalLineList[res].conditions.append(newInfo1.conditions[-1])
                verticalLineList[res].weight = min(newInfo1.weight, verticalLineList[res].weight)
        if newInfo2 is not None:
            # 用一个res来存IsInList返回的值
            newInfo2.conditions.append(["正方形的邻边相互垂直", info1])
            res = newInfo2.IsInList(verticalLineList)
            newInfo2.weight = info1.weight + 1
            if res is False:
                verticalLineList.append(newInfo2)
                flag2 = True
            elif res is True:
                pass
            else:
                nums = len(verticalLineList[res].conditions)
                for item in verticalLineList[res].conditions:
                    if len(item) != len(newInfo2.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo2.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    verticalLineList[res].conditions.append(newInfo2.conditions[-1])
                verticalLineList[res].weight = min(newInfo2.weight, verticalLineList[res].weight)
        if newInfo3 is not None:
            # 用一个res来存IsInList返回的值
            newInfo3.conditions.append(["正方形的邻边相互垂直", info1])
            res = newInfo3.IsInList(verticalLineList)
            newInfo3.weight = info1.weight + 1
            if res is False:
                verticalLineList.append(newInfo3)
                flag3 = True
            elif res is True:
                pass
            else:
                nums = len(verticalLineList[res].conditions)
                for item in verticalLineList[res].conditions:
                    if len(item) != len(newInfo3.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo3.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    verticalLineList[res].conditions.append(newInfo3.conditions[-1])
                verticalLineList[res].weight = min(newInfo3.weight, verticalLineList[res].weight)
        if newInfo4 is not None:
            # 用一个res来存IsInList返回的值
            newInfo4.conditions.append(["正方形的邻边相互垂直", info1])
            res = newInfo4.IsInList(verticalLineList)
            newInfo4.weight = info1.weight + 1
            if res is False:
                verticalLineList.append(newInfo4)
                flag4 = True
            elif res is True:
                pass
            else:
                nums = len(verticalLineList[res].conditions)
                for item in verticalLineList[res].conditions:
                    if len(item) != len(newInfo4.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo4.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    verticalLineList[res].conditions.append(newInfo4.conditions[-1])
                verticalLineList[res].weight = min(newInfo4.weight, verticalLineList[res].weight)
        if newInfo5 is not None:
            # 用一个res来存IsInList返回的值
            newInfo5.conditions.append(["正方形的邻边相互垂直", info1])
            res = newInfo5.IsInList(verticalLineList)
            newInfo5.weight = info1.weight + 1
            if res is False and Aux is not None:
                verticalLineList.append(newInfo5)
                flag5 = True
            elif res is True:
                pass
            else:
                nums = len(verticalLineList[res].conditions)
                for item in verticalLineList[res].conditions:
                    if len(item) != len(newInfo5.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo5.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    verticalLineList[res].conditions.append(newInfo5.conditions[-1])
                verticalLineList[res].weight = min(newInfo5.weight, verticalLineList[res].weight)
        if newInfo6 is not None:
            # 用一个res来存IsInList返回的值
            newInfo6.conditions.append(["正方形的对角线相互平分", info1])
            res = newInfo6.IsInList(midPointList)
            newInfo6.weight = info1.weight + 1
            if res is False and Aux is not None:
                midPointList.append(newInfo6)
                flag6 = True
            elif res is True:
                pass
            else:
                nums = len(midPointList[res].conditions)
                for item in midPointList[res].conditions:
                    if len(item) != len(newInfo6.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo6.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    midPointList[res].conditions.append(newInfo6.conditions[-1])
                midPointList[res].weight = min(newInfo6.weight, midPointList[res].weight)
        if newInfo7 is not None:
            # 用一个res来存IsInList返回的值
            newInfo7.conditions.append(["正方形的对角线相互平分", info1])
            res = newInfo7.IsInList(midPointList)
            newInfo7.weight = info1.weight + 1
            if res is False and Aux is not None:
                midPointList.append(newInfo7)
                flag7 = True
            elif res is True:
                pass
            else:
                nums = len(midPointList[res].conditions)
                for item in midPointList[res].conditions:
                    if len(item) != len(newInfo7.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo7.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    midPointList[res].conditions.append(newInfo7.conditions[-1])
                midPointList[res].weight = min(newInfo7.weight, midPointList[res].weight)

        flag = flag1 or flag2 or flag3 or flag4 or flag5 or flag6 or flag7
        return flag


# 矩形得四对邻边垂直
class LmRectangleGetVertical(Lemma):
    def __init__(self):
        self.name = "矩形的邻边相互垂直"
        self.inputNum = 2

    @staticmethod
    def Infer(info1, verticalLineList, pointList):
        flag = flag1 = flag2 = flag3 = flag4 = False
        # 四对邻边垂直
        newInfo1 = newInfo2 = newInfo3 = newInfo4 = None
        newInfo1 = Informations.VerticalLine(info1.p1, info1.p2, info1.p2, info1.p3, pointList, info1.p2)
        newInfo2 = Informations.VerticalLine(info1.p2, info1.p3, info1.p3, info1.p4, pointList, info1.p3)
        newInfo3 = Informations.VerticalLine(info1.p3, info1.p4, info1.p4, info1.p1, pointList, info1.p4)
        newInfo4 = Informations.VerticalLine(info1.p4, info1.p1, info1.p1, info1.p2, pointList, info1.p1)
        if newInfo1 is not None:
            # 用一个res来存IsInList返回的值
            newInfo1.conditions.append(["矩形的邻边相互垂直", info1])
            res = newInfo1.IsInList(verticalLineList)
            newInfo1.weight = info1.weight + 1
            if res is False:
                verticalLineList.append(newInfo1)
                flag1 = True
            elif res is True:
                pass
            else:
                nums = len(verticalLineList[res].conditions)
                for item in verticalLineList[res].conditions:
                    if len(item) != len(newInfo1.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo1.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    verticalLineList[res].conditions.append(newInfo1.conditions[-1])
                verticalLineList[res].weight = min(newInfo1.weight, verticalLineList[res].weight)
        if newInfo2 is not None:
            # 用一个res来存IsInList返回的值
            newInfo2.conditions.append(["矩形的邻边相互垂直", info1])
            res = newInfo2.IsInList(verticalLineList)
            newInfo2.weight = info1.weight + 1
            if res is False:
                verticalLineList.append(newInfo2)
                flag2 = True
            elif res is True:
                pass
            else:
                nums = len(verticalLineList[res].conditions)
                for item in verticalLineList[res].conditions:
                    if len(item) != len(newInfo2.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo2.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    verticalLineList[res].conditions.append(newInfo2.conditions[-1])
                verticalLineList[res].weight = min(newInfo2.weight, verticalLineList[res].weight)
        if newInfo3 is not None:
            # 用一个res来存IsInList返回的值
            newInfo3.conditions.append(["矩形的邻边相互垂直", info1])
            res = newInfo3.IsInList(verticalLineList)
            newInfo3.weight = info1.weight + 1
            if res is False:
                verticalLineList.append(newInfo3)
                flag3 = True
            elif res is True:
                pass
            else:
                nums = len(verticalLineList[res].conditions)
                for item in verticalLineList[res].conditions:
                    if len(item) != len(newInfo3.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo3.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    verticalLineList[res].conditions.append(newInfo3.conditions[-1])
                verticalLineList[res].weight = min(newInfo3.weight, verticalLineList[res].weight)
        if newInfo4 is not None:
            # 用一个res来存IsInList返回的值
            newInfo4.conditions.append(["矩形的邻边相互垂直", info1])
            res = newInfo4.IsInList(verticalLineList)
            newInfo4.weight = info1.weight + 1
            if res is False:
                verticalLineList.append(newInfo4)
                flag4 = True
            elif res is True:
                pass
            else:
                nums = len(verticalLineList[res].conditions)
                for item in verticalLineList[res].conditions:
                    if len(item) != len(newInfo4.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo4.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    verticalLineList[res].conditions.append(newInfo4.conditions[-1])
                verticalLineList[res].weight = min(newInfo4.weight, verticalLineList[res].weight)

        flag = flag1 or flag2 or flag3 or flag4
        return flag


# 正方形得到内错角为45°
class LmSquareGetneiangle45(Lemma):
    def __init__(self):
        self.name = "正方形得到内错角为45°°"
        self.inputNum = 2

    @staticmethod
    def Infer(info1, angleList):
        flag = flag1 = flag2 = flag3 = flag4 = flag5 = flag6 = flag7 = flag8 = False
        # 四对邻边垂直
        newInfo1 = newInfo2 = newInfo3 = newInfo4 = newInfo5 = newInfo6 = newInfo7 = newInfo8 = None
        newInfo1 = Informations.Angle(info1.p2, info1.p1, info1.p3, 45)
        newInfo2 = Informations.Angle(info1.p4, info1.p1, info1.p3, 45)

        newInfo3 = Informations.Angle(info1.p1, info1.p2, info1.p4, 45)
        newInfo4 = Informations.Angle(info1.p3, info1.p2, info1.p4, 45)

        newInfo5 = Informations.Angle(info1.p2, info1.p3, info1.p1, 45)
        newInfo6 = Informations.Angle(info1.p4, info1.p3, info1.p1, 45)

        newInfo7 = Informations.Angle(info1.p1, info1.p4, info1.p2, 45)
        newInfo8 = Informations.Angle(info1.p3, info1.p4, info1.p2, 45)
        if newInfo1 is not None:
            # 用一个res来存IsInList返回的值
            newInfo1.conditions.append(["正方形得到内错角为45°", info1])
            res = newInfo1.IsInList(angleList)
            newInfo1.weight = info1.weight + 1
            if res is False:
                angleList.append(newInfo1)
                flag1 = True
            elif res is True:
                pass
            else:
                nums = len(angleList[res].conditions)
                for item in angleList[res].conditions:
                    if len(item) != len(newInfo1.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo1.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    angleList[res].conditions.append(newInfo1.conditions[-1])
                angleList[res].weight = min(newInfo1.weight, angleList[res].weight)
        if newInfo2 is not None:
            # 用一个res来存IsInList返回的值
            newInfo2.conditions.append(["正方形得到内错角为45°", info1])
            res = newInfo2.IsInList(angleList)
            newInfo2.weight = info1.weight + 1
            if res is False:
                angleList.append(newInfo2)
                flag2 = True
            elif res is True:
                pass
            else:
                nums = len(angleList[res].conditions)
                for item in angleList[res].conditions:
                    if len(item) != len(newInfo2.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo2.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    angleList[res].conditions.append(newInfo2.conditions[-1])
                angleList[res].weight = min(newInfo2.weight, angleList[res].weight)
        if newInfo3 is not None:
            # 用一个res来存IsInList返回的值
            newInfo3.conditions.append(["正方形得到内错角为45°", info1])
            res = newInfo3.IsInList(angleList)
            newInfo3.weight = info1.weight + 1
            if res is False:
                angleList.append(newInfo3)
                flag3 = True
            elif res is True:
                pass
            else:
                nums = len(angleList[res].conditions)
                for item in angleList[res].conditions:
                    if len(item) != len(newInfo3.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo3.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    angleList[res].conditions.append(newInfo3.conditions[-1])
                angleList[res].weight = min(newInfo3.weight, angleList[res].weight)
        if newInfo4 is not None:
            # 用一个res来存IsInList返回的值
            newInfo4.conditions.append(["正方形得到内错角为45°", info1])
            res = newInfo4.IsInList(angleList)
            newInfo4.weight = info1.weight + 1
            if res is False:
                angleList.append(newInfo4)
                flag4 = True
            elif res is True:
                pass
            else:
                nums = len(angleList[res].conditions)
                for item in angleList[res].conditions:
                    if len(item) != len(newInfo4.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo4.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    angleList[res].conditions.append(newInfo4.conditions[-1])
                angleList[res].weight = min(newInfo4.weight, angleList[res].weight)
        if newInfo5 is not None:
            # 用一个res来存IsInList返回的值
            newInfo5.conditions.append(["正方形得到内错角为45°", info1])
            res = newInfo5.IsInList(angleList)
            newInfo5.weight = info1.weight + 1
            if res is False:
                angleList.append(newInfo5)
                flag5 = True
            elif res is True:
                pass
            else:
                nums = len(angleList[res].conditions)
                for item in angleList[res].conditions:
                    if len(item) != len(newInfo5.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo5.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    angleList[res].conditions.append(newInfo5.conditions[-1])
                angleList[res].weight = min(newInfo5.weight, angleList[res].weight)
        if newInfo6 is not None:
            # 用一个res来存IsInList返回的值
            newInfo6.conditions.append(["正方形得到内错角为45°", info1])
            res = newInfo6.IsInList(angleList)
            newInfo6.weight = info1.weight + 1
            if res is False:
                angleList.append(newInfo6)
                flag6 = True
            elif res is True:
                pass
            else:
                nums = len(angleList[res].conditions)
                for item in angleList[res].conditions:
                    if len(item) != len(newInfo6.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo6.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    angleList[res].conditions.append(newInfo6.conditions[-1])
                angleList[res].weight = min(newInfo6.weight, angleList[res].weight)
        if newInfo7 is not None:
            # 用一个res来存IsInList返回的值
            newInfo7.conditions.append(["正方形得到内错角为45°", info1])
            res = newInfo7.IsInList(angleList)
            newInfo7.weight = info1.weight + 1
            if res is False:
                angleList.append(newInfo7)
                flag7 = True
            elif res is True:
                pass
            else:
                nums = len(angleList[res].conditions)
                for item in angleList[res].conditions:
                    if len(item) != len(newInfo7.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo7.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    angleList[res].conditions.append(newInfo7.conditions[-1])
                angleList[res].weight = min(newInfo7.weight, angleList[res].weight)
        if newInfo8 is not None:
            # 用一个res来存IsInList返回的值
            newInfo8.conditions.append(["正方形得到内错角为45°", info1])
            res = newInfo8.IsInList(angleList)
            newInfo8.weight = info1.weight + 1
            if res is False:
                angleList.append(newInfo8)
                flag8 = True
            elif res is True:
                pass
            else:
                nums = len(angleList[res].conditions)
                for item in angleList[res].conditions:
                    if len(item) != len(newInfo8.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo8.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    angleList[res].conditions.append(newInfo8.conditions[-1])
                angleList[res].weight = min(newInfo8.weight, angleList[res].weight)
        flag = flag1 or flag2 or flag3 or flag4 or flag5 or flag6 or flag7 or flag8
        return flag


# 正方形得到邻边相等
class LmSquareGetLineEQ(Lemma):
    def __init__(self):
        self.name = "正方形得到邻边相等°"
        self.inputNum = 2

    @staticmethod
    def Infer(info1, equalLineList):
        flag = False
        newInfo = Informations.EqualLine(info1.p1, info1.p2, info1.p2, info1.p3)
        if newInfo is not None:
            # 用一个res来存IsInList返回的值
            newInfo.conditions.append(["正方形得到邻边相等", info1])
            res = newInfo.IsInList(equalLineList)
            newInfo.weight = info1.weight + 1
            if res is False:
                equalLineList.append(newInfo)
                flag = True
            elif res is True:
                pass
            else:
                nums = len(equalLineList[res].conditions)
                for item in equalLineList[res].conditions:
                    if len(item) != len(newInfo.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalLineList[res].conditions.append(newInfo.conditions[-1])
                equalLineList[res].weight = min(newInfo.weight, equalLineList[res].weight)
        return flag


# 角度相等的角相等
class LmAngleNumEQ(Lemma):
    def __init__(self):
        self.name = "角度相等的角相等"
        self.inputNum = 2

    @staticmethod
    def Infer(info1, info2, equalAngleList, complementaryAngleList, coterminalAngleList, coLineList):
        flag = False
        if info1.p4 == info2.p4:
            newInfo = Informations.EqualAngle(info1.p1, info1.p2, info1.p3, info2.p1, info2.p2, info2.p3)
            if newInfo is not None:
                # 用一个res来存IsInList返回的值
                newInfo.conditions.append(["角度相等的角相等", info1, info2])
                res = newInfo.IsInList(equalAngleList, coLineList)
                newInfo.weight = max(info1.weight, info2.weight) + 1
                if res is False:
                    equalAngleList.append(newInfo)
                    flag = True
                elif res is True:
                    pass
                else:
                    nums = len(equalAngleList[res].conditions)
                    for item in equalAngleList[res].conditions:
                        if len(item) != len(newInfo.conditions[-1]):
                            nums -= 1
                            continue
                        else:
                            for list_no in range(len(item)):
                                if item[list_no] != newInfo.conditions[-1][list_no]:
                                    nums -= 1
                                    break
                    if nums == 0:
                        equalAngleList[res].conditions.append(newInfo.conditions[-1])
                    equalAngleList[res].weight = min(newInfo.weight, equalAngleList[res].weight)
        if (info1.p4 + info2.p4) == 180:
            newInfo1 = Informations.ComplementaryAngle(info1.p1, info1.p2, info1.p3, info2.p1, info2.p2, info2.p3)
            if newInfo1 is not None:
                # 用一个res来存IsInList返回的值
                newInfo1.conditions.append(["互补角", info1, info2])
                res = newInfo1.IsInList(complementaryAngleList, coLineList)
                newInfo1.weight = max(info1.weight, info2.weight) + 1
                if res is False:
                    complementaryAngleList.append(newInfo1)
                    flag = True
                elif res is True:
                    pass
                else:
                    nums = len(complementaryAngleList[res].conditions)
                    for item in complementaryAngleList[res].conditions:
                        if len(item) != len(newInfo1.conditions[-1]):
                            nums -= 1
                            continue
                        else:
                            for list_no in range(len(item)):
                                if item[list_no] != newInfo1.conditions[-1][list_no]:
                                    nums -= 1
                                    break
                    if nums == 0:
                        complementaryAngleList[res].conditions.append(newInfo1.conditions[-1])
                    complementaryAngleList[res].weight = min(newInfo1.weight, complementaryAngleList[res].weight)
        if (info1.p4 + info2.p4) == 90:
            newInfo2 = Informations.CoterminalAngles(info1.p1, info1.p2, info1.p3, info2.p1, info2.p2, info2.p3)
            if newInfo2 is not None:
                # 用一个res来存IsInList返回的值
                newInfo2.conditions.append(["互余角", info1, info2])
                res = newInfo2.IsInList(coterminalAngleList, coLineList)
                newInfo2.weight = max(info1.weight, info2.weight) + 1
                if res is False:
                    coterminalAngleList.append(newInfo2)
                    flag = True
                elif res is True:
                    pass
                else:
                    nums = len(coterminalAngleList[res].conditions)
                    for item in coterminalAngleList[res].conditions:
                        if len(item) != len(newInfo2.conditions[-1]):
                            nums -= 1
                            continue
                        else:
                            for list_no in range(len(item)):
                                if item[list_no] != newInfo2.conditions[-1][list_no]:
                                    nums -= 1
                                    break
                    if nums == 0:
                        coterminalAngleList[res].conditions.append(newInfo2.conditions[-1])
                    coterminalAngleList[res].weight = min(newInfo2.weight, coterminalAngleList[res].weight)
        return flag


# 等边三角形得到三个角为60°
class LmRegularTriangGetAngle(Lemma):
    def __init__(self):
        self.name = "等边三角形得到三个角为60°"
        self.inputNum = 2

    @staticmethod
    def Infer(info1, angleList):
        flag = flag1 = flag2 = flag3 = False
        newInfo1 = Informations.Angle(info1.p1, info1.p2, info1.p3, 60)
        newInfo2 = Informations.Angle(info1.p2, info1.p3, info1.p1, 60)
        newInfo3 = Informations.Angle(info1.p3, info1.p1, info1.p2, 60)
        if newInfo1 is not None:
            # 用一个res来存IsInList返回的值
            newInfo1.conditions.append(["等边三角形得到三个角为60°", info1])
            res = newInfo1.IsInList(angleList)
            newInfo1.weight = info1.weight + 1
            if res is False:
                angleList.append(newInfo1)
                flag1 = True
            elif res is True:
                pass
            else:
                nums = len(angleList[res].conditions)
                for item in angleList[res].conditions:
                    if len(item) != len(newInfo1.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo1.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    angleList[res].conditions.append(newInfo1.conditions[-1])
                angleList[res].weight = min(newInfo1.weight, angleList[res].weight)
        if newInfo2 is not None:
            # 用一个res来存IsInList返回的值
            newInfo2.conditions.append(["等边三角形得到三个角为60°", info1])
            res = newInfo2.IsInList(angleList)
            newInfo2.weight = info1.weight + 1
            if res is False:
                angleList.append(newInfo2)
                flag2 = True
            elif res is True:
                pass
            else:
                nums = len(angleList[res].conditions)
                for item in angleList[res].conditions:
                    if len(item) != len(newInfo2.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo2.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    angleList[res].conditions.append(newInfo2.conditions[-1])
                angleList[res].weight = min(newInfo2.weight, angleList[res].weight)
        if newInfo3 is not None:
            # 用一个res来存IsInList返回的值
            newInfo3.conditions.append(["等边三角形得到三个角为60°", info1])
            res = newInfo3.IsInList(angleList)
            newInfo3.weight = info1.weight + 1
            if res is False:
                angleList.append(newInfo3)
                flag3 = True
            elif res is True:
                pass
            else:
                nums = len(angleList[res].conditions)
                for item in angleList[res].conditions:
                    if len(item) != len(newInfo3.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo3.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    angleList[res].conditions.append(newInfo3.conditions[-1])
                angleList[res].weight = min(newInfo3.weight, angleList[res].weight)

        flag = flag1 or flag2 or flag3
        return flag


# 等边三角形得到三个边分别相等
class LmRegularTriangLine(Lemma):
    def __init__(self):
        self.name = "等边三角形得到三个角为60°"
        self.inputNum = 2

    @staticmethod
    def Infer(info1, equalLineList):
        flag = flag1 = flag2 = False
        newInfo1 = Informations.EqualLine(info1.p1, info1.p2, info1.p2, info1.p3)
        newInfo2 = Informations.EqualLine(info1.p2, info1.p3, info1.p3, info1.p1)
        if newInfo1 is not None:
            # 用一个res来存IsInList返回的值
            newInfo1.conditions.append(["等边三角形得到三个边分别相等", info1])
            res = newInfo1.IsInList(equalLineList)
            newInfo1.weight = info1.weight + 1
            if res is False:
                equalLineList.append(newInfo1)
                flag1 = True
            elif res is True:
                pass
            else:
                nums = len(equalLineList[res].conditions)
                for item in equalLineList[res].conditions:
                    if len(item) != len(newInfo1.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo1.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalLineList[res].conditions.append(newInfo1.conditions[-1])
                equalLineList[res].weight = min(newInfo1.weight, equalLineList[res].weight)
        if newInfo2 is not None:
            # 用一个res来存IsInList返回的值
            newInfo2.conditions.append(["等边三角形得到三个边分别相等", info1])
            res = newInfo2.IsInList(equalLineList)
            newInfo2.weight = info1.weight + 1
            if res is False:
                equalLineList.append(newInfo2)
                flag2 = True
            elif res is True:
                pass
            else:
                nums = len(equalLineList[res].conditions)
                for item in equalLineList[res].conditions:
                    if len(item) != len(newInfo2.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo2.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalLineList[res].conditions.append(newInfo2.conditions[-1])
                equalLineList[res].weight = min(newInfo2.weight, equalLineList[res].weight)
        flag = flag1 or flag2
        return flag


# 四点共圆的性质
class LmFourPointOnCircle(Lemma):
    def __init__(self):
        self.name = "四点共圆的性质"
        self.inputNum = 2

    @staticmethod
    def Infer(info1, equalAngleList, complementaryAngleList, coLineList):
        flag = flag1 = flag2 = flag3 = flag4 = flag5 = flag6 = False
        newInfo1 = Informations.ComplementaryAngle(info1.p1, info1.p2, info1.p3, info1.p3, info1.p4, info1.p1)
        newInfo2 = Informations.ComplementaryAngle(info1.p2, info1.p3, info1.p4, info1.p4, info1.p1, info1.p2)
        if newInfo1 is not None:
            # 用一个res来存IsInList返回的值
            newInfo1.conditions.append(["圆内接四边形的对角互补", info1])
            res = newInfo1.IsInList(complementaryAngleList, coLineList)
            newInfo1.weight = info1.weight + 1
            if res is False:
                complementaryAngleList.append(newInfo1)
                flag1 = True
            elif res is True:
                pass
            else:
                nums = len(complementaryAngleList[res].conditions)
                for item in complementaryAngleList[res].conditions:
                    if len(item) != len(newInfo1.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo1.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    complementaryAngleList[res].conditions.append(newInfo1.conditions[-1])
                complementaryAngleList[res].weight = min(newInfo1.weight, complementaryAngleList[res].weight)
        if newInfo2 is not None:
            # 用一个res来存IsInList返回的值
            newInfo2.conditions.append(["圆内接四边形的对角互补", info1])
            res = newInfo2.IsInList(complementaryAngleList, coLineList)
            newInfo2.weight = info1.weight + 1
            if res is False:
                complementaryAngleList.append(newInfo2)
                flag2 = True
            elif res is True:
                pass
            else:
                nums = len(complementaryAngleList[res].conditions)
                for item in complementaryAngleList[res].conditions:
                    if len(item) != len(newInfo2.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo2.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    complementaryAngleList[res].conditions.append(newInfo2.conditions[-1])
                complementaryAngleList[res].weight = min(newInfo2.weight, complementaryAngleList[res].weight)

        newInfo21 = Informations.EqualAngle(info1.p1, info1.p3, info1.p2, info1.p1, info1.p4, info1.p2)
        newInfo22 = Informations.EqualAngle(info1.p2, info1.p1, info1.p3, info1.p2, info1.p4, info1.p3)
        newInfo23 = Informations.EqualAngle(info1.p3, info1.p1, info1.p4, info1.p3, info1.p2, info1.p4)
        newInfo24 = Informations.EqualAngle(info1.p4, info1.p2, info1.p1, info1.p4, info1.p3, info1.p1)
        if newInfo21 is not None:
            # 用一个res来存IsInList返回的值
            newInfo21.conditions.append(["共圆的四个点所连成同侧共底的两个三角形的顶角相等", info1])
            res = newInfo21.IsInList(equalAngleList, coLineList)
            newInfo21.weight = info1.weight + 1
            if res is False:
                equalAngleList.append(newInfo21)
                flag3 = True
            elif res is True:
                pass
            else:
                nums = len(equalAngleList[res].conditions)
                for item in equalAngleList[res].conditions:
                    if len(item) != len(newInfo21.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo21.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalAngleList[res].conditions.append(newInfo21.conditions[-1])
                equalAngleList[res].weight = min(newInfo21.weight, equalAngleList[res].weight)
        if newInfo22 is not None:
            # 用一个res来存IsInList返回的值
            newInfo22.conditions.append(["共圆的四个点所连成同侧共底的两个三角形的顶角相等", info1])
            res = newInfo22.IsInList(equalAngleList, coLineList)
            newInfo22.weight = info1.weight + 1
            if res is False:
                equalAngleList.append(newInfo22)
                flag4 = True
            elif res is True:
                pass
            else:
                nums = len(equalAngleList[res].conditions)
                for item in equalAngleList[res].conditions:
                    if len(item) != len(newInfo22.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo22.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalAngleList[res].conditions.append(newInfo22.conditions[-1])
                equalAngleList[res].weight = min(newInfo22.weight, equalAngleList[res].weight)
        if newInfo23 is not None:
            # 用一个res来存IsInList返回的值
            newInfo23.conditions.append(["共圆的四个点所连成同侧共底的两个三角形的顶角相等", info1])
            res = newInfo23.IsInList(equalAngleList, coLineList)
            newInfo23.weight = info1.weight + 1
            if res is False:
                equalAngleList.append(newInfo23)
                flag5 = True
            elif res is True:
                pass
            else:
                nums = len(equalAngleList[res].conditions)
                for item in equalAngleList[res].conditions:
                    if len(item) != len(newInfo23.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo23.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalAngleList[res].conditions.append(newInfo23.conditions[-1])
                equalAngleList[res].weight = min(newInfo23.weight, equalAngleList[res].weight)
        if newInfo24 is not None:
            # 用一个res来存IsInList返回的值
            newInfo24.conditions.append(["共圆的四个点所连成同侧共底的两个三角形的顶角相等", info1])
            res = newInfo24.IsInList(equalAngleList, coLineList)
            newInfo24.weight = info1.weight + 1
            if res is False:
                equalAngleList.append(newInfo24)
                flag6 = True
            elif res is True:
                pass
            else:
                nums = len(equalAngleList[res].conditions)
                for item in equalAngleList[res].conditions:
                    if len(item) != len(newInfo24.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo24.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalAngleList[res].conditions.append(newInfo24.conditions[-1])
                equalAngleList[res].weight = min(newInfo24.weight, equalAngleList[res].weight)

        flag = flag1 or flag2 or flag3 or flag4 or flag5 or flag6
        return flag
