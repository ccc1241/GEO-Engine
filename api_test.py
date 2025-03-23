from gpt_test import call_gpt4_api, string_parse, convert_to_example_thm, get_system_prompt, point_sort
import time
import concurrent.futures
from InterGPS.diagram_parser.detection import dia_test
from InterGPS.diagram_parser.parser import diagram_parser




textlist = ["平行四边形ABCD，连接AC，分别过B、D作AC的垂线交于E、F两点,使得BE⊥AC,DF垂直于AC，求证：BE=DF。",     # 3000  1
            "正方形 ABCD 及等边三角形EDC 如图位置放置，连接 AE，BE。求证:AE=BE。",
            "AD⊥DB，AC⊥CB，E、F是AB、CD的中点，求证：△CFE全等于△DFE。",
            "在平行四边形ABCD中，G对角线是BD的中点，过点G的直线EF 分别交AD，BC于E、F两点，连接BE，DF。求证:四边形BEDF是平行四边形。",
            "在正方形 ABCD 中，E是 BC 边上的一点，连接 AE，过点B作 BF⊥AE，垂足为 F，延长 BF交CD 于点G，连接 AG。求证:AE=BG",
            "在矩形ABCD中，E是AD的中点，延长CE，BA相交于点F，连接AC，DF。求证：四边形ACDF是平行四边形。",
            "在正方形ABCD中，E为CD边上的一点，F为BC的延长线上一点，CE=CF。求证：△BCE全等于△DCF",
            "三角形ABC中，∠BAC=90°,D、F、E分别为BC,CA,AB 的中点求证:EF =AD",
            "三角形ABC中，AB=AC,AD 是角平分线,DE,DF 分别垂直于AB、AC.求证:EB=FC",
            "平行四边形AEBD，在△ACE的两边，ADC是等边三角形、ECB是等边三角形.求证：BD⊥DA",
            "平行四边形ABCD，圆内接四边形ABCD，AC交BD于E. 求证：AB⊥BC。",  # 3010  11
            "在△ABC中,AB=AC,点D为BC的中点,连结AD,点E为AD的中点,作DG⊥BE于点G,点F为AC的中点. 求证：GF=DF。",
            "在△ABC中，∠ABC=90°，AD是∠BAC的平分线，DE⊥AC于点E，点F在AB上，CD=DF．求证：BF=EC",
            "△ABC中，CA=CB，作CD⊥AB，BE⊥CA，垂足分别为D，E，CD和BE相交于点F，若已知CE=BE．求证：△CEF≌△BEA",
            "如图，AC∥BE，AF=DB，∠ACD=∠FEB，A、F、D、B四点在同一直线上．求证：CD∥FE．",
            "已知在△ABC中，高线AD，BE相交于点F，点G是BF的中点，∠ABC=45°．求证：△BDF≌△ADC．",  # 3015    16
            "在四边形ABCD中，BC=DC，AB=AD，E为线段AC上一点，求证：EB=ED．",
            "△ABC中，AD⊥BC于D，BE平分∠ABC，AF=AE．求证：AB⊥AC．",
            "△ADC和△BEC中，点C为AB上一点，DC=CE，AD=BC，AC=BE，求证：AD∥BE",
            "△ABC和△DBC中, AC、DB相交于点E，AB=DC，AC=DB．求证：∠BAC=∠BDC",
            "在△ADE和△BCF中，点C、D在AB上，AC=DB，AE=BF，∠EAB=∠FBA．求证：∠AED=∠BFC",          # 3020  21
            "D是△ABC中BC上一点，且BD=CD，BE⊥AD，交AD的延长线于点E，CF⊥AD，垂足为F．求证：BE=CF",
            "在△ACD和△BCF中，点A、B、C、D在一条直线上，AC=DB，ED=FB，∠EDA=∠ABF．求证：AE=CF",
            "△ABC和△ADE是底边在同一条直线上的两个等腰三角形，求证：BD=CE",
            "在△ADC和△CEB中, 点C是AB的中点，CD=BE，AD=CE, 求证：△ADC≌△CEB",
            "在△ACD中，∠ACD=90°，AC=DC，AB⊥CB于B，DE⊥CB于E．求证：△DEC≌△CBA",
            "ABCD是平行四边形，AE⊥BD于点E，CF⊥BD于点F，BF=DE．求证：△ABE≌△CDF",
            "在△ABC和△DEF中, 已知点B，E，C，F在一条直线上，BE=CF，AC∥DE，∠BAC=∠FDE．求证：△ABC≌△DFE",
            "在△CAB和△DBA中, 已知∠ACB=∠ADB=90°，CB与DA交于点E，且CB=DA．求证：△CAB≌△DBA",
            "在△AED和△BFC中,点A、C、D、B共线，AE=BF，∠EAB=∠FBA，AC=BD．求证：△AED≌△BFC",
            "在△ABC和△ADE中, ∠BAE=∠CAD，AB=AE，AC=AD．求证：BC=ED",          # 3030
            "在△AED和△AFD中, 已知∠E=∠F=90°，点B，C分别在AE，AF上，AB=AC，BD=CD．求证：△ABD≌△ACD",  # 有问题
            "在△ACE和△BDF中, ACDB在同一条直线上. AE=BF, AC=BD, AE∥BF. 求证：CE=DF",
            "在Rt△ADC和△BEF中，AFDB四点共线，∠A=90°，AF=DB，CD=FE，且AC∥BE．求证：AC=BE",
            "在△ADC和△BFE中, A、F、D、B在同一直线上，AC=BE，AF=BD，∠CAD=∠EBF. 求证：△ADC≌△BFE",
            "在Rt△CAB中，∠ACB=90°，CB=2AC，点D是CB的中点．将一块锐角为45°的直角三角板如图放置，使三角板斜边的两个端点分别与C、D重合，连接AE、EB．求证：△CAE≌△DBE",
            "在△ADC和△CED中，B是两三角形外一点，连接BA、BC、BE，已知AC=DC，AB=DE，∠CAB=∠CDE, 求证：CB=CE",
            "在△ABF和△CDE中，点E，F在BC上，AB=DC，AF=DE，∠BAF=∠CDE．求证：△ABF≌△DCE",
            "在△ABE和△DAC中，E是AD上一点，AB=AD，AB∥CD，∠AEB=∠ACD，求证：△ABE≌△DAC",
            "在△ABC中，点D为线段BC上一点，BD=AC，过点D作DE∥AC且∠DBE=∠BAC，求证：DE=BC",
            "AC与BD相交于点E，AC=BD，EA=EB，求证：∠ADB=∠ACB",
            "在△ABC和△DEF中，点B，F，C，E在一条直线上，AB=DE，AB∥DE，BF=EC．求证：△ABC≌△DEF",
            "在△ABC中，E是AB上一点，DE交AC于点F，DF=FE，DC∥AB．求证：点F为AC中点",
            "在△ABC和△DEF中，点B、E、C、F在一条直线上，AB=DE，AC=DF，BE=CF．求证：△ABC≌△DEF.",
            "在△ABD和△ACE中，E是AB上一点，D是AC上一点，BD和CE交于F点，AB=AC，AD=AE．求证：△ABD≌△ACE",
            "在△ACE和△ABD中, A，E，D三点在同一直线上，AB=AC，∠BAC=∠BDF=∠CEF．求证：AE=BD",
            "在△ACE和△ABD中, AB与CD交于点F，BE与AC交于点G，AB=AC，AF=AG，∠ADC=∠AEB．求证：AD=AE",
            "在△ABC中，CD⊥AB于点D，且CD=BD，在CD上取一点E，使得DE=DA，连接BE，AE．求证：∠ACD=∠EBD",
            "在△ACD和△CBE中，点C为AB中点，CD=BE，CD∥BE．求证：△ACD≌△CBE",
            "在△ABC和△DEF中，B，F，C，E四点在同一条直线上，AB∥ED，AB=DE，BF=EC，连接AD交BE于O．求证：AC∥FD",
            "在△ABC和△DEF中，B，F，C，E四点在同一条直线上，AB∥ED，AB=DE，BF=EC，连接AD交BE于O．求证：OA=OD",# 3050 51
            "在△ABC中，AB=AC，AD是BC边上的中线，CE⊥AB于点E．求证：∠CAD=∠BCE",
            "已知△ABC，E是AB延长线上一点，CD平分它的外角∠BCE，AB∥CD，求证：CA=CB",
            "△ABC为等边三角形，BD⊥AC交AC于点D，DE∥BC交AB于点E．求证：△ADE是等边三角形",
            "△ABC为等边三角形，BD⊥AC交AC于点D，DE∥BC交AB于点E．求证：AE=1/2AB",
            "在△ABC中，AB=AC，AD是BC边上的中线，CE⊥AB于点E．求证：∠CAD=∠BCE",
            "四边形ABCD中，∠ABC=∠BCD=90°，E是BC的中点，DE平分∠ADC．求证：AE平分∠BAD",
            "四边形ABCD中，∠ABC=∠BCD=90°，E是BC的中点，DE平分∠ADC．求证：△ADE是直角三角形",
            "在△ABC中, AB=AC，D是AB上一点，DE⊥BC于点E，ED的延长线交CA的延长线于点F．求证：△ADF是等腰三角形",
            "在△ABC中, O为BC、ED中点，直线OD交AC于点E. 求证△BDO≌△CEO",
            "在△AEC中,B是AE上一点，D是EC上一点 DE⊥AB于E，DF⊥AC于F，若BD=CD，BE=CF．求证：AD平分∠BAC",
            "在四边形ABED中，C是BE延长线上一点，连接DC，已知∠ABC=∠DCB，AB∥DE，DE交BC于点E．求证：△DEC是等腰三角形",
            "△ABC中，D为AC边上一点，DE⊥AB于E，ED的延长线交BC的延长线于F，且CD=CF．求证：△ABC是等腰三角形",
            "在△ABC中，AB=AC，点D是BC的中点，连接AD，过点C作CE∥AD，交BA的延长线于点E．求证：EC⊥BC",
            "在等边三角形ABC的三边上，分别取点D，E，F，使AD=BE=CF．求证：△DEF是等边三角形",
            "在△ABC中，AB=AC，点D、E、F分别在AB、BC、AC上，且BD=CE，BE=CF．求证：△DEF是等腰三角形",
            "在△ABC中，AB=AC，D为BC的中点，DE⊥AB，DF⊥AC，垂足分别为E、F，求证：DE=DF",
            "在△ABC中，D是BC上一点，DE是线段AB的垂直平分线，AD=CD．求证：AC⊥AB",
            "在四边形ABCD中，AD∥BC，BD平分∠ABC．求证：AB=AD",
            "△ABC中，AB=AC，AC与AB边上的高BD、CE相交于点O．求证：△OBC是等腰三角形",
            "在△ABC中，AB=AC，D为BC边上一点，∠ABC=30°，∠DAB=45°．求证：△ADC是等腰三角形",# 3070
            "在△ABC中，AB的垂直平分线EF交BC于点E，交AB于点F，D为线段CE的中点，BE=AC．求证：AD⊥BC",
            "在△ABC中，边AB的垂直平分线EF分别交边BC，AB于点E，F，过点A作AD⊥BC于点D，且D为线段CE的中点．求证：BE=AC",
            "△ABC是等边三角形，DE∥BC，分别交AB，AC于点D，E．求证：△ADE是等边三角形",
            "等边三角形ABC的∠BAC和∠ABC的两条角平分线相交于点D，延长BD至点E，使得AE=AD，求证：△ADE是等边三角形",
            "△ABC中，AD⊥BC，EF垂直平分AC，交AC于点F，交BC于点E，且BD=DE，连接AE．求证：AB=EC",
            "D，E分别在AB，AC上，∠ADC=∠AEB=90°，BE，CD相交于点O，OB=OC．求证：∠BAO=∠OAC",
            "在△ABC和△DEF中，点B、E、C、F在同一条直线上，AC∥DF，BE=CF；AC=DF，求证：AB∥DE",
            "在△ABF和△DEC中，点E，F在BC上，BE=CF，AB=DC，∠ABC=∠CDB，AF与DE交于点G．求证：△ABF≌△DCE",
            "在锐角△ABC中，∠ABC=45°，点D为BC的中点，AE⊥BC于点E，点F在AE上，且EF=EC，CG∥BF交FD的延长线于点G．求证：BF=AC",
            "△ABC与△DCB中，AC与BD交于点E，且∠ABD=∠DCA，AB=DC．求证：△ABE≌△DCE",
            "△ABE与△DCF中,A、E、F、D在一条直线上，BE⊥AD，CF⊥AD，垂足分别为点E，F，AF=DE，∠ABE=∠DCF，求证：AB=CD",
            "在四边形ABCD中，已知AB=DC，AB∥CD，E、F是AC上两点，且AF=CE．求证：△ABE≌△CDF",
            "在△ABC和△DEF中，B，E，C，F在同一条直线上, AB=DE, BE=CF, ∠ABC=∠DEF．求证：△ABC≌△DEF",
            "已知△ABC中，D为BC上一点，E为△ABC外部一点，DE交AC于一点O，AC=AE，AD=AB，∠BAC=∠DAE．求证：△ABC≌△ADE",
            "在△ABC和△CED中，E是BC上一点，∠BAC=∠CED，AB∥CD，BC=CD．求证：△ABC≌△ECD．",
            "四边形ABCD中，对角线AC、BD交于点O，AB=AC，点E是BD上一点，且∠ABD=∠ACD，∠EAD=∠BAC．求证：AE=AD",
            "在△ABC和△CED中，B、C、E三点在同一条直线上，AC∥DE，AC=CE，∠ACD=∠ABC．求证：BC=DE",
            "在△ABC中，D是BC上一点，AD平分∠BAC，DE⊥AC，垂足为E，BF∥AC交ED的延长线于点F，若BC恰好平分∠ABF．求证：点D为EF的中点",
            "在△ABC中，D是BC上一点，AD平分∠BAC，DE⊥AC，垂足为E，BF∥AC交ED的延长线于点F，若BC恰好平分∠ABF．求证：AD⊥BC",
            "在△ABC和△FED中, 点A、C、F、D在同一直线上，AB∥DE，AF=DC，∠ABC=∠DEF，求证：BC=EF", # 3090
            "在△ABC中AD是BC边上的中线，过C作AB的平行线交AD的延长线于E点．求证：AB=EC",
            "在△ABC、△ADE中，∠BAC=∠DAE=90°，AB=AC，AD=AE，点C、D、E三点在同一直线上，连接BD．求证：△BAD≌△CAE",
            "在△ABC和△DEF中，A、C、F、D在同一直线上，AF=DC，AB∥DE，AB=DE，求证：△ABC≌△DEF",
            "在△ABC和△DEF中，A、C、F、D在同一直线上，AF=DC，AB∥DE，AB=DE，求证：BC∥EF",
            "在△ABC中，AD⊥BC于D，CE⊥AB于E，AD与CE交于点F，且AD=CD．求证：△ABD≌△CFD",
            "在△AFC和△ABD和△ACE中，B在FC上，D在EC上，∠BAD=∠CAE=90°，AB=AD，AE=AC，AF⊥CB，垂足为F．求证：△ABC≌△ADE",
            "在△ABC和△DEF中，点B，F，C，E在同一直线上，AB=DE，BF=CE，AB∥DE，求证：△ABC≌△DEF．",
            "△ABC中，AB=BC，∠ABC=90°，F为AB延长线上一点，点E在BC上，且AE=CF．求证：△ABE≌△CBF",
            "在△ABC和△DEF中，点B、F、C、E在一条直线上，OA=OD，AC∥FD，AD交BE于O．求证：△ACO≌△DFO",
            "在△ADF和△CBE中, 点A、E、F、C在同一直线上，AD∥BC，AD=CB，AE=CF．求证：∠CBE=∠FDA．",
            "在△ABC中，D是BC的中点，过D点的直线EG交AB于点E，交AB的平行线CG于点G，DF⊥EG，交AC于点F. 求证：BE=CG",
            "点A、E、F、B在同一条直线上，CA⊥AB，DB⊥AB，AE=FB，CF=DE．求证：∠AFC=∠DEB",
            "AB⊥BC，CD⊥DA，AB=CD．AB和DC相交于点O，求证：OB=OD．",
            "点D在△ABC的BC边上，AC∥BE，BC=BE，∠ABC=∠BED，求证：AB=DE．",
            "在△ABC和△CDE中，点E、A、C在同一直线上，AB∥CD，∠ABC=∠DEC，AC=CD, ∠BAC=∠ECD.求证： BC=ED",
            "Rt△ABC中，∠ACB=90°，M是边AB的中点，CH⊥AB于点H，CD平分∠ACB．",
            "在△ABC中，∠ACB=90°，AC=BC，BE⊥CE于E，AD⊥CE于D．求证：△ADC≌△CEB．",
            "在△ABC中，BE、CF分别是AC、AB两边上的高，在BE上截取BD=AC，在CF的延长线上截取CG=AB，连接AD、AG. 求证AD=AG",
            "已知ACD三点，AB平分∠CAD，AC=AD．求证：∠ACB=∠BDA",
            "在△ABC和△DEF中，F、C是AD上的两点，且AB=DE，AB∥DE，AF=CD．求证：△ABC≌△DEF",   # 3110
            "在△ABC和△DEF中，F、C是AD上的两点，且AB=DE，AB∥DE，AF=CD．求证：BC∥EF",
            "在△AED和△ABC中，AE⊥AB，BC⊥AB，AE=AB，ED=AC．求证：ED⊥AC",
            "在△ABC中，AB=AC，D，E分别是边BC，AC上的点，且BD=EC，∠ADE=∠ABC．求证：AD=DE",
            "OC平分∠AOB，点D，E分别在OA，OB上，点P在OC上且有PD=PE．求证：∠PDO=∠PEB．",
            "已知：AC∥DF，点B为线段AC上一点，连接BF交DC于点H，过点A作AE∥BF分别交DC、DF于点G、点E，DG=CH，求证：△DFH≌△CAG",
            "已知：点A、F、E、C在同一条直线上，AF=CE，BE∥DF，BE=DF．求证：△ABE≌△CDF",
            "已知点B、E、F、C在同一条直线上，BE=CF，AF∥DE，AF=DE，求证：AB∥CD",
            "在四边形ABCD中，AB∥CD，E为AD的中点，连接CE并延长交BA的延长线于点F．求证：△CDE≌△FAE",
            "已知，△ABC中，AB=AC，D、E分别是AC、AB上的点，M、N分别是CE，BD上的点，若MA⊥CE，AN⊥BD，AM=AN．求证：△ABN≌△ACM",
            "已知，△ABC中，AB=AC，D、E分别是AC、AB上的点，M、N分别是CE，BD上的点，若MA⊥CE，AN⊥BD，AM=AN．求证：EM=DN",
            "在△AED和△ABC中，D在CE上，AB=AC，AD=AE，∠BAC=∠DAE．求证：△ABD≌△ACE",
            "在△ABD和△ACD中，AB=AC，BD=CD，求证：AD平分∠BAC",
            "在△ABF和△ECD中，BEFC在一条直线上，已知AB∥CD，AB=CD，BE=CF．求证：AF∥DE",
            "在△ABC中，AB=AC，△ABC的两条高CD、BE交于点F．求证：CD=BE",
            "在△ABC中，AB=AC，D为BA延长线上一点，E为BC上一点，DC=DE．求证：∠BDE=∠ACD",
            "在△ABC和△DEF中，BECF在同一直线上，已知AB=DE，AC=DF，BE=CF，AC与DE相交于点H．求证：△ABC≌△DEF",
            "在△ABC中，已知D是三角形中一点，CA=CB，AD=BD，M、N分别是CA、CB的中点，求证：DM=DN",
            "在△AEC和△BED中，∠EAC=∠DBE，AE=BE，点D在AC边上，∠DEC=∠BEA，AE和BD相交于点O．求证：△AEC≌△BED",
            "在四边形ABCD中，AB∥CD，∠BDA=∠ECD，AD=EC．求证：△ABD≌△EDC",
            "ABC和△DBC中，∠ACB=∠DBC=90°，E是BC的中点，且ED⊥AB于点F，且AB=DE． 求证：BD=2EC",  # 3130
            "△ABF和△DEC中，BEFC在同一直线上，∠BAC=∠CDB=90°，点B，E，F，C在同一直线上，AB=CD，BE=CF，求证：∠ABC=∠DCE",
            "△ABF和△DEC中，点E在边AC上，已知AB=DC，∠CAB=∠CDE，BC∥DE．求证：△ABC≌△DCE",
            "在△ABF和△DEF中，A、D、C、F在一条直线上，BC与DE交于点G，AD=CF，AB=DE，BC=EF，求证：∠CBA=∠FED",
            "在△AEC和△DBF中，点A，B，C，D在同一条直线上，AB=CD，AE=DF，CE=BF．求证：∠AEC=∠DFB．",
            "点C、D在线段AB上，且AC=BD，AE=BF，AE∥BF，连接CE、DE、CF、DF，求证CF=DE",
            "在△ABE和△DCF中，点B，F，E，C在同一条直线上，若AB∥CD，AB=CD且CE=BF．求证：AE=DF",
            "在四边形ABCD中，已知AB=AD，CB=CD，E是AC上一点，求证：∠AEB=∠AED",
            "在四边形ABCD中，AD∥BC，E为CD中点，连接AE并延长交BC的延长线于点F．求证：CF=AD",
            "在四边形ABCD中，AB=AD，AC是∠BAD的角平分线．求证：△ABC≌△ADC",
            "四边形ABDC中，∠CDB=∠ABD=90°，点O为BD的中点，且OA⊥OC．求证：CO平分∠ACD",
            "在四边形ABCD中，AD∥BC，E为CD的中点，连接AE、BE，延长AE交BC的延长线于点F．求证：CF=AD",
            "四边形ABCD的对角线AC、BD交于点O，已知O是AC的中点，AE=CF，DF∥BE．求证：△BOE≌△DOF",
            "四边形ABCD中，∠ABC=90°，AB∥CD，M为BC边上的一点，且AM平分∠BAD，DM平分∠ADC，求证：AM⊥DM",
            "在四边形ABCD中，AB=AD，BC=DC，E为AC上的一动点（不与A重合），求证：BE=DE",
            "四边形ABCD中，AD=BC，BE=DF，AE⊥BD，CF⊥BD，垂足分别为E、F．求证：△ADE≌△CBF",
            "四边形ABCD中，AD=BC，BE=DF，AE⊥BD，CF⊥BD，垂足分别为E、F．若AC与BD相交于点O，求证：AO=CO",
            "在△ABC中，AD是BC边上的中线，E是AD的中点，延长BE到F，使BE=EF，连接AF、CF、DF．求证：AF=BD",
            "四边形ABCD中，E为BC边上一点，∠ABC=∠AED=∠BCD，AB=EC，求证：AE=ED",
            "在四边形ABCD中，AD∥BC，AB⊥AD，BC=CD，BE⊥CD，垂足为点E，点F在BD上，连接AF、EF．求证：AD=ED",
            "在四边形ABCD中，AB=CD，对角线AC、BD相交于点O，且AC=BD，求证OA=OD",# 3150
            "在四边形ABCD中，AD=BC，∠DAB=∠CBA，E为AB的中点，连接CE，DE．求证：△ADE≌△BCE",
            "在四边形ABCD中，AD∥BC，∠BAD=90°，BD=BC，CE⊥BD于E．求证：BE=AD",
            "在△ABC中，D是BC边上的一点，连接AD，E是AD边上的中点，过点A作BC的平行线交CE的延长线于点F，且AF=BD，连接BF．求证：BD=CD",
            "在四边形ABCD中，AB=AD，AC是∠BAD的角平分线．求证：△ABC≌△ADC",
            "如图，在等边△ABC中,点D在边AB上,点E在CB的延长线上,且AD=BE.点F是CD的中点.求证:AF⊥FE",# 3155
            "如图，在等边△ABC中,点D在边AB上,点E在CB的延长线上,且AD=BE.点F是CD的中点.求证:DC=DE.",
            "如图，△ABC中,AH为高,AM为中线.点X,Y分别位于直线AB,AC上,且AX=XC,AY=YB, XY的中点是K.求证:K到点H和M的距离相等",
            "如图，在△ABC中，BA⊥BC，BD是高，BE是中线，过D作BE的垂线交直线BA于F，交直线BC于G，求证DF=DG.",
            "如图，在△ABC中，延长BC到D，使得CD=BC，延长CA到E，使得AE=2CA. 若∠BAC=90°，求证：DA=BE",
            "已知:M,N分别是平行四边形ABCD 的边AB,CD 的中点,E,F分别为AN,CM与BD的交点，求证:BF=FE",
            "已知:M,N分别是平行四边形ABCD 的边AB,CD 的中点,E,F分别为AN,CM与BD的交点，求证:ED=FE",
            "已知:M,N分别是平行四边形ABCD 的边AB,CD 的中点,E,F分别为AN,CM与BD的交点，求证:BF=ED",
            "在矩形ABCD中,延长 CB到E,使CE=CA,F是AE的中点求证:BF⊥DF",
            "已知以△ABC的AB 边为一边作平行四边形ABDE，并使DA // BC交EC于F.求证:EF =FC",
            "E为平行四边形ABCD 的边DC上的一点,过E作DB的平行线交CB于F,连AE,AF 分别交DB于M,N求证，DM=NB",
            "AD,CE是△ABC的高线,在AB 上取点F,使AF=AD,过F作 BC 的平行线交AC于G.求证:FG=CE.",
            "在△ABC中，∠ACB=90°,CH⊥AB，AD=DC,CE 平分∠ACH,DE与CH的延长线相交于点F，求证:BF // CE.",
            "AD是△ABC的中线,过CD 上任意一点F作EG //AB,与AC和AD 的延长线分别相交于G,E,FH //AC交AB于点H,求证：BE=GH.",
            "△ABC中,D为BC的中点,O为AD上一点,BO交AC于E,CO交AB于F.求证:EF // BC.",
            "△ABC中,AC=BC，∠C=90°,O为BC中点,由C引AO的垂线交AB于D,E为垂足.求证:AD=2BD.",
            "三角形ABC中,AB=AC，过A作BC的平行线分别交∠ABC的平分线BD于E,交∠ACB的平分线CF于G.求证:DE=FG",
            "C为线段AB 上一点,分别以AC,CB 为一边在AB 的同侧作正三角形ACD与正三角形ECB.",
            "已知三角形ABC的，D是BC的中点。CF垂直AD于F点，BE垂直AD于E点。求证：BE=CF.",
            "AB平行于ED，∠EAB=∠BDE，AF=CD,EF=BC,求证：∠F=∠C.",
            "G在线段DB上，E在线段DB上，AC平行于EF，∠CAB=∠DFE,AB=DC,求证：AB平行于DC。",
            "∠BAD=∠CAD,CD=DE,EF平行于AB,求证EF=AC.",
            "三角形ABC是等腰直角三角形，三角形ADE也是等腰直角三角形，B、C、D在同一条直线上，求证：三角形ABE全等于三角形ACD",
            "已知D是AB上的一点，CE平行于AB，DE与AC交于点O，且OA=OC。求证ADCE是平行四边形。",
            "F是线段AD上的一点，C也是线段AD上的一点，AB∥DE,AF∥DC,连接AE、BD,求证ABDE是平行四边形。",
            "在平行四边形ABCD中，AE⊥BC,CF⊥AD,垂足分别是E、F。求证：三角形ABE≌三角形CDF。",
            "已知ABCD是平行四边形，DE平行AC，交BC的延长线于点E，EF⊥AB于点F，求证AD=CF。",
            "在正方形ABCD中，点E在对角线AC上，点F在边BC上，连接BE，DF与对角线AC的交点是G，且DE=DG，求证：AE=CG.",
            "在正方形ABCD中，点E在对角线AC上，点F在边BC上，连接BE，DF与对角线AC的交点是G，且DE=DG，求证：BE∥DF",
            "ABCD是正方形，点E在BC的延长线上，DF⊥AE于点F,BG⊥AE于点G，且∠ABG=∠AEB，求证：AG=DF。",
            "如图，在平行四边形 ABCD中，点G，H分别是 AB，CD的中点，点E、F在对角线AC上，且AE=CF.求证:四边形EGFH是平行四边形.",
            "如图，在平行四边形 ABCD中，点G，H分别是 AB，CD的中点，点E、F在对角线AC上，且AE=CF.求证:三角形AGF≌三角形CHE.",
            "已知，如图，在RtABC中，∠ACB=90°，D、E分别是AB、AC的中点，F是BC延长线上的一点，且EF∥DC，求证:四边形CDEF是平行四边形:",
            "如图，在平行四边形ABCD中，点E是CD的中点，点F是BC边上的一点，且EF⊥AE. 线段FE与线段AD交于点M.求证:∠DAE=∠FAE.",
            "在△ABC中, O为BC、ED中点，直线OD交AC于点E. 求证△BDO≌△CEO",
            "在△AEC中,B是AE上一点，D是EC上一点 DE⊥AB于E，DF⊥AC于F，若BD=CD，BE=CF．求证：AD平分∠BAC",
            "在△ABC中，AB=AC，点D是BC的中点，连接AD，过点C作CE∥AD，交BA的延长线于点E．求证：EC⊥BC；",
            "在等边三角形ABC的三边上，分别取点D，E，F，使AD=BE=CF．求证：△DEF是等边三角形",
            "在四边形ABCD中，AD∥BC，BD平分∠ABC．求证：AB=AD．",
            "在△ABC中，AB的垂直平分线EF交BC于点E，交AB于点F，D为线段CE的中点，BE=AC．求证：AD⊥BC．",
            "等边三角形ABC的∠BAC和∠ABC的两条角平分线相交于点D，延长BD至点E，使得AE=AD，求证：△ADE是等边三角形．",
            "在△ABC和△DEF中，点B、E、C、F在同一条直线上，AC∥DF，BE=CF；AC=DF，求证：AB∥DE．",
            "在锐角△ABC中，∠ABC=45°，点D为BC的中点，AE⊥BC于点E，点F在AE上，且EF=EC，CG∥BF交FD的延长线于点G．求证：BF=AC",
            "在四边形ABCD中，已知AB=DC，AB∥CD，E、F是AC上两点，且AF=CE．求证：△ABE≌△CDF",
            "已知△ABC中，D为BC上一点，E为△ABC外部一点，DE交AC于一点O，AC=AE，AD=AB，∠BAC=∠DAE．求证：△ABC≌△ADE"
            ]


