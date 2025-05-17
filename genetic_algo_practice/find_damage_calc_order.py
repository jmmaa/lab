from __future__ import annotations
import random
import typing as t

CDMG_MULTI = b"0000"
ELEM_MULTI = b"0001"
SKILL_MULTI = b"0010"
UNSHT_MULTI = b"0011"
STAB = b"0100"
PRORATE = b"0101"
SKILL_REL_MULTI = b"0110"
RANGE_DMG_MULTI = b"0111"
LETHARGY = b"1000"
LAST_DMG_MULTI = b"1001"
COMBO_REL_MULTI = b"1010"
GEM_REDUC = b"1011"
GUARD_REDUC = b"1100"
ULTIMA_MULTI = b"1101"


NUM_OF_MULTIPLIERS = 14
BIT_SIZE_PER_MULTIPLIER = 4

PARAMETERS: dict[
    t.Literal[
        # flat
        "BASE_DAMAGE",
        "BASE_DEFENSE",
        "CONSTANT",
        "FLAT_UNSHT",
        # multipliers
        "CDMG_MULTI",
        "ELEM_MULTI",
        "SKILL_MULTI",
        "UNSHT_MULTI",
        "STAB",
        "PRORATE",
        "SKILL_REL_MULTI",
        "RANGE_DMG_MULTI",
        "LETHARGY",
        "LAST_DMG_MULTI",
        "COMBO_REL_MULTI",
        "GEM_REDUC",
        "GUARD_REDUC",
        "ULTIMA_MULTI",
        "FINAL_DAMAGE",
    ],
    float,
]


GENE_TO_MULTI_IDENT_MAPPING: dict[
    bytes,
    t.Literal[
        # flat
        "BASE_DAMAGE",
        "BASE_DEFENSE",
        "CONSTANT",
        "FLAT_UNSHT",
        # multipliers
        "CDMG_MULTI",
        "ELEM_MULTI",
        "SKILL_MULTI",
        "UNSHT_MULTI",
        "STAB",
        "PRORATE",
        "SKILL_REL_MULTI",
        "RANGE_DMG_MULTI",
        "LETHARGY",
        "LAST_DMG_MULTI",
        "COMBO_REL_MULTI",
        "GEM_REDUC",
        "GUARD_REDUC",
        "ULTIMA_MULTI",
        "FINAL_DAMAGE",
    ],
] = {
    CDMG_MULTI: "CDMG_MULTI",
    ELEM_MULTI: "ELEM_MULTI",
    SKILL_MULTI: "SKILL_MULTI",
    UNSHT_MULTI: "UNSHT_MULTI",
    STAB: "STAB",
    PRORATE: "PRORATE",
    SKILL_REL_MULTI: "SKILL_REL_MULTI",
    RANGE_DMG_MULTI: "RANGE_DMG_MULTI",
    LETHARGY: "LETHARGY",
    LAST_DMG_MULTI: "LAST_DMG_MULTI",
    COMBO_REL_MULTI: "COMBO_REL_MULTI",
    GEM_REDUC: "GEM_REDUC",
    GUARD_REDUC: "GUARD_REDUC",
    ULTIMA_MULTI: "ULTIMA_MULTI",
}

MULTI_IDENT_LIST = [
    CDMG_MULTI,
    ELEM_MULTI,
    SKILL_MULTI,
    UNSHT_MULTI,
    STAB,
    PRORATE,
    SKILL_REL_MULTI,
    RANGE_DMG_MULTI,
    LETHARGY,
    LAST_DMG_MULTI,
    COMBO_REL_MULTI,
    GEM_REDUC,
    GUARD_REDUC,
    ULTIMA_MULTI,
]


def parse_gene_to_multiplier_identifier(
    gene: bytes,
) -> t.Literal[
    # flat
    "BASE_DAMAGE",
    "BASE_DEFENSE",
    "CONSTANT",
    "FLAT_UNSHT",
    # multipliers
    "CDMG_MULTI",
    "ELEM_MULTI",
    "SKILL_MULTI",
    "UNSHT_MULTI",
    "STAB",
    "PRORATE",
    "SKILL_REL_MULTI",
    "RANGE_DMG_MULTI",
    "LETHARGY",
    "LAST_DMG_MULTI",
    "COMBO_REL_MULTI",
    "GEM_REDUC",
    "GUARD_REDUC",
    "ULTIMA_MULTI",
    "FINAL_DAMAGE",
]:
    return GENE_TO_MULTI_IDENT_MAPPING[gene]


