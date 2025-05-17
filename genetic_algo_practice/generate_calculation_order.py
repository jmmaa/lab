from __future__ import annotations
import random

import typing as t


T = t.TypeVar("T")


def create_random_order(list_: list[T]):
    random.shuffle(list_)

    return list_


def create_random_orders(list_: list[T], n: int):
    results = []

    for _ in range(n):
        results.append(create_random_order(list_))

    return results


class Parameters(t.TypedDict):
    """
    ```py
    critical_damage_multiplier: int
    ```
    total critical damage to be used for fitting. Defaults to 100 (100%)
    """

    base_damage: int
    base_defense: int
    constant: int
    unsheathe_attack_flat: int
    target_damage: int

    damage_multipliers: dict[
        t.Literal[
            "CRITICAL_DAMAGE",
            "ELEMENTAL_BOOST",
            "SKILL",
            "UNSHEATHE_ATTACK",
            "STABILITY",
            "PRORATION",
            "SKILL_RELATED",
            "RANGE_RELATED",
            "IS_AFFECTED_BY_LETHARGY",
            "LAST_DAMAGE",
            "COMBO_RELATED",
            "GEM_RELATED_DAMAGE_REDUCTION",
            "IS_AFFECTED_BY_GUARD",
            "ULTIMA_LION_RAGE",
        ],
        int,
    ]


def fit_damage_calc_order(
    multiplier_list: list[
        t.Literal[
            "CRITICAL_DAMAGE",
            "ELEMENTAL_BOOST",
            "SKILL",
            "UNSHEATHE_ATTACK",
            "STABILITY",
            "PRORATION",
            "SKILL_RELATED",
            "RANGE_RELATED",
            "IS_AFFECTED_BY_LETHARGY",
            "LAST_DAMAGE",
            "COMBO_RELATED",
            "GEM_RELATED_DAMAGE_REDUCTION",
            "IS_AFFECTED_BY_GUARD",
            "ULTIMA_LION_RAGE",
        ]
    ],
    parameters: Parameters,
):
    damage_multipliers = parameters["damage_multipliers"]

    result = (
        parameters["base_damage"]
        - parameters["base_defense"]
        + parameters["constant"]
        + parameters["unsheathe_attack_flat"]
    )

    for key in multiplier_list:
        result *= damage_multipliers[key] / 100
        result = int(result)

    # getting fitness score

    fitness_score = abs(result - parameters["target_damage"])
    return fitness_score


def find_best_damage_calc_orders(
    damage_calc_orders: list[
        list[
            t.Literal[
                "CRITICAL_DAMAGE",
                "ELEMENTAL_BOOST",
                "SKILL",
                "UNSHEATHE_ATTACK",
                "STABILITY",
                "PRORATION",
                "SKILL_RELATED",
                "RANGE_RELATED",
                "IS_AFFECTED_BY_LETHARGY",
                "LAST_DAMAGE",
                "COMBO_RELATED",
                "GEM_RELATED_DAMAGE_REDUCTION",
                "IS_AFFECTED_BY_GUARD",
                "ULTIMA_LION_RAGE",
            ]
        ]
    ],
    n: int,
    parameters: Parameters,
):
    return sorted(
        damage_calc_orders,
        key=lambda list_: fit_damage_calc_order(list_, parameters),
    )[0:n]


def mutate_damage_calc_order(
    damage_calc_order: list[
        t.Literal[
            "CRITICAL_DAMAGE",
            "ELEMENTAL_BOOST",
            "SKILL",
            "UNSHEATHE_ATTACK",
            "STABILITY",
            "PRORATION",
            "SKILL_RELATED",
            "RANGE_RELATED",
            "IS_AFFECTED_BY_LETHARGY",
            "LAST_DAMAGE",
            "COMBO_RELATED",
            "GEM_RELATED_DAMAGE_REDUCTION",
            "IS_AFFECTED_BY_GUARD",
            "ULTIMA_LION_RAGE",
        ]
    ],
):
    randomizer_a = random.randint(0, len(damage_calc_order) - 1)
    randomizer_b = random.randint(0, len(damage_calc_order) - 1)

    # switch

    damage_calc_order[randomizer_a], damage_calc_order[randomizer_b] = (
        damage_calc_order[randomizer_b],
        damage_calc_order[randomizer_a],
    )

    return damage_calc_order