def text(which_title):
    user_input = textlist[which_title-1]
    messages = []
    messages.append({"role": "user", "content": get_system_prompt() + user_input})
    # 获取GPT-4的响应
    assistant_reply = call_gpt4_api(messages)
    parsed_string = string_parse(assistant_reply)
    return parsed_string


def diagram(which_title):
    res_json = None
    which_title += 2999
    path_to_dia = 'diagram-test/' + str(which_title) + '.png'
    # 第一步，图像分析
    dia_test.main('diagram-test', 'csv_retinanet_1.pt', 'classes.txt', 'test_results', 'test_results/ocr_results',
                  list(range(which_title, which_title+1)))
    # 第二步，坐标处理
    res_json = diagram_parser.main('test_results/ocr_results', 'test_results/box_results', path_to_dia,
                                   list(range(which_title, which_title+1)))
    return res_json


def main(which_title):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 提交两个函数的执行任务
        future_text = executor.submit(text, which_title)
        future_dia = executor.submit(diagram, which_title)
        # 等待两个任务完成
        concurrent.futures.wait([future_text, future_dia])
        # 获取任务的结果
        res_dia = future_dia.result()
        res_text = future_text.result()
        # circle = res_dia["circle_instances"]
        diagram_relationship = res_dia["diagram_logic_forms"]
        point_positions = res_dia["point_positions"]
        return diagram_relationship, point_positions, res_text


if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 提交两个函数的执行任务
        future_text = executor.submit(text)
        future_dia = executor.submit(diagram)
        # 等待两个任务完成
        concurrent.futures.wait([future_text, future_dia])
        # 获取任务的结果
        res_dia = future_dia.result()
        res_text = future_text.result()
        # circle = res_dia["circle_instances"]
        diagram_relationship = res_dia["diagram_logic_forms"]
        point_positions = res_dia["point_positions"]
