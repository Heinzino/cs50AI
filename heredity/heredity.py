import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]

def joint_probability(people:dict, one_gene:set, two_genes:set, have_trait:set) -> float:
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    total_joint_probability = 1
    joint_prob_query_dict = make_joint_probability_query_dict(people,one_gene,two_genes,have_trait)

    for person in people.keys():
        person_has_no_parents = people[person]["mother"] == None and people[person]["father"] == None
        person_num_genes = joint_prob_query_dict[person][0]
        person_has_trait = joint_prob_query_dict[person][1]

        joint_probability_has_trait = PROBS["trait"][person_num_genes][person_has_trait]

        if person_has_no_parents:
            joint_probability_has_gene = PROBS["gene"][person_num_genes]
        else:
            joint_probability_has_gene = calculate_joint_prob_has_gene_with_parents(person,people,joint_prob_query_dict)
        
        joint_probability_for_person = (joint_probability_has_trait*joint_probability_has_gene)
        total_joint_probability *= joint_probability_for_person

    return total_joint_probability

def make_joint_probability_query_dict(people:dict,one_gene:set,two_genes:set,have_trait:set) -> dict:
    """
    Returns easier to work with dictionary that works like this
    {person : [numGenes, hasTrait] }
    Ex.
    {James : [2,True]}; James is getting queried for having 2 genes and showing the trait
    """
    joint_probability_people_query_dictionary = {person : [0,True] for person in people}
    geneIndex = 0
    traitIndex = 1

    for person in people.keys():
        if person in one_gene:
            joint_probability_people_query_dictionary[person][geneIndex] = 1
        elif person in two_genes:
            joint_probability_people_query_dictionary[person][geneIndex] = 2
        elif person not in one_gene and person not in two_genes:
            joint_probability_people_query_dictionary[person][geneIndex] = 0

        if person in have_trait:
            joint_probability_people_query_dictionary[person][traitIndex] = True
        else:
            joint_probability_people_query_dictionary[person][traitIndex] = False

    return joint_probability_people_query_dictionary

def NOT(probability):
    return (1 - probability)

def probability_parent_passes_a_gene(parent_num_genes:int):
    """
    Returns probability parents passes ONE gene
    """

    if parent_num_genes == 0:
        return PROBS["mutation"]
    elif parent_num_genes == 2:
        return NOT(PROBS["mutation"])
    elif parent_num_genes == 1:
        #50% chance to choose wrong gene and mutate OR 50% chance to choose right gene and not mutate -> simplifies to just 0.5
        return 0.5


def calculate_joint_prob_has_gene_with_parents(person:str,people:dict,joint_prob_query_dict:dict) -> float:
    """
    Returns joint probability that the person with parents has the specified num of genes
    """
    person_num_genes = joint_prob_query_dict[person][0]
    mother_num_genes = joint_prob_query_dict[people[person]["mother"]][0] 
    father_num_genes = joint_prob_query_dict[people[person]["father"]][0]

    if person_num_genes == 0:
        #Probability I don't get any genes from mom and dad
        return NOT(probability_parent_passes_a_gene(mother_num_genes)) * NOT(probability_parent_passes_a_gene(father_num_genes))
    elif person_num_genes == 1:
        #Probability I get one gene from mom and not dad OR one gene from dad and not mom
        return ( (probability_parent_passes_a_gene(mother_num_genes)*NOT(probability_parent_passes_a_gene(father_num_genes)))
                + (probability_parent_passes_a_gene(father_num_genes)*NOT(probability_parent_passes_a_gene(mother_num_genes))) )
    else:
        #Probability I get one gene from mom and one gene from dad
        return probability_parent_passes_a_gene(mother_num_genes) * probability_parent_passes_a_gene(father_num_genes)
    


def update(probabilities:dict, one_gene:set, two_genes:set, have_trait:set, p:float) -> None:
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    joint_prob_query_dict = make_joint_probability_query_dict(probabilities,one_gene,two_genes,have_trait)

    for person,data in probabilities.items():
        person_num_genes = joint_prob_query_dict[person][0]
        person_has_trait = joint_prob_query_dict[person][1]

        data["gene"][person_num_genes] += p
        data["trait"][person_has_trait] += p


def normalize(probabilities:dict) -> None:
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    #Ratio idea 0.3 : 0.1 would be 0.3 / (0.3+0.1) = 0.75:0.25, extend with multiplie porportion
    #Update Gene Probability Distribution
    for person,data in probabilities.items():

        total_proportions_genes = sum(data["gene"].values())
        for gene in data["gene"].keys():
            data["gene"][gene] = data["gene"][gene] / total_proportions_genes

        total_proportions_trait = sum(data["trait"].values())
        for trait in data["trait"].keys():
            data["trait"][trait] = data["trait"][trait] / total_proportions_trait



if __name__ == "__main__":
    main()
