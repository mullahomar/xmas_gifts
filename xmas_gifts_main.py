import pandas as pd
import numpy as np

_marriages = {
    'Carl': 'John',
    'John': 'Carl',
    'Steve': 'Beth',
    'Beth': 'Steve',
    'Gardner': 'Martha',
    'Martha': 'Gardner'
}


def generate_relationships(marriages):
    relationships = pd.DataFrame(index=marriages.keys(), columns=marriages.keys())
    for p in relationships.index:
        relationships.loc[p, p] = 0
        relationships.loc[p, marriages[p]] = 0
        relationships.loc[marriages[p], p] = 0

    relationships = relationships.fillna(1)

    return relationships


def generate_gifts(relationships):
    gifts = pd.DataFrame(index=relationships.index, columns=relationships.columns).fillna(0)
    relationships_remaining = relationships.copy(deep=True)

    while gifts.sum().sum() < len(gifts.columns):
        gifts_assigned = gifts.sum()
        gifts_unassigned = gifts_assigned[gifts_assigned != 1].index
        recipient = gifts_unassigned[int(np.random.rand() * len(gifts_unassigned))]

        avail_givers = relationships_remaining.loc[:, recipient]
        avail_givers = avail_givers[avail_givers == 1].index

        if len(avail_givers) > 0:
            giver = avail_givers[int(np.random.rand() * len(avail_givers))]

            gifts.loc[giver, recipient] = 1
            gifts.loc[gifts.index != giver, recipient] = 0
            gifts.loc[giver, gifts.columns != recipient] = 0

            relationships_remaining.loc[relationships_remaining.index == giver, :] = 0

        else:
            print('Corner case reached! Trying again.')
            return False, False

    return gifts, True


def check_gifts(gifts, marriages):
    for giver in gifts.columns:
        recipients = gifts.loc[gifts.index == giver, :]
        recipients = recipients[recipients == 1].index
        for recipient in recipients:
            if marriages[giver] == recipient:
                raise ValueError('{0} cannot give a gift to {1}!'.format(giver, recipient))

    pass


def print_gifts(gifts):
    for giver in gifts.columns:
        recipients = gifts.loc[:, giver]
        recipients = recipients[recipients == 1].index
        for recipient in recipients:
            print('{0} gives to {1}\n'.format(giver, recipient))


def xmas_gifts_main(marriages, max_iter=1000):
    relationships = generate_relationships(marriages)

    feasible_solution = False
    i = 0
    while not feasible_solution and i < max_iter:
        gifts, feasible_solution = generate_gifts(relationships)
        i += 1

    check_gifts(gifts, marriages)
    print_gifts(gifts)


if __name__ == '__main__':
    xmas_gifts_main(_marriages)

marriages = _marriages