# def parse_genome_to_damage_order(genome: bytes) -> list[str]:
#     order = []

#     num_of_multi_ident = 14
#     start = 0
#     stop = 4
#     for _ in range(1, num_of_multi_ident + 1):
#         gene = genome[start:stop]
#         order.append(parse_gene_to_multiplier_identifier(gene))

#         start += 4
#         stop += 4


#     return order
def parse_genome_to_genes(genome: bytes) -> list[bytes]:
    order = []

    start = 0
    stop = BIT_SIZE_PER_MULTIPLIER
    for _ in range(1, NUM_OF_MULTIPLIERS + 1):
        gene = genome[start:stop]
        order.append(gene)

        start += BIT_SIZE_PER_MULTIPLIER
        stop += BIT_SIZE_PER_MULTIPLIER

    return order


def create_genomes(n: int) -> list[bytes]:
    solutions = []
    for _ in range(1, n):
        random.shuffle(MULTI_IDENT_LIST)

        solutions.append(b"".join(MULTI_IDENT_LIST))

    return solutions


# def calculate_based_on_genome(genome: bytes):

#     for gene in genome


def fit(
    genome: bytes,
    params: dict[
        t.Literal[
            # base
            "BASE_DAMAGE",
            "BASE_DEFENSE",
            "CONSTANT",
            "FLAT_UNSHT",
            # multipliers
            "CDMG_MULTI",
            "ELEM_MULTI",
            "SKILL_MULTI",
            "UNSHT_MULTI",
            "STAB",
            "PRORATE",
            "SKILL_REL_MULTI",
            "RANGE_DMG_MULTI",
            "LETHARGY",
            "LAST_DMG_MULTI",
            "COMBO_REL_MULTI",
            "GEM_REDUC",
            "GUARD_REDUC",
            "ULTIMA_MULTI",
            "FINAL_DAMAGE",
        ],
        float,
    ],
):
    genes = parse_genome_to_genes(genome)

    result = (
        params["BASE_DAMAGE"]
        - params["BASE_DEFENSE"]
        + params["CONSTANT"]
        + params["FLAT_UNSHT"]
    )

    for gene in genes:
        identifier = parse_gene_to_multiplier_identifier(gene)

        parameter = params[identifier] / 100

        result *= parameter

        result = int(result)

    score = abs(result - params["FINAL_DAMAGE"])

    return score


def find_best_genomes(
    genomes: list[bytes],
    params: dict[
        t.Literal[
            # base
            "BASE_DAMAGE",
            "BASE_DEFENSE",
            "CONSTANT",
            "FLAT_UNSHT",
            # multipliers
            "CDMG_MULTI",
            "ELEM_MULTI",
            "SKILL_MULTI",
            "UNSHT_MULTI",
            "STAB",
            "PRORATE",
            "SKILL_REL_MULTI",
            "RANGE_DMG_MULTI",
            "LETHARGY",
            "LAST_DMG_MULTI",
            "COMBO_REL_MULTI",
            "GEM_REDUC",
            "GUARD_REDUC",
            "ULTIMA_MULTI",
            "FINAL_DAMAGE",
        ],
        float,
    ],
):
    return sorted(
        genomes,
        key=lambda genome: fit(genome, params),
    )[0:10]


