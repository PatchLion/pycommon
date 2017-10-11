from .ArgsChecker import *
import unittest

class ApiTest(unittest.TestCase):
    args = {"name": "lucy",
                "age": 90,
                "height": 172,
                "nick": "Baby",
                "levels": {"Math": 'A', "Chinese": 'A'},
                "firends": []}
    def test_BooleanChecker(self):
        ck1 = ArgsChecker(self.args)
        sex = ck1.addBooleanChecker(name="sex", is_req=True)
        self.assertEquals(sex, None)
        self.assertEquals(ck1.checkResult()[0], False)

        self.args["sex"] = False
        ck1 = ArgsChecker(self.args)
        sex = ck1.addBooleanChecker(name="sex", is_req=True)
        self.assertEquals(sex, False)
        self.assertEquals(ck1.checkResult()[0], True)

        ck2 = ArgsChecker(self.args)
        nick = ck2.addBooleanChecker(name="nick", is_req=True)
        self.assertEquals(nick, None)
        self.assertEquals(ck2.checkResult()[0], False)

        ck3 = ArgsChecker(self.args)
        nick2 = ck3.addBooleanChecker(name="nick2", is_req=False)
        self.assertEquals(nick2, None)
        self.assertEquals(ck3.checkResult()[0], True)

    def test_ArrayChecker(self):
        ck1 = ArgsChecker(self.args)
        firends = ck1.addArrayChecker(name="firends", is_req=True)
        self.assertEquals(firends, None)
        self.assertEquals(ck1.checkResult()[0], False)

        ck1 = ArgsChecker(self.args)
        firends = ck1.addArrayChecker(name="firends", is_req=False)
        self.assertEquals(firends, None)
        self.assertEquals(ck1.checkResult()[0], False)

        ck2 = ArgsChecker(self.args)
        cards = ck2.addArrayChecker(name="cards", is_req=False)
        self.assertEquals(cards, None)
        self.assertEquals(ck2.checkResult()[0], True)

        self.args["cards"] = ["恒丰银行"]
        ck3 = ArgsChecker(self.args)
        cards = ck3.addArrayChecker(name="cards", is_req=False)
        self.assertEquals(len(cards),1)
        self.assertEquals(ck3.checkResult()[0], True)


        self.args["skills"] = ["吉他"]
        ck4 = ArgsChecker(self.args)
        skills = ck4.addArrayChecker(name="skills", value_range=["吉他", "架子鼓", "声乐", "其他"], is_req=False)
        self.assertEquals(len(skills),1)
        self.assertEquals(ck4.checkResult()[0], True)

        self.args["skills"].append("非洲手鼓")
        ck4 = ArgsChecker(self.args)
        skills = ck4.addArrayChecker(name="skills", value_range=["吉他", "架子鼓", "声乐", "其他"], is_req=False)
        self.assertEquals(skills, None)
        self.assertEquals(ck4.checkResult()[0], False)

        ck4 = ArgsChecker(self.args)
        skills = ck4.addArrayChecker(name="skills", value_range=["非洲手鼓", "吉他", "架子鼓", "声乐", "其他"], is_req=False)
        self.assertEquals(len(skills), 2)
        self.assertEquals(ck4.checkResult()[0], True)

    def test_DictChecker(self):
        ck1 = ArgsChecker(self.args)
        levels = ck1.addDictChecker(name="levels", is_req=True)
        self.assertEquals(len(levels.keys()), 2)
        self.assertEquals(ck1.checkResult()[0], True)

        ck2 = ArgsChecker(self.args)
        levels = ck2.addDictChecker(name="levels", keys=['Math', 'Chinese'], is_req=True)
        self.assertEquals(len(levels.keys()), 2)
        self.assertEquals(ck2.checkResult()[0], True)

        ck3 = ArgsChecker(self.args)
        levels = ck3.addDictChecker(name="levels", keys=['Math', 'Chinese', 'English'], is_req=True)
        self.assertEquals(levels, None)
        self.assertEquals(ck3.checkResult()[0], False)

        ck4 = ArgsChecker(self.args)
        levels = ck4.addDictChecker(name="levels", keys=['Math', 'English'], is_req=True)
        self.assertEquals(levels, None)
        self.assertEquals(ck4.checkResult()[0], False)

    def test_NumberChecker(self):
        ck1 = ArgsChecker(self.args)
        age = ck1.addNumerChecker(name="age", range=(0, 150), is_req=True)
        self.assertEquals(age, 90)
        self.assertEquals(ck1.checkResult()[0], True)

        ck2 = ArgsChecker(self.args)
        toies_count = ck2.addNumerChecker(name="toies_count", range=(0, None), is_req=False)
        self.assertEquals(toies_count, None)
        self.assertEquals(ck2.checkResult()[0], True)

        ck3 = ArgsChecker(self.args)
        skills_count = ck3.addNumerChecker(name="skills_count", range=(0, None), is_req=True)
        self.assertEquals(skills_count, None)
        self.assertEquals(ck3.checkResult()[0], False)

        self.args["skills_count"] = -1
        ck4 = ArgsChecker(self.args)
        skills_count = ck4.addNumerChecker(name="skills_count", range=(0, None), is_req=True)
        self.assertEquals(skills_count, None)
        self.assertEquals(ck4.checkResult()[0], False)

        self.args["skills_count"] = 8
        ck4 = ArgsChecker(self.args)
        skills_count = ck4.addNumerChecker(name="skills_count", range=(0, None), is_req=True)
        self.assertEquals(skills_count, 8)
        self.assertEquals(ck4.checkResult()[0], True)

        self.args["skills_count"] = 8
        ck4 = ArgsChecker(self.args)
        skills_count = ck4.addNumerChecker(name="skills_count", range=(0, 7), is_req=True)
        self.assertEquals(skills_count, None)
        self.assertEquals(ck4.checkResult()[0], False)
    def test_StringChecker(self):
        ck1 = ArgsChecker(self.args)
        name = ck1.addStringChecker(name="name", is_req=True)
        self.assertEquals(name, "lucy")
        self.assertEquals(ck1.checkResult()[0], True)

        ck2 = ArgsChecker(self.args)
        hobby = ck2.addStringChecker(name="hobby", is_req=False)
        self.assertEquals(hobby, None)
        self.assertEquals(ck2.checkResult()[0], True)

        ck3 = ArgsChecker(self.args)
        hobby = ck3.addStringChecker(name="hobby", is_req=True)
        self.assertEquals(hobby, None)
        self.assertEquals(ck3.checkResult()[0], False)

        ck3 = ArgsChecker(self.args)
        father = ck3.addStringChecker(name="father", is_req=True)
        self.assertEquals(father, None)
        self.assertEquals(ck3.checkResult()[0], False)

        self.args["father"] = "PatchLion"
        ck4 = ArgsChecker(self.args)
        father = ck4.addStringChecker(name="father", is_req=True)
        self.assertEquals(father, "PatchLion")
        self.assertEquals(ck4.checkResult()[0], True)

        self.args["mother"] = "WuYueWuXue"
        ck5 = ArgsChecker(self.args)
        mother = ck5.addStringChecker(name="mother", is_req=True)
        self.assertEquals(mother, "WuYueWuXue")
        self.assertEquals(ck5.checkResult()[0], True)

        ck6 = ArgsChecker(self.args)
        toy = ck6.addStringChecker(name="toy", is_req=False)
        self.assertEquals(toy, None)
        self.assertEquals(ck6.checkResult()[0], True)