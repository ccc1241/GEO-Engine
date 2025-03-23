import copy
from collections import deque

import Informations
import Lemmas
import time
import re
import api_test
# import sys
import os

os.environ['OMP_NUM_THREADS'] = '1'
# sys.setrecursionlimit(10000)
# 存放从题目得到的已知信息，以及在推理过程中生成的所有信息
# 线段与线段相交没有对应的谓词，拆分成了共线、对顶角等谓词
pointList = list()  # 点集合@
midPointList = list()  # 中点集合@
parallelLineList = list()  # 平行线集合@
verticalLineList = list()  # 垂直线集合@
angleList = list()  # 角集合@
rightAngleList = list()  # 直角集合@
triangleList = list()  # 三角形集合@
rtTrianglelist = list()  # 直角三角形集合
parallogramList = list()  # 平行四边形集合@
rhombusList = list()  # 菱形集合#
rectangleList = list()  # 矩形集合@
squareList = list()  # 正方形集合@
ovalList = list()  # 椭圆集合#
circleList = list()  # 圆集合#
equalLineList = list()  # 相等线集合@
equalAngleList = list()  # 相等角集合@
alter_Inter_AngleList = list()  # 内错角集合#
equalTriangleList = list()  # 全等三角形集合@
similarTriangleList = list()  # 相似三角形集合@
coLineList = list()  # 共线集合@
regularTriangList = list()  # 等边三角形集合@
complementaryAngleList = list()  # 互补角集合@
coterminalAngleList = list()  # 互余角集合@
ratioLineList = list()  # 成比例线段集合@
ratioAngleList = list()  # 成比例角集合@
bisectorAngleList = list()  # 角平分线集合@
isoTriangleList = list()  # 等腰三角形集合@
isoAndRtTriangleList = list()  # 等腰直角三角形集合

alreadySquareList = list()  # 已经构建过对角线交叉辅助点的正方形
conjectureList = list()  # 待证结论

set_new_title = set()  # 新题所用条件
set_old_title = set()  # 旧题所用条件

proveTreeList = []


def Clear_fixpoint():
    pointList.clear()
    midPointList.clear()
    parallelLineList.clear()
    verticalLineList.clear()
    angleList.clear()
    rightAngleList.clear()
    triangleList.clear()
    parallogramList.clear()
    rhombusList.clear()
    rectangleList.clear()
    squareList.clear()
    ovalList.clear()
    circleList.clear()
    equalLineList.clear()
    equalAngleList.clear()
    alter_Inter_AngleList.clear()
    equalTriangleList.clear()
    similarTriangleList.clear()
    coLineList.clear()
    regularTriangList.clear()
    complementaryAngleList.clear()
    coterminalAngleList.clear()
    ratioLineList.clear()
    ratioAngleList.clear()
    bisectorAngleList.clear()
    isoTriangleList.clear()
    isoAndRtTriangleList.clear()
    alreadySquareList.clear()
    conjectureList.clear()
    set_new_title.clear()
    set_old_title.clear()
    print("缓存已清除")


# 构造辅助点的类
class StaticAuxPoint:
    static_var = 'X'

    @classmethod
    def get_next(cls):
        current_value = cls.static_var
        cls.static_var = chr(ord(cls.static_var) + 1)
        print("构造辅助点：", current_value)
        return current_value


def get_cut(input_title):
    book = [25, 25, 25, 25]
    return 25


# 两个三角形，两个角分别相等，则第三个角也相等
def ReasonByLmDoubleangle_ThirdAngle():
    # 当对应链表中元素小于2，则没法推理，直接返回
    if len(equalAngleList) < 2:
        return False
    flag = False  # 判断一轮挖掘过程是否生成新的信息，生成即返回True
    for i in range(len(equalAngleList)):
        for j in range(i + 1, len(equalAngleList)):
            newInfo = Lemmas.LmDoubleangle_ThirdAngle.Infer(equalAngleList[i], equalAngleList[j])
            if newInfo is not None:
                # 用一个res来存IsInList返回的值
                res = newInfo.IsInList(equalAngleList, coLineList)
                newInfo.weight = max(equalAngleList[i].weight, equalAngleList[j].weight) + 1
                if res is False:
                    equalAngleList.append(newInfo)
                    flag = True
                elif res is True:
                    continue
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
    checkEndlessLoop(flag, "ReasonByLmDoubleangle_ThirdAngle")
    return flag


# 内错角转为相等角
def ReasonByLmAIangle_EQangle():
    # 当对应链表中元素小于2，则没法推理，直接返回
    if len(alter_Inter_AngleList) < 1:
        return False
    flag = False  # 判断一轮挖掘过程是否生成新的信息，生成即返回True
    for i in range(len(alter_Inter_AngleList)):
        newInfo = Informations.EqualAngle(alter_Inter_AngleList[i].p1, alter_Inter_AngleList[i].p2,
                                          alter_Inter_AngleList[i].p3, alter_Inter_AngleList[i].p4,
                                          alter_Inter_AngleList[i].p5, alter_Inter_AngleList[i].p6)
        # newInfo.source = "内错角相等"
        newInfo.conditions.append(["内错角相等", alter_Inter_AngleList[i]])
        # 在加入链表之前，要判断链表中是否已有相同信息；若相同则不添加
        if newInfo is not None:
            # 用一个res来存IsInList返回的值
            res = newInfo.IsInList(equalAngleList, coLineList)
            newInfo.weight = alter_Inter_AngleList[i].weight + 1
            if res is False:
                equalAngleList.append(newInfo)
                flag = True
            elif res is True:
                continue
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
    checkEndlessLoop(flag, "ReasonByLmAIangle_EQangle")
    return flag


# 直角转为相等角
def ReasonByLmRangle_EQangle():
    # 当对应链表中元素小于2，则没法推理，直接返回
    if len(rightAngleList) < 2:
        return False
    flag = False  # 判断一轮挖掘过程是否生成新的信息，生成即返回True
    for i in range(len(rightAngleList)):
        for j in range(i + 1, len(rightAngleList)):
            newInfo = Informations.EqualAngle(rightAngleList[i].p1, rightAngleList[i].p2,
                                              rightAngleList[i].p3, rightAngleList[j].p1,
                                              rightAngleList[j].p2, rightAngleList[j].p3)
            # newInfo.source = "直角相等"
            # newInfo.conditions.append(rightAngleList[i])
            newInfo.conditions.append(["直角相等", rightAngleList[i], rightAngleList[j]])

            # 在加入链表之前，要判断链表中是否已有相同信息；若相同则不添加
            if newInfo is not None:
                # 用一个res来存IsInList返回的值
                res = newInfo.IsInList(equalAngleList, coLineList)
                newInfo.weight = max(rightAngleList[i].weight, rightAngleList[j].weight) + 1
                if res is False:
                    equalAngleList.append(newInfo)
                    flag = True
                elif res is True:
                    continue
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
    checkEndlessLoop(flag, "ReasonByLmRangle_EQangle")
    return flag


# 两个复合角相等的证明
# def ReasonByLmdDoubleAngleEqual():
# # 当对应链表中元素小于2，则没法推理，直接返回
# if len(angleList) < 2 and len(equalAngleList) < 2:
#     return False
# flag = False  # 判断一轮挖掘过程是否生成新的信息，生成即返回True
# for i in range(len(angleList)):
#     for j in range(i + 1, len(angleList)):
#         newInfo = Lemmas.LmdDoubleAngleEqual.Infer(angleList[i], angleList[j])
#         # 在加入链表之前，要判断链表中是否已有相同信息；若相同则不添加
#         if newInfo != None and newInfo.IsInList(angleList) == False:
#             angleList.append(newInfo)
#             for n in range(len(equalAngleList)):
#                 newInfo1 = LmFindequalAngle(angleList[i], equalAngleList[n])
#                 if newInfo1 != None and newInfo1.IsInList(angleList) == False:
#                     angleList.append(newInfo1)
#                 for m in range(len(equalAngleList)):
#                     newInfo2 = LmFindequalAngle(angleList[j], equalAngleList[m])
#                     if newInfo2 != None and newInfo2.IsInList(angleList) == False:
#                         angleList.append(newInfo2)
#                 if newInfo1 and newInfo2:
#                     newInfo3 = Lemmas.LmdDoubleAngleEqual.Infer(newInfo1, newInfo2)
#                     if newInfo3:
#                         newInfo4 = Informations.EqualAngle(newInfo.p1, newInfo.p2, newInfo.p3, newInfo3.p1,
#                                                            newInfo3.p2, newInfo3.p3)
#                         if newInfo4 != None and newInfo4.IsInList(equalAngleList, coLineList) == False:
#                             newInfo4.source = "两个大角各自的两个小角相等，推出两个大角也相等"
#                             newInfo4.conditions.append(newInfo)
#                             newInfo4.conditions.append(newInfo3)
#                             newInfo4.conditions.append(equalAngleList[n])
#                             newInfo4.conditions.append(equalAngleList[m])
#                             equalAngleList.append(newInfo4)
#                             flag = True
# return flag


# 在相等角集合info2中找出角info1的相等角newInfo
# def LmFindequalAngle(info1, info2):
#     newInfo = None
#     if info1.p2 == info2.p2:
#         if (info1.p1 == info2.p1 and info1.p3 == info2.p3) or (info1.p1 == info2.p3 and info1.p3 == info2.p1):
#             newInfo = Informations.Angle(info2.p4, info2.p5, info2.p6)
#     elif info1.p2 == info2.p5:
#         if (info1.p1 == info2.p4 and info1.p3 == info2.p6) or (info1.p1 == info2.p6 and info1.p3 == info2.p4):
#             newInfo = Informations.Angle(info2.p1, info2.p2, info2.p3)
#     return newInfo


# 全等三角形的证明（角边角）
def ReasonByLmEqualTriangleALA():
    # printAllList(1)
    # 当对应链表中元素小于2，则没法推理，直接返回
    if len(equalLineList) < 1 and len(equalAngleList) < 2:
        return False
    flag = False  # 判断一轮挖掘过程是否生成新的信息，生成即返回True
    for i in range(len(equalAngleList)):
        set1 = set()
        set1.update(equalAngleList[i].p1, equalAngleList[i].p2, equalAngleList[i].p3)
        for m in range(len(equalLineList)):
            set2 = set()
            set3 = set()
            set2.update(equalLineList[m].p1, equalLineList[m].p2)
            set3.update(equalLineList[m].p3, equalLineList[m].p4)
            if len(set1 - set2) == 1 or len(set1 - set3) == 1:
                for j in range(i + 1, len(equalAngleList)):
                    set4 = set()
                    set5 = set()
                    set4.update(equalAngleList[j].p1, equalAngleList[j].p2, equalAngleList[j].p3)
                    set5.update(equalAngleList[j].p4, equalAngleList[j].p5, equalAngleList[j].p6)
                    if set1 == set4 or set1 == set5:
                        newInfo = Lemmas.LmEqualTriangleALA.Infer(equalAngleList[i], equalAngleList[j],
                                                                  equalLineList[m])
                        # 在加入链表之前，要判断链表中是否已有相同信息；若相同则不添加
                        if newInfo is not None:
                            # 用一个res来存IsInList返回的值
                            res = newInfo.IsInList(equalTriangleList, coLineList)
                            newInfo.weight = max(equalAngleList[i].weight, equalAngleList[j].weight,
                                                 equalLineList[m].weight) + 1
                            if res is False:
                                equalTriangleList.append(newInfo)
                                flag = True
                            elif res is True:
                                continue
                            else:
                                # 对比equalTriangleList[res].conditions中的每一个condition和newInfo.conditions中的[-1]号condition，如果相同就跳过，不相同就append
                                # equalTriangleList[res] 等于 newInfo，需要判断前者的conditions中是否已经包含了newInfo的condition
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
    checkEndlessLoop(flag, "ReasonByLmEqualTriangleALA")
    return flag


# 全等三角形的证明（边边边）
def ReasonByLmEqualTriangleLLL():
    # 当对应链表中元素小于2，则没法推理，直接返回
    if len(equalLineList) < 2:
        return False
    flag = flag1 = flag2 = False  # 判断一轮挖掘过程是否生成新的信息，生成即返回True
    newInfo1 = newInfo2 = None
    for i in range(len(equalLineList)):
        for j in range(i + 1, len(equalLineList)):
            # 推理有邻边的全等三角形
            flag1 = Lemmas.LmEqualTriangleLLL_1.Infer(equalLineList[i], equalLineList[j], equalTriangleList, coLineList)
            # 在加入链表之前，要判断链表中是否已有相同信息；若相同则不添加
            for m in range(j + 1, len(equalLineList)):
                # 推理无邻边的全等三角形
                flag2 = Lemmas.LmEqualTriangleLLL_2.Infer(equalLineList[i], equalLineList[j], equalLineList[m],
                                                          equalTriangleList, coLineList)
    flag = flag1 or flag2
    checkEndlessLoop(flag, "ReasonByLmEqualTriangleLLL")
    return flag


# 全等三角形的证明（边角边）
def ReasonByLmEqualTriangleLAL():
    if len(equalLineList) < 2 and len(equalAngleList) < 1:
        return False
    flag = False  # 判断一轮挖掘过程是否生成新的信息，生成即返回True

    for m in range(len(equalAngleList)):
        for i in range(len(equalLineList)):
            for j in range(i + 1, len(equalLineList)):
                newInfo = Lemmas.LmEqualTriangleLAL.Infer(equalAngleList[m], equalLineList[i], equalLineList[j])
                # 在加入链表之前，要判断链表中是否已有相同信息；若相同则不添加
                if newInfo is not None:
                    # 用一个res来存IsInList返回的值
                    res = newInfo.IsInList(equalTriangleList, coLineList)
                    newInfo.weight = max(equalAngleList[m].weight, equalLineList[i].weight, equalLineList[j].weight) + 1
                    if res is False:
                        equalTriangleList.append(newInfo)
                        flag = True
                    elif res is True:
                        continue
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
    checkEndlessLoop(flag, "ReasonByLmEqualTriangleLAL")
    return flag


# 无邻边的全等三角形的证明（HL）
def ReasonByLmEqualTriangleHL():
    if len(rightAngleList) < 2 and len(equalLineList) < 2:
        return False
    flag = False  # 判断一轮挖掘过程是否生成新的信息，生成即返回True

    for i in range(len(rightAngleList)):
        # set1是第一个直角三角形的斜边
        # set1_1、set1_2是第一个直角三角形的两个直角边
        set1 = set()
        set1_1 = set()
        set1_2 = set()
        set1.update(rightAngleList[i].p1, rightAngleList[i].p3)
        set1_1.update(rightAngleList[i].p1, rightAngleList[i].p2)
        set1_2.update(rightAngleList[i].p2, rightAngleList[i].p3)
        for j in range(i + 1, len(rightAngleList)):
            # set2是第二个直角三角形的斜边
            # set2_1、set2_2是第二个直角三角形的两个直角边
            set2 = set()
            set2_1 = set()
            set2_2 = set()
            set2.update(rightAngleList[j].p1, rightAngleList[j].p3)
            set2_1.update(rightAngleList[j].p1, rightAngleList[j].p2)
            set2_2.update(rightAngleList[j].p2, rightAngleList[j].p3)
            flag_HF = 0
            flag_HF_1 = 0
            temp = 0
            temp1 = 0
            newInfo = None
            if set1 == set2:
                flag_HF_1 = 1
            # 直角边为邻边的情况：
            elif set1_1 == set2_1:
                flag_HF_1 = 2
            elif set1_1 == set2_2:
                flag_HF_1 = 3
            elif set1_2 == set2_1:
                flag_HF_1 = 4
            elif set1_2 == set2_2:
                flag_HF_1 = 5
            for m in range(len(equalLineList)):
                set_m_1 = set()
                set_m_2 = set()
                set_m_1.update(equalLineList[m].p1, equalLineList[m].p2)
                set_m_2.update(equalLineList[m].p3, equalLineList[m].p4)
                if flag_HF_1 != 1:
                    if (set1 == set_m_1 and set2 == set_m_2) or (set1 == set_m_2 and set2 == set_m_1):
                        temp = m
                        flag_HF += 1
                if flag_HF_1 == 0 or flag_HF_1 == 1:
                    if (set1_1 == set_m_1 and set2_1 == set_m_2) or (set1_1 == set_m_2 and set2_1 == set_m_1):
                        temp1 = m
                        flag_HF += 1
                    elif (set1_1 == set_m_1 and set2_2 == set_m_2) or (set1_1 == set_m_2 and set2_2 == set_m_1):
                        temp1 = m
                        flag_HF += 1
                    elif (set1_2 == set_m_1 and set2_1 == set_m_2) or (set1_2 == set_m_2 and set2_1 == set_m_1):
                        temp1 = m
                        flag_HF += 1
                    elif (set1_2 == set_m_1 and set2_2 == set_m_2) or (set1_2 == set_m_2 and set2_2 == set_m_1):
                        temp1 = m
                        flag_HF += 1
                if flag_HF == 2:
                    newInfo1 = Informations.EqualTriangle(rightAngleList[i].p1, rightAngleList[i].p2,
                                                          rightAngleList[i].p3,
                                                          rightAngleList[j].p1, rightAngleList[j].p2,
                                                          rightAngleList[j].p3)
                    newInfo2 = Informations.EqualTriangle(rightAngleList[i].p1, rightAngleList[i].p2,
                                                          rightAngleList[i].p3,
                                                          rightAngleList[j].p3, rightAngleList[j].p2,
                                                          rightAngleList[j].p1)
                    if Lemmas.check_EQTiangle(newInfo1, equalLineList[temp], equalLineList[temp1]):
                        newInfo = newInfo1
                    elif Lemmas.check_EQTiangle(newInfo2, equalLineList[temp], equalLineList[temp1]):
                        newInfo = newInfo2
                if flag_HF == 1 and flag_HF_1 == 1:
                    newInfo1 = Informations.EqualTriangle(rightAngleList[i].p1, rightAngleList[i].p2,
                                                          rightAngleList[i].p3,
                                                          rightAngleList[j].p1, rightAngleList[j].p2,
                                                          rightAngleList[j].p3)
                    newInfo2 = Informations.EqualTriangle(rightAngleList[i].p1, rightAngleList[i].p2,
                                                          rightAngleList[i].p3,
                                                          rightAngleList[j].p3, rightAngleList[j].p2,
                                                          rightAngleList[j].p1)
                    if Lemmas.check_EQTiangle_withoneline(newInfo1, equalLineList[temp1]):
                        newInfo = newInfo1
                    elif Lemmas.check_EQTiangle_withoneline(newInfo2, equalLineList[temp1]):
                        newInfo = newInfo2
                if flag_HF == 1 and flag_HF_1 != 1 and flag_HF_1 != 0:
                    newInfo1 = Informations.EqualTriangle(rightAngleList[i].p1, rightAngleList[i].p2,
                                                          rightAngleList[i].p3,
                                                          rightAngleList[j].p1, rightAngleList[j].p2,
                                                          rightAngleList[j].p3)
                    newInfo2 = Informations.EqualTriangle(rightAngleList[i].p1, rightAngleList[i].p2,
                                                          rightAngleList[i].p3,
                                                          rightAngleList[j].p3, rightAngleList[j].p2,
                                                          rightAngleList[j].p1)
                    if Lemmas.check_EQTiangle_withoneline(newInfo1, equalLineList[temp]):
                        newInfo = newInfo1
                    elif Lemmas.check_EQTiangle_withoneline(newInfo2, equalLineList[temp]):
                        newInfo = newInfo2

            if newInfo is not None:
                # 用一个res来存IsInList返回的值
                if flag_HF_1 == 1 or flag_HF_1 == 0:
                    newInfo.conditions.append(
                        ["全等三角形的证明（HL）", rightAngleList[i], rightAngleList[j], equalLineList[temp1]])
                    newInfo.weight = max(rightAngleList[i].weight, rightAngleList[j].weight,
                                         equalLineList[temp1].weight) + 1
                if flag_HF_1 != 1:
                    newInfo.conditions.append(
                        ["全等三角形的证明（HL）", rightAngleList[i], rightAngleList[j], equalLineList[temp]])
                    newInfo.weight = max(rightAngleList[i].weight, rightAngleList[j].weight,
                                         equalLineList[temp].weight) + 1
                res = newInfo.IsInList(equalTriangleList, coLineList)
                if res is False:
                    equalTriangleList.append(newInfo)
                    flag = True
                elif res is True:
                    continue
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

            # if newInfo is not None and newInfo.IsInList(equalTriangleList, coLineList) is False:
            #     # newInfo.source = "全等三角形的证明（HL）"
            #     # newInfo.conditions.append(rightAngleList[i])
            #     # newInfo.conditions.append(["全等三角形的证明（HL）", rightAngleList[i], rightAngleList[j]])
            #     if flag_HF_1 == 1 or flag_HF_1 == 0:
            #         newInfo.conditions.append(["全等三角形的证明（HL）", rightAngleList[i], rightAngleList[j], equalLineList[temp1]])
            #     if flag_HF_1 != 1:
            #         newInfo.conditions.append(["全等三角形的证明（HL）", rightAngleList[i], rightAngleList[j], equalLineList[temp]])
            #     equalTriangleList.append(newInfo)
            #     flag = True
    checkEndlessLoop(flag, "ReasonByLmEqualTriangleHL1")
    return flag