def mutate_genomes(genomes: list[bytes]) -> list[bytes]:
    mutated_genomes = []
    for genome in genomes:
        # split the genome to half

        left_slice_idx = (NUM_OF_MULTIPLIERS // 2) * 4
        right_slice_idx = (NUM_OF_MULTIPLIERS // 2) * 4

        left_slice_genome = genome[:left_slice_idx]
        right_slice_genome = genome[right_slice_idx:]

        randomizer_num_for_choosing_the_half_to_mutate = random.randint(1, 2)

        start = 0
        stop = BIT_SIZE_PER_MULTIPLIER
        if randomizer_num_for_choosing_the_half_to_mutate == 1:
            genome_to_mutate = left_slice_genome

        else:
            genome_to_mutate = right_slice_genome

        genes = []
        for _ in range(1, (NUM_OF_MULTIPLIERS // 2) + 1):
            genes.append(genome_to_mutate[start:stop])  # pyright: ignore

            start += BIT_SIZE_PER_MULTIPLIER
            stop += BIT_SIZE_PER_MULTIPLIER

        random.shuffle(genes)

        new_mutated_genome_slice = b"".join(genes)

        if randomizer_num_for_choosing_the_half_to_mutate == 1:
            mutated_genomes.append(
                b"".join([new_mutated_genome_slice, right_slice_genome])
            )

        else:
            mutated_genomes.append(
                b"".join([new_mutated_genome_slice, left_slice_genome])
            )

    return mutated_genomes


def shift_list(my_list, shift_by):
    return my_list[shift_by:] + my_list[:shift_by]


def create_inherited_genomes(
    genomes_to_inherit_from: list[bytes], n: int
) -> list[bytes]:
    new_genomes = []

    for _ in range(1, n + 1):
        randomizer = random.randint(1, 5)
        shift_num = random.choice([-1, 1])

        if randomizer <= 2:
            target_genome = genomes_to_inherit_from[0]

            new_genome = b"".join(
                shift_list(parse_genome_to_genes(target_genome), shift_num)
            )
            new_genomes.append(new_genome)

        elif randomizer >= 3 and randomizer <= 4:
            target_genome = genomes_to_inherit_from[
                random.randint(0, len(genomes_to_inherit_from) - 1)
            ]

            new_genome = b"".join(
                shift_list(parse_genome_to_genes(target_genome), shift_num)
            )
            new_genomes.append(new_genome)

        else:
            target_genome = genomes_to_inherit_from[-1]

            new_genome = b"".join(
                shift_list(parse_genome_to_genes(target_genome), shift_num)
            )
            new_genomes.append(new_genome)

    return new_genomes


def parse_genome_to_damage_order(genome: bytes) -> str:
    genes = parse_genome_to_genes(genome)

    return " -> ".join([parse_gene_to_multiplier_identifier(gene) for gene in genes])


if __name__ == "__main__":
    genomes = create_genomes(100)

    params = {
        "BASE_DAMAGE": 6350.0,
        "BASE_DEFENSE": 40.0,
        "CONSTANT": 600.0,
        "FLAT_UNSHT": 0.0,
        "CDMG_MULTI": 321.0,
        "ELEM_MULTI": 100.0,
        "SKILL_MULTI": 1350.0,
        "UNSHT_MULTI": 100.0,
        "STAB": 100.0,
        "PRORATE": 250.0,
        "SKILL_REL_MULTI": 100.0,
        "RANGE_DMG_MULTI": 135.0,
        "LETHARGY": 100.0,
        "LAST_DMG_MULTI": 140.0,
        "COMBO_REL_MULTI": 110.0,
        "GEM_REDUC": 100.0,
        "GUARD_REDUC": 100.0,
        "ULTIMA_MULTI": 100.0,
        # final damage
        "FINAL_DAMAGE": 1556354.0,
    }

    best_genomes = find_best_genomes(
        genomes,
        params,  # pyright: ignore
    )
    # print(best_genomes)
    gen_counts = 0

    print(
        f"== GEN {gen_counts} ==\norder: {parse_genome_to_damage_order(best_genomes[0])}\nscore: {fit(best_genomes[0], params)}"  # pyright:ignore
    )

    while fit(best_genomes[0], params) != 0:  # pyright: ignore
        mutated_genomes = mutate_genomes(best_genomes)
        new_genomes = create_inherited_genomes(mutated_genomes, 100)

        best_genomes = new_genomes

        print(
            f"== GEN {gen_counts} ==\norder: {parse_genome_to_damage_order(best_genomes[0])}\nscore: {fit(best_genomes[0], params)}"  # pyright:ignore
        )

        gen_counts += 1
    print(best_genomes[0])
    print(parse_genome_to_damage_order(best_genomes[0]))
    print(fit(best_genomes[0], params))  # pyright: ignore
