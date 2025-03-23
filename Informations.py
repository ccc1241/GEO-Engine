# 信息父类


class Information(object):

    def __init__(self):
        self.name = " 基类"  # 信息名称
        self.source = ""  # 应用何定理得到
        self.conditions = []  # 该代理依赖的前提条件
        self.ID = 0
        self.info_name = self.name + ""
        self.prove_load = []  # 证明该点的推理链
        self.weight = 100  # 该谓词的权重

    def __hash__(self):
        return hash(tuple(self.info_name))  # 根据conditions属性来生成哈希值，可根据实际调整

    def __eq__(self, other):
        if isinstance(other, Information):
            return self.info_name == other.info_name
        return False
    # def __eq__(self, other):
    #     return self.name == other.name and self.info_name == other.info_name

    def __ne__(self, other):
        return not self.__eq__(other)
    # 给前提条件编号
    def SetID(self, Id):
        self.ID = Id

    # 判断一个信息，是否已存在于列表中
    def IsInList(self, llist):
        return False

    def Print(self):
        print(self.name)

    def printSelf(self):
        print(self.name)

    def printSelf_CN(self):
        print(self.name, end="")

    def printSelf_re(self):
        return self.name

# 点信息
class Point(Information):
    def __init__(self, p1, x, y):
        self.name = "点"
        self.source = ""  # 应用何定理得到
        self.conditions = []  # 该代理依赖的前提条件
        self.prove_load = []  # 证明该点的推理链
        self.weight = 100  # 该谓词的权重

        self.p1 = p1
        self.position = (x, y)
        self.ID = 0
        self.info_name = self.name + p1
    # 给前提条件编号
    def SetID(self, Id):
        self.ID = Id

    # 判断一个信息，是否已存在于列表中
    def IsInList(self, llist):
        for i in range(len(llist)):
            info = llist[i]
            if info.p1 == self.p1:
                return i
        return False
    def printSelf_CN(self):
        print("%s点的坐标是%s" % (self.p1, self.position), end="")
    def Print(self):
        if self.source == "已知":
            print("point", "(%s %s )" % (self.p1, self.position), " (已知)")
        else:
            for info in self.conditions:
                info.Print()
            print("point", "(%s %s)" % (self.p1, self.position))

# p1是p2和p3的中点
# 中点信息
class MidPoint(Information):
    def __init__(self, p1, p2, p3):
        self.name = "中点"
        self.source = ""  # 应用何定理得到
        self.conditions = []  # 该代理依赖的前提条件
        self.prove_load = []  # 证明该点的推理链
        self.weight = 100  # 该谓词的权重

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.ID = 0

        self.info_name = self.name + p1 + p2 + p3
    # 给前提条件编号
    def SetID(self, Id):
        self.ID = Id

    # 判断一个信息，是否已存在于列表中
    def IsInList(self, llist):
        for i in range(len(llist)):
            info = llist[i]
            if ((self.p1 == info.p1 and self.p2 == info.p2 and self.p3 == info.p3) or
                    (self.p1 == info.p1 and self.p2 == info.p3 and self.p3 == info.p2)):
                return i
        return False

    def Print(self):
        if self.source == "已知":
            print("mid", "(%s %s %s)" % (self.p1, self.p2, self.p3), " (已知)")
        else:
            for info in self.conditions:
                info.Print()
            print("mid", "(%s %s %s)" % (self.p1, self.p2, self.p3))

    def printSelf(self):
        print("mid", "(%s %s %s)" % (self.p1, self.p2, self.p3))

    def printSelf_CN(self):
        print("%s点是%s%s的中点" % (self.p1, self.p2, self.p3), end="")

    def printSelf_re(self):
        return "%s点是%s%s的中点" % (self.p1, self.p2, self.p3)


# 垂点信息，p1-p2和p3-p4相互垂直于p5点
# class Verticalpoint(Information):
#     def __init__(self, p1, p2, p3, p4, p5):
#         self.name = "垂点"
#         self.source = ""  # 应用何定理得到
#         self.conditions = []  # 该代理依赖的前提条件
#
#         self.p1 = p1
#         self.p2 = p2
#         self.p3 = p3
#         self.p4 = p4
#         self.p5 = p5
#
#     # 判断一个信息，是否已存在于列表中
#     def IsInList(self, llist):
#         for i in range(len(llist)):
#             info = llist[i]
#             if ((self.p1 == info.p1 and self.p2 == info.p2 and self.p3 == info.p3) or
#                     (self.p1 == info.p1 and self.p2 == info.p3 and self.p3 == info.p2)):
#                 return True
#         return False
#
#     def Print(self):
#         if self.source == "已知":
#             print("Verticalpoint", "(%s %s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5), " (已知)")
#         else:
#             for info in self.conditions:
#                 info.Print()
#             print("Verticalpoint", "(%s %s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5),
#                   " (%s)" % (self.source))
#
#     def printSelf(self):
#         print("Verticalpoint", "(%s %s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5))
#
#     def printSelf_CN(self):
#         print("线段%s%s与线段%s%s垂直于%s点" % (self.p1, self.p2, self.p3, self.p4, self.p5))