# 有邻边的全等三角形的证明（HL）
# def ReasonByLmEqualTriangleHL2():
#     if len(rightAngleList) < 2 and len(equalLineList) < 2:
#         return False
#     flag = False  # 判断一轮挖掘过程是否生成新的信息，生成即返回True
#
#     for i in range(len(rightAngleList)):
#         # set1是第一个直角三角形的斜边
#         # set1_1、set1_2是第一个直角三角形的两个直角边
#         set1 = set()
#         set1_1 = set()
#         set1_2 = set()
#         set1.update(rightAngleList[i].p1, rightAngleList[i].p3)
#         set1_1.update(rightAngleList[i].p1, rightAngleList[i].p2)
#         set1_2.update(rightAngleList[i].p2, rightAngleList[i].p3)
#         for j in range(i+1, len(rightAngleList)):
#             # set2是第二个直角三角形的斜边
#             # set2_1、set2_2是第二个直角三角形的两个直角边
#             set2 = set()
#             set2_1 = set()
#             set2_2 = set()
#             set2.update(rightAngleList[j].p1, rightAngleList[j].p3)
#             set2_1.update(rightAngleList[j].p1, rightAngleList[j].p2)
#             set2_2.update(rightAngleList[j].p2, rightAngleList[j].p3)
#             flag_HF = 0
#             temp = 0
#             temp1 = 0
#             newInfo = None
#             # 斜边为邻边的情况：
#             if set1 == set2:
#                 flag_HF = 1
#             # 直角边为邻边的情况：
#             elif set1_1 == set2_1:
#                 flag_HF = 2
#             elif set1_1 == set2_2:
#                 flag_HF = 3
#             elif set1_2 == set2_1:
#                 flag_HF = 4
#             elif set1_2 == set2_2:
#                 flag_HF = 5
#             for m in range(len(equalLineList)):
#                 set_m_1 = set()
#                 set_m_2 = set()
#                 set_m_1.update(equalLineList[m].p1, equalLineList[m].p2)
#                 set_m_2.update(equalLineList[m].p3, equalLineList[m].p4)
#                 if (set1 == set_m_1 and set2 == set_m_2) or (set1 == set_m_2 and set2 == set_m_1):
#                     temp = m
#                     flag_HF += 1
#                 if (set1_1 == set_m_1 and set2_1 == set_m_2) or (set1_1 == set_m_2 and set2_1 == set_m_1):
#                     temp1 = m
#                     flag_HF += 1
#                 elif (set1_1 == set_m_1 and set2_2 == set_m_2) or (set1_1 == set_m_2 and set2_2 == set_m_1):
#                     temp1 = m
#                     flag_HF += 1
#                 elif (set1_2 == set_m_1 and set2_1 == set_m_2) or (set1_2 == set_m_2 and set2_1 == set_m_1):
#                     temp1 = m
#                     flag_HF += 1
#                 elif (set1_2 == set_m_1 and set2_2 == set_m_2) or (set1_2 == set_m_2 and set2_2 == set_m_1):
#                     temp1 = m
#                     flag_HF += 1
#                 if flag_HF == 2:
#                     newInfo1 = Informations.EqualTriangle(rightAngleList[i].p1, rightAngleList[i].p2, rightAngleList[i].p3,
#                                                           rightAngleList[j].p1, rightAngleList[j].p2, rightAngleList[j].p3)
#                     newInfo2 = Informations.EqualTriangle(rightAngleList[i].p1, rightAngleList[i].p2, rightAngleList[i].p3,
#                                                           rightAngleList[j].p3, rightAngleList[j].p2, rightAngleList[j].p1)
#                     if Lemmas.check_EQTiangle(newInfo1, equalLineList[temp], equalLineList[temp1]):
#                         newInfo = newInfo1
#                     elif Lemmas.check_EQTiangle(newInfo2, equalLineList[temp], equalLineList[temp1]):
#                         newInfo = newInfo2
#             if newInfo is not None and newInfo.IsInList(equalTriangleList, coLineList) == False:
#                 newInfo.source = "全等三角形的证明（HL）"
#                 newInfo.conditions.append(rightAngleList[i])
#                 newInfo.conditions.append(rightAngleList[j])
#                 newInfo.conditions.append(equalLineList[temp])
#                 newInfo.conditions.append(equalLineList[temp1])
#                 equalTriangleList.append(newInfo)
#                 flag = True
#     checkEndlessLoop(flag, "ReasonByLmEqualTriangleHL2")
#     return flag

# 全等三角形推出三边相等以及三角相等
def ReasonByLmEqualTriangle_reverse():
    # 当对应链表中元素小于2，则没法推理，直接返回
    if len(equalLineList) < 1 and len(equalAngleList) < 1 and len(equalTriangleList) < 1:
        return False
    flag1 = flag2 = False  # 判断一轮挖掘过程是否生成新的信息，生成即返回True

    # for i in range(len(equalTriangleList)):
    #     for j in range(len(equalLineList)):
    #         newInfo = Lemmas.LmEqualTriangle_reverseAngle.Infer(equalTriangleList[i], equalLineList[j])
    #         # 在加入链表之前，要判断链表中是否已有相同信息；若相同则不添加
    #         if newInfo != None and newInfo.IsInList(equalAngleList, coLineList) == False:
    #             equalAngleList.append(newInfo)
    #             flag1 = True
    #     for m in range(len(equalLineList)):
    #         newInfo = Lemmas.LmEqualTriangle_reverseLine.Infer(equalTriangleList[i], equalAngleList[m])
    #         # 在加入链表之前，要判断链表中是否已有相同信息；若相同则不添加
    #         if newInfo != None and newInfo.IsInList(equalLineList) == False:
    #             equalLineList.append(newInfo)
    #             flag2 = True
    for i in range(len(equalTriangleList)):
        flag1 = Lemmas.LmEqualTriangleGetAngle.Infer(equalTriangleList[i], equalAngleList, coLineList)
        flag2 = Lemmas.LmEqualTriangleGetLine.Infer(equalTriangleList[i], equalLineList)
    flag = flag1 or flag2
    checkEndlessLoop(flag, "ReasonByLmEqualTriangle_reverse")
    return flag


# 基于中位线定理，对中点信息进行推理
def ReasonByLmMedianLine():
    # 当对应链表中元素小于2，则没法推理，直接返回
    if len(midPointList) < 2:
        return False
    flag = False  # 判断一轮挖掘过程是否生成新的信息，生成即返回True
    for i in range(len(midPointList)):
        for j in range(i + 1, len(midPointList)):
            flag = Lemmas.LmMedianLine.Infer(midPointList[i], midPointList[j], parallelLineList, ratioLineList)

    checkEndlessLoop(flag, "ReasonByLmMedianLine")
    return flag


# 成比例线段的传递性
def ReasonByLmRatioLineGetMore():
    # 当对应链表中元素小于2，则没法推理，直接返回
    if len(ratioLineList) < 2:
        return False
    flag = False  # 判断一轮挖掘过程是否生成新的信息，生成即返回True
    for i in range(len(ratioLineList)):
        for j in range(i + 1, len(ratioLineList)):
            flag = Lemmas.LmRatioLineGetMore.Infer(ratioLineList[i], ratioLineList[j], ratioLineList, equalLineList)

    checkEndlessLoop(flag, "ReasonByLmMedianLine")
    return flag


# 成比例角的传递性
def ReasonByLmRatioAngleGetMore():
    # 当对应链表中元素小于2，则没法推理，直接返回
    if len(ratioAngleList) < 2:
        return False
    flag = False  # 判断一轮挖掘过程是否生成新的信息，生成即返回True
    for i in range(len(ratioAngleList)):
        for j in range(i + 1, len(ratioAngleList)):
            flag = Lemmas.LmRatioAngleGetMore.Infer(ratioAngleList[i], ratioAngleList[j], ratioAngleList,
                                                    equalAngleList, coLineList)

    checkEndlessLoop(flag, "ReasonByLmRatioAngleGetMore")
    return flag


# 平行四边形对边有中点，推出四条小边平行且相等
# def ReasonByLmparallogram_Oppo_Midpoint():
#     # 当对应链表中元素小于2，则没法推理，直接返回
#     if len(midPointList) < 2 and len(parallogramList) < 1:
#         return False
#     flag = False  # 判断一轮挖掘过程是否生成新的信息，生成即返回True
#     for i in range(len(midPointList)):
#         for j in range(i + 1, len(midPointList)):
#             for m in range(len(parallogramList)):
#                 flag = Lemmas.Lmparallogram_Oppo_Midpoint.Infer(midPointList[i], midPointList[j], parallogramList[m],
#                                                                 equalLineList, parallelLineList)
#                 if flag:
#                     return flag
#     return flag

# 三角形的三个角之和为180°
def ReasonByLmTriangle180():
    # 当对应链表中元素小于2，则没法推理，直接返回
    if len(angleList) < 2:
        return False
    flag = False  # 判断一轮挖掘过程是否生成新的信息，生成即返回True
    for i in range(len(angleList)):
        for j in range(i + 1, len(angleList)):
            newInfo = None
            set1 = set()
            set2 = set()
            set1.update(angleList[i].p1, angleList[i].p2, angleList[i].p3)
            set2.update(angleList[j].p1, angleList[j].p2, angleList[j].p3)
            if set1 == set2:
                if angleList[i].p1 != angleList[j].p2:
                    newInfo = Informations.Angle(angleList[i].p2, angleList[i].p1, angleList[j].p2,
                                                 180 - angleList[i].p4 - angleList[j].p4)
                elif angleList[i].p3 != angleList[j].p2:
                    newInfo = Informations.Angle(angleList[i].p2, angleList[i].p3, angleList[j].p2,
                                                 180 - angleList[i].p4 - angleList[j].p4)
                if newInfo is not None:
                    # 用一个res来存IsInList返回的值
                    newInfo.conditions.append(["三角形内角和为180°", angleList[i], angleList[j]])
                    res = newInfo.IsInList(angleList)
                    newInfo.weight = max(angleList[i].weight, angleList[j].weight) + 1
                    if res is False:
                        angleList.append(newInfo)
                        flag = True
                    elif res is True:
                        continue
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


