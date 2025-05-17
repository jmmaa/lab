from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Skill:
    name: str
    level: int


depth = 0


@dataclass
class SkillNode:
    skill: Skill
    parent: SkillNode | None
    children: list[SkillNode]

    def add_skill_node(self, node: SkillNode):
        node.parent = self
        self.children.append(node)

    def get_level(self):
        depth = 0

        curr = self.parent
        while curr is not None:
            depth += 1
            curr = curr.parent

        return depth

    def __str__(self) -> str:
        tabs = self.get_level() * "\t" + "\t"

        children = "".join([tabs + str(edge) for edge in self.children])

        return f"{self.skill.name} lv{self.skill.level}\n{children}"

    def set_skill_point(self, n: int):
        # for removing sp on connected skills
        self.skill.level = n
        if self.skill.level < 5:
            queued = []

            for child in self.children:
                queued.append(child)

            while len(queued) != 0:
                child = queued.pop(0)

                child.set_skill_point(0)

        curr = self.parent
        while curr is not None:
            if curr.skill.level < 5:
                curr.skill.level = 5
            curr = curr.parent
        self.skill.level = n

    def get_all_skills(self):
        # BFS algorithm

        visited = []
        queued = []

        curr = self
        visited.append(curr)
        queued.append(curr)

        while len(queued) != 0:
            curr = queued.pop(0)

            for child in curr.children:
                visited.append(child)
                queued.append(child)

        return visited

    def set_skill_point_to_skill(self, name: str, n: int):
        # BFS algorithm

        queued = []

        curr = self
        # visited.append(curr)
        queued.append(curr)

        while len(queued) != 0:
            curr = queued.pop(0)
            if curr.skill.name == name:
                curr.set_skill_point(n)
            else:
                for child in curr.children:
                    # visited.append(child)
                    queued.append(child)


root = SkillNode(Skill("bash", 0), None, [])

parent1 = SkillNode(Skill("blade sting", 0), None, [])
parent1.add_skill_node(SkillNode(Skill("condemn", 0), None, []))
parent1.add_skill_node(SkillNode(Skill("air assault", 0), None, []))

parent2 = SkillNode(Skill("slaying slash", 0), None, [])
parent2.add_skill_node(SkillNode(Skill("multiple thrust", 0), None, []))
parent2.add_skill_node(SkillNode(Skill("death wish", 0), None, []))


parent3 = SkillNode(Skill("cutthroat", 0), None, [])
parent3.add_skill_node(SkillNode(Skill("blink", 0), None, []))
parent3.add_skill_node(SkillNode(Skill("flying slash", 0), None, []))

parent2.add_skill_node(parent3)

root.add_skill_node(parent1)
root.add_skill_node(parent2)


# sample = SkillNode(
#     Skill("hard_hit", 5),
#     None,
#     [
#         SkillNode(Skill("sonic_blade", 5), None, []),
#         SkillNode(Skill("astute", 5), None, []),
#     ],
# )


# print(root)
# root.set_skill_point_to_skill("flying slash", 10)
# print(root)
# root.set_skill_point_to_skill("air assault", 2)
# print(root)
# root.set_skill_point_to_skill("condemn", 2)
# print(root)
# root.set_skill_point_to_skill("bash", 4)
# print(root)
# # for n, skill in enumerate(root.get_all_skills()):
# #     print(n, skill)


# # ADD SUBTRACT SKILL POINT


# skill_tree =


while True:
    print(root)
    inp = input("Enter the Skill and SP to spend: <name> <sp spent>")

    name, sp = inp.split(",")

    root.set_skill_point_to_skill(name, int(sp))