# 平行信息，p1-p2平行于p3-p4
class Parallel(Information):
    def __init__(self, p1, p2, p3, p4):
        self.name = "平行"
        self.source = ""  # 应用何定理得到
        self.conditions = []  # 该代理依赖的前提条件
        self.prove_load = []  # 证明该点的推理链
        self.weight = 100  # 该谓词的权重

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.ID = 0

        self.info_name = self.name + p1 + p2 + p3 + p4
    # 给前提条件编号
    def SetID(self, Id):
        self.ID = Id

    # 判断一个信息，是否已存在于列表中
    def IsInList(self, llist):
        set3 = set()
        set1 = set()
        set1.add(self.p1)
        set1.add(self.p2)
        set2 = set()
        set2.add(self.p3)
        set2.add(self.p4)
        set3.update(set1, set2)
        if len(set3) != 4:
            return True
        for i in range(len(llist)):
            info = llist[i]
            set3 = set()
            set3.add(info.p1)
            set3.add(info.p2)

            set4 = set()
            set4.add(info.p3)
            set4.add(info.p4)

            if (set1 == set3 and set2 == set4) or (set1 == set4 and set2 == set3):
                return i
        return False

    def Print(self):
        if self.source == "已知":
            print("parallel", "(%s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4), " (已知)")
        else:
            for info in self.conditions:
                info.Print()
            print("parallel", "(%s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4), " (%s)" % (self.source))

    def printSelf(self):
        print("parallel", "(%s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4))

    def printSelf_CN(self):
        print("%s%s∥%s%s" % (self.p1, self.p2, self.p3, self.p4), end="")

    def printSelf_re(self):
        return "%s%s∥%s%s" % (self.p1, self.p2, self.p3, self.p4)

import time
# 垂直信息，p1-p2垂直于p3-p4，垂点为p5，注意有重合点的情况
class VerticalLine(Information):
    def __init__(self, p1, p2, p3, p4, pointList, p5='#'):
        self.name = "垂直"
        self.source = ""  # 应用何定理得到
        self.conditions = []  # 该代理依赖的前提条件
        self.prove_load = []  # 证明该点的推理链
        self.weight = 100  # 该谓词的权重

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.p5 = p5
        self.ID = 0
        self.info_name = self.name + p1 + p2 + p3 + p4
        if p5 == '#':
            p1_list = p2_list = p3_list = p4_list = None
            for item in pointList:
                if item.p1 == p1:
                    p1_list = item.position
                elif item.p1 == p2:
                    p2_list = item.position
                elif item.p1 == p3:
                    p3_list = item.position
                elif item.p1 == p4:
                    p4_list = item.position
            if p1_list is not None and p2_list is not None and p3_list is not None and p4_list is not None:
                x1 = p1_list[0]
                y1 = p1_list[1]
                x2 = p2_list[0]
                y2 = p2_list[1]
                x3 = p3_list[0]
                y3 = p3_list[1]
                x4 = p4_list[0]
                y4 = p4_list[1]
                # 计算交点的坐标
                intersection_x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / \
                                 ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))

                intersection_y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / \
                                 ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))

                intersection_point = (intersection_x, intersection_y)
                # 检查交点是否在给定的点列表中
                tolerance = 5
                for item1 in pointList:
                    if abs(item1.position[0] - intersection_point[0]) <= tolerance and abs(item1.position[1] - intersection_point[1]) <= tolerance:
                        self.p5 = item1.p1
    # 给前提条件编号
    def SetID(self, Id):
        self.ID = Id

    # 判断一个信息，是否已存在于列表中
    def IsInList(self, llist):
        set1 = set()
        set1.add(self.p1)
        set1.add(self.p2)

        set2 = set()
        set2.add(self.p3)
        set2.add(self.p4)
        if len(set1) != 2 or len(set2) != 2:
            return True
        for i in range(len(llist)):
            info = llist[i]
            set3 = set()
            set3.add(info.p1)
            set3.add(info.p2)

            set4 = set()
            set4.add(info.p3)
            set4.add(info.p4)

            if ((set1 == set3 and set2 == set4) or (set1 == set4 and set2 == set3)):
                return i
        return False

    def Print(self):
        if self.source == "已知":
            print("Vertical", "(%s %s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5), " (已知)")
        else:
            for info in self.conditions:
                info.Print()
            print("Vertical", "(%s %s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5),
                  " (%s)" % (self.source))

    def printSelf(self):
        print("Vertical", "(%s %s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5))

    def printSelf_CN(self):
        print("%s%s⊥%s%s" % (self.p1, self.p2, self.p3, self.p4), end="")

    def printSelf_re(self):
        return "%s%s⊥%s%s" % (self.p1, self.p2, self.p3, self.p4)


# 角信息，∠123 = p4°
class Angle(Information):
    def __init__(self, p1, p2, p3, p4):
        self.name = "角"
        self.source = ""  # 应用何定理得到
        self.conditions = []  # 该代理依赖的前提条件
        self.prove_load = []  # 证明该点的推理链
        self.weight = 100  # 该谓词的权重

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.ID = 0

        self.info_name = self.name + p1 + p2 + p3
    # 给前提条件编号
    def SetID(self, Id):
        self.ID = Id

    # 判断一个信息，是否已存在于列表中
    def IsInList(self, llist):
        set_check = set()
        set_check.update(self.p1, self.p2, self.p3)
        if len(set_check) != 3:
            return True
        for i in range(len(llist)):
            info = llist[i]
            if ((self.p1 == info.p1 and self.p2 == info.p2 and self.p3 == info.p3) or
                    (self.p1 == info.p3 and self.p2 == info.p2 and self.p3 == info.p1)):
                return i
        return False

    def Print(self):
        if self.source == "已知":
            print("Angle", "(%s %s %s 为%s°)" % (self.p1, self.p2, self.p3, self.p4), " (已知)")
        else:
            for info in self.conditions:
                info.Print()
            print("Angle", "(%s %s %s 为%s°)" % (self.p1, self.p2, self.p3, self.p4), " (%s)" % (self.source))

    def printSelf(self):
        print("Angle", "(%s %s %s 为%s°)" % (self.p1, self.p2, self.p3, self.p4))

    def printSelf_CN(self):
        print("角%s%s%s为%s°" % (self.p1, self.p2, self.p3, self.p4), end="")

    def printSelf_re(self):
        return "角%s%s%s为%s°" % (self.p1, self.p2, self.p3, self.p4)


# 直角信息，p1-p2垂直于p2-p3
class RightAngle(Information):
    def __init__(self, p1, p2, p3):
        self.name = "直角"
        self.source = ""  # 应用何定理得到
        self.conditions = []  # 该代理依赖的前提条件
        self.prove_load = []  # 证明该点的推理链
        self.weight = 100  # 该谓词的权重

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.ID = 0

        self.info_name = self.name + p1 + p2 + p3
    # 给前提条件编号
    def SetID(self, Id):
        self.ID = Id

    # 判断一个信息，是否已存在于列表中
    def IsInList(self, llist):
        if self.p1 == self.p2 or self.p1 == self.p3 or self.p2 == self.p3:
            return True
        for i in range(len(llist)):
            info = llist[i]
            if ((self.p1 == info.p1 and self.p2 == info.p2 and self.p3 == info.p3) or
                    (self.p1 == info.p3 and self.p2 == info.p2 and self.p3 == info.p1)):
                return i
        return False

    def Print(self):
        if self.source == "已知":
            print("rightAngle", "(%s %s %s)" % (self.p1, self.p2, self.p3), " (已知)")
        else:
            for info in self.conditions:
                info.Print()
            print("rightAngle", "(%s %s %s)" % (self.p1, self.p2, self.p3), " (%s)" % (self.source))

    def printSelf(self):
        print("rightAngle", "(%s %s %s)" % (self.p1, self.p2, self.p3))

    def printSelf_CN(self):
        print("∠%s%s%s是直角" % (self.p1, self.p2, self.p3), end="")

    def printSelf_re(self):
        return "∠%s%s%s是直角" % (self.p1, self.p2, self.p3)

# 直角三角形信息，p2p3是直角边
class RtTriangle(Information):
    def __init__(self, p1, p2, p3):
        self.name = "直角三角形"
        self.source = ""  # 应用何定理得到
        self.conditions = []  # 该代理依赖的前提条件
        self.prove_load = []  # 证明该点的推理链
        self.weight = 100  # 该谓词的权重

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.ID = 0

        self.info_name = self.name + p1 + p2 + p3
    # 给前提条件编号
    def SetID(self, Id):
        self.ID = Id

    # 判断一个信息，是否已存在于列表中
    def IsInList(self, llist):
        set1 = set()
        set1.add(self.p2)
        set1.add(self.p3)
        for i in range(len(llist)):
            info = llist[i]
            set2 = set()
            set2.add(info.p2)
            set2.add(info.p3)

            if set1 == set2 and self.p1 == info.p1:
                return i
        return False

    def Print(self):
        if self.source == "已知":
            print("RtTriangle", "(%s %s %s)" % (self.p1, self.p2, self.p3), " (已知)")
        else:
            for info in self.conditions:
                info.Print()
            print("RtTriangle", "(%s %s %s)" % (self.p1, self.p2, self.p3), "  (%s)" % (self.source))

    def printSelf(self):
        print("RtTriangle", "(%s %s %s)" % (self.p1, self.p2, self.p3))

    def printSelf_CN(self):
        print("直角△%s%s%s" % (self.p1, self.p2, self.p3), end="")

    def printSelf_re(self):
        return "直角△%s%s%s" % (self.p1, self.p2, self.p3)



# 等腰三角形信息，p1是顶点
class IsoTriangle(Information):
    def __init__(self, p1, p2, p3):
        self.name = "等腰三角形"
        self.source = ""  # 应用何定理得到
        self.conditions = []  # 该代理依赖的前提条件
        self.prove_load = []  # 证明该点的推理链
        self.weight = 100  # 该谓词的权重

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.ID = 0

        self.info_name = self.name + p1 + p2 + p3
    # 给前提条件编号
    def SetID(self, Id):
        self.ID = Id

    # 判断一个信息，是否已存在于列表中
    def IsInList(self, llist):
        set1 = set()
        set1.add(self.p2)
        set1.add(self.p3)
        for i in range(len(llist)):
            info = llist[i]
            set2 = set()
            set2.add(info.p2)
            set2.add(info.p3)

            if set1 == set2 and self.p1 == info.p1:
                return i
        return False

    def Print(self):
        if self.source == "已知":
            print("isotriangle", "(%s %s %s)" % (self.p1, self.p2, self.p3), " (已知)")
        else:
            for info in self.conditions:
                info.Print()
            print("isotriangle", "(%s %s %s)" % (self.p1, self.p2, self.p3), "  (%s)" % (self.source))

    def printSelf(self):
        print("isotriangle", "(%s %s %s)" % (self.p1, self.p2, self.p3))

    def printSelf_CN(self):
        print("等腰△%s%s%s" % (self.p1, self.p2, self.p3), end="")

    def printSelf_re(self):
        return "等腰△%s%s%s" % (self.p1, self.p2, self.p3)


# 等腰直角三角形信息，p1是顶点
class IsoAndRtTriangle(Information):
    def __init__(self, p1, p2, p3):
        self.name = "等腰直角三角形"
        self.source = ""  # 应用何定理得到
        self.conditions = []  # 该代理依赖的前提条件
        self.prove_load = []  # 证明该点的推理链
        self.weight = 100  # 该谓词的权重

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.ID = 0

        self.info_name = self.name + p1 + p2 + p3
    # 给前提条件编号
    def SetID(self, Id):
        self.ID = Id

    # 判断一个信息，是否已存在于列表中
    def IsInList(self, llist):
        set1 = set()
        set1.add(self.p2)
        set1.add(self.p3)
        for i in range(len(llist)):
            info = llist[i]
            set2 = set()
            set2.add(info.p2)
            set2.add(info.p3)

            if set1 == set2 and self.p1 == info.p1:
                return i
        return False

    def Print(self):
        if self.source == "已知":
            print("iso_rt_triangle", "(%s %s %s)" % (self.p1, self.p2, self.p3), " (已知)")
        else:
            for info in self.conditions:
                info.Print()
            print("iso_rt_triangle", "(%s %s %s)" % (self.p1, self.p2, self.p3), "  (%s)" % (self.source))

    def printSelf(self):
        print("iso_rt_triangle", "(%s %s %s)" % (self.p1, self.p2, self.p3))

    def printSelf_CN(self):
        print("等腰直角△%s%s%s" % (self.p1, self.p2, self.p3), end="")

    def printSelf_re(self):
        return "等腰直角△%s%s%s" % (self.p1, self.p2, self.p3)


# 平行四边形信息,注意四点的顺序（逆时针）（顺时针也行？）
class Parallogram(Information):
    def __init__(self, p1, p2, p3, p4):
        self.name = "平行四边形"
        self.source = ""  # 应用何定理得到
        self.conditions = []  # 该代理依赖的前提条件
        self.prove_load = []  # 证明该点的推理链
        self.weight = 100  # 该谓词的权重

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.ID = 0

        self.info_name = self.name + p1 + p2 + p3 + p4
    # 给前提条件编号
    def SetID(self, Id):
        self.ID = Id

    # 判断一个信息，是否已存在于列表中
    def IsInList(self, llist):
        set1 = set()
        set1.add(self.p1)
        set1.add(self.p2)
        set1.add(self.p3)
        set1.add(self.p4)
        if len(set1) != 4:
            return True
        for i in range(len(llist)):
            info = llist[i]
            set2 = set()
            set2.add(info.p1)
            set2.add(info.p2)
            set2.add(info.p3)
            set2.add(info.p4)

            if (set1 == set2):
                return i
        return False

    def Print(self):
        if self.source == "已知":
            print("parallogram", "(%s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4), " (已知)")
        else:
            for info in self.conditions:
                info.Print()
            print("parallogram", "(%s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4), "  (%s)" % (self.source))

    def printSelf(self):
        print("parallogram", "(%s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4))

    def printSelf_CN(self):
        print("平行四边形%s%s%s%s" % (self.p1, self.p2, self.p3, self.p4), end="")

    def printSelf_re(self):
        return "平行四边形%s%s%s%s" % (self.p1, self.p2, self.p3, self.p4)


# 菱形信息,注意四点的顺序（逆时针）
class Rhombus(Information):
    def __init__(self, p1, p2, p3, p4):
        self.name = "菱形"
        self.source = ""  # 应用何定理得到
        self.conditions = []  # 该代理依赖的前提条件
        self.prove_load = []  # 证明该点的推理链
        self.weight = 100  # 该谓词的权重

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.ID = 0

        self.info_name = self.name + p1 + p2 + p3 + p4
    # 给前提条件编号
    def SetID(self, Id):
        self.ID = Id

    # 判断一个信息，是否已存在于列表中
    def IsInList(self, llist):
        set1 = set()
        set1.add(self.p1)
        set1.add(self.p2)
        set1.add(self.p3)
        set1.add(self.p4)
        for i in range(len(llist)):
            info = llist[i]
            set2 = set()
            set2.add(info.p1)
            set2.add(info.p2)
            set2.add(info.p3)
            set2.add(info.p4)

            if (set1 == set2):
                return i
        return False

    def Print(self):
        if self.source == "已知":
            print("rhombus", "(%s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4), " (已知)")
        else:
            for info in self.conditions:
                info.Print()
            print("rhombus", "(%s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4), "  (%s)" % (self.source))

    def printSelf(self):
        print("rhombus", "(%s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4), "  (%s)" % (self.source))

    def printSelf_CN(self):
        print("菱形%s%s%s%s" % (self.p1, self.p2, self.p3, self.p4), end="")

    def printSelf_re(self):
        return "菱形%s%s%s%s" % (self.p1, self.p2, self.p3, self.p4)


# 矩形信息,注意四点的顺序（逆时针）
class Rectangle(Information):
    def __init__(self, p1, p2, p3, p4):
        self.name = "矩形"
        self.source = ""  # 应用何定理得到
        self.conditions = []  # 该代理依赖的前提条件
        self.prove_load = []  # 证明该点的推理链
        self.weight = 100  # 该谓词的权重

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.ID = 0
        self.info_name = self.name + p1 + p2 + p3 + p4

    # 给前提条件编号
    def SetID(self, Id):
        self.ID = Id

    # 判断一个信息，是否已存在于列表中
    def IsInList(self, llist):
        set1 = set()
        set1.add(self.p1)
        set1.add(self.p2)
        set1.add(self.p3)
        set1.add(self.p4)
        for i in range(len(llist)):
            info = llist[i]
            set2 = set()
            set2.add(info.p1)
            set2.add(info.p2)
            set2.add(info.p3)
            set2.add(info.p4)

            if (set1 == set2):
                return i
        return False

    def Print(self):
        if self.source == "已知":
            print("rectangle", "(%s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4), " (已知)")
        else:
            for info in self.conditions:
                info.Print()
            print("rectangle", "(%s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4), "  (%s)" % (self.source))

    def printSelf(self):
        print("rectangle", "(%s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4))

    def printSelf_CN(self):
        print("矩形%s%s%s%s" % (self.p1, self.p2, self.p3, self.p4), end="")

    def printSelf_re(self):
        return "矩形%s%s%s%s" % (self.p1, self.p2, self.p3, self.p4)


# 正方形形信息,注意四点的顺序（逆时针）
class Square(Information):
    def __init__(self, p1, p2, p3, p4):
        self.name = "正方形"
        self.source = ""  # 应用何定理得到
        self.conditions = []  # 该代理依赖的前提条件
        self.prove_load = []  # 证明该点的推理链
        self.weight = 100  # 该谓词的权重

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.ID = 0
        self.info_name = self.name + p1 + p2 + p3 + p4

    # 给前提条件编号
    def SetID(self, Id):
        self.ID = Id

    # 判断一个信息，是否已存在于列表中
    def IsInList(self, llist):
        set1 = set()
        set1.add(self.p1)
        set1.add(self.p2)
        set1.add(self.p3)
        set1.add(self.p4)
        for i in range(len(llist)):
            info = llist[i]
            set2 = set()
            set2.add(info.p1)
            set2.add(info.p2)
            set2.add(info.p3)
            set2.add(info.p4)

            if (set1 == set2):
                return i
        return False

    def Print(self):
        if self.source == "已知":
            print("square", "(%s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4), " (已知)")
        else:
            for info in self.conditions:
                info.Print()
            print("square", "(%s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4), "  (%s)" % (self.source))

    def printSelf(self):
        print("square", "(%s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4))

    def printSelf_CN(self):
        print("正方形%s%s%s%s" % (self.p1, self.p2, self.p3, self.p4), end="")

    def printSelf_re(self):
        return "正方形%s%s%s%s" % (self.p1, self.p2, self.p3, self.p4)


# 相等线信息
class EqualLine(Information):
    def __init__(self, p1, p2, p3, p4):
        self.name = "相等线"
        self.source = ""  # 应用何定理得到
        self.conditions = []  # 该代理依赖的前提条件
        self.prove_load = []  # 证明该点的推理链
        self.weight = 100  # 该谓词的权重

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.ID = 0
        self.info_name = self.name + p1 + p2 + p3 + p4

    # 给前提条件编号
    def SetID(self, Id):
        self.ID = Id

    # 判断一个信息，是否已存在于列表中
    def IsInList(self, llist):
        set1 = set()
        set2 = set()
        set1.add(self.p1)
        set1.add(self.p2)
        set2.add(self.p3)
        set2.add(self.p4)
        if set1 == set2:
            return True
        # print(len(llist))
        for i in range(len(llist)):
            info = llist[i]
            set3 = set()
            set4 = set()
            set3.add(info.p1)
            set3.add(info.p2)
            set4.add(info.p3)
            set4.add(info.p4)
            if (set1 == set3 and set2 == set4) or (set1 == set4 and set2 == set3):
                return i

        return False

    def Print(self):
        if self.source == "已知":
            print("equalLine", "(%s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4), " (已知)")
        else:
            for info in self.conditions:
                info.Print()
            print("equalLine", "(%s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4), " (%s)" % (self.source))

    def printSelf(self):
        print("equalLine", "(%s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4))

    def printSelf_CN(self):
        print("%s%s=%s%s" % (self.p1, self.p2, self.p3, self.p4), end="")

    def printSelf_re(self):
        return "%s%s=%s%s" % (self.p1, self.p2, self.p3, self.p4)


# 成比例线段信息
class RatioLine(Information):
    def __init__(self, p1, p2, p3, p4, num1, num2):
        self.name = "成比例线段"
        self.source = ""  # 应用何定理得到
        self.conditions = []  # 该代理依赖的前提条件
        self.prove_load = []  # 证明该点的推理链
        self.weight = 100  # 该谓词的权重

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.num1 = num1
        self.num2 = num2
        self.ID = 0
        self.info_name = self.name + p1 + p2 + p3 + p4

    # 给前提条件编号
    def SetID(self, Id):
        self.ID = Id

    # 判断一个信息，是否已存在于列表中
    def IsInList(self, llist):
        set1 = set()
        set2 = set()
        set1.add(self.p1)
        set1.add(self.p2)
        set2.add(self.p3)
        set2.add(self.p4)
        if set1 == set2:
            return True
        for i in range(len(llist)):
            info = llist[i]
            set3 = set()
            set4 = set()
            set3.add(info.p1)
            set3.add(info.p2)
            set4.add(info.p3)
            set4.add(info.p4)
            if (set1 == set3 and set2 == set4) or (set1 == set4 and set2 == set3):
                return i

        return False

    def Print(self):
        if self.source == "已知":
            print("RatioLine", "(%s %s : %s %s = %s:%s)" % (self.p1, self.p2, self.p3, self.p4, self.num1, self.num2),
                  " (已知)")
        else:
            for info in self.conditions:
                info.Print()
            print("RatioLine", "(%s %s : %s %s = %s:%s)" % (self.p1, self.p2, self.p3, self.p4, self.num1, self.num2))

    def printSelf(self):
        print("RatioLine", "(%s %s : %s %s = %s:%s)" % (self.p1, self.p2, self.p3, self.p4, self.num1, self.num2), )

    def printSelf_CN(self):
        print("%s%s : %s%s = %s:%s" % (self.p1, self.p2, self.p3, self.p4, self.num1, self.num2), end="")

    def printSelf_re(self):
        return "%s%s : %s%s = %s:%s" % (self.p1, self.p2, self.p3, self.p4, self.num1, self.num2)


# 相等角信息 ∠123 =∠456
class EqualAngle(Information):
    def __init__(self, p1, p2, p3, p4, p5, p6):
        self.name = "相等角"
        self.source = ""  # 应用何定理得到
        self.conditions = []  # 该代理依赖的前提条件
        self.prove_load = []  # 证明该点的推理链
        self.weight = 100  # 该谓词的权重

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.p5 = p5
        self.p6 = p6
        self.ID = 0
        self.info_name = self.name + p1 + p2 + p3 + p4 + p5 + p6

    # 给前提条件编号
    def SetID(self, Id):
        self.ID = Id

    # 判断一个信息，是否已存在于列表中
    def IsInList(self, llist, colist):
        set1 = set()
        set2 = set()
        set1.add(self.p1)
        set1.add(self.p3)
        set2.add(self.p4)
        set2.add(self.p6)
        setco3 = set()
        setco4 = set()
        setco3.update(self.p1, self.p2, self.p3)
        setco4.update(self.p4, self.p5, self.p6)
        if self.p1 == self.p2 or self.p1 == self.p3 or self.p2 == self.p3:
            return True
        if self.p4 == self.p5 or self.p4 == self.p6 or self.p5 == self.p6:
            return True
        for i in range(len(colist)):
            setco = set()
            setco.update(colist[i].p1, colist[i].p2, colist[i].p3)
            if setco == setco3 or setco == setco4:
                return True
        for i in range(len(llist)):
            info = llist[i]
            set3 = set()
            set4 = set()
            set3.add(info.p1)
            set3.add(info.p3)
            set4.add(info.p4)
            set4.add(info.p6)
            if ((set1 == set3 and set2 == set4) and (self.p2 == info.p2 and self.p5 == info.p5)) or (
                    (set1 == set4 and set2 == set3) and (self.p2 == info.p5 and self.p5 == info.p2)):
                return i
        return False

    def Print(self):
        if self.source == "已知":
            print("equalAngle", "(%s %s %s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6),
                  " (已知)")
        else:
            for info in self.conditions:
                info.Print()
            print("equalAngle", "(%s %s %s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6),
                  " (%s)" % (self.source))

    def printSelf(self):
        print("equalAngle", "(%s %s %s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6))

    def printSelf_CN(self):
        print("∠%s%s%s = ∠%s%s%s" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6), end="")

    def printSelf_re(self):
        return "∠%s%s%s = ∠%s%s%s" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6)


# 成比例角信息 ∠123 =m∠456
class RatioAngle(Information):
    def __init__(self, p1, p2, p3, p4, p5, p6, num1, num2):
        self.name = "相等角"
        self.source = ""  # 应用何定理得到
        self.conditions = []  # 该代理依赖的前提条件
        self.prove_load = []  # 证明该点的推理链
        self.weight = 100  # 该谓词的权重

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.p5 = p5
        self.p6 = p6
        self.num1 = num1
        self.num2 = num2
        self.ID = 0
        self.info_name = self.name + p1 + p2 + p3 + p4 + p5 + p6

    # 给前提条件编号
    def SetID(self, Id):
        self.ID = Id

    # 判断一个信息，是否已存在于列表中
    def IsInList(self, llist, colist):
        set1 = set()
        set2 = set()
        set1.add(self.p1)
        set1.add(self.p3)
        set2.add(self.p4)
        set2.add(self.p6)
        setco3 = set()
        setco4 = set()
        setco3.update(self.p1, self.p2, self.p3)
        setco4.update(self.p4, self.p5, self.p6)
        if self.p1 == self.p2 or self.p1 == self.p3 or self.p2 == self.p3:
            return True
        if self.p4 == self.p5 or self.p4 == self.p6 or self.p5 == self.p6:
            return True
        for i in range(len(colist)):
            setco = set()
            setco.update(colist[i].p1, colist[i].p2, colist[i].p3)
            if setco == setco3 or setco == setco4:
                return True
        for i in range(len(llist)):
            info = llist[i]
            set3 = set()
            set4 = set()
            set3.add(info.p1)
            set3.add(info.p3)
            set4.add(info.p4)
            set4.add(info.p6)
            if ((set1 == set3 and set2 == set4) and (self.p2 == info.p2 and self.p5 == info.p5)) or (
                    (set1 == set4 and set2 == set3) and (self.p2 == info.p5 and self.p5 == info.p2)):
                return i
        return False

    def Print(self):
        if self.source == "已知":
            print("ratioAngle", "(∠%s %s %s : ∠%s %s %s = %s : %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.num1, self.num2),
                  " (已知)")
        else:
            for info in self.conditions:
                info.Print()
            print("ratioAngle", "(∠%s %s %s : ∠%s %s %s = %s : %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.num1, self.num2),
                  " (%s)" % self.source)

    def printSelf(self):
        print("ratioAngle", "(∠%s %s %s : ∠%s %s %s = %s : %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.num1, self.num2))

    def printSelf_CN(self):
        print("(∠%s %s %s : ∠%s %s %s = %s : %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.num1, self.num2), end="")

    def printSelf_re(self):
        return "(∠%s %s %s : ∠%s %s %s = %s : %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.num1, self.num2)

# 角平分线信息 p4p5是∠123的角平分线
class BisectorAngle(Information):
    def __init__(self, p1, p2, p3, p4, p5):
        self.name = "角平分线"
        self.source = ""  # 应用何定理得到
        self.conditions = []  # 该代理依赖的前提条件
        self.prove_load = []  # 证明该点的推理链
        self.weight = 100  # 该谓词的权重

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.p5 = p5
        self.ID = 0
        self.info_name = self.name + p1 + p2 + p3 + p4 + p5

    # 给前提条件编号
    def SetID(self, Id):
        self.ID = Id

    # 判断一个信息，是否已存在于列表中
    def IsInList(self, llist):
        set1 = set()
        set2 = set()
        set1.add(self.p1)
        set1.add(self.p3)
        set2.add(self.p4)
        set2.add(self.p5)
        for i in range(len(llist)):
            item = llist[i]
            set3 = set()
            set4 = set()
            set3.update(item.p1, item.p3)
            set4.update(item.p4, item.p5)
            if set1 == set3 and set2 == set4 and self.p2 == item.p2:
                return i
        return False

    def Print(self):
        if self.source == "已知":
            print("bisectorAngle", "(%s %s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5),
                  " (已知)")
        else:
            for info in self.conditions:
                info.Print()
            print("bisectorAngle", "(%s %s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5),
                  " (%s)" % self.source)

    def printSelf(self):
        print("bisectorAngle", "(%s %s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5))

    def printSelf_CN(self):
        print("∠%s%s%s的角平分线是%s%s" % (self.p1, self.p2, self.p3, self.p4, self.p5), end="")

    def printSelf_re(self):
        return "∠%s%s%s的角平分线是%s%s" % (self.p1, self.p2, self.p3, self.p4, self.p5)


# 互补角，不一定相邻
# ∠123+∠456=180°
class ComplementaryAngle(Information):
    def __init__(self, p1, p2, p3, p4, p5, p6):
        self.name = "互补角"
        self.source = ""  # 应用何定理得到
        self.conditions = []  # 该代理依赖的前提条件
        self.prove_load = []  # 证明该点的推理链
        self.weight = 100  # 该谓词的权重

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.p5 = p5
        self.p6 = p6
        self.ID = 0
        self.info_name = self.name + p1 + p2 + p3 + p4 + p5 + p6

    # 给前提条件编号
    def SetID(self, Id):
        self.ID = Id

    # 判断一个信息，是否已存在于列表中
    def IsInList(self, llist, colist):
        set1 = set()
        set2 = set()
        set1.add(self.p1)
        set1.add(self.p3)
        set2.add(self.p4)
        set2.add(self.p6)
        setco3 = set()
        setco4 = set()
        setco3.update(self.p1, self.p2, self.p3)
        setco4.update(self.p4, self.p5, self.p6)
        if self.p1 == self.p2 or self.p1 == self.p3 or self.p2 == self.p3:
            return True
        if self.p4 == self.p5 or self.p4 == self.p6 or self.p5 == self.p6:
            return True
        for i in range(len(colist)):
            setco = set()
            setco.update(colist[i].p1, colist[i].p2, colist[i].p3)
            if setco == setco3 or setco == setco4:
                return True
        for i in range(len(llist)):
            info = llist[i]
            set3 = set()
            set4 = set()
            set3.add(info.p1)
            set3.add(info.p3)
            set4.add(info.p4)
            set4.add(info.p6)
            if ((set1 == set3 and set2 == set4) and (self.p2 == info.p2 and self.p5 == info.p5)) or (
                    (set1 == set4 and set2 == set3) and (self.p2 == info.p5 and self.p5 == info.p2)):
                return i
        return False

    def Print(self):
        if self.source == "已知":
            print("ComplementaryAngle", "(%s %s %s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6),
                  " (已知)")
        else:
            for info in self.conditions:
                info.Print()
            print("ComplementaryAngle", "(%s %s %s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6),
                  " (%s)" % (self.source))

    def printSelf(self):
        print("ComplementaryAngle", "(%s %s %s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6))

    def printSelf_CN(self):
        print("∠%s%s%s + ∠%s%s%s = 180°" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6), end="")

    def printSelf_re(self):
        return "∠%s%s%s + ∠%s%s%s = 180°" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6)

# 互余角，不一定相邻
# ∠123+∠456=90°
class CoterminalAngles(Information):
    def __init__(self, p1, p2, p3, p4, p5, p6):
        self.name = "互余角"
        self.source = ""  # 应用何定理得到
        self.conditions = []  # 该代理依赖的前提条件
        self.prove_load = []  # 证明该点的推理链
        self.weight = 100  # 该谓词的权重

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.p5 = p5
        self.p6 = p6
        self.ID = 0
        self.info_name = self.name + p1 + p2 + p3 + p4 + p5 + p6

    # 给前提条件编号
    def SetID(self, Id):
        self.ID = Id

    # 判断一个信息，是否已存在于列表中
    def IsInList(self, llist, colist):
        set1 = set()
        set2 = set()
        set1.add(self.p1)
        set1.add(self.p3)
        set2.add(self.p4)
        set2.add(self.p6)
        setco3 = set()
        setco4 = set()
        setco3.update(self.p1, self.p2, self.p3)
        setco4.update(self.p4, self.p5, self.p6)
        if self.p1 == self.p2 or self.p1 == self.p3 or self.p2 == self.p3:
            return True
        if self.p4 == self.p5 or self.p4 == self.p6 or self.p5 == self.p6:
            return True
        for i in range(len(colist)):
            setco = set()
            setco.update(colist[i].p1, colist[i].p2, colist[i].p3)
            if setco == setco3 or setco == setco4:
                return True
        for i in range(len(llist)):
            info = llist[i]
            set3 = set()
            set4 = set()
            set3.add(info.p1)
            set3.add(info.p3)
            set4.add(info.p4)
            set4.add(info.p6)
            if ((set1 == set3 and set2 == set4) and (self.p2 == info.p2 and self.p5 == info.p5)) or (
                    (set1 == set4 and set2 == set3) and (self.p2 == info.p5 and self.p5 == info.p2)):
                return i
        return False

    def Print(self):
        if self.source == "已知":
            print("CoterminalAngle", "(%s %s %s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6),
                  " (已知)")
        else:
            for info in self.conditions:
                info.Print()
            print("CoterminalAngle", "(%s %s %s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6),
                  " (%s)" % (self.source))

    def printSelf(self):
        print("CoterminalAngle", "(%s %s %s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6))

    def printSelf_CN(self):
        print("∠%s%s%s + ∠%s%s%s = 90°" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6), end="")

    def printSelf_re(self):
        return "∠%s%s%s + ∠%s%s%s = 90°" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6)


# 内错角信息 ∠123 =∠456
class Alter_Inter_Angle(Information):
    def __init__(self, p1, p2, p3, p4, p5, p6):
        self.name = "内错角"
        self.source = ""  # 应用何定理得到
        self.conditions = []  # 该代理依赖的前提条件
        self.prove_load = []  # 证明该点的推理链
        self.weight = 100  # 该谓词的权重

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.p5 = p5
        self.p6 = p6
        self.ID = 0
        self.info_name = self.name + p1 + p2 + p3 + p4 + p5 + p6

    # 给前提条件编号
    def SetID(self, Id):
        self.ID = Id

    # 判断一个信息，是否已存在于列表中
    def IsInList(self, llist):
        set1 = set()
        set2 = set()
        set1.add(self.p1)
        set1.add(self.p3)
        set2.add(self.p4)
        set2.add(self.p6)
        for i in range(len(llist)):
            info = llist[i]
            set3 = set()
            set4 = set()
            set3.add(info.p1)
            set3.add(info.p3)
            set4.add(info.p4)
            set4.add(info.p6)
            if ((set1 == set3 and set2 == set4) and (self.p2 == info.p2 and self.p5 == info.p5)) or (
                    (set1 == set4 and set2 == set3) and (self.p2 == info.p5 and self.p4 == info.p5)):
                return i
        return False

    def Print(self):
        if self.source == "已知":
            print("Alter_Inter_Angle", "(%s %s %s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6),
                  " (已知)")
        else:
            for info in self.conditions:
                info.Print()
            print("Alter_Inter_Angle", "(%s %s %s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6),
                  " (%s)" % (self.source))

    def printSelf(self):
        print("Alter_Inter_Angle", "(%s %s %s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6))

    def printSelf_CN(self):
        print("∠%s%s%s与∠%s%s%s是一对内错角" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6), end="")

    def printSelf_re(self):
        return "∠%s%s%s与∠%s%s%s是一对内错角" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6)


# 全等三角形信息 ▲123 全等于 ▲456     需要顺序存储∠1=∠4 ∠2=∠5 ∠3=∠6
class EqualTriangle(Information):
    def __init__(self, p1, p2, p3, p4, p5, p6):
        self.name = "全等三角形"
        self.source = ""  # 应用何定理得到
        self.conditions = []  # 该代理依赖的前提条件
        self.prove_load = []  # 证明该点的推理链
        self.weight = 100  # 该谓词的权重

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.p5 = p5
        self.p6 = p6
        self.ID = 0
        self.info_name = self.name + p1 + p2 + p3 + p4 + p5 + p6

    # 给前提条件编号
    def SetID(self, Id):
        self.ID = Id

    # 判断一个信息，是否已存在于列表中
    def IsInList(self, llist, coLineList):
        set1 = set()
        set2 = set()
        set1.add(self.p1)
        set1.add(self.p2)
        set1.add(self.p3)
        set2.add(self.p4)
        set2.add(self.p5)
        set2.add(self.p6)
        if set1 == set2:
            return True
        for i in range(len(coLineList)):
            setco = set()
            setco.update(coLineList[i].p1, coLineList[i].p2, coLineList[i].p3)
            if setco == set1 or setco == set2:
                return True
        for i in range(len(llist)):
            info = llist[i]
            set3 = set()
            set4 = set()
            set3.add(info.p1)
            set3.add(info.p2)
            set3.add(info.p3)
            set4.add(info.p4)
            set4.add(info.p5)
            set4.add(info.p6)
            if (set1 == set3 and set2 == set4) or (set1 == set4 and set2 == set3):
                return i
        return False

    def Print(self):
        if self.source == "已知":
            print("equalTriangle", "(%s %s %s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6),
                  " (已知)")
        else:
            for info in self.conditions:
                info.Print()
            print("equalTriangle", "(%s %s %s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6),
                  " (%s)" % (self.source))

    def printSelf(self):
        print("equalTriangle", "(%s %s %s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6))

    def printSelf_CN(self):
        print("△%s%s%s≌△%s%s%s" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6), end="")

    def printSelf_re(self):
        return "△%s%s%s≌△%s%s%s" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6)


# 相似三角形信息 ▲123 相似于 ▲456
class SimilarTriangle(Information):
    def __init__(self, p1, p2, p3, p4, p5, p6):
        self.name = "相似三角形"
        self.source = ""  # 应用何定理得到
        self.conditions = []  # 该代理依赖的前提条件
        self.prove_load = []  # 证明该点的推理链
        self.weight = 100  # 该谓词的权重

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.p5 = p5
        self.p6 = p6
        self.ID = 0
        self.info_name = self.name + p1 + p2 + p3 + p4 + p5 + p6

    # 给前提条件编号
    def SetID(self, Id):
        self.ID = Id

    # 判断一个信息，是否已存在于列表中
    def IsInList(self, llist):
        set1 = set()
        set2 = set()
        set1.add(self.p1)
        set1.add(self.p2)
        set1.add(self.p3)
        set2.add(self.p4)
        set2.add(self.p5)
        set2.add(self.p6)
        for i in range(len(llist)):
            info = llist[i]
            set3 = set()
            set4 = set()
            set3.add(info.p1)
            set3.add(info.p2)
            set3.add(info.p3)
            set4.add(info.p4)
            set4.add(info.p5)
            set4.add(info.p6)
            if (set1 == set3 and set2 == set4) or (set1 == set4 and set2 == set3):
                return i
        return False

    def Print(self):
        if self.source == "已知":
            print("similarTriangle", "(%s %s %s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6),
                  " (已知)")
        else:
            for info in self.conditions:
                info.Print()
            print("similarTriangle", "(%s %s %s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6),
                  " (%s)" % (self.source))

    def printSelf(self):
        print("similarTriangle", "(%s %s %s %s %s %s)" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6))

    def printSelf_CN(self):
        print("△%s%s%s∽△%s%s%s" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6), end="")

    def printSelf_re(self):
        return "△%s%s%s∽△%s%s%s" % (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6)


# 共线信息 p1在p2和p3中间
class CoLine(Information):
    def __init__(self, p1, p2, p3, check=0):
        self.name = "共线"
        self.source = ""  # 应用何定理得到
        self.conditions = []  # 该代理依赖的前提条件
        self.prove_load = []  # 证明该点的推理链
        self.weight = 100  # 该谓词的权重

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.check = check  # check代表这条共线信息的第一个点即p1是不是位于p2和p3中间，如果是的话check的值为1，不是的话为0，默认为0
        self.ID = 0
        self.info_name = self.name + p1 + p2 + p3

    # 给前提条件编号
    def SetID(self, Id):
        self.ID = Id

    # 判断一个信息，是否已存在于列表中
    def IsInList(self, llist):
        set1 = set()
        set1.add(self.p1)
        set1.add(self.p2)
        set1.add(self.p3)
        if self.p1 == "#" or self.p2 == "#" or self.p3 == "#":
            return True
        if self.p1 == self.p2 or self.p1 == self.p3 or self.p3 == self.p2:
            return True
        for i in range(len(llist)):
            info = llist[i]
            set3 = set()
            set3.add(info.p1)
            set3.add(info.p2)
            set3.add(info.p3)
            if set1 == set3:
                return i
        return False

    def Print(self):
        if self.source == "已知":
            print("CoLine", "(%s %s %s)" % (self.p1, self.p2, self.p3),
                  " (已知)")
        else:
            for info in self.conditions:
                info.Print()
            print("CoLine", "(%s %s %s)" % (self.p1, self.p2, self.p3),
                  " (%s)" % (self.source))

    def printSelf(self):
        print("CoLine", "(%s %s %s) %s" % (self.p1, self.p2, self.p3, self.check))

    def printSelf_CN(self):
        # 这里把check去掉了
        print("%s%s%s三点共线" % (self.p1, self.p2, self.p3), end="")

    def printSelf_re(self):
        return "%s%s%s三点共线" % (self.p1, self.p2, self.p3)


# 等边三角形
class Regular_triangle(Information):
    def __init__(self, p1, p2, p3):
        self.name = "等边三角形"
        self.source = ""  # 应用何定理得到
        self.conditions = []  # 该代理依赖的前提条件
        self.prove_load = []  # 证明该点的推理链
        self.weight = 100  # 该谓词的权重

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.ID = 0
        self.info_name = self.name + p1 + p2 + p3

    # 给前提条件编号
    def SetID(self, Id):
        self.ID = Id

    # 判断一个信息，是否已存在于列表中
    def IsInList(self, llist):
        set1 = set()
        set1.add(self.p1)
        set1.add(self.p1)
        set1.add(self.p2)
        set1.add(self.p3)
        if len(set1) != 3:
            return True
        for i in range(len(llist)):
            info = llist[i]
            set3 = set()
            set3.add(info.p1)
            set3.add(info.p2)
            set3.add(info.p3)
            if (set1 == set3):
                return i
        return False

    def Print(self):
        if self.source == "已知":
            print("RegularTriangle", "(%s %s %s)" % (self.p1, self.p2, self.p3),
                  " (已知)")
        else:
            for info in self.conditions:
                info.Print()
            print("RegularTriangle", "(%s %s %s)" % (self.p1, self.p2, self.p3),
                  " (%s)" % self.source)

    def printSelf(self):
        print("RegularTriangle", "(%s %s %s)" % (self.p1, self.p2, self.p3))

    def printSelf_CN(self):
        print("△%s%s%s是等边三角形" % (self.p1, self.p2, self.p3), end="")

    def printSelf_re(self):
        return "△%s%s%s是等边三角形" % (self.p1, self.p2, self.p3)

# 圆
class Circle(Information):
    def __init__(self, o='null', **kwargs):
        self.name = "圆"
        self.source = ""  # 应用何定理得到
        self.conditions = []  # 该代理依赖的前提条件
        self.prove_load = []  # 证明该点的推理链
        self.weight = 100  # 该谓词的权重
        self.o = o
        self.ID = 0
        for key, value in kwargs.items():
            setattr(self, key, value)
        # 获取设置的所有属性及其值
        attributes = vars(self)
        for attr, value in attributes.items():
            self.info_name += value
    # 给前提条件编号
    def SetID(self, Id):
        self.ID = Id

    # 判断一个信息，是否已存在于列表中
    def IsInList(self, llist):
        for i in range(len(llist)):
            if self.o == llist[i].o:
                return i
        return False

    def Print(self):
        if self.source == "已知":
            print("Circle", "(%s)" % self.o, " (已知)")
        else:
            for info in self.conditions:
                info.Print()
            print("Circle", "(%s)" % self.o, " (%s)" % self.source)

    def printSelf(self):
        print("Circle", "(%s)" % self.o)

    def printSelf_CN(self):
        print("%s%s%s%s共圆" % (self.p1, self.p2, self.p3, self.p4))

    def printSelf_re(self):
        return "%s%s%s%s共圆" % (self.p1, self.p2, self.p3, self.p4)

class Test(Information):
    def __init__(self, p1):
        self.name = "测试"
        self.source = ""  # 应用何定理得到
        self.conditions = []  # 该代理依赖的前提条件
        self.prove_load = []  # 证明该点的推理链
        self.weight = 100  # 该谓词的权重

        self.p1 = p1
        self.ID = 0
        self.info_name = self.name + p1

    # 给前提条件编号
    def SetID(self, Id):
        self.ID = Id

    # 判断一个信息，是否已存在于列表中
    def IsInList(self, llist):
        for i in range(len(llist)):
            info = llist[i]
            if info.p1 == self.p1:
                return i
        return False

    def printSelf_CN(self):
        print("%s点的坐标是%s" % (self.p1), end="")

    def Print(self):
        if self.source == "已知":
            print("测试", "(%s )" % (self.p1), " (已知)")
        else:
            for info in self.conditions:
                info.Print()
            print("测试", "(%s )" % (self.p1))