# 基于中点分割出两条相等边公理，对中点信息进行推理
# 中点推出共线
def ReasonByLmMidPoint_EqualLine():
    if len(midPointList) < 1:
        return False

    flag1 = flag2 = flag3 = flag4 = False
    for i in range(len(midPointList)):
        newInfo = Lemmas.LmMidPoint_EqualLine.Infer(midPointList[i])
        # 在加入链表之前，要判断链表中是否已有相同信息；若相同则不添加
        if newInfo is not None:
            # 用一个res来存IsInList返回的值
            res = newInfo.IsInList(equalLineList)
            newInfo.weight = midPointList[i].weight
            if res is False:
                equalLineList.append(newInfo)
                flag1 = True
            elif res is True:
                continue
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

        newInfo_coline = Informations.CoLine(midPointList[i].p1, midPointList[i].p2, midPointList[i].p3, 1)
        # 在加入链表之前，要判断链表中是否已有相同信息；若相同则不添加
        if newInfo_coline is not None:
            # 用一个res来存IsInList返回的值
            newInfo_coline.conditions.append(["中点与剩余两点共线", midPointList[i]])
            res = newInfo_coline.IsInList(coLineList)
            newInfo_coline.weight = midPointList[i].weight + 1
            if res is False:
                coLineList.append(newInfo_coline)
                flag2 = True
            elif res is True:
                continue
            else:
                nums = len(coLineList[res].conditions)
                for item in coLineList[res].conditions:
                    if len(item) != len(newInfo_coline.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo_coline.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    coLineList[res].conditions.append(newInfo_coline.conditions[-1])
                coLineList[res].weight = min(newInfo_coline.weight, coLineList[res].weight)

        newInfo_ratio_1 = Informations.RatioLine(midPointList[i].p1, midPointList[i].p2, midPointList[i].p2,
                                                 midPointList[i].p3, 1, 2)
        newInfo_ratio_2 = Informations.RatioLine(midPointList[i].p1, midPointList[i].p3, midPointList[i].p2,
                                                 midPointList[i].p3, 1, 2)
        if newInfo_ratio_1 is not None:
            # 用一个res来存IsInList返回的值
            newInfo_ratio_1.conditions.append(["中点平分线段", midPointList[i]])
            res = newInfo_ratio_1.IsInList(ratioLineList)
            newInfo_ratio_1.weight = midPointList[i].weight + 1
            if res is False:
                ratioLineList.append(newInfo_ratio_1)
                flag3 = True
            elif res is True:
                continue
            else:
                nums = len(ratioLineList[res].conditions)
                for item in ratioLineList[res].conditions:
                    if len(item) != len(newInfo_ratio_1.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo_ratio_1.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    ratioLineList[res].conditions.append(newInfo_ratio_1.conditions[-1])
                ratioLineList[res].weight = min(newInfo_ratio_1.weight, ratioLineList[res].weight)

        if newInfo_ratio_2 is not None:
            # 用一个res来存IsInList返回的值
            newInfo_ratio_2.conditions.append(["中点平分线段", midPointList[i]])
            res = newInfo_ratio_2.IsInList(ratioLineList)
            newInfo_ratio_2.weight = midPointList[i].weight + 1
            if res is False:
                ratioLineList.append(newInfo_ratio_2)
                flag4 = True
            elif res is True:
                continue
            else:
                nums = len(ratioLineList[res].conditions)
                for item in ratioLineList[res].conditions:
                    if len(item) != len(newInfo_ratio_2.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo_ratio_2.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    ratioLineList[res].conditions.append(newInfo_ratio_2.conditions[-1])
                ratioLineList[res].weight = min(newInfo_ratio_2.weight, ratioLineList[res].weight)

    flag = flag1 or flag2 or flag3 or flag4
    checkEndlessLoop(flag, "ReasonByLmMidPoint_EqualLine")
    return flag


# 直角三角形斜边中线定理
def ReasonByLmRTriangleMidLine():
    if len(rightAngleList) < 1 and len(midPointList) < 1:
        return False

    flag1 = flag2 = flag3 = False
    for i in range(len(rightAngleList)):
        for j in range(len(midPointList)):
            set1 = set()
            set2 = set()
            set1.update(rightAngleList[i].p1, rightAngleList[i].p3)
            set2.update(midPointList[j].p2, midPointList[j].p3)
            if set1 == set2:
                newInfo1 = Informations.EqualLine(midPointList[j].p1, rightAngleList[i].p2, midPointList[j].p1,
                                                  rightAngleList[i].p1)
                newInfo2 = Informations.EqualLine(midPointList[j].p1, rightAngleList[i].p2, midPointList[j].p1,
                                                  rightAngleList[i].p3)
                newInfo3 = Informations.RatioLine(midPointList[j].p1, rightAngleList[i].p2, midPointList[j].p2,
                                                  midPointList[j].p3, 1, 2)
                # 在加入链表之前，要判断链表中是否已有相同信息；若相同则不添加
                if newInfo1 is not None:
                    # 用一个res来存IsInList返回的值
                    newInfo1.conditions.append(["直角三角形斜边中线定理", rightAngleList[i], midPointList[j]])
                    res = newInfo1.IsInList(equalLineList)
                    newInfo1.weight = max(rightAngleList[i].weight, midPointList[j].weight) + 1
                    if res is False:
                        equalLineList.append(newInfo1)
                        flag1 = True
                    elif res is True:
                        continue
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
                    newInfo2.conditions.append(["直角三角形斜边中线定理", rightAngleList[i], midPointList[j]])
                    res = newInfo2.IsInList(equalLineList)
                    newInfo2.weight = max(rightAngleList[i].weight, midPointList[j].weight) + 1
                    if res is False:
                        equalLineList.append(newInfo2)
                        flag2 = True
                    elif res is True:
                        continue
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

                if newInfo3 is not None:
                    # 用一个res来存IsInList返回的值
                    newInfo3.conditions.append(["直角三角形斜边中线定理", rightAngleList[i], midPointList[j]])
                    res = newInfo3.IsInList(ratioLineList)
                    newInfo3.weight = max(rightAngleList[i].weight, midPointList[j].weight) + 1
                    if res is False:
                        ratioLineList.append(newInfo3)
                        flag3 = True
                    elif res is True:
                        continue
                    else:
                        nums = len(ratioLineList[res].conditions)
                        for item in ratioLineList[res].conditions:
                            if len(item) != len(newInfo3.conditions[-1]):
                                nums -= 1
                                continue
                            else:
                                for list_no in range(len(item)):
                                    if item[list_no] != newInfo3.conditions[-1][list_no]:
                                        nums -= 1
                                        break
                        if nums == 0:
                            ratioLineList[res].conditions.append(newInfo3.conditions[-1])
                        ratioLineList[res].weight = min(newInfo3.weight, ratioLineList[res].weight)
    flag = flag1 or flag2 or flag3
    checkEndlessLoop(flag, "ReasonByLmRTriangleMidLine")
    return flag


# 直角三角形斜边中线定理   逆定理
def ReasonByLmReRTriangleMidLine():
    if len(equalLineList) < 1 and len(midPointList) < 1:
        return False

    flag = False
    newInfo = None
    for item1 in midPointList:
        set1 = set()
        set2 = set()
        set_check = set()
        set1.update(item1.p1, item1.p2)
        set2.update(item1.p1, item1.p3)
        set_check.add(item1.p1)
        for item2 in equalLineList:
            newInfo = None
            set3 = set()
            set4 = set()
            set3.update(item2.p1, item2.p2)
            set4.update(item2.p3, item2.p4)
            if set1 == set3 and set2 != set4 and len(set4 & set_check) == 1:
                if item2.p3 != item1.p1:
                    temp = item2.p3
                else:
                    temp = item2.p4
                newInfo = Informations.VerticalLine(item1.p2, temp, item1.p3, temp, pointList, temp)
            elif set1 == set4 and set2 != set3 and len(set3 & set_check) == 1:
                if item2.p1 != item1.p1:
                    temp = item2.p1
                else:
                    temp = item2.p2
                newInfo = Informations.VerticalLine(item1.p2, temp, item1.p3, temp, pointList, temp)
            elif set2 == set3 and set1 != set4 and len(set4 & set_check) == 1:
                if item2.p3 != item1.p1:
                    temp = item2.p3
                else:
                    temp = item2.p4
                newInfo = Informations.VerticalLine(item1.p2, temp, item1.p3, temp, pointList, temp)
            elif set2 == set4 and set1 != set3 and len(set3 & set_check) == 1:
                if item2.p1 != item1.p1:
                    temp = item2.p1
                else:
                    temp = item2.p2
                newInfo = Informations.VerticalLine(item1.p2, temp, item1.p3, temp, pointList, temp)
            # 在加入链表之前，要判断链表中是否已有相同信息；若相同则不添加
            if newInfo is not None:
                # 用一个res来存IsInList返回的值
                newInfo.conditions.append(["三角形斜边上的中点等于斜边的一半，这个三角形是直角三角形", item1, item2])
                res = newInfo.IsInList(verticalLineList)
                newInfo.weight = max(item1.weight, item2.weight) + 1
                if res is False:
                    verticalLineList.append(newInfo)
                    flag = True
                elif res is True:
                    continue
                else:
                    nums = len(verticalLineList[res].conditions)
                    for item in verticalLineList[res].conditions:
                        if len(item) != len(newInfo.conditions[-1]):
                            nums -= 1
                            continue
                        else:
                            for list_no in range(len(item)):
                                if item[list_no] != newInfo.conditions[-1][list_no]:
                                    nums -= 1
                                    break
                    if nums == 0:
                        verticalLineList[res].conditions.append(newInfo.conditions[-1])
                    verticalLineList[res].weight = min(newInfo.weight, verticalLineList[res].weight)
    checkEndlessLoop(flag, "ReasonByLmReRTriangleMidLine")
    return flag


# 基于相等线的传递性公理，对相等线信息进行推理
def ReasonByLmEqualLineTransitivity():
    # 当对应链表中元素小于2，则没法推理，直接返回
    if len(equalLineList) < 2:
        return False
    flag = False
    for i in range(len(equalLineList)):
        for j in range(i + 1, len(equalLineList)):

            newInfo = Lemmas.LmEqualLineTransitivity.Infer(equalLineList[i], equalLineList[j])
            # 在加入链表之前，要判断链表中是否已有相同信息；若相同则不添加
            if newInfo is not None:
                # 用一个res来存IsInList返回的值
                res = newInfo.IsInList(equalLineList)
                newInfo.weight = max(equalLineList[i].weight, equalLineList[j].weight) + 1
                if res is False:
                    equalLineList.append(newInfo)
                    flag = True
                elif res is True:
                    continue
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
    checkEndlessLoop(flag, "ReasonByLmEqualLineTransitivity")
    return flag


# 基于相等角的传递性公理，对相等角信息进行推理
def ReasonByLmEqualAngleTransitivity():
    # 当对应链表中元素小于2，则没法推理，直接返回
    if len(equalAngleList) < 2:
        return False
    flag = False
    for i in range(len(equalAngleList)):
        for j in range(i + 1, len(equalAngleList)):
            flag = Lemmas.LmEqualAngleTransitivity.Infer(equalAngleList[i], equalAngleList[j], equalAngleList,
                                                         coLineList)
            # 在加入链表之前，要判断链表中是否已有相同信息；若相同则不添加
    checkEndlessLoop(flag, "ReasonByLmEqualAngleTransitivity")

    return flag


# 基于平行线传递性公理，对平行信息进行推理
def ReasonByLmParallalTransitivity():
    # 当对应链表中元素小于2，则没法推理，直接返回
    if len(parallelLineList) < 2:
        return False
    # print("mymain检查点21")
    flag = False
    for i in range(len(parallelLineList)):
        for j in range(i + 1, len(parallelLineList)):

            newInfo = Lemmas.LmParallalTransitivity.Infer(parallelLineList[i], parallelLineList[j])

            # 在加入链表之前，要判断链表中是否已有相同信息；若相同则不添加
            if newInfo is not None:
                # 用一个res来存IsInList返回的值
                res = newInfo.IsInList(parallelLineList)
                newInfo.weight = max(parallelLineList[i].weight, parallelLineList[j].weight) + 1
                if res is False:
                    parallelLineList.append(newInfo)
                    flag = True
                elif res is True:
                    continue
                else:
                    nums = len(parallelLineList[res].conditions)
                    for item in parallelLineList[res].conditions:
                        if len(item) != len(newInfo.conditions[-1]):
                            nums -= 1
                            continue
                        else:
                            for list_no in range(len(item)):
                                if item[list_no] != newInfo.conditions[-1][list_no]:
                                    nums -= 1
                                    break
                    if nums == 0:
                        parallelLineList[res].conditions.append(newInfo.conditions[-1])
                    parallelLineList[res].weight = min(newInfo.weight, parallelLineList[res].weight)
    checkEndlessLoop(flag, "ReasonByLmParallalTransitivity")
    return flag


# 基于两对边平行的四边形是平行四边形这一公理，对平行信息进行推理
def ReasonByLmParallelogramaDetermination1():
    # 当对应链表中元素小于2，则没法推理，直接返回
    if len(parallelLineList) < 2:
        return False
    # print("mymain检查点31")
    flag = False
    for i in range(len(parallelLineList)):
        for j in range(i + 1, len(parallelLineList)):
            newInfo = Lemmas.LmParallelogramaDetermination1.Infer(parallelLineList[i], parallelLineList[j])
            # 在加入链表之前，要判断链表中是否已有相同信息；若相同则不添加
            if newInfo is not None:
                # 用一个res来存IsInList返回的值
                res = newInfo.IsInList(parallogramList)
                newInfo.weight = max(parallelLineList[i].weight, parallelLineList[j].weight) + 1
                if res is False:
                    parallogramList.append(newInfo)
                    flag = True
                elif res is True:
                    continue
                else:
                    nums = len(parallogramList[res].conditions)
                    for item in parallogramList[res].conditions:
                        if len(item) != len(newInfo.conditions[-1]):
                            nums -= 1
                            continue
                        else:
                            for list_no in range(len(item)):
                                if item[list_no] != newInfo.conditions[-1][list_no]:
                                    nums -= 1
                                    break
                    if nums == 0:
                        parallogramList[res].conditions.append(newInfo.conditions[-1])
                    parallogramList[res].weight = min(newInfo.weight, parallogramList[res].weight)
    checkEndlessLoop(flag, "ReasonByLmParallelogramaDetermination1")
    return flag


# 基于一对边平行且相等的四边形是平行四边形这一公理，对平行信息进行推理
def ReasonByLmParallelogramaDetermination2():
    # 当平行列表中元素小于1或者相等线集合中元素小于1，则没法推理，直接返回
    if len(parallelLineList) < 1 or len(equalLineList) < 1:
        return False
    # print("mymain检查点41")
    flag = False
    for i in range(len(parallelLineList)):
        for j in range(len(equalLineList)):
            newInfo = Lemmas.LmParallelogramaDetermination2.Infer(parallelLineList[i], equalLineList[j], pointList)
            # 在加入链表之前，要判断链表中是否已有相同信息；若相同则不添加
            if newInfo is not None:
                # 用一个res来存IsInList返回的值
                res = newInfo.IsInList(parallogramList)
                newInfo.weight = max(parallelLineList[i].weight, equalLineList[j].weight) + 1
                if res is False:
                    parallogramList.append(newInfo)
                    flag = True
                elif res is True:
                    continue
                else:
                    nums = len(parallogramList[res].conditions)
                    for item in parallogramList[res].conditions:
                        if len(item) != len(newInfo.conditions[-1]):
                            nums -= 1
                            continue
                        else:
                            for list_no in range(len(item)):
                                if item[list_no] != newInfo.conditions[-1][list_no]:
                                    nums -= 1
                                    break
                    if nums == 0:
                        parallogramList[res].conditions.append(newInfo.conditions[-1])
                    parallogramList[res].weight = min(newInfo.weight, parallogramList[res].weight)
    checkEndlessLoop(flag, "ReasonByLmParallelogramaDetermination2")
    return flag


# 平行四边形推理出新信息
def ReasoningByLmParallogramGetLineParall():
    if len(parallogramList) == 0:
        return False
    flag1 = flag2 = flag3 = flag4 = False
    # 平行四边形得到对边平行且相等
    for i in range(len(parallogramList)):
        flag1 = Lemmas.LmParallogramGetLineParall.Infer(parallogramList[i], equalLineList, parallelLineList)
    # 平行四边形得到内错角相等
    for i in range(len(parallogramList)):
        flag2 = Lemmas.LmParallogramGetneiangle.Infer(parallogramList[i], equalAngleList, coLineList)
    # 平行四边形得到对角相等
    for i in range(len(parallogramList)):
        flag3 = Lemmas.LmParallogramGetduiangle.Infer(parallogramList[i], equalAngleList, coLineList)
    # 平行四边形的两条对角线相互平分
    if len(coLineList) > 1:
        for i in range(len(parallogramList)):
            set1 = set()
            set1.update(parallogramList[i].p1, parallogramList[i].p2, parallogramList[i].p3, parallogramList[i].p4)
            for m in range(len(coLineList)):
                if coLineList[m].check == 1:
                    for n in range(m + 1, len(coLineList)):
                        if coLineList[n].check == 1:
                            if coLineList[m].p1 == coLineList[n].p1:
                                set2 = set()
                                set2.update(coLineList[n].p2, coLineList[n].p3, coLineList[m].p2, coLineList[m].p3)
                                if set1 == set2:
                                    flag4 = Lemmas.LmParallogramGetduiLine.Infer(coLineList[m], coLineList[n],
                                                                                 midPointList, parallogramList[i])
    flag = flag1 or flag2 or flag3 or flag4
    checkEndlessLoop(flag, "ReasoningByLmParallogramGetLineParall")
    return flag


# 垂直推出直角、共线
def ReasonByLmVertiGetRiangleAndCoLine():
    if len(verticalLineList) == 0:
        return False

    flag1 = flag2 = False
    for i in range(len(verticalLineList)):
        flag1 = Lemmas.LmVertiGetRiangle.Infer(verticalLineList[i], rightAngleList)
    for i in range(len(verticalLineList)):
        flag2 = Lemmas.LmVertiGetCoLine.Infer(verticalLineList[i], coLineList)
    flag = flag1 or flag2
    checkEndlessLoop(flag, "ReasonByLmVertiGetRiangleAndCoLine")
    return flag


# 共线传递
def ReasonByLmCoLineGetCoLine():
    if len(coLineList) < 2:
        return False

    flag = False
    for i in range(len(coLineList)):
        for j in range(i + 1, len(coLineList)):
            flag = Lemmas.LmCoLineGetCoLine.Infer(coLineList[i], coLineList[j], coLineList)

    checkEndlessLoop(flag, "ReasonByLmCoLineGetCoLine")
    return flag


# 确定共线的顺序
def check_coLine():
    if len(coLineList) < 1:
        return False
    flag = False
    for i in coLineList:
        if i.check == 1:
            continue
        pos_1 = pos_2 = pos_3 = None
        for j in pointList:
            if i.p1 == j.p1:
                pos_1 = j.position
            elif i.p2 == j.p1:
                pos_2 = j.position
            elif i.p3 == j.p1:
                pos_3 = j.position
        if coline_is_ordered(pos_1, pos_2, pos_3):
            i.check = 1
            flag = True
            # i.printSelf()
        elif coline_is_ordered(pos_1, pos_3, pos_2):
            temp = i.p2
            i.p2 = i.p3
            i.p3 = temp
            i.check = 1
            flag = True
            # i.printSelf()
        elif coline_is_ordered(pos_2, pos_1, pos_3):
            temp = i.p1
            i.p1 = i.p2
            i.p2 = temp
            i.check = 1
            flag = True
            # i.printSelf()
    checkEndlessLoop(flag, "check_coLine")
    return flag


# 确定垂直交点的顺序
def check_vertical():
    if len(verticalLineList) < 1:
        return False
    flag = False
    for i in verticalLineList:
        if i.p5 != "#":
            continue
        # 先用点的名字排除
        p = set()
        p.update(i.p1, i.p2, i.p3, i.p4)
        if len(p) == 3:
            if i.p1 == i.p2 or i.p1 == i.p3 or i.p1 == i.p4:
                i.p5 = i.p1
            if i.p2 == i.p1 or i.p2 == i.p3 or i.p2 == i.p4:
                i.p5 = i.p2
            if i.p3 == i.p1 or i.p3 == i.p2 or i.p3 == i.p4:
                i.p5 = i.p3
            if i.p4 == i.p1 or i.p4 == i.p2 or i.p4 == i.p3:
                i.p5 = i.p4
        else:
            # 再用点的坐标排除
            pos_1 = pos_2 = pos_3 = pos_4 = None
            for j in pointList:
                if i.p1 == j.p1:
                    pos_1 = j.position
                elif i.p2 == j.p1:
                    pos_2 = j.position
                elif i.p3 == j.p1:
                    pos_3 = j.position
                elif i.p4 == j.p1:
                    pos_4 = j.position
            r = calculate_intersection(pos_1, pos_2, pos_3, pos_4)
            for j in pointList:
                if -1 < j.position[0] - r[0] < 1 and -1 < j.position[1] - r[1] < 1:
                    i.p5 = j.p1
    checkEndlessLoop(flag, "check_coLine")
    return flag


def calculate_intersection(point1, point2, point3, point4):
    # 提取端点坐标
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    x4, y4 = point4

    # 处理斜率为无穷大的情况
    if x1 == x2:
        # 第一条线段垂直于 x 轴
        m2 = (y4 - y3) / (x4 - x3) if x4 != x3 else None
        if m2 is not None:
            b2 = y3 - m2 * x3
            # 交点的 x 坐标就是第一条线段的 x 坐标
            x = x1
            y = m2 * x + b2
        else:
            return None
    elif x3 == x4:
        # 第二条线段垂直于 x 轴
        m1 = (y2 - y1) / (x2 - x1)
        b1 = y1 - m1 * x1
        # 交点的 x 坐标就是第二条线段的 x 坐标
        x = x3
        y = m1 * x + b1
    else:
        # 计算两条线段的斜率和截距
        m1 = (y2 - y1) / (x2 - x1)
        b1 = y1 - m1 * x1
        m2 = (y4 - y3) / (x4 - x3)
        b2 = y3 - m2 * x3

        # 检查两条线段是否垂直
        if abs(m1 * m2 + 1) > 1e-9:
            return None

        # 联立方程求解交点
        x = (b2 - b1) / (m1 - m2)
        y = m1 * x + b1

    # 检查交点是否在线段上
    if (min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2) and
            min(x3, x4) <= x <= max(x3, x4) and min(y3, y4) <= y <= max(y3, y4)):
        return (x, y)
    else:
        return None


# 确定共线顺序的工具函数
def coline_is_ordered(point_a, point_b, point_c):
    x_a, y_a = point_a
    x_b, y_b = point_b
    x_c, y_c = point_c
    flag = False
    diff_abx = abs(x_a - x_b)
    diff_acx = abs(x_a - x_c)
    diff_bcx = abs(x_b - x_c)
    diff_aby = abs(y_a - y_b)
    diff_acy = abs(y_a - y_c)
    diff_bcy = abs(y_b - y_c)
    # 如果三点平行于水平面（消除误差）：
    if diff_abx < 10 and diff_acx < 10 and diff_bcx < 10:
        if y_b <= y_a <= y_c or y_b >= y_a >= y_c:
            flag = True
    # 如果三点垂直于水平面（消除误差）：
    elif diff_aby < 10 and diff_acy < 10 and diff_bcy < 10:
        if x_b <= x_a <= x_c or x_b >= x_a >= x_c:
            flag = True
    # 既不垂直也不平行于水平面
    else:
        if x_b <= x_a <= x_c:
            if y_b <= y_a <= y_c or y_b >= y_a >= y_c:
                flag = True
        elif x_b >= x_a >= x_c:
            if y_b <= y_a <= y_c or y_b >= y_a >= y_c:
                flag = True
    return flag


# 三点共线推出垂直、平行、相等角和对顶角互补角，实际上是同一个线段.VPA是垂直、平行、相等角的缩写
def ReasoningByLmCoLineGetVPA():
    if len(verticalLineList) == 0 and len(parallelLineList) == 0 and len(equalAngleList) == 0:
        return False
    flag1 = flag2 = flag3 = flag4 = False
    for i in range(len(coLineList)):
        # 三点共线推出垂直
        flag1 = Lemmas.LmCoLineGetVertical.Infer(coLineList[i], verticalLineList, pointList)
        # 三点共线推出平行
        flag2 = Lemmas.LmCoLineGetParallel.Infer(coLineList[i], parallelLineList)
        # 三点共线推出相等角、互补角
        if coLineList[i].check == 1:
            flag4 = Lemmas.LmCoLineGetAngle.Infer(coLineList[i], equalAngleList, complementaryAngleList, coLineList)
    # 三点共线推出相等角和对顶角、互补角
    for k in range(len(coLineList)):
        if coLineList[k].check == 1:
            for m in range(k + 1, len(coLineList)):
                # 两条线段自身的对顶角、互补角
                if coLineList[m].check == 1:
                    set1 = set()
                    set1.update(coLineList[k].p1, coLineList[k].p2, coLineList[k].p3, coLineList[m].p1,
                                coLineList[m].p2, coLineList[m].p3)
                    if len(set1) != 5:
                        continue
                    set2 = set()
                    set2.update(coLineList[k].p2, coLineList[k].p3, coLineList[m].p2, coLineList[m].p3)
                    # 情况一：共同点是两个线段的中间点,会有两对对顶角和四对互补角
                    if coLineList[k].p1 == coLineList[m].p1:
                        flag3 = Lemmas.LmCoLineGetComplementaryAngle_1.Infer(coLineList[k], coLineList[m],
                                                                             complementaryAngleList, equalAngleList,
                                                                             coLineList)
                    # 情况二：共同点是一个线段的中间点和另一个线段的边点，会有两对相等角和四对互补角
                    elif coLineList[k].p1 != coLineList[m].p1 and len(set2) == 4:
                        flag3 = Lemmas.LmCoLineGetComplementaryAngle_2.Infer(coLineList[k], coLineList[m],
                                                                             complementaryAngleList, equalAngleList,
                                                                             coLineList)
                    # 情况三：共同点是两个线段的边点，只有六对相等角
                    elif coLineList[k].p1 != coLineList[m].p1 and len(set2) == 3:
                        flag3 = Lemmas.LmCoLineGetComplementaryAngle_3.Infer(coLineList[k], coLineList[m],
                                                                             equalAngleList, coLineList)
    flag = flag1 or flag2 or flag3 or flag4
    checkEndlessLoop(flag, "ReasoningByLmCoLineGetVPA")
    return flag


# 正方形的性质
def ReasoningByLmSquare():
    if len(squareList) == 0:
        return False
    flag1 = flag2 = flag3 = flag4 = flag5 = False
    # 正方形得到平行四边形的性质
    for i in range(len(squareList)):
        newInfo = Informations.Parallogram(squareList[i].p1, squareList[i].p2, squareList[i].p3, squareList[i].p4)
        if newInfo is not None:
            # 用一个res来存IsInList返回的值
            newInfo.conditions.append(["正方形是特殊的平行四边形", squareList[i]])
            res = newInfo.IsInList(parallogramList)
            newInfo.weight = squareList[i].weight + 1
            if res is False:
                parallogramList.append(newInfo)
                flag1 = True
            elif res is True:
                continue
            else:
                nums = len(parallogramList[res].conditions)
                for item in parallogramList[res].conditions:
                    if len(item) != len(newInfo.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    parallogramList[res].conditions.append(newInfo.conditions[-1])
                parallogramList[res].weight = min(newInfo.weight, parallogramList[res].weight)
    # 正方形得四对邻边垂直、一对对角线垂直平分
    for j in range(len(squareList)):
        Aux = None
        if squareList[j].IsInList(alreadySquareList) is False:
            Aux = StaticAuxPoint.get_next()
            print("作正方形", squareList[j].p1, squareList[j].p2, squareList[j].p3, squareList[j].p4,
                  "对角线的交点，交于", Aux, "点")
            alreadySquareList.append(squareList[j])
            flag2 = Lemmas.LmSquareGetVertical.Infer(squareList[j], verticalLineList, Aux, midPointList, pointList)
    # 正方形得到内错角为45°
    for k in range(len(squareList)):
        flag3 = Lemmas.LmSquareGetneiangle45.Infer(squareList[k], angleList)
    # 正方形得到邻边相等、对角线相等
    for m in range(len(squareList)):
        flag4 = Lemmas.LmSquareGetLineEQ.Infer(squareList[m], equalLineList)
        newInfo1 = Informations.EqualLine(squareList[m].p1, squareList[m].p3, squareList[m].p2, squareList[m].p4)
        if newInfo1 is not None:
            # 用一个res来存IsInList返回的值
            newInfo1.conditions.append(["正方形的对角线相等", squareList[m]])
            res = newInfo1.IsInList(equalLineList)
            newInfo1.weight = squareList[m].weight + 1
            if res is False:
                equalLineList.append(newInfo1)
                flag5 = True
            elif res is True:
                continue
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
    flag = flag1 or flag2 or flag3 or flag4 or flag5
    checkEndlessLoop(flag, "ReasoningByLmSquare")
    return flag


# 矩形的性质
def ReasoningByLmRectangle():
    if len(rectangleList) == 0:
        return False
    flag1 = flag2 = False
    # 矩形得到平行四边形的性质
    for i in range(len(rectangleList)):
        newInfo = Informations.Parallogram(rectangleList[i].p1, rectangleList[i].p2, rectangleList[i].p3,
                                           rectangleList[i].p4)
        if newInfo is not None:
            # 用一个res来存IsInList返回的值
            newInfo.conditions.append(["矩形是特殊的平行四边形", rectangleList[i]])
            res = newInfo.IsInList(parallogramList)
            newInfo.weight = rectangleList[i].weight + 1
            if res is False:
                parallogramList.append(newInfo)
                flag1 = True
            elif res is True:
                continue
            else:
                nums = len(parallogramList[res].conditions)
                for item in parallogramList[res].conditions:
                    if len(item) != len(newInfo.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    parallogramList[res].conditions.append(newInfo.conditions[-1])
                parallogramList[res].weight = min(newInfo.weight, parallogramList[res].weight)
    # 矩形得四对邻边垂直
    for j in range(len(rectangleList)):
        flag2 = Lemmas.LmRectangleGetVertical.Infer(rectangleList[j], verticalLineList, pointList)
    flag = flag1 or flag2
    checkEndlessLoop(flag, "ReasoningByLmRectangle")
    return flag


# 直角推出90°
def ReasonByLmRiangleGet90():
    if len(rightAngleList) == 0:
        return False

    flag = False
    for i in range(len(rightAngleList)):
        flag = Lemmas.LmRiangleGet90.Infer(rightAngleList[i], angleList)
    checkEndlessLoop(flag, "ReasonByLmRiangleGet90")
    return flag


# 角度相等的角相等、具体角之间推互补、互余
def ReasonByLmAngleNumEQ():
    if len(angleList) < 2:
        return False
    flag = False
    for i in range(len(angleList)):
        for j in range(i + 1, len(angleList)):
            flag = Lemmas.LmAngleNumEQ.Infer(angleList[i], angleList[j], equalAngleList, complementaryAngleList,
                                             coterminalAngleList, coLineList)
    checkEndlessLoop(flag, "ReasonByLmAngleNumEQ")
    return flag


# 等边三角形的性质
def ReasonByLmRegularTriang():
    if len(regularTriangList) < 1:
        return False

    flag = flag1 = flag2 = False
    # 等边三角形得到三个角为60°
    for i in range(len(regularTriangList)):
        flag1 = Lemmas.LmRegularTriangGetAngle.Infer(regularTriangList[i], angleList)
    # 等边三角形得到三个边分别相等
    for i in range(len(regularTriangList)):
        flag2 = Lemmas.LmRegularTriangLine.Infer(regularTriangList[i], equalLineList)
    flag = flag1 or flag2
    checkEndlessLoop(flag, "ReasonByLmRegularTriang")
    return flag


# 相等角的角度相等
def ReasonByLmEQAngleGetDegree():
    if len(equalAngleList) < 1 and len(angleList) < 1:
        return False
    flag = False
    for i in range(len(angleList)):
        set1 = set()
        set1.update(angleList[i].p1, angleList[i].p3)
        for j in range(len(equalAngleList)):
            newInfo = None
            set2 = set()
            set3 = set()
            set2.update(equalAngleList[j].p1, equalAngleList[j].p3)
            set3.update(equalAngleList[j].p4, equalAngleList[j].p6)
            if set1 == set2 and angleList[i].p2 == equalAngleList[j].p2:
                newInfo = Informations.Angle(equalAngleList[j].p4, equalAngleList[j].p5, equalAngleList[j].p6,
                                             angleList[i].p4)
            if set1 == set3 and angleList[i].p2 == equalAngleList[j].p5:
                newInfo = Informations.Angle(equalAngleList[j].p1, equalAngleList[j].p2, equalAngleList[j].p3,
                                             angleList[i].p4)
            if newInfo is not None:
                # 用一个res来存IsInList返回的值
                newInfo.conditions.append(["相等角的角度相等", angleList[i], equalAngleList[j]])
                res = newInfo.IsInList(angleList)
                newInfo.weight = max(angleList[i].weight, equalAngleList[j].weight) + 1
                if res is False:
                    angleList.append(newInfo)
                    flag = True
                elif res is True:
                    continue
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
    checkEndlessLoop(flag, "ReasonByLmEQAngleGetDegree")
    return flag


# 角平分线的性质 & 角平分线平分有值角
def ReasonByLmBisectorAngle():
    if len(bisectorAngleList) < 1:
        return False
    flag = False
    for item in bisectorAngleList:
        newInfo = newInfo1 = newInfo2 = None
        set1 = set()
        set1.update(item.p1, item.p3)
        if item.p4 != item.p2:
            newInfo = Informations.EqualAngle(item.p1, item.p2, item.p4, item.p3, item.p2, item.p4)
            if len(angleList) != 0:
                for item1 in angleList:
                    set2 = set()
                    set2.update(item1.p1, item1.p3)
                    if set1 == set2 and item.p2 == item1.p2:
                        newInfo1 = Informations.Angle(item.p1, item.p2, item.p4, item1.p4 / 2.0)
                        newInfo2 = Informations.Angle(item.p3, item.p2, item.p4, item1.p4 / 2.0)
        else:
            newInfo = Informations.EqualAngle(item.p1, item.p2, item.p5, item.p3, item.p2, item.p5)
            if len(angleList) != 0:
                for item1 in angleList:
                    set2 = set()
                    set2.update(item1.p1, item1.p3)
                    if set1 == set2 and item.p2 == item1.p2:
                        newInfo1 = Informations.Angle(item.p1, item.p2, item.p5, item1.p4 / 2.0)
                        newInfo2 = Informations.Angle(item.p3, item.p2, item.p5, item1.p4 / 2.0)
        if newInfo is not None:
            # 用一个res来存IsInList返回的值
            newInfo.conditions.append(["角平分线分出一对相等角", item])
            res = newInfo.IsInList(equalAngleList, coLineList)
            newInfo.weight = item.weight + 1
            if res is False:
                equalAngleList.append(newInfo)
                flag = True
            elif res is True:
                continue
            else:
                nums = len(equalAngleList[res].conditions)
                for x in equalAngleList[res].conditions:
                    if len(x) != len(newInfo.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(x)):
                            if x[list_no] != newInfo.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalAngleList[res].conditions.append(newInfo.conditions[-1])
                equalAngleList[res].weight = min(newInfo.weight, equalAngleList[res].weight)
        if newInfo1 is not None:
            # 用一个res来存IsInList返回的值
            newInfo1.conditions.append(["角平分线分出一对相等角", item])
            res = newInfo1.IsInList(angleList)
            # if type(item) == list:
            #     print(1)
            newInfo1.weight = item.weight + 1
            if res is False:
                angleList.append(newInfo1)
                flag = True
            elif res is True:
                continue
            else:
                nums = len(angleList[res].conditions)
                for x in angleList[res].conditions:
                    if len(x) != len(newInfo1.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(x)):
                            if x[list_no] != newInfo1.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    angleList[res].conditions.append(newInfo1.conditions[-1])
                angleList[res].weight = min(newInfo1.weight, angleList[res].weight)
        if newInfo2 is not None:
            # 用一个res来存IsInList返回的值
            newInfo2.conditions.append(["角平分线分出一对相等角", item])
            res = newInfo2.IsInList(angleList)
            newInfo2.weight = item.weight + 1
            if res is False:
                angleList.append(newInfo2)
                flag = True
            elif res is True:
                continue
            else:
                nums = len(angleList[res].conditions)
                for x in angleList[res].conditions:
                    if len(x) != len(newInfo2.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(x)):
                            if x[list_no] != newInfo2.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    angleList[res].conditions.append(newInfo2.conditions[-1])
                angleList[res].weight = min(newInfo2.weight, angleList[res].weight)
    checkEndlessLoop(flag, "ReasonByLmBisectorAngle")
    return flag


# 等腰三角形的证明1（两边相等）
def ReasonByLmLineProveIsoTriangle():
    if len(equalLineList) < 1:
        return False
    flag = False
    for item in equalLineList:
        newInfo = None
        set1 = set()
        set1.update(item.p1, item.p2, item.p3, item.p4)
        if len(set1) != 3:
            continue
        if item.p1 == item.p3:
            newInfo = Informations.IsoTriangle(item.p1, item.p2, item.p4)
        elif item.p1 == item.p4:
            newInfo = Informations.IsoTriangle(item.p1, item.p2, item.p3)
        elif item.p2 == item.p3:
            newInfo = Informations.IsoTriangle(item.p2, item.p1, item.p4)
        elif item.p2 == item.p4:
            newInfo = Informations.IsoTriangle(item.p2, item.p1, item.p3)
        if newInfo is not None:
            # 用一个res来存IsInList返回的值
            newInfo.conditions.append(["三角形的两个邻边相等，该三角形是等腰三角形", item])
            res = newInfo.IsInList(isoTriangleList)
            newInfo.weight = item.weight + 1
            if res is False:
                isoTriangleList.append(newInfo)
                flag = True
            elif res is True:
                continue
            else:
                nums = len(isoTriangleList[res].conditions)
                for item in isoTriangleList[res].conditions:
                    if len(item) != len(newInfo.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    isoTriangleList[res].conditions.append(newInfo.conditions[-1])
                isoTriangleList[res].weight = min(newInfo.weight, isoTriangleList[res].weight)
    checkEndlessLoop(flag, "ReasonByLmLineProveIsoTriangle")
    return flag


# 等腰三角形的证明2（两角相等）
def ReasonByLmAngleProveIsoTriangle():
    if len(equalAngleList) < 1:
        return False
    flag = False
    for item in equalAngleList:
        newInfo = None
        set1 = set()
        set1.update(item.p1, item.p2, item.p3)
        set2 = set()
        set2.update(item.p4, item.p5, item.p6)
        if set1 != set2:
            continue
        if item.p1 != item.p5:
            newInfo = Informations.IsoTriangle(item.p1, item.p2, item.p5)
        elif item.p3 != item.p5:
            newInfo = Informations.IsoTriangle(item.p3, item.p2, item.p5)
        if newInfo is not None:
            # 用一个res来存IsInList返回的值
            newInfo.conditions.append(["三角形的两个邻边相等，该三角形是等腰三角形", item])
            res = newInfo.IsInList(isoTriangleList)
            newInfo.weight = item.weight + 1
            if res is False:
                isoTriangleList.append(newInfo)
                flag = True
            elif res is True:
                continue
            else:
                nums = len(isoTriangleList[res].conditions)
                for item in isoTriangleList[res].conditions:
                    if len(item) != len(newInfo.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item)):
                            if item[list_no] != newInfo.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    isoTriangleList[res].conditions.append(newInfo.conditions[-1])
                isoTriangleList[res].weight = min(newInfo.weight, isoTriangleList[res].weight)
    checkEndlessLoop(flag, "ReasonByLmAngleProveIsoTriangle")
    return flag


# 等腰三角形的性质
# 两个腰相等#
# 两个底角相等
# 如果底边有中点，可以得到角平分线和垂直信息
def ReasonByLmIsoTriangleProve():
    if len(isoTriangleList) < 1:
        return False
    flag = False
    i = 0
    for item in isoTriangleList:
        newInfo3 = newInfo4 = None
        newInfo1 = Informations.EqualLine(item.p1, item.p2, item.p1, item.p3)
        newInfo2 = Informations.EqualAngle(item.p1, item.p2, item.p3, item.p1, item.p3, item.p2)
        if len(midPointList) > 0:
            for i in range(len(midPointList)):
                set1 = set()
                set2 = set()
                set1.update(midPointList[i].p2, midPointList[i].p3)
                set2.update(item.p2, item.p3)
                if set1 == set2:
                    newInfo3 = Informations.BisectorAngle(item.p2, item.p1, item.p3, item.p1, midPointList[i].p1)
                    newInfo4 = Informations.VerticalLine(item.p1, midPointList[i].p1, item.p2, item.p3, pointList,
                                                         midPointList[i].p1)
        if newInfo1 is not None:
            # 用一个res来存IsInList返回的值
            newInfo1.conditions.append(["等腰三角形的两个腰相等", item])
            res = newInfo1.IsInList(equalLineList)
            newInfo1.weight = item.weight + 1
            if res is False:
                equalLineList.append(newInfo1)
                flag = True
            elif res is True:
                continue
            else:
                nums = len(equalLineList[res].conditions)
                for item1 in equalLineList[res].conditions:
                    if len(item1) != len(newInfo1.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item1)):
                            if item1[list_no] != newInfo1.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalLineList[res].conditions.append(newInfo1.conditions[-1])
                equalLineList[res].weight = min(newInfo1.weight, equalLineList[res].weight)
        if newInfo2 is not None:
            # 用一个res来存IsInList返回的值
            newInfo2.conditions.append(["等腰三角形的两个底角相等", item])
            res = newInfo2.IsInList(equalAngleList, coLineList)
            newInfo2.weight = item.weight + 1
            if res is False:
                equalAngleList.append(newInfo2)
                lag = True
            elif res is True:
                continue
            else:
                nums = len(equalAngleList[res].conditions)
                for item2 in equalAngleList[res].conditions:
                    if len(item2) != len(newInfo2.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item2)):
                            if item2[list_no] != newInfo2.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    equalAngleList[res].conditions.append(newInfo2.conditions[-1])
                equalAngleList[res].weight = min(newInfo2.weight, equalAngleList[res].weight)
        if newInfo3 is not None:
            # 用一个res来存IsInList返回的值
            newInfo3.conditions.append(["等腰三角形三线合一", item, midPointList[i]])
            res = newInfo3.IsInList(bisectorAngleList)
            newInfo3.weight = max(item.weight, midPointList[i].weight) + 1
            if res is False:
                bisectorAngleList.append(newInfo3)
                flag = True
            elif res is True:
                continue
            else:
                nums = len(bisectorAngleList[res].conditions)
                for item3 in bisectorAngleList[res].conditions:
                    if len(item3) != len(newInfo3.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item3)):
                            if item3[list_no] != newInfo3.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    bisectorAngleList[res].conditions.append(newInfo3.conditions[-1])
                bisectorAngleList[res].weight = min(newInfo3.weight, bisectorAngleList[res].weight)
        if newInfo4 is not None:
            # 用一个res来存IsInList返回的值
            newInfo4.conditions.append(["等腰三角形三线合一", item, midPointList[i]])
            res = newInfo4.IsInList(verticalLineList)
            newInfo4.weight = max(item.weight, midPointList[i].weight) + 1
            if res is False:
                verticalLineList.append(newInfo4)
                flag = True
            elif res is True:
                continue
            else:
                nums = len(verticalLineList[res].conditions)
                for item4 in verticalLineList[res].conditions:
                    if len(item4) != len(newInfo4.conditions[-1]):
                        nums -= 1
                        continue
                    else:
                        for list_no in range(len(item4)):
                            if item4[list_no] != newInfo4.conditions[-1][list_no]:
                                nums -= 1
                                break
                if nums == 0:
                    verticalLineList[res].conditions.append(newInfo4.conditions[-1])
                verticalLineList[res].weight = min(newInfo4.weight, verticalLineList[res].weight)
    checkEndlessLoop(flag, "ReasonByLmIsoTriangleProve")
    return flag


# 等腰直角三角形的证明
# 顶点是直角的等腰三角形是等腰直角三角形
def ReasonByLmLineProveIsoAndRtTriangle():
    if len(isoTriangleList) < 1 or len(rightAngleList) < 1:
        return False
    flag = False
    for item in isoTriangleList:
        for item1 in rightAngleList:
            newInfo = None
            set1 = set()
            set2 = set()
            set1.update(item.p1, item.p2, item.p3)
            set2.update(item1.p1, item1.p2, item1.p3)
            if set1 == set2:
                newInfo = Informations.IsoAndRtTriangle(item.p1, item.p2, item.p3)
            if newInfo is not None:
                # 用一个res来存IsInList返回的值
                newInfo.conditions.append(["有一个直角的等腰三角形是等腰直角三角形", item, item1])
                res = newInfo.IsInList(isoAndRtTriangleList)
                newInfo.weight = max(item.weight, item1.weight) + 1
                if res is False:
                    isoAndRtTriangleList.append(newInfo)
                    flag = True
                elif res is True:
                    continue
                else:
                    nums = len(isoAndRtTriangleList[res].conditions)
                    for x in isoAndRtTriangleList[res].conditions:
                        if len(x) != len(newInfo.conditions[-1]):
                            nums -= 1
                            continue
                        else:
                            for list_no in range(len(x)):
                                if x[list_no] != newInfo.conditions[-1][list_no]:
                                    nums -= 1
                                    break
                    if nums == 0:
                        isoAndRtTriangleList[res].conditions.append(newInfo.conditions[-1])
                    isoAndRtTriangleList[res].weight = min(newInfo.weight, isoAndRtTriangleList[res].weight)
    checkEndlessLoop(flag, "ReasonByLmLineProveIsoAndRtTriangle")
    return flag


# 两对互补角推相等角
def ReasonByLmCompAngleGetEQAngle():
    if len(complementaryAngleList) < 2:
        return False
    flag = False
    for i in range(len(complementaryAngleList)):
        for j in range(i + 1, len(complementaryAngleList)):
            newInfo = None
            set1 = set()
            set2 = set()
            set3 = set()
            set4 = set()
            set1.update(complementaryAngleList[i].p1, complementaryAngleList[i].p3)
            set2.update(complementaryAngleList[i].p4, complementaryAngleList[i].p6)
            set3.update(complementaryAngleList[j].p1, complementaryAngleList[j].p3)
            set4.update(complementaryAngleList[j].p4, complementaryAngleList[j].p6)
            if set1 == set3 and complementaryAngleList[i].p2 == complementaryAngleList[j].p2:
                newInfo = Informations.EqualAngle(complementaryAngleList[i].p4, complementaryAngleList[i].p5,
                                                  complementaryAngleList[i].p6, complementaryAngleList[j].p4,
                                                  complementaryAngleList[j].p5, complementaryAngleList[j].p6)
            elif set1 == set4 and complementaryAngleList[i].p2 == complementaryAngleList[j].p5:
                newInfo = Informations.EqualAngle(complementaryAngleList[i].p4, complementaryAngleList[i].p5,
                                                  complementaryAngleList[i].p6, complementaryAngleList[j].p1,
                                                  complementaryAngleList[j].p2, complementaryAngleList[j].p3)
            elif set2 == set3 and complementaryAngleList[i].p5 == complementaryAngleList[j].p2:
                newInfo = Informations.EqualAngle(complementaryAngleList[i].p1, complementaryAngleList[i].p2,
                                                  complementaryAngleList[i].p3, complementaryAngleList[j].p4,
                                                  complementaryAngleList[j].p5, complementaryAngleList[j].p6)
            elif set2 == set4 and complementaryAngleList[i].p5 == complementaryAngleList[j].p5:
                newInfo = Informations.EqualAngle(complementaryAngleList[i].p1, complementaryAngleList[i].p2,
                                                  complementaryAngleList[i].p3, complementaryAngleList[j].p1,
                                                  complementaryAngleList[j].p2, complementaryAngleList[j].p3)
            if newInfo is not None:
                # 用一个res来存IsInList返回的值
                newInfo.conditions.append(["两对互补角推相等角", complementaryAngleList[i], complementaryAngleList[j]])
                res = newInfo.IsInList(equalAngleList, coLineList)
                newInfo.weight = max(complementaryAngleList[i].weight, complementaryAngleList[j].weight) + 1
                if res is False:
                    equalAngleList.append(newInfo)
                    flag = True
                elif res is True:
                    continue
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
    checkEndlessLoop(flag, "ReasonByLmCompAngleGetEQAngle")
    return flag


# 有公共边的一对互补角推出共线关系
def ReasonByLmComGetCoLine():
    if len(complementaryAngleList) < 1 or len(coLineList) < 1:
        return False
    flag = False
    for item1 in complementaryAngleList:
        newInfo1 = None
        if item1.p2 == item1.p5:
            if item1.p1 == item1.p4:
                for item2 in coLineList:
                    if item2.check == 1 and item2.p1 == item1.p2 and (
                            item2.p2 == item1.p3 and item2.p3 == item1.p6) or (
                            item2.p2 == item1.p6 and item2.p3 == item1.p3):
                        newInfo1 = Informations.CoLine(item1.p2, item1.p3, item1.p6, 1)
            elif item1.p1 == item1.p6:
                for item2 in coLineList:
                    if item2.check == 1 and item2.p1 == item1.p2 and (
                            item2.p2 == item1.p3 and item2.p3 == item1.p4) or (
                            item2.p2 == item1.p4 and item2.p3 == item1.p3):
                        newInfo1 = Informations.CoLine(item1.p2, item1.p3, item1.p4, 1)
            elif item1.p3 == item1.p4:
                for item2 in coLineList:
                    if item2.check == 1 and item2.p1 == item1.p2 and (
                            item2.p2 == item1.p1 and item2.p3 == item1.p6) or (
                            item2.p2 == item1.p6 and item2.p3 == item1.p1):
                        newInfo1 = Informations.CoLine(item1.p2, item1.p1, item1.p6, 1)
            elif item1.p3 == item1.p6:
                for item2 in coLineList:
                    if item2.check == 1 and item2.p1 == item1.p2 and (
                            item2.p2 == item1.p1 and item2.p3 == item1.p4) or (
                            item2.p2 == item1.p4 and item2.p3 == item1.p1):
                        newInfo1 = Informations.CoLine(item1.p2, item1.p1, item1.p4, 1)
        if newInfo1 is not None:
            # 用一个res来存IsInList返回的值
            newInfo1.conditions.append(["既相邻又互补的一对角组成一个平角", item1])
            res = newInfo1.IsInList(coLineList)
            newInfo1.weight = item1.weight + 1
            if res is False:
                coLineList.append(newInfo1)
                flag = True
            elif res is True:
                continue
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
    checkEndlessLoop(flag, "ReasonByLmComGetCoLine")
    return flag


# 既相等又互补的一对角都是直角 && 互补角的传递性
def ReasonByLmEQAndComAngle90():
    if len(equalAngleList) < 1 or len(complementaryAngleList) < 1:
        return False
    flag = False

    for item1 in equalAngleList:
        set1 = set()
        set2 = set()
        set1.update(item1.p1, item1.p3)
        set2.update(item1.p4, item1.p6)
        for item2 in complementaryAngleList:
            newInfo1 = newInfo2 = newInfo3 = None
            set3 = set()
            set4 = set()
            set3.update(item2.p1, item2.p3)
            set4.update(item2.p4, item2.p6)
            if (set1 == set3 and set2 == set4 and item1.p2 == item2.p2 and item1.p5 == item2.p5) or (
                    set1 == set4 and set2 == set3 and item1.p2 == item2.p5 and item1.p5 == item2.p2):
                newInfo1 = Informations.VerticalLine(item1.p1, item1.p2, item1.p3, item1.p2, pointList, item1.p2)
                newInfo2 = Informations.VerticalLine(item1.p4, item1.p5, item1.p6, item1.p5, pointList, item1.p5)
            # 13相等，24互补
            if set1 == set3 and set2 != set4 and item1.p2 == item2.p2 and item1.p5 != item2.p5:
                newInfo3 = Informations.ComplementaryAngle(item1.p4, item1.p5, item1.p6, item2.p4, item2.p5, item2.p6)
            # 14相等，23互补
            elif set1 == set4 and set2 != set3 and item1.p2 == item2.p5 and item1.p5 != item2.p2:
                newInfo3 = Informations.ComplementaryAngle(item1.p4, item1.p5, item1.p6, item2.p1, item2.p2, item2.p3)
            # 23相等，14互补
            elif set2 == set3 and set1 != set4 and item1.p5 == item2.p2 and item1.p2 != item2.p5:
                newInfo3 = Informations.ComplementaryAngle(item1.p1, item1.p2, item1.p3, item2.p4, item2.p5, item2.p6)
            # 24相等，13互补
            elif set2 == set4 and set1 != set3 and item1.p5 == item2.p5 and item1.p2 != item2.p2:
                newInfo3 = Informations.ComplementaryAngle(item1.p1, item1.p2, item1.p3, item2.p1, item2.p2, item2.p3)
            if newInfo1 is not None:
                # 用一个res来存IsInList返回的值
                newInfo1.conditions.append(["既相等又互补的一对角都是直角", item1, item2])
                res = newInfo1.IsInList(verticalLineList)
                newInfo1.weight = max(item1.weight, item2.weight) + 1
                if res is False:
                    verticalLineList.append(newInfo1)
                    flag = True
                elif res is True:
                    continue
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
                newInfo2.conditions.append(["既相等又互补的一对角都是直角", item1, item2])
                res = newInfo2.IsInList(verticalLineList)
                newInfo2.weight = max(item1.weight, item2.weight) + 1
                if res is False:
                    verticalLineList.append(newInfo2)
                    flag = True
                elif res is True:
                    continue
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
                newInfo3.conditions.append(["互补角的传递性", item1, item2])
                res = newInfo3.IsInList(complementaryAngleList, coLineList)
                newInfo3.weight = max(item1.weight, item2.weight) + 1
                if res is False:
                    complementaryAngleList.append(newInfo3)
                    flag = True
                elif res is True:
                    continue
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
    checkEndlessLoop(flag, "ReasonByLmEQAndComAngle90")
    return flag


# 两对互余角推相等角
def ReasonByLmCoterAngleGetEQAngle():
    if len(coterminalAngleList) < 2:
        return False
    flag = False
    for i in range(len(coterminalAngleList)):
        for j in range(i + 1, len(coterminalAngleList)):
            newInfo = None
            set1 = set()
            set2 = set()
            set3 = set()
            set4 = set()
            set1.update(coterminalAngleList[i].p1, coterminalAngleList[i].p3)
            set2.update(coterminalAngleList[i].p4, coterminalAngleList[i].p6)
            set3.update(coterminalAngleList[j].p1, coterminalAngleList[j].p3)
            set4.update(coterminalAngleList[j].p4, coterminalAngleList[j].p6)
            if set1 == set3 and coterminalAngleList[i].p2 == coterminalAngleList[j].p2:
                newInfo = Informations.EqualAngle(coterminalAngleList[i].p4, coterminalAngleList[i].p5,
                                                  coterminalAngleList[i].p6, coterminalAngleList[j].p4,
                                                  coterminalAngleList[j].p5, coterminalAngleList[j].p6)
            elif set1 == set4 and coterminalAngleList[i].p2 == coterminalAngleList[j].p5:
                newInfo = Informations.EqualAngle(coterminalAngleList[i].p4, coterminalAngleList[i].p5,
                                                  coterminalAngleList[i].p6, coterminalAngleList[j].p1,
                                                  coterminalAngleList[j].p2, coterminalAngleList[j].p3)
            elif set2 == set3 and coterminalAngleList[i].p5 == coterminalAngleList[j].p2:
                newInfo = Informations.EqualAngle(coterminalAngleList[i].p1, coterminalAngleList[i].p2,
                                                  coterminalAngleList[i].p3, coterminalAngleList[j].p4,
                                                  coterminalAngleList[j].p5, coterminalAngleList[j].p6)
            elif set2 == set4 and coterminalAngleList[i].p5 == coterminalAngleList[j].p5:
                newInfo = Informations.EqualAngle(coterminalAngleList[i].p1, coterminalAngleList[i].p2,
                                                  coterminalAngleList[i].p3, coterminalAngleList[j].p1,
                                                  coterminalAngleList[j].p2, coterminalAngleList[j].p3)
            if newInfo is not None:
                # 用一个res来存IsInList返回的值
                newInfo.conditions.append(["两对互余角推相等角", coterminalAngleList[i], coterminalAngleList[j]])
                res = newInfo.IsInList(equalAngleList, coLineList)
                newInfo.weight = max(coterminalAngleList[i].weight, coterminalAngleList[j].weight) + 1
                if res is False:
                    equalAngleList.append(newInfo)
                    flag = True
                elif res is True:
                    continue
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
    checkEndlessLoop(flag, "ReasonByLmCoterAngleGetEQAngle")
    return flag


# 既相等又互余的一对角都是直角 && 互余角的传递性
def ReasonByLmEQAndCoterAngle45():
    if len(equalAngleList) < 1 or len(coterminalAngleList) < 1:
        return False
    flag = False
    for item1 in equalAngleList:
        set1 = set()
        set2 = set()
        set1.update(item1.p1, item1.p3)
        set2.update(item1.p4, item1.p6)
        for item2 in coterminalAngleList:
            newInfo1 = newInfo2 = newInfo3 = None
            set3 = set()
            set4 = set()
            set3.update(item2.p1, item2.p3)
            set4.update(item2.p4, item2.p6)
            if (set1 == set3 and set2 == set4 and item1.p2 == item2.p2 and item1.p5 == item2.p5) or \
                    (set1 == set4 and set2 == set3 and item1.p2 == item2.p5 and item1.p5 == item2.p2):
                newInfo1 = Informations.Angle(item1.p1, item1.p2, item1.p3, 45)
                newInfo2 = Informations.Angle(item1.p4, item1.p5, item1.p6, 45)
            # 13相等，24互余
            if set1 == set3 and set2 != set4 and item1.p2 == item2.p2 and item1.p5 != item2.p5:
                newInfo3 = Informations.CoterminalAngles(item1.p4, item1.p5, item1.p6, item2.p4, item2.p5, item2.p6)
            # 14相等，23互余
            elif set1 == set4 and set2 != set3 and item1.p2 == item2.p5 and item1.p5 != item2.p2:
                newInfo3 = Informations.CoterminalAngles(item1.p4, item1.p5, item1.p6, item2.p1, item2.p2, item2.p3)
            # 23相等，14互余
            elif set2 == set3 and set1 != set4 and item1.p5 == item2.p2 and item1.p2 != item2.p5:
                newInfo3 = Informations.CoterminalAngles(item1.p1, item1.p2, item1.p3, item2.p4, item2.p5, item2.p6)
            # 24相等，13互余
            elif set2 == set4 and set1 != set3 and item1.p5 == item2.p5 and item1.p2 != item2.p2:
                newInfo3 = Informations.CoterminalAngles(item1.p1, item1.p2, item1.p3, item2.p1, item2.p2, item2.p3)
            if newInfo1 is not None:
                # 用一个res来存IsInList返回的值
                newInfo1.conditions.append(["既相等又互余的一对角都是45°角", item1, item2])
                res = newInfo1.IsInList(angleList)
                newInfo1.weight = max(item1.weight, item2.weight) + 1
                if res is False:
                    angleList.append(newInfo1)
                    flag = True
                elif res is True:
                    continue
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
                newInfo2.conditions.append(["既相等又互余的一对角都是45°角", item1, item2])
                res = newInfo2.IsInList(angleList)
                newInfo2.weight = max(item1.weight, item2.weight) + 1
                if res is False:
                    angleList.append(newInfo2)
                    flag = True
                elif res is True:
                    continue
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
                newInfo3.conditions.append(["互余角的传递性", item1, item2])
                res = newInfo3.IsInList(coterminalAngleList, coLineList)
                newInfo3.weight = max(item1.weight, item2.weight) + 1
                if res is False:
                    coterminalAngleList.append(newInfo3)
                    flag = True
                elif res is True:
                    continue
                else:
                    nums = len(coterminalAngleList[res].conditions)
                    for item in coterminalAngleList[res].conditions:
                        if len(item) != len(newInfo3.conditions[-1]):
                            nums -= 1
                            continue
                        else:
                            for list_no in range(len(item)):
                                if item[list_no] != newInfo3.conditions[-1][list_no]:
                                    nums -= 1
                                    break
                    if nums == 0:
                        coterminalAngleList[res].conditions.append(newInfo3.conditions[-1])
                    coterminalAngleList[res].weight = min(newInfo3.weight, coterminalAngleList[res].weight)
    checkEndlessLoop(flag, "ReasonByLmEQAndCoterAngle45")
    return flag


# 有公共边的一对互余角推出垂直关系
def ReasonByLmCoterGetVer():
    if len(coterminalAngleList) < 1:
        return False
    flag = False
    for item1 in coterminalAngleList:
        newInfo1 = None
        if item1.p2 == item1.p5:
            if item1.p1 == item1.p4:
                newInfo1 = Informations.Angle(item1.p3, item1.p2, item1.p6, 90)
            elif item1.p1 == item1.p6:
                newInfo1 = Informations.Angle(item1.p3, item1.p2, item1.p4, 90)
            elif item1.p3 == item1.p4:
                newInfo1 = Informations.Angle(item1.p1, item1.p2, item1.p6, 90)
            elif item1.p3 == item1.p6:
                newInfo1 = Informations.Angle(item1.p1, item1.p2, item1.p4, 90)
        if newInfo1 is not None:
            # 用一个res来存IsInList返回的值
            newInfo1.conditions.append(["既相邻又互余的一对角组成一个直角", item1])
            res = newInfo1.IsInList(angleList)
            newInfo1.weight = item1.weight + 1
            if res is False:
                angleList.append(newInfo1)
                flag = True
            elif res is True:
                continue
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
    checkEndlessLoop(flag, "ReasonByLmCoterGetVer")
    return flag


# 四点共圆的性质
# 1、共圆的四个点所连成同侧共底的两个三角形的顶角相等
# 2、圆内接四边形的对角互补
def ReasonByLmFourPointOnCircle():
    if len(circleList) < 1:
        return False
    flag = False
    for item in circleList:
        # 检查这个圆有没有四个点
        if hasattr(item, 'p4'):
            flag = Lemmas.LmFourPointOnCircle.Infer(item, equalAngleList, complementaryAngleList, coLineList)
    checkEndlessLoop(flag, "ReasonByLmFourPointOnCircle")
    return flag


# 垂直于同一条直线的两条直线平行
def ReasonByLmVerGetPall():
    if len(verticalLineList) < 2:
        return False
    flag = False
    for i in range(len(verticalLineList)):
        for j in range(i + 1, len(verticalLineList)):
            newInfo = None
            if verticalLineList[i].p5 == "#" or verticalLineList[j].p5 == "#" or verticalLineList[i].p5 != \
                    verticalLineList[j].p5:
                set1 = set()
                set2 = set()
                set3 = set()
                set4 = set()
                set1.update(verticalLineList[i].p1, verticalLineList[i].p2)
                set2.update(verticalLineList[i].p3, verticalLineList[i].p4)
                set3.update(verticalLineList[j].p1, verticalLineList[j].p2)
                set4.update(verticalLineList[j].p3, verticalLineList[j].p4)
                if set1 == set3:
                    newInfo = Informations.Parallel(verticalLineList[i].p3, verticalLineList[i].p4,
                                                    verticalLineList[j].p3,
                                                    verticalLineList[j].p4)
                elif set1 == set4:
                    newInfo = Informations.Parallel(verticalLineList[i].p3, verticalLineList[i].p4,
                                                    verticalLineList[j].p1,
                                                    verticalLineList[j].p2)
                elif set2 == set3:
                    newInfo = Informations.Parallel(verticalLineList[i].p1, verticalLineList[i].p2,
                                                    verticalLineList[j].p3,
                                                    verticalLineList[j].p4)
                elif set2 == set4:
                    newInfo = Informations.Parallel(verticalLineList[i].p1, verticalLineList[i].p2,
                                                    verticalLineList[j].p1,
                                                    verticalLineList[j].p2)
                if newInfo is not None:
                    # 用一个res来存IsInList返回的值
                    newInfo.conditions.append(
                        ["垂直于同一条直线的两条直线平行", verticalLineList[i], verticalLineList[j]])
                    res = newInfo.IsInList(parallelLineList)
                    newInfo.weight = max(verticalLineList[i].weight, verticalLineList[j].weight) + 1
                    if res is False:
                        parallelLineList.append(newInfo)
                        flag = True
                    elif res is True:
                        continue
                    else:
                        nums = len(parallelLineList[res].conditions)
                        for item in parallelLineList[res].conditions:
                            if len(item) != len(newInfo.conditions[-1]):
                                nums -= 1
                                continue
                            else:
                                for list_no in range(len(item)):
                                    if item[list_no] != newInfo.conditions[-1][list_no]:
                                        nums -= 1
                                        break
                        if nums == 0:
                            parallelLineList[res].conditions.append(newInfo.conditions[-1])
                        parallelLineList[res].weight = min(newInfo.weight, parallelLineList[res].weight)
    checkEndlessLoop(flag, "ReasonByLmVerGetPall")
    return flag


# 一条直线垂直于平行线中的一条,则垂直另一条
def ReasonByLmVerAndParGetVer():
    if len(verticalLineList) < 1 or len(parallelLineList) < 1:
        return False
    flag = False
    for item1 in verticalLineList:
        for item2 in parallelLineList:
            newInfo = None
            set1 = set()
            set2 = set()
            set3 = set()
            set4 = set()
            set1.update(item1.p1, item1.p2)
            set2.update(item1.p3, item1.p4)
            set3.update(item2.p1, item2.p2)
            set4.update(item2.p3, item2.p4)
            # 13相等，24垂直
            if set1 == set3:
                newInfo = Informations.VerticalLine(item1.p3, item1.p4, item2.p3, item2.p4, pointList)
            # 14相等，23垂直
            elif set1 == set4:
                newInfo = Informations.VerticalLine(item1.p3, item1.p4, item2.p1, item2.p2, pointList)
            # 23相等，14垂直
            elif set2 == set3:
                newInfo = Informations.VerticalLine(item1.p1, item1.p2, item2.p3, item2.p4, pointList)
            # 24相等，13垂直
            elif set2 == set4:
                newInfo = Informations.VerticalLine(item1.p1, item1.p2, item2.p1, item2.p2, pointList)
            if newInfo is not None:
                # 用一个res来存IsInList返回的值
                newInfo.conditions.append(["一条直线垂直于平行线中的一条,则垂直另一条", item1, item2])
                res = newInfo.IsInList(verticalLineList)
                newInfo.weight = max(item1.weight, item2.weight) + 1
                if res is False:
                    verticalLineList.append(newInfo)
                    flag = True
                elif res is True:
                    continue
                else:
                    nums = len(verticalLineList[res].conditions)
                    for item in verticalLineList[res].conditions:
                        if len(item) != len(newInfo.conditions[-1]):
                            nums -= 1
                            continue
                        else:
                            for list_no in range(len(item)):
                                if item[list_no] != newInfo.conditions[-1][list_no]:
                                    nums -= 1
                                    break
                    if nums == 0:
                        verticalLineList[res].conditions.append(newInfo.conditions[-1])
                    verticalLineList[res].weight = min(newInfo.weight, verticalLineList[res].weight)
    checkEndlessLoop(flag, "ReasonByLmVerAndParGetVer")
    return flag


# 共线且相邻的一对相等边推出中点
def ReasonByLmColineGetMid():
    if len(coLineList) < 1 or len(equalLineList) < 1:
        return False
    flag = False
    for item1 in equalLineList:
        set1 = set()
        set2 = set()
        set1.update(item1.p1, item1.p2)
        set2.update(item1.p3, item1.p4)
        for item2 in coLineList:
            newInfo = None
            if item2.check == 0:
                continue
            set3 = set()
            set4 = set()
            set3.update(item2.p1, item2.p2)
            set4.update(item2.p2, item2.p3)
            if (set1 == set3 and set2 == set4) or (set1 == set4 and set2 == set3):
                newInfo = Informations.MidPoint(item2.p2, item2.p1, item2.p3)
            if newInfo is not None:
                # 用一个res来存IsInList返回的值
                newInfo.conditions.append(["共线且相邻的一对相等边推出中点", item1, item2])
                res = newInfo.IsInList(midPointList)
                newInfo.weight = max(item1.weight, item2.weight) + 1
                if res is False:
                    midPointList.append(newInfo)
                    flag = True
                elif res is True:
                    continue
                else:
                    nums = len(midPointList[res].conditions)
                    for item in midPointList[res].conditions:
                        if len(item) != len(newInfo.conditions[-1]):
                            nums -= 1
                            continue
                        else:
                            for list_no in range(len(item)):
                                if item[list_no] != newInfo.conditions[-1][list_no]:
                                    nums -= 1
                                    break
                    if nums == 0:
                        midPointList[res].conditions.append(newInfo.conditions[-1])
                    midPointList[res].weight = min(newInfo.weight, midPointList[res].weight)
    checkEndlessLoop(flag, "ReasonByLmColineGetMid")
    return flag


# 互补、互余角之间已知一角的角度推另外一角的角度
def ReasonByLmCompGetAnotherAngle():
    if not ((len(complementaryAngleList) > 0 or len(coterminalAngleList) > 0) and len(angleList) > 0):
        return False
    flag = False
    for item1 in angleList:
        set1 = set()
        set2 = set()
        set1.update(item1.p1, item1.p3)
        for item2 in complementaryAngleList:
            newInfo = None
            set3 = set()
            set4 = set()
            set3.update(item2.p1, item2.p3)
            set4.update(item2.p4, item2.p6)
            if set1 == set3 and item1.p2 == item2.p2:
                newInfo = Informations.Angle(item2.p4, item2.p5, item2.p6, 180 - item1.p4)
            elif set1 == set4 and item1.p2 == item2.p5:
                newInfo = Informations.Angle(item2.p1, item2.p2, item2.p3, 180 - item1.p4)
            if newInfo is not None:
                # 用一个res来存IsInList返回的值
                newInfo.conditions.append(["互补角之间已知一角的角度推另外一角的角度", item1, item2])
                res = newInfo.IsInList(angleList)
                newInfo.weight = max(item1.weight, item2.weight) + 1
                if res is False:
                    angleList.append(newInfo)
                    flag = True
                elif res is True:
                    continue
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
        for item3 in coterminalAngleList:
            newInfo = None
            set5 = set()
            set6 = set()
            set5.update(item3.p1, item3.p3)
            set6.update(item3.p4, item3.p6)
            if set1 == set5 and item1.p2 == item3.p2:
                newInfo = Informations.Angle(item3.p4, item3.p5, item3.p6, 90 - item1.p4)
            elif set1 == set6 and item1.p2 == item3.p5:
                newInfo = Informations.Angle(item3.p1, item3.p2, item3.p3, 90 - item1.p4)
            if newInfo is not None:
                # 用一个res来存IsInList返回的值
                newInfo.conditions.append(["互余角之间已知一角的角度推另外一角的角度", item1, item3])
                res = newInfo.IsInList(angleList)
                newInfo.weight = max(item1.weight, item3.weight) + 1
                if res is False:
                    angleList.append(newInfo)
                    flag = True
                elif res is True:
                    continue
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
    checkEndlessLoop(flag, "ReasonByLmCompGetAnotherAngle")
    return flag


def GEO():
    # for item in coLineList:
    #     item.printSelf()
    return False


# 推理过程持续迭代，直到不再生成新的信息
def ReasoningEngine():
    info = None
    while (True):
        if (
                check_coLine() == False and
                check_vertical() == False and
                ReasonByLmMidPoint_EqualLine() == False and
                ReasonByLmVertiGetRiangleAndCoLine() == False and
                ReasonByLmCoLineGetCoLine() == False and
                ReasonByLmMedianLine() == False and
                ReasonByLmParallalTransitivity() == False and
                ReasonByLmParallelogramaDetermination1() == False and
                ReasonByLmParallelogramaDetermination2() == False and  # 对边平行且相等证明平行四边形，未完善，需要cv辅助
                ReasonByLmEqualLineTransitivity() == False and
                ReasoningByLmParallogramGetLineParall() == False and
                # ReasonByLmparallogram_Oppo_Midpoint() == False and  # 线段加减相等规则 未完善
                # ReasonByLmdDoubleAngleEqual() == False and              # 角加减相等规则 未完善
                ReasonByLmEqualTriangleALA() == False and
                ReasonByLmEqualTriangleLLL() == False and
                ReasonByLmEqualTriangleLAL() == False and
                ReasonByLmEqualTriangle_reverse() == False and
                ReasonByLmDoubleangle_ThirdAngle() == False and
                ReasonByLmAIangle_EQangle() == False and
                ReasonByLmRangle_EQangle() == False and
                ReasonByLmEqualAngleTransitivity() == False and
                ReasoningByLmCoLineGetVPA() == False and
                ReasoningByLmSquare() == False and
                ReasonByLmRiangleGet90() == False and
                ReasonByLmAngleNumEQ() == False and
                ReasonByLmRegularTriang() == False and
                ReasonByLmEQAngleGetDegree() == False and
                ReasonByLmRTriangleMidLine() == False and
                ReasoningByLmRectangle() == False and
                ReasonByLmRatioLineGetMore() == False and
                ReasonByLmBisectorAngle() == False and
                ReasonByLmCompAngleGetEQAngle() == False and
                ReasonByLmLineProveIsoTriangle() == False and
                ReasonByLmAngleProveIsoTriangle() == False and
                ReasonByLmIsoTriangleProve() == False and
                ReasonByLmTriangle180() == False and
                ReasonByLmLineProveIsoAndRtTriangle() == False and
                ReasonByLmReRTriangleMidLine() == False and
                ReasonByLmFourPointOnCircle() == False and
                ReasonByLmEQAndComAngle90() == False and
                ReasonByLmRatioAngleGetMore() == False and
                ReasonByLmCoterAngleGetEQAngle() == False and
                ReasonByLmEQAndCoterAngle45() == False and
                ReasonByLmComGetCoLine() == False and
                ReasonByLmCoterGetVer() == False and
                ReasonByLmVerGetPall() == False and
                # ReasonByLmVerAndParGetVer() == False and  # 一条直线垂直于平行线中的一条,则垂直另一条，未解决#交点问题
                ReasonByLmColineGetMid() == False and
                ReasonByLmCompGetAnotherAngle() == False and
                ReasonByLmEqualTriangleHL() == False and
                GEO() == False
        ):
            return False
        if (len(conjectureList) > 0):
            info = IsConjectureProved(conjectureList[0])
        if info is not None:
            return True


# 推理fixpoint
def FixpointEngine():
    while (True):
        if (
                check_coLine() == False and
                check_vertical() == False and
                ReasonByLmMidPoint_EqualLine() == False and
                ReasonByLmVertiGetRiangleAndCoLine() == False and
                ReasonByLmCoLineGetCoLine() == False and
                ReasonByLmMedianLine() == False and
                ReasonByLmParallalTransitivity() == False and
                ReasonByLmParallelogramaDetermination1() == False and
                ReasonByLmParallelogramaDetermination2() == False and
                ReasonByLmEqualLineTransitivity() == False and
                ReasoningByLmParallogramGetLineParall() == False and
                # ReasonByLmparallogram_Oppo_Midpoint() == False and  # 线段加减相等规则 未完善
                # ReasonByLmdDoubleAngleEqual() == False and              # 角加减相等规则 未完善
                ReasonByLmEqualTriangleALA() == False and
                ReasonByLmEqualTriangleLLL() == False and
                ReasonByLmEqualTriangleLAL() == False and
                ReasonByLmEqualTriangle_reverse() == False and
                ReasonByLmDoubleangle_ThirdAngle() == False and
                ReasonByLmAIangle_EQangle() == False and
                ReasonByLmRangle_EQangle() == False and
                ReasonByLmEqualAngleTransitivity() == False and
                ReasoningByLmCoLineGetVPA() == False and
                ReasoningByLmSquare() == False and
                ReasonByLmRiangleGet90() == False and
                ReasonByLmAngleNumEQ() == False and
                ReasonByLmRegularTriang() == False and
                ReasonByLmEQAngleGetDegree() == False and
                ReasonByLmRTriangleMidLine() == False and
                ReasoningByLmRectangle() == False and
                ReasonByLmRatioLineGetMore() == False and
                ReasonByLmBisectorAngle() == False and
                ReasonByLmCompAngleGetEQAngle() == False and
                ReasonByLmLineProveIsoTriangle() == False and
                ReasonByLmAngleProveIsoTriangle() == False and
                ReasonByLmIsoTriangleProve() == False and
                ReasonByLmTriangle180() == False and
                ReasonByLmLineProveIsoAndRtTriangle() == False and
                ReasonByLmReRTriangleMidLine() == False and
                ReasonByLmFourPointOnCircle() == False and
                ReasonByLmEQAndComAngle90() == False and
                ReasonByLmRatioAngleGetMore() == False and
                ReasonByLmCoterAngleGetEQAngle() == False and
                ReasonByLmEQAndCoterAngle45() == False and
                ReasonByLmComGetCoLine() == False and
                ReasonByLmCoterGetVer() == False and
                ReasonByLmVerGetPall() == False and
                # ReasonByLmVerAndParGetVer() == False and
                ReasonByLmColineGetMid() == False and
                ReasonByLmCompGetAnotherAngle() == False and
                ReasonByLmEqualTriangleHL() == False and
                GEO() == False
        ):
            break


# 检测推理出的信息中，是否有待证结论，若有，就说明得证
# 如下代码只考虑了待证结论为一条的情形，遇到多条的题目，需要改写
def IsConjectureProved(i):
    if i.name == "平行四边形":
        set1 = set()
        set1.add(i.p1)
        set1.add(i.p2)
        set1.add(i.p3)
        set1.add(i.p4)
        for info in parallogramList:
            set2 = set()
            set2.add(info.p1)
            set2.add(info.p2)
            set2.add(info.p3)
            set2.add(info.p4)

            if (set1 == set2):
                return info
    if i.name == "相等线":
        set1 = set()
        set2 = set()
        set1.add(i.p1)
        set1.add(i.p2)
        set2.add(i.p3)
        set2.add(i.p4)
        for info in equalLineList:
            set3 = set()
            set4 = set()
            set3.add(info.p1)
            set3.add(info.p2)
            set4.add(info.p3)
            set4.add(info.p4)

            if (set1 == set3 and set2 == set4) or (set1 == set4 and set2 == set3):
                return info
    if i.name == "全等三角形":
        set1 = set()
        set2 = set()
        set1.add(i.p1)
        set1.add(i.p2)
        set1.add(i.p3)
        set2.add(i.p4)
        set2.add(i.p5)
        set2.add(i.p6)
        for info in equalTriangleList:
            set3 = set()
            set4 = set()
            set3.add(info.p1)
            set3.add(info.p2)
            set3.add(info.p3)
            set4.add(info.p4)
            set4.add(info.p5)
            set4.add(info.p6)
            if (set1 == set3 and set2 == set4) or (set1 == set4 and set2 == set3):
                return info
    if i.name == "相等角":
        set1 = set()
        set2 = set()
        set1.add(i.p1)
        set1.add(i.p3)
        set2.add(i.p4)
        set2.add(i.p6)
        for info in equalAngleList:
            set3 = set()
            set4 = set()
            set3.add(info.p1)
            set3.add(info.p3)
            set4.add(info.p4)
            set4.add(info.p6)
            if (set1 == set3 and set2 == set4 and i.p2 == info.p2 and i.p5 == info.p5) or (
                    set1 == set4 and set2 == set3 and i.p2 == info.p5 and i.p5 == info.p2):
                return info
    if i.name == "等腰三角形":
        set1 = set()
        set1.add(i.p1)
        set1.add(i.p2)
        set1.add(i.p3)
        for info in isoTriangleList:
            set3 = set()
            set3.add(info.p1)
            set3.add(info.p2)
            set3.add(info.p3)
            if set1 == set3:
                return info
    if i.name == "等腰直角三角形":
        set1 = set()
        set1.add(i.p1)
        set1.add(i.p2)
        set1.add(i.p3)
        for info in isoAndRtTriangleList:
            set3 = set()
            set3.add(info.p1)
            set3.add(info.p2)
            set3.add(info.p3)
            if set1 == set3:
                return info
    if i.name == "垂直":
        set1 = set()
        set2 = set()
        set1.add(i.p1)
        set1.add(i.p2)
        set2.add(i.p3)
        set2.add(i.p4)
        for info in verticalLineList:
            set3 = set()
            set4 = set()
            set3.add(info.p1)
            set3.add(info.p2)
            set4.add(info.p3)
            set4.add(info.p4)
            if (set1 == set3 and set2 == set4 and i.p5 == info.p5) or (
                    set1 == set4 and set2 == set3 and i.p5 == info.p5):
                return info
    return None


def checkEndlessLoop(flag, def_name):
    if flag:
        print(def_name, "is still running")
    return


# 显示推理链，类似于传统的证明过程
def PrintReasonlingPath(conjecture):
    queue = list()
    stack = list()

    templist = list()
    templist.append(conjecture)

    queue.append(templist)
    while (len(queue) > 0):
        infoList = queue.pop(0)
        stack.append(infoList)

        for info in infoList:
            if info.source != "已知":
                queue.append(info.conditions)

    while (len(stack) > 0):
        infolist = stack.pop()
        for info in infolist:
            info.Print()


# 求所有推理路径的深度搜索函数
def find_all_paths(start, proveTree, visited=None, level=0):
    # if level > 1:
    #     return
    # 如果没有已遍历集合visited，就初始化一个
    if visited is None:
        visited = set()
    # 如果遍历到叶子结点，返回空
    if start.source == "已知":
        return
    # for condition in start.conditions:
    # 这个start结点的第一个condition组的字符串表示
    for condition in start.conditions[0:2]:
        # 改
        res_temp = ""
        conditions_info = ""
        for item in condition[1:]:
            conditions_info += item.info_name
        # 已经遍历过start结点的这个condition组了
        if conditions_info in visited:
            continue
        else:
            # 维护一个已遍历 谓词组 的集合 visited
            visited.add(conditions_info)
            flag = 1
            for node in condition[1:]:
                if flag == 1:
                    res_temp += "\n第" + str(level) + "层：\n因为：" + node.printSelf_re()
                else:
                    res_temp += " 且 " + node.printSelf_re()
                flag += 1
            res_temp += "\n"
            res_temp += "所以：" + start.printSelf_re()
            res_temp += "（ " + condition[0] + " ）"
            res_temp += "\n*******************************"
            # print(res_temp)
            for node in condition[1:]:
                temp_prove_tree = ProveTree(res_temp)
                find_all_paths(node, temp_prove_tree, visited, level + 1)
                proveTree.addchild(temp_prove_tree)
            # if len(start.conditions) > 50:
            #     start.printSelf_CN()
            #     for cb in start.conditions:
            #         print("隔断")
            #         for x in cb[1:]:
            #             print("               ", end=" ")
            #             x.printSelf_CN()
            # print(len(start.conditions))
            # print(len(condition))
            # print("#####################")
            # 回溯操作
            visited.remove(conditions_info)
    return


class ProveTree(object):
    def __init__(self, info):
        self.info = info
        self.childs = []
        self.isLeaf = False

    def addchild(self, child):
        self.childs.append(child)

    def addinfo(self, info):
        self.info = info

    def copy(self):
        new_tree = ProveTree(self.info)
        # 复制子节点
        for child in self.childs:
            # 对于每个子节点，进行浅拷贝，确保新对象仍然引用原始对象中的相同子对象
            new_tree.addchild(child.copy())
        return new_tree


proveTree = ProveTree("根结点")


def get_paths(tree, current_path="", paths=[]):
    # 如果当前节点是叶子节点，则将当前路径添加到路径列表中
    if not tree.childs:
        paths.append(current_path + tree.info)
        return paths

    # 遍历当前节点的每个子节点
    for child in tree.childs:
        # 递归地获取子节点的路径
        get_paths(child, current_path + tree.info, paths)

    return paths


def FindNewTitle(old_result):
    new_title_list_output = []
    for item1 in parallogramList:
        if 7 > item1.weight > 3 and item1.info_name != old_result:
            new_title_list_output.append(item1)
    for item1 in parallelLineList:
        if 7 > item1.weight > 3 and item1.info_name != old_result:
            new_title_list_output.append(item1)
    for item1 in equalLineList:
        if 7 > item1.weight > 3 and item1.info_name != old_result:
            new_title_list_output.append(item1)
    for item1 in equalTriangleList:
        if 7 > item1.weight > 3 and item1.info_name != old_result:
            new_title_list_output.append(item1)
    for item1 in ratioLineList:
        if 7 > item1.weight > 3 and item1.info_name != old_result:
            new_title_list_output.append(item1)
    for item1 in ratioAngleList:
        if 7 > item1.weight > 3 and item1.info_name != old_result:
            new_title_list_output.append(item1)
    for item1 in equalAngleList:
        if 7 > item1.weight > 3 and item1.info_name != old_result and item1.p2 != item1.p5:
            new_title_list_output.append(item1)
    return new_title_list_output


def printAllList(check):
    if check == 0:
        return None
    i = 0
    print("\n####################################################################################", end="")
    print("fixpoint:")
    for item in midPointList:
        if item is None:
            print("None")
        else:
            item.printSelf()
            i += 1
    # for item in verticalpointList:
    #     if item is None:
    #         print("None")
    #     else:
    #         item.printSelf()
    for item in parallelLineList:
        if item is None:
            print("None")
        else:
            item.printSelf()
            i += 1
    for item in verticalLineList:
        if item is None:
            print("None")
        else:
            item.printSelf()
            i += 1
    for item in angleList:
        if item is None:
            print("None")
        else:
            item.printSelf()
            i += 1
    for item in rightAngleList:
        if item is None:
            print("None")
        else:
            item.printSelf()
            i += 1
    for item in triangleList:
        if item is None:
            print("None")
        else:
            item.printSelf()
            i += 1
    for item in parallogramList:
        if item is None:
            print("None")
        else:
            item.printSelf()
            i += 1
    for item in rhombusList:
        if item is None:
            print("None")
        else:
            item.printSelf()
            i += 1
    for item in rectangleList:
        if item is None:
            print("None")
        else:
            item.printSelf()
            i += 1
    for item in ovalList:
        if item is None:
            print("None")
        else:
            item.printSelf()
            i += 1
    for item in circleList:
        if item is None:
            print("None")
        else:
            item.printSelf()
            i += 1
    for item in equalLineList:
        if item is None:
            print("None")
        else:
            item.printSelf()
            i += 1
    for item in ratioLineList:
        if item is None:
            print("None")
        else:
            item.printSelf()
            i += 1
    eqline = 0
    for item in equalAngleList:
        if item is None:
            print("None")
        else:
            item.printSelf()
            i += 1
            eqline += 1
    print("相等角的个数为：", eqline)
    for item in ratioAngleList:
        if item is None:
            print("None")
        else:
            item.printSelf()
            i += 1
    for item in bisectorAngleList:
        if item is None:
            print("None")
        else:
            item.printSelf()
            i += 1
    for item in alter_Inter_AngleList:
        if item is None:
            print("None")
        else:
            item.printSelf()
            i += 1
    for item in equalTriangleList:
        if item is None:
            print("None")
        else:
            item.printSelf()
            # PrintTree(item)
            i += 1
    for item in similarTriangleList:
        if item is None:
            print("None")
        else:
            item.printSelf()
            i += 1
    for item in coLineList:
        if item is None:
            print("None")
        else:
            item.printSelf()
            i += 1
    for item in squareList:
        if item is None:
            print("None")
        else:
            item.printSelf()
            i += 1
    for item in regularTriangList:
        if item is None:
            print("None")
        else:
            item.printSelf()
            i += 1
    for item in isoTriangleList:
        if item is None:
            print("None")
        else:
            item.printSelf()
            i += 1
    for item in isoAndRtTriangleList:
        if item is None:
            print("None")
        else:
            item.printSelf()
            i += 1
    for item in complementaryAngleList:
        if item is None:
            print("None")
        else:
            item.printSelf()
            i += 1
    for item in coterminalAngleList:
        if item is None:
            print("None")
        else:
            item.printSelf()
            i += 1
    print("fixpoint的总数为", i)


def print_title():
    print("例题一：平行四边形ABCD，连接AC，分别过B、D作AC的垂线交于E、F两点,使得BE⊥AC,DF垂直于AC，求证：BE=DF。")
    print("例题二：正方形 ABCD 及等边三角形EDC 如图位置放置，连接 AE，BE。求证:AE=BE。")
    print("例题三：AD⊥DB，AC⊥CB，E、F是AB、CD的中点，求证：△CFE全等于△DFE。")
    print(
        "例题四：在平行四边形ABCD 中，O对角线 BD 的中点，过点 O的直线EF 分别交 AD，BC于E、F 两点，连接 BE，DF。求证:四边形 BEDF 是平行四边形。")
    print(
        "例题五：在正方形 ABCD 中，E是 BC 边上的一点，连接 AE，过点B作 BH⊥AE，垂足为 H，延长 BH交CD 于点F，连接 AF。求证:AE=BF")
    print("例题六：在矩形ABCD中，E是AD的中点，延长CE，BA相交于点F，连接AC，DF。求证：四边形ACDF是平行四边形。")
    print("例题七：在正方形ABCD中，E为CD边上的一点，F为BC的延长线上一点，CE=CF。求证：△BCE全等于△DCF")
    print("例题八：三角形ABC中，∠BAC=90°,M、F、E分别为BC,CA,AB 的中点求证:EF =AM")
    print("例题九：三角形ABC中，AB=AC,AD 是角平分线,DE,DF 分别垂直于AB、AC.求证:EB=FC")
    print("例题十：平行四边形AEBD，在△ACE的两边，向外作等边三角形ADC、ECB.求证：BD⊥DA.")
    print("例十一：平行四边形BEAC，圆内接四边形BEAC，EC交BA于D. 求证：BC⊥CA.")
    print("例十二：在△ABC中,AB=AC,点D为BC的中点,连结AD,点E为AD的中点,作DG⊥BE于点G,点F为AC的中点. 求证：GF=DF.")


def choose_title(title_num):
    if title_num == 0:
        m1 = Informations.RightAngle("A", "B", "C")
        rightAngleList.append(m1)
        m2 = Informations.RightAngle("X", "B", "D")
        rightAngleList.append(m2)
        # m3 = Informations.EqualLine("A", "C", "A", "C", )
        # equalLineList.append(m3)
        m4 = Informations.EqualLine("A", "C", "D", "X")
        equalLineList.append(m4)
        # m5 = Informations.Angle("d", "e", "f", 43)
        # angleList.append(m5)
        c1 = Informations.EqualTriangle("C", "A", "D", "C", "D", "B")
        conjectureList.append(c1)
    if title_num == 1:
        pointList.append(Informations.Point('A', round(108.41, 2), round(2.58, 2)))
        pointList.append(Informations.Point('B', round(2.69, 2), round(332.51, 2)))
        pointList.append(Informations.Point('C', round(465.57, 2), round(333.14, 2)))
        pointList.append(Informations.Point('D', round(572.55, 2), round(3.66, 2)))
        pointList.append(Informations.Point('E', round(216.05, 2), round(100.04, 2)))
        pointList.append(Informations.Point('F', round(361.0, 2), round(231.0, 2)))
        m1 = Informations.Parallogram("A", "B", "C", "D")
        parallogramList.append(m1)
        m2 = Informations.VerticalLine("D", "F", "A", "C", pointList)
        m4 = Informations.VerticalLine("B", "E", "A", "C", pointList)
        # m2 = Informations.VerticalLine("D", "F", "A", "C", "F")
        # m4 = Informations.VerticalLine("B", "E", "A", "C", "E")
        # verticalLineList.append(m2)
        # verticalLineList.append(m4)
        m5 = Informations.CoLine("E", "A", "F", 1)
        m6 = Informations.CoLine("E", "A", "C", 1)
        # m7 = Informations.CoLine("F", "A", "C", 1)
        # m8 = Informations.CoLine("F", "E", "C", 1)
        coLineList.append(m5)
        coLineList.append(m6)
        # coLineList.append(m7)
        # coLineList.append(m8)
        m1.source = "已知"
        m2.source = "已知"
        m4.source = "已知"
        m5.source = "已知"
        m6.source = "已知"
        c1 = Informations.EqualLine("E", "B", "F", "D", )
        conjectureList.append(c1)
    if title_num == 2:
        m1 = Informations.Square("A", "B", "C", "D")
        m1.SetID(1)
        squareList.append(m1)
        m2 = Informations.Regular_triangle("D", "C", "E")
        m2.SetID(2)
        regularTriangList.append(m2)
        c1 = Informations.EqualLine("A", "E", "B", "E")
        conjectureList.append(c1)
        set_old_title.update(m1.ID, m2.ID)
    if title_num == 3:
        m1 = Informations.VerticalLine("A", "D", "B", "D", "D")
        m1.SetID(1)
        verticalLineList.append(m1)
        m2 = Informations.VerticalLine("C", "B", "C", "A", "C")
        m1.SetID(2)
        verticalLineList.append(m2)
        m3 = Informations.MidPoint("F", "C", "D")
        m1.SetID(3)
        midPointList.append(m3)
        m4 = Informations.MidPoint("E", "A", "B")
        m1.SetID(4)
        midPointList.append(m4)
        # c1 = Informations.EqualTriangle("C", "F", "E", "D", "F", "E")
        c1 = Informations.VerticalLine("C", "D", "E", "F", "F")
        conjectureList.append(c1)
        set_old_title.update(m1.ID, m2.ID, m3.ID, m4.ID)
    if title_num == 4:
        pointList.append(Informations.Point('A', round(118.89, 2), round(7.33, 2)))
        pointList.append(Informations.Point('B', round(3.33, 2), round(251.45, 2)))
        pointList.append(Informations.Point('C', round(422.5, 2), round(250.32, 2)))
        pointList.append(Informations.Point('D', round(542.01, 2), round(2.34, 2)))
        pointList.append(Informations.Point('E', round(220.7, 2), round(8.27, 2)))
        pointList.append(Informations.Point('F', round(324.82, 2), round(249.59, 2)))
        pointList.append(Informations.Point('G', round(270.57, 2), round(128.26, 2)))
        m1 = Informations.Parallogram("A", "B", "C", "D")
        m1.source = "已知"
        parallogramList.append(m1)
        m3 = Informations.MidPoint("G", "B", "D")
        m3.source = "已知"
        midPointList.append(m3)
        m2 = Informations.CoLine("E", "A", "D", 1)
        m2.source = "已知"
        coLineList.append(m2)
        m4 = Informations.CoLine("F", "B", "C", 1)
        m4.source = "已知"
        coLineList.append(m4)
        m5 = Informations.CoLine("G", "E", "F", 1)
        m5.source = "已知"
        coLineList.append(m5)
        c1 = Informations.Parallogram("E", "B", "F", "D")
        conjectureList.append(c1)
    if title_num == 5:
        m1 = Informations.Square("A", "B", "C", "D")
        squareList.append(m1)
        m2 = Informations.CoLine("E", "B", "C", 1)
        coLineList.append(m2)
        m3 = Informations.VerticalLine("B", "H", "A", "E", "H")
        verticalLineList.append(m3)
        m4 = Informations.CoLine("H", "A", "E", 1)
        coLineList.append(m4)
        m5 = Informations.CoLine("H", "B", "F", 1)
        coLineList.append(m5)
        m6 = Informations.CoLine("F", "D", "C", 1)
        coLineList.append(m6)
        c1 = Informations.EqualLine("E", "A", "F", "B")
        conjectureList.append(c1)
    if title_num == 6:
        m1 = Informations.Rectangle("A", "B", "C", "D")
        rectangleList.append(m1)
        m2 = Informations.MidPoint("E", "A", "D")
        midPointList.append(m2)
        m4 = Informations.CoLine("E", "F", "C", 1)
        coLineList.append(m4)
        m5 = Informations.CoLine("A", "B", "F", 1)
        coLineList.append(m5)
        c1 = Informations.Parallogram("A", "F", "C", "D")
        conjectureList.append(c1)
    if title_num == 7:
        m1 = Informations.Square("A", "B", "C", "D")
        squareList.append(m1)
        m4 = Informations.CoLine("E", "C", "D", 1)
        coLineList.append(m4)
        m5 = Informations.CoLine("C", "B", "F", 1)
        coLineList.append(m5)
        m6 = Informations.EqualLine("C", "E", "C", "F")
        equalLineList.append(m6)
        c1 = Informations.EqualTriangle("B", "C", "E", "D", "C", "F")
        conjectureList.append(c1)
    if title_num == 8:
        m1 = Informations.VerticalLine("A", "B", "C", "A", "A")
        m1.SetID(1)
        verticalLineList.append(m1)
        m4 = Informations.MidPoint("E", "A", "B")
        m4.SetID(2)
        midPointList.append(m4)
        m6 = Informations.MidPoint("F", "A", "C")
        m6.SetID(3)
        midPointList.append(m6)
        m5 = Informations.MidPoint("M", "C", "B")
        m5.SetID(4)
        midPointList.append(m5)
        c1 = Informations.EqualLine("E", "F", "A", "M")
        conjectureList.append(c1)
        set_old_title.update(m1.ID, m4.ID, m6.ID, m5.ID)
    if title_num == 9:
        m1 = Informations.EqualLine("A", "B", "C", "A")
        equalLineList.append(m1)
        m2 = Informations.CoLine("D", "B", "C", 1)
        coLineList.append(m2)
        m3 = Informations.CoLine("E", "B", "A", 1)
        coLineList.append(m3)
        m7 = Informations.CoLine("F", "A", "C", 1)
        coLineList.append(m7)
        m4 = Informations.BisectorAngle("B", "A", "C", "A", "D")
        bisectorAngleList.append(m4)
        m6 = Informations.VerticalLine("B", "A", "E", "D", "E")
        verticalLineList.append(m6)
        m5 = Informations.VerticalLine("A", "C", "D", "F", "F")
        verticalLineList.append(m5)
        c1 = Informations.EqualLine("E", "B", "F", "C")
        conjectureList.append(c1)
    if title_num == 10:
        m1 = Informations.Parallogram("A", "E", "B", "D")
        m1.SetID(1)
        parallogramList.append(m1)
        m2 = Informations.Regular_triangle("A", "C", "D")
        m2.SetID(2)
        regularTriangList.append(m2)
        m3 = Informations.Regular_triangle("E", "C", "B")
        m3.SetID(3)
        regularTriangList.append(m3)
        m4 = Informations.CoLine("C", "B", "A", 1)
        m4.SetID(4)
        coLineList.append(m4)
        m5 = Informations.CoLine("C", "D", "E", 1)
        m5.SetID(5)
        coLineList.append(m5)
        c1 = Informations.VerticalLine("B", "D", "D", "A", "D")
        conjectureList.append(c1)
        set_old_title.update(m1.ID, m2.ID, m3.ID, m4.ID, m5.ID)
    if title_num == -10:
        m1 = Informations.Parallogram("A", "E", "B", "C")
        m1.SetID(1)
        parallogramList.append(m1)
        m2 = Informations.Regular_triangle("A", "D", "C")
        m2.SetID(2)
        regularTriangList.append(m2)
        m3 = Informations.Regular_triangle("E", "D", "B")
        m3.SetID(3)
        regularTriangList.append(m3)
        m4 = Informations.CoLine("D", "B", "A", 1)
        m4.SetID(4)
        coLineList.append(m4)
        m5 = Informations.CoLine("D", "C", "E", 1)
        m5.SetID(5)
        coLineList.append(m5)
        c1 = Informations.VerticalLine("B", "C", "C", "A", "C")
        conjectureList.append(c1)
        set_old_title.update(m1.ID, m2.ID, m3.ID, m4.ID, m5.ID)
    if title_num == 11:
        m1 = Informations.Parallogram("B", "E", "A", "C")
        m1.SetID(1)
        parallogramList.append(m1)
        m2 = Informations.Circle(p1='E', p2='A', p3='C', p4='B')
        m2.SetID(2)
        circleList.append(m2)
        c1 = Informations.VerticalLine("B", "C", "C", "A", "C")
        conjectureList.append(c1)
        set_old_title.update(m1.ID, m2.ID)
    if title_num == -11:
        m1 = Informations.Parallogram("B", "E", "A", "D")
        m1.SetID(1)
        parallogramList.append(m1)
        m2 = Informations.Circle(p1='E', p2='A', p3='D', p4='B')
        m2.SetID(2)
        circleList.append(m2)
        c1 = Informations.VerticalLine("B", "D", "D", "A", "D")
        conjectureList.append(c1)
        set_old_title.update(m1.ID, m2.ID)
    if title_num == 12:
        m1 = Informations.Rectangle("A", "B", "C", "D")
        m1.SetID(1)
        rectangleList.append(m1)
        m2 = Informations.Circle(p1='A', p2='E', p3='F', p4='C')
        m2.SetID(2)
        circleList.append(m2)
        m3 = Informations.CoLine("O", "E", "B", 1)
        m3.SetID(3)
        coLineList.append(m3)
        m4 = Informations.CoLine("O", "A", "F", 1)
        m4.SetID(4)
        coLineList.append(m4)
        c1 = Informations.VerticalLine("A", "F", "E", "B", "O")
        conjectureList.append(c1)
        set_old_title.update(m1.ID, m2.ID, m3.ID, m4.ID)


def ReasoningEngineStart(user_input):
    input_title = user_input
    choose_title(input_title)

    # input_fixpoint = int(input("是否输出fixpoint，1输出，0不输出："))

    # 2 推理原题证明过程
    start = time.perf_counter()
    ReasoningEngine()
    flag = ReasoningEngine()
    if flag:
        print("证明过程如下：", end="")
    else:
        print("证明失败！")
    for i in conjectureList:
        result = IsConjectureProved(i)
        if result is not None:
            # result.Print()
            reasoning_output = ""
            # reasoning_output = PrintReasonlingTree(reasoning_output, result)
    print(reasoning_output)
    end = time.perf_counter()
    print("\n证明耗时", end - start)
    # 清理内存
    Clear_fixpoint()
    return reasoning_output


def NewTitleEngineStart(user_input):
    input_title = user_input
    choose_title(input_title)

    # 2 推理原题证明过程
    start = time.perf_counter()
    ReasoningEngine()
    flag = ReasoningEngine()
    if flag:
        print("证明过程如下：", end="")
    else:
        print("证明失败！")
    for i in conjectureList:
        result = IsConjectureProved(i)
        if result is not None:
            # result.Print()
            reasoning_output = ""
            # reasoning_output = PrintReasonlingTree(reasoning_output, result)

    # 3 推理fixpoint
    FixpointEngine()

    # 4 出题
    new_title_list = FindNewTitle()
    # 5 清理内存
    Clear_fixpoint()
    return new_title_list


def get_condition(item, text_id):
    # 共线不需要从文字中获取
    # if item[0] == "CO_LINE":
    #     m = Informations.CoLine(item[1], item[2], item[3], 0)
    #     m.SetID(text_id)
    #     m.source = "已知"
    #     coLineList.append(m)
    #     text_id += 1
    #     set_old_title.update(str(m.ID))
    if item[0] == "EQ_LINE":
        m = Informations.EqualLine(item[1], item[2], item[3], item[4])
        m.SetID(text_id)
        m.source = "已知"
        m.weight = 0
        equalLineList.append(m)
        text_id += 1
        set_old_title.update(str(m.ID))
    elif item[0] == "RATIO_LINE":
        m = Informations.RatioLine(item[1], item[2], item[3], item[4], int(item[5]), int(item[6]))
        m.SetID(text_id)
        m.source = "已知"
        m.weight = 0
        ratioLineList.append(m)
        text_id += 1
        set_old_title.update(str(m.ID))
    elif item[0] == "ANGLE":

        m = Informations.Angle(item[1], item[2], item[3], int(item[4]))

        m.SetID(text_id)
        m.source = "已知"
        m.weight = 0
        angleList.append(m)
        text_id += 1
        set_old_title.update(str(m.ID))
    elif item[0] == "BI_ANGLE":
        m = Informations.BisectorAngle(item[1], item[3], item[2], item[3], item[4])
        m.SetID(text_id)
        m.source = "已知"
        m.weight = 0
        bisectorAngleList.append(m)
        text_id += 1
        set_old_title.update(str(m.ID))
    elif item[0] == "R_ANGLE":
        m = Informations.RightAngle(item[1], item[2], item[3])
        m.SetID(text_id)
        m.source = "已知"
        m.weight = 0
        rightAngleList.append(m)
        text_id += 1
        set_old_title.update(str(m.ID))
    elif item[0] == "EQ_ANGLE":
        m = Informations.EqualAngle(item[1], item[2], item[3], item[4], item[5], item[6])
        m.SetID(text_id)
        m.source = "已知"
        m.weight = 0
        equalAngleList.append(m)
        text_id += 1
        set_old_title.update(str(m.ID))
    elif item[0] == "COMP_ANGLE":
        m = Informations.ComplementaryAngle(item[1], item[2], item[3], item[4], item[5], item[6])
        m.SetID(text_id)
        m.source = "已知"
        m.weight = 0
        complementaryAngleList.append(m)
        text_id += 1
        set_old_title.update(str(m.ID))
    elif item[0] == "COTER_ANGLE":
        m = Informations.CoterminalAngles(item[1], item[2], item[3], item[4], item[5], item[6])
        m.SetID(text_id)
        m.source = "已知"
        m.weight = 0
        coterminalAngleList.append(m)
        text_id += 1
        set_old_title.update(str(m.ID))
    elif item[0] == "RATIO_ANGLE":
        m = Informations.RatioAngle(item[1], item[2], item[3], item[4], item[5], item[6], int(item[7]), int(item[8]))
        m.SetID(text_id)
        m.source = "已知"
        m.weight = 0
        ratioAngleList.append(m)
        text_id += 1
        set_old_title.update(str(m.ID))
    elif item[0] == "MID":
        m = Informations.MidPoint(item[1], item[2], item[3])
        m.SetID(text_id)
        m.source = "已知"
        m.weight = 0
        midPointList.append(m)
        text_id += 1
        set_old_title.update(str(m.ID))
    elif item[0] == "VERTI":
        m = Informations.VerticalLine(item[1], item[2], item[3], item[4], pointList)
        m.SetID(text_id)
        m.source = "已知"
        m.weight = 0
        verticalLineList.append(m)
        text_id += 1
        set_old_title.update(str(m.ID))
    elif item[0] == "PARALLEL":
        m = Informations.Parallel(item[1], item[2], item[3], item[4])
        m.SetID(text_id)
        m.source = "已知"
        m.weight = 0
        parallelLineList.append(m)
        text_id += 1
        set_old_title.update(str(m.ID))
    # elif item[0] == "INTERSECTION_LL":
    #     m = Informations.CoLine(item[1], item[2], item[5], 0)
    #     n = Informations.CoLine(item[3], item[4], item[5], 0)
    #     m.SetID(text_id)
    #     m.source = "已知"
    #     n.SetID(text_id)
    #     n.source = "已知"
    #     coLineList.append(m)
    #     coLineList.append(n)
    #     text_id += 2
    #     set_old_title.update(str(m.ID))
    #     set_old_title.update(str(n.ID))
    # 感觉不需要三角形？
    # elif item[0] == "TRIANGLE":
    #     pass
    #     # m = Informations.
    #     # m.SetID(text_id)
    #     # .append(m)
    #     # text_id += 1
    #     # set_old_title.update(str(m.ID))
    elif item[0] == "R_TRIANGLE":
        p1 = p2 = p3 = ()
        for position in pointList:
            if position.p1 == item[1]:
                p1 = position.position
            elif position.p1 == item[2]:
                p2 = position.position
            elif position.p1 == item[3]:
                p3 = position.position
        if p1 is None or p2 is None or p3 is None:
            return text_id
        qqq = check_r_triangle(p1, p2, p3)
        temp = None
        if qqq == 1:
            temp = Informations.RtTriangle(item[1], item[2], item[3])
        if qqq == 2:
            temp = Informations.RtTriangle(item[2], item[1], item[3])
        if qqq == 3:
            temp = Informations.RtTriangle(item[3], item[1], item[2])
        m = temp
        m.SetID(text_id)

        m.source = "已知"
        m.weight = 0
        rtTrianglelist.append(m)
        text_id += 1
        set_old_title.update(str(m.ID))
    elif item[0] == "EQ_TRIANGLE":
        m = Informations.EqualTriangle(item[1], item[2], item[3], item[4], item[5], item[6])
        m.SetID(text_id)
        m.source = "已知"
        m.weight = 0
        equalTriangleList.append(m)
        text_id += 1
        set_old_title.update(str(m.ID))
    elif item[0] == "SIM_TRIANGLE":
        m = Informations.SimilarTriangle(item[1], item[2], item[3], item[4], item[5], item[6])
        m.SetID(text_id)
        m.source = "已知"
        m.weight = 0
        similarTriangleList.append(m)
        text_id += 1
        set_old_title.update(str(m.ID))
    elif item[0] == "ISO_TRIANGLE":
        p1 = p2 = p3 = ()
        for position in pointList:
            if position.p1 == item[1]:
                p1 = position.position
            elif position.p1 == item[2]:
                p2 = position.position
            elif position.p1 == item[3]:
                p3 = position.position
        if p1 is None or p2 is None or p3 is None:
            return text_id
        qqq = check_iso_triangle(p1, p2, p3)
        temp = None
        if qqq == 1:
            temp = Informations.IsoTriangle(item[1], item[2], item[3])
        if qqq == 2:
            temp = Informations.IsoTriangle(item[2], item[1], item[3])
        if qqq == 3:
            temp = Informations.IsoTriangle(item[3], item[1], item[2])
        m = temp
        m.SetID(text_id)
        m.source = "已知"
        m.weight = 0
        isoTriangleList.append(m)
        text_id += 1
        set_old_title.update(str(m.ID))
    elif item[0] == "REGU_TRIANGLE":
        m = Informations.Regular_triangle(item[1], item[2], item[3])
        m.SetID(text_id)
        m.source = "已知"
        m.weight = 0
        regularTriangList.append(m)
        text_id += 1
        set_old_title.update(str(m.ID))
    elif item[0] == "IR_TRIANGLE":
        p1 = p2 = p3 = ()
        for position in pointList:
            if position.p1 == item[1]:
                p1 = position.position
            elif position.p1 == item[2]:
                p2 = position.position
            elif position.p1 == item[3]:
                p3 = position.position
        if p1 is None or p2 is None or p3 is None:
            return text_id
        p1, p2, p3 = check_r_triangle(p1, p2, p3)
        m = Informations.RtTriangle(p1, p2, p3)
        m.SetID(text_id)
        m.source = "已知"
        m.weight = 0
        isoAndRtTriangleList.append(m)
        text_id += 1
        set_old_title.update(str(m.ID))
    elif item[0] == "PARALLELOGRAM":
        p1 = p2 = p3 = p4 = ()
        for position in pointList:
            if position.p1 == item[1]:
                p1 = position.position
            elif position.p1 == item[2]:
                p2 = position.position
            elif position.p1 == item[3]:
                p3 = position.position
            elif position.p1 == item[4]:
                p4 = position.position
        if p1 is None or p2 is None or p3 is None or p4 is None:
            return text_id
        check = check_parallelogram(p1, p2, p3, p4)
        if check:
            m = Informations.Parallogram(item[1], item[2], item[3], item[4])
        else:
            m = Informations.Parallogram(item[1], item[2], item[4], item[3])
        m.SetID(text_id)
        m.source = "已知"
        m.weight = 0
        parallogramList.append(m)
        # m.printSelf_CN()
        text_id += 1
        set_old_title.update(str(m.ID))
    elif item[0] == "RECTANGLE":
        p1 = p2 = p3 = p4 = ()
        for position in pointList:
            if position.p1 == item[1]:
                p1 = position.position
            elif position.p1 == item[2]:
                p2 = position.position
            elif position.p1 == item[3]:
                p3 = position.position
            elif position.p1 == item[4]:
                p4 = position.position
        if p1 is None or p2 is None or p3 is None or p4 is None:
            return text_id
        check = check_parallelogram(p1, p2, p3, p4)
        if check:
            m = Informations.Rectangle(item[1], item[2], item[3], item[4])
        else:
            m = Informations.Rectangle(item[1], item[2], item[4], item[3])
        m.SetID(text_id)
        m.source = "已知"
        m.weight = 0
        rectangleList.append(m)
        text_id += 1
        set_old_title.update(str(m.ID))
    elif item[0] == "SQUARE":
        p1 = p2 = p3 = p4 = ()
        for position in pointList:
            if position.p1 == item[1]:
                p1 = position.position
            elif position.p1 == item[2]:
                p2 = position.position
            elif position.p1 == item[3]:
                p3 = position.position
            elif position.p1 == item[4]:
                p4 = position.position
        if p1 is None or p2 is None or p3 is None or p4 is None:
            return text_id
        check = check_parallelogram(p1, p2, p3, p4)
        if check:
            m = Informations.Square(item[1], item[2], item[3], item[4])
        else:
            m = Informations.Square(item[1], item[2], item[4], item[3])
        m.SetID(text_id)
        m.source = "已知"
        m.weight = 0
        squareList.append(m)
        text_id += 1
        set_old_title.update(str(m.ID))
    elif item[0] == "CIRCLE":
        m = Informations.Circle(p1=item[1], p2=item[2], p3=item[3], p4=item[4])
        m.SetID(text_id)
        m.source = "已知"
        m.weight = 0
        circleList.append(m)
        text_id += 1
        set_old_title.update(str(m.ID))
    return text_id


def check_parallelogram(p1, p2, p3, p4):
    # 计算三个相邻点的叉积
    cross_product1 = (p2[0] - p1[0]) * (p3[1] - p2[1]) - (p2[1] - p1[1]) * (p3[0] - p2[0])
    cross_product2 = (p3[0] - p2[0]) * (p4[1] - p3[1]) - (p3[1] - p2[1]) * (p4[0] - p3[0])

    # 判断叉积的符号，使用保留两位小数的精确值
    return (cross_product1 >= 0 and cross_product2 >= 0) or (cross_product1 < 0 and cross_product2 < 0)


def check_r_triangle(p1, p2, p3):
    # 计算向量
    v12 = (p2[0] - p1[0], p2[1] - p1[1])
    v13 = (p3[0] - p1[0], p3[1] - p1[1])
    v23 = (p3[0] - p2[0], p3[1] - p2[1])

    # 计算点积
    dot_product_1 = v12[0] * v13[0] + v12[1] * v13[1]
    dot_product_2 = (-v12[0]) * v23[0] + (-v12[1]) * v23[1]
    dot_product_3 = (-v13[0]) * (-v23[0]) + (-v13[1]) * (-v23[1])

    # 判断哪个点是直角点
    if abs(dot_product_1) > abs(dot_product_2) and abs(dot_product_1) > abs(dot_product_3):
        return 1
    elif abs(dot_product_2) > abs(dot_product_1) and abs(dot_product_2) > abs(dot_product_3):
        return 2
    elif abs(dot_product_3) > abs(dot_product_1) and abs(dot_product_3) > abs(dot_product_2):
        return 3
    else:
        return None


def distance(p1, p2):
    """计算两点之间的距离"""
    return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5


def check_iso_triangle(p1, p2, p3):
    # 计算三条边的长度
    d12 = distance(p1, p2)
    d13 = distance(p1, p3)
    d23 = distance(p2, p3)

    # 设定误差范围
    tolerance = 3

    # 判断哪两条边相等，进而确定顶点
    if abs(d12 - d13) < tolerance:
        return 1
    elif abs(d12 - d23) < tolerance:
        return 2
    elif abs(d13 - d23) < tolerance:
        return 3
    else:
        return None


def get_conclution(item):
    if item[0] == "CO_LINE":
        m = Informations.CoLine(item[2], item[1], item[3], 1)
        conjectureList.append(m)
    elif item[0] == "EQ_LINE":
        m = Informations.EqualLine(item[1], item[2], item[3], item[4])
        conjectureList.append(m)
    elif item[0] == "RATIO_LINE":
        m = Informations.RatioLine(item[1], item[2], item[3], item[4], int(item[5]), int(item[6]))
        conjectureList.append(m)
        set_old_title.update(str(m.ID))
    elif item[0] == "ANGLE":
        m = Informations.Angle(item[1], item[2], item[3], int(item[4]))
        conjectureList.append(m)
    elif item[0] == "BI_ANGLE":
        m = Informations.BisectorAngle(item[1], item[3], item[2], item[3], item[4])
        conjectureList.append(m)
    elif item[0] == "R_ANGLE":
        m = Informations.RightAngle(item[1], item[2], item[3])
        conjectureList.append(m)
    elif item[0] == "EQ_ANGLE":
        m = Informations.EqualAngle(item[1], item[2], item[3], item[4], item[5], item[6])
        conjectureList.append(m)
    elif item[0] == "COMP_ANGLE":
        m = Informations.ComplementaryAngle(item[1], item[2], item[3], item[4], item[5], item[6])
        conjectureList.append(m)
    elif item[0] == "COTER_ANGLE":
        m = Informations.CoterminalAngles(item[1], item[2], item[3], item[4], item[5], item[6])
        conjectureList.append(m)
    elif item[0] == "RATIO_ANGLE":
        m = Informations.RatioAngle(item[1], item[2], item[3], item[4], item[5], item[6], int(item[7]), int(item[8]))
        conjectureList.append(m)
    elif item[0] == "MID":
        m = Informations.MidPoint(item[1], item[2], item[3])
        conjectureList.append(m)
    elif item[0] == "VERTI":
        m = Informations.VerticalLine(item[1], item[2], item[3], item[4], pointList)
        conjectureList.append(m)
    elif item[0] == "PARALLEL":
        m = Informations.Parallel(item[1], item[2], item[3], item[4])
        conjectureList.append(m)
    elif item[0] == "R_TRIANGLE":
        pass
        # 未分析哪个角是直角点
        m = Informations.RtTriangle(item[1], item[2], item[3])
        conjectureList.append(m)
    elif item[0] == "EQ_TRIANGLE":
        m = Informations.EqualTriangle(item[1], item[2], item[3], item[4], item[5], item[6])
        conjectureList.append(m)
    elif item[0] == "SIM_TRIANGLE":
        m = Informations.SimilarTriangle(item[1], item[2], item[3], item[4], item[5], item[6])
        conjectureList.append(m)
    elif item[0] == "ISO_TRIANGLE":
        pass
        # 未分析哪个点是顶点
        m = Informations.IsoTriangle(item[1], item[2], item[3])
        conjectureList.append(m)
    elif item[0] == "REGU_TRIANGLE":
        m = Informations.Regular_triangle(item[1], item[2], item[3])
        conjectureList.append(m)
    elif item[0] == "IR_TRIANGLE":
        pass
        # 未分析哪个点是顶点
        m = Informations.IsoAndRtTriangle(item[1], item[2], item[3])
        conjectureList.append(m)
    elif item[0] == "PARALLELOGRAM":
        m = Informations.Parallogram(item[1], item[2], item[3], item[4])
        conjectureList.append(m)
    elif item[0] == "RECTANGLE":
        m = Informations.Rectangle(item[1], item[2], item[3], item[4])
        conjectureList.append(m)
    elif item[0] == "SQUARE":
        m = Informations.Square(item[1], item[2], item[3], item[4])
        conjectureList.append(m)
    return


def sort_list_by_weight(list1, list2):
    combined = list(zip(list1, list2))
    combined.sort(key=lambda x: x[1])
    sorted_list1 = [item[0] for item in combined]
    return sorted_list1


# 2025.1.14新版本，这个版本是用已遍历节点来去环
def break_cycles(node, level, cut, visited=set()):
    """
    尝试切断给定节点及其子节点构成的数据结构中的环。
    """
    # print(level)
    # if node.info_name == "相等线DEBF" or node.info_name == "全等三角形BGFDGE":
    #     time.sleep(1)
    print("break_cycles_numOfNode:")
    print(len(visited))
    # 推理链长度超过20？这个阈值视为垃圾推理，直接排除掉
    if len(visited) > cut:
        return False
    level += 1
    if node.source == "已知":
        return
    if len(node.conditions) == 0:
        return
    conditions_weight = []
    for item in node.conditions:
        max_num = -1
        for cons in item[1:]:
            if cons.weight > max_num:
                max_num = cons.weight
        conditions_weight.append(max_num)
    node.conditions = sort_list_by_weight(node.conditions, conditions_weight)
    # 过滤掉权重大于15的解法
    # count = len([it for it in conditions_weight if it < 10])
    # node.conditions = node.conditions[:count]
    if len(node.conditions) > 2:
        node.conditions = node.conditions[:2]
    # 遍历当前节点的conditions中的每个子列表cons
    i = -1
    while i < len(node.conditions) - 1:
        i += 1
        # 判断是不是指向根节点，从而形成环
        flag = 0
        # 判断是否已经访问过同一个结点，从而形成环
        for sub_list in node.conditions[i][1:]:
            if sub_list.info_name not in visited:
                visited.add(sub_list.info_name)
                is_path = break_cycles(sub_list, level, cut, visited)
                # 删去低效推理点
                # if is_path is False:
                #     del node.conditions[i]
                #     flag = 1
                #     i -= 1
                #     visited.remove(sub_list.info_name)
                #     break
                visited.remove(sub_list.info_name)
            else:

                del node.conditions[i]
                flag = 1
                i -= 1
                break
        if flag == 1:
            continue
    return node


# # 去环
# 2025.1.13老版本，这个版本是用已遍历节点组来去环
# def break_cycles(node, root, level, visited=set()):
#     """
#     尝试切断给定节点及其子节点构成的数据结构中的环。
#     """
#     # print("numOfNode")
#     # print(len(visited))
#     level += 1
#     if node.source == "已知":
#         return
#     if len(node.conditions) == 0:
#         return True
#     # 遍历当前节点的conditions中的每个子列表cons
#     i = -1
#     for cons in node.conditions:
#         i += 1
#         res = cons[0]
#         # 判断是不是指向根节点，从而形成环
#         flag = 0
#         for sub_list in cons[1:]:
#             if sub_list == root:
#                 print("删去"+node.conditions[i][0]+"结点")
#                 del node.conditions[i]
#                 flag = 1
#                 i -= 1
#         if flag == 1:
#             continue
#         # 判断是否已经访问过同一个cons，从而形成环
#         for sub_list in cons[1:]:
#             res += "且"
#             res += sub_list.info_name
#         if res not in visited:
#             visited.add(res)
#             for sub_list in cons[1:]:
#                 break_cycles(sub_list, root, level, visited)
#             visited.remove(res)
#         else:
#             # 删去这个cons
#             print("删去"+node.conditions[i][0]+"结点")
#             if node.info_name == "相等线FBED":
#                 print(1)
#             del node.conditions[i]
#             i -= 1
#     return node


# 给每个结点求一个字符串类型的推理路径
def add_prove_load(node, level):
    if node.source != "已知":
        if node.conditions is None:
            return
        for cons in node.conditions:
            len_of_cons = len(cons) - 1
            if len_of_cons == 1:
                if cons[1].prove_load is None:
                    continue
                for child_prove_load in cons[1].prove_load:
                    if child_prove_load not in node.prove_load:
                        qianzhi = child_prove_load
                        if cons[1].source == "已知":
                            qianzhi = ""
                        # node.prove_load.append(node.info_name + " (" + cons[0] + ")" + "[" + child_prove_load + "]")
                        one = qianzhi + "\n" + "∵ " + cons[1].printSelf_re() + "\n∴ " + node.printSelf_re() + " (" + \
                              cons[0] + ")"
                        if one not in node.prove_load:
                            node.prove_load.append(one)
                        # print("你好1")
            if len_of_cons == 2:
                if cons[1].prove_load is None or cons[2].prove_load is None:
                    continue
                list1 = []
                list2 = []
                for child_prove_load in cons[1].prove_load:
                    if child_prove_load not in list1:
                        list1.append(child_prove_load)
                for child_prove_load in cons[2].prove_load:
                    if child_prove_load not in list2:
                        list2.append(child_prove_load)
                for x in list1:
                    for y in list2:
                        qianzhi = x + y
                        if cons[1].source == "已知" and cons[2].source == "已知":
                            qianzhi = ""
                        elif cons[1].source == "已知":
                            qianzhi = y
                        elif cons[2].source == "已知":
                            qianzhi = x
                        # node.prove_load.append(node.info_name + " (" + cons[0] + ")" + "[" + x + "，" + y + "]")
                        two = qianzhi + "\n" + "∵ " + cons[1].printSelf_re() + " 且 " + cons[
                            2].printSelf_re() + "\n∴ " + node.printSelf_re() + " (" + cons[0] + ")"
                        if two not in node.prove_load:
                            node.prove_load.append(two)
                        # print("你好2")
            if len_of_cons == 3:
                if cons[1].prove_load is None or cons[2].prove_load is None or cons[3].prove_load is None:
                    continue
                list1 = []
                list2 = []
                list3 = []
                for child_prove_load in cons[1].prove_load:
                    if child_prove_load not in list1:
                        list1.append(child_prove_load)
                for child_prove_load in cons[2].prove_load:
                    if child_prove_load not in list2:
                        list2.append(child_prove_load)
                for child_prove_load in cons[3].prove_load:
                    if child_prove_load not in list3:
                        list3.append(child_prove_load)
                for x in list1:
                    for y in list2:
                        for z in list3:
                            x1 = x
                            y1 = y
                            z1 = z
                            if cons[1].source == "已知":
                                x1 = ""
                            elif cons[2].source == "已知":
                                y1 = ""
                            elif cons[3].source == "已知":
                                z1 = ""
                            qianzhi = x1 + y1 + z1
                            # node.prove_load.append(node.info_name + " (" + cons[0] + ")" + "[" + x + "，" + y + "，" + z + "]")
                            three = qianzhi + "\n" + "∵ " + cons[1].printSelf_re() + " 且 " + cons[
                                2].printSelf_re() + " 且 " + cons[
                                        3].printSelf_re() + "\n∴ " + node.printSelf_re() + " (" + cons[0] + ")"
                            if three not in node.prove_load:
                                node.prove_load.append(three)
                            # print("你好3")
    else:
        node.prove_load.append(node.info_name + "(已知)")


def find_load(node, level):
    # 好像不太对，add_prove_load需要所有子节点都已经构建出了prove_load后才能更新本结点的prove_load
    # find_load是中根算法，所以遍历到某个结点的时候只有左子树更新了prove_load，需要改成后根算法
    # 2025.1.13更新：是后根算法。。。
    if level >= 10:
        return False
    print(level)  # 需要设计一个算法，让递归深度小于10，大于十的时候直接切断
    if node.weight > 20:
        return
    if node.source == "已知":
        add_prove_load(node, level)
    else:
        for cons in node.conditions:
            for child in cons[1:]:
                find_load(child, level + 1)
        add_prove_load(node, level)


def has_cycle(node):
    visited = set()
    recursion_stack = set()

    def dfs(current_node):
        if current_node.source in ("已知", "无解"):
            return False
        if current_node in recursion_stack:
            return True
        if current_node in visited:
            return False
        visited.add(current_node)
        recursion_stack.add(current_node)
        for cons in current_node.conditions:
            for sub_node in cons[1:]:
                if dfs(sub_node):
                    return True
        recursion_stack.remove(current_node)
        return False

    return dfs(node)


def add_test_node():
    newInfo1 = Informations.Test("1")
    newInfo2 = Informations.Test("2")
    newInfo3 = Informations.Test("3")
    newInfo4 = Informations.Test("4")
    newInfo5 = Informations.Test("5")
    newInfo6 = Informations.Test("6")
    newInfo7 = Informations.Test("7")
    newInfo8 = Informations.Test("8")
    newInfo9 = Informations.Test("9")

    newInfo5.source = "已知"
    newInfo6.source = "已知"
    newInfo7.source = "已知"
    newInfo8.source = "已知"
    # newInfo9.source = "已知"

    newInfo1.conditions.append(["一号结点的第一个证明方式", newInfo2])
    newInfo1.conditions.append(["一号结点的第二个证明方式", newInfo3, newInfo4])
    newInfo2.conditions.append(["二号结点的第一个证明方式", newInfo5])
    newInfo2.conditions.append(["二号结点的第二个证明方式", newInfo6])
    newInfo3.conditions.append(["三号结点的第一个证明方式", newInfo7])
    newInfo3.conditions.append(["三号结点的第二个证明方式", newInfo8])
    newInfo4.conditions.append(["四号结点的第一个证明方式", newInfo9])
    newInfo9.conditions.append(["九号结点的第一个证明方式", newInfo3, newInfo4])
    return newInfo1


def parse_tree(s):
    def helper(index, indent):
        res = ""
        while index < len(s):
            if s[index] == '[':
                res += '\n' + '--' * indent
                index += 1
                sub_result, index = helper(index, indent + 1)
                res += sub_result
            elif s[index] == ']':
                index += 1
                return res, index
            elif s[index] == '，':
                index += 1
                res += '\n' + '--' * (indent - 1)
            else:
                start = index
                while index < len(s) and s[index] not in ['[', ']', '，']:
                    index += 1
                res += s[start:index]
        return res, index

    res, _ = helper(0, 1)
    return res


import matplotlib.pyplot as plt


def plot_points_and_lines(points, names):
    # 提取 x 和 y 坐标
    x_coords = [point[0] for point in points]
    y_coords = [point[1] for point in points]

    # 上下翻转 y 坐标
    max_y = max(y_coords)
    min_y = min(y_coords)
    flipped_y_coords = [max_y + min_y - y for y in y_coords]

    # 绘制点
    plt.scatter(x_coords, flipped_y_coords, color='red', label='Points')

    # 所有点之间两两连线
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            x1, y1 = x_coords[i], flipped_y_coords[i]
            x2, y2 = x_coords[j], flipped_y_coords[j]
            plt.plot([x1, x2], [y1, y2], color='blue')

    # 在每个点旁边添加名称标注
    for i, (x, y) in enumerate(zip(x_coords, flipped_y_coords)):
        plt.annotate(names[i], (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

    # 设置坐标轴标签和标题
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('All Points Connected with Names (Flipped Vertically)')

    # 显示图例
    plt.legend()

    # 显示网格线
    plt.grid(True)

    # 显示图形
    plt.show()


import matplotlib.patches as patches
from matplotlib.path import Path


def plot_points_and_lines_eqt(points, names, six_points):
    # 提取 x 和 y 坐标
    x_coords = [point[0] for point in points]
    y_coords = [point[1] for point in points]

    # 上下翻转 y 坐标
    max_y = max(y_coords)
    min_y = min(y_coords)
    flipped_y_coords = [max_y + min_y - y for y in y_coords]

    # 提取六个点的 x 和 y 坐标
    six_x_coords = [point[0] for point in six_points]
    six_y_coords = [point[1] for point in six_points]
    # 上下翻转六个点的 y 坐标
    six_flipped_y_coords = [max_y + min_y - y for y in six_y_coords]

    # 绘制点
    plt.scatter(x_coords, flipped_y_coords, color='red', label='Points')

    # 所有点之间两两连线
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            x1, y1 = x_coords[i], flipped_y_coords[i]
            x2, y2 = x_coords[j], flipped_y_coords[j]
            plt.plot([x1, x2], [y1, y2], color='blue')

    # 在每个点旁边添加名称标注
    for i, (x, y) in enumerate(zip(x_coords, flipped_y_coords)):
        plt.annotate(names[i], (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

    # 处理前三个点围成的区域
    first_three_verts = [(six_x_coords[i], six_flipped_y_coords[i]) for i in range(3)]
    first_three_codes = [Path.MOVETO] + [Path.LINETO] * 2
    first_three_path = Path(first_three_verts, first_three_codes)
    first_three_patch = patches.PathPatch(
        first_three_path, facecolor='yellow', edgecolor='none', alpha=0.3)
    plt.gca().add_patch(first_three_patch)

    # 处理后三个点围成的区域
    second_three_verts = [(six_x_coords[i], six_flipped_y_coords[i]) for i in range(3, 6)]
    second_three_codes = [Path.MOVETO] + [Path.LINETO] * 2
    second_three_path = Path(second_three_verts, second_three_codes)
    second_three_patch = patches.PathPatch(
        second_three_path, facecolor='green', edgecolor='none', alpha=0.3)
    plt.gca().add_patch(second_three_patch)

    # 设置坐标轴标签和标题
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('All Points Connected with Names (Flipped Vertically)')

    # 显示图例
    plt.legend()

    # 显示网格线
    plt.grid(True)

    # 显示图形
    plt.show()


if __name__ == '__main__':
    # 1 获取题号
    # print_title()
    # input是题号
    input_title = int(input("\n输入题目序号："))

    # 定义要写入文件的文本信息
    text_to_write = str(input_title) + "题：\n"

    # 1 获取谓词以及点的坐标
    res_dia, point_positions, res_text = api_test.main(input_title)
    print(res_text)
    # 2 清洗谓词
    # 原谓词的id
    text_id = 1
    # 提取题目给出的点，用于除去检测出来的异常点
    str_point = res_text[1]
    point_list = str_point.split()
    # 清洗point_positions
    for key, value in point_positions.items():
        if key is None:
            continue
        m = Informations.Point(key, round(value[0], 2), round(value[1], 2))
        if not m.IsInList(pointList) and key in point_list:
            pointList.append(m)
            m.printSelf_CN()
    # # 测试图像识别模块用
    # print("")
    # for key, value in point_positions.items():
    #     if key is None:
    #         continue
    #     if key in point_list:
    #         print("有效点： " + key, end="")
    #         print(value)
    #     else:
    #         print("噪声点： " + key, end="")
    #         print(value)
    # 画图
    point_for_draw = []
    point_name = []
    for item in pointList:
        point_for_draw.append(item.position)
        point_name.append(item.p1)
    plot_points_and_lines(point_for_draw, point_name)
    # input("测试图像识别模块用.请输入任意内容并按回车键继续：")
    # exit()
    # 清洗res_text, 主要是处理文本信息
    for item in res_text[2:-2]:
        item_list = item.split()
        print(item_list)
        text_id = get_condition(item_list, text_id)
    # 清洗res_dia, 主要是处理共线信息
    pattern = r'PointLiesOnLine\((\w+), Line\((\w+), (\w+)\)\)'
    for item in res_dia:
        match = re.match(pattern, item)
        if match and match.group(1) in point_list and match.group(2) in point_list and match.group(3) in point_list:
            m = Informations.CoLine(match.group(1), match.group(2), match.group(3), 0)
            # m.printSelf_CN()
            # m.SetID(text_id)
            coLineList.append(m)
            print("dia中的共线：")
            m.printSelf()
            m.weight = 0
            set_old_title.update(str(text_id))
            text_id += 1
    last_item = res_text[-1]
    conjecture = last_item.split()
    get_conclution(conjecture)

    printAllList(1)
    # 2 推理原题证明过程
    start = time.perf_counter()
    ReasoningEngine()
    ReasoningEngine()
    FixpointEngine()
    FixpointEngine()
    oldtitle = ""
    # 共线谓词全部设为已知
    for i in coLineList:
        i.source = "已知"
    printAllList(1)
    for i in conjectureList:
        result = IsConjectureProved(i)
        if result is not None:
            oldtitle = result.info_name
            # 切断环路
            setRoot = set()
            setRoot.add(result.info_name)
            cut = get_cut(input_title)
            break_cycles(result, 0, 10, setRoot)
            if has_cycle(result):
                print("推理链中有环路，可能发生死循环！！！")
            else:
                print("推理链中无环")

            # 递归求解
            find_load(result, 1)
            a = set()
            for item in result.prove_load:
                a.add(item)
            for item in a:
                print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                print(item)
                text_to_write = text_to_write + item + "\n" + "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&" + "\n"
            print("一共有" + str(len(a)) + "种解法")
            text_to_write = text_to_write + "一共有" + str(len(a)) + "种解法" + "\n"
        else:
            print("证明失败")
    end = time.perf_counter()
    print("\n证明耗时", end - start)
    text_to_write = text_to_write + "\n证明耗时" + str(end - start) + "\n"
    # 3 推理fixpoint
    # FixpointEngine()
    # printAllList(input_fixpoint)
    # fixpointend = time.perf_counter()
    # print("fixpoint耗时", fixpointend - start)
    #
    # 4 出题
    input("按下回车键继续...")
    user_input = api_test.textlist[input_title - 1]
    title = user_input[:user_input.find("求证")]
    new_title_list = FindNewTitle(oldtitle)
    i = 1
    for item in new_title_list:
        print(str(i) + ": " + title + "求证：" + item.printSelf_re())
        i += 1
        text_to_write = text_to_write + "求证：" + item.printSelf_re() + "\n"
    print("一共发现了" + str(i - 1) + "道新题目")
    text_to_write = text_to_write + "一共发现了" + str(i - 1) + "道新题目" + "\n"

    # 指定文件路径和文件名，如果文件不存在，open() 函数会创建它
    file_path = r"C:\Users\12418\Desktop\论文相关\推理模块实验\test" + str(input_title) + ".txt"

    try:
        # 以写入模式打开文件，如果文件不存在则创建，如果存在则覆盖原有内容
        # 使用 'w' 模式打开文件进行写入操作
        with open(file_path, 'w', encoding='utf-8') as file:
            # 将文本信息写入文件
            file.write(text_to_write)
        print(f"成功将信息写入文件：{file_path}")
    except Exception as e:
        print(f"写入文件时出现错误：{e}")
    new = int(input("请输入想获取证明过程的新题目序号："))
    new -= 1
    # 画图
    if new_title_list[new].name == "全等三角形":
        p1position = ()
        p2position = ()
        p3position = ()
        p4position = ()
        p5position = ()
        p6position = ()
        for x in pointList:
            if x.p1 == new_title_list[new].p1:
                p1position = x.position
            if x.p1 == new_title_list[new].p2:
                p2position = x.position
            if x.p1 == new_title_list[new].p3:
                p3position = x.position
            if x.p1 == new_title_list[new].p4:
                p4position = x.position
            if x.p1 == new_title_list[new].p5:
                p5position = x.position
            if x.p1 == new_title_list[new].p6:
                p6position = x.position
        plot_points_and_lines_eqt(point_for_draw, point_name,
                                  [p1position, p2position, p3position, p4position, p5position, p6position])
    setRoot = set()
    setRoot.add(new_title_list[new].info_name)
    # 对newtitle切环再findload。
    break_cycles(new_title_list[new], 0, 10, setRoot)
    find_load(new_title_list[new], 1)
    a = set()
    for item in new_title_list[new].prove_load:
        a.add(item)
    for item in a:
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(item)
    print("一共有" + str(len(a)) + "种解法")
    # 5 清理内存
    Clear_fixpoint()