def mutate_damage_calc_orders(
    damage_calc_orders: list[
        list[
            t.Literal[
                "CRITICAL_DAMAGE",
                "ELEMENTAL_BOOST",
                "SKILL",
                "UNSHEATHE_ATTACK",
                "STABILITY",
                "PRORATION",
                "SKILL_RELATED",
                "RANGE_RELATED",
                "IS_AFFECTED_BY_LETHARGY",
                "LAST_DAMAGE",
                "COMBO_RELATED",
                "GEM_RELATED_DAMAGE_REDUCTION",
                "IS_AFFECTED_BY_GUARD",
                "ULTIMA_LION_RAGE",
            ]
        ]
    ],
):
    # mutation function, just switches places with some elements

    new_damage_calc_orders = []

    for damage_calc_order in damage_calc_orders:
        new_damage_calc_orders.append(mutate_damage_calc_order(damage_calc_order))

    return new_damage_calc_orders


def generate_damage_calc_orders_from_previous_gen(
    damage_calc_orders: list[
        list[
            t.Literal[
                "CRITICAL_DAMAGE",
                "ELEMENTAL_BOOST",
                "SKILL",
                "UNSHEATHE_ATTACK",
                "STABILITY",
                "PRORATION",
                "SKILL_RELATED",
                "RANGE_RELATED",
                "IS_AFFECTED_BY_LETHARGY",
                "LAST_DAMAGE",
                "COMBO_RELATED",
                "GEM_RELATED_DAMAGE_REDUCTION",
                "IS_AFFECTED_BY_GUARD",
                "ULTIMA_LION_RAGE",
            ]
        ]
    ],
    n: int,
):
    new_damage_calc_orders = []

    for _ in range(n):
        randomizer = random.randint(0, len(damage_calc_orders) - 1)
        new_damage_calc_order = mutate_damage_calc_order(damage_calc_orders[randomizer])
        new_damage_calc_orders.append(new_damage_calc_order)

    return new_damage_calc_orders


def print_step(gen_count: int, best_order: list, score: int):
    print(
        f"== generation {gen_count} ==\nbest: {' -> '.join(best_order)}\nscore: {score}"
    )


def find_damage_calc_order(parameters: Parameters):
    current_damage_calc_orders = create_random_orders(
        list(parameters["damage_multipliers"].keys()),
        1000,
    )

    generation_counts = 0

    while fit_damage_calc_order(current_damage_calc_orders[0], parameters) != 0:
        current_best_damage_calc_orders = find_best_damage_calc_orders(
            current_damage_calc_orders, 3, parameters
        )
        current_mutated_damage_calc_orders = mutate_damage_calc_orders(
            current_best_damage_calc_orders
        )

        current_damage_calc_orders = generate_damage_calc_orders_from_previous_gen(
            current_mutated_damage_calc_orders, 1000
        )

        print_step(
            generation_counts,
            current_damage_calc_orders[0],
            fit_damage_calc_order(current_damage_calc_orders[0], parameters),
        )

        generation_counts += 1

    return current_damage_calc_orders[0]


if __name__ == "__main__":
    print(
        find_damage_calc_order(
            {
                "base_damage": 6350,
                "base_defense": 40,
                "constant": 600,
                "target_damage": 1063483,
                "unsheathe_attack_flat": 0,
                "damage_multipliers": {
                    "CRITICAL_DAMAGE": 321,
                    "SKILL": 1500,
                    "COMBO_RELATED": 110,
                    "PRORATION": 250,
                    "RANGE_RELATED": 135,
                    "LAST_DAMAGE": 140,
                    "ELEMENTAL_BOOST": 123,
                    "STABILITY": 50,
                },
            }
        )
    )
